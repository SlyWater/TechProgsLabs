from pydantic import BaseModel
from uuid import UUID


class ProductCreate(BaseModel):
    id: str
    name: str
    definition: str
    price: float
    image: str | None = None


class ProductResponse(ProductCreate):
    id: UUID

    class Config:
        from_attributes = True
