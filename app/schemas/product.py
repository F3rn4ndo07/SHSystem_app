from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    category: str
    unit_of_measure: Literal["UNIT", "METER", "PACK", "BOX"]
    image_url: Optional[str] = None
    min_stock: Decimal = Field(default=0)
    is_fractionable: bool = False
    price_base: Decimal

    @field_validator("min_stock")
    @classmethod
    def min_stock_non_negative(cls, v: Decimal):
        if v < 0:
            raise ValueError("min_stock debe ser >= 0")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit_of_measure: Optional[Literal["UNIT", "METER", "PACK", "BOX"]] = None
    image_url: Optional[str] = None
    min_stock: Optional[Decimal] = None
    is_fractionable: Optional[bool] = None
    price_base: Optional[Decimal] = None


class ProductOut(ProductBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True
