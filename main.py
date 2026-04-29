"""
Main module for basic data analysis using Pandas and Streamlit.
"""

from pathlib import Path
import pandas as pd
import streamlit as st
from datetime import datetime
import io


def read_data(file_path) -> pd.DataFrame:
    """
    Reads data from the specified file path.
    """
    # O Streamlit passa um objeto de buffer, o pandas lê direto
    return pd.read_csv(file_path, sep=',')


def process_data(data_frame) -> pd.DataFrame:
    """
    Processes the given DataFrame by applying filters, groupings, etc.
    """
    if data_frame is not None:
        colunas = ["Order", "Inventory type", "Ordered quantity", "Item", "Item description"]
        
        # .copy() evita o erro "SettingWithCopyWarning" ao criar a nova coluna
        df = data_frame[colunas].copy()

        df['Acao'] = df['Inventory type'].apply(lambda x: "Corte" if x == 14 else "Analisar")
        df = df.sort_values(by="Ordered quantity", ascending=False)

        return df
    return None


def main() -> None:
    st.set_page_config(page_title="Data Analysis", layout="wide")
    st.title("Data Analysis Overview")

    # 1. Drag and Drop
    loaded_file = st.file_uploader("Arraste seu OrderLine aqui: ", type='csv')

   

    # 2. Trava de segurança: Só executa se o arquivo existir
    if loaded_file is not None:
        try:
            # Lê os dados
            data_frame = read_data(loaded_file)
            
            # Processa
            df_final = process_data(data_frame)

            # Exibe os resultados
            st.subheader("Resultado do Processamento")
            st.dataframe(df_final, use_container_width=True)

            buffer = io.BytesIO()

            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False)

            df_bytes = buffer.getvalue()

            st.download_button(
                label="📥 Baixar como Excel",
                data=df_bytes,
                file_name=f"OrderLine_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Feedback de sucesso
            st.success(f"Arquivo '{loaded_file.name}' processado com sucesso!")
            
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
    else:
        # Mensagem caso não tenha arquivo
        st.info("Aguardando upload do arquivo CSV (OrderLine) para análise.")

    



if __name__ == "__main__":
    main()

