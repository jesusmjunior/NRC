import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime
import traceback

# ================== SISTEMA DE LOGIN MUITO SIMPLES ==================
# Lista de usuários e senhas (simples e direto)
usuarios_validos = {
    "COGEX": "X",
    # Adicione novos usuários:
    # "usuario1": "senha1",
    # "usuario2": "senha2",
    # "usuario3": "senha3",
    # "usuario4": "senha4",
    # "usuario5": "senha5",
    # "usuario6": "senha6",
    # "usuario7": "senha7",
    # "usuario8": "senha8",
}

# ================== FUNÇÃO DE LOGIN ==================
def login():
    st.title("🔐 BEM VINDO! NRC COGEX -MA!")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username in usuarios_validos and password == usuarios_validos[username]:
            st.session_state["autenticado"] = True
            st.success("\u2705 Login realizado com sucesso!")
        else:
            st.error("\u274C Usuário ou senha incorretos.")

# ================== CHECAGEM DE LOGIN ==================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    login()
    st.stop()

# ================== CONFIGURAÇÃO DO DASHBOARD ==================
st.set_page_config(
    page_title="PAINEL GERENCIAL - Tabela Unidades Interligadas - NRC CGJ - ATUALIZADA", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CABEÇALHO ==================
col1, col2 = st.columns([6, 1])

with col1:
    st.title("\U0001F4CA PAINEL GERENCIAL - Tabela Unidades Interligadas - NRC COGEX -MA - ATUALIZADA CORREGEDORIA DO FORO EXTRAJUDICIAL NRC 2025")
    st.subheader("\U0001F4C4 DADOS DO FORMULÁRIO OBRIGATÓRIO DAS UNIDADES INTERLIGADAS - PROV 07")
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

with col2:
    st.image("https://raw.githubusercontent.com/jesusmjunior/dashboard-registro-civil-prov07/main/CGX.png", width=120)

# ================== AVISO ==================
st.warning("\U0001F6A8 **ATENÇÃO! UNIDADE INTERLIGADA!**\n\nAcesse e preencha/atualize seus dados do Provimento 07/2021.", icon="⚠️")
st.markdown("[\U0001F4DD **Clique aqui para acessar o Formulário Obrigatório**](https://forms.gle/vETZAjAStN3F9YHx9)")

# ================== RESUMO ==================
with st.expander("ℹ️ Sobre o Provimento 07/2021 - Clique para detalhes"):
    st.markdown("""
**Resumo do Provimento CGJ:**

A instalação de unidades interligadas em hospitais é obrigatória, independentemente do número de partos. Os registros de nascimento e óbito são feitos nessas unidades com livro próprio. Os serviços devem enviar relatório mensal até o dia 10 via [Formulário Online](https://forms.gle/vETZAjAStN3F9YHx9), sob pena de sanções administrativas.

**Desembargador José Jorge Figueiredo dos Anjos**  
Corregedor-Geral da Justiça (Biênio 2024-2026)
""")

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

# ================== ID das Planilhas ==================
subregistro_sheet_id = "1UD1B9_5_zwd_QD0drE1fo3AokpE6EDnYTCwywrGkD-Y"
subregistro_base_url = f"https://docs.google.com/spreadsheets/d/{subregistro_sheet_id}/gviz/tq?tqx=out:csv&sheet=subregistro"

sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

# ================== URLs ==================
sheet_urls = {
    "UNIDADES INTERLIGADAS": f"{base_url}UNIDADES%20INTERLIGADAS",
    "STATUS RECEBIMENTO FORMULÁRIO": f"{base_url}STATUS%20RECEB%20FORMULARIO",
    "MUNICÍPIOS PARA INSTALAR": f"{base_url}MUNICIPIOS%20PARA%20INSTALAR",
    "PROVIMENTO 09": f"{base_url}PROVIMENTO%2009",
    "MUNICÍPIOS PARA REATIVAÇÃO": f"{base_url}MUNIC%C3%8DPIOS%20PARA%20REATIVA",
    "ACOMPANHAMENTO ARTICULAÇÃO": f"{base_url}TAB%20ACOMPANHAMENTO%20ARTICULA%C3%87%C3%83O",
    "ÍNDICES DE SUB-REGISTRO": f"{base_url}%C3%8DNDICES%20DE%20SUB-REGISTRO",
    "SUB-REGISTRO": subregistro_base_url
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

# ================== EXIBIÇÃO DOS DADOS ==================
# Aqui você coloca suas condições para cada aba, como já está implementado no seu código original.
