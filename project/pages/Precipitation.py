import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns




st.set_page_config(layout="wide")
st.title("Precipitation")





df = st.session_state.data





st.header("Summary Statistics")
sum_prep = df['Precipitation (mm)'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Precipitation:", f"{sum_prep:.2f}")





selected_graphs = st.multiselect(
    "Select statistical graphs to display: (Optional)",
    ["KDE Plot", "Box Plot"],
    default=["KDE Plot"]
)
col1, col2, col3 = st.columns(3)
if "KDE Plot" in selected_graphs:
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.kdeplot(df['Precipitation (mm)'], fill=True, ax=ax, color='CornflowerBlue')
        ax.set_title('KDE Plot of Precipitation', fontsize=20)
        ax.set_xlabel('Precipitation (mm)', fontsize=18)
        ax.set_ylabel('Density', fontsize=18)
        ax.tick_params(axis='both', labelsize=16)
        st.pyplot(fig)
if "Box-Plot" in selected_graphs:
    with col2:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x=df['Precipitation (mm)'], ax=ax, color='CornflowerBlue')
        ax.set_title('Box-Plot of Precipitation', fontsize=20)
        ax.set_xlabel('Precipitation (mm)', fontsize=18)
        ax.tick_params(axis='both', labelsize=16)
        st.pyplot(fig)









yearly_data = df.resample('YE').sum(numeric_only=True)
start_year, end_year = st.slider(
    "Select Year Range: (Optional)",
    min_value=int(yearly_data.index.year.min()),
    max_value=int(yearly_data.index.year.max()),
    value=(int(yearly_data.index.year.min()), int(yearly_data.index.year.max())),
    step=1
)
filtered_yearly_data = yearly_data.loc[f"{start_year}":f"{end_year}"]
st.subheader(f"Yearly Totals ({start_year} - {end_year})")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=filtered_yearly_data.index,
    y=filtered_yearly_data['Precipitation (mm)'],
    mode='lines',
    line=dict(color='CornflowerBlue')))
fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    height=300)
st.plotly_chart(fig, key="10")









st.sidebar.title("Select for Seasonal View")
selected_year = st.sidebar.selectbox("Select Year: (Optional)", [None] + list(df.index.year.unique()))
if selected_year:
    st.header("Sesonal Totals")
    df_year = df[df.index.year == selected_year]
    monthly_data = df_year.resample('M').sum(numeric_only=True)
    st.subheader(f"Summary statistics in {selected_year}")
    max_prep_m = monthly_data['Precipitation (mm)'].max()
    max_month = monthly_data['Precipitation (mm)'].idxmax().month_name()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label=f"Max Precipitation:", value=f"{max_prep_m:.2f}")
    col2.metric(label=f"Month with Max Precipitation", value=f"{max_month:}")
    st.subheader(f"Monthly Totals in {selected_year}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['Precipitation (mm)'],
                             mode='lines', name='Precipitation (mm)', line=dict(color='CornflowerBlue')))
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=300)
    st.plotly_chart(fig, key="1")

    

    
    selected_month = st.sidebar.selectbox("Select Month: (Optional)", [None] + list(df_year.index.month_name().unique()))
    if selected_month:
        df_month = df_year[df_year.index.month_name() == selected_month]
        daily_data = df_month.resample('D').sum(numeric_only=True)
        st.subheader(f"Summary statistics in {selected_month} {selected_year}")
        max_prep_d = daily_data['Precipitation (mm)'].max()
        max_day = daily_data['Precipitation (mm)'].idxmax().day
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label=f"Max Precipitation:", value=f"{max_prep_d:.2f}")
        col2.metric(label=f"Day with Max Precipitation", value=f"{max_day:}")
        st.subheader(f"Daily Totals in {selected_month} {selected_year}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data['Precipitation (mm)'],
                                 mode='lines', name='Precipitation (mm)', line=dict(color='CornflowerBlue')))
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=300)
        st.plotly_chart(fig, key="3")

        


        selected_day = st.sidebar.selectbox("Select Day: (Optional)", [None] + list(df_month.index.day.unique()))
        if selected_day:
            df_day = df_month[df_month.index.day == selected_day]
            hourly_data = df_day.resample('H').sum(numeric_only=True)
            st.subheader(f"Summary statistics on {selected_day} {selected_month} {selected_year}")
            max_prep_h = hourly_data['Precipitation (mm)'].max()
            max_hour = hourly_data['Precipitation (mm)'].idxmax().hour
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label=f"Max Precipitation:", value=f"{max_prep_h:.2f}")
            col2.metric(label=f"Hour with Max Precipitation", value=f"{max_hour:}")
            st.subheader(f"Hourly Totals on {selected_day} {selected_month} {selected_year}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hourly_data.index, y=hourly_data['Precipitation (mm)'],
                                     mode='lines', name='Precipitation (mm)', line=dict(color='CornflowerBlue')))
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                height=300)
            st.plotly_chart(fig, key="5")
