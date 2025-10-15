# General funes for STREAMLIT DATA and INTERFACE management

import streamlit as st
import pandas as pd
import os 
import re
from collections import defaultdict

##SET EXAMPLE FILES HERE



## Defines HufflePlots SIDEBAR UPLOAD
### File Upload with SELECTBOX  - RMSD/RMSF/Rg .csv/.tsv direct input (tab1)
def csv_upload():
    st.sidebar.subheader("1.Plots RMSD/RMSF/Rg")
    select = st.sidebar.selectbox("Select your Desired Plot:",
                                  ("RMSD","RMSF","Rg"))
    ## Selection based uploader - Plots
    if select == "RMSD":
        plot_file = st.sidebar.file_uploader("Upload do arquivo RMSD (CSV/TSV)", type=["csv", "tsv"], key="rmsd")
    elif select == "RMSF":
        plot_file = st.sidebar.file_uploader("Upload do arquivo RMSF (CSV/TSV)", type=["csv", "tsv"], key="rmsf")
    elif select == "Rg":
        plot_file = st.sidebar.file_uploader("Upload do arquivo RG (CSV/TSV)", type=["csv", "tsv"], key="rg")

    #Plot example for RMSD/RMSF - ADICIONAR Rg
    use_example = st.sidebar.checkbox("Use Example Files")
    example_folder = "example_files"

    #Plot for EXAMPLE FILES
    if use_example:
        rmsd_file = os.path.join(example_folder, "P03923_WTxN119S_F161L_RMSD.tsv")
        rmsf_file = os.path.join(example_folder, "P03923_WTxN119S_F161L_RMSF.tsv")


### File Upload for GROMACS .xvg Pre-Processing Files (tab2)
def xvg_upload():
    st.sidebar.subheader("2. Pre-Process GROMACS .xvg files to .csv")
    xvg_file = st.sidebar.file_uploader("Upload your .xvg files from GROMACS", type=["xvg"], key="xvg")
    st.sidebar.markdown(
        "_*Mixed rmsd/rmsf/rg uploaded files are identified by a header-based search (`gmx rms/rmsdist`, `gmx_rmsf`, `gmx_gyrate`), and processed separately.*_" )

    #ADICIONAR EXAMPLE DATA AQUI!!!!


### File Upload of .txt files for .CSV Compilation (tab3)
def txt_upload():
    st.sidebar.subheader("3. Compilator of calculation .txt files to .csv for Comparative Analysis")
    csv_file = st.sidebar.file_uploader("Upload your .txt files", type=["txt"], key="txt")
    st.sidebar.markdown(
        "_*Select for compilation molecule files of the same calculation only (RMSD/RMSF/Rg). The .csv generated can be used as an input to the `1.plot` process. `2.xvg_process` already generates the `.csv`*_" )


    #ADICIONAR EXAMPLE DATA AQUI!!!!!




