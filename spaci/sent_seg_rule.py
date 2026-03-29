from spacy.lang.en import English

nlp = English()  # just the language with no pipeline
nlp.add_pipe("sentencizer")
doc = nlp("This is a sentence. This is another sentence.")

for sent in doc.sents:
    print(sent.text)
