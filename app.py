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

# Custom CSS styling
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
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #F8FAFC;
            border-radius: 4px 4px 0 0;
            padding: 10px 20px;
            border: 1px solid #E2E8F0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #DBEAFE;
            border-bottom: 2px solid #2563EB;
        }
    </style>
    """, unsafe_allow_html=True)

# Overview tab
def render_overview_tab(dataframes):
    st.markdown("<div class='sub-header'>Overview</div>", unsafe_allow_html=True)
    
    if "UNIDADES INTERLIGADAS" in dataframes:
        df = dataframes["UNIDADES INTERLIGADAS"]
        
        # Display main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Total units
        total_units = len(df)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_units}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Total Interconnected Units</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Total municipalities
        total_municipalities = df['MUNICÍPIOS'].nunique()
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_municipalities}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Unique Municipalities</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Units by administrative sphere
        if 'ESFERA ADMINISTRATIVA' in df.columns:
            sphere_counts = df['ESFERA ADMINISTRATIVA'].value_counts()
            most_common_sphere = sphere_counts.index[0] if not sphere_counts.empty else "N/A"
            sphere_count = sphere_counts.iloc[0] if not sphere_counts.empty else 0
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{sphere_count}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-label'>Units in {most_common_sphere}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Active units
        if 'SITUAÇÃO' in df.columns:
            active_units = df[df['SITUAÇÃO'] == 'ATIVA'].shape[0]
            active_percentage = (active_units / total_units) * 100 if total_units > 0 else 0
            with col4:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{active_units}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-label'>Active Units ({active_percentage:.1f}%)</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Data visualization section
        st.markdown("<div class='sub-header'>Data Visualization</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Distribution of units by municipality
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Units by Municipality")
            
            municipality_counts = df['MUNICÍPIOS'].value_counts().reset_index()
            municipality_counts.columns = ['Municipality', 'Count']
            
            # Get top 10 municipalities by unit count
            top_municipalities = municipality_counts.head(10)
            
            fig = px.bar(
                top_municipalities, 
                x='Municipality', 
                y='Count',
                color='Count',
                color_continuous_scale='Blues',
                labels={'Count': 'Number of Units', 'Municipality': 'Municipality'}
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=30, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Administrative sphere distribution
        with col2:
            if 'ESFERA ADMINISTRATIVA' in df.columns:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Administrative Sphere Distribution")
                
                sphere_counts = df['ESFERA ADMINISTRATIVA'].value_counts().reset_index()
                sphere_counts.columns = ['Sphere', 'Count']
                
                fig = px.pie(
                    sphere_counts, 
                    values='Count', 
                    names='Sphere',
                    color_discrete_sequence=px.colors.sequential.Blues,
                    hole=0.4
                )
                
                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Administrative sphere data not available.")
        
        # Installations over time
        if 'DATA DA INSTALAÇÃO' in df.columns:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Installations Over Time")
            
            # Convert to datetime
            df['DATA DA INSTALAÇÃO'] = pd.to_datetime(df['DATA DA INSTALAÇÃO'], errors='coerce')
            
            # Group by year and month
            df['year_month'] = df['DATA DA INSTALAÇÃO'].dt.strftime('%Y-%m')
            monthly_counts = df.groupby('year_month').size().reset_index(name='count')
            monthly_counts['cumulative'] = monthly_counts['count'].cumsum()
            
            # Create figure with secondary y-axis
            fig = go.Figure()
            
            # Add monthly installations
            fig.add_trace(go.Bar(
                x=monthly_counts['year_month'],
                y=monthly_counts['count'],
                name='Monthly Installations',
                marker_color='#93C5FD'
            ))
            
            # Add cumulative installations
            fig.add_trace(go.Scatter(
                x=monthly_counts['year_month'],
                y=monthly_counts['cumulative'],
                name='Cumulative Installations',
                marker_color='#1E40AF',
                yaxis='y2'
            ))
            
            # Set layout
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                yaxis=dict(
                    title='Monthly Installations',
                    titlefont=dict(color='#93C5FD'),
                    tickfont=dict(color='#93C5FD')
                ),
                yaxis2=dict(
                    title='Cumulative Installations',
                    titlefont=dict(color='#1E40AF'),
                    tickfont=dict(color='#1E40AF'),
                    overlaying='y',
                    side='right'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Main data sheet 'UNIDADES INTERLIGADAS' not found in the spreadsheet.")

# Interconnected units tab
def render_units_tab(dataframes):
    st.markdown("<div class='sub-header'>Interconnected Units Analysis</div>", unsafe_allow_html=True)
    
    if "UNIDADES INTERLIGADAS" in dataframes:
        df = dataframes["UNIDADES INTERLIGADAS"]
        
        # Add filters in sidebar
        st.sidebar.markdown("### Filters")
        
        # Municipality filter
        all_municipalities = sorted(df['MUNICÍPIOS'].unique())
        selected_municipalities = st.sidebar.multiselect(
            "Select Municipalities", 
            all_municipalities,
            default=[]
        )
        
        # Administrative sphere filter
        if 'ESFERA ADMINISTRATIVA' in df.columns:
            all_spheres = sorted(df['ESFERA ADMINISTRATIVA'].unique())
            selected_spheres = st.sidebar.multiselect(
                "Select Administrative Spheres", 
                all_spheres,
                default=[]
            )
        
        # Status filter
        if 'SITUAÇÃO' in df.columns:
            all_statuses = sorted(df['SITUAÇÃO'].unique())
            selected_statuses = st.sidebar.multiselect(
                "Select Status", 
                all_statuses,
                default=[]
            )
        
        # Apply filters
        filtered_df = df.copy()
        if selected_municipalities:
            filtered_df = filtered_df[filtered_df['MUNICÍPIOS'].isin(selected_municipalities)]
        if 'ESFERA ADMINISTRATIVA' in df.columns and selected_spheres:
            filtered_df = filtered_df[filtered_df['ESFERA ADMINISTRATIVA'].isin(selected_spheres)]
        if 'SITUAÇÃO' in df.columns and selected_statuses:
            filtered_df = filtered_df[filtered_df['SITUAÇÃO'].isin(selected_statuses)]
        
        # Main content
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Status Distribution")
            
            if 'SITUAÇÃO' in df.columns:
                status_counts = filtered_df['SITUAÇÃO'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                fig = px.pie(
                    status_counts, 
                    values='Count', 
                    names='Status',
                    color_discrete_sequence=px.colors.sequential.Blues,
                    hole=0.4
                )
                
                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Status data not available.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("
