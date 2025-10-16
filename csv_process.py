# data_processing.py

import pandas as pd
import os
from typing import List, Tuple, Optional, Any

def compile_data_to_csv(uploaded_files: List[Any]) -> Tuple[Optional[pd.DataFrame], List[str]]:
    """
    Reads a list of text files, extracts data, and merges them into a single DataFrame.

    Args:
        uploaded_files: A list of Streamlit UploadedFile objects.

    Returns:
        A tuple containing:
        - A pandas.DataFrame with the merged data.
        - A list of error messages encountered during processing.
    """
    if not uploaded_files:
        return None, ["No files were uploaded."]

    errors = []
    
    # Use the first file to initialize the main DataFrame
    first_file = uploaded_files[0]
    first_label = os.path.splitext(first_file.name)[0]
    
    try:
        main_df = pd.read_csv(first_file, sep=r'\s+', header=None, names=['Model', first_label])
    except Exception as e:
        error_msg = f"Error processing file '{first_file.name}': {e}"
        return None, [error_msg]

    # Iterate over the remaining files and merge them
    for file in uploaded_files[1:]:
        label = os.path.splitext(file.name)[0]
        try:
            temp_df = pd.read_csv(file, sep=r'\s+', header=None, names=['Model', label])
            # Use an 'outer' join to ensure all models from all files are kept
            main_df = main_df.merge(temp_df, on='Model', how='outer')
        except Exception as e:
            errors.append(f"Error processing file '{file.name}': {e}")
            continue # Skip to the next file on error

    return main_df, errors