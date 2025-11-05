#xvg_process non-modular version - for streamlit page configuration

from collections import defaultdict
import streamlit as st
import os
import re
import io
from collections import defaultdict
import pandas as pd
import plotly.express as px
import sys
import glob
from io import StringIO
import zipfile


# --- UI Elements --- ui.py on modular version
# ui.py


def render_header():
    """
    Renderiza o cabeçalho da aplicação.
    """
    st.markdown(
        """
        ## ⚙️ GROMACS XVG Pre-Processing Module
        This module processes GROMACS `.xvg` files (RMSD, RMSF) and converts them into `.csv` format for further analysis.
        """
    )

def render_sidebar():
    """
    Renderiza a barra lateral e seus componentes.
    
    Retorna:
        tuple: Contendo os arquivos enviados, o estado do checkbox de exemplo e a unidade selecionada.
    """
    st.sidebar.title("Options")

    st.sidebar.subheader("2. Pre-Process GROMACS .xvg files to .csv")
    xvg_files = st.sidebar.file_uploader(
        "Upload your .xvg files from GROMACS",
        accept_multiple_files=True,
        type=["xvg"]
    )
    st.sidebar.markdown(
        "_*Mixed rmsd/rmsf uploaded files are identified by a header-based search (`gmx rms/rmsdist`, `gmx_rmsf`, `gmx_gyrate`), and processed separately.*_"
    )
    
    tab2_example = st.sidebar.checkbox(".xvg Example Files")

    return xvg_files, tab2_example

def display_results(processed_files):
    """
    Exibe a mensagem de sucesso e os botões de download para os arquivos processados.

    Args:
        processed_files (dict): Dicionário com os arquivos processados, agrupados por tipo.
    """
    st.success(f"Processing complete. Found: {', '.join([f'{len(v)} {k.upper()}' for k, v in processed_files.items()])} file(s).")

    for file_type, files_list in processed_files.items():
        st.subheader(f"Downloads for {file_type.upper()} data")

        # Gera a string para o arquivo .py
        py_list_string = f"files_{file_type} = [\n"
        for item in files_list:
            py_list_string += f"    ('{item['name']}.txt', '{item['name']}'),\n"
        py_list_string += "]\n"

        # Botões de download para arquivos de texto individuais
        for item in files_list:
            file_label = item['name']
            txt_filename = f"{file_label}.txt"
            st.download_button(
                label=f"Download {txt_filename}",
                data=item['data'].encode('utf-8'),
                file_name=txt_filename,
                mime="text/plain",
                key=f"txt_downloader_{file_label}" # Chave única
            )

        # Botão de download para a lista .py
        st.download_button(
            label=f"Download files_{file_type}_list.txt",
            data=py_list_string.encode('utf-8'),
            file_name=f"files_{file_type}_list.txt",
            mime="text/plain",
            key=f"py_downloader_{file_type}" # Chave única
        )
        
    # --- INÍCIO DA SEÇÃO DE DOWNLOAD DO ZIP ---
    st.subheader("Download All as .ZIP")

    # Cria um buffer de bytes em memória para o ZIP
    zip_buffer = io.BytesIO()

    # Cria o arquivo ZIP no buffer
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        # Adiciona os arquivos .txt ao ZIP
        for file_type, files_list in processed_files.items():
            for item in files_list:
                txt_filename = f"{item['name']}.txt"
                # Escreve o conteúdo de texto (codificado em bytes) no ZIP
                zip_f.writestr(txt_filename, item['data'].encode('utf-8'))
        

    # Cria o botão de download para o ZIP
    st.download_button(
        label="Download ALL_Processed_Files.zip",
        data=zip_buffer.getvalue(), # Obtém os bytes do buffer
        file_name="ALL_Processed_Files.zip",
        mime="application/zip",
        key="zip_downloader_all"
    )



# --- File Handler --- file_handler.py on modular version
def get_files_to_process(uploaded_files, use_examples, example_folder="examples"):
    """
    Obtém uma lista de dicionários de arquivos para processar,
    seja dos arquivos de exemplo ou dos arquivos enviados pelo usuário.

    Args:
        uploaded_files (list): Lista de arquivos do st.file_uploader.
        use_examples (bool): Se deve usar os arquivos de exemplo.
        example_folder (str): O caminho para a pasta de exemplos.

    Returns:
        list: Uma lista de dicionários, cada um contendo 'name' e 'content' do arquivo.
    """
    files_to_process = []

    if use_examples:
        example_paths = glob.glob(os.path.join(example_folder, "*.xvg"))
        for file_path in example_paths:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            files_to_process.append({'name': file_name, 'content': content})
    
    elif uploaded_files:
        for uploaded_file in uploaded_files:
            content = uploaded_file.getvalue().decode("utf-8")
            file_name = uploaded_file.name
            files_to_process.append({'name': file_name, 'content': content})

    return files_to_process



# --- XVG Processor --- xvg_processor.py on modular version
def process_xvg_content(content, file_name):
    """
    Identifica o tipo de arquivo .xvg (RMSD, RMSF ou Rg) com base no cabeçalho e extrai os dados.
    Considera '#gmx rmsdist' como um arquivo RMSD.

    Args:
        content (str): O conteúdo do arquivo .xvg.
        file_name (str): O nome do arquivo .xvg.

    Returns:
        tuple: (file_type, output_name, data_as_string) ou (None, None, None) se o tipo não for identificado.
    """
    lines = content.split('\n')
    file_type = None
    output_name = None

    for line in lines:
        if '# gmx rms ' in line or '#   gmx rmsdist' in line:
            file_type = 'rmsd'
            match = re.search(r'-o\s+(\S+)', line)
            if match:
                output_name = os.path.splitext(match.group(1))[0]
            else:
                output_name = os.path.splitext(file_name)[0] + "_rmsd"
            break
        elif '#   gmx rmsf' in line:
            file_type = 'rmsf'
            match = re.search(r'-o\s+(\S+)', line)
            if match:
                output_name = os.path.splitext(match.group(1))[0]
            else:
                output_name = os.path.splitext(file_name)[0] + "_rmsf"
            break
        elif '#   gmx gyrate' in line:
            file_type = 'rg'
            match = re.search(r'-o\s+(\S+)', line)
            if match:
                output_name = os.path.splitext(match.group(1))[0]
            else:
                output_name = os.path.splitext(file_name)[0] + "_rg"
            break

    if not file_type:
        return None, None, None

    # Remove o cabeçalho e retorna os dados como uma única string
    data_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith(('#', '@'))]
    return file_type, output_name, '\n'.join(data_lines)

# --- Main Application Logic --- main.py on modular version
def main():
    """
    Função principal que orquestra a aplicação Streamlit.
    """

    st.set_page_config(
        page_title="XVG File Pre-Processing Module",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    # --- Main Interface ---
    st.title("XVG File Pre-Processing Module")

    # Renderiza o cabeçalho e a barra lateral, obtendo as entradas do usuário
    render_header()
    uploaded_files, use_examples = render_sidebar()

    # Obtém a lista de arquivos a serem processados com base na entrada do usuário
    files_to_process = get_files_to_process(
        uploaded_files=uploaded_files,
        use_examples=use_examples,
        example_folder="examples_shimohara"
    )

    # Se houver arquivos, processe-os e exiba os resultados
    if files_to_process:
        processed_files = defaultdict(list)

        with st.spinner('Processing .xvg files...'):
            for item in files_to_process:
                content = item['content']
                file_name = item['name']
                
                # Processa o conteúdo de cada arquivo
                file_type, output_name, data_string = process_xvg_content(content, file_name)
                
                if file_type:
                    processed_files[file_type].append({'name': output_name, 'data': data_string})
        
        # Exibe os resultados e os botões de download
        if processed_files:
            display_results(processed_files)

if __name__ == "__main__":
    main()