import streamlit as st
import pandas as pd
import altair as alt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Unidades Interligadas", layout="wide")
st.title("📌 Dashboard Unidades Interligadas")

# Conexão Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/edit")

# -------------------- ABA 1: UNIDADES INTERLIGADAS --------------------
st.sidebar.title("🔎 Filtros - Unidades Interligadas")
worksheet_ui = sheet.worksheet('UNIDADES INTERLIGADAS')
df_ui = pd.DataFrame(worksheet_ui.get_all_records())

municipios = st.sidebar.multiselect("Selecione os Municípios", df_ui['MUNICÍPIOS'].unique(), default=df_ui['MUNICÍPIOS'].unique())

df_filtered = df_ui[df_ui['MUNICÍPIOS'].isin(municipios)]

st.subheader("🏥 Unidades Interligadas")
col1, col2, col3 = st.columns(3)
col1.metric("Total Hospitais", df_filtered.shape[0])
col2.metric("Com Justiça Aberta", df_filtered['JUSTIÇA ABERTA'].value_counts().get("Sim", 0))
col3.metric("Habilitação CRC OK", df_filtered['HABILITAÇÃO CRC'].value_counts().get("Habilitado", 0))

bar_chart = alt.Chart(df_filtered).mark_bar().encode(
    x=alt.X("MUNICÍPIOS", sort='-y'),
    y="ÍNDICES IBGE",
    color="SITUAÇÃO GERAL"
).properties(title="Distribuição por Municípios", width=700)

st.altair_chart(bar_chart, use_container_width=True)

pie_data = df_filtered['SITUAÇÃO GERAL'].value_counts().reset_index()
pie_data.columns = ['Situação Geral', 'Total']

pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta=alt.Theta(field="Total", type="quantitative"),
    color=alt.Color(field="Situação Geral", type="nominal")
).properties(title="Situação Geral")

st.altair_chart(pie_chart, use_container_width=True)

st.sidebar.download_button("📥 Baixar Dados", df_filtered.to_csv(index=False), file_name="unidades_interligadas.csv")

# -------------------- ABA 2: STATUS RECEB FORMULÁRIO --------------------
st.subheader("📄 Status Recebimento Formulário")
worksheet_status = sheet.worksheet('STATUS RECEB FORMULARIO')
df_status = pd.DataFrame(worksheet_status.get_all_records())

status = st.multiselect("Status Geral", df_status['STATUS GERAL RECEBIMENTO'].unique(), default=df_status['STATUS GERAL RECEBIMENTO'].unique())
df_status_filtered = df_status[df_status['STATUS GERAL RECEBIMENTO'].isin(status)]

st.dataframe(df_status_filtered)
st.metric("Formulários Enviados", df_status_filtered['STATUS GERAL RECEBIMENTO'].value_counts().get("Enviado", 0))

st.sidebar.download_button("📥 Baixar Status Formulário", df_status_filtered.to_csv(index=False), file_name="status_formulario.csv")

# -------------------- ABA 3 & 4: MUNICÍPIOS PARA INSTALAR --------------------
st.subheader("🚧 Municípios em Fase de Instalação")
worksheet_inst1 = sheet.worksheet('MUNICÍPIOS PARA INSTALAR')
df_inst1 = pd.DataFrame(worksheet_inst1.get_all_records())

worksheet_inst2 = sheet.worksheet('MUNICÍPIOS PARA INSTALAR2')
df_inst2 = pd.DataFrame(worksheet_inst2.get_all_records())

df_instalacao = pd.concat([df_inst1, df_inst2], ignore_index=True)
fase = st.multiselect("Fase de Instalação", df_instalacao['FASE'].unique(), default=df_instalacao['FASE'].unique())
df_instalacao_filtered = df_instalacao[df_instalacao['FASE'].isin(fase)]

st.dataframe(df_instalacao_filtered)

bar_fase = alt.Chart(df_instalacao_filtered).mark_bar().encode(
    x="MUNICÍPIOS EM FASE DE INSTALAÇÃO (PROV. 07):",
    color="FASE"
).properties(title="Distribuição por Fase")

st.altair_chart(bar_fase, use_container_width=True)

st.sidebar.download_button("📥 Baixar Municípios Instalação", df_instalacao_filtered.to_csv(index=False), file_name="municipios_instalacao.csv")

# -------------------- ABA 5: MUN. INVIÁVEIS DE INSTALAÇÃO --------------------
st.subheader("❌ Municípios Inváiveis")
worksheet_inv = sheet.worksheet('MUN. INVIÁVEIS DE INSTALAÇÃO')
df_inv = pd.DataFrame(worksheet_inv.get_all_records())

st.dataframe(df_inv)

pie_inv = df_inv['SITUAÇÃO'].value_counts().reset_index()
pie_inv.columns = ['Situação', 'Total']

pie_chart_inv = alt.Chart(pie_inv).mark_arc().encode(
    theta=alt.Theta(field="Total", type="quantitative"),
    color=alt.Color(field="Situação", type="nominal")
).properties(title="Situação dos Municípios Inváiveis")

st.altair_chart(pie_chart_inv, use_container_width=True)

st.sidebar.download_button("📥 Baixar Municípios Inváiveis", df_inv.to_csv(index=False), file_name="municipios_inviaveis.csv")

# -------------------- ABA 6: PROVIMENTO 09 --------------------
st.subheader("📜 Provimento 09 – TCT")
worksheet_tct = sheet.worksheet('PROVIMENTO 09')
df_tct = pd.DataFrame(worksheet_tct.get_all_records())

col1, col2 = st.columns(2)
col1.write("### MUNICÍPIOS QUE ASSINARAM O TCT")
col1.dataframe(df_tct['MUNICÍPIOS QUE ASSINARAM O TCT'].dropna())

col2.write("### MUNICÍPIOS VÃO ASSINAR O TCT")
col2.dataframe(df_tct['MUNICÍPIOS VÃO ASSINAR O TCT'].dropna())

st.sidebar.download_button("📥 Baixar Provimento 09", df_tct.to_csv(index=False), file_name="provimento09.csv")

st.success("✅ Dashboard carregado com sucesso!")
