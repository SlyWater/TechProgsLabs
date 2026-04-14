import json
from uuid import UUID, uuid4

from internet_shop.models import Product


def test_add_creates_product_in_db_and_cache_file(test_service):
    product = Product(
        name="Phone",
        definition="Flagship smartphone",
        price=999.99,
        image="phone.png",
    )

    created = test_service.add(product)

    assert created.id is not None
    assert created.name == "Phone"

    cache_data = json.loads(test_service._file_path.read_text(encoding="utf-8"))
    assert str(created.id) in cache_data
    assert cache_data[str(created.id)]["definition"] == "Flagship smartphone"


def test_search_returns_product_by_id(test_service):
    created = test_service.add(
        Product(
            name="Laptop",
            definition="Work laptop",
            price=1500.0,
            image="laptop.png",
        )
    )

    found = test_service.search(UUID(created.id))

    assert found is not None
    assert found.id == created.id
    assert found.name == "Laptop"


def test_search_returns_none_for_missing_product(test_service):
    result = test_service.search(uuid4())

    assert result is None


def test_add_allows_product_without_image(test_service):
    created = test_service.add(
        Product(
            name="Book",
            definition="Paper book",
            price=15.5,
            image=None,
        )
    )

    assert created.image is None

    cache_data = json.loads(test_service._file_path.read_text(encoding="utf-8"))
    assert cache_data[str(created.id)]["image"] is None


def test_search_returns_cached_product_without_db_lookup(test_service):
    created = test_service.add(
        Product(
            name="Camera",
            definition="Compact camera",
            price=500.0,
            image="camera.png",
        )
    )

    test_service._products[str(created.id)]["name"] = "Camera from cache"

    found = test_service.search(UUID(created.id))

    assert found is not None
    assert found.name == "Camera from cache"


def test_edit_updates_existing_product(test_service):
    created = test_service.add(
        Product(
            name="Mouse",
            definition="Wireless mouse",
            price=25.0,
            image="mouse.png",
        )
    )

    updated_product = Product(
        id=created.id,
        name="Mouse Pro",
        definition="Wireless gaming mouse",
        price=35.0,
        image="mouse-pro.png",
    )

    updated = test_service.edit(updated_product)

    assert updated.id == created.id
    assert updated.name == "Mouse Pro"
    assert updated.price == 35.0

    cache_data = json.loads(test_service._file_path.read_text(encoding="utf-8"))
    assert cache_data[str(created.id)]["name"] == "Mouse Pro"


def test_edit_can_clear_image_field(test_service):
    created = test_service.add(
        Product(
            name="Headphones",
            definition="Noise cancelling",
            price=120.0,
            image="headphones.png",
        )
    )

    updated = test_service.edit(
        Product(
            id=created.id,
            name="Headphones",
            definition="Noise cancelling",
            price=120.0,
            image=None,
        )
    )

    assert updated.image is None

    cache_data = json.loads(test_service._file_path.read_text(encoding="utf-8"))
    assert cache_data[str(created.id)]["image"] is None


def test_edit_raises_for_missing_product(test_service):
    missing_product = Product(
        id=str(uuid4()),
        name="Ghost",
        definition="Missing product",
        price=1.0,
        image=None,
    )

    try:
        test_service.edit(missing_product)
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError for missing product")


def test_remove_deletes_existing_product(test_service):
    created = test_service.add(
        Product(
            name="Keyboard",
            definition="Mechanical keyboard",
            price=80.0,
            image="keyboard.png",
        )
    )

    removed = test_service.remove(UUID(created.id))

    assert removed.id == created.id
    assert removed.name == "Keyboard"
    assert test_service.search(UUID(created.id)) is None

    cache_data = json.loads(test_service._file_path.read_text(encoding="utf-8"))
    assert str(created.id) not in cache_data


def test_remove_raises_for_missing_product(test_service):
    try:
        test_service.remove(uuid4())
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError for missing product")


def test_remove_twice_raises_on_second_attempt(test_service):
    created = test_service.add(
        Product(
            name="Speaker",
            definition="Portable speaker",
            price=60.0,
            image="speaker.png",
        )
    )

    first_removed = test_service.remove(UUID(created.id))

    assert first_removed.id == created.id

    try:
        test_service.remove(UUID(created.id))
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError on second remove")
