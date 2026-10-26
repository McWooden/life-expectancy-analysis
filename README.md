# Analisis Angka Harapan Hidup Global & Faktor Sosio-Ekonomi (2023)

Proyek analisis data deskriptif lintas negara untuk mengeksplorasi hubungan antara **Angka Harapan Hidup (*Life Expectancy*)** dengan indikator sosio-ekonomi utama: **GDP Per Kapita**, **Pengeluaran Kesehatan (*Healthcare Expenditure*)**, dan **Tingkat Melek Huruf Dewasa (*Adult Literacy Rate*)** pada **50 negara** di lima benua.

---

## 📌 Ringkasan Proyek & Ruang Lingkup

Proyek ini disusun untuk memenuhi seluruh kebutuhan analisis data deskriptif:
1. **Topik Terpilih**: *"Global Life Expectancy and Socioeconomic Factors (2023 Estimates)"* — topik objektif, mudah dipahami, tidak ambigu, dan berbasis data resmi internasional.
2. **Sumber Data Resmi**:
   - **World Bank Open Data** ([data.worldbank.org](https://data.worldbank.org)): GDP per kapita (USD), populasi (juta), dan tingkat melek huruf dewasa (%).
   - **World Health Organization (WHO) Global Health Observatory** ([who.int/data/gho](https://www.who.int/data/gho)): Angka harapan hidup saat lahir (tahun) dan belanja kesehatan (% dari GDP).
3. **Bahasa Laporan & Kode**: Laporan teknis (PDF) dan skrip R ditulis dalam Bahasa Inggris sesuai kebutuhan akademis/klien, dengan dokumentasi repositori (`README.md`) ini disajikan lengkap dalam Bahasa Indonesia.
4. **Hasil Akhir (Deliverables)**:
   - File dataset format **CSV** dan **Excel (.xlsx)**.
   - Skrip **R (`analysis.R`)** mandiri yang dapat langsung dijalankan ulang di RStudio.
   - Dokumen **R Markdown (`report.Rmd`)** untuk kompilasi (*knit*) laporan.
   - Laporan akhir **PDF 3 halaman (`report.pdf`)** berformat standar publikasi ilmiah.
   - 6 grafik visualisasi beresolusi tinggi (300 DPI) di dalam folder `output/`.

---

## 📂 Struktur Repositori

```text
life-expectancy-analysis/
├── README.md                      # Dokumentasi teknis proyek (Bahasa Indonesia)
├── report.pdf                     # Laporan akhir PDF 3 halaman (Bahasa Inggris)
├── report.Rmd                     # Source file R Markdown untuk RStudio
├── report.html                    # Versi HTML laporan
├── analysis.R                     # Skrip R analisis deskriptif & visualisasi
├── data/
│   ├── life_expectancy_data.csv   # Dataset dalam format CSV
│   └── life_expectancy_data.xlsx  # Dataset dalam format Microsoft Excel
├── output/
│   ├── 01_histogram_life_expectancy.png        # Histogram distribusi harapan hidup
│   ├── 02_boxplot_life_expectancy_by_region.png # Boxplot persebaran per kawasan
│   ├── 03_scatter_life_exp_vs_gdp.png          # Scatter plot vs GDP (Preston curve)
│   ├── 04_bar_avg_life_exp_by_region.png       # Bar chart rata-rata per benua
│   ├── 05_scatter_life_exp_vs_healthcare.png   # Scatter plot vs Belanja Kesehatan
│   └── 06_scatter_life_exp_vs_literacy.png     # Scatter plot vs Tingkat Melek Huruf
└── scripts/                       # Skrip pendukung pengujian dan kompilasi
```

---

## 📊 Variabel Dataset

Dataset terdiri atas **50 baris** observasi negara tanpa nilai kosong (*zero missing values / NA*):

| Nama Variabel | Tipe Data | Deskripsi | Satuan |
|---|---|---|---|
| `Country` | Karakter | Nama negara (50 negara lintas kawasan) | Teks |
| `Region` | Faktor / Kategori | Benua (Africa, Americas, Asia, Europe, Oceania) | Kategori |
| `Life_Expectancy` | Numerik | Angka harapan hidup saat lahir | Tahun |
| `GDP_Per_Capita` | Numerik | Produk Domestik Bruto (PDB) per kapita | USD ($) |
| `Healthcare_Expenditure_Pct` | Numerik | Belanja kesehatan nasional | % dari PDB |
| `Population_Millions` | Numerik | Total populasi penduduk | Juta jiwa |
| `Adult_Literacy_Rate` | Numerik | Tingkat melek huruf usia 15 tahun ke atas | % |

---

## 📈 Temuan Utama Analisis Statistik Deskriptif

### 1. Ukuran Pemusatan & Penyebaran Global
- **Rata-rata Harapan Hidup Global**: **74.88 tahun** (Standar Deviasi: **7.58 tahun**).
- **Median**: **76.60 tahun**, dengan rentang nilai dari **54.30 tahun** (Nigeria) hingga **84.80 tahun** (Jepang).
- Distribusi bersifat *left-skewed* (condong ke kiri) karena mayoritas negara maju/berkembang menengah terkonsentrasi di atas 75 tahun, sementara sejumlah negara di Afrika berada pada ekor bawah (54–66 tahun).

### 2. Disparitas Kawasan (Regional)
- **Oceania**: Rata-rata 82.7 tahun (PDB: $56,370)
- **Eropa**: Rata-rata 80.6 tahun (PDB: $47,381)
- **Amerika**: Rata-rata 77.5 tahun (PDB: $20,691)
- **Asia**: Rata-rata 75.9 tahun (PDB: $12,298)
- **Afrika**: Rata-rata 64.4 tahun (PDB: $2,266)
- Terdapat kesenjangan harapan hidup hingga **18.3 tahun** antara kawasan Oceania/Eropa dan Afrika.

### 3. Analisis Korelasi Bivariat
- **Harapan Hidup vs. Melek Huruf Dewasa**: $r = +0.785$ (Korelasi positif kuat). Pendidikan dasar berkaitan sangat erat dengan pemahaman kesehatan dan higienitas.
- **Harapan Hidup vs. PDB Per Kapita**: $r = +0.694$ (Korelasi positif moderat-kuat non-linear). Mengikuti pola kurva *Preston*: peningkatan pendapatan meningkatkan harapan hidup secara signifikan pada negara miskin/berkembang, namun mencapai titik jenuh (*plateau*) di negara maju.
- **Harapan Hidup vs. Belanja Kesehatan**: $r = +0.661$ (Korelasi positif moderat).

> **Catatan Metodologi**: Analisis ini bersifat **deskriptif observasional**. Korelasi yang ditemukan tidak digunakan untuk mengklaim hubungan sebab-akibat (*causation*) tanpa analisis ekonometrik terkontrol lebih lanjut.

---

## 🚀 Panduan Menjalankan Kode di RStudio

### 1. Prasyarat Paket R
Pastikan pustaka CRAN berikut telah terpasang:
```r
install.packages(c("readr", "writexl", "ggplot2", "dplyr", "tidyr", 
                   "scales", "gridExtra", "knitr", "rmarkdown"))
```

### 2. Menjalankan Skrip Analisis (`analysis.R`)
1. Buka RStudio.
2. Atur direktori kerja ke folder repositori:
   ```r
   setwd("/mnt/alterra/repo/life-expectancy-analysis")
   ```
3. Buka file `analysis.R` dan klik tombol **Source** (atau tekan `Ctrl + Shift + S`).
4. Skrip secara otomatis:
   - Membaca file data CSV.
   - Mengekspor salinan data Excel `.xlsx`.
   - Menghitung dan mencetak seluruh ringkasan deskriptif di console R.
   - Membuat dan menyimpan 6 grafik visualisasi ke folder `output/`.

### 3. Mengompilasi Laporan R Markdown (`report.Rmd`)
1. Buka file `report.Rmd` di RStudio.
2. Klik menu **Knit** -> **Knit to PDF** (memerlukan distribusi LaTeX seperti TinyTeX: `tinytex::install_tinytex()`).
3. File laporan PDF siap pakai yang telah terkompilasi juga sudah tersedia langsung di [`report.pdf`](report.pdf).

---

## 📄 Berkas Hasil Akhir (Deliverables)

| Berkas | Deskripsi |
|---|---|
| [`report.pdf`](report.pdf) | Laporan teknis 3 halaman berformat publikasi (Bahasa Inggris) |
| [`analysis.R`](analysis.R) | Skrip R lengkap untuk replikasi analisis di RStudio |
| [`data/life_expectancy_data.xlsx`](data/life_expectancy_data.xlsx) | Dataset olahan format Microsoft Excel |
| [`data/life_expectancy_data.csv`](data/life_expectancy_data.csv) | Dataset mentah terstruktur format CSV |
| [`output/`](output/) | Kumpulan 6 berkas gambar grafik beresolusi tinggi (PNG) |
