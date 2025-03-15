import streamlit as st
import pandas as pd
import plotly.express as px

# URL do Google Sheets (compartilhada publicamente)
sheet_url = "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/export?format=csv&id=1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq&gid=666685797"

# Carregar os dados do Google Sheets (via CSV)
@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    return df

df = load_data()

# Configuração do Dashboard
st.set_page_config(page_title="Dashboard Interativo - Sistema de Saúde", layout="wide")
st.title("📊 Dashboard Interativo - Sistema de Saúde")

# Filtros dinâmicos
st.sidebar.header("🔎 Filtros")
municipios = st.sidebar.multiselect("Selecione os Municípios", df["Municípios"].unique(), default=df["Municípios"].unique())
esferas = st.sidebar.multiselect("Selecione as Esferas", df["Esferas"].unique(), default=df["Esferas"].unique())

# Aplicar os filtros aos dados
df_filtrado = df[df["Municípios"].isin(municipios) & df["Esferas"].isin(esferas)]

# Exibir a tabela filtrada
st.write(f"### 📌 {df_filtrado.shape[0]} Unidades Selecionadas")
st.dataframe(df_filtrado)

# Função de gráfico para "Unidades Interligadas"
def plot_unidades_interligadas(df):
    st.write("### 📊 Distribuição de Unidades Interligadas por Municípios")
    fig = px.bar(df, x="Municípios", y="Índices IBGE", title="Distribuição por Índice IBGE")
    st.plotly_chart(fig)

# Função para "Status de Recebimento de Formulários"
def plot_status_formulario(df):
    st.write("### 📊 Status de Recebimento de Formulários")
    fig_status = px.pie(df, names="Status Geral Recebimento", title="Status Geral de Recebimento")
    st.plotly_chart(fig_status)

# Função para "Fase de Instalação"
def plot_fase_instalacao(df):
    st.write("### 📊 Fase do Processo de Instalação")
    fig_fase = px.bar(df, x="Municípios", y="Fase do Processo", title="Fase de Instalação dos Municípios")
    st.plotly_chart(fig_fase)

# Função para "Hospitais das UI Municípios com UI"
def plot_hospitais_ui(df):
    st.write("### 📊 Hospitais Fora da Lista Alice")
    fig_hospitais = px.bar(df, x="Municípios", y="Hospitais Fora da Lista Alice", title="Hospitais Fora da Lista Alice")
    st.plotly_chart(fig_hospitais)

# Função para "UI Paralisadas e Sem Contato"
def plot_ui_paralisadas(df):
    st.write("### 📊 UI Paralisadas e Sem Contato")
    fig_paralisadas = px.bar(df, x="Unidades Paralisadas", y="Situação", title="UI Paralisadas e Sem Contato")
    st.plotly_chart(fig_paralisadas)

# Função para "Cidades com Selo UNICEF"
def plot_cidades_unicef(df):
    st.write("### 📊 Cidades com Selo UNICEF")
    fig_unicef = px.bar(df, x="Cidades com Selo UNICEF", y="Com ou Sem UI", title="Cidades com Selo UNICEF e Unidades Interligadas")
    st.plotly_chart(fig_unicef)

# Funções para cada aba
def plot_municipios_instalacao(df):
    st.write("### 📊 Municípios em Fase de Instalação")
    fig_instalacao = px.bar(df, x="Municípios", y="Fase do Processo", title="Fase de Instalação dos Municípios")
    st.plotly_chart(fig_instalacao)

def plot_municipios_inviaveis(df):
    st.write("### 📊 Municípios Inviáveis de Instalação")
    fig_inviaveis = px.bar(df, x="Municípios", y="Situação", title="Situação dos Municípios Inviáveis")
    st.plotly_chart(fig_inviaveis)

def plot_termo_cooperacao(df):
    st.write("### 📊 Termo de Cooperação (Provisão 09)")
    fig_termo = px.pie(df, names="Municípios que Assinaram o TCT", title="Termo de Cooperação Assinado ou Pendente")
    st.plotly_chart(fig_termo)

def plot_operadores(df):
    st.write("### 📊 Operadores e Responsáveis")
    fig_operadores = px.bar(df, x="UI e Serventia Conveniada", y="Operador/Preposto da UI", title="Operadores Responsáveis")
    st.plotly_chart(fig_operadores)

# Seções do Dashboard
tabs = ["Unidades Interligadas", "Status Recebimento Formulário", "Municípios em Fase de Instalação", 
        "Municípios Inviáveis de Instalação", "Termo de Cooperação", "Operadores", 
        "Hospitais das UI", "UI Paralisadas", "Horários de Funcionamento", "Cidades com Selo UNICEF"]

selected_tab = st.sidebar.selectbox("Escolha a Seção", tabs)

# Exibindo diferentes seções com base na escolha do usuário
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
