from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routers import tasks


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Backend Journey Task Tracker")
app.include_router(tasks.router)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(BASE_DIR / "templates" / "index.html")
