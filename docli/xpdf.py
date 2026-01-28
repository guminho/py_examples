import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def extract_pages(input_pdf: str, output_pdf: str, pages: list[int]):
    with (
        PdfReader(input_pdf) as reader,
        PdfWriter() as writer,
    ):
        n = len(reader.pages)
        pages = (int(p) for p in pages)
        pages = [p for p in pages if p < n]

        # Run
        for i in pages:
            writer.add_page(reader.pages[i])

        # Save
        with open(output_pdf, "wb") as f:
            writer.write(f)
        print("Success")


# Usage
path1 = Path(sys.argv[1])
path2 = path1.with_name(sys.argv[2])
pages = sys.argv[3].split(",")
extract_pages(path1, path2, pages)
