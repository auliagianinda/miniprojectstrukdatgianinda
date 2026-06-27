# 🧬 Automatic Exon-Intron Splicer & Bioinformatics Pipeline Dashboard

[![Python Version](https://img.shields.io/badge/python-3.13+-ff69b4.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-blueviolet.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Sebuah aplikasi *pipeline* bioinformatika berbasis web (Flask) yang dirancang untuk melakukan prapemrosesan, pemotongan otomatis (*auto-splicing*), serta analisis komparasi struktur internal gen eukariotik (**Ekson vs Intron**). Aplikasi ini menerima satu berkas *gelondongan* berformat GenBank (`.gb`/`.gbk`) langsung dari NCBI, lalu secara mandiri mengisolasi dan membedakan profil stabilitas *GC-content* serta frekuensi nukleotida menggunakan pemrograman struktur data dasar (*List* dan *Dictionary*) tanpa pustaka komputasi berat pihak ketiga.

---

## 🔮 Fitur Utama

- **Auto-Splicing Engine:** Membaca instruksi peta koordinat fisik pada baris `FEATURES` GenBank dan memotong sekuens utama (`ORIGIN`) menjadi fragmen ekson dan intron secara mandiri melalui teknik *string slicing*.
- **Kalkulator Matriks Nukleotida:** Menghitung frekuensi kemunculan basa Nitrogen (A, T, G, C) secara akurat menggunakan struktur data *Dictionary*.
- **Analisis Komparasi Kontras (Top 3 Juara):** Algoritma filter otomatis yang mengisolasi nilai ekstrem biologis, menampilkan 2 ekson dengan *GC-content* tertinggi dan 1 intron dengan *GC-content* terendah untuk perbandingan termal untai.
- **Visualisasi Dinamis Matplotlib:** Menghasilkan grafik distribusi diagram batang dua warna secara otomatis (**Biru Pastel** untuk Ekson, **Pink Pastel** untuk Intron).
- **Ekspor Laporan Biomedis:** Menyediakan fitur unduhan instan data olahan mentah ke dalam format `.csv` untuk keperluan pengarsipan data laboratorium.
- **Antarmuka Estetis:** Desain dasbor responsif menggunakan Bootstrap 5 dengan palet warna kustom bertema *Soft Pink, Pastel Blue, dan Slate Purple*.

---

## 📐 Alur Kerja Sistem (Bioinformatics Pipeline)

Aplikasi ini bekerja melalui arsitektur komputasi sekuensial terintegrasi sebagai berikut:

1. **Upload & Parse:** Pengguna mengunggah berkas GenBank gelondongan dari NCBI. Sistem mengekstrak batasan koordinat fitur dan membersihkan untai DNA utama.
2. **Slicing & Analisis:** Untai dipotong otomatis berdasarkan koordinat fungsional, kemudian dihitung persentase rumus kimiawi *GC-content*:
   $$\text{GC Content (\%)} = \frac{\text{Jumlah G} + \text{Jumlah C}}{\text{Total Panjang Fragmen}} \times 100$$
3. **Penyaringan & Rendering:** Data diurutkan secara menurun (*descending*), diekstrak sampel kontrasnya, dirender menjadi grafik, dan disajikan langsung ke dasbor web.

---

## 🛠️ Panduan Instalasi Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek ini di komputer lokal Anda:

### 1. Kloning Repositori
```bash
git clone [https://github.com/username-kamu/nama-repositori-kamu.git](https://github.com/username-kamu/nama-repositori-kamu.git)
cd nama-repositori-kamu

```

### 2. Membuat dan Mengaktifkan Virtual Environment (Ekosistem Terisolasi)

**Pada Windows (PowerShell):**
Jika eksekusi script diblokir oleh sistem, jalankan bypass kebijakan terlebih dahulu:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1

```

**Pada Windows (Command Prompt / CMD):**

```cmd
.\venv\Scripts\activate.bat

```

**Pada Linux / macOS:**

```bash
source venv/bin/activate

```

### 3. Instalasi Dependensi / Library

Pastikan Anda berada di lingkungan virtual `(venv)`, lalu instal kerangka kerja web dan pustaka visualisasi:

```bash
pip install Flask matplotlib

```

### 4. Menjalankan Aplikasi

Eksekusi server lokal Flask menggunakan perintah:

```bash
python app.py

```

Setelah server menyala, buka penjelajah web (*browser*) Anda dan akses alamat:
`http://127.0.0.1:5000`

---

## 📊 Contoh Data Uji (Studi Kasus Gen HBB)

Proyek ini telah divalidasi menggunakan sekuens gen *Homo sapiens* subunit hemoglobin beta (**HBB**) dengan kode akses **AH001475.2** dari NCBI Nucleotide. Hasil komputasi otomatis menunjukkan fenomena biologi molekuler yang nyata:

| Nama Fragmen Potongan | Panjang Basa (bp) | GC-Content (%) | Fungsi Biologis |
| --- | --- | --- | --- |
| `HBB_exon_1_(Auto_Cut)` | 92 bp | **59.78%** | Wilayah Pengode (Stabilitas Tinggi) |
| `HBB_exon_3_(Auto_Cut)` | 109 bp | **57.80%** | Wilayah Pengode (Stabilitas Tinggi) |
| `HBB_exon_4_(Auto_Cut)` | 104 bp | **55.77%** | Wilayah Pengode (Stabilitas Tinggi) |
| `HBB_intron_1_(Auto_Cut)` | 130 bp | **45.38%** | Wilayah Non-Pengode (Kaya A-T) |
| `HBB_intron_3_(Auto_Cut)` | 688 bp | **41.13%** | Wilayah Non-Pengode (Kaya A-T) |

*Kesimpulan Biologis:* Wilayah Ekson memiliki nilai *GC-content* yang dominan tinggi karena tuntutan tekanan seleksi evolusioner (*evolutionary selective pressure*) untuk mempertahankan akurasi translasi protein melalui stabilitas tiga ikatan hidrogen basa G-C. Sebaliknya, wilayah Intron bebas berakumulasi dengan mutasi kaya basa A-T (ikatan hidrogen ganda) karena akan dibuang pada proses *splicing*.

---

## 📂 Struktur Direktori Proyek

```text
mini_project_bif/
│
├── static/               # Menyimpan file output grafik .png dan laporan .csv otomatis
│   ├── gc_chart.png
│   └── hasil_analisis.csv
│
├── templates/            # Komponen tampilan Frontend (UI/UX)
│   └── index.html
│
├── app.py                # Kontroler Server Utama Flask & Logika Pipeline
├── bioinformatics.py     # Kelas Utama Parser dan Analyzer (List & Dictionary)
└── README.md             # Dokumentasi Proyek GitHub

```
