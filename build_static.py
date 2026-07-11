import os
import json
import shutil
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DIST_DIR = BASE_DIR / "dist"

def get_about_content():
    """Reads about.md and converts it to HTML."""
    about_path = DATA_DIR / "about.md"
    if about_path.exists():
        with open(about_path, "r", encoding="utf-8") as f:
            return markdown.markdown(f.read())
    return "<p>Hakkımda bilgisi henüz eklenmedi.</p>"

def get_contact_data():
    """Reads contacts.json and returns it as a dict."""
    contact_path = DATA_DIR / "contacts.json"
    if contact_path.exists():
        with open(contact_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_projects_data():
    """Reads projects.json and returns it as a list."""
    projects_path = DATA_DIR / "projects.json"
    if projects_path.exists():
        with open(projects_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_experiences_data():
    """Reads experiences.json and returns it as a list."""
    experiences_path = DATA_DIR / "experiences.json"
    if experiences_path.exists():
        with open(experiences_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_project_markdown(slug: str):
    """Reads data/projects/{slug}.md and converts it to HTML."""
    md_path = DATA_DIR / "projects" / f"{slug}.md"
    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            return markdown.markdown(f.read(), extensions=["fenced_code", "codehilite"])
    return None

def build():
    print("Starting static build...")

    # 1. Fetch all data
    about_html = get_about_content()
    contact_info = get_contact_data()
    projects_list = get_projects_data()
    experiences_list = get_experiences_data()
    pinned_projects = [p for p in projects_list if p.get("pinned") is True]

    # 2. Prepare projects data for javascript (bundling markdown content)
    projects_bundle = {}
    for project in projects_list:
        slug = project.get("slug")
        detail_html = get_project_markdown(slug)
        if not detail_html:
            detail_html = "<p>Bu projenin detaylı açıklaması henüz eklenmedi.</p>"
        
        projects_bundle[slug] = {
            "name": project.get("name"),
            "github": project.get("github"),
            "content": detail_html
        }

    # 3. Write projects_data.js to static/js/projects_data.js
    static_js_dir = STATIC_DIR / "js"
    static_js_dir.mkdir(parents=True, exist_ok=True)
    
    js_content = f"""// Auto-generated static data bundle
const PROJECTS_DATA = {json.dumps(projects_bundle, indent=4, ensure_ascii=False)};
const CONTACTS_DATA = {json.dumps(contact_info, indent=4, ensure_ascii=False)};
"""
    with open(static_js_dir / "projects_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("✓ Created static/js/projects_data.js")

    # 4. Render index.html templates using Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("index.html")
    
    rendered_html = template.render(
        about=about_html,
        contacts=contact_info,
        projects=projects_list,
        pinned_projects=pinned_projects,
        experiences=experiences_list
    )

    # 5. Make absolute paths relative in index.html to allow double clicking (file:// protocol)
    # Replace "/static/" with "static/"
    rendered_html = rendered_html.replace('href="/static/', 'href="static/')
    rendered_html = rendered_html.replace('src="/static/', 'src="static/')
    rendered_html = rendered_html.replace("url('/static/", "url('static/")
    rendered_html = rendered_html.replace('url("/static/', 'url("static/')
    # Replace project page links href="/project/slug" with href="#project-slug"
    rendered_html = rendered_html.replace('href="/project/', 'href="#project-')

    # 6. Save index.html to root directory
    with open(BASE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print("✓ Created index.html in the root directory")

    # 7. Create/Update dist directory
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copy index.html to dist/
    shutil.copy2(BASE_DIR / "index.html", DIST_DIR / "index.html")
    
    # Copy static/ to dist/static/ (remove if exists to make sure it is fresh)
    dist_static = DIST_DIR / "static"
    if dist_static.exists():
        shutil.rmtree(dist_static)
    shutil.copytree(STATIC_DIR, dist_static)
    print("✓ Copied assets to dist/ directory")

    print("\nStatic build complete! You can open 'index.html' or 'dist/index.html' directly in your browser.")

if __name__ == "__main__":
    build()
