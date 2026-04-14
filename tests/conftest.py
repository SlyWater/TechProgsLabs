from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from internet_shop.database import Base
from internet_shop.dependencies import get_product_service
from internet_shop.main import app
from internet_shop.repositories.product_repository import ProductRepository
from internet_shop.services.product_service import ProductService


@pytest.fixture
def test_service(tmp_path) -> ProductService:
    db_file = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    repository = ProductRepository(testing_session_local)
    return ProductService(repository)


@pytest.fixture
def client(test_service: ProductService) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_product_service] = lambda: test_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
