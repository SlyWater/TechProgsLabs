from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from internet_shop.dependencies import get_product_service
from internet_shop.main import app
from internet_shop.services.product_service import ProductService
from internet_shop.settings import Settings


class FakeQuery:
    def __init__(self, storage):
        self._storage = storage

    def all(self):
        return list(self._storage.values())


class FakeSession:
    def __init__(self, storage):
        self._storage = storage

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def query(self, _model):
        return FakeQuery(self._storage)

    def add(self, product):
        if not getattr(product, "id", None):
            product.id = str(uuid4())
        self._storage[str(product.id)] = product

    def get(self, _model, product_id):
        return self._storage.get(str(product_id))

    def delete(self, product):
        self._storage.pop(str(product.id), None)

    def commit(self):
        return None

    def refresh(self, _product):
        return None


@pytest.fixture
def test_service(tmp_path) -> ProductService:
    cache_file = tmp_path / "database.json"
    storage = {}

    def session_factory():
        return FakeSession(storage)

    return ProductService(
        session_factory=session_factory,
        settings=Settings(database_file_path=cache_file),
    )


@pytest.fixture
def client(test_service: ProductService) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_product_service] = lambda: test_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
