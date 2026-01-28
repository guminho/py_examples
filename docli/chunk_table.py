import math
import re

import tiktoken
from docling_core.transforms.chunker.doc_chunk import DocChunk
from docling_core.transforms.chunker.hierarchical_chunker import (
    ChunkingDocSerializer,
    ChunkingSerializerProvider,
)
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
from docling_core.transforms.serializer.markdown import MarkdownTableSerializer
from docling_core.types.doc.document import TableItem

ROW_RE = re.compile(r"\r|<br\s*/?>")  # sub with SPACE


def chunk_has_table(doc_chunk: DocChunk) -> bool:
    """Check if a doc chunk contains any table items."""
    if not doc_chunk.meta or not doc_chunk.meta.doc_items:
        return False

    return any(isinstance(item, TableItem) for item in doc_chunk.meta.doc_items)


def clean_row(row: str):
    row = ROW_RE.sub(" ", row)
    cells = row.strip()[1:-1].split("|")
    cells = (c.strip() for c in cells)
    return f"| {' | '.join(cells)} |"


def clean_sep(row: str):
    cells = row.strip()[1:-1].split("|")
    cells = ("---" for _ in cells)
    return f"| {' | '.join(cells)} |"


def check_theader(rows: list[str]):
    return "|" in rows[0] and "|" in rows[1] and "---" in rows[1]


def clean_theader(rows: list[str]):
    return f"{clean_row(rows[0])}\n{clean_sep(rows[1])}\n"


class DoclingHybridChunker(HybridChunker):
    def _split_using_plain_text(self, doc_chunk: DocChunk) -> list[DocChunk]:
        lengths = self._doc_chunk_length(doc_chunk)
        if lengths.total_len <= self.max_tokens:
            return [DocChunk(**doc_chunk.export_json_dict())]

        # How much room is there for text after subtracting out the headers and
        # captions:
        available_length = self.max_tokens - lengths.other_len
        if available_length <= 0:
            new_chunk = DocChunk(**doc_chunk.export_json_dict())
            new_chunk.meta.captions = None
            new_chunk.meta.headings = None
            return self._split_using_plain_text(doc_chunk=new_chunk)

        if chunk_has_table(doc_chunk):
            text = doc_chunk.text
            print("@@chunk:", [text])
            lines = text.split("\n")
            header_text = ""
            if check_theader(lines[:2]):
                temp_header_text = clean_theader(lines[:2])
                header_tokens = self._count_text_tokens(temp_header_text)
                if available_length - header_tokens > 0:
                    header_text = temp_header_text
                    available_length -= header_tokens
                    lines = lines[2:]
            rows = [clean_row(x) for x in lines]
            partsize = len(rows) / lengths.total_len * available_length
            partsize = max(2, math.floor(partsize))

            chunks = []
            while rows:
                text = header_text + "\n".join(rows[:partsize])
                chunks.append(DocChunk(text=text, meta=doc_chunk.meta))
                rows = rows[partsize:]
            return chunks

        return super()._split_using_plain_text(doc_chunk)


class MDTableSerializerProvider(ChunkingSerializerProvider):
    def get_serializer(self, doc):
        return ChunkingDocSerializer(
            doc=doc,
            table_serializer=MarkdownTableSerializer(),
        )


def get_table_chunker():
    chunker = DoclingHybridChunker(
        tokenizer=OpenAITokenizer(
            tokenizer=tiktoken.encoding_for_model("gpt-4o"),
            max_tokens=512,
        ),
        serializer_provider=MDTableSerializerProvider(),
    )
    return chunker


def run_chunk(doc, chunker: HybridChunker):
    chunk_iter = chunker.chunk(dl_doc=doc)
    for i, chunk in enumerate(chunk_iter):
        print(f"\n\n=== {i} ===\n\n")
        print(chunk.text)
