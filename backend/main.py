import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from prometheus_fastapi_instrumentator import Instrumentator
from .config import get_settings
from .database import Base, engine
from .routers import delays, health, stats
from .services.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO)
settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title=settings.app_name, version="2.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["GET", "POST", "DELETE"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(delays.router)
app.include_router(stats.router)
Instrumentator().instrument(app).expose(app, include_in_schema=False)


@app.get("/", tags=["health"])
@limiter.limit("30/minute")
def root(request: Request):
    return {"service": settings.app_name, "version": "2.0.0", "status": "online"}
