import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
# Pastikan Anda telah mengganti 'your_data.csv' dengan nama file atau URL yang sesuai dengan data Anda
daily_data = pd.read_csv('day.csv')

# Function to set style and display barplot
def display_barplot(x, y, data, title, xlabel, ylabel):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x, y=y, data=data, estimator=sum, ci=None)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    st.pyplot()

# Function to display information
def display_info(info):
    st.write(info)

# Sidebar
st.sidebar.title("Pilih Visualisasi")

# Visualizations
visualization_option = st.sidebar.selectbox(
    "Pilih visualisasi:",
    ["Peminjaman Sepeda pada Hari Libur dan Hari Kerja", "Peminjaman Sepeda pada Setiap Musim", "Perbandingan Peminjaman Sepeda pada Cuaca Cerah dan Hujan", "Total Peminjaman Sepeda Perusahaan Setiap Tahun"]
)

if visualization_option == "Peminjaman Sepeda pada Hari Libur dan Hari Kerja":
    display_barplot('holiday', 'count', daily_data, 'Total Peminjaman Sepeda pada Hari Libur', 'Hari Libur (1) / Hari Kerja (0)', 'Total Peminjaman')
    display_barplot('workingday', 'count', daily_data, 'Total Peminjaman Sepeda pada Hari Kerja', 'Hari Kerja (1) / Hari Libur (0)', 'Total Peminjaman')

elif visualization_option == "Peminjaman Sepeda pada Setiap Musim":
    display_barplot('season', 'count', daily_data, 'Total Peminjaman Sepeda pada Setiap Musim', 'Musim', 'Total Peminjaman')

elif visualization_option == "Perbandingan Peminjaman Sepeda pada Cuaca Cerah dan Hujan":
    display_barplot('weather', 'count', daily_data, 'Perbandingan Peminjaman Sepeda pada Cuaca Cerah dan Hujan', 'Cuaca (1: Cerah, 3: Hujan)', 'Total Peminjaman')
    display_info(f"Cuaca dengan Peminjaman Sepeda Paling Banyak: {max_weather} (Jumlah: {max_count})")

elif visualization_option == "Total Peminjaman Sepeda Perusahaan Setiap Tahun":
    display_barplot('year', 'count', yearly_total, 'Total Peminjaman Sepeda Perusahaan Setiap Tahun', 'Tahun', 'Total Peminjaman')
    display_info(f"Tahun dengan Peminjaman Tertinggi: {tahun_peminjaman_tertinggi} (Jumlah: {jumlah_peminjaman_tertinggi})")
