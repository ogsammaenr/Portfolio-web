import json
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Template ve Statik dosya yolları
templates = Jinja2Templates(directory="templates")
app.mount(
    "/static", StaticFiles(directory="static"), name="static"
)  # CSS eklediğinde açabilirsin

DATA_DIR = Path("data")


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

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "about": about_html,
            "contacts": contact_info,
            "projects": projects_list,
            "experiences": experiences_list,
        },
    )


@app.get("/project/{slug}", response_class=HTMLResponse)
async def project_detail(request: Request, slug: str):
    project = get_project_by_slug(slug)

    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")

    detail_html = get_project_markdown(slug)

    if not detail_html:
        # Eğer JSON'da var ama .md dosyası henüz yoksa bir uyarı gösterelim
        detail_html = "<p>Bu projenin detaylı açıklaması henüz eklenmedi.</p>"

    return templates.TemplateResponse(
        request=request,
        name="project_detail.html",
        context={"project": project, "content": detail_html},
    )
