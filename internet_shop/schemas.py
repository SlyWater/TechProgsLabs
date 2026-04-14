from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
