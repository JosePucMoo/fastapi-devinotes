import os
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

url = os.environ["DATABASE_URL"]

if url:
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

#engine = create_engine(settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})

engine = create_engine(url, pool_pre_ping=True)

def init_db() -> None:
    if settings.ENVIRONMENT == "DEV":
        SQLModel.metadata.create_all(engine) #unicamente para desarrollo, crea automaticamente las tablas de la base de datos
        
    
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session