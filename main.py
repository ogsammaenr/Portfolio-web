import json
from pathlib import Path

import markdown
import os
import smtplib
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from email.message import EmailMessage
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Template ve Statik dosya yolları
templates = Jinja2Templates(directory="templates")
app.mount(
    "/static", StaticFiles(directory="static"), name="static"
)  # CSS eklediğinde açabilirsin

DATA_DIR = Path("data")


SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def get_about_content():
    """about.md dosyasını okur ve HTML'e çevirir."""
    about_path = DATA_DIR / "about.md"
    if about_path.exists():
        with open(about_path, "r", encoding="utf-8") as f:
            return markdown.markdown(f.read())
    return "<p>Hakkımda bilgisi henüz eklenmedi.</p>"


def get_contact_data():
    """contacts.json dosyasını sözlük olarak döner."""
    contact_path = DATA_DIR / "contacts.json"
    if contact_path.exists():
        with open(contact_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_projects_data():
    """projects.json dosyasini liste olarak döner."""
    projects_path = DATA_DIR / "projects.json"
    if projects_path.exists():
        with open(projects_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_experiences_data():
    """experiences.json dosyasını liste olarak döner."""
    experiences_path = DATA_DIR / "experiences.json"
    if experiences_path.exists():
        with open(experiences_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_project_by_slug(slug: str):
    """projects.json içinden slug'a göre projeyi bulur."""
    projects = get_projects_data()
    for project in projects:
        if project.get("slug") == slug:
            return project
    return None


def get_project_markdown(slug: str):
    """data/projects/{slug}.md dosyasını okur ve HTML'e çevirir."""
    md_path = DATA_DIR / "projects" / f"{slug}.md"
    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            return markdown.markdown(f.read(), extensions=["fenced_code", "codehilite"])
    return None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    about_html = get_about_content()
    contact_info = get_contact_data()
    projects_list = get_projects_data()
    experiences_list = get_experiences_data()

    pinned_projects = [p for p in projects_list if p.get("pinned") is True]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "about": about_html,
            "contacts": contact_info,
            "projects": projects_list,
            "pinned_projects": pinned_projects,
            "experiences": experiences_list,
        },
    )


# --- API: PROJE DETAYLARINI MODAL İÇİN JSON OLARAK VER ---
@app.get("/api/project/{slug}")
async def api_project_detail(slug: str):
    project = get_project_by_slug(slug)
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")

    detail_html = get_project_markdown(slug)
    if not detail_html:
        detail_html = "<p>Bu projenin detaylı açıklaması henüz eklenmedi.</p>"

    return {
        "name": project.get("name"),
        "github": project.get("github"),
        "content": detail_html,
    }


@app.post("/send-message")
async def send_message(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    system_bot_check: str = Form(default=""),  # YENİ: Gizli Honeypot Alanı
):
    # 1. ANTI-SPAM (HONEYPOT) KONTROLÜ
    # Botlar CSS okuyamaz, gizli olan bu alanı görüp doldururlar.
    # Eğer bu alan boş değilse, bu kesinlikle bir bottur.
    if system_bot_check != "":
        print(f"[GÜVENLİK UYARISI] Spam bot engellendi. Hedef: {email}")
        # Bota başarılı olmuş gibi davranıp sayfaya geri yolluyoruz (Tersine Mühendislik)
        return RedirectResponse(url="/#contact", status_code=303)

    # 2. E-POSTA PAKETİNİ HAZIRLAMA (Bloat-free, standart kütüphane)
    msg = EmailMessage()
    msg["Subject"] = f"[Portfolyo Sistem Mesajı] {subject}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    # Mesajın içeriği
    body = f"""
    Sistem üzerinden yeni bir iletişim protokolü başlatıldı.

    [GÖNDEREN BİLGİLERİ]
    Alias / İsim: {name}
    Geri Dönüş Adresi: {email}
    
    [SİSTEM MESAJI]
    {message}
    """
    msg.set_content(body)

    # 3. SMTP SUNUCUSUNA BAĞLANIP İLETİMİ GERÇEKLEŞTİRME
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("[BAŞARILI] Sistem mesajı iletildi.")

    except Exception as e:
        print(f"[HATA] İletim başarısız: {e}")
        # İstersen burada bir hata sayfasına yönlendirme yapabilirsin

    # 4. PRG (Post-Redirect-Get) MİMARİSİ
    return RedirectResponse(url="/?status=success#contact", status_code=303)
