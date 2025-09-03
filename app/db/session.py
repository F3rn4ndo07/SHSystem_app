from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connection import DATABASE_URL

# Engine para SQLAlchemy 2.x
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    future=True,
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)

def get_session():
    """
    Dependency-style generator:
    with SessionLocal() as session:
        yield session
    """
    with SessionLocal() as session:
        yield session
