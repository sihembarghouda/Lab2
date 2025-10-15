# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# Pour tests locaux simples on utilise SQLite. Si tu veux PostgreSQL, change l'URL.
DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # nécessaire pour SQLite + threads
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()
