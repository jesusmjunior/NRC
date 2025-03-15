import streamlit as st
import pandas as pd
import plotly.express as px

# URL da planilha do Google Sheets (compartilhada publicamente)
sheet_url = "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/export?format=csv&id=1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq&gid=666685797"

# Carregar os dados do Google Sheets com cache
@st.cache_data
def load_data():
    """Função para carregar dados da planilha do Google Sheets"""
    return pd.read_csv(sheet_url)

# Carregar os dados na variável df
df = load_data()

# Configuração do Dashboard
st.set_page_config(page_title="Dashboard Interativo - Sistema de Saúde", layout="wide")
st.title("📊 Dashboard Interativo - Sistema de Saúde")

# Filtros dinâmicos na barra lateral
st.sidebar.header("🔎 Filtros")
municipios = st.sidebar.multiselect("Selecione os Municípios", df["Municípios"].unique(), default=df["Municípios"].unique())
esferas = st.sidebar.multiselect("Selecione as Esferas", df["Esferas"].unique(), default=df["Esferas"].unique())

# Aplicar filtros aos dados
df_filtrado = df[df["Municípios"].isin(municipios) & df["Esferas"].isin(esferas)]

# Exibir os dados filtrados
st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
st.dataframe(df_filtrado)

# Funções para gráficos de distribuição
def plot_unidades_interligadas(df):
    """Gráfico de distribuição das Unidades Interligadas por Municípios"""
    st.write("### 📊 Distribuição das Unidades Interligadas por Municípios")
    fig = px.bar(df, x="Municípios", y="Índices IBGE", title="Distribuição por Índice IBGE")
    st.plotly_chart(fig)

def plot_status_formulario(df):
    """Gráfico de status de recebimento de formulários"""
    st.write("### 📊 Status de Recebimento de Formulários")
    fig = px.pie(df, names="Status Geral Recebimento", title="Status Geral de Recebimento")
    st.plotly_chart(fig)

def plot_fase_instalacao(df):
    """Gráfico da fase de instalação dos municípios"""
    st.write("### 📊 Fase de Instalação dos Municípios")
    fig = px.bar(df, x="Municípios", y="Fase do Processo", title="Fase do Processo de Instalação")
    st.plotly_chart(fig)

def plot_hospitais_ui(df):
    """Gráfico de hospitais fora da lista Alice"""
    st.write("### 📊 Hospitais Fora da Lista Alice")
    fig = px.bar(df, x="Municípios", y="Hospitais Fora da Lista Alice", title="Hospitais Fora da Lista Alice")
    st.plotly_chart(fig)

def plot_ui_paralisadas(df):
    """Gráfico de Unidades Interligadas Paralisadas e Sem Contato"""
    st.write("### 📊 UI Paralisadas e Sem Contato")
    fig = px.bar(df, x="Unidades Paralisadas", y="Situação", title="UI Paralisadas e Sem Contato")
    st.plotly_chart(fig)

def plot_cidades_unicef(df):
    """Gráfico de Cidades com Selo UNICEF"""
    st.write("### 📊 Cidades com Selo UNICEF")
    fig = px.bar(df, x="Cidades com Selo UNICEF", y="Com ou Sem UI", title="Cidades com Selo UNICEF e Unidades Interligadas")
    st.plotly_chart(fig)

# Funções para outras seções
def plot_municipios_instalacao(df):
    """Gráfico de Municípios em Fase de Instalação"""
    st.write("### 📊 Municípios em Fase de Instalação")
    fig = px.bar(df, x="Municípios", y="Fase do Processo", title="Fase de Instalação dos Municípios")
    st.plotly_chart(fig)

def plot_municipios_inviaveis(df):
    """Gráfico de Municípios Inviáveis de Instalação"""
    st.write("### 📊 Municípios Inviáveis de Instalação")
    fig = px.bar(df, x="Municípios", y="Situação", title="Situação dos Municípios Inviáveis")
    st.plotly_chart(fig)

def plot_termo_cooperacao(df):
    """Gráfico de Termo de Cooperação (Provisão 09)"""
    st.write("### 📊 Termo de Cooperação (Provisão 09)")
    fig = px.pie(df, names="Municípios que Assinaram o TCT", title="Termo de Cooperação Assinado ou Pendente")
    st.plotly_chart(fig)

def plot_operadores(df):
    """Gráfico de Operadores e Responsáveis"""
    st.write("### 📊 Operadores e Responsáveis")
    fig = px.bar(df, x="UI e Serventia Conveniada", y="Operador/Preposto da UI", title="Operadores Responsáveis")
    st.plotly_chart(fig)

# Seções do Dashboard
tabs = [
    "Unidades Interligadas", "Status Recebimento Formulário", "Municípios em Fase de Instalação",
    "Municípios Inviáveis de Instalação", "Termo de Cooperação", "Operadores",
    "Hospitais das UI", "UI Paralisadas", "Horários de Funcionamento", "Cidades com Selo UNICEF"
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
elif selected_tab == "Hospitais das UI":
    plot_hospitais_ui(df_filtrado)
elif selected_tab == "UI Paralisadas":
    plot_ui_paralisadas(df_filtrado)
elif selected_tab == "Cidades com Selo UNICEF":
    plot_cidades_unicef(df_filtrado)
elif selected_tab == "Municípios Inviáveis de Instalação":
    plot_municipios_inviaveis(df_filtrado)
elif selected_tab == "Termo de Cooperação":
    plot_termo_cooperacao(df_filtrado)
elif selected_tab == "Operadores":
    plot_operadores(df_filtrado)

# Baixar dados filtrados
st.sidebar.download_button("📥 Baixar Dados Filtrados", df_filtrado.to_csv(index=False), "dados_filtrados.csv", "text/csv")
