from app.db.base import Base
from app.db.session import engine
import app.models

def init_models() -> None:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas correctamente.")

if __name__ == "__main__":
    init_models()
