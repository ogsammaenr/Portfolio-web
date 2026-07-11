import os
import requests

# FastAPI yerelde hangi portta çalışıyorsa
BASE_URL = "http://127.0.0.1:3030"

# Sitenizdeki tüm rotaları (sayfaları) buraya yazın
PAGES = {
    "/": "index.html",
    "/about": "about.html",
    "/projects": "projects.html",
    # Varsa diğer sayfalarınız...
}

DIST_DIR = "dist"
os.makedirs(DIST_DIR, exist_ok=True)

print("Statik sayfalar oluşturuluyor...")

for route, filename in PAGES.items():
    response = requests.get(f"{BASE_URL}{route}")
    if response.status_code == 200:
        # Varsa static klasör yollarını düzeltmek için küçük bir replace (isteğe bağlı)
        content = response.text

        with open(os.path.join(DIST_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ {route} -> {DIST_DIR}/{filename}")
    else:
        print(f"✗ {route} yüklenirken hata oluştu: {response.status_code}")

print("İşlem tamamlandı! 'dist' klasörünü Plesk'e yükleyebilirsiniz.")
