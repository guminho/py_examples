import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for token in doc:
    attrs = (
        token.text,
        token.lemma_,
        token.pos_,
        token.tag_,
        token.dep_,
        token.shape_,
        token.is_alpha,
        token.is_stop,
    )
    template = "{:>10}" * len(attrs)
    print(template.format(*attrs))

html = displacy.render(doc, style="dep", page=True)
with open("dep_parse.html", "w") as f:
    f.write(html)
