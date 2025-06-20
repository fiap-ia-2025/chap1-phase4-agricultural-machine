import streamlit as st  # Cria a interface web interativa com Streamlit
import pandas as pd  # Manipula e carrega dados em tabelas (DataFrames)
from sklearn.metrics import accuracy_score # Calcula acurácia do modelo
from sklearn.model_selection import train_test_split # Separa modelo para teste e para treino
from sklearn.tree import DecisionTreeClassifier # Modelo preditivo de Árvore de decisão
from sklearn.preprocessing import LabelEncoder # Tranforma colunas categóricas em numéricas

# Carrega DataFrame
path = 'coletas.csv'
df = pd.read_csv(path)

st.set_page_config(page_title='Modelagem Preditiva', layout='wide')
st.title("Modelagem Preditiva com Árvore de Decisão 🧠")

# Cria Filtros
st.sidebar.title('Filtros de dados')
min_humidity, max_humidity = st.sidebar.slider(
    f'Umidade (%):',
    min_value=float(df['humidity'].min()),
    max_value=float(df['humidity'].max()),
    value=(float(df['humidity'].min()), float(df['humidity'].max()))
)

min_phsimulated, max_phsimulated = st.sidebar.slider(
    f'PH Simulado:',
    min_value=float(df['phsimulated'].min()),
    max_value=float(df['phsimulated'].max()),
    value=(float(df['phsimulated'].min()), float(df['phsimulated'].max()))
)

min_temperature, max_temperature = st.sidebar.slider(
    f'Temperatura (ºC):',
    min_value=float(df['temperature'].min()),
    max_value=float(df['temperature'].max()),
    value=(float(df['temperature'].min()), float(df['temperature'].max()))
)

# Aplica Filtros ao DataFrame

filter_df = df[
    (df['humidity'] >= min_humidity) & (df['humidity'] <= max_humidity) &
    (df['phsimulated'] >= min_phsimulated) & (df['phsimulated'] <= max_phsimulated) &
    (df['temperature'] >= min_temperature) & (df['temperature'] <= max_temperature)
]

st.header("Dados após filtragem")

filter_df.drop( columns=["phosphorusstatus", "potassiumstatus"] , inplace=True )
X = filter_df.drop('shouldirrigate', axis=1)
y = filter_df['shouldirrigate']

st.write(f'Total de registros após filtragem: {len(X)}')

# Modelo Árvore de Decisão
## Tranformar colunas categóricas em numéricas
st.header("Acurácia Modelo Árvore de Decisão")

## Filtrar colunas relevantes
### Dividindo os dados em conjunto de teste e treinamento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)

decisiontree = DecisionTreeClassifier(random_state=50)
decisiontree.fit(X_train, y_train)
y_decisiontree_predict = decisiontree.predict(X_test)
decisiontree_accuracy = accuracy_score(y_test, y_decisiontree_predict)
st.write(f"Acurácia Árvore de Decisão: {decisiontree_accuracy}")

# Realiza Previsão do Modelo
st.header("Previsões do Modelo")

## Coleta dados
input_humidity = st.number_input('Umidade (%)', value=float(filter_df['humidity'].mean()))
input_phsimulated = st.number_input('PH Simulado', value=float(filter_df['phsimulated'].mean()))
input_temperature = st.number_input('Temperatura (°C)', value=float(filter_df['temperature'].mean()))

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
if not input_error:
    input_data = {
        'humidity': [input_humidity],
        'phsimulated': [input_phsimulated],
        'temperature': [input_temperature],
    }
input_df = pd.DataFrame(input_data)

## Realiza previsão
prediction = decisiontree.predict(input_df)
st.subheader('Resultado da Previsão')
prediction_results = []
for valor in prediction:
    if valor == 1:
        prediction_results.append('Sim')
    else:
        prediction_results.append('Não')

st.write(f'**Previsão de Irrigação:** {prediction_results}')
