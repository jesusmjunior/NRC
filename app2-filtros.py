import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import traceback

# ================== CONFIGURAÇÃO DO DASHBOARD ==================
st.set_page_config(
    page_title="Dashboard UI - Parte 2", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard UI - Parte 2")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ================== CARREGAR DADOS DO GOOGLE SHEETS ==================
@st.cache_data(ttl=3600)
def load_data(sheet_url):
    try:
        df = pd.read_csv(sheet_url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.error(traceback.format_exc())
        return pd.DataFrame()

# ================== URLs das abas ==================
sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

sheet_urls = {
    "MUN. INVIÁVEIS DE INSTALAÇÃO": f"{base_url}MUN.%20INVI%C3%81VEIS%20DE%20INSTALA%C3%87%C3%83O",
    "MUNICÍPIOS PARA REATIVA": f"{base_url}MUNIC%C3%8DPIOS%20PARA%20REATIVA",
    "TAB ACOMPANHAMENTO ARTICULAÇÃO": f"{base_url}TAB%20ACOMPANHAMENTO%20ARTICULA%C3%87%C3%83O",
    "ÍNDICES DE SUB-REGISTRO": f"{base_url}%C3%8DNDICES%20DE%20SUB-REGISTRO"
}

# ================== BARRA LATERAL - SELEÇÃO DE ABA ==================
st.sidebar.header("📂 Seleção de Aba")
tabs = list(sheet_urls.keys())
selected_tab = st.sidebar.radio("Selecione uma aba:", tabs)

# ================== LOADING SPINNER ==================
with st.spinner(f"Carregando dados de {selected_tab}..."):
    df = load_data(sheet_urls[selected_tab])

if df.empty:
    st.error(f"Não foi possível carregar os dados da aba {selected_tab}.")
    st.stop()

# ================== FUNÇÕES AUXILIARES ==================
def create_download_button(dataframe, filename):
    csv = dataframe.to_csv(index=False, encoding='utf-8-sig')
    return st.sidebar.download_button(
        label="📥 Baixar Dados",
        data=csv.encode('utf-8-sig'),
        file_name=filename,
        mime='text/csv'
    )

def show_data_summary(dataframe):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de registros", dataframe.shape[0])
    with col2:
        st.metric("Colunas disponíveis", dataframe.shape[1])
    with col3:
        st.metric("Última atualização", datetime.now().strftime("%d/%m/%Y"))

# ================== ABA 5: MUN. INVIÁVEIS DE INSTALAÇÃO ==================
if selected_tab == "MUN. INVIÁVEIS DE INSTALAÇÃO":
    st.header("🚫 Municípios Inviáveis de Instalação")
    try:
        col_municipios = "MUNICÍPIOS"
        col_situacao = "SITUAÇÃO"
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )
        situacao = st.sidebar.multiselect(
            "Situação", 
            df[col_situacao].unique(), 
            default=df[col_situacao].unique()
        )
        df_filtrado = df[(df[col_municipios].isin(municipios)) & (df[col_situacao].isin(situacao))]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        create_download_button(df_filtrado, "municipios_inviaveis.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 7: MUNICÍPIOS PARA REATIVA ==================
elif selected_tab == "MUNICÍPIOS PARA REATIVA":
    st.header("🔄 Municípios para Reativação")
    try:
        col_municipios = "MUNICÍPIO"
        col_hospital = "HOSPITAL/MATERNIDADE"
        col_esfera = "ESFERA"
        col_serventia = "SERVENTIA"
        col_situacao = "SITUAÇÃO"

        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", df[col_municipios].unique(), default=df[col_municipios].unique()
        )
        situacao = st.sidebar.multiselect(
            "Situação", df[col_situacao].unique(), default=df[col_situacao].unique()
        )

        df_filtrado = df[(df[col_municipios].isin(municipios)) & (df[col_situacao].isin(situacao))]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        create_download_button(df_filtrado, "municipios_reativa.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 8: TAB ACOMPANHAMENTO ARTICULAÇÃO ==================
elif selected_tab == "TAB ACOMPANHAMENTO ARTICULAÇÃO":
    st.header("📑 Acompanhamento da Articulação")
    try:
        col_situacao = "SITUAÇÃO"
        col_municipios = "MUNICÍPIOS"

        situacao = st.sidebar.multiselect(
            "Selecione a Situação", df[col_situacao].unique(), default=df[col_situacao].unique()
        )
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", df[col_municipios].unique(), default=df[col_municipios].unique()
        )

        df_filtrado = df[(df[col_situacao].isin(situacao)) & (df[col_municipios].isin(municipios))]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        create_download_button(df_filtrado, "acompanhamento_articulacao.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 9: ÍNDICES DE SUB-REGISTRO ==================
elif selected_tab == "ÍNDICES DE SUB-REGISTRO":
    st.header("📉 Índices de Sub-registro")
    try:
        col_cidade = "CIDADE"
        cidades = st.sidebar.multiselect(
            "Selecione as Cidades", df[col_cidade].unique(), default=df[col_cidade].unique()
        )

        df_filtrado = df[df[col_cidade].isin(cidades)]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        create_download_button(df_filtrado, "indices_subregistro.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba: {str(e)}")
        st.error(traceback.format_exc())

# ================== MENSAGEM FINAL ==================
st.success("✅ Dashboard atualizado com os dados das abas do Google Sheets!")
