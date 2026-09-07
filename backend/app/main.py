from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, is_emirleri, predictions, tahminler

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


@app.get("/health")
def health():
    return {"status": "ok"}
