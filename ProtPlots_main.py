# app.py
import streamlit as st
import os
from plots_ui import create_sidebar
from plots_utils import load_data
from plot import plot_rmsd, plot_rmsf

def main():
    st.image('HufflePlots.png')
    st.title("HufflePlots: Protein Molecular Dynamics *Harry Plotter*")

    # Cria a sidebar e obtém as seleções do usuário
    unit, rmsd_file_uploaded, rmsf_file_uploaded, use_example = create_sidebar()

    # Define os arquivos a serem usados (upload ou exemplo)
    rmsd_file = None
    rmsf_file = None
    example_folder = "example_files"

    if use_example:
        rmsd_file = os.path.join(example_folder, "P03923_WTxN119S_F161L_RMSD.tsv")
        rmsf_file = os.path.join(example_folder, "P03923_WTxN119S_F161L_RMSF.tsv")
    else:
        rmsd_file = rmsd_file_uploaded
        rmsf_file = rmsf_file_uploaded

    # Processa os arquivos e gera os gráficos
    if rmsd_file or rmsf_file:
        st.subheader("Uploaded Data and Plots")

        if rmsd_file:
            st.write("### RMSD Data")
            rmsd_data = load_data(rmsd_file)
            if rmsd_data is not None:
                st.dataframe(rmsd_data.head())
                plot_rmsd(rmsd_data, unit)

        if rmsf_file:
            st.write("### RMSF Data")
            rmsf_data = load_data(rmsf_file)
            if rmsf_data is not None:
                st.write("Diagnóstico do DataFrame RMSF:")
                st.write("Arquivo carregado com sucesso. Dimensões:", rmsf_data.shape)
                st.write("Primeiras linhas do DataFrame:")
                st.dataframe(rmsf_data.head())
                plot_rmsf(rmsf_data, unit)
            else:
                st.error("O DataFrame RMSF não pôde ser carregado e é 'None'.")
            # --- FIM DO DIAGNÓSTICO ---
            # Checando problema de carregamento

            if rmsf_data is not None:
                st.dataframe(rmsf_data.head())
                plot_rmsf(rmsf_data, unit)

if __name__ == "__main__":
    main()
   