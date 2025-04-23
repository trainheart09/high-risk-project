# streamlit_duckdb_app.py
import streamlit as st
import duckdb
import os
import pandas as pd

st.set_page_config(page_title="Synthetic OMOP Explorer")
st.title("Synthetic OMOP Explorer")

DATA_DIR = "/content/omop_synthetic"
available_tables = {
    "patients": "patients_synthetic.csv",
    "conditions": "conditions_synthetic.csv",
    "encounters": "encounters_synthetic.csv",
    "medications": "medications_synthetic.csv",
    "observations": "observations_synthetic.csv",
    "procedures": "procedures_synthetic.csv",
}

con = duckdb.connect()
for table_name, csv_file in available_tables.items():
    path = os.path.join(DATA_DIR, csv_file)
    if os.path.exists(path):
        con.sql(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{path}')")

if st.checkbox("Show available tables and columns"):
    for table in available_tables:
        st.subheader(f"{table}")
        try:
            df = con.sql(f"SELECT * FROM {table} LIMIT 5").df()
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error previewing table `{table}`: {e}")

st.subheader("🔎 Run SQL Query")
query = st.text_area("Enter SQL query:", "SELECT * FROM patients LIMIT 5")
if st.button("Run"):
    try:
        result = con.sql(query).df()
        st.success(f"Returned {len(result)} rows")
        st.dataframe(result)
    except Exception as e:
        st.error(f"Query failed: {e}")
