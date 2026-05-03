from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

HEADERS_TO_SPLIT = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]

# ~500 tokens chunk_size, ~100 tokens overlap (1 token ≈ 4 chars)
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400


def chunk_markdown(text: str) -> list[Document]:
    """2-stage markdown chunking.

    Stage 1: Split by markdown headers (#, ##, ###) — preserves section hierarchy as metadata.
    Stage 2: Further split large sections by character count to fit embedding model context window.
    """
    # Stage 1: split by headers
    header_splitter = MarkdownHeaderTextSplitter(HEADERS_TO_SPLIT)
    header_docs = header_splitter.split_text(text)

    # Stage 2: split large sections into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return text_splitter.split_documents(header_docs)
