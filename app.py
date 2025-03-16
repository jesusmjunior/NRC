import streamlit as st
import pandas as pd
import altair as alt

# URL da planilha do Google Sheets (compartilhada publicamente)
sheet_url = "https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/edit?usp=sharing&ouid=113285550239608793612&rtpof=true&sd=true"

# Converter a URL padrão para URL de exportação CSV
# Formato: /spreadsheets/d/[ID]/export?format=csv
sheet_id = sheet_url.split("/")[5]
csv_export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Carregar dados do Google Sheets
@st.cache_data
def carregar_dados(nome_planilha):
    try:
        # Em uma implementação real, precisaríamos acessar diferentes abas
        # Esta é uma abordagem simplificada usando um único URL
        df = pd.read_csv(csv_export_url)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Configuração do Dashboard
st.set_page_config(page_title="Dashboard Sistema de Saúde", layout="wide")
st.title("📊 Dashboard - Sistema de Saúde")

# Carregar os dados
df = carregar_dados("UNIDADES INTERLIGADAS")

# Verificar se os dados foram carregados com sucesso
if df.empty:
    st.warning("Nenhum dado disponível. Verifique a URL da planilha do Google Sheets e certifique-se de que esteja acessível publicamente.")
    st.stop()

# ================== BARRA LATERAL - NAVEGAÇÃO ==================
st.sidebar.title("📂 Navegação")
abas = [
    "Unidades Interligadas", 
    "Status Recebimento Formulário", 
    "Municípios para Instalar 1", 
    "Municípios para Instalar 2", 
    "Municípios Inviáveis", 
    "Provimento 09 - TCT"
]
aba_selecionada = st.sidebar.radio("Selecione uma aba:", abas)

# ================== FUNÇÕES DE VISUALIZAÇÃO ==================
def criar_grafico_barras(dados, coluna_x, coluna_y, coluna_cor=None, titulo=""):
    """
    Criar gráfico de barras com Altair
    """
    if coluna_cor:
        grafico = alt.Chart(dados).mark_bar().encode(
            x=alt.X(f'{coluna_x}:N', sort='-y'),
            y=f'{coluna_y}:Q',
            color=f'{coluna_cor}:N',
            tooltip=[coluna_x, coluna_y, coluna_cor]
        ).properties(
            title=titulo,
            height=400
        ).interactive()
    else:
        grafico = alt.Chart(dados).mark_bar().encode(
            x=alt.X(f'{coluna_x}:N', sort='-y'),
            y=f'{coluna_y}:Q',
            tooltip=[coluna_x, coluna_y]
        ).properties(
            title=titulo,
            height=400
        ).interactive()
    
    return grafico

def criar_grafico_pizza(dados, coluna, titulo=""):
    """
    Criar gráfico de pizza com Altair
    """
    # Converter para o formato necessário para o gráfico de pizza
    df_contagem = dados[coluna].value_counts().reset_index()
    df_contagem.columns = ['categoria', 'contagem']
    
    # Criar um gráfico de pizza usando Altair
    pizza = alt.Chart(df_contagem).mark_arc().encode(
        theta=alt.Theta(field="contagem", type="quantitative"),
        color=alt.Color(field="categoria", type="nominal"),
        tooltip=['categoria', 'contagem']
    ).properties(
        title=titulo,
        height=300,
        width=300
    )
    
    return pizza

def exibir_metricas(dict_metricas):
    """
    Exibir métricas em colunas
    """
    colunas = st.columns(len(dict_metricas))
    for i, (rotulo, valor) in enumerate(dict_metricas.items()):
        with colunas[i]:
            st.metric(rotulo, valor)

# ================== ABA 1 - UNIDADES INTERLIGADAS ==================
def mostrar_unidades_interligadas():
    st.header("🏥 Unidades Interligadas")
    
    # Aqui normalmente carregaríamos uma aba específica,
    # mas estamos usando os dados já carregados no exemplo
    df_aba = df
    
    # Verificar colunas esperadas
    colunas_esperadas = [
        'MUNICÍPIOS', 'HOSPITAL', 'DATA DA INSTALAÇÃO', 'ESFERA', 
        'SERVENTIA', 'JUSTIÇA ABERTA', 'HABILITAÇÃO CRC', 
        'SITUAÇÃO ATUAL', 'SITUAÇÃO GERAL', 'ÍNDICES IBGE', 'OBSERVAÇÕES'
    ]
    
    # Verificar se as colunas existem e filtrar de acordo
    colunas_ausentes = [col for col in colunas_esperadas if col not in df_aba.columns]
    if colunas_ausentes:
        st.warning(f"Colunas ausentes nos dados: {', '.join(colunas_ausentes)}")
        st.write("Colunas disponíveis:", ", ".join(df_aba.columns))
        st.dataframe(df_aba)
        return
    
    # Filtros
    municipios = st.sidebar.multiselect(
        "Selecione os Municípios:", 
        df_aba['MUNICÍPIOS'].unique(), 
        default=df_aba['MUNICÍPIOS'].unique()
    )
    
    esferas = st.sidebar.multiselect(
        "Selecione as Esferas:", 
        df_aba['ESFERA'].unique(), 
        default=df_aba['ESFERA'].unique()
    )
    
    df_filtrado = df_aba[
        (df_aba['MUNICÍPIOS'].isin(municipios)) & 
        (df_aba['ESFERA'].isin(esferas))
    ]
    
    # KPIs
    metricas = {
        "Total de Hospitais": df_filtrado.shape[0],
        "Com Justiça Aberta": df_filtrado['JUSTIÇA ABERTA'].value_counts().get("Sim", 0),
        "Habilitação CRC OK": df_filtrado['HABILITAÇÃO CRC'].value_counts().get("Habilitado", 0)
    }
    exibir_metricas(metricas)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        grafico_barras = criar_grafico_barras(
            df_filtrado, 
            "MUNICÍPIOS", 
            "ÍNDICES IBGE", 
            "SITUAÇÃO GERAL", 
            "Distribuição por Municípios"
        )
        st.altair_chart(grafico_barras, use_container_width=True)
    
    with col2:
        grafico_pizza = criar_grafico_pizza(
            df_filtrado, 
            "SITUAÇÃO GERAL", 
            "Situação Geral das Unidades"
        )
        st.altair_chart(grafico_pizza, use_container_width=True)
    
    # Tabela e Download
    st.subheader("Tabela de Dados")
    st.dataframe(df_filtrado)
    st.download_button(
        "📥 Baixar Dados", 
        df_filtrado.to_csv(index=False), 
        file_name="unidades_interligadas.csv"
    )

# ================== ABA 2 - STATUS RECEBIMENTO FORMULÁRIO ==================
def mostrar_status_recebimento():
    st.header("📄 Status de Recebimento de Formulário")
    
    # Aqui usaríamos df_aba = carregar_dados("STATUS RECEB FORMULARIO")
    # Mas estamos usando os mesmos dados para exemplo
    df_aba = df
    
    # Verificar colunas esperadas
    colunas_esperadas = [
        'MUNICÍPIOS', 'HOSPITAL', 'SERVENTIA', 
        'STATUS GERAL RECEBIMENTO', 'FALTANTES E ENVIADOS'
    ]
    
    # Verificar se as colunas existem e filtrar de acordo
    colunas_ausentes = [col for col in colunas_esperadas if col not in df_aba.columns]
    if colunas_ausentes:
        st.warning(f"Colunas ausentes nos dados: {', '.join(colunas_ausentes)}")
        st.write("Colunas disponíveis:", ", ".join(df_aba.columns))
        st.dataframe(df_aba)
        return
    
    # Filtros
    municipios = st.sidebar.multiselect(
        "Selecione os Municípios:", 
        df_aba['MUNICÍPIOS'].unique(), 
        default=df_aba['MUNICÍPIOS'].unique()
    )
    
    df_filtrado = df_aba[df_aba['MUNICÍPIOS'].isin(municipios)]
    
    # KPIs
    total = len(df_filtrado)
    recebidos = df_filtrado['STATUS GERAL RECEBIMENTO'].value_counts().get('Recebido', 0)
    faltantes = total - recebidos
    
    metricas = {
        "Recebidos": recebidos,
        "Faltantes": faltantes,
        "Total": total
    }
    exibir_metricas(metricas)
    
    # Gráfico
    grafico_pizza = criar_grafico_pizza(
        df_filtrado, 
        "STATUS GERAL RECEBIMENTO", 
        "Status Geral de Recebimento"
    )
    st.altair_chart(grafico_pizza, use_container_width=True)
    
    # Tabela e Download
    st.subheader("Tabela de Dados")
    st.dataframe(df_filtrado)
    st.download_button(
        "📥 Baixar Dados", 
        df_filtrado.to_csv(index=False), 
        file_name="status_recebimento.csv"
    )

# ================== ABA 3 - MUNICÍPIOS PARA INSTALAR 1 ==================
def mostrar_municipios_instalar_1():
    st.header("🏗️ Municípios para Instalar - Prov. 07")
    
    # Aqui usaríamos df_aba = carregar_dados("MUNICÍPIOS PARA INSTALAR")
    # Mas estamos usando os mesmos dados para exemplo
    df_aba = df
    
    # Verificar colunas esperadas
    colunas_esperadas = [
        'MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07):', 
        'FASE', 
        'OBSERVAÇÃO'
    ]
    
    # Verificar se as colunas existem e filtrar de acordo
    colunas_ausentes = [col for col in colunas_esperadas if col not in df_aba.columns]
    if colunas_ausentes:
        st.warning(f"Colunas ausentes nos dados: {', '.join(colunas_ausentes)}")
        st.write("Colunas disponíveis:", ", ".join(df_aba.columns))
        st.dataframe(df_aba)
        return
    
    # Filtros
    fases = st.sidebar.multiselect(
        "Filtrar por Fase:", 
        df_aba['FASE'].unique(), 
        default=df_aba['FASE'].unique()
    )
    
    df_filtrado = df_aba[df_aba['FASE'].isin(fases)]
    
    # Contagem por fase
    contagem_fases = df_filtrado['FASE'].value_counts().reset_index()
    contagem_fases.columns = ['FASE', 'contagem']
    
    # Gráfico
    grafico = alt.Chart(contagem_fases).mark_bar().encode(
        x='FASE:N',
        y='contagem:Q',
        color='FASE:N',
        tooltip=['FASE', 'contagem']
    ).properties(
        title="Distribuição por Fase",
        height=400
    ).interactive()
    
    st.altair_chart(grafico, use_container_width=True)
    
    # Tabela e Download
    st.subheader("Tabela de Dados")
    st.dataframe(df_filtrado)
    st.download_button(
        "📥 Baixar Dados", 
        df_filtrado.to_csv(index=False), 
        file_name="municipios_instalar.csv"
    )

# ================== ABA 4 - MUNICÍPIOS PARA INSTALAR 2 ==================
def mostrar_municipios_instalar_2():
    st.header("🏗️ Municípios para Instalar - Prov. 07 (Parte 2)")
    
    # Aqui usaríamos df_aba = carregar_dados("MUNICÍPIOS PARA INSTALAR 2")
    # Mas estamos usando os mesmos dados para exemplo
    df_aba = df
    
    # Verificar colunas esperadas
    colunas_esperadas = [
        'MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07):', 
        'FASE', 
        'OBSERVAÇÃO'
    ]
    
    # Verificar se as colunas existem e filtrar de acordo
    colunas_ausentes = [col for col in colunas_esperadas if col not in df_aba.columns]
    if colunas_ausentes:
        st.warning(f"Colunas ausentes nos dados: {', '.join(colunas_ausentes)}")
        st.write("Colunas disponíveis:", ", ".join(df_aba.columns))
        st.dataframe(df_aba)
        return
    
    # Filtros
    fases = st.sidebar.multiselect(
        "Filtrar por Fase:", 
        df_aba['FASE'].unique(), 
        default=df_aba['FASE'].unique()
    )
    
    df_filtrado = df_aba[df_aba['FASE'].isin(fases)]
    
    # Contagem por fase
    contagem_fases = df_filtrado['FASE'].value_counts().reset_index()
    contagem_fases.columns = ['FASE', 'contagem']
    
    # Gráfico
    grafico = alt.Chart(contagem_fases).mark_bar().encode(
        x='FASE:N',
        y='contagem:Q',
        color='FASE:N
