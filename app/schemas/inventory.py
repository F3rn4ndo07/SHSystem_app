# app/schemas/inventory.py
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.models.inventory_movement import MovementType

class MovementCreate(BaseModel):
    product_id: int
    branch_id: int
    movement_type: MovementType
    quantity: Decimal = Field(..., description="Cantidad positiva; la lógica aplica el signo")
    # Obligatorio para INCOME/RETURN y ajustes valorizados; opcional en otros casos
    unit_price: Optional[Decimal] = Field(
        None, description="Obligatorio para INCOME/RETURN y ajustes valorizados"
    )
    document_ref: Optional[str] = None
    notes: Optional[str] = None
    from_lima: bool = False

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v: Decimal):
        if v <= 0:
            raise ValueError("quantity debe ser > 0")
        return v


class MovementOut(BaseModel):
    id: int
    product_id: int
    branch_id: int
    movement_type: MovementType
    quantity: Decimal
    unit_price: Optional[Decimal]
    document_ref: Optional[str]
    notes: Optional[str]
    from_lima: bool
    created_at: datetime

    # v2: serializa enums por su value y permite from_attributes (ORM)
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class KardexLine(BaseModel):
    created_at: datetime
    movement_type: MovementType
    quantity: Decimal
    document_ref: Optional[str]
    user_id: Optional[int]
    notes: Optional[str]

    model_config = ConfigDict(use_enum_values=True)


class LowStockItem(BaseModel):
    product_id: int
    name: str
    category: str
    unit_of_measure: str
    current_stock: Decimal
    min_stock: Decimal
