from sentence_transformers import SparseEncoder

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")

sents = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]

embds = model.encode(sents)
print(embds.shape)  # (3, 30522)

sims = model.similarity(embds, embds)
print(sims)

stats = SparseEncoder.sparsity(embds)
print(stats)
