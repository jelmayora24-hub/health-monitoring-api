# 🏥 Aplikasi Monitoring Kesehatan

Aplikasi monitoring kesehatan real-time menggunakan FastAPI dengan fitur WebSocket untuk monitoring detak jantung pasien secara real-time.

## 📋 Daftar Fitur

✅ **Registrasi dan Manajemen Pasien**
- Buat, baca, update, dan hapus data pasien
- Menyimpan informasi: nama, usia, detak jantung, tekanan darah, lokasi

✅ **Monitoring Real-time**
- WebSocket untuk update data real-time
- Riwayat monitoring per pasien
- Endpoint HTTP untuk update manual

✅ **Sistem Alarm Otomatis**
- Alarm untuk detak jantung kritis (< 50 atau > 100 bpm)
- Alarm waspada untuk detak 50-59 bpm
- Menyimpan lokasi dan timestamp saat alarm
- Daftar alarm dengan filter waktu

✅ **Tracking Lokasi**
- Menyimpan latitude dan longitude pasien
- Update lokasi real-time melalui WebSocket

✅ **Notifikasi Darurat**
- Statistik alarm
- Alert untuk kondisi kritis
- Riwayat lengkap untuk audit

✅ **CORS Middleware**
- Akses dari aplikasi mobile/web

✅ **Health Check**
- Endpoint `/health` untuk cek server

## 🚀 Quick Start

### 1. Instalasi Dependencies

```bash
cd proyek-kesehatan
pip install -r requirements.txt
```

### 2. Jalankan Server

```bash
python main.py
```

atau dengan Uvicorn:

```bash
uvicorn main:app --reload
```

Server akan berjalan di `http://localhost:8000`

### 3. Akses Dokumentasi

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Manajemen Pasien (`/api/pasien`)

#### Buat Pasien Baru
```bash
POST /api/pasien
Content-Type: application/json

{
  "nama": "Budi Santoso",
  "usia": 45,
  "detak_jantung": 75,
  "tekanan_darah_sistol": 120,
  "tekanan_darah_diastol": 80,
  "lokasi": {
    "latitude": -6.2088,
    "longitude": 106.8456
  }
}
```

#### Ambil Daftar Pasien
```bash
GET /api/pasien
```

#### Ambil Detail Pasien
```bash
GET /api/pasien/{pasien_id}
```

#### Update Pasien
```bash
PUT /api/pasien/{pasien_id}
```

#### Hapus Pasien
```bash
DELETE /api/pasien/{pasien_id}
```

### Monitoring Real-time (`/api/monitor`)

#### Update Monitoring
```bash
POST /api/monitor/{pasien_id}/update
Content-Type: application/json

{
  "detak_jantung": 85,
  "tekanan_darah_sistol": 125,
  "tekanan_darah_diastol": 82,
  "lokasi": {
    "latitude": -6.2088,
    "longitude": 106.8456
  }
}
```

#### Ambil Riwayat Monitoring
```bash
GET /api/monitor/{pasien_id}/riwayat?limit=100
```

#### WebSocket Real-time
```javascript
// Client JavaScript
const ws = new WebSocket('ws://localhost:8000/api/monitor/ws/1');

ws.onopen = (event) => {
  // Kirim data monitoring
  const data = {
    detak_jantung: 88,
    tekanan_darah_sistol: 120,
    tekanan_darah_diastol: 80,
    lokasi: {
      latitude: -6.2088,
      longitude: 106.8456
    }
  };
  ws.send(JSON.stringify(data));
};

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log('Status:', response.status);
  console.log('Pesan:', response.pesan);
  console.log('Alarm:', response.alarm);
};

ws.onerror = (event) => {
  console.error('WebSocket error:', event);
};
```

### Sistem Alarm (`/api/alarm`)

#### Ambil Semua Alarm
```bash
GET /api/alarm
```

#### Ambil Alarm Pasien
```bash
GET /api/alarm/pasien/{pasien_id}?jam_terakhir=24
```

#### Ambil Alarm Kritis
```bash
GET /api/alarm/kritis
```

#### Statistik Alarm
```bash
GET /api/alarm/statistik
```

#### Hapus Alarm
```bash
DELETE /api/alarm/{alarm_id}
```

#### Hapus Semua Alarm Pasien
```bash
DELETE /api/alarm/pasien/{pasien_id}/all
```

### System Health

#### Health Check
```bash
GET /health
```

#### Info Aplikasi
```bash
GET /api/info
```

## 📊 Status Kesehatan

| Status | Detak Jantung | Keterangan |
|--------|---------------|-----------|
| NORMAL | 60-100 bpm | Kondisi sehat |
| WASPADA | 50-59 bpm | Detak rendah, perlu perhatian |
| BAHAYA | < 50 bpm | KRITIS RENDAH - Darurat! |
| BAHAYA | > 100 bpm | KRITIS TINGGI - Darurat! |

## 📁 Struktur Project

```
proyek-kesehatan/
├── main.py                      # File utama FastAPI
├── models.py                    # Schema Pydantic
├── database.py                  # Koneksi SQLite & helper
├── routes/
│   ├── __init__.py
│   ├── pasien.py               # Endpoint manajemen pasien
│   ├── monitor.py              # Endpoint monitoring & WebSocket
│   └── alarm.py                # Endpoint sistem alarm
├── requirements.txt             # Dependencies
├── monitoring_kesehatan.db      # Database SQLite (auto-created)
└── README.md                    # Dokumentasi ini
```

## 🔐 Response Format

Semua response API dalam format JSON:

```json
{
  "status": "NORMAL",
  "pesan": "Data berhasil diproses",
  "data": {
    "id": 1,
    "nama": "Budi Santoso"
  },
  "timestamp": "2024-01-15T10:30:45.123456",
  "alarm": false
}
```

## 🛠️ Teknologi

- **FastAPI** - Web framework modern Python
- **Uvicorn** - ASGI server
- **Pydantic** - Validasi data
- **SQLite** - Database lokal
- **WebSocket** - Real-time communication
- **Python DateTime** - Timestamp

## 📱 Integrasi dengan Aplikasi Mobile

Aplikasi ini sudah dilengkapi CORS middleware, sehingga bisa diakses dari:
- Aplikasi mobile React Native
- Aplikasi web JavaScript
- Aplikasi desktop

Contoh fetch dari JavaScript:

```javascript
// Buat pasien baru
fetch('http://localhost:8000/api/pasien', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nama: 'Budi Santoso',
    usia: 45,
    detak_jantung: 75,
    tekanan_darah_sistol: 120,
    tekanan_darah_diastol: 80,
    lokasi: {
      latitude: -6.2088,
      longitude: 106.8456
    }
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## 🧪 Testing dengan cURL

### 1. Cek Server
```bash
curl http://localhost:8000/health
```

### 2. Buat Pasien
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

### 3. Ambil Daftar Pasien
```bash
curl http://localhost:8000/api/pasien
```

### 4. Update Monitoring
```bash
curl -X POST http://localhost:8000/api/monitor/1/update \
  -H "Content-Type: application/json" \
  -d '{
    "detak_jantung": 45,
    "tekanan_darah_sistol": 110,
    "tekanan_darah_diastol": 70,
    "lokasi": {
      "latitude": -6.2088,
      "longitude": 106.8456
    }
  }'
```

### 5. Ambil Alarm Kritis
```bash
curl http://localhost:8000/api/alarm/kritis
```

## 📝 Aturan Bisnis

- Detak jantung normal adalah 60-100 bpm
- Detak < 50 bpm diperlakukan sebagai BAHAYA KRITIS
- Detak 50-59 bpm diperlakukan sebagai WASPADA
- Detak > 100 bpm diperlakukan sebagai BAHAYA KRITIS
- Setiap data monitoring otomatis disimpan ke riwayat
- Alarm otomatis dibuat ketika ada kondisi abnormal
- Lokasi dan timestamp selalu tercatat saat alarm

## 🐛 Troubleshooting

### Port 8000 sudah digunakan
```bash
# Gunakan port berbeda
uvicorn main:app --port 8001
```

### Database error
```bash
# Hapus database lama dan buat baru
rm monitoring_kesehatan.db
python main.py
```

### CORS error
Pastikan CORS middleware sudah aktif di main.py

## 📞 Support

Untuk pertanyaan atau laporan bug, silakan buka issue atau hubungi tim development.

---

**Dibuat dengan ❤️ menggunakan FastAPI**
