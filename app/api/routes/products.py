from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services.product_services import create_product, list_products, get_product, update_product, soft_delete_product

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductOut)
def create(data: ProductCreate, db: Session = Depends(get_session)):
    return create_product(db, data)

@router.get("", response_model=list[ProductOut])
def list_all(q: str | None = Query(default=None), db: Session = Depends(get_session)):
    return list_products(db, q)

@router.get("/{product_id}", response_model=ProductOut)
def get_one(product_id: int, db: Session = Depends(get_session)):
    obj = get_product(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return obj

@router.patch("/{product_id}", response_model=ProductOut)
def update(product_id: int, data: ProductUpdate, db: Session = Depends(get_session)):
    obj = update_product(db, product_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return obj

@router.delete("/{product_id}")
def delete_soft(product_id: int, db: Session = Depends(get_session)):
    ok = soft_delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"status": "ok"}
