import lancedb
import streamlit as st

db = lancedb.connect("data/lancedb")
table_name = st.selectbox("Chọn bảng", db.table_names())
tbl = db.open_table(table_name)
st.dataframe(tbl.to_pandas())
