#Def containing markdown with styling configuration

## Dependencies and Libraries
import streamlit as st
import os
import re
from collections import defaultdict


def custom():
    #Define Sidebar and its Main Configurations
    ## Increse Sidebar width, Color pattern for Light/Dark
    st.markdown(
        """
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child { 
            width: 350px; 
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 350px; 
            margin-left: -350px; 
        }
        """,
        unsafe_allow_html=True
    )

    ##Hiding Sidebar
    # Hide sidebar using query parameters
    # Access with ?embedded=true
    if "embedded" in st.query_params:
        st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {display: none}
        </style>
        """,
        unsafe_allow_html=True
        )

