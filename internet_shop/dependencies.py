from functools import lru_cache

from internet_shop.database import SessionLocal
from internet_shop.services.interfaces import IProductService
from internet_shop.services.product_service import ProductService
from internet_shop.settings import get_settings


@lru_cache
def get_product_service() -> IProductService:
    return ProductService(SessionLocal, get_settings())
