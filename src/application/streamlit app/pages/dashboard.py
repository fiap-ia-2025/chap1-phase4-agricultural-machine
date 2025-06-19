import streamlit as st  # Cria a interface web interativa com Streamlit
import matplotlib.pyplot as plt  # Cria e personaliza gráficos com controle total (base de visualização)
import seaborn as sns  # Gera gráficos estatísticos com visual bonito e menos código
import pandas as pd  # Manipula e carrega dados em tabelas (DataFrames)
import sqlite3

arquivo = 'farm_data.db'
conn = sqlite3.connect(arquivo)
query = "SELECT * FROM leitura_sensor"
df = pd.read_sql_query(query, conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Cria seção com análise de Umidade e pH lado a lado
col1, col2 = st.columns(2)

# ---- Análise 1 (Umidade do Solo + Acionamento): Avaliar se o sistema está acionando a bomba no momento certo ----
with col1:
    # Título e explicação da seção
    st.header("📈 Umidade do Solo e Acionamento da Bomba")
    st.info("""
    Este gráfico mostra a variação da umidade do solo com marcações dos momentos de irrigação.

    **Você pode avaliar:**
    - Quando a bomba foi acionada
    - Se a irrigação foi eficiente (Aumento de Umidade)
    - Se a lógica de ativação está funcionando corretamente
    """)

    # Criação do gráfico com Matplotlib
    fig1, ax1 = plt.subplots(figsize=(6, 4))

    # Plota a linha da umidade
    sns.lineplot(data=df, x="timestamp", y="umidade", label="umidade", ax=ax1)

    # Destaca os pontos em que a bomba foi ligada (em vermelho)
    bomba_ligada = df[df["status_bomba"] == 1]
    ax1.scatter(bomba_ligada["timestamp"], bomba_ligada["umidade"], color="red", label="Bomba Ligada")

    # Personalização visual
    ax1.set_title("Umidade do Solo ao Longo do Tempo", fontsize=12)
    ax1.set_ylabel("Umidade (%)")
    ax1.set_xlabel("Tempo (s)")
    plt.xticks(rotation=45)
    plt.legend()

    # Renderiza no Streamlit
    st.pyplot(fig1)

# ---- Análise 2 (Variação de pH): Analisar o comportamento no pH no solo ao longo do tempo ----
with col2:
    # Título e explicação da seção de pH
    st.header("🧪 Variação do pH do Solo")
    st.info("""
    Este gráfico mostra como o pH do solo está variando ao longo do tempo.  

    **Você pode avaliar:**
    - Se o pH está na faixa ideal (para a maioria das culturas está entre **6.0 e 7.5**).
    - Se há variações bruscas no solo (ex: chuva ácida, excesso de fertilizantes)
    - Se o solo tende a ser mais ácido ou alcalino ao longo do tempo
    """)

    # Criação do gráfico de pH
    fig_ph, ax_ph = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=df, x="timestamp", y="ph", color="purple", ax=ax_ph)

    # Faixa ideal de pH (visual guide)
    ax_ph.axhspan(6.0, 7.5, facecolor='green', alpha=0.1, label="Faixa Ideal (6.0 - 7.5)")

    # Personalização
    ax_ph.set_title("pH do Solo ao Longo do Tempo", fontsize=12)
    ax_ph.set_ylabel("pH")
    ax_ph.set_ylim(0, 14)
    ax_ph.legend()
    plt.xticks(rotation=45)

    # Exibe no Streamlit
    st.pyplot(fig_ph)

# ---- Análise 3 (Nutrientes em solo): Identificar frequência e padrão de ausência de nutrientes no solo ao longo do tempo (P e K) ----
# Título e explicação da seção de nutrientes
st.header("🧪 Nutrientes no Solo")
st.info("""
🌱 Este gráfico mostra a presença ou ausência dos nutrientes **Fósforo (P)** e **Potássio (K)** ao longo do tempo.

Você pode avaliar:
- A frequência com que os nutrientes estão ausentes
- Se há um padrão de esgotamento do solo
- Quando aplicar adubação corretiva
""")

# Cria colunas lado a lado
col3, col4 = st.columns(2)

# FÓSFORO (P)
with col3:
    # Explica Seção
    st.markdown("### 🔹 Fósforo (P)")
    st.markdown("_Presença = 1 · Ausência = 0_")

    # Plota Gráfico e Ajusta Visual
    fig_p, ax_p = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df, x="timestamp", y="fosforo", color="skyblue", ax=ax_p)
    ax_p.set_title("Fósforo (P)")
    ax_p.set_yticks([0, 1])
    ax_p.set_yticklabels(["Ausente", "Presente"])
    ax_p.set_ylabel("Presença")
    ax_p.set_xlabel("Tempo (s)")
    plt.xticks(rotation=45)
    plt.ylim(0, 1.2)
    st.pyplot(fig_p)

# POTÁSSIO (K)
with col4:
    # Explica Seção
    st.markdown("### 🟢 Potássio (K)")
    st.markdown("_Presença = 1 · Ausência = 0_")

    # Plota Gráfico e Ajusta Visual
    fig_k, ax_k = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df, x="timestamp", y="potassio", color="seagreen", ax=ax_k)
    ax_k.set_title("Potássio (K)")
    ax_k.set_yticks([0, 1])
    ax_k.set_yticklabels(["Ausente", "Presente"])
    ax_k.set_ylabel("Presença")
    ax_p.set_xlabel("Tempo (s)")
    plt.xticks(rotation=45)
    plt.ylim(0, 1.2)
    st.pyplot(fig_k)

# ---- Análise 4 (interativa)
# Título
st.header('Análise Interativa')
# Seleção de variáveis pelo usuário
st.subheader('Gráfico de Dispersão Interativo')

col1, col2, col3 = st.columns(3)
columns_numeric= ["timestamp","fosforo", "potassio", "ph", "umidade", "status_bomba"]
with col1:
    x_var = st.selectbox('Selecione a variável X:', options=columns_numeric)
with col2:
    y_var = st.selectbox('Selecione a variável Y:', options=columns_numeric)
with col3:
    color_var = st.selectbox('Selecione a variável para colorir:', options=columns_numeric)

if x_var in df.columns and y_var in df.columns:
    corr_temp_prod = df[[x_var,y_var]].corr().iloc[0,1]
    st.write(f"A correlação de Pearson entre {y_var} e {x_var} é: {corr_temp_prod:.2f}")

# Plota Gráfico e Ajusta Visual
fig_int, ax_int = plt.subplots(figsize=(12, 3))
sns.barplot(data=df, x=x_var, y=y_var, hue=color_var, ax=ax_int)
ax_int.set_title(f'{y_var} x {x_var} colorido por {color_var}')
ax_int.set_ylabel(y_var)
ax_int.set_xlabel(x_var)
st.pyplot(fig_int)

