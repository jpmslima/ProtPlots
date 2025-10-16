# ui.py

import streamlit as st

def render_sidebar():
    """Renders the sidebar controls and returns their values."""
    st.sidebar.title("⚙️ Controls")

    analysis_type = st.sidebar.selectbox(
        "1. Select data type to compile:",
        ("RMSD", "RMSF", "Rg"),
        help="The analysis type determines the output filename."
    )

    output_prefix = st.sidebar.text_input(
        "2. Enter a prefix for the output CSV:",
        value="compiled_data",
        help="E.g., 'ProteinA'. The final name will be 'ProteinA_RMSD.csv'."
    )

    txt_files = st.sidebar.file_uploader(
        f"3. Upload your .txt {analysis_type} files",
        type="txt",
        accept_multiple_files=True,
        help="You can select multiple files at once."
    )
    
    return analysis_type, output_prefix, txt_files

def display_results(result_df, output_prefix, analysis_type):
    """Displays the results DataFrame and a download button."""
    st.success("Data compiled successfully!")
    st.write("### Data Preview")
    st.dataframe(result_df.head())

    # Convert DataFrame to CSV in memory
    csv_data = result_df.to_csv(index=False).encode('utf-8')
    
    # Assemble the final filename
    final_filename = f"{output_prefix}_{analysis_type}.csv"

    # Create the download button
    st.download_button(
        label=f"📥 Download {final_filename}",
        data=csv_data,
        file_name=final_filename,
        mime='text/csv',
    )
