import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns




st.set_page_config(layout="wide")
st.title("Relative Humidity")


st.markdown(
    """
    <style>
        /* Reduce sidebar width */
        [data-testid="stSidebar"] {
            width: 240px !important;
            min-width: 240px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)




@st.cache_data
def load_data():
    df = pd.read_parquet("project/new_df.parquet")
    return df

if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Access the data from session state
df = st.session_state.data




st.header("Summary Statistics")
mean_rh = df['Relative Humidity (%RH)'].mean()
min_rh = df['Relative Humidity (%RH)'].min()
max_rh = df['Relative Humidity (%RH)'].max()

col1, col2, col3 = st.columns(3)
col1.metric("Average Relative Humidity:", f"{mean_rh:.2f}")
col2.metric("Maximum Relative Humidity:", f"{max_rh:.2f}")
col3.metric("Minimum Relative Humidity:", f"{min_rh:.2f}")







selected_graphs = st.multiselect(
    "Select statistical graphs to display: (Optional)",
    ["Histogram", "Box-Plot"],
    default=["Histogram"]
)
col1, col2, col3 = st.columns(3)
if "Histogram" in selected_graphs:
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.histplot(df['Relative Humidity (%RH)'], bins=40, ax=ax, color='CornflowerBlue')
        ax.set_title('Histogram of Relative Humidity', fontsize=20)
        ax.set_xlabel('Relative Humidity (%RH)', fontsize=18)
        ax.set_ylabel('Density', fontsize=18)
        ax.tick_params(axis='both', labelsize=16)
        st.pyplot(fig)
if "Box-Plot" in selected_graphs: 
    with col2:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x=df['Relative Humidity (%RH)'], ax=ax, color='CornflowerBlue')
        ax.set_title('Box-Plot of Relative Humidity', fontsize=20)
        ax.set_xlabel('Relative Humidity (%RH)', fontsize=18)
        ax.tick_params(axis='both', labelsize=16)
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
    y=filtered_yearly_data['Relative Humidity (%RH)'],
    mode='lines',
    line=dict(color='CornflowerBlue')))
fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    height=300)
st.plotly_chart(fig, key="10")









st.sidebar.title("Select for Seasonal View")
selected_year = st.sidebar.selectbox("Select Year: (Optional)", [None] + list(df.index.year.unique()))
if selected_year:
    st.header("Sesonal Averages")
    df_year = df[df.index.year == selected_year]
    monthly_data = df_year.resample('M').mean(numeric_only=True)
    st.subheader(f"Summary statistics in {selected_year}")
    max_rh_m = monthly_data['Relative Humidity (%RH)'].max()
    min_rh_m = monthly_data['Relative Humidity (%RH)'].min()
    max_month = monthly_data['Relative Humidity (%RH)'].idxmax().month_name()
    min_month = monthly_data['Relative Humidity (%RH)'].idxmin().month_name()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label=f"Max Relative Humidity:", value=f"{max_rh_m:.2f}")
    col2.metric(label=f"Month with Max Relative Humidity:", value=f"{max_month:}")
    col3.metric(label=f"Min Relative Humidity:", value=f"{min_rh_m:.2f}")
    col4.metric(label=f"Month with Min Relative Humidity:", value=f"{min_month:}")
    other_variables = df_year[['Air Temperature (°C)', 'Wind Speed (km/h)']].columns.tolist()
    selected_variable = st.sidebar.radio("Select another variable to compare with Relative Humidity: (Optional)", options=[None] + other_variables, key="0")
    st.subheader(f"Monthly Averages in {selected_year}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['Relative Humidity (%RH)'],
                             mode='lines', name='Relative Humidity (%RH)', line=dict(color='dodgerblue')))
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=300)
    if selected_variable:
        fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data[selected_variable],
                                 mode='lines', name=selected_variable, line=dict(color='Coral'), yaxis="y2"))
        fig.update_layout(
            yaxis_title='Relative Humidity (%RH)',
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
    st.plotly_chart(fig, key="1")

    

    
    selected_month = st.sidebar.selectbox("Select Month: (Optional)", [None] + list(df_year.index.month_name().unique()))
    if selected_month:
        df_month = df_year[df_year.index.month_name() == selected_month]
        daily_data = df_month.resample('D').mean(numeric_only=True)
        st.subheader(f"Summary statistics in {selected_month} {selected_year}")
        max_rh_d = daily_data['Relative Humidity (%RH)'].max()
        min_rh_d = daily_data['Relative Humidity (%RH)'].min()
        max_day = daily_data['Relative Humidity (%RH)'].idxmax().day
        min_day = daily_data['Relative Humidity (%RH)'].idxmin().day
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label=f"Max Relative Humidity:", value=f"{max_rh_d:.2f}")
        col2.metric(label=f"Day with Max Relative Humidity:", value=f"{max_day:}")
        col3.metric(label=f"Min Relative Humidity:", value=f"{min_rh_d:.2f}")
        col4.metric(label=f"Day with Min Relative Humidity:", value=f"{min_day:}")
        other_variables = df_month[['Air Temperature (°C)', 'Wind Speed (km/h)']].columns.tolist()
        selected_variable = st.sidebar.radio("Select another variable to compare with Relative Humidity: (Optional)", options=[None] + other_variables, key="2")
        st.subheader(f"Daily Averages in {selected_month} {selected_year}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data['Relative Humidity (%RH)'],
                                 mode='lines', name='Relative Humidity (%RH)', line=dict(color='dodgerblue')))
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=300)
        if selected_variable:            
            fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data[selected_variable],
                                     mode='lines', name=selected_variable, line=dict(color='Coral'), yaxis="y2"))
            fig.update_layout(
                yaxis_title='Relative Humidity (%RH)',
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
        st.plotly_chart(fig, key="3")

        


        selected_day = st.sidebar.selectbox("Select Day: (Optional)", [None] + list(df_month.index.day.unique()))
        if selected_day:
            df_day = df_month[df_month.index.day == selected_day]
            hourly_data = df_day.resample('H').mean(numeric_only=True)
            st.subheader(f"Summary statistics on {selected_day} {selected_month} {selected_year}")
            max_rh_h = hourly_data['Relative Humidity (%RH)'].max()
            min_rh_h = hourly_data['Relative Humidity (%RH)'].min()
            max_hour = hourly_data['Relative Humidity (%RH)'].idxmax().hour
            min_hour = hourly_data['Relative Humidity (%RH)'].idxmin().hour
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label=f"Max Relative Humidity:", value=f"{max_rh_h:.2f}")
            col2.metric(label=f"Hour with Max Relative Humidity:", value=f"{max_hour:}")
            col3.metric(label=f"Min Relative Humidity:", value=f"{min_rh_h:.2f}")
            col4.metric(label=f"Hour with Min Relative Humidity:", value=f"{min_hour:}")
            other_variables = df_day[['Air Temperature (°C)', 'Wind Speed (km/h)']].columns.tolist()
            selected_variable = st.sidebar.radio("Select another variable to compare with Relative Humidity: (Optional)", options=[None] + other_variables, key="4")
            st.subheader(f"Hourly Averages on {selected_day} {selected_month} {selected_year}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hourly_data.index, y=hourly_data['Relative Humidity (%RH)'],
                                     mode='lines', name='Relative Humidity (%RH)', line=dict(color='dodgerblue')))
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                height=300)
            if selected_variable:
                fig.add_trace(go.Scatter(x=hourly_data.index, y=hourly_data[selected_variable],
                                         mode='lines', name=selected_variable, line=dict(color='Coral'), yaxis="y2"))
                fig.update_layout(
                    yaxis_title='Relative Humidity (%RH)',
                    yaxis2=dict(title=selected_variable if selected_variable else '', overlaying='y', side='right'),
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
