# streamlit_duckdb_app.py — explore synthetic OMOP data
import streamlit as st, duckdb, os, pandas as pd
st.set_page_config(page_title="Synthetic OMOP Explorer")
st.title("Synthetic OMOP Explorer")
# folder where synthetic csvs are stored
DATA_DIR = "omop_synthetic"
# mapping table names to CSV filenames
tables = {
    "patients": "patients_synthetic.csv",
    "conditions": "conditions_synthetic.csv",
    "encounters": "encounters_synthetic.csv",
    "medications": "medications_synthetic.csv",
    "observations": "observations_synthetic.csv",
    "procedures": "procedures_synthetic.csv"
}
# connect to in-memory duckdb and load CSVs as tables
con = duckdb.connect()
for name, file in tables.items():
    path = os.path.join(DATA_DIR, file)
    if os.path.exists(path):
        con.sql(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{path}')")
# optional: preview table schemas and top rows
if st.checkbox("Show available tables and columns"):
    for name in tables:
        st.subheader(f"{name}")
        try: st.dataframe(con.sql(f"SELECT * FROM {name} LIMIT 5").df())
        except Exception as e: st.error(f"Error loading `{name}`: {e}")
# user query input
st.subheader("Run SQL Query")
query = st.text_area("Enter SQL query:", "SELECT * FROM patients LIMIT 5")
if st.button("Run"):
    try:
        result = con.sql(query).df()
        st.success(f"Returned {len(result)} rows")
        st.dataframe(result)
    except Exception as e:
        st.error(f"Query failed: {e}")
