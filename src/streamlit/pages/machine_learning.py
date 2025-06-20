import streamlit as st  # Cria a interface web interativa com Streamlit
import pandas as pd  # Manipula e carrega dados em tabelas (DataFrames)
from sklearn.metrics import accuracy_score # Calcula acurácia do modelo
from sklearn.model_selection import train_test_split # Separa modelo para teste e para treino
from sklearn.tree import DecisionTreeClassifier # Modelo preditivo de Árvore de decisão
from sklearn.preprocessing import LabelEncoder # Tranforma colunas categóricas em numéricas
import joblib

# Carregar o modelo
with open("/Users/amanda/Documents/FIAP/projetos/chap1-phase4-agricultural-machine/documents/decision_tree_model.pkl", 'rb') as f:
    modelo = joblib.load(f)

st.set_page_config(page_title='Modelagem Preditiva', layout='wide')
st.title("Modelagem Preditiva com Árvore de Decisão 🧠")

# Cria Filtros
st.sidebar.title('Filtros de dados')
humidity = st.sidebar.slider(
    'Umidade (%):',
    min_value=0.00,
    max_value=100.00,
    value=50.00
)

phsimulated = st.sidebar.slider(
    'PH Simulado:',
    min_value=0.11,
    max_value=13.89,
    value=0.11,
)

temperature = st.sidebar.slider(
    'Temperatura (ºC):',
    min_value=-40.00,
    max_value=80.00,
    value=60.00
)

# Realiza Previsão do com o modelo treinado
st.header("Previsões do Modelo")

## Coleta dados
input_humidity = st.number_input('Umidade (%)', value=humidity, min_value=0.0, max_value=100.0, step=0.01, key='humidity_input')
input_phsimulated = st.number_input('PH Simulado',value=phsimulated, min_value=0.11, max_value=13.89, step=0.01, key='phsimulated_input')
input_temperature = st.number_input('Temperatura (°C)', value=temperature, min_value=-40.00, max_value=80.00, step=0.01, key='temperature_input')

# Atualiza o slider se o input mudar
if input_humidity != humidity:
    humidity = input_humidity

if input_phsimulated != phsimulated:
    phsimulated = input_phsimulated

if input_temperature != temperature:
    temperature = input_temperature

## Valida dados
input_error = False
if not (0 <= input_humidity <= 100):
    st.error('A umidade deve estar entre 0% e 100%.')
    input_error = True
if not (0.11 <= input_phsimulated <= 13.89):
    st.error('O PH deve estar entre 0.11 e 13.89.')
    input_error = True
if not (-40.00 <= input_temperature <= 80.00):
    st.error('A temperatura deve estar entre -40.00ºC e 80.00ºC.')
    input_error = True

if input_error:
    st.stop()

input_data = {
    'humidity': [input_humidity],
    'phsimulated': [input_phsimulated],
    'temperature': [input_temperature],
    'phosphorusstatus_enconder': [0],  # Placeholder, pois não está sendo usado
    'potassiumstatus_enconder': [0]  # Placeholder, pois não está sendo usado
}

input_df = pd.DataFrame(input_data)

## Realiza previsão
pred = modelo.predict(input_df)

# Exibe o resultado da previsão
if pred is None or len(pred) == 0:
    st.error("Erro ao realizar a previsão. Verifique os dados de entrada.")
    st.stop()

status = "IRRIGAR" if pred == 1 else "NÃO IRRIGAR"
emoji = "💧" if pred == 1 else "🌱"
cor = "green" if pred == 1 else "orange"

st.markdown(f"""
<div style="padding: 2rem; border-radius: 1rem; border: 2px solid {cor}; text-align: center;">
    <h2 style="color: {cor};">{emoji} Resultado da Simulação</h2>
    <p style="font-size: 1.5rem; color: {cor};">Com base nos dados fornecidos, o sistema recomenda: <strong>{status}</strong></p>
    <p style="font-size: 1.2rem; color: {cor};">Umidade: {input_humidity:.2f}% | pH Simulado: {input_phsimulated:.2f} | Temperatura: {input_temperature:.2f}°C</p>
    <p style="font-size: 1.2rem; color: {cor};">A previsão foi realizada com sucesso utilizando o modelo de Árvore de Decisão.</p>
</div>
""", unsafe_allow_html=True)

