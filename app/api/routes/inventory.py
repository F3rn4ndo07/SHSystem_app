from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.inventory import MovementCreate, MovementOut, KardexLine, LowStockItem
from app.services.inventory_services import create_movement, kardex, low_stock

router = APIRouter(prefix="/inventory", tags=["inventory"])

# Placeholder: cuando tengas JWT (Sprint 6), pon el user_id real
def get_current_user_id() -> int | None:
    return None

@router.post("/movements", response_model=MovementOut)
def create_mov(data: MovementCreate, db: Session = Depends(get_session), user_id: int | None = Depends(get_current_user_id)):
    try:
        mov = create_movement(db, data, user_id)
        return mov
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/kardex", response_model=list[KardexLine])
def get_kardex(product_id: int = Query(...), branch_id: int = Query(...), db: Session = Depends(get_session)):
    rows = kardex(db, product_id, branch_id)
    return [
        KardexLine(
            created_at=row.created_at,
            movement_type=row.movement_type,
            quantity=row.quantity,
            document_ref=row.document_ref,
            user_id=row.user_id,
            notes=row.notes,
        )
        for row in rows
    ]

@router.get("/low-stock", response_model=list[LowStockItem])
def get_low_stock(branch_id: int = Query(...), db: Session = Depends(get_session)):
    return low_stock(db, branch_id)
