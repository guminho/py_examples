import os
from pathlib import Path

import pandas as pd
from docling.document_converter import DocumentConverter


def main():
    doc_converter = DocumentConverter()

    source = os.getenv("DOCSRC")
    conv_res = doc_converter.convert(source)

    output_dir = Path("scratch")
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_res.input.file.stem

    # Export tables
    for table_ix, table in enumerate(conv_res.document.tables):
        table_df: pd.DataFrame = table.export_to_dataframe(doc=conv_res.document)
        print(f"## Table {table_ix}")
        print(table_df.to_markdown())

        # Save the table as CSV
        element_csv_filename = output_dir / f"{doc_filename}-table-{table_ix + 1}.csv"
        table_df.to_csv(element_csv_filename)

        # Save the table as HTML
        element_html_filename = output_dir / f"{doc_filename}-table-{table_ix + 1}.html"
        with element_html_filename.open("w") as fp:
            fp.write(table.export_to_html(doc=conv_res.document))


if __name__ == "__main__":
    main()
