#Import necessary libraries
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd


#Page configuration
st.set_page_config(page_title="Home Page", layout="wide")


#Placing Rothamsted logo and page title side by side
col1, col2 = st.columns([1, 5])  
with col1:
    st.image("C:/Users/user.NBIALPER/Desktop/codes/project/logo.jpg", width=180)  
with col2:
    st.markdown("<h1 style='margin-top: 20px;'>Welcome to the North Wyke Farm Platform Meteorological Data Dashboard!</h1>", unsafe_allow_html=True)
st.write(f"This web application features visualizations of various statistical methods applied to the 9-year (2014-2022) NWFP Meteorological (MET) data. For a variable-focused study, please select one of the MET measurements from the sidebar. Each section contains components of summary statistics, seasonal perspectives of the time series and comparisons of the selected measurement. For further evaluation, you may also visit the 'Missingness Impact' Tableau dashboard via the link provided below.")


#Adding a link to Tableau dashboard
st.markdown('👉[Click here to visit Tableau Public](https://public.tableau.com/app/profile/gulce.alper/vizzes)')


#Loading and caching data from local file
@st.cache_data
def load_data():
    df = pd.read_parquet("C:/Users/user.NBIALPER/Desktop/codes/project/new_df.parquet")
    return df


#Initializing session state to collect data at first load
if 'data' not in st.session_state:
    st.session_state.data = load_data()
df = st.session_state.data


#Placing NWFP map image and Plotly stacked bar chart side by side
col1, col2 = st.columns([1, 2]) 
with col1:
    st.image("C:/Users/user.NBIALPER/Desktop/codes/project/nwfp.png")
    st.markdown('<p style="text-align: center; font-size: 50px, font-weight: bold; color: black;">NWFP Map</p>', unsafe_allow_html=True)
melted_df = df.melt(value_vars=['Precipitation (mm) Quality', 'Air Temperature (°C) Quality', 
                                'Relative Humidity (%RH) Quality', 'Wind Speed (km/h) Quality', 'Wind Direction (°) Quality'], var_name='Category', value_name='Value')
with col2:
    fig = px.histogram(melted_df, x='Value', color='Category', barmode='stack')
    new_legend_titles = {
        'Precipitation (mm) Quality': 'Precipitation',
        'Air Temperature (°C) Quality': 'Air Temperature',
        'Relative Humidity (%RH) Quality': 'Relative Humidity',
        'Wind Speed (km/h) Quality': 'Wind Speed',
        'Wind Direction (°) Quality': 'Wind Direction'
        }
    fig.for_each_trace(lambda t: t.update(name=new_legend_titles.get(t.name, t.name)))
    fig.update_layout(
        title='The NWFP MET Data Quality Distribution by Variable',
        title_x=0.4,
        template='seaborn',
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='', showgrid=False),
        xaxis_title='NWFP Met Variables',
        yaxis_title='Count',
        bargap=0.3,
        width=800,
        height=550,
        legend=dict(title=None, orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5,))
    st.plotly_chart(fig)




















