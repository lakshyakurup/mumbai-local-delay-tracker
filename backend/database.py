from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

_is_sqlite = settings.database_url.startswith("sqlite")

_connect_args = {}
if not _is_sqlite:
    _connect_args["sslmode"] = "require"

_engine_kwargs = {
    "connect_args": _connect_args,
}
if not _is_sqlite:
    _engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    })

engine = create_engine(
    settings.database_url,
    **_engine_kwargs,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
