from __future__ import annotations
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Optional, cast
from app.models.inventory_movement import InventoryMovement, MovementType
from app.models.product import Product
from app.schemas.inventory import MovementCreate, LowStockItem


def _check_fractionable(product: Product, qty: Decimal) -> None:
    if not product.is_fractionable and qty != qty.to_integral():
        raise ValueError("El producto no es fraccionable; la cantidad debe ser entera.")


def _signed_qty(movement_type: MovementType, qty: Decimal) -> Decimal:
    if movement_type in (MovementType.INCOME, MovementType.RETURN):
        return qty
    if movement_type in (MovementType.SALE, MovementType.WASTE):
        return -qty
    return qty  # ADJUSTMENT (puede ser + o - según lo que envíes)


def create_movement(db: Session, data: MovementCreate, performed_by_user_id: int | None) -> InventoryMovement:
    product: Optional[Product] = db.get(Product, data.product_id)
    if not product or product.is_deleted:
        raise ValueError("Producto no encontrado o eliminado.")

    _check_fractionable(cast(Product, product), data.quantity)

    mt = MovementType(data.movement_type)

    # Reglas de obligatoriedad de unit_price
    if mt in (MovementType.INCOME, MovementType.RETURN) and data.unit_price is None:
        raise ValueError("unit_price es obligatorio para INCOME/RETURN.")
    # Para ADJUSTMENT/WASTE/Sale puedes decidir si exigir valorización; de momento lo dejamos opcional.

    movement = InventoryMovement(
        product_id=data.product_id,
        branch_id=data.branch_id,
        user_id=performed_by_user_id,
        movement_type=mt,
        quantity=_signed_qty(mt,data.quantity),
        unit_price=data.unit_price,
        document_ref=data.document_ref,
        notes=data.notes,
        from_lima=bool(data.from_lima),
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def current_stock(db: Session, product_id: int, branch_id: int) -> Decimal:
    stmt = (
        select(func.coalesce(func.sum(InventoryMovement.quantity), 0))
        .where(InventoryMovement.product_id == product_id, InventoryMovement.branch_id == branch_id)
    )
    return Decimal(db.scalar(stmt))


def kardex(db: Session, product_id: int, branch_id: int) -> list[InventoryMovement]:
    stmt = (
        select(InventoryMovement)
        .where(InventoryMovement.product_id == product_id, InventoryMovement.branch_id == branch_id)
        .order_by(InventoryMovement.created_at.asc(), InventoryMovement.id.asc())
    )
    return list(db.scalars(stmt))


def low_stock(db: Session, branch_id: int) -> list[LowStockItem]:
    qty_sum = func.coalesce(func.sum(InventoryMovement.quantity), 0)
    stmt = (
        select(
            Product.id.label("product_id"),
            Product.name,
            Product.category,
            Product.unit_of_measure,
            Product.min_stock,
            qty_sum.label("current_stock"),
        )
        .join(InventoryMovement, InventoryMovement.product_id == Product.id, isouter=True)
        .where(Product.is_deleted == False)
        .where((InventoryMovement.branch_id == branch_id) | (InventoryMovement.branch_id.is_(None)))
        .group_by(Product.id, Product.name, Product.category, Product.unit_of_measure, Product.min_stock)
        .having(qty_sum < Product.min_stock)
        .order_by((qty_sum - Product.min_stock).asc())
    )
    rows = db.execute(stmt).all()
    return [
        LowStockItem(
            product_id=r.product_id,
            name=r.name,
            category=r.category,
            unit_of_measure=str(r.unit_of_measure),
            current_stock=r.current_stock,
            min_stock=r.min_stock,
        )
        for r in rows
    ]
