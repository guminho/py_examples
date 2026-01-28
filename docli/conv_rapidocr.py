import os

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from modelscope import snapshot_download


def main():
    # Download RapidOCR models from Hugging Face
    download_path = snapshot_download(repo_id="RapidAI/RapidOCR")
    det_model_path = os.path.join(
        download_path, "onnx", "PP-OCRv5", "det", "ch_PP-OCRv5_server_det.onnx"
    )
    rec_model_path = os.path.join(
        download_path, "onnx", "PP-OCRv5", "rec", "ch_PP-OCRv5_rec_server_infer.onnx"
    )
    cls_model_path = os.path.join(
        download_path, "onnx", "PP-OCRv4", "cls", "ch_ppocr_mobile_v2.0_cls_infer.onnx"
    )
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,
        ocr_options=RapidOcrOptions(
            det_model_path=det_model_path,
            rec_model_path=rec_model_path,
            cls_model_path=cls_model_path,
        ),
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
