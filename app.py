import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Conexão Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("LINK_DO_SHEET")
worksheet = sheet.worksheet('UNIDADES INTERLIGADAS')
data = pd.DataFrame(worksheet.get_all_records())

st.title("📊 Unidades Interligadas")

# Filtros
municipios = st.sidebar.multiselect("Filtrar Municípios", data['MUNICÍPIOS'].unique())
if municipios:
    data = data[data['MUNICÍPIOS'].isin(municipios)]

# KPIs
st.metric("Total Hospitais", data.shape[0])
st.metric("Com Justiça Aberta", data['JUSTIÇA ABERTA'].value_counts().get("Sim", 0))
st.metric("Habilitação CRC OK", data['HABILITAÇÃO CRC'].value_counts().get("Habilitado", 0))

# Gráficos
fig = px.bar(data, x="MUNICÍPIOS", y="ÍNDICES IBGE", color="SITUAÇÃO GERAL", title="Distribuição por Municípios")
st.plotly_chart(fig)

pie_fig = px.pie(data, names="SITUAÇÃO GERAL", title="Situação Geral das Unidades")
st.plotly_chart(pie_fig)

# Download
st.sidebar.download_button("📥 Baixar CSV", data.to_csv(index=False), file_name="unidades_interligadas.csv")
