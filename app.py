import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime
import traceback

# ================== CONFIGURAÇÃO DO DASHBOARD ==================
st.set_page_config(
    page_title="Dashboard de Unidades Interligadas", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard de Unidades Interligadas")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ================== CARREGAR DADOS DO GOOGLE SHEETS ==================
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data(sheet_url):
    try:
        df = pd.read_csv(sheet_url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove colunas Unnamed
        df.columns = df.columns.str.strip()  # Limpa espaços extras
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.error(traceback.format_exc())
        return pd.DataFrame()

# ================== URLs das abas ==================
sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

sheet_urls = {
    "UNIDADES INTERLIGADAS": f"{base_url}UNIDADES%20INTERLIGADAS",
    "STATUS RECEB FORMULARIO": f"{base_url}STATUS%20RECEB%20FORMULARIO",
    "MUNICIPIOS PARA INSTALAR": f"{base_url}MUNICIPIOS%20PARA%20INSTALAR",
    "PROVIMENTO 09": f"{base_url}PROVIMENTO%2009"
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

# ================== ABA 1: UNIDADES INTERLIGADAS ==================
if selected_tab == "UNIDADES INTERLIGADAS":
    st.header("🏥 Unidades Interligadas")
    
    try:
        col_municipios = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"
        col_esfera = "ESFERA"
        col_situacao = "SITUAÇÃO GERAL" if "SITUAÇÃO GERAL" in df.columns else "SITUACAO GERAL"
        
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )
        esfera = st.sidebar.multiselect(
            "Esfera", 
            df[col_esfera].unique(), 
            default=df[col_esfera].unique()
        )

        df_filtrado = df[
            (df[col_municipios].isin(municipios)) & 
            (df[col_esfera].isin(esfera))
        ]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pie_data = df_filtrado[col_situacao].value_counts().reset_index()
            pie_data.columns = ['Situação Geral', 'Total']
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="Situação Geral", type="nominal"),
                tooltip=['Situação Geral', 'Total']
            ).properties(
                title="Distribuição da Situação Geral",
                height=300
            )
            st.altair_chart(pie_chart, use_container_width=True)
        with col2:
            mun_count = df_filtrado[col_municipios].value_counts().reset_index()
            mun_count.columns = ['Município', 'Total']
            if not mun_count.empty:
                bar_chart = alt.Chart(mun_count).mark_bar().encode(
                    x=alt.X('Município:N', sort='-y'),
                    y=alt.Y('Total:Q'),
                    color=alt.value('#1f77b4'),
                    tooltip=['Município', 'Total']
                ).properties(
                    title="Unidades por Município",
                    height=300
                )
                st.altair_chart(bar_chart, use_container_width=True)

        create_download_button(df_filtrado, "unidades_interligadas.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba UNIDADES INTERLIGADAS: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 2: STATUS RECEB FORMULARIO ==================
elif selected_tab == "STATUS RECEB FORMULARIO":
    st.header("📄 Status Recebimento Formulário")
    
    try:
        col_municipios = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"
        col_status = "STATUS GERAL RECEBIMENTO"
        
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )
        status = st.sidebar.multiselect(
            "Status Geral Recebimento", 
            df[col_status].unique(), 
            default=df[col_status].unique()
        )

        df_filtrado = df[
            (df[col_municipios].isin(municipios)) & 
            (df[col_status].isin(status))
        ]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pie_data = df_filtrado[col_status].value_counts().reset_index()
            pie_data.columns = ['Status', 'Total']
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="Status", type="nominal"),
                tooltip=['Status', 'Total']
            ).properties(
                title="Distribuição do Status de Recebimento",
                height=300
            )
            st.altair_chart(pie_chart, use_container_width=True)
        with col2:
            mun_count = df_filtrado[col_municipios].value_counts().reset_index()
            mun_count.columns = ['Município', 'Total']
            if not mun_count.empty:
                bar_chart = alt.Chart(mun_count).mark_bar().encode(
                    x=alt.X('Município:N', sort='-y'),
                    y=alt.Y('Total:Q'),
                    color=alt.value('#1f77b4'),
                    tooltip=['Município', 'Total']
                ).properties(
                    title="Registros por Município",
                    height=300
                )
                st.altair_chart(bar_chart, use_container_width=True)

        create_download_button(df_filtrado, "status_recebimento.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba STATUS RECEB FORMULARIO: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 3: MUNICIPIOS PARA INSTALAR ==================
elif selected_tab == "MUNICIPIOS PARA INSTALAR":
    st.header("🔹 Municípios para Instalar")
    
    try:
        col_municipios = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"
        
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )
        
        df_filtrado = df[df[col_municipios].isin(municipios)]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        create_download_button(df_filtrado, "municipios_para_instalar.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba MUNICIPIOS PARA INSTALAR: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 5: PROVIMENTO 09 ==================
elif selected_tab == "PROVIMENTO 09":
    st.header("📜 Provimento 09 - TCT Assinados")
    
    try:
        col_municipios = "MUNICÍPIOS QUE ASSINARAM O TCT" if "MUNICÍPIOS QUE ASSINARAM O TCT" in df.columns else "MUNICÍPIOS"
        
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios que Assinaram", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )
        
        df_filtrado = df[df[col_municipios].isin(municipios)]

        show_data_summary(df_filtrado)
        st.write(f"### 📌 {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        create_download_button(df_filtrado, "provimento_09.csv")
        
    except Exception as e:
        st.error(f"Erro ao processar a aba PROVIMENTO 09: {str(e)}")
        st.error(traceback.format_exc())

# ================== MENSAGEM FINAL ==================
st.success("✅ Dashboard atualizado com os dados das abas do Google Sheets!")
