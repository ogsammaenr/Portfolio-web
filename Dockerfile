# Olabildiğince hafif ve gereksiz paketlerden arındırılmış slim imajını kullanıyoruz
FROM python:3.11-slim

# Konteyner içindeki çalışma dizinini belirliyoruz
WORKDIR /app

# Docker'ın katman (layer) önbelleğinden faydalanmak için önce sadece requirements dosyasını kopyalıyoruz
COPY requirements.txt .

# Bağımlılıkları kurarken gereksiz önbellek dosyalarının tutulmasını engelliyoruz
RUN pip install --no-cache-dir -r requirements.txt

# data, static, templates klasörleri ve main.py dahil tüm dosyaları kopyalıyoruz
COPY . .

# Konteynerin dışarıya açacağı portu belirtiyoruz
EXPOSE 8000

# Uygulamayı Uvicorn ile başlatıyoruz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
