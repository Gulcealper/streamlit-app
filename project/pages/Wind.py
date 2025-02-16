
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np


st.set_page_config(layout="wide")
st.title("Wind Speed/Direction")






# Access the data from session state
df = st.session_state.data



st.header("Summary Statistics")
mean_ws = df['Wind Speed (km/h)'].mean()
min_ws = df['Wind Speed (km/h)'].min()
max_ws = df['Wind Speed (km/h)'].max()


col1, col2, col3 = st.columns(3)
col1.metric("Average Wind Speed:", f"{mean_ws:.2f}")
col2.metric("Maximum Wind Speed:", f"{max_ws:.2f}")
col3.metric("Minimum Wind Speed:", f"{min_ws:.2f}")






selected_graphs = st.multiselect(
    "Select statistical graphs to display: (Optional)",
    ["Histogram", "Box Plot", "Rose Plot"],
    default=["Histogram"]
)
col1, col2, col3 = st.columns(3)
if "Histogram" in selected_graphs:
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.histplot(df['Wind Speed (km/h)'], bins=40, ax=ax, color='CornflowerBlue')
        ax.set_title('Histogram of Wind Speed', fontsize=20)
        ax.set_xlabel('Wind Speed (km/h)', fontsize=18)
        ax.set_ylabel('Density', fontsize=18)
        ax.tick_params(axis='both', labelsize=16)
        st.pyplot(fig)
if "Box Plot" in selected_graphs: 
    with col2:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x=df['Wind Speed (km/h)'], ax=ax, color='CornflowerBlue')
        ax.set_title('Box-Plot of Wind Speed', fontsize=20)
        ax.set_xlabel('Wind Speed (km/h)', fontsize=18)
        ax.tick_params(axis='both', labelsize=16)
        st.pyplot(fig)
if "Rose Plot" in selected_graphs:
    with col3:
        angles = np.deg2rad(df['Wind Direction (°)'])
        direction_names = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        angles_ticks = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3, 3))
        ax.hist(angles, bins=35, color='CornflowerBlue', edgecolor='black')
        ax.set_xticks(angles_ticks)  
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_title('Rose Plot of Wind Direction', fontsize=10)
        ax.set_xticklabels(direction_names, fontsize=10)
        ax.set_yticks([])
        st.pyplot(fig)








yearly_data = df.resample('YE').mean(numeric_only=True)
start_year, end_year = st.slider(
    "Select Year Range: (Optional)",
    min_value=int(yearly_data.index.year.min()),
    max_value=int(yearly_data.index.year.max()),
    value=(int(yearly_data.index.year.min()), int(yearly_data.index.year.max())),
    step=1
)
filtered_yearly_data = yearly_data.loc[f"{start_year}":f"{end_year}"]
st.subheader(f"Yearly Averages ({start_year} - {end_year})")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=filtered_yearly_data.index,
    y=filtered_yearly_data['Wind Speed (km/h)'],
    mode='lines',
    line=dict(color='CornflowerBlue')))
fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    height=300)
st.plotly_chart(fig, key="0")








st.sidebar.title("Select for Seasonal View")
selected_year = st.sidebar.selectbox("Select Year: (Optional)", [None] + list(df.index.year.unique()))
if selected_year:
    st.header("Sesonal Averages")
    df_year = df[df.index.year == selected_year]
    monthly_data = df_year.resample('M').mean(numeric_only=True)
    st.subheader(f"Summary statistics in {selected_year}")
    max_ws_m = monthly_data['Wind Speed (km/h)'].max()
    min_ws_m = monthly_data['Wind Speed (km/h)'].min()
    max_month = monthly_data['Wind Speed (km/h)'].idxmax().month_name()
    min_month = monthly_data['Wind Speed (km/h)'].idxmin().month_name()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label=f"Max Wind Speed:", value=f"{max_ws_m:.2f}")
    col2.metric(label=f"Month with Max Wind Speed:", value=f"{max_month:}")
    col3.metric(label=f"Min Wind Speed:", value=f"{min_ws_m:.2f}")
    col4.metric(label=f"Month with Min Wind Speed:", value=f"{min_month:}")
    other_variables = df_year[['Air Temperature (°C)', 'Relative Humidity (%RH)']].columns.tolist()
    selected_variable = st.sidebar.radio("Select another variable to compare with Wind Speed: (Optional)", options=[None] + other_variables, key="1")
    st.subheader(f"Monthly Averages in {selected_year}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['Wind Speed (km/h)'],
                             mode='lines', name='Wind Speed (km/h)', line=dict(color='dodgerblue')))
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=300)
    if selected_variable:
        fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data[selected_variable],
                                 mode='lines', name=selected_variable, line=dict(color='Coral'), yaxis="y2"))
        fig.update_layout(
            yaxis_title='Wind Speed (km/h)',
            yaxis2=dict(title=selected_variable if selected_variable else '', overlaying='y', side='right'),
            margin=dict(t=0, b=0, l=0, r=0),
            height=300,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.3,
                xanchor='center', 
                x=0.5
            )
        )
    st.plotly_chart(fig, key="2")
    angles = np.deg2rad(monthly_data['Wind Direction (°)'])
    r = monthly_data['Wind Speed (km/h)']    
    fig_polar_monthly = go.Figure(
        data=go.Scatterpolar(
            r=r, 
            theta=np.rad2deg(angles),  
            mode='markers',  
            marker=dict(
                color=r,
                colorscale='ice_r',
                line=dict(width=1, color='black'),
                size=15,
                colorbar=dict(title='Wind Speed', x=1, y=0.5, len=1.5)),
                opacity=0.70 ))
    fig_polar_monthly.update_layout(
        width=450,
        height=450,
        margin=dict(t=0, b=0, l=0, r=0),
        polar=dict(
            angularaxis=dict(
                direction="clockwise",  
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                tickmode='array',),
            radialaxis=dict(
                visible=True,
                ticks='outside')))
    st.subheader(f"Monthly Wind Directions in {selected_year}")
    st.plotly_chart(fig_polar_monthly, key="3")


    

    selected_month = st.sidebar.selectbox("Select Month: (Optional)", [None] + list(df_year.index.month_name().unique()))
    if selected_month:
        df_month = df_year[df_year.index.month_name() == selected_month]
        daily_data = df_month.resample('D').mean(numeric_only=True)
        st.subheader(f"Summary statistics in {selected_month} {selected_year}")
        max_ws_d = daily_data['Wind Speed (km/h)'].max()
        min_ws_d = daily_data['Wind Speed (km/h)'].min()
        max_day = daily_data['Wind Speed (km/h)'].idxmax().day
        min_day = daily_data['Wind Speed (km/h)'].idxmin().day
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label=f"Max Wind Speed:", value=f"{max_ws_d:.2f}")
        col2.metric(label=f"Day with Max Wind Speed:", value=f"{max_day:}")
        col3.metric(label=f"Min Wind Speed:", value=f"{min_ws_d:.2f}")
        col4.metric(label=f"Day with Min Wind Speed:", value=f"{min_day:}")
        other_variables = df_month[['Air Temperature (°C)', 'Relative Humidity (%RH)']].columns.tolist()
        selected_variable = st.sidebar.radio("Select another variable to compare with Wind Speed: (Optional)", options=[None] + other_variables, key="4")
        st.subheader(f"Daily Averages in {selected_month} {selected_year}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data['Wind Speed (km/h)'],
                                 mode='lines', name='Wind Speed (km/h)', line=dict(color='dodgerblue')))
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=300)
        if selected_variable:
            fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data[selected_variable],
                                     mode='lines', name=selected_variable, line=dict(color='Coral'), yaxis="y2"))
            fig.update_layout(
                yaxis_title='Wind Speed (km/h)',
                yaxis2=dict(title=selected_variable if selected_variable else '', overlaying='y', side='right'),
                margin=dict(t=0, b=0, l=0, r=0),
                height=300,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=-0.3,
                    xanchor='center', 
                    x=0.5
                )
            )
        st.plotly_chart(fig, key="5")
        angles = np.deg2rad(daily_data['Wind Direction (°)'])
        r = daily_data['Wind Speed (km/h)']
        fig_polar_daily = go.Figure(
            data=go.Scatterpolar(
                r=r,  
                theta=np.rad2deg(angles),  
                mode='markers',  
                marker=dict(
                    color=r,
                    colorscale='ice_r',
                    line=dict(width=1, color='black'),
                    size=15,
                    colorbar=dict(title='Wind Speed', x=1, y=0.5, len=1.5)),
                    opacity=0.70 ))
        fig_polar_daily.update_layout(
            width=450,
            height=450,
            margin=dict(t=0, b=0, l=0, r=0),
            polar=dict(
                angularaxis=dict(
                    direction="clockwise",  
                    tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                    ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                    tickmode='array',),
                radialaxis=dict(
                    visible=True,
                    ticks='outside')))
        st.subheader(f"Daily Wind Directions in {selected_month} {selected_year}")
        st.plotly_chart(fig_polar_daily, key="6")




        selected_day = st.sidebar.selectbox("Select Day: (Optional)", [None] + list(df_month.index.day.unique()))
        if selected_day:
            df_day = df_month[df_month.index.day == selected_day]
            hourly_data = df_day.resample('H').mean(numeric_only=True)
            st.subheader(f"Summary statistics on {selected_day} {selected_month} {selected_year}")
            max_ws_h = hourly_data['Wind Speed (km/h)'].max()
            min_ws_h = hourly_data['Wind Speed (km/h)'].min()
            max_hour = hourly_data['Wind Speed (km/h)'].idxmax().hour
            min_hour = hourly_data['Wind Speed (km/h)'].idxmin().hour
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label=f"Max Wind Speed:", value=f"{max_ws_h:.2f}")
            col2.metric(label=f"Hour with Max Wind Speed:", value=f"{max_hour:}")
            col3.metric(label=f"Min Wind Speed:", value=f"{min_ws_h:.2f}")
            col4.metric(label=f"Hour with Min Wind Speed:", value=f"{min_hour:}")
            other_variables = df_day[['Air Temperature (°C)', 'Relative Humidity (%RH)']].columns.tolist()
            selected_variable = st.sidebar.radio("Select another variable to compare with Wind Speed: (Optional)", options=[None] + other_variables, key="7")
            st.subheader(f"Hourly Averages on {selected_day} {selected_month} {selected_year}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hourly_data.index, y=hourly_data['Wind Speed (km/h)'],
                                     mode='lines', name='Wind Speed (km/h)', line=dict(color='dodgerblue')))
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                height=300)
            if selected_variable:
                fig.add_trace(go.Scatter(x=hourly_data.index, y=hourly_data[selected_variable],
                                         mode='lines', name=selected_variable, line=dict(color='Coral'), yaxis="y2"))
                fig.update_layout(
                    yaxis_title='Wind Speed (km/h)',
                    yaxis2=dict(title=selected_variable if selected_variable else '', overlaying='y', side='right'),
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=300,
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=-0.3,
                        xanchor='center', 
                        x=0.5
                    )
                )
            st.plotly_chart(fig, key="8")
            angles = np.deg2rad(hourly_data['Wind Direction (°)'])
            r = hourly_data['Wind Speed (km/h)']
            fig_polar_hourly = go.Figure(
                data=go.Scatterpolar(
                    r=r,  
                    theta=np.rad2deg(angles),  
                    mode='markers',
                    marker=dict(
                        color=r,
                        colorscale='ice_r',
                        line=dict(width=1, color='black'),
                        size=15,
                        colorbar=dict(title='Wind Speed', x=1, y=0.5, len=1.5)),
                        opacity=0.70 ))
            fig_polar_hourly.update_layout(
                width=450,
                height=450,
                margin=dict(t=0, b=0, l=0, r=0),
                polar=dict(
                    angularaxis=dict(
                        direction="clockwise",  
                        tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                        ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                        tickmode='array',),
                    radialaxis=dict(
                        visible=True,
                        ticks='outside')))
            st.subheader(f"Hourly Wind Directions on {selected_day} {selected_month} {selected_year}")
            st.plotly_chart(fig_polar_hourly, key="9")





        


  

        


   
    

    



