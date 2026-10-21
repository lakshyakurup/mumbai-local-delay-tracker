import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from backend.config import settings
from backend.database import engine, Base
from backend.middleware import LoggingMiddleware, limiter, RateLimitExceeded, _rate_limit_exceeded_handler
from backend.routers import delays
from backend.services.scheduler import start_scheduler

logging.basicConfig(level=settings.log_level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

app = FastAPI(
    title="Mumbai Local Train Delay Tracker API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(delays.router)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    start_scheduler()

@app.get("/health", tags=["System"])
def health_check():
    from sqlalchemy import text
    from backend.database import SessionLocal
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    finally:
        db.close()
        
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/metrics", include_in_schema=False, tags=["System"])
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
