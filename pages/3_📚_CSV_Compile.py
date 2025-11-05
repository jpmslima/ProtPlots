import streamlit as st
import pandas as pd
import os
import glob

st.set_page_config(layout="centered") #CENTERED

# --- Utility Functions ---

def compile_data_to_csv(uploaded_files):
    """
    Reads a list of text files, extracts the data, and merges them into a single DataFrame.

    Args:
        uploaded_files: A list of Streamlit UploadedFile objects,
                        where each file is a .txt with two columns separated by spaces.

    Returns:
        A pandas.DataFrame containing the merged data. The first column is 'Model',
        and subsequent columns are named after the input filenames.
        Returns None if the input list is empty.
    """
    if not uploaded_files:
        return None

    # Use the first file to initialize the main DataFrame
    first_file = uploaded_files[0]
    # Use the filename (without the .txt extension) as the column label
    first_label = os.path.splitext(first_file.name)[0]
    
    try:
        # Read the file using multiple spaces as the separator and name the columns
        main_df = pd.read_csv(first_file, sep=r'\s+', header=None, names=['Model', first_label])
    except Exception as e:
        st.error(f"Error processing file '{first_file.name}': {e}")
        return None

    # Iterate over the remaining files and merge them into the main DataFrame
    for file in uploaded_files[1:]:
        label = os.path.splitext(file.name)[0]
        try:
            temp_df = pd.read_csv(file, sep=r'\s+', header=None, names=['Model', label])
            # 'outer' join to ensure all models from all files are retained
            main_df = main_df.merge(temp_df, on='Model', how='outer')
        except Exception as e:
            st.error(f"Error processing file '{file.name}': {e}")
            continue # Skip to the next file in case of error

    return main_df

# --- Streamlit Interface ---

st.title("CSV Compiler for Protein Comparative Analysis")
st.write("Upload your RMSD, RMSF, or Rg files to compile them into a single CSV file.")

# 1. Select analysis type
analysis_type = st.selectbox(
    "1. Select the type of data you want to compile:",
    ("RMSD", "RMSF"), #Removed Rg for now, updates alter will be made to add it
    help="The type of analysis determines the name of the output file. Build .csv for RMSD or RMSF data separately."
)

# 2. Upload files
txt_files = st.file_uploader(
    f"2. Upload your .txt files for {analysis_type}",
    type="txt",
    accept_multiple_files=True,
    help="You can select multiple files at once. Make sure the files selected are all of the same type (RMSD or RMSF)."
)

# 3. Define output prefix
output_prefix = st.text_input(
    "3. Enter a prefix for the output .csv file:",
    value="compiled_data",
    help="Ex: 'PTN1'. The final name will be 'PTN1_RMSD.csv'."
)

# Example files
#st.subheader("Use Example Files")
#csv_example = st.checkbox(".CSV Example Files")
#example_folder = "example_files"

## CAMINHOS DIFERENTES PARA EXAMPLE E UPLOAD

txt_to_process = []

#if csv_example:
#         example_paths = glob.glob(os.path.join(example_folder, "*.txt"))
#         for file_path in example_paths:
#             file_name = os.path.basename(file_path)
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 txt_to_process.append({'name': file_name, 'content': content})


# Processing when files are Uploaded

if txt_files:
    for uploaded_file in txt_files:
        content = uploaded_file.getvalue().decode("utf-8")
        file_name = uploaded_file.name
        txt_to_process.append({'name': file_name, 'content': content})
    
         

# 4. Processing and download button
if txt_files:
    st.info(f"Processing {len(txt_files)} file(s)...")

    # Call the optimized function to process the files
    result_df = compile_data_to_csv(txt_files)

    if result_df is not None and not result_df.empty:
        st.success("Data compiled successfully!")
        st.write("### Data Preview")
        st.dataframe(result_df.head())

        # Convert the DataFrame to CSV in memory
        csv_data = result_df.to_csv(index=False).encode('utf-8')

        # Build the final filename
        final_filename = f"{output_prefix}_{analysis_type}.csv"

        # Create the download button
        st.download_button(
            label=f"📥 Download {final_filename}",
            data=csv_data,
            file_name=final_filename,
            mime='text/csv',
        )
else:
    st.warning("Waiting for file upload to start processing.")