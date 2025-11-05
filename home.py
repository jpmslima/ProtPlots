# home.py
# Builds the main home page of the st app, as well as link the other pages
# Other pages MUST be in the "pages" folder, and as a single script each. 
import streamlit as st
import io
import os


# --- Set Page Config --- #
st.set_page_config(
    page_title="HufflePlots Home",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Main Interface --- (Home Page)
st.title("HufflePlots: Protein Molecular Dynamics *Harry Plotter*")

st.info("""
Welcome to HufflePlots! 
Use the **sidebar on the left** to navigate to different functionalities of the app.
""")

st.image('HufflePlots.png', width=250)


#st.info("ℹ️ A navegação foi movida para a barra lateral (sidebar).", icon="ℹ️")
