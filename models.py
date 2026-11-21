"""
Models dan schema data untuk aplikasi monitoring kesehatan
Menggunakan Pydantic untuk validasi data
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Lokasi(BaseModel):
    """Model untuk data lokasi pasien"""
    latitude: float = Field(..., description="Latitude lokasi pasien")
    longitude: float = Field(..., description="Longitude lokasi pasien")


class PasienCreate(BaseModel):
    """Model untuk membuat data pasien baru"""
    nama: str = Field(..., min_length=1, description="Nama pasien")
    usia: int = Field(..., ge=1, le=150, description="Usia pasien dalam tahun")
    detak_jantung: int = Field(..., ge=0, description="Detak jantung dalam bpm")
    tekanan_darah_sistol: int = Field(..., description="Tekanan darah sistol (angka atas)")
    tekanan_darah_diastol: int = Field(..., description="Tekanan darah diastol (angka bawah)")
    lokasi: Lokasi = Field(..., description="Lokasi pasien")


class Pasien(BaseModel):
    """Model untuk data pasien lengkap"""
    id: int
    nama: str
    usia: int
    detak_jantung: int
    tekanan_darah_sistol: int
    tekanan_darah_diastol: int
    lokasi_latitude: float
    lokasi_longitude: float
    status: str
    dibuat_pada: datetime
    diperbarui_pada: datetime

    class Config:
        from_attributes = True


class DataMonitoring(BaseModel):
    """Model untuk data monitoring pasien"""
    id: int
    pasien_id: int
    detak_jantung: int
    tekanan_darah_sistol: int
    tekanan_darah_diastol: int
    lokasi_latitude: float
    lokasi_longitude: float
    status: str
    ada_alarm: bool
    timestamp: datetime

    class Config:
        from_attributes = True


class UpdateMonitoring(BaseModel):
    """Model untuk update data monitoring real-time"""
    detak_jantung: int = Field(..., ge=0, description="Detak jantung dalam bpm")
    tekanan_darah_sistol: int = Field(..., description="Tekanan darah sistol")
    tekanan_darah_diastol: int = Field(..., description="Tekanan darah diastol")
    lokasi: Lokasi = Field(..., description="Lokasi pasien saat ini")


class Alarm(BaseModel):
    """Model untuk sistem alarm"""
    id: int
    pasien_id: int
    tipe_alarm: str
    nilai_detak: int
    lokasi_latitude: float
    lokasi_longitude: float
    pesan: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ResponseAPI(BaseModel):
    """Model response standar API"""
    status: str = Field(..., description="Status: NORMAL/WASPADA/BAHAYA")
    pesan: str = Field(..., description="Pesan keterangan")
    data: Optional[dict] = Field(default=None, description="Data response")
    timestamp: datetime = Field(default_factory=datetime.now, description="Waktu response")
    alarm: bool = Field(default=False, description="Ada alarm atau tidak")
