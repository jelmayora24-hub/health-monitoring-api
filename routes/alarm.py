"""
Route untuk sistem alarm dan notifikasi darurat
"""

from fastapi import APIRouter, HTTPException, status, Query
from datetime import datetime, timedelta
import sqlite3
from models import Alarm, ResponseAPI
from database import get_db_connection


router = APIRouter(prefix="/api/alarm", tags=["Alarm"])


@router.get("/", response_model=list[Alarm])
async def daftar_alarm():
    """Mendapatkan daftar semua alarm"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM alarm 
        ORDER BY timestamp DESC
    """)
    hasil = cursor.fetchall()
    conn.close()
    
    alarm_list = [dict(row) for row in hasil]
    return alarm_list


@router.get("/pasien/{pasien_id}", response_model=list[Alarm])
async def ambil_alarm_pasien(
    pasien_id: int,
    jam_terakhir: int = Query(24, ge=1, description="Alarm dalam jam terakhir")
):
    """Mendapatkan daftar alarm untuk pasien tertentu"""
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
    
    # Hitung waktu dari jam terakhir
    waktu_awal = datetime.now() - timedelta(hours=jam_terakhir)
    
    cursor.execute("""
        SELECT * FROM alarm 
        WHERE pasien_id = ? AND timestamp >= ?
        ORDER BY timestamp DESC
    """, (pasien_id, waktu_awal))
    
    hasil = cursor.fetchall()
    conn.close()
    
    alarm_list = [dict(row) for row in hasil]
    return alarm_list


@router.get("/kritis", response_model=ResponseAPI)
async def ambil_alarm_kritis():
    """Mendapatkan alarm kritis (detak jantung < 50 atau > 100)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) as total FROM alarm 
        WHERE tipe_alarm = 'DETAK JANTUNG KRITIS'
        AND timestamp >= datetime('now', '-24 hours')
    """)
    
    hasil = cursor.fetchone()
    total_kritis = hasil['total'] if hasil else 0
    
    # Ambil alarm kritis terakhir
    cursor.execute("""
        SELECT * FROM alarm 
        WHERE tipe_alarm = 'DETAK JANTUNG KRITIS'
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    
    alarm_list = cursor.fetchall()
    conn.close()
    
    detail_alarm = [dict(row) for row in alarm_list]
    
    return ResponseAPI(
        status="BAHAYA" if total_kritis > 0 else "NORMAL",
        pesan=f"Total alarm kritis dalam 24 jam: {total_kritis}",
        data={
            "total_kritis": total_kritis,
            "alarm_terbaru": detail_alarm[:5]  # Top 5 alarm terakhir
        },
        alarm=total_kritis > 0
    )


@router.get("/statistik", response_model=ResponseAPI)
async def ambil_statistik_alarm():
    """Mendapatkan statistik alarm"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total alarm semua waktu
    cursor.execute("SELECT COUNT(*) as total FROM alarm")
    total_alarm = cursor.fetchone()['total']
    
    # Alarm hari ini
    cursor.execute("""
        SELECT COUNT(*) as total FROM alarm 
        WHERE DATE(timestamp) = DATE('now')
    """)
    alarm_hari_ini = cursor.fetchone()['total']
    
    # Alarm jam terakhir
    cursor.execute("""
        SELECT COUNT(*) as total FROM alarm 
        WHERE timestamp >= datetime('now', '-1 hour')
    """)
    alarm_jam_terakhir = cursor.fetchone()['total']
    
    # Alarm per tipe
    cursor.execute("""
        SELECT tipe_alarm, COUNT(*) as jumlah FROM alarm 
        GROUP BY tipe_alarm
    """)
    alarm_per_tipe = dict((row['tipe_alarm'], row['jumlah']) for row in cursor.fetchall())
    
    # Top 3 pasien dengan alarm terbanyak
    cursor.execute("""
        SELECT pasien_id, COUNT(*) as total_alarm 
        FROM alarm 
        GROUP BY pasien_id 
        ORDER BY total_alarm DESC 
        LIMIT 3
    """)
    top_pasien = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return ResponseAPI(
        status="NORMAL",
        pesan="Statistik alarm sistem monitoring",
        data={
            "total_alarm_semua_waktu": total_alarm,
            "alarm_hari_ini": alarm_hari_ini,
            "alarm_jam_terakhir": alarm_jam_terakhir,
            "alarm_per_tipe": alarm_per_tipe,
            "top_3_pasien_dengan_alarm": top_pasien
        },
        alarm=False
    )


@router.delete("/{alarm_id}", response_model=ResponseAPI)
async def hapus_alarm(alarm_id: int):
    """Menghapus alarm berdasarkan ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah alarm ada
    cursor.execute("SELECT id FROM alarm WHERE id = ?", (alarm_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alarm dengan ID {alarm_id} tidak ditemukan"
        )
    
    try:
        cursor.execute("DELETE FROM alarm WHERE id = ?", (alarm_id,))
        conn.commit()
        conn.close()
        
        return ResponseAPI(
            status="NORMAL",
            pesan=f"✓ Alarm ID {alarm_id} berhasil dihapus",
            data={"alarm_id": alarm_id},
            alarm=False
        )
    
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal menghapus alarm: {str(e)}"
        )


@router.delete("/pasien/{pasien_id}/all", response_model=ResponseAPI)
async def hapus_semua_alarm_pasien(pasien_id: int):
    """Menghapus semua alarm untuk pasien tertentu"""
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
        cursor.execute("DELETE FROM alarm WHERE pasien_id = ?", (pasien_id,))
        jumlah_dihapus = cursor.rowcount
        conn.commit()
        conn.close()
        
        return ResponseAPI(
            status="NORMAL",
            pesan=f"✓ Semua alarm pasien '{nama_pasien}' berhasil dihapus",
            data={
                "pasien_id": pasien_id,
                "jumlah_alarm_dihapus": jumlah_dihapus
            },
            alarm=False
        )
    
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal menghapus alarm: {str(e)}"
        )
