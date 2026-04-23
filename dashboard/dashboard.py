import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
from babel.numbers import format_currency

sns.set(style='dark')

def create_daily_rentals_df(df):
    """Membuat dataframe peminjaman harian"""
    # Filter hanya data harian (hr is NaN)
    daily_data = df[df['hr'].isna()].copy()
    daily_data = daily_data.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_data = daily_data.reset_index()
    daily_data.rename(columns={
        "cnt": "total_rentals",
        "casual": "casual_rentals",
        "registered": "registered_rentals"
    }, inplace=True)
    return daily_data

def create_season_df(df):
    """Membuat dataframe peminjaman berdasarkan musim"""
    # Filter hanya data harian (hr is NaN)
    daily_data = df[df['hr'].isna()].copy()
    season_df = daily_data.groupby(by="season_desc").agg({
        "cnt": "mean",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    season_df["season_desc"] = pd.Categorical(season_df["season_desc"], categories=season_order, ordered=True)
    season_df = season_df.sort_values("season_desc").reset_index(drop=True)
    season_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return season_df

def create_weather_df(df):
    """Membuat dataframe peminjaman berdasarkan kondisi cuaca"""
    # Gunakan data per jam agar kategori Heavy Rain/Ice tetap muncul
    # dan skala rata-rata sesuai visualisasi referensi.
    hourly_data = df[df['hr'].notna()].copy()
    weather_df = hourly_data.groupby(by="weather_desc").agg({
        "cnt": "mean",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()

    # Urutan kategori cuaca mengikuti tampilan referensi.
    weather_order = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Snow/Rain", "Heavy Rain/Ice"]
    weather_df["weather_desc"] = pd.Categorical(weather_df["weather_desc"], categories=weather_order, ordered=True)
    weather_df = weather_df.sort_values("weather_desc").reset_index(drop=True)

    weather_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return weather_df

def create_weekday_df(df):
    """Membuat dataframe peminjaman berdasarkan hari dalam seminggu"""
    weekday_df = df.groupby(by="weekday_desc").agg({
        "cnt": "mean",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_df["weekday_desc"] = pd.Categorical(weekday_df["weekday_desc"], categories=weekday_order, ordered=True)
    weekday_df = weekday_df.sort_values("weekday_desc").reset_index(drop=True)
    weekday_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return weekday_df

def create_hourly_df(df):
    """Membuat dataframe peminjaman per jam"""
    hourly_data = df[df['hr'].notna()].copy()
    hourly_df = hourly_data.groupby(by="hr").agg({
        "cnt": "mean",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    hourly_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return hourly_df

def create_workingday_df(df):
    """Membuat dataframe peminjaman berdasarkan hari kerja vs akhir pekan"""
    workingday_df = df.groupby(by="workingday_desc").agg({
        "cnt": "mean",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    workingday_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return workingday_df

def create_holiday_df(df):
    """Membuat dataframe peminjaman berdasarkan hari libur"""
    holiday_df = df.groupby(by="holiday_desc").agg({
        "cnt": "mean",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    holiday_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return holiday_df

def create_hourly_workingday_df(df):
    """Membuat dataframe peminjaman per jam berdasarkan tipe hari"""
    hourly_data = df[df['hr'].notna()].copy()
    hourly_workingday_df = hourly_data.groupby(by=["workingday_desc", "hr"]).agg({
        "cnt": "mean"
    }).reset_index()
    hourly_workingday_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)
    return hourly_workingday_df


# ==================== MEMUAT DATA ====================
# Load data gabungan yang sudah dibersihkan
BASE_DIR = Path(__file__).resolve().parent


def load_main_data():
    """Memuat data utama dari lokasi yang paling umum dipakai saat menjalankan app."""
    candidate_paths = [
        BASE_DIR / "main_data.csv",
        Path.cwd() / "main_data.csv",
        BASE_DIR.parent / "main_data.csv",
    ]

    for path in candidate_paths:
        if path.exists():
            return pd.read_csv(path)

    searched_paths = "\n".join(f"- {path}" for path in candidate_paths)
    raise FileNotFoundError(
        "Tidak menemukan file main_data.csv. Lokasi yang dicoba:\n"
        f"{searched_paths}"
    )


main_data = load_main_data()

# Pastikan kolom datetime
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

# Urutkan data berdasarkan tanggal
main_data.sort_values(by="dteday", inplace=True)
main_data.reset_index(drop=True, inplace=True)


# ==================== FILTER DATA ====================
min_date = main_data["dteday"].min()
max_date = main_data["dteday"].max()

with st.sidebar:
    # Menampilkan identitas dashboard dalam bentuk teks
    st.markdown("### Bike Sharing Dashboard")
    
    # Mengambil tanggal mulai dan tanggal akhir
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            label='Tanggal Mulai',
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
    with col2:
        end_date = st.date_input(
            label='Tanggal Akhir',
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

# Filter data berdasarkan rentang waktu yang dipilih
main_df = main_data[(main_data["dteday"] >= pd.Timestamp(start_date)) & 
                    (main_data["dteday"] <= pd.Timestamp(end_date))]


# ==================== MENYIAPKAN DATAFRAME ====================
daily_rentals_df = create_daily_rentals_df(main_df)
season_df = create_season_df(main_df)
weather_df = create_weather_df(main_df)
weekday_df = create_weekday_df(main_df)
hourly_df = create_hourly_df(main_df)
workingday_df = create_workingday_df(main_df)
holiday_df = create_holiday_df(main_df)
hourly_workingday_df = create_hourly_workingday_df(main_df)


# ==================== TAMPILAN DASHBOARD ====================

# Header utama
st.header('Dashboard Penyewaan Sepeda 🚲')
st.markdown('Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan waktu, musim, cuaca, dan tipe pengguna.')

# Penjelasan peminjaman sepeda
st.markdown("""
**Penjelasan Peminjaman Sepeda:**
- **Total Peminjaman (cnt)**: Jumlah total sepeda yang disewa
- **Pengguna Casual**: Pengguna tanpa keanggotaan (peminjaman sesekali)
- **Pengguna Registered**: Pengguna terdaftar/berlangganan (peminjaman rutin)
""")

# ==================== RINGKASAN PEMINJAMAN HARIAN ====================
st.subheader('Ringkasan Peminjaman Sepeda Keseluruhan')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rentals_df.total_rentals.sum()
    st.metric("Total Peminjaman", value=f"{total_rentals:,.0f}")

with col2:
    total_casual = daily_rentals_df.casual_rentals.sum()
    st.metric("Total Pengguna Casual", value=f"{total_casual:,.0f}")

with col3:
    total_registered = daily_rentals_df.registered_rentals.sum()
    st.metric("Total Pengguna Terdaftar", value=f"{total_registered:,.0f}")

# Grafik tren peminjaman harian
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_rentals"],
    marker='o',
    linewidth=3,
    color="#90CAF9",
    markersize=8
)
ax.set_title("Tren Peminjaman Sepeda Harian", fontsize=24, fontweight='bold')
ax.set_xlabel("Tanggal", fontsize=16)
ax.set_ylabel("Jumlah Peminjaman", fontsize=16)
ax.tick_params(axis='x', labelsize=14, rotation=45)
ax.tick_params(axis='y', labelsize=14)
ax.grid(True, alpha=0.3)
st.pyplot(fig)


# ==================== ANALISIS PERBEDAAN HARI LIBUR ====================
st.subheader(' Analisis Perbedaan Hari Libur (Holiday vs Non-Holiday)')

# Grafik rata-rata peminjaman berdasarkan status hari libur
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#4A90E2', '#357ABD']
bars = ax.bar(holiday_df['holiday_desc'], holiday_df['avg_rentals'], color=colors, edgecolor='white', linewidth=2)
ax.set_title('Perbandingan Peminjaman: Hari Libur vs Bukan Libur', fontsize=14, fontweight='bold')
ax.set_xlabel('Status Hari', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
ax.tick_params(axis='y', labelsize=11)

# Tambahkan nilai di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.grid(True, alpha=0.3, axis='y')
st.pyplot(fig)


# ==================== ANALISIS PERBEDAAN HARI KERJA ====================
st.subheader(' Analisis Perbedaan Hari Kerja (Working Day vs Weekend/Holiday)')

# Grafik rata-rata peminjaman berdasarkan tipe hari
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#4A90E2', '#357ABD']
bars = ax.bar(workingday_df['workingday_desc'], workingday_df['avg_rentals'], color=colors, edgecolor='white', linewidth=2)
ax.set_title('Perbandingan Peminjaman: Hari Kerja vs Akhir Pekan', fontsize=14, fontweight='bold')
ax.set_xlabel('Status Hari', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
ax.tick_params(axis='y', labelsize=11)

# Tambahkan nilai di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.grid(True, alpha=0.3, axis='y')
st.pyplot(fig)


# ==================== ANALISIS PERBEDAAN HARI DALAM SEMINGGU ====================
st.subheader(' Analisis Perbedaan Jumlah Peminjaman Sepeda per Hari')

# Grafik rata-rata peminjaman per hari dalam seminggu
fig, ax = plt.subplots(figsize=(12, 6))
colors_weekday = '#4A90E2'
bars = ax.bar(weekday_df['weekday_desc'], weekday_df['avg_rentals'], color=colors_weekday, edgecolor='white', linewidth=2)
ax.set_title('Rata-rata Jumlah Peminjaman Sepeda per Hari', fontsize=14, fontweight='bold')
ax.set_xlabel('Hari', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
ax.tick_params(axis='x', labelsize=11, rotation=45)
ax.tick_params(axis='y', labelsize=11)

# Tambahkan nilai di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
st.pyplot(fig)


# ==================== ANALISIS PEMINJAMAN PER MUSIM ====================
st.subheader(' Rata-rata Jumlah Peminjaman Sepeda per Musim')

fig, ax = plt.subplots(figsize=(12, 6))
colors = '#4A90E2'
bars = ax.bar(season_df['season_desc'], season_df['avg_rentals'], color=colors, edgecolor='white', linewidth=2)
ax.set_title('Rata-rata Jumlah Peminjaman Sepeda per Musim', fontsize=14, fontweight='bold')
ax.set_xlabel('Musim', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)

# Tambahkan nilai di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
st.pyplot(fig)


# ==================== ANALISIS PEMINJAMAN PER JAM ====================
st.subheader('Pola Rata-rata Peminjaman Sepeda per Jam dalam Sehari')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_df['hr'], hourly_df['avg_rentals'], marker='o', linewidth=2, markersize=6, color='#4A90E2')
ax.set_title('Pola Rata-rata Peminjaman Sepeda per Jam dalam Sehari', fontsize=14, fontweight='bold')
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
ax.set_xticks(range(0, 24))
ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig)


# ==================== ANALISIS PEMINJAMAN PER KONDISI CUACA ====================
st.subheader('Perbandingan Peminjaman Casual vs Registered per Kondisi Cuaca')

fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(weather_df))
width = 0.35

bars1 = ax.bar([i - width/2 for i in x], weather_df['casual'], width, label='Casual', color='#7ECEF4', edgecolor='white', linewidth=2)
bars2 = ax.bar([i + width/2 for i in x], weather_df['registered'], width, label='Registered', color='#FF7A5C', edgecolor='white', linewidth=2)

ax.set_title('Perbandingan Peminjaman Casual vs Registered per Kondisi Cuaca', fontsize=14, fontweight='bold')
ax.set_xlabel('Kondisi Cuaca', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(weather_df['weather_desc'], rotation=45, ha='right')
ax.tick_params(axis='y', labelsize=11)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

# Tambahkan nilai di atas bar
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
st.pyplot(fig)


