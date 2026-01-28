import os

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    RapidOcrOptions,
    TableStructureOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption


def main():
    # Any of the OCR options can be used: EasyOcrOptions, TesseractOcrOptions,
    # TesseractCliOcrOptions, OcrMacOptions (macOS only), RapidOcrOptions
    # ocr_options = EasyOcrOptions(force_full_page_ocr=True)
    # ocr_options = TesseractOcrOptions(force_full_page_ocr=True)
    # ocr_options = OcrMacOptions(force_full_page_ocr=True)
    ocr_options = RapidOcrOptions(force_full_page_ocr=True)
    # ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options = TableStructureOptions(
        do_cell_matching=True
    )
    pipeline_options.ocr_options = ocr_options
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
