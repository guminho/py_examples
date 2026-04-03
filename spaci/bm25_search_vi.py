# Install: pip install bm25s pyvi
import os
import warnings

# Broadly suppress all warnings (e.g. numpy VisibleDeprecationWarning and SyntaxWarnings compilation errors)
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import bm25s  # noqa: E402
from pyvi import ViTokenizer  # noqa: E402


def vietnamese_tokenizer(texts: list[str]):
    """
    Custom Tokenizer for Vietnamese using pyvi.
    """
    tokenized_docs = []
    for text in texts:
        # pyvi will transform: "ngân hàng số" -> "ngân_hàng số"
        segmented_text = ViTokenizer.tokenize(text)

        # Then split by space and convert to lowercase
        tokens = segmented_text.lower().split()
        tokenized_docs.append(tokens)
    return tokenized_docs


# Part 1 & 2: Indexing
def build_index(docs: list[str]):
    # Tokenize using custom Vietnamese tokenizer
    corpus_tokens = vietnamese_tokenizer(docs)

    # Indexing (In-memory)
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    return retriever


# Part 3: Search
def search(query: str, retriever: bm25s.BM25, original_docs: list[str]):
    # Tokenize the query
    query_tokens = vietnamese_tokenizer([query])

    # Get results for all documents
    docs, scores = retriever.retrieve(
        query_tokens, corpus=original_docs, k=len(original_docs)
    )

    # The result is a 2D array, use [0] to get the list of results for the first (and only) query
    # Filter results with score > 0
    results = [(score, doc) for doc, score in zip(docs[0], scores[0]) if score > 0]
    return results


# Part 4: Run
documents = [
    "Python là một ngôn ngữ tuyệt vời cho lập trình backend.",
    "Tôi sử dụng Python để phát triển các mô hình học máy theo hướng dẫn.",
    "Lập trình backend là một công việc rất thú vị và nhiều thách thức.",
    "Kubernetes được sử dụng để điều phối và quản lý các công nghệ container.",
    "FastAPI là một web framework hiện đại giúp xây dựng các hệ thống API bằng Python.",
]

## Indexing - Run once
retriever = build_index(documents)

## Search - Run many
queries = [
    "lập trình backend",
    "học máy với python",
    "cách quản lý container kubernetes",
    "golang API",  # Not included in DB
]
for q in queries:
    print(f"Query: '{q}'")
    results = search(q, retriever, documents)
    if not results:
        print("  -> Not found.")
    else:
        for score, doc in results:
            print(f"  Score: {score:.2f}: {doc}")
        print()
