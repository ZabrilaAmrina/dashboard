import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
 
# load dataset

df_day = pd.read_csv("https://raw.githubusercontent.com/ZabrilaAmrina/dashboard/main/cleaned_bikeshare_day.csv")
df_hour = pd.read_csv("https://raw.githubusercontent.com/ZabrilaAmrina/dashboard/main/cleaned_bikeshare_hour.csv")
df_day['date'] = pd.to_datetime(df_day['date'])
df_hour['date'] = pd.to_datetime(df_hour['date'])
st.set_page_config(page_title="Capital Bikeshare: Bike-sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# create helper functions

def create_monthly_users_df(df_day):
    monthly_users_df = df_day.resample(rule='M', on='date').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df_day):
    seasonly_users_df = df_day.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weatherly_users_df(df_day):
    weatherly_users_df = df_day.groupby("weather").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    weatherly_users_df = weatherly_users_df.reset_index()
    weatherly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weatherly_users_df = pd.melt(weatherly_users_df,
                                      id_vars=['weather'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weatherly_users_df['weather'] = pd.Categorical(weatherly_users_df['weather'],
                                             categories=['Clear/Partly Cloudy','Misty/Cloudy','Light Snow/Rain','Severe Weather'])
    weatherly_users_df = weatherly_users_df.sort_values('weather')
    
    return weatherly_users_df

def create_hourly_users_df(df_hour):
    hourly_users_df = df_hour.groupby('hour').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

# make filter components (komponen filter)

min_date = df_day["date"].min()
max_date = df_day["date"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/ZabrilaAmrina/dashboard/main/images.jpg")

    st.sidebar.header("Filter:")
    
    
    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Visit my Profile:")

st.sidebar.markdown("Zabrila Amrina Zadia Putri")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](www.linkedin.com/in/zabrila-amrina-a33812290)")
with col2:
    st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/ZabrilaAmrina)")

# hubungkan filter dengan main_df

main_df_day = df_day[
    (df_day["date"] >= str(start_date)) &
    (df_day["date"] <= str(end_date))
]
main_df_hour = df_hour[
    (df_hour["date"] >= str(start_date)) &
    (df_hour["date"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_df_day)
seasonly_users_df = create_seasonly_users_df(main_df_day)
hourly_users_df = create_hourly_users_df(main_df_hour)
weatherly_users_df = create_weatherly_users_df(main_df_day)

# ----- MAINPAGE -----
st.title("Capital Bikeshare: Bike-Sharing Dashboard Zabrila Amrina Zadia Putri")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df_day['count'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df_day['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df_day['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# ----- CHART -----
fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')

#st.plotly_chart(fig, use_container_width=True)
fig2 = px.bar(weatherly_users_df,
              x='weather',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by weather').update_layout(xaxis_title='', yaxis_title='Total Rides')


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig = px.line(hourly_users_df,
              x='hour',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=["skyblue", "orange"],
              markers=True,
              title='Count of bikeshare rides by hour of day').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

st.caption('Copyright (c), Created by Zabrila Amrina Zadia Putri')

st.subheader("Total Peminjaman Sepeda per Tahun")
total_yearly = main_df_day.groupby('year')[['registered', 'casual']].sum()
total_yearly['Jumlah penyewa'] = total_yearly.sum(axis=1)
years_yearly = total_yearly.index
total_rentals_yearly = total_yearly['Jumlah penyewa']
fig_yearly, ax_yearly = plt.subplots(figsize=(6, 2))
ax_yearly.bar(years_yearly, total_rentals_yearly, color=['skyblue', 'orange'])
ax_yearly.set_xlabel('Tahun')
ax_yearly.set_ylabel('Jumlah Penyewaan')
ax_yearly.set_title('Total Penyewaan Sepeda per Tahun')
st.pyplot(fig_yearly)
st.write("Terlihat jelas bahwa jumlah penyewaan pada tahun 2012 lebih tinggi dengan jumlah 2049576 daripada tahun 2011 dengan jumlah 2049576")

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
