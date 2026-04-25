import lancedb
from lancedb.embeddings import TextEmbeddingFunction, register
from lancedb.pydantic import LanceModel, Vector
from pydantic import PrivateAttr
from sentence_transformers import SentenceTransformer


@register("my-sbert")
class SBertEmbedFunc(TextEmbeddingFunction):
    model_name: str = "all-MiniLM-L6-v2"
    _model: SentenceTransformer = PrivateAttr(default=None)

    @property
    def model(self) -> SentenceTransformer:
        # lazy-load: model is created only on first embedding call
        if self._model is None:
            self._model = SentenceTransformer(self.model_name, backend="onnx")
        return self._model

    def generate_embeddings(self, texts: list[str]):
        # normalize_embeddings=True → unit vectors; dot product == cosine, no division needed at query time
        return self.model.encode(
            texts, convert_to_numpy=True, normalize_embeddings=True
        ).tolist()

    def ndims(self):
        return 384


func = SBertEmbedFunc.create()
db = lancedb.connect("./lance_sbert")


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
