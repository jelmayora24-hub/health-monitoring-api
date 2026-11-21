# Aplikasi Monitoring Kesehatan - Setup & Running Guide

## 🚀 Cara Menjalankan Aplikasi

### Langkah 1: Masuk ke Folder Project
```bash
cd proyek-kesehatan
```

### Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Jika menggunakan virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# atau
source venv/bin/activate        # Linux/Mac

pip install -r requirements.txt
```

### Langkah 3: Jalankan Server
```bash
python main.py
```

Atau dengan Uvicorn secara langsung:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Output yang diharapkan:
```
============================================================
🏥 APLIKASI MONITORING KESEHATAN
============================================================
✓ Database diinisialisasi
✓ API siap melayani request
✓ WebSocket siap untuk monitoring real-time
============================================================

🚀 Memulai server...
📍 URL: http://localhost:8000
📚 Dokumentasi: http://localhost:8000/docs
```

### Langkah 4: Akses Aplikasi

- **API Dokumentasi**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testing Aplikasi

### Test 1: Dengan cURL (Command Line)
```bash
# Test health
curl http://localhost:8000/health

# Buat pasien
curl -X POST http://localhost:8000/api/pasien \
  -H "Content-Type: application/json" \
  -d "{\"nama\": \"Budi\", \"usia\": 45, \"detak_jantung\": 75, \"tekanan_darah_sistol\": 120, \"tekanan_darah_diastol\": 80, \"lokasi\": {\"latitude\": -6.2088, \"longitude\": 106.8456}}"
```

### Test 2: Dengan Python Script
```bash
# Pastikan install requests
pip install requests

# Jalankan test
python test_api.py
```

### Test 3: Dengan WebSocket
```bash
# Pastikan install websockets
pip install websockets

# Jalankan WebSocket client (buat pasien dulu)
python websocket_client.py
```

### Test 4: Dengan Postman
1. Buka Postman
2. Import dari Swagger UI: http://localhost:8000/openapi.json
3. Atau manual create request

## 📚 Contoh Request

### 1. Buat Pasien
```bash
curl -X POST http://localhost:8000/api/pasien \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Budi Santoso",
    "usia": 45,
    "detak_jantung": 75,
    "tekanan_darah_sistol": 120,
    "tekanan_darah_diastol": 80,
    "lokasi": {
      "latitude": -6.2088,
      "longitude": 106.8456
    }
  }'
```

### 2. Ambil Daftar Pasien
```bash
curl http://localhost:8000/api/pasien
```

### 3. Ambil Detail Pasien
```bash
curl http://localhost:8000/api/pasien/1
```

### 4. Update Monitoring
```bash
curl -X POST http://localhost:8000/api/monitor/1/update \
  -H "Content-Type: application/json" \
  -d '{
    "detak_jantung": 88,
    "tekanan_darah_sistol": 125,
    "tekanan_darah_diastol": 82,
    "lokasi": {
      "latitude": -6.2088,
      "longitude": 106.8456
    }
  }'
```

### 5. Ambil Riwayat
```bash
curl http://localhost:8000/api/monitor/1/riwayat
```

### 6. Ambil Alarm
```bash
curl http://localhost:8000/api/alarm
```

### 7. Ambil Alarm Pasien
```bash
curl http://localhost:8000/api/alarm/pasien/1
```

### 8. Statistik Alarm
```bash
curl http://localhost:8000/api/alarm/statistik
```

## 🎯 Alur Penggunaan

1. **Registrasi Pasien**: POST /api/pasien
   - Input: nama, usia, detak jantung awal, tekanan darah, lokasi

2. **Monitoring Real-time**: POST /api/monitor/{id}/update atau WebSocket
   - Kirim: detak jantung terbaru, tekanan darah, lokasi

3. **Cek Alarm**: GET /api/alarm/pasien/{id}
   - Lihat riwayat alarm untuk pasien

4. **Statistik**: GET /api/alarm/statistik
   - Dashboard monitoring keseluruhan

## 🔍 Troubleshooting

### Error: "Port 8000 already in use"
```bash
# Gunakan port lain
uvicorn main:app --port 8001
```

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Install dependencies
pip install -r requirements.txt
```

### Database Error
```bash
# Hapus database lama
rm monitoring_kesehatan.db
# Jalankan lagi, database akan dibuat otomatis
python main.py
```

### WebSocket Connection Failed
- Pastikan server sedang berjalan
- Cek URL WebSocket: ws://localhost:8000
- Pastikan client terhubung sebelum kirim data

## 📝 Fitur yang Tersedia

✅ Manajemen Pasien (CRUD)
✅ Monitoring Real-time (HTTP + WebSocket)
✅ Sistem Alarm Otomatis
✅ Riwayat Monitoring
✅ Tracking Lokasi
✅ Statistik Alarm
✅ CORS Support
✅ Dokumentasi Otomatis
✅ Health Check

## 🛠️ Struktur File

```
proyek-kesehatan/
├── main.py                    # Entry point aplikasi
├── models.py                  # Pydantic models
├── database.py                # Database functions
├── routes/
│   ├── pasien.py             # Patient management endpoints
│   ├── monitor.py            # Monitoring & WebSocket
│   └── alarm.py              # Alarm endpoints
├── test_api.py               # API testing script
├── websocket_client.py        # WebSocket client
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # Documentation
└── SETUP.md                   # This file
```

## 📞 Tips & Tricks

### Disable Database Auto-commit
Di database.py, gunakan context manager untuk better control

### Menambah Validasi Custom
Edit models.py dan tambahkan validators dari Pydantic

### Extend Endpoints
Tambah file baru di `routes/` folder dan include di main.py

### Production Deployment
Gunakan Gunicorn:
```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

**Last Updated**: 2024
**Version**: 1.0.0
