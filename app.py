import streamlit as st
import pandas as pd
import altair as alt

# Link da planilha do Google Sheets (compartilhada publicamente)
sheet_url = "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/export?format=csv&id=1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq&gid=666685797"

# Carregar os dados do Google Sheets
@st.cache_data
def load_data():
    """Função para carregar dados da planilha do Google Sheets"""
    return pd.read_csv(sheet_url)

# Carregar os dados na variável df
df = load_data()

# Configuração do Dashboard
st.set_page_config(page_title="Painel Gerencial 01 NRC", layout="wide")
st.title("📊 Painel Gerencial 01 NRC")

# Filtros dinâmicos na barra lateral
st.sidebar.header("🔎 Filtros")
municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())  # Usando o nome exato da coluna
esferas = st.sidebar.multiselect("Selecione as Esferas", df["ESFERA"].unique(), default=df["ESFERA"].unique())  # Usando o nome exato da coluna

# Aplicar filtros aos dados
df_filtrado = df[df["MUNICÍPIOS"].isin(municipios) & df["ESFERA"].isin(esferas)]

# Exibir os dados filtrados
st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
st.dataframe(df_filtrado)

# Funções para gráficos de distribuição com Altair

def plot_unidades_interligadas(df):
    st.write("### 📊 Distribuição das Unidades Interligadas por Municípios")
    chart = alt.Chart(df).mark_bar().encode(
        x='MUNICÍPIOS',
        y='ÍNDICES IBGE',
        tooltip=['MUNICÍPIOS', 'ÍNDICES IBGE']
    ).properties(title="Distribuição por Índice IBGE")
    st.altair_chart(chart, use_container_width=True)

def plot_status_formulario(df):
    st.write("### 📊 Status de Recebimento de Formulários")
    chart = alt.Chart(df).mark_arc().encode(
        theta='count():Q',
        color='STATUS GERAL RECEBIMENTO',
        tooltip=['STATUS GERAL RECEBIMENTO', 'count():Q']
    ).properties(title="Status Geral de Recebimento")
    st.altair_chart(chart, use_container_width=True)

def plot_municipios_instalacao(df):
    st.write("### 📊 Municípios em Fase de Instalação")
    chart = alt.Chart(df).mark_bar().encode(
        x='MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07):',
        y='FASE',
        tooltip=['MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07):', 'FASE']
    ).properties(title="Fase do Processo de Instalação")
    st.altair_chart(chart, use_container_width=True)

def plot_municipios_inviaveis(df):
    st.write("### 📊 Municípios Inviáveis de Instalação")
    chart = alt.Chart(df).mark_bar().encode(
        x='MUNICÍPIOS',
        y='SITUAÇÃO',
        tooltip=['MUNICÍPIOS', 'SITUAÇÃO']
    ).properties(title="Situação dos Municípios Inviáveis")
    st.altair_chart(chart, use_container_width=True)

# Seções do Dashboard
tabs = [
    "Unidades Interligadas", "Status Recebimento Formulário", "Municípios em Fase de Instalação",
    "Municípios Inviáveis de Instalação"
]

# Barra lateral para escolha de seção
selected_tab = st.sidebar.selectbox("Escolha a Seção", tabs)

# Exibindo gráficos e informações com base na seção escolhida
if selected_tab == "Unidades Interligadas":
    plot_unidades_interligadas(df_filtrado)
elif selected_tab == "Status Recebimento Formulário":
    plot_status_formulario(df_filtrado)
elif selected_tab == "Municípios em Fase de Instalação":
    plot_municipios_instalacao(df_filtrado)
elif selected_tab == "Municípios Inviáveis de Instalação":
    plot_municipios_inviaveis(df_filtrado)

# Baixar dados filtrados
st.sidebar.download_button("📥 Baixar Dados Filtrados", df_filtrado.to_csv(index=False), "dados_filtrados.csv", "text/csv")
