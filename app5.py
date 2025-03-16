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

st.title("\U0001F4CA Dashboard de Unidades Interligadas")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ================== FUNÇÃO PARA CARREGAR DADOS ==================
@st.cache_data(ttl=3600)
def carregar_dados(sheet_url):
    try:
        df = pd.read_csv(sheet_url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.error(traceback.format_exc())
        return pd.DataFrame()

# ================== URLs das Planilhas ==================
sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

sheet_urls = {
    "UNIDADES INTERLIGADAS": f"{base_url}UNIDADES%20INTERLIGADAS",
    "STATUS RECEBIMENTO FORMULÁRIO": f"{base_url}STATUS%20RECEB%20FORMULARIO",
    "MUNICÍPIOS PARA INSTALAR": f"{base_url}MUNICIPIOS%20PARA%20INSTALAR",
    "PROVIMENTO 09": f"{base_url}PROVIMENTO%2009",
    "MUNICÍPIOS PARA REATIVAÇÃO": f"{base_url}MUNIC%C3%8DPIOS%20PARA%20REATIVA",
    "ACOMPANHAMENTO ARTICULAÇÃO": f"{base_url}TAB%20ACOMPANHAMENTO%20ARTICULA%C3%87%C3%83O",
    "ÍNDICES DE SUB-REGISTRO": f"{base_url}%C3%8DNDICES%20DE%20SUB-REGISTRO"
}

# ================== BARRA LATERAL - SELEÇÃO DE ABA ==================
st.sidebar.header("\U0001F4C2 Seleção de Aba")
tabs = list(sheet_urls.keys())
aba_selecionada = st.sidebar.radio("Selecione uma aba:", tabs)

# ================== LOADING SPINNER ==================
with st.spinner(f"Carregando dados da aba {aba_selecionada}..."):
    df = carregar_dados(sheet_urls[aba_selecionada])

if df.empty:
    st.error(f"Não foi possível carregar os dados da aba {aba_selecionada}.")
    st.stop()

# ================== FUNÇÕES AUXILIARES ==================
def botao_download(dataframe, filename):
    csv = dataframe.to_csv(index=False, encoding='utf-8-sig')
    return st.sidebar.download_button(
        label="\U0001F4E5 Baixar Dados",
        data=csv.encode('utf-8-sig'),
        file_name=filename,
        mime='text/csv'
    )

def resumo_dados(dataframe):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de registros", dataframe.shape[0])
    with col2:
        st.metric("Colunas disponíveis", dataframe.shape[1])
    with col3:
        st.metric("Última atualização", datetime.now().strftime("%d/%m/%Y"))

# ================== ABA 1: UNIDADES INTERLIGADAS ==================
if aba_selecionada == "UNIDADES INTERLIGADAS":
    st.header("\U0001F3E5 Unidades Interligadas")
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

        df_filtrado = df[(df[col_municipios].isin(municipios)) & (df[col_esfera].isin(esfera))]

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pie_data = df_filtrado[col_situacao].value_counts().reset_index()
            pie_data.columns = ['Situação Geral', 'Total']
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="Situação Geral", type="nominal"),
                tooltip=['Situação Geral', 'Total']
            ).properties(title="Distribuição da Situação Geral", height=300)
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
                ).properties(title="Unidades por Município", height=300)
                st.altair_chart(bar_chart, use_container_width=True)

        botao_download(df_filtrado, "unidades_interligadas.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba UNIDADES INTERLIGADAS: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 2: STATUS RECEBIMENTO FORMULÁRIO ==================
elif aba_selecionada == "STATUS RECEBIMENTO FORMULÁRIO":
    st.header("\U0001F4C4 Status de Recebimento do Formulário")
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

        df_filtrado = df[(df[col_municipios].isin(municipios)) & (df[col_status].isin(status))]

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pie_data = df_filtrado[col_status].value_counts().reset_index()
            pie_data.columns = ['Status', 'Total']
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="Status", type="nominal"),
                tooltip=['Status', 'Total']
            ).properties(title="Distribuição do Status", height=300)
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
                ).properties(title="Registros por Município", height=300)
                st.altair_chart(bar_chart, use_container_width=True)

        botao_download(df_filtrado, "status_recebimento.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba STATUS RECEBIMENTO FORMULÁRIO: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 3: MUNICÍPIOS PARA INSTALAR ==================
elif aba_selecionada == "MUNICÍPIOS PARA INSTALAR":
    st.header("\U0001F539 Municípios para Instalar")
    try:
        col_municipios = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"

        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )

        df_filtrado = df[df[col_municipios].isin(municipios)]

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        botao_download(df_filtrado, "municipios_para_instalar.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba MUNICÍPIOS PARA INSTALAR: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 4: PROVIMENTO 09 ==================
elif aba_selecionada == "PROVIMENTO 09":
    st.header("\U0001F4DC Provimento 09 - Municípios que Assinaram")
    try:
        col_municipios = "MUNICÍPIOS QUE ASSINARAM O TCT" if "MUNICÍPIOS QUE ASSINARAM O TCT" in df.columns else "MUNICÍPIOS"

        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )

        df_filtrado = df[df[col_municipios].isin(municipios)]

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        botao_download(df_filtrado, "provimento_09.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba PROVIMENTO 09: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 5: MUNICÍPIOS PARA REATIVAÇÃO ==================
elif aba_selecionada == "MUNICÍPIOS PARA REATIVAÇÃO":
    st.header("\U0001F501 Municípios para Reativação")
    try:
        col_municipios = "MUNICÍPIO"
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

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        botao_download(df_filtrado, "municipios_reativacao.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba MUNICÍPIOS PARA REATIVAÇÃO: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 6: ACOMPANHAMENTO ARTICULAÇÃO ==================
elif aba_selecionada == "ACOMPANHAMENTO ARTICULAÇÃO":
    st.header("\U0001F4D1 Acompanhamento da Articulação")
    try:
        col_situacao = "SITUAÇÃO"
        col_municipios = "MUNICÍPIOS"

        situacao = st.sidebar.multiselect(
            "Selecione a Situação", 
            df[col_situacao].unique(), 
            default=df[col_situacao].unique()
        )
        municipios = st.sidebar.multiselect(
            "Selecione os Municípios", 
            df[col_municipios].unique(), 
            default=df[col_municipios].unique()
        )

        df_filtrado = df[(df[col_situacao].isin(situacao)) & (df[col_municipios].isin(municipios))]

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        botao_download(df_filtrado, "acompanhamento_articulacao.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba ACOMPANHAMENTO ARTICULAÇÃO: {str(e)}")
        st.error(traceback.format_exc())

# ================== ABA 7: ÍNDICES DE SUB-REGISTRO ==================
elif aba_selecionada == "ÍNDICES DE SUB-REGISTRO":
    st.header("\U0001F4C9 Índices de Sub-Registro")
    try:
        col_cidade = "CIDADE"
        cidades = st.sidebar.multiselect(
            "Selecione as Cidades", 
            df[col_cidade].unique(), 
            default=df[col_cidade].unique()
        )

        df_filtrado = df[df[col_cidade].isin(cidades)]

        resumo_dados(df_filtrado)
        st.write(f"### \U0001F4CC {df_filtrado.shape[0]} Registros Selecionados")
        st.dataframe(df_filtrado, use_container_width=True)

        botao_download(df_filtrado, "indices_subregistro.csv")

    except Exception as e:
        st.error(f"Erro ao processar a aba ÍNDICES DE SUB-REGISTRO: {str(e)}")
        st.error(traceback.format_exc())

# ================== MENSAGEM FINAL ==================
st.success("\u2705 Dashboard atualizado com sucesso!")
