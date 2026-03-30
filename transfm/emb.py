from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sents = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]

embds = model.encode(sents)
print(embds.shape)  # (3, 384)

sims = model.similarity(embds, embds)
print(sims)
