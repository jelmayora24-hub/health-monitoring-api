import requests
import json

BASE_URL = "http://localhost:8000"

print("🔍 Test 1: Health Check")
response = requests.get(f"{BASE_URL}/health")
print(response.json())

print("\n🔍 Test 2: Mendaftarkan Pasien Baru")
pasien_dummy = {
    "nama": "Budi Santoso",
    "usia": 45,
    "detak_jantung": 75,
    "tekanan_darah_sistol": 120,
    "tekanan_darah_diastol": 80,
    "lokasi": {"latitude": -6.2088, "longitude": 106.8456}
}
res = requests.post(f"{BASE_URL}/api/pasien", json=pasien_dummy)
print(res.json())