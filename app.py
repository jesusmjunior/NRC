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
    "STATUS RECEB FORMULARIO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=STATUS%20RECEB%20FORMULARIO"
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

# ================== MENSAGEM FINAL ==================
st.success("✅ Dashboard atualizado com os dados das abas do Google Sheets!")
