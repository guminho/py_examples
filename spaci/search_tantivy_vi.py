# Install: pip install tantivy pyvi
import os
import warnings

# Broadly suppress all warnings (e.g. numpy VisibleDeprecationWarning and SyntaxWarnings compilation errors)
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import tantivy  # noqa: E402
from pyvi import ViTokenizer  # noqa: E402


def vietnamese_tokenizer(text: str) -> str:
    """
    Custom Tokenizer for Vietnamese using pyvi.
    Tantivy uses space-based tokenization by default, so we pre-segment words with underscores (e.g. `ngân_hàng`).
    """
    # pyvi will transform: "ngân hàng số" -> "ngân_hàng số"
    segmented_text = ViTokenizer.tokenize(text)

    # Convert to lowercase and return as a single string
    return segmented_text.lower()


# Part 1 & 2: Indexing
def build_index(docs: list[str]):
    # Setup Tantivy Schema
    schema_builder = tantivy.SchemaBuilder()
    schema_builder.add_text_field("body", stored=False)
    schema_builder.add_text_field("raw_body", stored=True)
    schema = schema_builder.build()

    # Indexing (In-memory)
    index = tantivy.Index(schema)
    writer = index.writer()

    for original_doc in docs:
        # Tokenize using custom Vietnamese tokenizer
        processed_text = vietnamese_tokenizer(original_doc)

        # Add to index
        writer.add_document(
            tantivy.Document(body=[processed_text], raw_body=[original_doc])
        )

    writer.commit()
    index.reload()
    return index


# Part 3: Search
def search(query: str, index: tantivy.Index, original_docs: list[str]):
    searcher = index.searcher()

    # Tokenize the query
    processed_query = vietnamese_tokenizer(query)
    # Parse query against the "body" field
    parsed_query = index.parse_query(processed_query, ["body"])
    # Get results
    results_raw = searcher.search(parsed_query, len(original_docs))

    results = []
    # Filter results with score > 0
    for score, doc_address in results_raw.hits:
        if score > 0:
            doc = searcher.doc(doc_address)
            # Retrieve the original text from the mapped raw_body
            retrieved_doc = doc["raw_body"][0]
            results.append((score, retrieved_doc))
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
index = build_index(documents)

## Search - Run many
queries = [
    "lập trình backend",
    "học máy với python",
    "cách quản lý container kubernetes",
    "golang API",  # Not included in DB
]
for q in queries:
    print(f"Query: '{q}'")
    results = search(q, index, documents)
    if not results:
        print("  -> Not found.")
    else:
        for score, doc in results:
            print(f"  Score: {score:.2f}: {doc}")
        print()
