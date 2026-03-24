from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from internet_shop.models import Product
from internet_shop.services.interfaces import IProductService


class ProductService(IProductService):

    def __init__(self, db: Session):
        self.db = db

    def add(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def remove(self, product_id: UUID) -> Product:
        product = self.db.get(Product, str(product_id))
        if not product:
            raise ValueError("Product not found")

        self.db.delete(product)
        self.db.commit()
        return product

    def edit(self, product: Product) -> Product:
        existing_product = self.db.get(Product, product.id)
        if not existing_product:
            raise ValueError("Product not found")

        existing_product.name = product.name
        existing_product.definition = product.definition
        existing_product.price = product.price
        existing_product.image = product.image

        self.db.commit()
        self.db.refresh(existing_product)
        return existing_product

    def search(self, product_id: UUID) -> Optional[Product]:
        return self.db.get(Product, str(product_id))
