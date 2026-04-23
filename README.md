# bike-sharing-dashboard

Proyek ini menganalisis pola peminjaman sepeda dari dataset bike-sharing, lalu menyajikannya dalam dashboard interaktif berbasis Streamlit

## Dashboard Online

https://bikesharing12.streamlit.app/

## Pertanyaan Bisnis

1. Bagaimana perbedaan rata-rata dan total jumlah peminjaman sepeda (cnt) antara hari libur (holiday), hari kerja (workingday), dan setiap hari dalam seminggu (weekday)?
2. Musim (season) mana yang memiliki rata-rata dan total jumlah peminjaman sepeda (cnt) tertinggi dibandingkan musim lainnya?
3. Pada jam (hr) berapa rata-rata jumlah peminjaman sepeda (cnt) mencapai nilai tertinggi dalam satu hari?
4. Bagaimana perbedaan rata-rata jumlah peminjaman sepeda antara pengguna casual dan registered pada setiap kondisi cuaca (weathersit)?

## Ringkasan Hasil Analisis

1. Hari kerja memiliki total peminjaman lebih tinggi daripada hari libur. Berdasarkan rata-rata harian, Kamis dan Jumat menjadi hari tersibuk, sedangkan Minggu terendah.
2. Musim Gugur (Fall) memiliki rata-rata dan total peminjaman tertinggi, diikuti Musim Panas. Musim Semi (Spring) menjadi yang terendah.
3. Puncak rata-rata peminjaman terjadi pada pukul 08.00 serta 17.00-18.00, menunjukkan pola penggunaan komuter (berangkat dan pulang kerja/sekolah).
4. Pengguna registered mendominasi jumlah peminjaman pada semua kondisi cuaca. Pengguna casual lebih sensitif terhadap cuaca buruk, dengan penurunan yang jauh lebih tajam saat hujan/salju.

## Struktur Proyek

- `Notebook.ipynb`: notebook utama untuk proses analisis end-to-end.
- `dashboard/dashboard.py`: aplikasi dashboard Streamlit.
- `dashboard/main_data.csv`: data utama yang digunakan dashboard.
- `data/day.csv` dan `data/hour.csv`: dataset sumber.

## Menjalankan Proyek di VS Code

1. Buka folder proyek di VS Code.
2. Buka terminal VS Code melalui menu **Terminal > New Terminal**.
3. Jalankan instalasi dependency:

```bash
pip install -r requirements.txt
```

4. Jalankan dashboard Streamlit dari root project:

```bash
cd dashboard
streamlit run dashboard.py
```

