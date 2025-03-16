import streamlit as st
import pandas as pd
import altair as alt

# ================== CONFIGURAÇÃO DO DASHBOARD ==================
st.set_page_config(page_title="Dashboard de Serventias", layout="wide")
st.title("📊 Dashboard de Serventias Extrajudiciais")

# ================== CARREGAR DADOS DO GOOGLE SHEETS ==================
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1LNJIB4_jAD4luRwrqPHmiKYoX33uP2fv-r2KQuLMwQg/gviz/tq?tqx=out:csv"
    df = pd.read_csv(sheet_url)
    return df

# Carregar dados
df = load_data()

# ================== BARRA LATERAL - FILTROS ==================
st.sidebar.header("🔎 Filtros")
municipio = st.sidebar.multiselect("Selecione o Município", df["MUNICIPIO"].unique(), default=df["MUNICIPIO"].unique())
forma_ingresso = st.sidebar.multiselect("Forma de Ingresso", df["FORMA_INGRESSO"].unique(), default=df["FORMA_INGRESSO"].unique())
responsavel = st.sidebar.multiselect("Responsável", df["RESPONSAVEL"].unique(), default=df["RESPONSAVEL"].unique())

# ================== APLICAR FILTROS ==================
df_filtrado = df[
    (df["MUNICIPIO"].isin(municipio)) &
    (df["FORMA_INGRESSO"].isin(forma_ingresso)) &
    (df["RESPONSAVEL"].isin(responsavel))
]

# ================== EXIBIR RESULTADOS ==================
st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
st.dataframe(df_filtrado)

# ================== GRÁFICOS ==================

# Gráfico de Barras - Faturamento por Município
st.write("### 📊 Distribuição Geográfica de Faturamento")
bar_chart = alt.Chart(df_filtrado).mark_bar().encode(
    x=alt.X("MUNICIPIO", sort='-y'),
    y="FATURAMENTO_SEMESTRAL",
    color="MUNICIPIO"
).properties(title="Faturamento por Município")
st.altair_chart(bar_chart, use_container_width=True)

# Boxplot - Receita por Forma de Ingresso
st.write("### 📊 Comparação de Receita por Forma de Ingresso")
box_chart = alt.Chart(df_filtrado).mark_boxplot().encode(
    x="FORMA_INGRESSO",
    y="FATURAMENTO_SEMESTRAL",
    color="FORMA_INGRESSO"
).properties(title="Faturamento por Forma de Ingresso")
st.altair_chart(box_chart, use_container_width=True)

# Pie Chart - Distribuição de Responsáveis
st.write("### 📊 Distribuição de Responsáveis")
pie_data = df_filtrado['RESPONSAVEL'].value_counts().reset_index()
pie_data.columns = ['Responsável', 'Total']
pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta=alt.Theta(field="Total", type="quantitative"),
    color=alt.Color(field="Responsável", type="nominal")
).properties(title="Titulares vs. Interinos")
st.altair_chart(pie_chart, use_container_width=True)

# Scatter Plot - Correlação entre Interinidade e Receita
st.write("### 📊 Correlação entre Tempo de Interinidade e Receita")
scatter_chart = alt.Chart(df_filtrado).mark_circle(size=60).encode(
    x="PERÍODO_INTERINIDADE",
    y="FATURAMENTO_SEMESTRAL",
    color="MUNICIPIO",
    tooltip=['MUNICIPIO', 'PERÍODO_INTERINIDADE', 'FATURAMENTO_SEMESTRAL']
).properties(title="Correlação entre Interinidade e Receita")
st.altair_chart(scatter_chart, use_container_width=True)

# ================== DOWNLOAD ==================
st.sidebar.download_button("📥 Baixar Dados Filtrados", df_filtrado.to_csv(index=False), "dados_filtrados.csv", "text/csv")

st.success("✅ Dashboard atualizado automaticamente com os dados do Google Sheets!")
