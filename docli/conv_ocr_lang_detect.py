import os

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption


def main():
    ocr_options = TesseractCliOcrOptions(lang=["auto"])
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,
        force_full_page_ocr=True,
        ocr_options=ocr_options,
    )
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )

    source = os.getenv("DOCSRC", "https://arxiv.org/pdf/2408.09869")
    doc = converter.convert(source).document
    print(doc.export_to_markdown())


if __name__ == "__main__":
    main()
