@echo off
REM Script untuk startup aplikasi Monitoring Kesehatan di Windows
REM Buat folder dan install dependencies jika belum ada

echo.
echo ============================================================
echo 🏥 Startup Aplikasi Monitoring Kesehatan
echo ============================================================
echo.

REM Cek apakah venv sudah ada
if exist venv (
    echo ✓ Virtual environment sudah ada
) else (
    echo ⏳ Membuat virtual environment...
    python -m venv venv
    echo ✓ Virtual environment berhasil dibuat
)

REM Activate virtual environment
echo.
echo ⏳ Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo ⏳ Menginstall dependencies...
pip install -r requirements.txt

REM Jalankan aplikasi
echo.
echo ============================================================
echo 🚀 Memulai server...
echo 📍 URL: http://localhost:8000
echo 📚 Dokumentasi: http://localhost:8000/docs
echo ============================================================
echo.

python main.py

pause
