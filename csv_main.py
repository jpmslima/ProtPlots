# app.py

import streamlit as st
from csv_ui import render_sidebar, display_results
from csv_process import compile_data_to_csv

# --- Page Configuration ---
st.set_page_config(
    page_title="MD Data Compiler",
    layout="centered"
)

# --- Main Interface ---
st.title("Molecular Dynamics Data Compiler")
st.write("Upload your RMSD, RMSF, or Rg files to compile them into a single CSV file.")

# --- Render UI and Get Inputs ---
analysis_type, output_prefix, txt_files = render_sidebar()

# --- Main Logic ---
if txt_files:
    st.info(f"Processing {len(txt_files)} file(s)...")

    # Call the processing function from the data_processing module
    result_df, errors = compile_data_to_csv(txt_files)

    # Display any errors that occurred
    if errors:
        for error in errors:
            st.error(error)

    # If processing was successful, display the results
    if result_df is not None and not result_df.empty:
        display_results(result_df, output_prefix, analysis_type)

else:
    st.warning("Waiting for files to be uploaded. Please use the controls in the sidebar.")