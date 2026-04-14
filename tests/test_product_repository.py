from uuid import UUID, uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from internet_shop.database import Base
from internet_shop.models import Product
from internet_shop.repositories.product_repository import ProductRepository


def create_repository(tmp_path) -> ProductRepository:
    db_file = tmp_path / "repository-test.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)
    return ProductRepository(testing_session_local)


def test_add_persists_product_in_database(tmp_path):
    repository = create_repository(tmp_path)

    created = repository.add(
        Product(
            name="Phone",
            definition="Flagship smartphone",
            price=999.99,
            image="phone.png",
        )
    )

    assert created.id is not None

    found = repository.get_by_id(UUID(created.id))
    assert found is not None
    assert found.name == "Phone"


def test_get_by_id_returns_none_for_missing_product(tmp_path):
    repository = create_repository(tmp_path)

    result = repository.get_by_id(uuid4())

    assert result is None


def test_update_changes_existing_product(tmp_path):
    repository = create_repository(tmp_path)
    created = repository.add(
        Product(
            name="Mouse",
            definition="Wireless mouse",
            price=25.0,
            image="mouse.png",
        )
    )

    updated = repository.update(
        Product(
            id=created.id,
            name="Mouse Pro",
            definition="Wireless gaming mouse",
            price=35.0,
            image=None,
        )
    )

    assert updated.name == "Mouse Pro"
    assert updated.image is None

    found = repository.get_by_id(UUID(created.id))
    assert found is not None
    assert found.name == "Mouse Pro"
    assert found.image is None


def test_update_raises_for_missing_product(tmp_path):
    repository = create_repository(tmp_path)

    try:
        repository.update(
            Product(
                id=str(uuid4()),
                name="Ghost",
                definition="Missing product",
                price=1.0,
                image=None,
            )
        )
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError for missing product")


def test_delete_removes_existing_product(tmp_path):
    repository = create_repository(tmp_path)
    created = repository.add(
        Product(
            name="Keyboard",
            definition="Mechanical keyboard",
            price=80.0,
            image="keyboard.png",
        )
    )

    removed = repository.delete(UUID(created.id))

    assert removed.id == created.id
    assert repository.get_by_id(UUID(created.id)) is None


def test_delete_raises_for_missing_product(tmp_path):
    repository = create_repository(tmp_path)

    try:
        repository.delete(uuid4())
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError for missing product")
