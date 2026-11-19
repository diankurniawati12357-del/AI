# BIOVA AI Model Training Documentation

Panduan pelatihan model klasifikasi gambar flora & fauna lingkungan Universitas Negeri Surabaya (UNESA).

## 1. Struktur Dataset

Siapkan foto-foto observasi atau dokumentasi lapangan pada direktori berikut:

```text
datasets/
├── hewan/
│   ├── Mamalia/
│   ├── Aves/
│   ├── Reptil/
│   ├── Amfibi/
│   ├── Pisces/
│   └── Invertebrata/
│
└── tumbuhan/
    ├── Dikotil/
    └── Monokotil/
```

- Format foto: JPG, JPEG, atau PNG.
- Disarankan minimal 50-100 foto berkualitas baik per kelas.
- Hindari dataset sintetik atau non-UNESA yang tidak terverifikasi.

## 2. Menjalankan Pelatihan (Training)

Jalankan perintah berikut dari root direktori `WEB UAS`:

```powershell
# Melatih model hewan (6 kelas)
python training/train_animals.py

# Melatih model tumbuhan (2 kelas: Dikotil & Monokotil)
python training/train_plants.py
```

Model akan otomatis diekspor ke:
- `models/model_hewan.keras` dan `models/labels/label_hewan.json`
- `models/model_tumbuhan.keras` dan `models/labels/label_tumbuhan.json`

## 3. Evaluasi Model

Untuk menguji akurasi, presisi, recall, F1-score, dan confusion matrix:

```powershell
python training/evaluate_model.py hewan
python training/evaluate_model.py tumbuhan
```
