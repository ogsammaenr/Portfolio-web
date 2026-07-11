#!/bin/bash

# 1. Çevre değişkenlerini genişletip sistem yollarını zorla tanımlıyoruz
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# 2. Plesk hapishanesindeki hata çıktınızdan aldığımız net mutlak yola geçiş yapıyoruz
cd /httpdocs/portfolio

# 3. Eski süreci PID dosyası üzerinden kapatıyoruz (lsof gerektirmez)
if [ -f "uvicorn.pid" ]; then
  OLD_PID=$(cat uvicorn.pid)
  echo "Eski süreç sonlandırılıyor: $OLD_PID"
  kill -9 $OLD_PID 2>/dev/null
  rm uvicorn.pid
fi

# Güvenlik önlemi: Eğer pkill komutu ortamda varsa uvicorn'u her ihtimale karşı temizle
pkill -f "uvicorn" 2>/dev/null

# 4. venv kontrolü (Hata çıkarsa venv_creation.log dosyasına yazacak)
if [ ! -d "venv" ]; then
  echo "Sanal ortam oluşturuluyor..."
  python3 -m venv venv >venv_creation.log 2>&1
fi

# 5. Bağımlılıkları yükle
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 6. Uvicorn'u başlat ve Bash'in yerleşik '$!' özelliğini kullanarak PID'sini kaydet
nohup ./venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 >uvicorn.log 2>&1 &
echo $! >uvicorn.pid

echo "FastAPI başlatma komutu tetiklendi!"
