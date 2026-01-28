import json
from urllib.request import urlopen

import rich
from cli import client
from sentence_transformers import SentenceTransformer

# Ini
model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX = "book_index"
client.indices.create(index=INDEX)


# Add data
url = "https://raw.githubusercontent.com/elastic/elasticsearch-labs/main/notebooks/search/data.json"
resp = urlopen(url)
books = json.loads(resp.read())

operations = []
for book in books:
    operations.append({"index": {"_index": INDEX}})
    # Transforming the title into an embedding using the model
    book["title_vector"] = model.encode(book["title"]).tolist()
    operations.append(book)
client.bulk(index=INDEX, operations=operations, refresh=True)


# Search
resp = client.search(
    index=INDEX,
    knn={
        "field": "title_vector",
        "query_vector": model.encode("javascript books"),
        "k": 10,
        "num_candidates": 100,
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# Filter
resp = client.search(
    index=INDEX,
    knn={
        "field": "title_vector",
        "query_vector": model.encode("javascript books"),
        "k": 10,
        "num_candidates": 100,
        "filter": {"term": {"publisher.keyword": "addison-wesley"}},
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])
