import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Load dataset
df_day = pd.read_csv("https://raw.githubusercontent.com/ZabrilaAmrina/dashboard/main/cleaned_bikeshare_day.csv")
df_hour = pd.read_csv("https://raw.githubusercontent.com/ZabrilaAmrina/dashboard/main/cleaned_bikeshare_hour.csv")
df_day['date'] = pd.to_datetime(df_day['date'])
df_hour['date'] = pd.to_datetime(df_hour['date'])
st.set_page_config(page_title="Capital Bikeshare: Bike-sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# Create helper functions
# (Your existing helper functions)

# Make filter components (komponen filter)
min_date = df_day["date"].min()
max_date = df_day["date"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # Add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/ZabrilaAmrina/dashboard/main/images.jpg")
    st.sidebar.header("Filter:")

    # Mengambil start_date & end_date dari date_input
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

    # Hubungkan filter dengan main_df
    main_df_day = df_day[
        (df_day["date"] >= str(start_date)) &
        (df_day["date"] <= str(end_date))
    ]
    main_df_hour = df_hour[
        (df_hour["date"] >= str(start_date)) &
        (df_hour["date"] <= str(end_date))
    ]

    # Assign main_df ke helper functions yang telah dibuat sebelumnya
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

    # Additional Seaborn Visualizations
    st.subheader("Additional Visualizations:")
       
    # Set style
    sns.set(style="whitegrid")

    # Peminjaman sepeda di hari libur
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(x='holiday', y='count', data=daily_data, estimator=sum, ci=None)
    plt.title('Total Peminjaman Sepeda pada Hari Libur')

    # Peminjaman sepeda di hari kerja
    plt.subplot(1, 2, 2)
    sns.barplot(x='workingday', y='count', data=daily_data, estimator=sum, ci=None)
    plt.title('Total Peminjaman Sepeda pada Hari Kerja')

    plt.tight_layout()
    st.pyplot()

    # Set style
    sns.set(style="whitegrid")

    # Visualisasi total peminjaman sepeda setiap tahun
    plt.figure(figsize=(12, 6))
    sns.barplot(x='year', y='count', data=yearly_total, palette='muted')
    plt.title('Total Peminjaman Sepeda Perusahaan Setiap Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Total Peminjaman')
    st.pyplot()

    # Menampilkan informasi tentang tahun dengan peminjaman tertinggi
    st.subheader(f"Tahun dengan Peminjaman Tertinggi: {tahun_peminjaman_tertinggi} (Jumlah: {jumlah_peminjaman_tertinggi})")
