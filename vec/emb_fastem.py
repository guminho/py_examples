import lancedb
from fastembed import TextEmbedding
from lancedb.embeddings import TextEmbeddingFunction, register
from lancedb.pydantic import LanceModel, Vector
from pydantic import PrivateAttr


@register("my-fastembed")
class FastEmbedFunc(TextEmbeddingFunction):
    model_name: str = "BAAI/bge-small-en-v1.5"
    _model: TextEmbedding = PrivateAttr(default=None)

    @property
    def model(self) -> TextEmbedding:
        # lazy-load: model is created only on first embedding call
        if self._model is None:
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def generate_embeddings(self, texts: list[str]):
        # fastembed normalizes output vectors unconditionally → unit-length, cosine == dot
        return [e.tolist() for e in self.model.embed(texts)]

    def ndims(self):
        return 384


func = FastEmbedFunc.create()
db = lancedb.connect("./lance_fast")


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
