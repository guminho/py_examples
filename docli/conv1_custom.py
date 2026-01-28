import os
from time import monotonic

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    RapidOcrOptions,
    TableStructureOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption


def conv0():
    return DocumentConverter()


def conv_fium_n():
    # PyPdfium without EasyOCR
    # --------------------
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.table_structure_options = TableStructureOptions(
        do_cell_matching=False
    )
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
            )
        }
    )


def conv_fium_o():
    # PyPdfium with EasyOCR
    # -----------------
    pipeline_options = PdfPipelineOptions()
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
            )
        }
    )


def conv_dparse_n():
    # Docling Parse without EasyOCR
    # -------------------------
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )


def conv_dparse_o():
    # Docling Parse with EasyOCR (default)
    # -------------------------------
    # Enables OCR and table structure with EasyOCR, using automatic device
    # selection via AcceleratorOptions. Adjust languages as needed.
    pipeline_options = PdfPipelineOptions()
    pipeline_options.ocr_options.lang = ["vi"]
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )


def conv_dparse_tes():
    # Docling Parse with Tesseract CLI
    # --------------------------------
    pipeline_options = PdfPipelineOptions()
    pipeline_options.ocr_options = TesseractCliOcrOptions()
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )


def conv_dparse_rapid():
    pipeline_options = PdfPipelineOptions()
    pipeline_options.ocr_options = RapidOcrOptions()
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )


def run_conv(source: str, converter: DocumentConverter):
    tik = monotonic()
    doc = converter.convert(source).document
    tok = monotonic()
    print(f"\n\n@@ === {converter_fn.__name__} in {tok - tik:.3f}s === \n\n")
    print(doc.export_to_markdown())
    return doc


if __name__ == "__main__":
    for source in os.environ["DOCSRC"].split(","):
        for converter_fn in [
            conv0,
            conv_fium_n,
            conv_fium_o,
            conv_dparse_n,
            conv_dparse_o,
            conv_dparse_tes,
            conv_dparse_rapid,
        ]:
            doc = run_conv(source, converter_fn())
