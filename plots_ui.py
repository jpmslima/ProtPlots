# ui.py
import streamlit as st

def create_sidebar():
    """Cria a sidebar e retorna as opções selecionadas pelo usuário."""
    st.sidebar.title("Options")

    # Seleção de unidade
    st.sidebar.subheader("Files values are in Nanometers (nm) or Angstrom (Å)?")
    unit = st.sidebar.radio("Choose the unit for y-axis:", ("nm", "Å"))

    # Seção de upload de arquivos
    st.sidebar.subheader("Upload Files")
    rmsd_file = st.sidebar.file_uploader("Upload RMSD File (CSV/TSV)", type=["csv", "tsv"])
    rmsf_file = st.sidebar.file_uploader("Upload RMSF File (CSV/TSV)", type=["csv", "tsv"])

    # Seção de arquivos de exemplo
    st.sidebar.subheader("Use Example Files")
    use_example = st.sidebar.checkbox("Use Example Files")

    return unit, rmsd_file, rmsf_file, use_example
