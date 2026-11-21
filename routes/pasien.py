"""
Route untuk manajemen data pasien
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import sqlite3
from models import PasienCreate, Pasien, ResponseAPI
from database import get_db_connection, init_database, tentukan_status_detak


router = APIRouter(prefix="/api/pasien", tags=["Pasien"])


@router.get("/", response_model=list[Pasien])
async def daftar_pasien():
    """Mendapatkan daftar semua pasien"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pasien")
    hasil = cursor.fetchall()
    conn.close()
    
    pasien_list = [dict(row) for row in hasil]
    return pasien_list


@router.post("/", response_model=ResponseAPI)
async def buat_pasien(pasien_data: PasienCreate):
    """Membuat data pasien baru dengan registrasi"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tentukan status awal berdasarkan detak jantung
    status, _ = tentukan_status_detak(pasien_data.detak_jantung)
    
    try:
        cursor.execute("""
            INSERT INTO pasien 
            (nama, usia, detak_jantung, tekanan_darah_sistol, 
             tekanan_darah_diastol, lokasi_latitude, lokasi_longitude, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pasien_data.nama,
            pasien_data.usia,
            pasien_data.detak_jantung,
            pasien_data.tekanan_darah_sistol,
            pasien_data.tekanan_darah_diastol,
            pasien_data.lokasi.latitude,
            pasien_data.lokasi.longitude,
            status
        ))
        
        conn.commit()
        pasien_id = cursor.lastrowid
        conn.close()
        
        return ResponseAPI(
            status="NORMAL",
            pesan=f"✓ Pasien '{pasien_data.nama}' berhasil didaftarkan",
            data={
                "id": pasien_id,
                "nama": pasien_data.nama,
                "usia": pasien_data.usia
            },
            alarm=False
        )
    
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal membuat pasien: {str(e)}"
        )


@router.get("/{pasien_id}", response_model=Pasien)
async def ambil_pasien(pasien_id: int):
    """Mendapatkan data pasien berdasarkan ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pasien WHERE id = ?", (pasien_id,))
    pasien = cursor.fetchone()
    conn.close()
    
    if not pasien:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pasien dengan ID {pasien_id} tidak ditemukan"
        )
    
    return dict(pasien)


@router.put("/{pasien_id}", response_model=ResponseAPI)
async def perbarui_pasien(pasien_id: int, pasien_data: PasienCreate):
    """Memperbarui data pasien"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah pasien ada
    cursor.execute("SELECT id FROM pasien WHERE id = ?", (pasien_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pasien dengan ID {pasien_id} tidak ditemukan"
        )
    
    status_baru, _ = tentukan_status_detak(pasien_data.detak_jantung)
    
    try:
        cursor.execute("""
            UPDATE pasien
            SET nama = ?, usia = ?, detak_jantung = ?,
                tekanan_darah_sistol = ?, tekanan_darah_diastol = ?,
                lokasi_latitude = ?, lokasi_longitude = ?,
                status = ?, diperbarui_pada = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            pasien_data.nama,
            pasien_data.usia,
            pasien_data.detak_jantung,
            pasien_data.tekanan_darah_sistol,
            pasien_data.tekanan_darah_diastol,
            pasien_data.lokasi.latitude,
            pasien_data.lokasi.longitude,
            status_baru,
            pasien_id
        ))
        
        conn.commit()
        conn.close()
        
        return ResponseAPI(
            status="NORMAL",
            pesan=f"✓ Data pasien '{pasien_data.nama}' berhasil diperbarui",
            data={"id": pasien_id},
            alarm=False
        )
    
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal memperbarui pasien: {str(e)}"
        )


@router.delete("/{pasien_id}", response_model=ResponseAPI)
async def hapus_pasien(pasien_id: int):
    """Menghapus data pasien"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah pasien ada
    cursor.execute("SELECT nama FROM pasien WHERE id = ?", (pasien_id,))
    pasien = cursor.fetchone()
    
    if not pasien:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pasien dengan ID {pasien_id} tidak ditemukan"
        )
    
    nama_pasien = pasien[0]
    
    try:
        # Hapus riwayat monitoring terlebih dahulu
        cursor.execute("DELETE FROM monitoring_riwayat WHERE pasien_id = ?", (pasien_id,))
        # Hapus alarm
        cursor.execute("DELETE FROM alarm WHERE pasien_id = ?", (pasien_id,))
        # Hapus pasien
        cursor.execute("DELETE FROM pasien WHERE id = ?", (pasien_id,))
        
        conn.commit()
        conn.close()
        
        return ResponseAPI(
            status="NORMAL",
            pesan=f"✓ Pasien '{nama_pasien}' berhasil dihapus",
            data={"id": pasien_id},
            alarm=False
        )
    
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal menghapus pasien: {str(e)}"
        )
