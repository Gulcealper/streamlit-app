#Import necessary libraries
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd



#Page configuration
st.set_page_config(page_title="NWFP MET", layout="wide")




st.markdown(
    """
    <style>
        /* Reduce sidebar width */
        [data-testid="stSidebar"] {
            width: 190px !important;
            min-width: 190px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#Placing Rothamsted logo and page title side by side
col1, col2 = st.columns([1, 5])  
with col1:
    st.image("project/logo.jpg", width=100)  
with col2:
    st.markdown("<h1 style='margin-top: -10px; font-size: 34px; margin-right: 0px;'>Welcome to the North Wyke Farm Platform Meteorological Data Dashboard!</h1>", unsafe_allow_html=True)
st.write(f"This web application provides visualizations of seasonal changes of the 9-year (2014-2022) NWFP Meteorological (MET) data. For a variable-focused study, please select one of the MET measurements from the sidebar. Each section contains components of summary statistics, seasonal perspectives of the time series and a optional comparison of the selected variables. For further evaluation, you may also visit the 'Missing Data Analysis of NWFP MET Data' Tableau dashboard via the link provided below.")


#Adding a link to Tableau dashboard
st.markdown('👉[Click here to visit Tableau Public](https://public.tableau.com/app/profile/gulce.alper4379/viz/NWFPMET/Dashboard)')


#Loading and caching data from local file
@st.cache_data
def load_data():
    df = pd.read_parquet("project/new_df.parquet")
    return df


if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Access the data from session state
df = st.session_state.data


#Placing NWFP map image and Plotly stacked bar chart side by side
col1, col2 = st.columns([1, 2]) 
with col1:
    st.image("project/nwfp.png")
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
        title_x=0.3,
        template='seaborn',
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='', showgrid=False),
        xaxis_title='NWFP Met Variables',
        yaxis_title='Count',
        bargap=0.2,
        width=300,
        height=400,
        legend=dict(title=None, orientation='h', yanchor='bottom', y=-0.5, xanchor='center', x=0.1,))
    st.plotly_chart(fig)




















