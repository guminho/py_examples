import bm25s
import Stemmer


# Part 1 & 2: Indexing
def build_index(docs: list[str]):
    # Use PyStemmer for extremely fast tokenization
    stemmer = Stemmer.Stemmer("english")
    corpus_tokens = bm25s.tokenize(docs, stemmer=stemmer)

    # Indexing (In-memory)
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    return retriever, stemmer


# Part 3: Search
def search(
    query: str,
    retriever: bm25s.BM25,
    stemmer: Stemmer.Stemmer,
    original_docs: list[str],
):
    query_tokens = bm25s.tokenize([query], stemmer=stemmer)

    # Get results for all documents
    docs, scores = retriever.retrieve(
        query_tokens, corpus=original_docs, k=len(original_docs)
    )

    # The result is a 2D array, use [0] to get the results for the first (and only) query
    # Filter results with score > 0
    results = [(score, doc) for doc, score in zip(docs[0], scores[0]) if score > 0]
    return results


# Part 4: Run
documents = [
    "Python is great for backend development.",
    "I use Python for machine learning.",
    "Backend development is fun.",
    "Kubernetes is used for container orchestration.",
    "FastAPI is a modern web framework for building APIs with Python.",
]

## Indexing - Run once
retriever, stemmer = build_index(documents)

## Search - Run many
queries = [
    "python backend",
    "machine learning with python",
    "how to use kubernetes",
    "golang API",  # Not included in DB
]
for q in queries:
    print(f"Query: '{q}'")
    results = search(q, retriever, stemmer, documents)
    if not results:
        print("  -> Not found.")
    else:
        for score, doc in results:
            print(f"  Score: {score:.2f}: {doc}")
        print()
