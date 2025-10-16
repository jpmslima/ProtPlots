# utils.py
import streamlit as st
import pandas as pd

def load_data(file):
    try:
        if isinstance(file, str):  # For example files
            if file.endswith(".csv"):
                return pd.read_csv(file)
            elif file.endswith(".tsv"):
                return pd.read_csv(file, sep="\	")
        else:  # For uploaded files
            if file.name.endswith(".csv"):
                return pd.read_csv(file)
            elif file.name.endswith(".tsv"):
                return pd.read_csv(file, sep="\	")
    except Exception as e:
        st.error("Error loading file: " + str(e))
        return None
