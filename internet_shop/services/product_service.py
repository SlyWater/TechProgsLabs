import json
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from internet_shop.models import Product
from internet_shop.services.interfaces import IProductService
from internet_shop.settings import Settings


class ProductService(IProductService):

    def __init__(self, session_factory: Callable[[], Session], settings: Settings):
        self._session_factory = session_factory
        self._settings = settings
        self._file_path = Path(settings.database_file_path)
        self._lock = Lock()
        self._products: dict[str, dict[str, Any]] = {}
        self._init_from_file()

    def _serialize_product(self, product: Product) -> dict[str, Any]:
        return {
            "id": str(product.id),
            "name": product.name,
            "definition": product.definition,
            "price": product.price,
            "image": product.image,
        }

    def _product_from_data(self, data: dict[str, Any]) -> Product:
        return Product(**data)

    def _load_cache_from_db(self) -> None:
        with self._session_factory() as db:
            products = db.query(Product).all()
            self._products = {
                str(product.id): self._serialize_product(product) for product in products
            }

    def _init_from_file(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self._file_path.exists() or not self._file_path.read_text(encoding="utf-8").strip():
            self._load_cache_from_db()
            self._write_to_file()
            return

        try:
            file_data = json.loads(self._file_path.read_text(encoding="utf-8"))
            self._products = {
                str(product_id): product_data
                for product_id, product_data in file_data.items()
            }
        except (json.JSONDecodeError, OSError):
            self._load_cache_from_db()
            self._write_to_file()

    def _write_to_file(self) -> None:
        self._file_path.write_text(
            json.dumps(self._products, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add(self, product: Product) -> Product:
        with self._lock:
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

                self._products[str(db_product.id)] = self._serialize_product(db_product)
                self._write_to_file()
                return db_product

    def remove(self, product_id: UUID) -> Product:
        with self._lock:
            with self._session_factory() as db:
                product = db.get(Product, str(product_id))
                if not product:
                    raise ValueError("Product not found")

                removed_product = self._serialize_product(product)
                db.delete(product)
                db.commit()

                self._products.pop(str(product_id), None)
                self._write_to_file()
                return self._product_from_data(removed_product)

    def edit(self, product: Product) -> Product:
        with self._lock:
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

                self._products[str(existing_product.id)] = self._serialize_product(
                    existing_product
                )
                self._write_to_file()
                return existing_product

    def search(self, product_id: UUID) -> Optional[Product]:
        cached_product = self._products.get(str(product_id))
        if cached_product:
            return self._product_from_data(cached_product)

        with self._session_factory() as db:
            product = db.get(Product, str(product_id))
            if product:
                self._products[str(product.id)] = self._serialize_product(product)
            return product
