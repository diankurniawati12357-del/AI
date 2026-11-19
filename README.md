# BIOVA — Belajar dari Alam
> **Jelajahi Sekitarmu! Temukan, Kenali, & Pelajari.**

Aplikasi web edukasi interaktif berbasis **Python Streamlit** dan **Artificial Intelligence (AI)** untuk pengenalan keanekaragaman hayati (hewan dan tumbuhan) di lingkungan kampus Universitas Negeri Surabaya (UNESA).

---

## 🌿 Fitur Utama

1. **Autentikasi Pengguna & Keamanan:**
   - Pendaftaran akun baru dan login aman menggunakan hashing PBKDF2-HMAC-SHA256.
   - Sesi interaktif menggunakan Streamlit Session State & basis data SQLite.
2. **AI Image Classification (Flora & Fauna):**
   - Identifikasi kelompok hewan (Mamalia, Aves, Reptil, Amfibi, Pisces, Invertebrata).
   - Identifikasi kelompok tumbuhan (Dikotil & Monokotil).
   - Validasi file (JPG/PNG, ukuran maks 10MB, integritas gambar).
   - Penanganan status transparan ketika model belum tersedia atau tingkat keyakinan rendah.
3. **Interactive 3D Model Visualization:**
   - Penampil model 3D interaktif (.glb/.gltf) menggunakan `<model-viewer>` yang mendukung rotasi 360°, pembesaran (zoom), dan pemutaran animasi gerakan satwa.
4. **Materi Pembelajaran Terstruktur:**
   - 3 Bab untuk Hewan dan 3 Bab untuk Tumbuhan, masing-masing berisi 5 kartu edukasi dengan fakta biologis terverifikasi (tanpa teks palsu/Lorem Ipsum).
5. **Kuis Interaktif & Gamifikasi:**
   - 5 soal pilihan ganda interaktif per bab dengan sistem penilaian langsung dan kotak pembahasan mendalam.
   - Sistem perolehan bintang (+1 per soal baru, bonus +3 untuk nilai sempurna 5/5).
   - Sistem Tier Pengguna: Bronze, Silver (≥20 ⭐), Gold (≥60 ⭐), dan Platinum (≥100 ⭐ & ≥20 unggahan valid).
   - Papan Peringkat (Leaderboard) berbasis data riil SQLite.
6. **Pembuatan Panorama (Image Stitching):**
   - Penggabungan beberapa foto bersambung menjadi satu foto panorama lebar menggunakan algoritma `cv2.Stitcher` dari OpenCV.

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa & Framework Utama:** Python 3.11+, Streamlit
- **Machine Learning & Visi Komputer:** TensorFlow / Keras, OpenCV, Pillow, NumPy
- **Visualisasi 3D:** Google `<model-viewer>` (GLB/glTF dengan kontrol rotasi, zoom, dan animasi)
- **Basis Data:** SQLite3
- **Pengujian:** Python `unittest` & `pytest`

---

## 📁 Struktur Direktori

```text
WEB UAS/
├── app.py                      # Entry point & controller routing utama
├── requirements.txt            # Daftar dependensi aplikasi
├── README.md                   # Dokumentasi teknis lengkap
├── .gitignore                  # Berkas pengabaian Git
│
├── .streamlit/
│   └── config.toml             # Konfigurasi tema & server Streamlit
│
├── views/                      # Modul antarmuka halaman
│   ├── welcome.py              # Layar sambutan (Welcome)
│   ├── auth.py                 # Layar Masuk (Login) & Daftar (Register)
│   ├── dashboard.py            # Beranda utama (Dashboard)
│   ├── scan.py                 # Unggah & pemindaian AI
│   ├── scan_result.py          # Hasil klasifikasi (sukses & gagal)
│   ├── learn.py                # Menu pemilihan belajar & kuis
│   ├── lesson.py               # Kartu materi pembelajaran
│   ├── quiz.py                 # Kuis pilihan ganda & pembahasan
│   ├── quiz_result.py          # Hasil nilai kuis & peringkat
│   ├── leaderboard.py          # Papan peringkat pengguna
│   ├── profile.py              # Profil akun & statistik tier
│   └── panorama.py             # Fitur stitching foto panorama
│
├── components/                 # Komponen antarmuka modular
│   ├── theme.py                # Injeksi CSS & styling sistem desain
│   ├── header.py               # Bar atas dengan avatar & bintang
│   ├── navigation.py           # Routing & navigasi bawah (navbar)
│   ├── cards.py                # Kartu kategori & banner panorama
│   ├── mascot.py               # Render maskot katak ramah BIOVA
│   └── three_d_viewer.py       # Penampil model 3D interaktif GLB
│
├── services/                   # Layer logika bisnis & layanan data
│   ├── config.py               # Konfigurasi jalur berkas & palet warna
│   ├── db.py                   # Inisialisasi basis data SQLite
│   ├── auth_service.py         # Layanan otentikasi & hash sandi
│   ├── model_service.py        # Pengelola model Keras & inferensi
│   ├── edukasi_service.py      # Katalog taksonomi & deskripsi ilmiah
│   ├── materi_service.py       # Pemuat data kartu materi
│   ├── quiz_service.py         # Mesin penilaian kuis & kunci jawaban
│   ├── game_service.py         # Perhitungan bintang, tier, & unlock bab
│   ├── leaderboard_service.py  # Query urutan peringkat pemain
│   ├── model3d_service.py      # Pemetaan spesies ke aset berkas 3D
│   ├── upload_service.py       # Validasi integritas gambar & hash
│   └── stitching_service.py    # Algoritma OpenCV Image Stitcher
│
├── models/                     # Tempat model AI (.keras) & label (.json)
│   └── labels/
│       ├── label_hewan.json
│       └── label_tumbuhan.json
│
├── training/                   # Skrip pelatihan AI
│   ├── train_animals.py        # Pelatihan model hewan 6 kelas
│   ├── train_plants.py         # Pelatihan model tumbuhan 2 kelas
│   ├── evaluate_model.py       # Evaluasi metrik & confusion matrix
│   └── README.md
│
├── datasets/                   # Direktori penampung foto dataset pelatihan
│   ├── hewan/
│   └── tumbuhan/
│
├── assets/                     # Berkas statis
│   ├── mascot/                 # Aset maskot katak BIOVA
│   ├── icons/                  # Ikon aplikasi
│   ├── images/                 # Gambar materi
│   └── 3d/                     # Model 3D (.glb)
│       ├── hewan/
│       └── tumbuhan/
│
├── content/                    # Data konten edukasi (JSON)
│   ├── spesies.json
│   ├── materi_hewan.json
│   ├── materi_tumbuhan.json
│   ├── kuis_hewan.json
│   └── kuis_tumbuhan.json
│
├── data/                       # Basis data lokal (biova.db)
├── references/ui/              # 17 gambar referensi desain antarmuka
└── tests/                      # Suite pengujian otomatis (20 unit tests)
    ├── test_auth.py
    ├── test_classification.py
    ├── test_quiz.py
    ├── test_gamification.py
    └── test_stitching.py
```

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Prasyarat Lingkungan
Pastikan Python 3.11 atau 3.12 telah terpasang di sistem operasi Windows Anda.

### 2. Mengaktifkan Virtual Environment
Jika menggunakan virtual environment yang telah disiapkan di workspace:

```powershell
# Mengaktifkan environment
..\PROGRAM\bab5\.venv\Scripts\Activate.ps1
```

### 3. Menjalankan Streamlit
Dari dalam folder `WEB UAS`, jalankan perintah:

```powershell
python -m streamlit run app.py
```
atau secara langsung:
```powershell
& "..\PROGRAM\bab5\.venv\Scripts\python.exe" -m streamlit run app.py
```

Buka peramban (browser) di alamat:
`http://localhost:8501`

---

## 🧪 Menjalankan Pengujian (Testing)

Semua fungsionalitas modul inti (otentikasi, klasifikasi aman, kuis, gamifikasi bintang, dan image stitching) telah diuji secara komprehensif.

Jalankan test suite dengan perintah:

```powershell
python -m unittest discover tests
```

Hasil:
```text
Ran 20 tests in 2.046s
OK
```

---

## 🤖 Menambahkan Model AI & Model 3D

1. **Model AI (.keras):**
   - Tempatkan model hewan di `models/model_hewan.keras`.
   - Tempatkan model tumbuhan di `models/model_tumbuhan.keras`.
   - Label kelas dikonfigurasi melalui `models/labels/label_hewan.json` dan `models/labels/label_tumbuhan.json`.
   - Jika model belum diletakkan, sistem akan menampilkan status transparan tanpa menghasilkan prediksi palsu.

2. **Model 3D (.glb):**
   - Letakkan berkas model 3D berformat `.glb` pada direktori `assets/3d/hewan/` atau `assets/3d/tumbuhan/` (misalnya `cat.glb`, `bird.glb`, `frog.glb`, `tree.glb`).
   - Apabila berkas 3D belum tersedia, aplikasi akan secara elegan menampilkan fallback informasi bahwa visualisasi 3D belum tersedia untuk objek tersebut.
