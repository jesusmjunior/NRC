import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime
import traceback

# ================================
# CONFIGURAÇÃO INICIAL PRIMEIRA LINHA
# ================================
st.set_page_config(page_title="PAINEL GERENCIAL - NRC COGEX", layout="wide")

# ================================
# LOGIN SIMPLES - ESTILO SIMPLES DIRETO
# ================================
def login():
    st.title("🔐 Área Protegida - NRC COGEX -MA!")
    user = st.text_input("Usuário (Email)")
    password = st.text_input("Senha", type="password")

    usuarios_validos = {
        "COGEX": "X",
        "NRC": "X",
        # Adicione novos usuários aqui, exemplo:
        # "usuario3@gmail.com": "senha3",
        # "usuario4@gmail.com": "senha4",
    }

    if user in usuarios_validos and password == usuarios_validos[user]:
        st.success("Login efetuado com sucesso ✅")
        return True
    else:
        if user and password:
            st.error("Usuário ou senha incorretos ❌")
        st.stop()

# ================================
# EXECUTA LOGIN
# ================================
login()

# ================================
# CABEÇALHO ================================
col1, col2 = st.columns([6, 1])

with col1:
    st.title("\U0001F4CA PAINEL GERENCIAL - Tabela Unidades Interligadas - NRC COGEX -MA - ATUALIZADA CORREGEDORIA DO FORO EXTRAJUDICIAL NRC 2025")
    st.subheader("\U0001F4C4 DADOS DO FORMULÁRIO OBRIGATÓRIO DAS UNIDADES INTERLIGADAS - PROV 07")
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

with col2:
    st.image("https://raw.githubusercontent.com/jesusmjunior/dashboard-registro-civil-prov07/main/CGX.png", width=120)

# ================================
# AVISO ================================
st.warning("\U0001F6A8 **ATENÇÃO! UNIDADE INTERLIGADA!**\n\nAcesse e preencha/atualize seus dados do Provimento 07/2021.", icon="⚠️")
st.markdown("[\U0001F4DD **Clique aqui para acessar o Formulário Obrigatório**](https://forms.gle/vETZAjAStN3F9YHx9)")

# ================================
# RESUMO ================================
with st.expander("ℹ️ Sobre o Provimento 07/2021 - Clique para detalhes"):
    st.markdown("""
**Resumo do Provimento CGJ:**

A instalação de unidades interligadas em hospitais é obrigatória, independentemente do número de partos. Os registros de nascimento e óbito são feitos nessas unidades com livro próprio. Os serviços devem enviar relatório mensal até o dia 10 via [Formulário Online](https://forms.gle/vETZAjAStN3F9YHx9), sob pena de sanções administrativas.

**Desembargador José Jorge Figueiredo dos Anjos**  
Corregedor-Geral da Justiça (Biênio 2024-2026)
""")

# ================================
# FUNÇÃO PARA CARREGAR DADOS ================================
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

# ================================
# ID das Planilhas ================================
subregistro_sheet_id = "1UD1B9_5_zwd_QD0drE1fo3AokpE6EDnYTCwywrGkD-Y"
subregistro_base_url = f"https://docs.google.com/spreadsheets/d/{subregistro_sheet_id}/gviz/tq?tqx=out:csv&sheet=subregistro"

sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

# ================================
# URLs ================================
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

# ================================
# BARRA LATERAL - SELEÇÃO DE ABA ================================
st.sidebar.header("\U0001F4C2 Seleção de Aba")
tabs = list(sheet_urls.keys())
aba_selecionada = st.sidebar.radio("Selecione uma aba:", tabs)

# ================================
# LOADING SPINNER ================================
with st.spinner(f"Carregando dados da aba {aba_selecionada}..."):
    df = carregar_dados(sheet_urls[aba_selecionada])

if df.empty:
    st.error(f"Não foi possível carregar os dados da aba {aba_selecionada}.")
    st.stop()

# ================================
# FUNÇÕES AUXILIARES ================================
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
# ID da planilha SUB-REGISTRO separada
subregistro_sheet_id = "1UD1B9_5_zwd_QD0drE1fo3AokpE6EDnYTCwywrGkD-Y"
subregistro_base_url = f"https://docs.google.com/spreadsheets/d/{subregistro_sheet_id}/gviz/tq?tqx=out:csv&sheet=subregistro"

# ================== ID das Planilhas ==================
subregistro_sheet_id = "1UD1B9_5_zwd_QD0drE1fo3AokpE6EDnYTCwywrGkD-Y"
subregistro_base_url = f"https://docs.google.com/spreadsheets/d/{subregistro_sheet_id}/gviz/tq?tqx=out:csv&sheet=subregistro"

sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

# ================== URLs das Planilhas ==================
sheet_urls = {
    "UNIDADES INTERLIGADAS": f"{base_url}UNIDADES%20INTERLIGADAS",
    "STATUS RECEBIMENTO FORMULÁRIO": f"{base_url}STATUS%20RECEB%20FORMULARIO",
    "MUNICÍPIOS PARA INSTALAR": f"{base_url}MUNICIPIOS%20PARA%20INSTALAR",
    "PROVIMENTO 09": f"{base_url}PROVIMENTO%2009",
    "MUNICÍPIOS PARA REATIVAÇÃO": f"{base_url}MUNIC%C3%8DPIOS%20PARA%20REATIVA",
    "ACOMPANHAMENTO ARTICULAÇÃO": f"{base_url}TAB%20ACOMPANHAMENTO%20ARTICULA%C3%87%C3%83O",
    "ÍNDICES DE SUB-REGISTRO": f"{base_url}%C3%8DNDICES%20DE%20SUB-REGISTRO",
    "SUB-REGISTRO": subregistro_base_url  # ✅ Link correto
}  # <<< AQUI FECHAMOS O DICIONÁRIO!

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
# ===================== ABA: SUB-REGISTRO =====================
elif aba_selecionada == "SUB-REGISTRO":
    st.header("⚠️ DATA SET ORGANIZADO 17/04/2024 - Índices de Sub-registro IBGE por Município")

    # Limpar colunas
    df.columns = df.columns.str.strip()

    # Ordenar pelos piores índices de sub-registro
    df_sorted = df[['Nome Município', 'Sub-registro IBGE(1)']].sort_values(by='Sub-registro IBGE(1)', ascending=False)

    st.metric("Total de Municípios", df_sorted.shape[0])
    st.dataframe(df_sorted, use_container_width=True)

    # Gráfico TOP 10 Piores
    chart = alt.Chart(df_sorted.head(10)).mark_bar().encode(
        x=alt.X('Sub-registro IBGE(1):Q', title='Índice de Sub-registro (%)'),
        y=alt.Y('Nome Município:N', sort='-x'),
        color=alt.value('#d62728'),
        tooltip=['Nome Município', 'Sub-registro IBGE(1)']
    ).properties(title='Top 10 Municípios com Piores Índices de Sub-registro')
    st.altair_chart(chart, use_container_width=True)

    # Download CSV
    csv = df_sorted.to_csv(index=False, encoding='utf-8-sig')
    st.sidebar.download_button("📥 Baixar Sub-registro CSV", data=csv.encode('utf-8-sig'), file_name="subregistro.csv", mime='text/csv')
# ================== ROBOZINHO VERTICAL COM LINK 100% CLICÁVEL ==================
st.markdown("""
    <style>
        .robo-lateral {
            position: fixed;
            right: 0;
            top: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            animation: descer 8s linear infinite alternate;
            z-index: 1000;
            pointer-events: auto;
        }
        @keyframes descer {
            0% { top: 5%; }
            100% { top: 80%; }
        }
        .robo-lateral img {
            width: 60px;
            transition: transform 0.3s ease;
        }
        .robo-lateral img:hover {
            transform: scale(1.2);
        }
        .faixa-texto {
            background-color: #800000;
            color: white;
            padding: 4px 8px;
            border-radius: 8px;
            margin-top: 8px;
            font-weight: bold;
            font-size: 12px;
        }
        .robo-link {
            text-decoration: none;
        }
    </style>
    <a class='robo-link' href='https://www.tjma.jus.br/site/extrajudicial' target='_blank'>
        <div class='robo-lateral'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png'/>
            <div class='faixa-texto'>I.A. COGEX 2025</div>
        </div>
    </a>
""", unsafe_allow_html=True)
# ================== RODAPÉ ==================
st.markdown("""
    <hr>
    <p style='text-align: center; color: #800000;'><strong>Corregedoria Geral do Foro Extrajudicial</strong><br>
    Rua Cumã, nº 300, 1º andar, Edifício Manhattan Center III, Jardim Renascença 2<br>
    São Luís - Maranhão CEP 65.075-700</p>
""", unsafe_allow_html=True)
st.success("\u2705 Painel COGEX 2025 carregado com sucesso!") LOGIN: COGEX SENHA: X
