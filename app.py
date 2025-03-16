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
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove colunas Unnamed
    return df

# ================== URLs das abas ==================
sheet_urls = {
    "UNIDADES INTERLIGADAS": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=UNIDADES%20INTERLIGADAS",
    "STATUS RECEB FORMULARIO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=STATUS%20RECEB%20FORMULARIO",
    "MUNICIPIOS PARA INSTALAR": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUNICIPIOS%20PARA%20INSTALAR",
    "MUN INVIAVEIS DE INSTALACAO": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUN%20INVIAVEIS%20DE%20INSTALACAO",
    "PROVIMENTO 09": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=PROVIMENTO%2009",
    "MUNICIPIOS PARA REATIVA": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=MUNICIPIOS%20PARA%20REATIVA",
    "CIDADES COM SELO UNICEF": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=CIDADES%20COM%20SELO%20UNICEF",
    "SUB-REGISTRO 2023": "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/gviz/tq?tqx=out:csv&sheet=SUB-REGISTRO%202023"
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

    pie_data = df_filtrado['STATUS GERAL RECEBIMENTO'].value_counts().reset_index()
    pie_data.columns = ['Status', 'Total']
    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Status", type="nominal")
    ).properties(title="Distribuição do Status de Recebimento")
    st.altair_chart(pie_chart, use_container_width=True)

    st.sidebar.download_button("📥 Baixar Dados", df_filtrado.to_csv(index=False), "status_recebimento.csv")

# ================== ABA 3: MUNICIPIOS PARA INSTALAR ==================
elif selected_tab == "MUNICIPIOS PARA INSTALAR":
    st.header("🔹 Municípios para Instalar")

    municipios = st.sidebar.multiselect("Selecione os Municípios", df["MUNICÍPIOS"].unique(), default=df["MUNICÍPIOS"].unique())

    df_filtrado = df[
        (df["MUNICÍPIOS"].isin(municipios))
    ]

    st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    st.sidebar.download_button("📥 Baixar Dados", df_filtrado.to_csv(index=False), "municipios_para_instalar.csv")

# ================== ABA 4: MUN INVIAVEIS DE INSTALACAO ==================
elif selected_tab == "MUN INVIAVEIS DE INSTALACAO":
    st.header("🔒 Municípios Inviáveis para Instalação")

    # Corrigindo os campos
    municipios = st.sidebar.multiselect(
        "Selecione os Municípios", 
        df["MUNICÍPIO"].unique(), 
        default=df["MUNICÍPIO"].unique()
    )

    situacoes = st.sidebar.multiselect(
        "Selecione a Situação", 
        df["SITUAÇÃO"].unique(), 
        default=df["SITUAÇÃO"].unique()
    )

    df_filtrado = df[
        (df["MUNICÍPIO"].isin(municipios)) &
        (df["SITUAÇÃO"].isin(situacoes))
    ]

    st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
    st.dataframe(df_filtrado)

    # Gráfico Pizza - Distribuição das Situações
    situacao_data = df_filtrado['SITUAÇÃO'].value_counts().reset_index()
    situacao_data.columns = ['Situação', 'Total']
    pie_chart = alt.Chart(situacao_data).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Situação", type="nominal")
    ).properties(title="Distribuição da Situação dos Municípios Inviáveis")
    st.altair_chart(pie_chart, use_container_width=True)

    # Download corrigido
    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
    st.sidebar.download_button(
        "📥 Baixar Dados", 
        data=csv.encode('utf-8-sig'), 
        file_name="municipios_inviaveis.csv", 
        mime='text/csv'
    )

# ================== ABA 5: PROVIMENTO 09 ==================
elif selected_tab == "PROVIMENTO 09":
    st.header("📜 Provimento 09")

    st.dataframe(df)

    st.sidebar.download_button("📥 Baixar Dados", df.to_csv(index=False), "provimento_09.csv")

# ================== ABA 6: MUNICIPIOS PARA REATIVA ==================
elif selected_tab == "MUNICIPIOS PARA REATIVA":
    st.header("🔄 Municípios para Reativação")

    st.dataframe(df)

    st.sidebar.download_button("📥 Baixar Dados", df.to_csv(index=False), "municipios_reativa.csv")

# ================== ABA 7: CIDADES COM SELO UNICEF ==================
elif selected_tab == "CIDADES COM SELO UNICEF":
    st.header("🏅 Cidades com Selo UNICEF")

    st.dataframe(df)

    st.sidebar.download_button("📥 Baixar Dados", df.to_csv(index=False), "cidades_selo_unicef.csv")

# ================== ABA 8: SUB-REGISTRO 2023 ==================
elif selected_tab == "SUB-REGISTRO 2023":
    st.header("📉 Sub-registro 2023")

    st.dataframe(df)

    st.sidebar.download_button("📥 Baixar Dados", df.to_csv(index=False), "subregistro_2023.csv")

# ================== MENSAGEM FINAL ==================
st.success("✅ Dashboard atualizado com os dados das abas do Google Sheets!")
