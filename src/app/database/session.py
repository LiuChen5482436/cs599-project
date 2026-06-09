from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base
from app.utils.config import Config
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/medical_agent.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///./", "")), exist_ok=True)
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
