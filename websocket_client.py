"""
Client WebSocket untuk testing monitoring real-time
Run dengan: python websocket_client.py
"""

import asyncio
import json
import websockets
from datetime import datetime

# Konfigurasi
WEBSOCKET_URL = "ws://localhost:8000/api/monitor/ws"
PASIEN_ID = 1  # Sesuaikan dengan ID pasien yang ada

async def monitor_pasien():
    """Connect ke WebSocket dan send monitoring data"""
    
    print("\n" + "=" * 70)
    print("📡 WEBSOCKET CLIENT - MONITORING REAL-TIME")
    print("=" * 70)
    print(f"Menghubung ke: {WEBSOCKET_URL}/{PASIEN_ID}\n")
    
    try:
        async with websockets.connect(f"{WEBSOCKET_URL}/{PASIEN_ID}") as websocket:
            print("✓ Terhubung ke server WebSocket\n")
            
            # Simulasi data monitoring
            monitoring_scenarios = [
                {
                    "skenario": "Status NORMAL",
                    "detak_jantung": 75,
                    "tekanan_darah_sistol": 120,
                    "tekanan_darah_diastol": 80
                },
                {
                    "skenario": "Status WASPADA",
                    "detak_jantung": 55,
                    "tekanan_darah_sistol": 118,
                    "tekanan_darah_diastol": 78
                },
                {
                    "skenario": "Status BAHAYA (Rendah)",
                    "detak_jantung": 45,
                    "tekanan_darah_sistol": 110,
                    "tekanan_darah_diastol": 70
                },
                {
                    "skenario": "Status BAHAYA (Tinggi)",
                    "detak_jantung": 120,
                    "tekanan_darah_sistol": 140,
                    "tekanan_darah_diastol": 90
                },
                {
                    "skenario": "Kembali Normal",
                    "detak_jantung": 72,
                    "tekanan_darah_sistol": 118,
                    "tekanan_darah_diastol": 79
                }
            ]
            
            for i, scenario in enumerate(monitoring_scenarios, 1):
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"📊 Skenario {i}: {scenario['skenario']}")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                
                # Siapkan data
                data = {
                    "detak_jantung": scenario["detak_jantung"],
                    "tekanan_darah_sistol": scenario["tekanan_darah_sistol"],
                    "tekanan_darah_diastol": scenario["tekanan_darah_diastol"],
                    "lokasi": {
                        "latitude": -6.2088,
                        "longitude": 106.8456
                    }
                }
                
                print(f"\n📤 Mengirim data:")
                print(f"   Detak Jantung: {data['detak_jantung']} bpm")
                print(f"   Tekanan Darah: {data['tekanan_darah_sistol']}/{data['tekanan_darah_diastol']} mmHg")
                print(f"   Lokasi: ({data['lokasi']['latitude']}, {data['lokasi']['longitude']})")
                
                # Kirim data
                await websocket.send(json.dumps(data))
                
                # Tunggu response
                print(f"\n⏳ Menunggu response dari server...")
                response = await websocket.recv()
                response_data = json.loads(response)
                
                print(f"\n📥 Response dari server:")
                print(f"   Status: {response_data['status']}")
                print(f"   Pesan: {response_data['pesan']}")
                print(f"   Alarm: {'🚨 ADA ALARM!' if response_data['alarm'] else '✓ Tidak ada alarm'}")
                print(f"   Timestamp: {response_data['timestamp']}\n")
                
                # Tunggu sebelum skenario berikutnya
                if i < len(monitoring_scenarios):
                    print("⏸️  Tunggu 2 detik sebelum skenario berikutnya...\n")
                    await asyncio.sleep(2)
            
            print("=" * 70)
            print("✅ Testing WebSocket selesai!")
            print("=" * 70 + "\n")
    
    except ConnectionRefusedError:
        print("❌ Tidak bisa terhubung ke server!")
        print(f"   Pastikan server FastAPI berjalan di {WEBSOCKET_URL}")
        print(f"   Jalankan: python main.py\n")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")


if __name__ == "__main__":
    print("\n💡 Pastikan:")
    print("   1. Server FastAPI sudah berjalan (python main.py)")
    print("   2. Pasien dengan ID 1 sudah dibuat")
    print("   3. Sudah install websockets: pip install websockets\n")
    
    # Jalankan client
    asyncio.run(monitor_pasien())
