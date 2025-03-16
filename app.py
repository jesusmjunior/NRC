import streamlit as st
import pandas as pd
import altair as alt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Dashboard Configuration
st.set_page_config(page_title="Healthcare System Dashboard", layout="wide")
st.title("📊 Healthcare System Dashboard")

# ================== GOOGLE SHEETS CONNECTION ==================
@st.cache_resource
def load_data(sheet_name):
    """
    Load data from Google Sheets with caching
    """
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq/edit")
    worksheet = sheet.worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# ================== VISUALIZATION FUNCTIONS ==================
def create_bar_chart(data, x_column, y_column, color_column=None, title=""):
    """
    Create Altair bar chart
    """
    if color_column:
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(f'{x_column}:N', sort='-y'),
            y=f'{y_column}:Q',
            color=f'{color_column}:N',
            tooltip=[x_column, y_column, color_column]
        ).properties(
            title=title,
            height=400
        ).interactive()
    else:
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(f'{x_column}:N', sort='-y'),
            y=f'{y_column}:Q',
            tooltip=[x_column, y_column]
        ).properties(
            title=title,
            height=400
        ).interactive()
    
    return chart

def create_pie_chart(data, column, title=""):
    """
    Create Altair pie chart
    """
    # Convert to format needed for pie chart
    count_df = data[column].value_counts().reset_index()
    count_df.columns = ['category', 'count']
    
    # Create a pie chart using Altair
    pie = alt.Chart(count_df).mark_arc().encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="category", type="nominal"),
        tooltip=['category', 'count']
    ).properties(
        title=title,
        height=300,
        width=300
    )
    
    return pie

def display_metrics(metrics_dict):
    """
    Display metrics in columns
    """
    cols = st.columns(len(metrics_dict))
    for i, (label, value) in enumerate(metrics_dict.items()):
        with cols[i]:
            st.metric(label, value)

# ================== SIDEBAR NAVIGATION ==================
st.sidebar.title("📂 Navigation")
tabs = [
    "Interconnected Units", 
    "Form Receipt Status", 
    "Municipalities to Install 1", 
    "Municipalities to Install 2", 
    "Non-viable Municipalities", 
    "Provision 09 - TCT"
]
selected_tab = st.sidebar.radio("Select a tab:", tabs)

# ================== TAB 1 - INTERCONNECTED UNITS ==================
def show_interconnected_units():
    st.header("🏥 Interconnected Units")
    df = load_data("UNIDADES INTERLIGADAS")

    # Filters
    municipios = st.sidebar.multiselect(
        "Select Municipalities:", 
        df['MUNICÍPIOS'].unique(), 
        default=df['MUNICÍPIOS'].unique()
    )
    df_filtered = df[df['MUNICÍPIOS'].isin(municipios)]

    # KPIs
    metrics = {
        "Total Hospitals": df_filtered.shape[0],
        "With Open Justice": df_filtered['JUSTIÇA ABERTA'].value_counts().get("Sim", 0),
        "CRC Qualification OK": df_filtered['HABILITAÇÃO CRC'].value_counts().get("Habilitado", 0)
    }
    display_metrics(metrics)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        bar_chart = create_bar_chart(
            df_filtered, 
            "MUNICÍPIOS", 
            "ÍNDICES IBGE", 
            "SITUAÇÃO GERAL", 
            "Distribution by Municipality"
        )
        st.altair_chart(bar_chart, use_container_width=True)
    
    with col2:
        pie_chart = create_pie_chart(
            df_filtered, 
            "SITUAÇÃO GERAL", 
            "General Status of Units"
        )
        st.altair_chart(pie_chart, use_container_width=True)
    
    # Table and Download
    st.subheader("Data Table")
    st.dataframe(df_filtered)
    st.download_button(
        "📥 Download Data", 
        df_filtered.to_csv(index=False), 
        file_name="interconnected_units.csv"
    )

# ================== TAB 2 - FORM RECEIPT STATUS ==================
def show_form_receipt_status():
    st.header("📄 Form Receipt Status")
    df = load_data("STATUS RECEB FORMULARIO")

    # Filters
    municipios = st.sidebar.multiselect(
        "Select Municipalities:", 
        df['MUNICÍPIOS'].unique(), 
        default=df['MUNICÍPIOS'].unique()
    )
    df_filtered = df[df['MUNICÍPIOS'].isin(municipios)]

    # KPIs
    total = len(df_filtered)
    received = df_filtered['STATUS GERAL RECEBIMENTO'].value_counts().get('Recebido', 0)
    missing = total - received
    
    metrics = {
        "Received": received,
        "Missing": missing,
        "Total": total
    }
    display_metrics(metrics)
    
    # Chart
    pie_chart = create_pie_chart(
        df_filtered, 
        "STATUS GERAL RECEBIMENTO", 
        "General Receipt Status"
    )
    st.altair_chart(pie_chart, use_container_width=True)
    
    # Table and Download
    st.subheader("Data Table")
    st.dataframe(df_filtered)
    st.download_button(
        "📥 Download Data", 
        df_filtered.to_csv(index=False), 
        file_name="form_receipt_status.csv"
    )

# ================== TAB 3 - MUNICIPALITIES TO INSTALL 1 ==================
def show_municipalities_to_install_1():
    st.header("🏗️ Municipalities to Install - Prov. 07")
    df = load_data("MUNICÍPIOS PARA INSTALAR")

    # Filters
    phase = st.sidebar.multiselect(
        "Filter by Phase:", 
        df['FASE'].unique(), 
        default=df['FASE'].unique()
    )
    df_filtered = df[df['FASE'].isin(phase)]
    
    # Charts
    phase_counts = df_filtered['FASE'].value_counts().reset_index()
    phase_counts.columns = ['FASE', 'count']
    
    chart = alt.Chart(phase_counts).mark_bar().encode(
        x='FASE:N',
        y='count:Q',
        color='FASE:N',
        tooltip=['FASE', 'count']
    ).properties(
        title="Distribution by Phase",
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Table and Download
    st.subheader("Data Table")
    st.dataframe(df_filtered)
    st.download_button(
        "📥 Download Data", 
        df_filtered.to_csv(index=False), 
        file_name="municipalities_to_install.csv"
    )

# ================== TAB 4 - MUNICIPALITIES TO INSTALL 2 ==================
def show_municipalities_to_install_2():
    st.header("🏗️ Municipalities to Install - Prov. 07 (Part 2)")
    df = load_data("MUNICÍPIOS PARA INSTALAR 2")

    # Filters
    phase = st.sidebar.multiselect(
        "Filter by Phase:", 
        df['FASE'].unique(), 
        default=df['FASE'].unique()
    )
    df_filtered = df[df['FASE'].isin(phase)]
    
    # Charts
    phase_counts = df_filtered['FASE'].value_counts().reset_index()
    phase_counts.columns = ['FASE', 'count']
    
    chart = alt.Chart(phase_counts).mark_bar().encode(
        x='FASE:N',
        y='count:Q',
        color='FASE:N',
        tooltip=['FASE', 'count']
    ).properties(
        title="Distribution by Phase",
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Table and Download
    st.subheader("Data Table")
    st.dataframe(df_filtered)
    st.download_button(
        "📥 Download Data", 
        df_filtered.to_csv(index=False), 
        file_name="municipalities_to_install_2.csv"
    )

# ================== TAB 5 - NON-VIABLE MUNICIPALITIES ==================
def show_nonviable_municipalities():
    st.header("🚫 Non-viable Municipalities for Installation")
    df = load_data("MUN. INVIÁVEIS DE INSTALAÇÃO")
    
    # Charts
    situation_counts = df['SITUAÇÃO'].value_counts().reset_index()
    situation_counts.columns = ['SITUAÇÃO', 'count']
    
    chart = alt.Chart(situation_counts).mark_bar().encode(
        x='SITUAÇÃO:N',
        y='count:Q',
        color='SITUAÇÃO:N',
        tooltip=['SITUAÇÃO', 'count']
    ).properties(
        title="Distribution by Situation",
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Table and Download
    st.subheader("Data Table")
    st.dataframe(df)
    st.download_button(
        "📥 Download Data", 
        df.to_csv(index=False), 
        file_name="nonviable_municipalities.csv"
    )

# ================== TAB 6 - PROVISION 09 ==================
def show_provision_09():
    st.header("📜 Provision 09 - Technical Cooperation Agreement (TCT)")
    df = load_data("PROVIMENTO 09")

    signed = df['MUNICÍPIOS QUE ASSINARAM O TCT'].dropna().count()
    will_sign = df['MUNICÍPIOS VÃO ASSINAR O TCT'].dropna().count()

    # KPIs
    metrics = {
        "Signed TCT": signed,
        "Will Sign": will_sign
    }
    display_metrics(metrics)
    
    # Chart
    tct_df = pd.DataFrame({
        'Status': ['Signed', 'Will Sign'],
        'Total': [signed, will_sign]
    })
    
    chart = alt.Chart(tct_df).mark_arc().encode(
        theta=alt.Theta(field="Total", type="quantitative"),
        color=alt.Color(field="Status", type="nominal"),
        tooltip=['Status', 'Total']
    ).properties(
        title="Technical Cooperation Agreement Status",
        height=400,
        width=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Table and Download
    st.subheader("Data Table")
    st.dataframe(df)
    st.download_button(
        "📥 Download Data", 
        df.to_csv(index=False), 
        file_name="provision09_tct.csv"
    )

# ================== MAIN APP LOGIC ==================
# Display selected tab
if selected_tab == "Interconnected Units":
    show_interconnected_units()
elif selected_tab == "Form Receipt Status":
    show_form_receipt_status()
elif selected_tab == "Municipalities to Install 1":
    show_municipalities_to_install_1()
elif selected_tab == "Municipalities to Install 2":
    show_municipalities_to_install_2()
elif selected_tab == "Non-viable Municipalities":
    show_nonviable_municipalities()
elif selected_tab == "Provision 09 - TCT":
    show_provision_09()
