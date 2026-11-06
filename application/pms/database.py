from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+psycopg://postgres:keepitprivate0@localhost:5432/pms_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

from .import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
