import pandas as pd  # Manipula e carrega dados em tabelas (DataFrames)
import sqlite3
import streamlit as st  # Cria a interface web interativa com Streamlit

# Estrutura do cabeçalho e layout da página
st.set_page_config(page_title="Sistema de Irrigação Inteligente", layout="wide")
st.title("🌿 Dashboard - Sistema de Irrigação Inteligente")
st.markdown(
    "Este painel apresenta a leitura dos sensores do solo e o comportamento do sistema de irrigação automático.")



st.title('Leitura do Sensor')

# Conexão com Base de dados
st.header('Conexão com Base de dados')
arquivo = 'D:\PARTICULAR\FIAP\FASE 4\chap1-phase4-agricultural-machine\scripts\\farm_data.db'
conn = sqlite3.connect(arquivo)
query = "SELECT * FROM leitura_sensor"
df = pd.read_sql_query(query, conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])

pd.set_option('display.max_columns', None)   # mostra todas as colunas
pd.set_option('display.max_rows', None)      # mostra todas as linhas
pd.set_option('display.width', None)         # evita quebra de linha
pd.set_option('display.max_colwidth', None)
st.dataframe(df)
conn.close()