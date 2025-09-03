"""
Crea las tablas definidas en los modelos usando SQLAlchemy.
Nota: Base.metadata.create_all SOLO crea objetos que no existen.
Para cambios de esquema usa Alembic (migraciones).
"""

from app.db.base import Base
from app.db.session import engine  # Debe exponer un Engine válido

# Importa los modelos para registrarlos en el metadata
from app.models.user import User          # noqa: F401
from app.models.role import Role          # noqa: F401
from app.models.branch import Branch      # noqa: F401
from app.models.user_role import UserRole # noqa: F401
from app.models.user_branch import UserBranch  # noqa: F401


def init_models() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas/verificadas correctamente.")


if __name__ == "__main__":
    init_models()
