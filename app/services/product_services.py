from __future__ import annotations
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.product import Product, UnitOfMeasure


def create_product(db: Session, data) -> Product:
    obj = Product(
        name=data.name,
        category=data.category,
        unit_of_measure=UnitOfMeasure(data.unit_of_measure),
        image_url=data.image_url,
        min_stock=data.min_stock,
        is_fractionable=data.is_fractionable,
        price_base=data.price_base,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_product(db: Session, product_id: int) -> Product | None:
    return db.scalar(select(Product).where(Product.id == product_id, Product.is_deleted == False))


def list_products(db: Session, q: str | None = None) -> list[Product]:
    stmt = select(Product).where(Product.is_deleted == False)
    if q:
        q_like = f"%{q}%"
        stmt = stmt.where((Product.name.ilike(q_like)) | (Product.category.ilike(q_like)))
    stmt = stmt.order_by(Product.name.asc())
    return list(db.scalars(stmt))


def update_product(db: Session, product_id: int, data) -> Product | None:
    obj = get_product(db, product_id)
    if not obj:
        return None
    for field in ["name", "category", "unit_of_measure", "image_url", "min_stock", "is_fractionable", "price_base"]:
        val = getattr(data, field, None)
        if val is not None:
            if field == "unit_of_measure":
                val = UnitOfMeasure(val)
            setattr(obj, field, val)
    db.commit()
    db.refresh(obj)
    return obj


def soft_delete_product(db: Session, product_id: int) -> bool:
    obj = get_product(db, product_id)
    if not obj:
        return False
    obj.is_deleted = True
    obj.deleted_at = datetime.utcnow()
    db.commit()
    return True
