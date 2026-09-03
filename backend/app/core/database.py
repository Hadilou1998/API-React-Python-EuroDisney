from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

DATABASE_URL = settings.effective_database_url

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False,
    }

engine_kwargs = {
    "pool_pre_ping": True,
    "echo": False,
    "future": True,
}

# pool_recycle: temps de recycle de la pool de connexions (en secondes)
if not DATABASE_URL.startswith("sqlite"):
    engine_kwargs["pool_recycle"] = 280

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs,
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
)

Base = declarative_base()

# Dependency FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()