from fastembed import TextEmbedding
from lancedb.embeddings import TextEmbeddingFunction, register
from pydantic import PrivateAttr


@register("fastembed")
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
