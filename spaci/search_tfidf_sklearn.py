from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Part 1 & 2: Indexing
def build_index(docs: list[str]):
    # TfidfVectorizer automatically handles lowercasing, tokenization, TF, and IDF.
    vectorizer = TfidfVectorizer()

    # fit_transform: "Learns" vocabulary (IDF) from docs and transforms docs into a TF-IDF matrix
    tfidf_docs = vectorizer.fit_transform(docs)

    # Return both the vectorizer (which contains the IDF dictionary) and the document matrix
    return vectorizer, tfidf_docs


# Part 3: Search
def search(
    query: str, vectorizer: TfidfVectorizer, tfidf_docs, original_docs: list[str]
):
    # 1. Convert query to a vector based on the learned vocabulary (automatically ignores new words)
    query_vector = vectorizer.transform([query])

    # 2. Calculate Cosine Similarity between the query and ALL docs simultaneously
    # The result is a 2D array, use flatten() to convert it into a 1D array
    scores = cosine_similarity(query_vector, tfidf_docs).flatten()

    # 3. Filter results with score > 0 and sort
    results = [
        (score, original_docs[idx]) for idx, score in enumerate(scores) if score > 0
    ]
    results.sort(key=lambda x: x[0], reverse=True)
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
vectorizer, tfidf_docs = build_index(documents)

## Search - Run many
queries = [
    "python backend",
    "machine learning with python",
    "how to use kubernetes",
    "golang API",  # Not included in DB
]
for q in queries:
    print(f"Query: '{q}'")
    results = search(q, vectorizer, tfidf_docs, documents)
    if not results:
        print("  -> Not found.")
    else:
        for score, doc in results:
            print(f"  Score: {score:.2f}: {doc}")
        print()
