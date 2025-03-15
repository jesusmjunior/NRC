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

# Verificar as colunas do DataFrame (para diagnóstico)
st.write("Colunas do DataFrame:", df.columns)

# Configuração do Dashboard
st.set_page_config(page_title="Dashboard Interativo - Sistema de Saúde", layout="wide")
st.title("📊 Dashboard Interativo - Sistema de Saúde")

# Filtros dinâmicos na barra lateral
st.sidebar.header("🔎 Filtros")
municipios = st.sidebar.multiselect("Selecione os Municípios", df["Municípios"].unique(), default=df["Municípios"].unique())  # Ajuste o nome da coluna se necessário
esferas = st.sidebar.multiselect("Selecione as Esferas", df["Esferas"].unique(), default=df["Esferas"].unique())

# Aplicar filtros aos dados
df_filtrado = df[df["Municípios"].isin(municipios) & df["Esferas"].isin(esferas)]

# Exibir os dados filtrados
st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
st.dataframe(df_filtrado)

# Funções para gráficos de distribuição com Altair
def plot_unidades_interligadas(df):
    """Gráfico de unidades interligadas por Municípios"""
    st.write("### 📊 Distribuição das Unidades Interligadas por Municípios")
    chart = alt.Chart(df).mark_bar().encode(
        x='Municípios',
        y='Índices IBGE',
        tooltip=['Municípios', 'Índices IBGE']
    ).properties(title="Distribuição por Índice IBGE")
    st.altair_chart(chart, use_container_width=True)

def plot_status_formulario(df):
    """Gráfico de status de recebimento de formulários"""
    st.write("### 📊 Status de Recebimento de Formulários")
    chart = alt.Chart(df).mark_arc().encode(
        theta='count():Q',
        color='Status Geral Recebimento:N',
        tooltip=['Status Geral Recebimento', 'count():Q']
    ).properties(title="Status Geral de Recebimento")
    st.altair_chart(chart, use_container_width=True)

def plot_municipios_instalacao(df):
    """Gráfico de Municípios em Fase de Instalação"""
    st.write("### 📊 Municípios em Fase de Instalação")
    chart = alt.Chart(df).mark_bar().encode(
        x='Municípios',
        y='Fase do Processo',
        tooltip=['Municípios', 'Fase do Processo']
    ).properties(title="Fase do Processo de Instalação")
    st.altair_chart(chart, use_container_width=True)

def plot_municipios_inviaveis(df):
    """Gráfico de Municípios Inviáveis de Instalação"""
    st.write("### 📊 Municípios Inviáveis de Instalação")
    chart = alt.Chart(df).mark_bar().encode(
        x='Municípios',
        y='Situação',
        tooltip=['Municípios', 'Situação']
    ).properties(title="Situação dos Municípios Inviáveis")
    st.altair_chart(chart, use_container_width=True)

def plot_termo_cooperacao(df):
    st.write("### 📊 Termo de Cooperação (Provisão 09)")
    chart = alt.Chart(df).mark_arc().encode(
        theta='count():Q',
        color='Municípios que Assinaram o TCT:N',
        tooltip=['Municípios que Assinaram o TCT', 'count():Q']
    ).properties(title="Termo de Cooperação Assinado ou Pendente")
    st.altair_chart(chart, use_container_width=True)

def plot_operadores(df):
    st.write("### 📊 Operadores e Responsáveis")
    chart = alt.Chart(df).mark_bar().encode(
        x='UI e Serventia Conveniada',
        y='Operador/Preposto da UI',
        tooltip=['UI e Serventia Conveniada', 'Operador/Preposto da UI']
    ).properties(title="Operadores Responsáveis")
    st.altair_chart(chart, use_container_width=True)

def plot_acompanhamento_articulacao(df):
    st.write("### 📊 Acompanhamento de Articulação")
    chart = alt.Chart(df).mark_bar().encode(
        x='Municípios',
        y='Por Ano (2022)',
        tooltip=['Municípios', 'Por Ano (2022)']
    ).properties(title="Acompanhamento Articulação")
    st.altair_chart(chart, use_container_width=True)

# Seções do Dashboard
tabs = [
    "Unidades Interligadas", "Status Recebimento Formulário", "Municípios em Fase de Instalação",
    "Municípios Inviáveis de Instalação", "Termo de Cooperação", "Operadores",
    "Hospitais das UI", "Acompanhamento Articulação"
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
    plot_operadores(df_filtrado)
elif selected_tab == "Acompanhamento Articulação":
    plot_acompanhamento_articulacao(df_filtrado)
elif selected_tab == "Municípios Inviáveis de Instalação":
    plot_municipios_inviaveis(df_filtrado)
elif selected_tab == "Termo de Cooperação":
    plot_termo_cooperacao(df_filtrado)

# Baixar dados filtrados
st.sidebar.download_button("📥 Baixar Dados Filtrados", df_filtrado.to_csv(index=False), "dados_filtrados.csv", "text/csv")
