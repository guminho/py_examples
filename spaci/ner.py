import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for ent in doc.ents:
    attrs = (ent.text, ent.start_char, ent.end_char, ent.label_)
    template = "{:>10}" * len(attrs)
    print(template.format(*attrs))

html = displacy.render(doc, style="ent", page=True)
with open("ent_parse.html", "w") as f:
    f.write(html)
