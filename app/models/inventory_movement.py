from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, Numeric, Enum, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

if TYPE_CHECKING:
    from .product import Product
    from .branch import Branch
    from .user import User

class MovementType(str, enum.Enum):
    INCOME = "INCOME"         # Ingreso (unit_price = costo unitario)
    SALE = "SALE"             # Venta  (unit_price = precio unitario efectivo de venta)
    ADJUSTMENT = "ADJUSTMENT" # Ajuste (+ o -)
    WASTE = "WASTE"           # Merma  (-)
    RETURN = "RETURN"         # Devolución (+)


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    __table_args__ = (
        Index("ix_movements_product_branch_date", "product_id", "branch_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType, name="movement_type_enum"), nullable=False)
    # Cantidad se guarda ya con signo según el tipo de movimiento
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    # Semántica:
    #  - INCOME/RETURN/ADJUSTMENT+: costo unitario (para valuación)
    #  - SALE: precio unitario efectivo de venta
    #  - WASTE/ADJUSTMENT-: costo promedio (si decides valorarlo)
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    document_ref: Mapped[str | None] = mapped_column(String(60), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Requerimiento: marcar ingresos desde Lima
    from_lima: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="movements")
    branch: Mapped["Branch"] = relationship("Branch")
    user: Mapped["User"] = relationship("User")

