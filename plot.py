# plotting.py
import streamlit as st
import plotly.express as px

def plot_rmsd(data, unit):
    """Gera e exibe o gráfico RMSD."""
    try:
        y_data = data.iloc[:, 1:].copy()  # Cria uma cópia para evitar SettingWithCopyWarning
        x_col_name = data.columns[0]
        
        # O DataFrame original não é modificado. A conversão é feita na cópia.
        if unit == "nm":
            y_data = y_data / 10

        # Constrói um novo DataFrame para o Plotly usar
        plot_data = data[[x_col_name]].join(y_data)

        fig = px.line(plot_data, x=x_col_name, y=plot_data.columns[1:], title="RMSD Plot")
        fig.update_yaxes(title_text=f"RMSD ({unit})")
        fig.update_layout(legend_title="Trajectory")
        st.plotly_chart(fig)

        # Botão de download
        st.download_button(
            label="Download RMSD Plot as PNG",
            data=fig.to_image(format="png"),
            file_name="rmsd_plot.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"Error generating RMSD plot: {e}")

def plot_rmsf(data, unit):
    """Gera e exibe o gráfico RMSF."""
    try:
        y_data = data.iloc[:, 1:].copy()
        x_col_name = data.columns[0]

        if unit == "nm":
            y_data = y_data / 10

        plot_data = data[[x_col_name]].join(y_data)

        fig = px.line(plot_data, x=x_col_name, y=plot_data.columns[1:], title="RMSF Plot")
        fig.update_yaxes(title_text=f"RMSF ({unit})")
        fig.update_layout(legend_title="Trajectory")
        st.plotly_chart(fig)

        # Botão de download
        st.download_button(
            label="Download RMSF Plot as PNG",
            data=fig.to_image(format="png"),
            file_name="rmsf_plot.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"Error generating RMSF plot: {e}")
