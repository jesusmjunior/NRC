# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import io
import os
from gspread_pandas import Spread, Client

# Set page configuration
st.set_page_config(
    page_title="NRC CGJ - Unidades Interligadas Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load data from Google Sheets
@st.cache_data(ttl=600)
def load_data():
    """
    Load data from Google Sheets using service account credentials
    """
    try:
        # The URL contains the spreadsheet ID
        spreadsheet_id = "1cWbDNgy8Fu75FvXLvk-q2RQ0X-n7OsXq"
        
        # For local development, use credentials.json
        # For deployment, use Streamlit secrets
        if os.path.exists('credentials.json'):
            credentials = service_account.Credentials.from_service_account_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets', 
                        'https://www.googleapis.com/auth/drive']
            )
        else:
            # Use Streamlit secrets for deployment
            credentials_dict = st.secrets["gcp_service_account"]
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets', 
                        'https://www.googleapis.com/auth/drive']
            )
        
        # Initialize gspread client
        client = gspread.authorize(credentials)
        
        # Open the spreadsheet
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        # Get all worksheets
        worksheets = spreadsheet.worksheets()
        
        # Create a dictionary to store dataframes
        dataframes = {}
        
        # Read each worksheet
        for sheet in worksheets:
            sheet_name = sheet.title
            data = sheet.get_all_values()
            if data:
                headers = data[0]
                if len(data) > 1:
                    df = pd.DataFrame(data[1:], columns=headers)
                    dataframes[sheet_name] = df
        
        return dataframes
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Apply custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #1E3A8A;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2563EB;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .card {
            background-color: #F1F5F9;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #EFF6FF;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1E40AF;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #64748B;
        }
        .divider {
            height: 2px;
            background-color: #E2E8F0;
            margin: 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Form status tab
def render_form_status_tab(dataframes):
    st.markdown("<div class='sub-header'>Form Submission Status</div>", unsafe_allow_html=True)
    
    if "STATUS RECEB FORMULARIO" in dataframes:
        df = dataframes["STATUS RECEB FORMULARIO"]
        
        # Calculate metrics
        total_forms = len(df)
        received_forms = df[df["STATUS GERAL"] == "RECEBIDO"].shape[0] if "STATUS GERAL" in df.columns else 0
        pending_forms = total_forms - received_forms
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_forms}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Total Forms</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{received_forms}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Received Forms</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{pending_forms}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Pending Forms</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Data table
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.subheader("Form Status Details")
        st.dataframe(df)
    else:
        st.error("Data sheet 'STATUS RECEB FORMULARIO' not found in the spreadsheet.")

# Installation tab
def render_installation_tab(dataframes):
    st.markdown("<div class='sub-header'>Installation Analysis</div>", unsafe_allow_html=True)
    
    # Check if the installation sheets exist
    if "MUNICÍPIOS PARA INSTALAR" in dataframes and "MUN. INVIÁVEIS DE INSTALAÇÃO" in dataframes:
        to_install_df = dataframes["MUNICÍPIOS PARA INSTALAR"]
        not_viable_df = dataframes["MUN. INVIÁVEIS DE INSTALAÇÃO"]
        
        # Calculate metrics
        to_install_count = len(to_install_df)
        not_viable_count = len(not_viable_df)
        
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{to_install_count}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Municipalities To Install</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{not_viable_count}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Non-Viable Municipalities</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Display data tables
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["To Install", "Non-Viable"])
        
        with tab1:
            st.subheader("Municipalities To Install")
            st.dataframe(to_install_df)
        
        with tab2:
            st.subheader("Non-Viable Municipalities")
            st.dataframe(not_viable_df)
    else:
        st.error("Installation data sheets not found in the spreadsheet.")

# Predictive Analysis Tab
def render_predictive_tab(dataframes):
    st.markdown("<div class='sub-header'>Predictive Analysis</div>", unsafe_allow_html=True)
    
    if "UNIDADES INTERLIGADAS" in dataframes:
        df = dataframes["UNIDADES INTERLIGADAS"]
        
        st.markdown("""
        This tab provides predictive analytics based on historical installation data. 
        The analysis helps forecast future installations and identify potential patterns.
        """)
        
        # Check if we have installation date data
        if 'DATA DA INSTALAÇÃO' in df.columns:
            # Convert to datetime
            df['DATA DA INSTALAÇÃO'] = pd.to_datetime(df['DATA DA INSTALAÇÃO'], errors='coerce')
            
            # Create year-month field
            df['year_month'] = df['DATA DA INSTALAÇÃO'].dt.strftime('%Y-%m')
            
            # Monthly installation counts
            monthly_counts = df.groupby('year_month').size().reset_index(name='count')
            
            # Simple moving average for trend
            window_size = min(3, len(monthly_counts))
            monthly_counts['trend'] = monthly_counts['count'].rolling(window=window_size).mean()
            
            # Create chart
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Installation Trend Analysis")
            
            fig = px.line(
                monthly_counts, 
                x='year_month', 
                y=['count', 'trend'],
                labels={'value': 'Number of Installations', 'year_month': 'Month', 'variable': 'Metric'},
                color_discrete_map={'count': '#3B82F6', 'trend': '#1E40AF'}
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=30, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Simple projection
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Installation Projection")
            
            # Calculate average monthly installations (last 6 months or all if less)
            recent_months = min(6, len(monthly_counts))
            avg_monthly = monthly_counts['count'].tail(recent_months).mean()
            
            # Create projection for next 6 months
            last_date = pd.to_datetime(monthly_counts['year_month'].iloc[-1])
            future_dates = [(last_date + pd.DateOffset(months=i+1)).strftime('%Y-%m') for i in range(6)]
            future_df = pd.DataFrame({
                'year_month': future_dates,
                'projected': [round(avg_monthly)] * 6
            })
            
            # Combine with historical data
            hist_df = monthly_counts[['year_month', 'count']].rename(columns={'count': 'historical'})
            combined_df = pd.merge(hist_df, future_df, on='year_month', how='outer')
            
            # Plot
            fig = go.Figure()
            
            # Historical line
            fig.add_trace(go.Scatter(
                x=combined_df['year_month'],
                y=combined_df['historical'],
                name='Historical',
                line=dict(color='#3B82F6', width=2)
            ))
            
            # Projection line
            fig.add_trace(go.Scatter(
                x=combined_df['year_month'],
                y=combined_df['projected'],
                name='Projection',
                line=dict(color='#10B981', width=2, dash='dash')
            ))
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title='Month',
                yaxis_title='Number of Installations'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""
            Based on the last {recent_months} months of data, we project an average of 
            **{avg_monthly:.1f} new installations per month** over the next 6 months.
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Installation date data is not available for predictive analysis.")
    else:
        st.error("Main data sheet 'UNIDADES INTERLIGADAS' not found in the spreadsheet.")

# Main app function
def main():
    apply_custom_css()
    
    # App header
    st.markdown("<div class='main-header'>NRC CGJ - Unidades Interligadas Dashboard</div>", unsafe_allow_html=True)
    
    # Load data
    dataframes = load_data()
    
    if dataframes:
        # Create tabs
        tabs = st.tabs(["Overview", "Interconnected Units", "Form Status", "Installation Analysis", "Predictive Analysis"])
        
        with tabs[0]:
            render_overview_tab(dataframes)
        
        with tabs[1]:
            render_units_tab(dataframes)
        
        with tabs[2]:
            render_form_status_tab(dataframes)
        
        with tabs[3]:
            render_installation_tab(dataframes)
        
        with tabs[4]:
            render_predictive_tab(dataframes)
    else:
        st.error("Failed to load data. Please check your connection and credentials.")

if __name__ == "__main__":
    main()
