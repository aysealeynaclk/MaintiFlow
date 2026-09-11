from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import admin, auth, is_emirleri, predictions, tahminler

MODELS_DIR = Path(__file__).resolve().parents[2] / "models"

app = FastAPI(title="MaintiFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predictions.router)
app.include_router(tahminler.router)
app.include_router(is_emirleri.router)
app.include_router(admin.router)

app.mount("/gorseller", StaticFiles(directory=str(MODELS_DIR)), name="gorseller")


@app.get("/health")
def health():
    return {"status": "ok"}
