import streamlit as st
import pandas as pd
import altair as alt

# ================== CONFIGURAÇÃO DO DASHBOARD ==================
st.set_page_config(page_title="Dashboard de Unidades Interligadas", layout="wide")
st.title("📊 Dashboard de Unidades Interligadas")

# ================== CARREGAR DADOS DO GOOGLE SHEETS ==================
@st.cache_data
def load_data(sheet_url):
    df = pd.read_csv(sheet_url)
    return df

# URLs das abas
sheet_urls = {
    "UNIDADES INTERLIGADAS": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=UNIDADES%20INTERLIGADAS",
    "STATUS RECEB FORMULARIO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=STATUS%20RECEB%20FORMULARIO",
    "MUNICÍPIOS PARA INSTALAR": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUNICÍPIOS%20PARA%20INSTALAR",
    "MUN. INVIÁVEIS DE INSTALAÇÃO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUN.%20INVIÁVEIS%20DE%20INSTALAÇÃO"
}

# ================== BARRA LATERAL - SELEÇÃO DE ABA ==================
st.sidebar.header("📂 Seleção de Aba")
tabs = list(sheet_urls.keys())
selected_tab = st.sidebar.radio("Selecione uma aba:", tabs)

# ================== CARREGAR DADOS DA ABA SELECIONADA ==================
df = load_data(sheet_urls[selected_tab])

# ================== ABA 1: UNIDADES INTERLIGADAS ==================
if selected_tab == "UNIDADES INTERLIGADAS":
    st.header("🏥 Unidades Interligadas")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())
    esfera = st.sidebar.multiselect("Esfera", df["ESFERA"].unique(), default=df["ESFERA"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS"].isin(municipios)) &
        (df["ESFERA"].isin(esfera))
    ]

    st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    # Gráfico Pie - Situação Geral
    pie_data = df_filtrado['SITUAÇÃO GERAL'].value_counts().reset_index()
    pie_data.columns = ['Situação Geral', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Situação Geral", type="nominal")
    ).properties(title="Distribuição da Situação Geral")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("📥 Baixar Dados", df_filtrado.to_csv(index=False), "unidades_interligadas.csv")

# ================== ABA 2: STATUS RECEB FORMULARIO ==================
elif selected_tab == "STATUS RECEB FORMULARIO":
    st.header("📄 Status Recebimento Formulário")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())
    status = st.sidebar.multiselect("Status Geral Recebimento", df["STATUS GERAL RECEBIMENTO"].unique(), default=df["STATUS GERAL RECEBIMENTO"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS"].isin(municipios)) &
        (df["STATUS GERAL RECEBIMENTO"].isin(status))
    ]

    st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    # Pie Chart - Status Recebimento
    pie_data = df_filtrado['STATUS GERAL RECEBIMENTO'].value_counts().reset_index()
    pie_data.columns = ['Status', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Status", type="nominal")
    ).properties(title="Distribuição do Status de Recebimento")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("📥 Baixar Dados", df_filtrado.to_csv(index=False), "status_recebimento.csv")

# ================== ABA 3: MUNICÍPIOS PARA INSTALAR ==================
elif selected_tab == "MUNICÍPIOS PARA INSTALAR":
    st.header("🏗️ Municípios para Instalar")

    fase = st.sidebar.multiselect("Fase", df['FASE'].unique(), default=df['FASE'].unique())
    df_filtrado = df[df['FASE'].isin(fase)]

    st.write(f"### 📌 {df_filtrado.shape[0]} Municípios Selecionados")
    st.dataframe(df_filtrado)

    # Bar Chart - Distribuição por Fase
    fase_data = df_filtrado['FASE'].value_counts().reset_index()
    fase_data.columns = ['Fase', 'Total']
    bar_chart = alt.Chart(fase_data).mark_bar().encode(
        x='Fase',
        y='Total'
    ).properties(title="Distribuição por Fase")
    st.altair_chart(bar_chart, use_container_width=True)

    st.sidebar.download_button("📥 Baixar Dados", df_filtrado.to_csv(index=False), "municipios_para_instalar.csv")

# ================== ABA 4: MUN. INVIÁVEIS DE INSTALAÇÃO ==================
elif selected_tab == "MUN. INVIÁVEIS DE INSTALAÇÃO":
    st.header("🚫 Municípios Inviáveis para Instalação")

    situacao = st.sidebar.multiselect("Situação", df['SITUAÇÃO'].unique(), default=df['SITUAÇÃO'].unique())
    df_filtrado = df[df['SITUAÇÃO'].isin(situacao)]

    st.write(f"### 📌 {df_filtrado.shape[0]} Municípios Inviáveis")
    st.dataframe(df_filtrado)

    # Pie Chart - Situação
    pie_data = df_filtrado['SITUAÇÃO'].value_counts().reset_index()
    pie_data.columns = ['Situação', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Situação", type="nominal")
    ).properties(title="Distribuição da Situação dos Municípios Inviáveis")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("📥 Baixar Dados", df_filtrado.to_csv(index=False), "municipios_inviaveis.csv")

# ================== MENSAGEM FINAL ==================
st.success("✅ Dashboard atualizado com os dados das abas do Google Sheets!")
