import os

from docling.document_converter import DocumentConverter

converter = DocumentConverter()

source = os.getenv("DOCSRC", "https://arxiv.org/pdf/2408.09869")
doc = converter.convert(source).document
print(doc.export_to_markdown())
