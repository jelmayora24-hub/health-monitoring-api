# 📋 API DOCUMENTATION - Aplikasi Monitoring Kesehatan

## Overview

API ini menyediakan endpoint lengkap untuk monitoring kesehatan pasien real-time dengan fitur WebSocket, alarm otomatis, dan tracking lokasi.

## Base URL
```
http://localhost:8000
```

## Format Response Standar

Semua response API dalam format JSON:
```json
{
  "status": "NORMAL|WASPADA|BAHAYA",
  "pesan": "Keterangan status",
  "data": {...},
  "timestamp": "2024-01-15T10:30:45.123456",
  "alarm": true|false
}
```

## Status Kesehatan

| Status | Detak Jantung | Warna | Aksi |
|--------|---------------|-------|------|
| NORMAL | 60-100 bpm | 🟢 Hijau | Monitoring normal |
| WASPADA | 50-59 bpm | 🟡 Kuning | Perlu perhatian |
| BAHAYA | < 50 bpm | 🔴 Merah | EMERGENCY - Hubungi dokter |
| BAHAYA | > 100 bpm | 🔴 Merah | EMERGENCY - Hubungi dokter |

---

# 🏥 ENDPOINT MANAJEMEN PASIEN

## 1. Daftar Semua Pasien

**GET** `/api/pasien`

Mendapatkan daftar semua pasien yang terdaftar.

### Request
```bash
curl http://localhost:8000/api/pasien
```

### Response (200 OK)
```json
[
  {
    "id": 1,
    "nama": "Budi Santoso",
    "usia": 45,
    "detak_jantung": 75,
    "tekanan_darah_sistol": 120,
    "tekanan_darah_diastol": 80,
    "lokasi_latitude": -6.2088,
    "lokasi_longitude": 106.8456,
    "status": "NORMAL",
    "dibuat_pada": "2024-01-15T10:00:00",
    "diperbarui_pada": "2024-01-15T10:30:00"
  }
]
```

---

## 2. Buat Pasien Baru (Registrasi)

**POST** `/api/pasien`

Mendaftarkan pasien baru dengan informasi awal.

### Request
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

### Request Body
```json
{
  "nama": "string (required, min 1 char)",
  "usia": "integer (required, 1-150)",
  "detak_jantung": "integer (required, >= 0)",
  "tekanan_darah_sistol": "integer (required)",
  "tekanan_darah_diastol": "integer (required)",
  "lokasi": {
    "latitude": "float (required)",
    "longitude": "float (required)"
  }
}
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "✓ Pasien 'Budi Santoso' berhasil didaftarkan",
  "data": {
    "id": 1,
    "nama": "Budi Santoso",
    "usia": 45
  },
  "timestamp": "2024-01-15T10:30:45.123456",
  "alarm": false
}
```

---

## 3. Ambil Detail Pasien

**GET** `/api/pasien/{pasien_id}`

Mendapatkan detail lengkap satu pasien.

### Request
```bash
curl http://localhost:8000/api/pasien/1
```

### Response (200 OK)
```json
{
  "id": 1,
  "nama": "Budi Santoso",
  "usia": 45,
  "detak_jantung": 75,
  "tekanan_darah_sistol": 120,
  "tekanan_darah_diastol": 80,
  "lokasi_latitude": -6.2088,
  "lokasi_longitude": 106.8456,
  "status": "NORMAL",
  "dibuat_pada": "2024-01-15T10:00:00",
  "diperbarui_pada": "2024-01-15T10:30:00"
}
```

### Error Response (404 Not Found)
```json
{
  "detail": "Pasien dengan ID 999 tidak ditemukan"
}
```

---

## 4. Update Data Pasien

**PUT** `/api/pasien/{pasien_id}`

Memperbarui data pasien yang sudah terdaftar.

### Request
```bash
curl -X PUT http://localhost:8000/api/pasien/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Budi Santoso",
    "usia": 46,
    "detak_jantung": 78,
    "tekanan_darah_sistol": 122,
    "tekanan_darah_diastol": 82,
    "lokasi": {
      "latitude": -6.2090,
      "longitude": 106.8460
    }
  }'
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "✓ Data pasien 'Budi Santoso' berhasil diperbarui",
  "data": {
    "id": 1
  },
  "timestamp": "2024-01-15T10:35:00.123456",
  "alarm": false
}
```

---

## 5. Hapus Pasien

**DELETE** `/api/pasien/{pasien_id}`

Menghapus pasien dan semua data terkaitnya.

### Request
```bash
curl -X DELETE http://localhost:8000/api/pasien/1
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "✓ Pasien 'Budi Santoso' berhasil dihapus",
  "data": {
    "id": 1
  },
  "timestamp": "2024-01-15T10:40:00.123456",
  "alarm": false
}
```

---

# 📊 ENDPOINT MONITORING

## 6. Update Monitoring Pasien

**POST** `/api/monitor/{pasien_id}/update`

Update data monitoring pasien dan otomatis mengecek status kesehatan.

### Request
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

### Response - Status NORMAL (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "NORMAL. Detak jantung 88 bpm (sehat)",
  "data": {
    "pasien_id": 1,
    "detak_jantung": 88,
    "tekanan_darah": "125/82",
    "lokasi": {
      "latitude": -6.2088,
      "longitude": 106.8456
    }
  },
  "timestamp": "2024-01-15T10:45:00.123456",
  "alarm": false
}
```

### Response - Status WASPADA (200 OK)
```json
{
  "status": "WASPADA",
  "pesan": "WASPADA! Detak jantung 55 bpm (rendah)",
  "data": {...},
  "alarm": true
}
```

### Response - Status BAHAYA (200 OK)
```json
{
  "status": "BAHAYA",
  "pesan": "BAHAYA KRITIS! Detak jantung 45 bpm (sangat rendah)",
  "data": {...},
  "alarm": true
}
```

---

## 7. Ambil Riwayat Monitoring

**GET** `/api/monitor/{pasien_id}/riwayat?limit=100`

Mendapatkan riwayat monitoring pasien.

### Query Parameters
- `limit` (optional): Jumlah riwayat yang diambil (default: 100, max: 1000)

### Request
```bash
curl "http://localhost:8000/api/monitor/1/riwayat?limit=50"
```

### Response (200 OK)
```json
[
  {
    "id": 150,
    "pasien_id": 1,
    "detak_jantung": 88,
    "tekanan_darah_sistol": 125,
    "tekanan_darah_diastol": 82,
    "lokasi_latitude": -6.2088,
    "lokasi_longitude": 106.8456,
    "status": "NORMAL",
    "ada_alarm": false,
    "timestamp": "2024-01-15T10:45:00"
  },
  {
    "id": 149,
    "pasien_id": 1,
    "detak_jantung": 75,
    "tekanan_darah_sistol": 120,
    "tekanan_darah_diastol": 80,
    "lokasi_latitude": -6.2088,
    "lokasi_longitude": 106.8456,
    "status": "NORMAL",
    "ada_alarm": false,
    "timestamp": "2024-01-15T10:40:00"
  }
]
```

---

## 8. WebSocket Monitoring Real-time

**WS** `/api/monitor/ws/{pasien_id}`

Monitoring real-time dengan WebSocket untuk update data langsung.

### JavaScript Client Example
```javascript
// Buat koneksi WebSocket
const ws = new WebSocket('ws://localhost:8000/api/monitor/ws/1');

// Handler ketika koneksi terbuka
ws.onopen = (event) => {
  console.log('Terhubung ke server');
  
  // Kirim data monitoring
  const data = {
    detak_jantung: 88,
    tekanan_darah_sistol: 125,
    tekanan_darah_diastol: 82,
    lokasi: {
      latitude: -6.2088,
      longitude: 106.8456
    }
  };
  
  ws.send(JSON.stringify(data));
};

// Handler ketika menerima pesan
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  
  console.log('Status:', response.status);
  console.log('Pesan:', response.pesan);
  console.log('Detak Jantung:', response.detak_jantung, 'bpm');
  console.log('Tekanan Darah:', response.tekanan_darah);
  console.log('Alarm:', response.alarm);
  console.log('Timestamp:', response.timestamp);
  
  // Update UI berdasarkan status
  if (response.status === 'NORMAL') {
    document.body.style.backgroundColor = '#90EE90'; // Hijau
  } else if (response.status === 'WASPADA') {
    document.body.style.backgroundColor = '#FFFF00'; // Kuning
  } else if (response.status === 'BAHAYA') {
    document.body.style.backgroundColor = '#FF0000'; // Merah
    playAlarmSound(); // Mainkan suara alarm
  }
};

// Handler error
ws.onerror = (event) => {
  console.error('WebSocket error:', event);
};

// Handler ketika koneksi ditutup
ws.onclose = (event) => {
  console.log('Koneksi ditutup');
};
```

### Python Client Example
```python
import asyncio
import json
import websockets

async def monitor():
    async with websockets.connect('ws://localhost:8000/api/monitor/ws/1') as ws:
        # Kirim data
        data = {
            "detak_jantung": 88,
            "tekanan_darah_sistol": 125,
            "tekanan_darah_diastol": 82,
            "lokasi": {
                "latitude": -6.2088,
                "longitude": 106.8456
            }
        }
        await ws.send(json.dumps(data))
        
        # Terima response
        response = await ws.recv()
        print(json.loads(response))

asyncio.run(monitor())
```

---

# 🚨 ENDPOINT ALARM & NOTIFIKASI

## 9. Ambil Semua Alarm

**GET** `/api/alarm`

Mendapatkan daftar semua alarm yang pernah terjadi.

### Request
```bash
curl http://localhost:8000/api/alarm
```

### Response (200 OK)
```json
[
  {
    "id": 1,
    "pasien_id": 1,
    "tipe_alarm": "DETAK JANTUNG KRITIS",
    "nilai_detak": 45,
    "lokasi_latitude": -6.2088,
    "lokasi_longitude": 106.8456,
    "pesan": "BAHAYA KRITIS! Detak jantung 45 bpm (sangat rendah)",
    "timestamp": "2024-01-15T10:50:00"
  }
]
```

---

## 10. Ambil Alarm Pasien Tertentu

**GET** `/api/alarm/pasien/{pasien_id}?jam_terakhir=24`

Mendapatkan alarm untuk pasien spesifik dalam periode tertentu.

### Query Parameters
- `jam_terakhir` (optional): Alarm dalam jam terakhir (default: 24)

### Request
```bash
curl "http://localhost:8000/api/alarm/pasien/1?jam_terakhir=24"
```

### Response (200 OK)
```json
[
  {
    "id": 5,
    "pasien_id": 1,
    "tipe_alarm": "DETAK JANTUNG WASPADA",
    "nilai_detak": 55,
    "lokasi_latitude": -6.2088,
    "lokasi_longitude": 106.8456,
    "pesan": "WASPADA! Detak jantung 55 bpm (rendah)",
    "timestamp": "2024-01-15T09:30:00"
  }
]
```

---

## 11. Ambil Alarm Kritis (24 jam terakhir)

**GET** `/api/alarm/kritis`

Mendapatkan ringkasan alarm kritis dan yang terbaru.

### Request
```bash
curl http://localhost:8000/api/alarm/kritis
```

### Response (200 OK)
```json
{
  "status": "BAHAYA",
  "pesan": "Total alarm kritis dalam 24 jam: 3",
  "data": {
    "total_kritis": 3,
    "alarm_terbaru": [
      {
        "id": 10,
        "pasien_id": 1,
        "tipe_alarm": "DETAK JANTUNG KRITIS",
        "nilai_detak": 120,
        "lokasi_latitude": -6.2088,
        "lokasi_longitude": 106.8456,
        "pesan": "BAHAYA KRITIS! Detak jantung 120 bpm (sangat tinggi)",
        "timestamp": "2024-01-15T10:50:00"
      }
    ]
  },
  "timestamp": "2024-01-15T10:55:00.123456",
  "alarm": true
}
```

---

## 12. Statistik Alarm

**GET** `/api/alarm/statistik`

Mendapatkan statistik lengkap sistem alarm.

### Request
```bash
curl http://localhost:8000/api/alarm/statistik
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "Statistik alarm sistem monitoring",
  "data": {
    "total_alarm_semua_waktu": 125,
    "alarm_hari_ini": 8,
    "alarm_jam_terakhir": 2,
    "alarm_per_tipe": {
      "DETAK JANTUNG KRITIS": 85,
      "DETAK JANTUNG WASPADA": 40
    },
    "top_3_pasien_dengan_alarm": [
      {
        "pasien_id": 1,
        "total_alarm": 45
      },
      {
        "pasien_id": 3,
        "total_alarm": 32
      },
      {
        "pasien_id": 5,
        "total_alarm": 28
      }
    ]
  },
  "timestamp": "2024-01-15T10:55:00.123456",
  "alarm": false
}
```

---

## 13. Hapus Alarm

**DELETE** `/api/alarm/{alarm_id}`

Menghapus satu alarm tertentu.

### Request
```bash
curl -X DELETE http://localhost:8000/api/alarm/1
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "✓ Alarm ID 1 berhasil dihapus",
  "data": {
    "alarm_id": 1
  },
  "timestamp": "2024-01-15T11:00:00.123456",
  "alarm": false
}
```

---

## 14. Hapus Semua Alarm Pasien

**DELETE** `/api/alarm/pasien/{pasien_id}/all`

Menghapus semua alarm untuk pasien tertentu.

### Request
```bash
curl -X DELETE http://localhost:8000/api/alarm/pasien/1/all
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "✓ Semua alarm pasien 'Budi Santoso' berhasil dihapus",
  "data": {
    "pasien_id": 1,
    "jumlah_alarm_dihapus": 45
  },
  "timestamp": "2024-01-15T11:05:00.123456",
  "alarm": false
}
```

---

# ⚙️ ENDPOINT SYSTEM

## 15. Health Check

**GET** `/health`

Mengecek apakah server sedang berjalan.

### Request
```bash
curl http://localhost:8000/health
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "✓ Server sedang berjalan dengan baik",
  "data": {
    "server": "Online",
    "timestamp": "2024-01-15T11:10:00",
    "status": "Operational"
  },
  "timestamp": "2024-01-15T11:10:00.123456",
  "alarm": false
}
```

---

## 16. Info Aplikasi

**GET** `/api/info`

Mendapatkan informasi lengkap tentang aplikasi.

### Request
```bash
curl http://localhost:8000/api/info
```

### Response (200 OK)
```json
{
  "status": "NORMAL",
  "pesan": "Informasi Aplikasi Monitoring Kesehatan",
  "data": {
    "nama": "Aplikasi Monitoring Kesehatan",
    "deskripsi": "Sistem monitoring real-time untuk mendeteksi kondisi kesehatan pasien",
    "teknologi": {
      "framework": "FastAPI",
      "server": "Uvicorn",
      "database": "SQLite",
      "real_time": "WebSocket",
      "validasi": "Pydantic"
    },
    "fitur": [
      "Registrasi dan manajemen pasien",
      "Monitoring detak jantung real-time",
      "Sistem alarm otomatis",
      "Riwayat data monitoring",
      "Tracking lokasi pasien",
      "Notifikasi darurat otomatis"
    ],
    "endpoint_utama": {
      "pasien": "/api/pasien",
      "monitoring": "/api/monitor",
      "alarm": "/api/alarm",
      "dokumentasi": "/docs"
    },
    "status_kesehatan": {
      "detak_normal": "60-100 bpm",
      "detak_waspada": "50-59 bpm",
      "detak_kritis_rendah": "< 50 bpm",
      "detak_kritis_tinggi": "> 100 bpm"
    }
  },
  "timestamp": "2024-01-15T11:15:00.123456",
  "alarm": false
}
```

---

# 🔄 Alur Penggunaan Khas

### 1. Registrasi Pasien Baru
```bash
POST /api/pasien
```

### 2. Mulai Monitoring
```bash
# Option A: Update berkala
POST /api/monitor/{id}/update

# Option B: Real-time WebSocket
WS /api/monitor/ws/{id}
```

### 3. Monitor Alarm
```bash
# Cek alarm kritis
GET /api/alarm/kritis

# Lihat alarm pasien spesifik
GET /api/alarm/pasien/{id}
```

### 4. Analisis Statistik
```bash
GET /api/alarm/statistik
GET /api/monitor/{id}/riwayat
```

---

# ⚠️ Error Handling

Semua error response memiliki struktur:

```json
{
  "detail": "Deskripsi error"
}
```

### Common Error Codes

| Code | Pesan | Penyebab |
|------|-------|---------|
| 400 | Validation Error | Input tidak sesuai format |
| 404 | Not Found | Resource tidak ditemukan |
| 422 | Unprocessable Entity | Data tidak valid |
| 500 | Internal Server Error | Error di server |

---

**API Version**: 1.0.0
**Last Updated**: 2024
**Status**: Active
