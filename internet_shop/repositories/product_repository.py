from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from internet_shop.models import Product


class ProductRepository:
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def add(self, product: Product) -> Product:
        with self._session_factory() as db:
            db_product = Product(
                name=product.name,
                definition=product.definition,
                price=product.price,
                image=product.image,
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        with self._session_factory() as db:
            return db.get(Product, str(product_id))

    def update(self, product: Product) -> Product:
        with self._session_factory() as db:
            existing_product = db.get(Product, str(product.id))
            if not existing_product:
                raise ValueError("Product not found")

            existing_product.name = product.name
            existing_product.definition = product.definition
            existing_product.price = product.price
            existing_product.image = product.image

            db.commit()
            db.refresh(existing_product)
            return existing_product

    def delete(self, product_id: UUID) -> Product:
        with self._session_factory() as db:
            product = db.get(Product, str(product_id))
            if not product:
                raise ValueError("Product not found")

            removed_product = Product(
                id=product.id,
                name=product.name,
                definition=product.definition,
                price=product.price,
                image=product.image,
            )
            db.delete(product)
            db.commit()
            return removed_product
