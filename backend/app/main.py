from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import detect, cameras, violations, stats, ws

app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time computer-vision system that detects missing PPE "
                 "(hard hats, safety vests, masks) on live camera feeds and "
                 "logs/alerts on violations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.mount("/snapshots", StaticFiles(directory=str(settings.VIOLATION_SNAPSHOTS_DIR)), name="snapshots")

app.include_router(detect.router)
app.include_router(cameras.router)
app.include_router(violations.router)
app.include_router(stats.router)
app.include_router(ws.router)


@app.get("/")
def root():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/health")
def health():
    return {"status": "healthy"}
