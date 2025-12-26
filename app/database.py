from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

Base = declarative_base()

_engine = None
_SessionLocal = None


def get_database_url():
    # Streamlit Cloud uses secrets, local dev can use env vars
    return (
        os.getenv("DATABASE_URL")
    )


def get_engine():
    global _engine
    if _engine is None:
        db_url = get_database_url()
        if not db_url:
            raise RuntimeError("DATABASE_URL is not set")
        _engine = create_engine(db_url, pool_pre_ping=True)
    return _engine


def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )
    return _SessionLocal()