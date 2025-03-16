import streamlit as st
import pandas as pd
import altair as alt

# ================== CONFIGURAÇÃO DO DASHBOARD ==================
st.set_page_config(page_title="Dashboard de Unidades Interligadas", layout="wide")
st.title("\ud83d\udcca Dashboard de Unidades Interligadas")

# ================== CARREGAR DADOS DO GOOGLE SHEETS ==================
@st.cache_data
def load_data(sheet_url):
    df = pd.read_csv(sheet_url)
    return df

# ================== URLs das abas ==================
sheet_urls = {
    "UNIDADES INTERLIGADAS": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=UNIDADES%20INTERLIGADAS",
    "STATUS RECEB FORMULARIO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=STATUS%20RECEB%20FORMULARIO",
    "MUNICIPIOS PARA INSTALAR": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUNICIPIOS%20PARA%20INSTALAR",
    "MUN INVIAVEIS DE INSTALACAO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUN%20INVIAVEIS%20DE%20INSTALACAO"
}

# ================== BARRA LATERAL - SELEÇÃO DE ABA ==================
st.sidebar.header("\ud83d\udcc2 Seleção de Aba")
tabs = list(sheet_urls.keys())
selected_tab = st.sidebar.radio("Selecione uma aba:", tabs)

# ================== CARREGAR DADOS DA ABA SELECIONADA ==================
df = load_data(sheet_urls[selected_tab])

# ================== ABA 1: UNIDADES INTERLIGADAS ==================
if selected_tab == "UNIDADES INTERLIGADAS":
    st.header("\ud83c\udfe5 Unidades Interligadas")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())
    esfera = st.sidebar.multiselect("Esfera", df["ESFERA"].unique(), default=df["ESFERA"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS"].isin(municipios)) &
        (df["ESFERA"].isin(esfera))
    ]

    st.write(f"### \ud83d\udccc {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    pie_data = df_filtrado['SITUAÇÃO GERAL'].value_counts().reset_index()
    pie_data.columns = ['Situação Geral', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Situação Geral", type="nominal")
    ).properties(title="Distribuição da Situação Geral")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("\ud83d\udcc5 Baixar Dados", df_filtrado.to_csv(index=False), "unidades_interligadas.csv")

# ================== ABA 2: STATUS RECEB FORMULARIO ==================
elif selected_tab == "STATUS RECEB FORMULARIO":
    st.header("\ud83d\udcc4 Status Recebimento Formulário")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())
    status = st.sidebar.multiselect("Status Geral Recebimento", df["STATUS GERAL RECEBIMENTO"].unique(), default=df["STATUS GERAL RECEBIMENTO"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS"].isin(municipios)) &
        (df["STATUS GERAL RECEBIMENTO"].isin(status))
    ]

    st.write(f"### \ud83d\udccc {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    pie_data = df_filtrado['STATUS GERAL RECEBIMENTO'].value_counts().reset_index()
    pie_data.columns = ['Status', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Status", type="nominal")
    ).properties(title="Distribuição do Status de Recebimento")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("\ud83d\udcc5 Baixar Dados", df_filtrado.to_csv(index=False), "status_recebimento.csv")

# ================== ABA 3: MUNICIPIOS PARA INSTALAR ==================
elif selected_tab == "MUNICIPIOS PARA INSTALAR":
    st.header("\ud83d\udd39 Municípios para Instalar")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07)"].unique(), default=df["MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07)"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07)"].isin(municipios))
    ]

    st.write(f"### \ud83d\udccc {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    st.sidebar.download_button("\ud83d\udcc5 Baixar Dados", df_filtrado.to_csv(index=False), "municipios_para_instalar.csv")

# ================== ABA 4: MUN INVIAVEIS DE INSTALACAO ==================
elif selected_tab == "MUN INVIAVEIS DE INSTALACAO":
    st.header("\ud83d\udd12 Municípios Inviáveis para Instalação")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS"].isin(municipios))
    ]

    st.write(f"### \ud83d\udccc {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    pie_data = df_filtrado['SITUAÇÃO'].value_counts().reset_index()
    pie_data.columns = ['Situação', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Situação", type="nominal")
    ).properties(title="Distribuição das Situações")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("\ud83d\udcc5 Baixar Dados", df_filtrado.to_csv(index=False), "municipios_inviaveis.csv")

# ================== MENSAGEM FINAL ==================
st.success("\u2705 Dashboard atualizado com os dados das abas do Google Sheets!")
