#Main Fune for Streamlit run. Orchestrate every .py 

## Dependencies and Libraries

import streamlit as st
import os
import re
from collections import defaultdict

## .py Scripts import for orchestration
### Upload and Sidebar Management
from reposit.utils import helpers
from reposit.utils import style
### Tabs Process and Analysis
from reposit.utils import funes
from reposit.analyses import plots
from reposit.analyses import xvg_process
from reposit.analyses import csv_compile



## Sets the main fune

def main():
    st.image('HufflePlots.png')
    st.title("HufflePlots: Protein Molecular Dynamics *Harry Plotter")

    #Markdown for Slyling Sidebars:
    style.custom()
    
    #Unit Selection (Used further for Plotting)
    st.sidebar.title("Options")
    st.sidebar.subheader("Files values for plots are in Nanometers (nm) or Angstrom (Å)")
    unit = st.sidebar.radio("Choose the unit for y-axis",("nm","Å"))


    #Sidebar Process Selection
    st.sidebar.header("Select One Analysis to Upload your data:")

    
    #Sidebar Processing by calling helpers.py
    helpers.csv_upload() # Build sidebar for tab1 Upload
    helpers.xvg_upload() # tab2 sidebar Upload
    helpers.txt_upload() # tab3 sidebar Upload

    #Define tabs
    tab1, tab2, tab3 = st.tabs([
        "Direct Plotting: .csv/.tsv files",
        "GROMACS: process .xvg files for Plotting",
        "Direct Plotting: .csv/.tsv files" #def de plotting pode ir pra utils compartilhado, e ser usada na etapa do GROMACS
    ])

    

if __name__ == "__main__":
    main()




