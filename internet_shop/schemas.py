from pydantic import BaseModel
from uuid import UUID


class ProductBase(BaseModel):
    name: str
    definition: str
    price: float
    image: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: UUID


class ProductResponse(ProductBase):
    id: UUID

    class Config:
        from_attributes = True
