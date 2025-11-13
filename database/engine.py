import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.models.base import Base

DATABASE_URL = os.getenv(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/tz_db")
)

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
	db: Session = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def init_db() -> None:
	Base.metadata.create_all(bind=engine)


__all__ = ["engine", "SessionLocal", "get_db", "init_db", "DATABASE_URL"]

