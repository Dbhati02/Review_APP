from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from loguru import logger

# Ensure DATABASE_URL exists
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is missing in .env file")

try:
    engine = create_engine(settings.DATABASE_URL, future=True)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base = declarative_base()
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Database init error: {e}")
    raise
