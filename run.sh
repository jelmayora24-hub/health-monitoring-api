#!/bin/bash
# Script untuk startup aplikasi Monitoring Kesehatan di Linux/Mac
# Buat folder dan install dependencies jika belum ada

echo ""
echo "============================================================"
echo "🏥 Startup Aplikasi Monitoring Kesehatan"
echo "============================================================"
echo ""

# Cek apakah venv sudah ada
if [ -d "venv" ]; then
    echo "✓ Virtual environment sudah ada"
else
    echo "⏳ Membuat virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment berhasil dibuat"
fi

# Activate virtual environment
echo ""
echo "⏳ Mengaktifkan virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "⏳ Menginstall dependencies..."
pip install -r requirements.txt

# Jalankan aplikasi
echo ""
echo "============================================================"
echo "🚀 Memulai server..."
echo "📍 URL: http://localhost:8000"
echo "📚 Dokumentasi: http://localhost:8000/docs"
echo "============================================================"
echo ""

python main.py
