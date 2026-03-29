import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence. This is another sentence.")

assert doc.has_annotation("SENT_START")
for sent in doc.sents:
    print(sent.text)
