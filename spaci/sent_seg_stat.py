import spacy

nlp = spacy.load("en_core_web_sm", exclude=["parser"])
nlp.enable_pipe("senter")
doc = nlp("This is a sentence. This is another sentence.")

for sent in doc.sents:
    print(sent.text)
