import math
from collections import Counter

import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt_tab", quiet=True)
nltk.download("punkt", quiet=True)


# Part 1
def tokenize(text: str):
    return word_tokenize(text.lower())


def compute_tf(tokenized_doc: list[str]):
    word_counts = Counter(tokenized_doc)
    total_words = word_counts.total()
    return {word: count / total_words for word, count in word_counts.items()}


def compute_idf(tokenized_docs: list[list[str]]):
    idf_dict = {}
    N = len(tokenized_docs)
    all_words = set(word for doc in tokenized_docs for word in doc)
    for word in all_words:
        containing_docs = sum(1 for doc in tokenized_docs if word in doc)
        idf_dict[word] = math.log(N / containing_docs)
    return idf_dict


# Part 2
def build_index(docs: list[str]):
    tokenized_docs = [tokenize(doc) for doc in docs]
    idf_dict = compute_idf(tokenized_docs)
    doc_vecs = []
    for doc in tokenized_docs:
        tf = compute_tf(doc)
        tfidf_doc = {word: tf[word] * idf_dict[word] for word in doc}
        doc_vecs.append(tfidf_doc)
    return doc_vecs, idf_dict


# Part 3
def compute_query_tfidf(query: str, idf_dict: dict):
    tokenized_query = tokenize(query)
    tf = compute_tf(tokenized_query)

    tfidf_query = {}
    for word in tokenized_query:
        if word in idf_dict:
            tfidf_query[word] = tf[word] * idf_dict[word]
        else:
            tfidf_query[word] = 0.0
    return tfidf_query


def cosine_similarity(vec1: dict, vec2: dict):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[word] * vec2[word] for word in intersection)

    sum1 = sum(val**2 for val in vec1.values())
    sum2 = sum(val**2 for val in vec2.values())

    if sum1 == 0.0 or sum2 == 0.0:
        return 0.0
    else:
        return numerator / (math.sqrt(sum1) * math.sqrt(sum2))


def search(query: str, tfidf_docs: list, idf_dict: dict, original_docs: list):
    query_vector = compute_query_tfidf(query, idf_dict)
    results = []
    for idx, doc_vector in enumerate(tfidf_docs):
        score = cosine_similarity(query_vector, doc_vector)
        if score > 0:
            results.append((score, original_docs[idx]))

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
tfidf_docs, idf_dict = build_index(documents)

## Search - Run many
queries = [
    "python backend",
    "machine learning with python",
    "how to use kubernetes",
    "golang API",  # Not included in DB
]
for q in queries:
    print(f"Query: '{q}'")
    results = search(q, tfidf_docs, idf_dict, documents)
    if not results:
        print("  -> Not found.")
    else:
        for score, doc in results:
            print(f"  Score: {score:.2f}: {doc}")
        print()
