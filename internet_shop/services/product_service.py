from threading import Lock
from typing import Optional
from uuid import UUID

from internet_shop.models import Product
from internet_shop.repositories.product_repository import ProductRepository
from internet_shop.services.interfaces import IProductService


class ProductService(IProductService):

    def __init__(self, repository: ProductRepository):
        self._repository = repository
        self._lock = Lock()

    def add(self, product: Product) -> Product:
        with self._lock:
            return self._repository.add(product)

    def remove(self, product_id: UUID) -> Product:
        with self._lock:
            return self._repository.delete(product_id)

    def edit(self, product: Product) -> Product:
        with self._lock:
            return self._repository.update(product)

    def search(self, product_id: UUID) -> Optional[Product]:
        return self._repository.get_by_id(product_id)
