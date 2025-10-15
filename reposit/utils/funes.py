#RMSD RMSF SCRIPT

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
                st.dataframe(rmsf_data.head())
                plot_rmsf(rmsf_data, unit)
