import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

func = get_registry().get("sentence-transformers").create(name="all-MiniLM-L6-v2")
db = lancedb.connect("./lance_st")


class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()


table = db.create_table("chunks", schema=Chunks, mode="overwrite")
table.add(
    [
        {"text": "LanceDB is great for local dev"},
        {"text": "Python is versatile"},
    ]
)

res = table.search("local development").distance_type("cosine").limit(1).to_list()
print(res[0]["text"])
