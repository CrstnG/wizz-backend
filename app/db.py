from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency que provee una sesión de base de datos por request.
    Se asegura de cerrar la sesión aunque ocurra un error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
