#!/bin/bash

# Scriptin çalıştığı klasörü (proje dizinini) otomatik bul
cd "$(dirname "$0")"

# venv yoksa oluştur
[ -d "venv" ] || python3 -m venv venv 2>/dev/null || /usr/bin/python3 -m venv venv 2>/dev/null

# Bağımlılıkları güncelle
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Port 8000'deki eski uvicorn'u temizle
lsof -t -i:8000 | xargs kill -9 2>/dev/null || true

# Uvicorn'u başlat
./venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 >uvicorn.log 2>&1
