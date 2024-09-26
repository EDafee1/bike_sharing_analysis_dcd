import streamlit as st
import pandas as pd
import plotly.express as px

# data prep
path_day = 'day.csv'
path_hour = 'hour.csv'

df_day = pd.read_csv(path_day)
df_hour = pd.read_csv(path_hour)

# title config
st.set_page_config(layout="wide", page_title='Submission')
st.title('Python Data Analysis')
st.header('Bike Sharing Dataset', divider='violet')
st.caption('Muhammad Dafi Hisbullah')

# kpi card
total_rentals = df_hour['cnt'].sum()
avg_rentals_day = df_day['cnt'].mean()
avg_rentals_hour = df_hour['cnt'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", total_rentals)
col2.metric("Avg. Rentals/Day", f"{avg_rentals_day:.2f}")
col3.metric("Avg. Rentals/Hour", f"{avg_rentals_hour:.2f}")

# time-series rentals
st.subheader("Rentals Over Time")
st.line_chart(df_day.set_index('dteday')['cnt'])

# rentals vs weather
st.subheader("Rentals vs. Weather")
st.scatter_chart(df_hour[['temp', 'cnt']].rename(columns={'temp': 'Temperature', 'cnt': 'Rentals'}), x='Temperature', y='Rentals')
st.scatter_chart(df_hour[['hum', 'cnt']].rename(columns={'hum': 'Humidity', 'cnt': 'Rentals'}), x='Humidity', y='Rentals')

# rentals by season and weathersit
st.subheader("Rentals by Category")

df_season_boxplot = df_hour.copy()
df_season_boxplot['season'] = df_season_boxplot['season'].map({
    1: 'Winter',
    2: 'Spring',
    3: 'Summer',
    4: 'Fall'
})
fig_season = px.box(df_season_boxplot, x='season', y='cnt', title='Rentals by Season')
st.plotly_chart(fig_season)

df_weather_boxplot = df_hour.copy()
df_weather_boxplot['weathersit'] = df_weather_boxplot['weathersit'].map({
    1: 'Clear, Few clouds',
    2: 'Mist + Cloudy',
    3: 'Light Snow, Light Rain',
    4: 'Heavy Rain, Ice Pallets'
})
fig_weather = px.box(df_weather_boxplot, x='weathersit', y='cnt', title='Rentals by Weather Situation')
st.plotly_chart(fig_weather)

# holiday
st.subheader("Rentals by Holiday")

fig_holiday = px.box(df_weather_boxplot, x='holiday', y='cnt', title='Rentals on Holiday vs Non-Holiday')
st.plotly_chart(fig_holiday)

# corr matrix
st.subheader("Correlation Matrix")

corr_matrix = df_hour.corr(numeric_only=True)
fig_heatmap = px.imshow(corr_matrix, 
                        x=corr_matrix.columns, 
                        y=corr_matrix.columns, 
                        color_continuous_scale='RdBu_r', 
                        title="Correlation Matrix",
                        height=700)
st.plotly_chart(fig_heatmap)