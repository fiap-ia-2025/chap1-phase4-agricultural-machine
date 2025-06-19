import streamlit as st  # Cria a interface web interativa com Streamlit
import pandas as pd  # Manipula e carrega dados em tabelas (DataFrames)
import sqlite3

arquivo = 'farm_data.db'
conn = sqlite3.connect(arquivo)
query = "SELECT * FROM leitura_sensor"
df = pd.read_sql_query(query, conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])

st.header("Modelagem Preditiva 🧠")

