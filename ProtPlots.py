# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Define the app
def main():
    st.title("RMSD and RMSF Plotting App")
    st.sidebar.title("Options")

    # File upload section
    st.sidebar.subheader("Upload Files")
    rmsd_file = st.sidebar.file_uploader("Upload RMSD File (CSV/TSV)", type=["csv", "tsv"])
    rmsf_file = st.sidebar.file_uploader("Upload RMSF File (CSV/TSV)", type=["csv", "tsv"])

    # Example files section
    st.sidebar.subheader("Use Example Files")
    use_example = st.sidebar.checkbox("Use Example Files")
    example_folder = "example_files"

    if use_example:
        rmsd_file = os.path.join(example_folder, "P03891-RMSD-All.csv")
        rmsf_file = os.path.join(example_folder, "P03891-RMSF-All.csv")

    # Process files and plot
    if rmsd_file or rmsf_file:
        st.subheader("Uploaded Data and Plots")

        if rmsd_file:
            st.write("### RMSD Data")
            rmsd_data = load_data(rmsd_file)
            if rmsd_data is not None:
                st.dataframe(rmsd_data.head())
                plot_rmsd(rmsd_data)

        if rmsf_file:
            st.write("### RMSF Data")
            rmsf_data = load_data(rmsf_file)
            if rmsf_data is not None:
                st.dataframe(rmsf_data.head())
                plot_rmsf(rmsf_data)

# Function to load data
def load_data(file):
    try:
        if isinstance(file, str):  # For example files
            if file.endswith(".csv"):
                return pd.read_csv(file)
            elif file.endswith(".tsv"):
                return pd.read_csv(file, sep="\t")
        else:  # For uploaded files
            if file.name.endswith(".csv"):
                return pd.read_csv(file)
            elif file.name.endswith(".tsv"):
                return pd.read_csv(file, sep="\t")
    except Exception as e:
        st.error("Error loading file: " + str(e))
        return None

# Function to plot RMSD
def plot_rmsd(data):
    try:
        fig = px.line(data, x=data.columns[0], y=data.columns[1:], title="RMSD Plot")
        st.plotly_chart(fig)
        # Download button for the plot
        st.download_button(
            label="Download RMSD Plot as PNG",
            data=fig.to_image(format="png"),
            file_name="rmsd_plot.png",
            mime="image/png"
        )
    except Exception as e:
        st.error("Error generating RMSD plot: " + str(e))

# Function to plot RMSF
def plot_rmsf(data):
    try:
        fig = px.line(data, x=data.columns[0], y=data.columns[1:], title="RMSF Plot")
        st.plotly_chart(fig)
        # Download button for the plot
        st.download_button(
            label="Download RMSF Plot as PNG",
            data=fig.to_image(format="png"),
            file_name="rmsf_plot.png",
            mime="image/png"
        )
    except Exception as e:
        st.error("Error generating RMSF plot: " + str(e))

if __name__ == "__main__":
    main()