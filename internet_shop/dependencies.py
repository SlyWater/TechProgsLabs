from functools import lru_cache

from internet_shop.database import SessionLocal
from internet_shop.repositories.product_repository import ProductRepository
from internet_shop.services.interfaces import IProductService
from internet_shop.services.product_service import ProductService


@lru_cache
def get_product_repository() -> ProductRepository:
    return ProductRepository(SessionLocal)


def get_product_service() -> IProductService:
    return ProductService(get_product_repository())
