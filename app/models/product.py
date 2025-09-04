from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Integer, Numeric, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

if TYPE_CHECKING:
    from .inventory_movement import InventoryMovement

class UnitOfMeasure(str, enum.Enum):
    UNIT = "UNIT"
    METER = "METER"
    PACK = "PACK"
    BOX = "BOX"


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("ix_products_name", "name"),
        Index("ix_products_category", "category"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    unit_of_measure: Mapped[UnitOfMeasure] = mapped_column(Enum(UnitOfMeasure, name="unit_of_measure_enum"), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    min_stock: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    is_fractionable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    price_base: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Eliminación lógica
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # backref de movimientos
    movements: Mapped[list["InventoryMovement"]] = relationship(
        "InventoryMovement", back_populates="product", cascade="all, delete-orphan"
    )

