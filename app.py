import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração do Dashboard
st.set_page_config(page_title="Dashboard Sistema Saúde", layout="wide")
st.title("📊 Dashboard - Sistema de Saúde")

# ================== CONEXÃO COM GOOGLE SHEETS ==================
@st.cache_resource
def load_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/edit")
    worksheet = sheet.worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# ================== BARRA LATERAL - NAVEGAÇÃO ==================
st.sidebar.title("📂 Navegação")
tabs = ["Unidades Interligadas", 
        "Status Recebimento Formulário", 
        "Municípios para Instalar 1", 
        "Municípios para Instalar 2", 
        "Municípios Inviáveis", 
        "Provimento 09 - TCT"]
selected_tab = st.sidebar.radio("Selecione uma aba:", tabs)

# ================== ABA 1 - UNIDADES INTERLIGADAS ==================
if selected_tab == "Unidades Interligadas":
    st.header("🏥 Unidades Interligadas")
    df = load_data("UNIDADES INTERLIGADAS")

    municipios = st.sidebar.multiselect("Selecione os Municípios:", df['MUNICÍPIOS'].unique(), default=df['MUNICÍPIOS'].unique())
    df = df[df['MUNICÍPIOS'].isin(municipios)]

    # KPIs
    st.metric("Total Hospitais", df.shape[0])
    st.metric("Com Justiça Aberta", df['JUSTIÇA ABERTA'].value_counts().get("Sim", 0))
    st.metric("Habilitação CRC OK", df['HABILITAÇÃO CRC'].value_counts().get("Habilitado", 0))

    # Gráficos
    fig = px.bar(df, x="MUNICÍPIOS", y="ÍNDICES IBGE", color="SITUAÇÃO GERAL", title="Distribuição por Municípios")
    st.plotly_chart(fig)

    pie_fig = px.pie(df, names="SITUAÇÃO GERAL", title="Situação Geral das Unidades")
    st.plotly_chart(pie_fig)

    # Tabela e Download
    st.dataframe(df)
    st.download_button("📥 Baixar Dados", df.to_csv(index=False), file_name="unidades_interligadas.csv")

# ================== ABA 2 - STATUS RECEBIMENTO ==================
elif selected_tab == "Status Recebimento Formulário":
    st.header("📄 Status de Recebimento de Formulário")
    df = load_data("STATUS RECEB FORMULARIO")

    municipios = st.sidebar.multiselect("Selecione os Municípios:", df['MUNICÍPIOS'].unique(), default=df['MUNICÍPIOS'].unique())
    df = df[df['MUNICÍPIOS'].isin(municipios)]

    # KPIs
    total = len(df)
    recebidos = df['STATUS GERAL RECEBIMENTO'].value_counts().get('Recebido', 0)
    faltantes = total - recebidos
    st.metric("Recebidos", recebidos)
    st.metric("Faltantes", faltantes)

    # Gráfico
    pie_fig = px.pie(df, names="STATUS GERAL RECEBIMENTO", title="Status Geral Recebimento")
    st.plotly_chart(pie_fig)

    # Tabela e Download
    st.dataframe(df)
    st.download_button("📥 Baixar Dados", df.to_csv(index=False), file_name="status_recebimento.csv")

# ================== ABA 3 - MUNICÍPIOS PARA INSTALAR 1 ==================
elif selected_tab == "Municípios para Instalar 1":
    st.header("🏗️ Municípios para Instalar - Prov. 07")
    df = load_data("MUNICÍPIOS PARA INSTALAR")

    fase = st.sidebar.multiselect("Filtrar por Fase:", df['FASE'].unique(), default=df['FASE'].unique())
    df = df[df['FASE'].isin(fase)]

    st.bar_chart(df['FASE'].value_counts())

    st.dataframe(df)
    st.download_button("📥 Baixar Dados", df.to_csv(index=False), file_name="municipios_instalar.csv")

# ================== ABA 4 - MUNICÍPIOS PARA INSTALAR 2 ==================
elif selected_tab == "Municípios para Instalar 2":
    st.header("🏗️ Municípios para Instalar - Prov. 07 (Parte 2)")
    df = load_data("MUNICÍPIOS PARA INSTALAR 2")

    fase = st.sidebar.multiselect("Filtrar por Fase:", df['FASE'].unique(), default=df['FASE'].unique())
    df = df[df['FASE'].isin(fase)]

    st.bar_chart(df['FASE'].value_counts())

    st.dataframe(df)
    st.download_button("📥 Baixar Dados", df.to_csv(index=False), file_name="municipios_instalar_2.csv")

# ================== ABA 5 - MUNICÍPIOS INVIÁVEIS ==================
elif selected_tab == "Municípios Inviáveis":
    st.header("🚫 Municípios Inviáveis para Instalação")
    df = load_data("MUN. INVIÁVEIS DE INSTALAÇÃO")

    st.bar_chart(df['SITUAÇÃO'].value_counts())

    st.dataframe(df)
    st.download_button("📥 Baixar Dados", df.to_csv(index=False), file_name="municipios_inviaveis.csv")

# ================== ABA 6 - PROVIMENTO 09 ==================
elif selected_tab == "Provimento 09 - TCT":
    st.header("📜 Provimento 09 - Termo de Cooperação Técnica (TCT)")
    df = load_data("PROVIMENTO 09")

    assinados = df['MUNICÍPIOS QUE ASSINARAM O TCT'].dropna().count()
    vao_assinar = df['MUNICÍPIOS VÃO ASSINAR O TCT'].dropna().count()

    # KPIs
    st.metric("Assinaram o TCT", assinados)
    st.metric("Vão Assinar", vao_assinar)

    # Gráfico
    tct_df = pd.DataFrame({
        'Status': ['Assinaram', 'Vão Assinar'],
        'Total': [assinados, vao_assinar]
    })
    fig = px.pie(tct_df, names='Status', values='Total', title="Status do Termo de Cooperação")
    st.plotly_chart(fig)

    st.dataframe(df)
    st.download_button("📥 Baixar Dados", df.to_csv(index=False), file_name="provimento09_tct.csv")
