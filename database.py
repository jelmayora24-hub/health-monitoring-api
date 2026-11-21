"""
Konfigurasi dan manajemen database SQLite
"""

import sqlite3
from datetime import datetime
from pathlib import Path


# Path ke database
DB_PATH = Path(__file__).parent / "monitoring_kesehatan.db"


def get_db_connection():
    """Membuat koneksi ke database SQLite"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Inisialisasi database dan membuat tabel jika belum ada"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabel pasien
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            usia INTEGER NOT NULL,
            detak_jantung INTEGER NOT NULL,
            tekanan_darah_sistol INTEGER NOT NULL,
            tekanan_darah_diastol INTEGER NOT NULL,
            lokasi_latitude REAL NOT NULL,
            lokasi_longitude REAL NOT NULL,
            status TEXT NOT NULL,
            dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            diperbarui_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabel riwayat monitoring
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pasien_id INTEGER NOT NULL,
            detak_jantung INTEGER NOT NULL,
            tekanan_darah_sistol INTEGER NOT NULL,
            tekanan_darah_diastol INTEGER NOT NULL,
            lokasi_latitude REAL NOT NULL,
            lokasi_longitude REAL NOT NULL,
            status TEXT NOT NULL,
            ada_alarm BOOLEAN NOT NULL DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pasien_id) REFERENCES pasien(id)
        )
    """)

    # Tabel alarm
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alarm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pasien_id INTEGER NOT NULL,
            tipe_alarm TEXT NOT NULL,
            nilai_detak INTEGER NOT NULL,
            lokasi_latitude REAL NOT NULL,
            lokasi_longitude REAL NOT NULL,
            pesan TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pasien_id) REFERENCES pasien(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✓ Database telah diinisialisasi")


def tentukan_status_detak(detak_jantung: int) -> tuple[str, bool]:
    """
    Menentukan status kesehatan berdasarkan detak jantung
    
    Returns:
        tuple: (status, ada_alarm)
    """
    if detak_jantung < 50:
        return "BAHAYA", True
    elif 50 <= detak_jantung < 60:
        return "WASPADA", True
    elif 60 <= detak_jantung <= 100:
        return "NORMAL", False
    else:  # detak_jantung > 100
        return "BAHAYA", True


def generate_pesan_status(detak_jantung: int, status: str) -> str:
    """Generate pesan status berdasarkan detak jantung"""
    if detak_jantung < 50:
        return f"BAHAYA KRITIS! Detak jantung {detak_jantung} bpm (sangat rendah)"
    elif 50 <= detak_jantung < 60:
        return f"WASPADA! Detak jantung {detak_jantung} bpm (rendah)"
    elif 60 <= detak_jantung <= 100:
        return f"NORMAL. Detak jantung {detak_jantung} bpm (sehat)"
    else:
        return f"BAHAYA KRITIS! Detak jantung {detak_jantung} bpm (sangat tinggi)"
