"""
File Utama Aplikasi Monitoring Kesehatan
Menggunakan FastAPI untuk API dan WebSocket real-time
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from database import init_database
from models import ResponseAPI
from routes.pasien import router as router_pasien
from routes.monitor import router as router_monitor
from routes.alarm import router as router_alarm


# Inisialisasi FastAPI
app = FastAPI(
    title="Aplikasi Monitoring Kesehatan",
    description="API Monitoring Kesehatan Real-time dengan WebSocket",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware - untuk akses dari aplikasi mobile/web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa juga spesifik: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router_pasien)
app.include_router(router_monitor)
app.include_router(router_alarm)


@app.on_event("startup")
async def startup_event():
    """Event yang dijalankan saat aplikasi startup"""
    init_database()
    print("=" * 60)
    print("🏥 APLIKASI MONITORING KESEHATAN")
    print("=" * 60)
    print("✓ Database diinisialisasi")
    print("✓ API siap melayani request")
    print("✓ WebSocket siap untuk monitoring real-time")
    print("=" * 60)


@app.get("/", response_model=ResponseAPI)
async def root():
    """Endpoint root - informasi aplikasi"""
    return ResponseAPI(
        status="NORMAL",
        pesan="Selamat datang di Aplikasi Monitoring Kesehatan",
        data={
            "nama_aplikasi": "Monitoring Kesehatan Real-time",
            "versi": "1.0.0",
            "dokumentasi": "/docs",
            "redoc": "/redoc"
        },
        alarm=False
    )


@app.get("/health", response_model=ResponseAPI)
async def health_check():
    """Endpoint untuk cek server berjalan - Health Check"""
    return ResponseAPI(
        status="NORMAL",
        pesan="✓ Server sedang berjalan dengan baik",
        data={
            "server": "Online",
            "timestamp": datetime.now().isoformat(),
            "status": "Operational"
        },
        alarm=False
    )


@app.get("/api/info", response_model=ResponseAPI)
async def info_aplikasi():
    """Informasi lengkap tentang aplikasi"""
    return ResponseAPI(
        status="NORMAL",
        pesan="Informasi Aplikasi Monitoring Kesehatan",
        data={
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
        alarm=False
    )


if __name__ == "__main__":
    import uvicorn
    
    print("\n🚀 Memulai server...")
    print("📍 URL: http://localhost:8000")
    print("📚 Dokumentasi: http://localhost:8000/docs\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
