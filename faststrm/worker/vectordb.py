import lancedb
from lancedb.pydantic import LanceModel, Vector

from worker.embeddings import FastEmbedFunc

func = FastEmbedFunc.create()

TABLE_NAME = "md_chunks"
LANCEDB_PATH = "./data/lancedb"


class MdChunk(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()  # 384-dim
    filename: str = ""
    file_hash: str = ""
    h1: str = ""
    h2: str = ""
    h3: str = ""


def connect_db() -> lancedb.DBConnection:
    return lancedb.connect(LANCEDB_PATH)


def get_or_create_table(db: lancedb.DBConnection) -> lancedb.table.Table:
    if TABLE_NAME in db.table_names():
        return db.open_table(TABLE_NAME)
    table = db.create_table(TABLE_NAME, schema=MdChunk)
    # Khởi tạo FTS index ngay khi tạo table
    table.create_fts_index("text", replace=True)
    return table


def create_fts_index(table: lancedb.table.Table):
    """Tạo hoặc cập nhật Full-Text Search index trên cột 'text'."""
    table.create_fts_index("text", replace=True)


def hash_exists(table: lancedb.table.Table, file_hash: str) -> bool:
    results = table.search().where(f"file_hash = '{file_hash}'").limit(1).to_list()
    return len(results) > 0


def add_chunks(
    table: lancedb.table.Table,
    docs: list,
    filename: str,
    file_hash: str,
) -> int:
    """Insert chunked documents into LanceDB. Returns the number of chunks added."""
    records = []
    for doc in docs:
        metadata = doc.metadata
        records.append(
            {
                "text": doc.page_content,
                "filename": filename,
                "file_hash": file_hash,
                "h1": metadata.get("h1", ""),
                "h2": metadata.get("h2", ""),
                "h3": metadata.get("h3", ""),
            }
        )
    table.add(records)
    return len(records)
