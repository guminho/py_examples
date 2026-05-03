from pathlib import Path

import lancedb
from faststream import Context, Logger
from faststream.redis import StreamSub

from worker.broker import broker
from worker.chunker import chunk_markdown
from worker.constants import CONSUMER_NAME, INGEST_GROUP, INGEST_STREAM
from worker.models import IngestMessage
from worker.vectordb import add_chunks, create_fts_index, hash_exists


@broker.subscriber(
    stream=StreamSub(INGEST_STREAM, group=INGEST_GROUP, consumer=CONSUMER_NAME)
)
async def handle_ingest(
    msg: IngestMessage,
    logger: Logger,
    md_chunks_table: lancedb.table.Table = Context(),
):
    # 1. Check duplicate by file hash
    if hash_exists(md_chunks_table, msg.file_hash):
        logger.info(
            f"⏭️  Skipping '{msg.filename}' — hash {msg.file_hash[:12]}... already ingested"
        )
        return

    # 2. Read markdown from disk
    file_path = Path(msg.file_path)
    if not file_path.exists():
        logger.error(f"❌ File not found: {file_path}")
        return

    text = file_path.read_text(encoding="utf-8")
    logger.info(f"📄 Read '{msg.filename}' ({len(text)} chars)")

    # 3. Chunk markdown (2-stage: header split → character split)
    docs = chunk_markdown(text)
    logger.info(f"✂️  Split into {len(docs)} chunks")

    # 4. Insert into LanceDB (embedding is handled automatically by LanceDB + FastEmbed)
    count = add_chunks(md_chunks_table, docs, msg.filename, msg.file_hash)

    # 5. Rebuild FTS index for hybrid search
    create_fts_index(md_chunks_table)

    logger.info(
        f"✅ Ingested {count} chunks for '{msg.filename}' into LanceDB (FTS Index updated)"
    )
