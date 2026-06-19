from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.paths import get_static_dir, get_templates_dir
from app.routers import tasks

TEMPLATES_DIR = get_templates_dir()
STATIC_DIR = get_static_dir()

app = FastAPI(title="Backend Journey Task Tracker")
app.include_router(tasks.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(TEMPLATES_DIR / "index.html")
