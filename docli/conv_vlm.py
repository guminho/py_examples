import os

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=VlmPipeline,
        ),
    }
)

source = os.getenv("DOCSRC", "https://arxiv.org/pdf/2408.09869")
doc = converter.convert(source).document
print(doc.export_to_markdown())
