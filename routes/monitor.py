"""
Route untuk monitoring real-time dan WebSocket
"""

from fastapi import APIRouter, WebSocket, HTTPException, status, Query
from datetime import datetime
import sqlite3
import json
from typing import List
from models import UpdateMonitoring, DataMonitoring, ResponseAPI
from database import (
    get_db_connection, 
    tentukan_status_detak,
    generate_pesan_status
)


router = APIRouter(prefix="/api/monitor", tags=["Monitoring"])

# Menyimpan koneksi WebSocket aktif per pasien
active_connections: dict[int, List[WebSocket]] = {}


@router.get("/{pasien_id}/riwayat", response_model=List[DataMonitoring])
async def ambil_riwayat(pasien_id: int, limit: int = Query(100, ge=1, le=1000)):
    """Mendapatkan riwayat monitoring per pasien"""
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
    
    # Ambil riwayat terbaru
    cursor.execute("""
        SELECT * FROM monitoring_riwayat 
        WHERE pasien_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (pasien_id, limit))
    
    hasil = cursor.fetchall()
    conn.close()
    
    riwayat = [dict(row) for row in hasil]
    return riwayat


@router.post("/{pasien_id}/update", response_model=ResponseAPI)
async def update_monitoring(pasien_id: int, data: UpdateMonitoring):
    """Update data monitoring pasien dan check status"""
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
    
    # Tentukan status berdasarkan detak jantung
    status_kesehatan, ada_alarm = tentukan_status_detak(data.detak_jantung)
    pesan_status = generate_pesan_status(data.detak_jantung, status_kesehatan)
    
    try:
        # Simpan ke riwayat monitoring
        cursor.execute("""
            INSERT INTO monitoring_riwayat
            (pasien_id, detak_jantung, tekanan_darah_sistol, 
             tekanan_darah_diastol, lokasi_latitude, lokasi_longitude, 
             status, ada_alarm, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            pasien_id,
            data.detak_jantung,
            data.tekanan_darah_sistol,
            data.tekanan_darah_diastol,
            data.lokasi.latitude,
            data.lokasi.longitude,
            status_kesehatan,
            ada_alarm
        ))
        
        # Update data pasien terbaru
        cursor.execute("""
            UPDATE pasien
            SET detak_jantung = ?, tekanan_darah_sistol = ?,
                tekanan_darah_diastol = ?, 
                lokasi_latitude = ?, lokasi_longitude = ?,
                status = ?, diperbarui_pada = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            data.detak_jantung,
            data.tekanan_darah_sistol,
            data.tekanan_darah_diastol,
            data.lokasi.latitude,
            data.lokasi.longitude,
            status_kesehatan,
            pasien_id
        ))
        
        # Jika ada alarm, simpan ke tabel alarm
        if ada_alarm:
            tipe_alarm = "DETAK JANTUNG KRITIS" if data.detak_jantung < 50 or data.detak_jantung > 100 else "DETAK JANTUNG WASPADA"
            
            cursor.execute("""
                INSERT INTO alarm
                (pasien_id, tipe_alarm, nilai_detak, 
                 lokasi_latitude, lokasi_longitude, pesan, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                pasien_id,
                tipe_alarm,
                data.detak_jantung,
                data.lokasi.latitude,
                data.lokasi.longitude,
                pesan_status
            ))
        
        conn.commit()
        conn.close()
        
        return ResponseAPI(
            status=status_kesehatan,
            pesan=pesan_status,
            data={
                "pasien_id": pasien_id,
                "detak_jantung": data.detak_jantung,
                "tekanan_darah": f"{data.tekanan_darah_sistol}/{data.tekanan_darah_diastol}",
                "lokasi": {
                    "latitude": data.lokasi.latitude,
                    "longitude": data.lokasi.longitude
                }
            },
            alarm=ada_alarm
        )
    
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal update monitoring: {str(e)}"
        )


@router.websocket("/ws/{pasien_id}")
async def websocket_monitor(websocket: WebSocket, pasien_id: int):
    """WebSocket endpoint untuk monitoring real-time per pasien"""
    
    # Cek apakah pasien ada
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama FROM pasien WHERE id = ?", (pasien_id,))
    pasien = cursor.fetchone()
    conn.close()
    
    if not pasien:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Pasien tidak ditemukan")
        return
    
    await websocket.accept()
    
    # Tambahkan ke daftar koneksi aktif
    if pasien_id not in active_connections:
        active_connections[pasien_id] = []
    active_connections[pasien_id].append(websocket)
    
    try:
        while True:
            # Terima data dari client
            data = await websocket.receive_text()
            data_json = json.loads(data)
            
            # Parse data monitoring
            monitoring_data = UpdateMonitoring(**data_json)
            
            # Proses seperti endpoint update biasa
            conn = get_db_connection()
            cursor = conn.cursor()
            
            status_kesehatan, ada_alarm = tentukan_status_detak(monitoring_data.detak_jantung)
            pesan_status = generate_pesan_status(monitoring_data.detak_jantung, status_kesehatan)
            
            # Simpan riwayat
            cursor.execute("""
                INSERT INTO monitoring_riwayat
                (pasien_id, detak_jantung, tekanan_darah_sistol, 
                 tekanan_darah_diastol, lokasi_latitude, lokasi_longitude, 
                 status, ada_alarm, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                pasien_id,
                monitoring_data.detak_jantung,
                monitoring_data.tekanan_darah_sistol,
                monitoring_data.tekanan_darah_diastol,
                monitoring_data.lokasi.latitude,
                monitoring_data.lokasi.longitude,
                status_kesehatan,
                ada_alarm
            ))
            
            # Update pasien
            cursor.execute("""
                UPDATE pasien
                SET detak_jantung = ?, tekanan_darah_sistol = ?,
                    tekanan_darah_diastol = ?, 
                    lokasi_latitude = ?, lokasi_longitude = ?,
                    status = ?, diperbarui_pada = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                monitoring_data.detak_jantung,
                monitoring_data.tekanan_darah_sistol,
                monitoring_data.tekanan_darah_diastol,
                monitoring_data.lokasi.latitude,
                monitoring_data.lokasi.longitude,
                status_kesehatan,
                pasien_id
            ))
            
            if ada_alarm:
                tipe_alarm = "DETAK JANTUNG KRITIS" if monitoring_data.detak_jantung < 50 or monitoring_data.detak_jantung > 100 else "DETAK JANTUNG WASPADA"
                
                cursor.execute("""
                    INSERT INTO alarm
                    (pasien_id, tipe_alarm, nilai_detak, 
                     lokasi_latitude, lokasi_longitude, pesan, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    pasien_id,
                    tipe_alarm,
                    monitoring_data.detak_jantung,
                    monitoring_data.lokasi.latitude,
                    monitoring_data.lokasi.longitude,
                    pesan_status
                ))
            
            conn.commit()
            conn.close()
            
            # Siapkan response
            response_data = {
                "status": status_kesehatan,
                "pesan": pesan_status,
                "detak_jantung": monitoring_data.detak_jantung,
                "tekanan_darah": f"{monitoring_data.tekanan_darah_sistol}/{monitoring_data.tekanan_darah_diastol}",
                "lokasi": {
                    "latitude": monitoring_data.lokasi.latitude,
                    "longitude": monitoring_data.lokasi.longitude
                },
                "alarm": ada_alarm,
                "timestamp": datetime.now().isoformat()
            }
            
            # Kirim ke semua client yang terhubung untuk pasien ini
            for connection in active_connections[pasien_id]:
                try:
                    await connection.send_json(response_data)
                except:
                    pass
    
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    
    finally:
        # Hapus koneksi dari daftar
        if pasien_id in active_connections:
            active_connections[pasien_id].remove(websocket)
            if not active_connections[pasien_id]:
                del active_connections[pasien_id]
