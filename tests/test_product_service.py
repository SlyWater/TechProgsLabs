from unittest.mock import Mock
from uuid import UUID, uuid4

from internet_shop.models import Product
from internet_shop.services.product_service import ProductService


def test_add_delegates_to_repository_and_returns_created_product():
    repository = Mock()
    service = ProductService(repository)
    input_product = Product(
        name="Phone",
        definition="Flagship smartphone",
        price=999.99,
        image="phone.png",
    )
    created_product = Product(
        id=str(uuid4()),
        name="Phone",
        definition="Flagship smartphone",
        price=999.99,
        image="phone.png",
    )
    repository.add.return_value = created_product

    result = service.add(input_product)

    assert result == created_product
    repository.add.assert_called_once_with(input_product)


def test_search_returns_product_by_id():
    repository = Mock()
    service = ProductService(repository)
    product_id = uuid4()
    found_product = Product(
        id=str(product_id),
        name="Laptop",
        definition="Work laptop",
        price=1500.0,
        image="laptop.png",
    )
    repository.get_by_id.return_value = found_product

    result = service.search(product_id)

    assert result == found_product
    repository.get_by_id.assert_called_once_with(product_id)


def test_search_returns_none_for_missing_product():
    repository = Mock()
    service = ProductService(repository)
    product_id = uuid4()
    repository.get_by_id.return_value = None

    result = service.search(product_id)

    assert result is None
    repository.get_by_id.assert_called_once_with(product_id)


def test_add_allows_product_without_image():
    repository = Mock()
    service = ProductService(repository)
    input_product = Product(
        name="Book",
        definition="Paper book",
        price=15.5,
        image=None,
    )
    created_product = Product(
        id=str(uuid4()),
        name="Book",
        definition="Paper book",
        price=15.5,
        image=None,
    )
    repository.add.return_value = created_product

    result = service.add(input_product)

    assert result.image is None
    repository.add.assert_called_once_with(input_product)


def test_edit_updates_existing_product():
    repository = Mock()
    service = ProductService(repository)
    updated_product = Product(
        id=str(uuid4()),
        name="Mouse Pro",
        definition="Wireless gaming mouse",
        price=35.0,
        image="mouse-pro.png",
    )
    repository.update.return_value = updated_product

    result = service.edit(updated_product)

    assert result == updated_product
    repository.update.assert_called_once_with(updated_product)


def test_edit_can_clear_image_field():
    repository = Mock()
    service = ProductService(repository)
    updated_product = Product(
        id=str(uuid4()),
        name="Headphones",
        definition="Noise cancelling",
        price=120.0,
        image=None,
    )
    repository.update.return_value = updated_product

    result = service.edit(updated_product)

    assert result.image is None
    repository.update.assert_called_once_with(updated_product)


def test_edit_raises_for_missing_product():
    repository = Mock()
    service = ProductService(repository)
    missing_product = Product(
        id=str(uuid4()),
        name="Ghost",
        definition="Missing product",
        price=1.0,
        image=None,
    )
    repository.update.side_effect = ValueError("Product not found")

    try:
        service.edit(missing_product)
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError for missing product")


def test_remove_deletes_existing_product():
    repository = Mock()
    service = ProductService(repository)
    product_id = uuid4()
    removed_product = Product(
        id=str(product_id),
        name="Keyboard",
        definition="Mechanical keyboard",
        price=80.0,
        image="keyboard.png",
    )
    repository.delete.return_value = removed_product

    result = service.remove(product_id)

    assert result == removed_product
    repository.delete.assert_called_once_with(product_id)


def test_remove_raises_for_missing_product():
    repository = Mock()
    service = ProductService(repository)
    product_id = uuid4()
    repository.delete.side_effect = ValueError("Product not found")

    try:
        service.remove(product_id)
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError for missing product")


def test_remove_twice_raises_on_second_attempt():
    repository = Mock()
    service = ProductService(repository)
    product_id = uuid4()
    removed_product = Product(
        id=str(product_id),
        name="Speaker",
        definition="Portable speaker",
        price=60.0,
        image="speaker.png",
    )
    repository.delete.side_effect = [removed_product, ValueError("Product not found")]

    first_removed = service.remove(product_id)

    assert first_removed == removed_product

    try:
        service.remove(product_id)
    except ValueError as exc:
        assert str(exc) == "Product not found"
    else:
        raise AssertionError("Expected ValueError on second remove")
