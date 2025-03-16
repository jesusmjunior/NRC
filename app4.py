import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime
import traceback

# ================== DASHBOARD CONFIGURATION ==================
st.set_page_config(
    page_title="Dashboard of Interconnected Units", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard of Interconnected Units")
st.caption(f"Last update: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ================== LOAD DATA FROM GOOGLE SHEETS ==================
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(sheet_url):
    try:
        df = pd.read_csv(sheet_url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove Unnamed columns
        df.columns = df.columns.str.strip()  # Clean extra spaces
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error(traceback.format_exc())
        return pd.DataFrame()

# ================== Sheet URLs ==================
sheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

sheet_urls = {
    "INTERCONNECTED UNITS": f"{base_url}UNIDADES%20INTERLIGADAS",
    "FORM RECEIPT STATUS": f"{base_url}STATUS%20RECEB%20FORMULARIO",
    "MUNICIPALITIES TO INSTALL": f"{base_url}MUNICIPIOS%20PARA%20INSTALAR",
    "PROVISION 09": f"{base_url}PROVIMENTO%2009",
    "MUNICIPALITIES FOR REACTIVATION": f"{base_url}MUNIC%C3%8DPIOS%20PARA%20REATIVA",
    "ARTICULATION MONITORING": f"{base_url}TAB%20ACOMPANHAMENTO%20ARTICULA%C3%87%C3%83O",
    "UNDERREGISTRATION INDICES": f"{base_url}%C3%8DNDICES%20DE%20SUB-REGISTRO"
}

# ================== SIDEBAR - TAB SELECTION ==================
st.sidebar.header("📂 Tab Selection")
tabs = list(sheet_urls.keys())
selected_tab = st.sidebar.radio("Select a tab:", tabs)

# ================== LOADING SPINNER ==================
with st.spinner(f"Loading data from {selected_tab}..."):
    df = load_data(sheet_urls[selected_tab])

if df.empty:
    st.error(f"Could not load data from tab {selected_tab}.")
    st.stop()

# ================== HELPER FUNCTIONS ==================
def create_download_button(dataframe, filename):
    csv = dataframe.to_csv(index=False, encoding='utf-8-sig')
    return st.sidebar.download_button(
        label="📥 Download Data",
        data=csv.encode('utf-8-sig'),
        file_name=filename,
        mime='text/csv'
    )

def show_data_summary(dataframe):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total records", dataframe.shape[0])
    with col2:
        st.metric("Available columns", dataframe.shape[1])
    with col3:
        st.metric("Last update", datetime.now().strftime("%d/%m/%Y"))

# ================== TAB 1: INTERCONNECTED UNITS ==================
if selected_tab == "INTERCONNECTED UNITS":
    st.header("🏥 Interconnected Units")
    
    try:
        col_municipalities = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"
        col_sphere = "ESFERA"
        col_situation = "SITUAÇÃO GERAL" if "SITUAÇÃO GERAL" in df.columns else "SITUACAO GERAL"
        
        municipalities = st.sidebar.multiselect(
            "Select Municipalities", 
            df[col_municipalities].unique(), 
            default=df[col_municipalities].unique()
        )
        sphere = st.sidebar.multiselect(
            "Sphere", 
            df[col_sphere].unique(), 
            default=df[col_sphere].unique()
        )

        df_filtered = df[
            (df[col_municipalities].isin(municipalities)) & 
            (df[col_sphere].isin(sphere))
        ]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pie_data = df_filtered[col_situation].value_counts().reset_index()
            pie_data.columns = ['General Situation', 'Total']
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="General Situation", type="nominal"),
                tooltip=['General Situation', 'Total']
            ).properties(
                title="General Situation Distribution",
                height=300
            )
            st.altair_chart(pie_chart, use_container_width=True)
        with col2:
            mun_count = df_filtered[col_municipalities].value_counts().reset_index()
            mun_count.columns = ['Municipality', 'Total']
            if not mun_count.empty:
                bar_chart = alt.Chart(mun_count).mark_bar().encode(
                    x=alt.X('Municipality:N', sort='-y'),
                    y=alt.Y('Total:Q'),
                    color=alt.value('#1f77b4'),
                    tooltip=['Municipality', 'Total']
                ).properties(
                    title="Units by Municipality",
                    height=300
                )
                st.altair_chart(bar_chart, use_container_width=True)

        create_download_button(df_filtered, "interconnected_units.csv")
        
    except Exception as e:
        st.error(f"Error processing INTERCONNECTED UNITS tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== TAB 2: FORM RECEIPT STATUS ==================
elif selected_tab == "FORM RECEIPT STATUS":
    st.header("📄 Form Receipt Status")
    
    try:
        col_municipalities = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"
        col_status = "STATUS GERAL RECEBIMENTO"
        
        municipalities = st.sidebar.multiselect(
            "Select Municipalities", 
            df[col_municipalities].unique(), 
            default=df[col_municipalities].unique()
        )
        status = st.sidebar.multiselect(
            "General Receipt Status", 
            df[col_status].unique(), 
            default=df[col_status].unique()
        )

        df_filtered = df[
            (df[col_municipalities].isin(municipalities)) & 
            (df[col_status].isin(status))
        ]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pie_data = df_filtered[col_status].value_counts().reset_index()
            pie_data.columns = ['Status', 'Total']
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="Status", type="nominal"),
                tooltip=['Status', 'Total']
            ).properties(
                title="Receipt Status Distribution",
                height=300
            )
            st.altair_chart(pie_chart, use_container_width=True)
        with col2:
            mun_count = df_filtered[col_municipalities].value_counts().reset_index()
            mun_count.columns = ['Municipality', 'Total']
            if not mun_count.empty:
                bar_chart = alt.Chart(mun_count).mark_bar().encode(
                    x=alt.X('Municipality:N', sort='-y'),
                    y=alt.Y('Total:Q'),
                    color=alt.value('#1f77b4'),
                    tooltip=['Municipality', 'Total']
                ).properties(
                    title="Records by Municipality",
                    height=300
                )
                st.altair_chart(bar_chart, use_container_width=True)

        create_download_button(df_filtered, "receipt_status.csv")
        
    except Exception as e:
        st.error(f"Error processing FORM RECEIPT STATUS tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== TAB 3: MUNICIPALITIES TO INSTALL ==================
elif selected_tab == "MUNICIPALITIES TO INSTALL":
    st.header("🔹 Municipalities to Install")
    
    try:
        col_municipalities = "MUNICÍPIOS" if "MUNICÍPIOS" in df.columns else "MUNICIPIOS"
        
        municipalities = st.sidebar.multiselect(
            "Select Municipalities", 
            df[col_municipalities].unique(), 
            default=df[col_municipalities].unique()
        )
        
        df_filtered = df[df[col_municipalities].isin(municipalities)]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        create_download_button(df_filtered, "municipalities_to_install.csv")
        
    except Exception as e:
        st.error(f"Error processing MUNICIPALITIES TO INSTALL tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== TAB 4: PROVISION 09 ==================
elif selected_tab == "PROVISION 09":
    st.header("📜 Provision 09 - Signed TCT")
    
    try:
        col_municipalities = "MUNICÍPIOS QUE ASSINARAM O TCT" if "MUNICÍPIOS QUE ASSINARAM O TCT" in df.columns else "MUNICÍPIOS"
        
        municipalities = st.sidebar.multiselect(
            "Select Municipalities that Signed", 
            df[col_municipalities].unique(), 
            default=df[col_municipalities].unique()
        )
        
        df_filtered = df[df[col_municipalities].isin(municipalities)]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        create_download_button(df_filtered, "provision_09.csv")
        
    except Exception as e:
        st.error(f"Error processing PROVISION 09 tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== TAB 5: MUNICIPALITIES FOR REACTIVATION ==================
elif selected_tab == "MUNICIPALITIES FOR REACTIVATION":
    st.header("🔄 Municipalities for Reactivation")
    try:
        col_municipalities = "MUNICÍPIO"
        col_situation = "SITUAÇÃO"

        municipalities = st.sidebar.multiselect(
            "Select Municipalities", 
            df[col_municipalities].unique(), 
            default=df[col_municipalities].unique()
        )
        situation = st.sidebar.multiselect(
            "Situation", 
            df[col_situation].unique(), 
            default=df[col_situation].unique()
        )

        df_filtered = df[(df[col_municipalities].isin(municipalities)) & (df[col_situation].isin(situation))]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        create_download_button(df_filtered, "municipalities_reactivation.csv")
        
    except Exception as e:
        st.error(f"Error processing tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== TAB 6: ARTICULATION MONITORING ==================
elif selected_tab == "ARTICULATION MONITORING":
    st.header("📑 Articulation Monitoring")
    try:
        col_situation = "SITUAÇÃO"
        col_municipalities = "MUNICÍPIOS"

        situation = st.sidebar.multiselect(
            "Select Situation", 
            df[col_situation].unique(), 
            default=df[col_situation].unique()
        )
        municipalities = st.sidebar.multiselect(
            "Select Municipalities", 
            df[col_municipalities].unique(), 
            default=df[col_municipalities].unique()
        )

        df_filtered = df[(df[col_situation].isin(situation)) & (df[col_municipalities].isin(municipalities))]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        create_download_button(df_filtered, "articulation_monitoring.csv")
        
    except Exception as e:
        st.error(f"Error processing tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== TAB 7: UNDERREGISTRATION INDICES ==================
elif selected_tab == "UNDERREGISTRATION INDICES":
    st.header("📉 Underregistration Indices")
    try:
        col_city = "CIDADE"
        cities = st.sidebar.multiselect(
            "Select Cities", 
            df[col_city].unique(), 
            default=df[col_city].unique()
        )

        df_filtered = df[df[col_city].isin(cities)]

        show_data_summary(df_filtered)
        st.write(f"### 📌 {df_filtered.shape[0]} Selected Records")
        st.dataframe(df_filtered, use_container_width=True)

        create_download_button(df_filtered, "underregistration_indices.csv")
        
    except Exception as e:
        st.error(f"Error processing tab: {str(e)}")
        st.error(traceback.format_exc())

# ================== FINAL MESSAGE ==================
st.success("✅ Dashboard updated with data from Google Sheets!")
