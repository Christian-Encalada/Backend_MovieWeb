from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Configuración de la URL de la base de datos con SSL
DATABASE_URL = settings.DATABASE_URL
if settings.db_host.endswith('.azure.com'):  # Si es Azure
    DATABASE_URL = f"{DATABASE_URL}?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()