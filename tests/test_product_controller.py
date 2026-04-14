from unittest.mock import Mock
from uuid import uuid4

from fastapi.testclient import TestClient

from internet_shop.dependencies import get_product_service
from internet_shop.main import app
from internet_shop.models import Product


def test_add_product_calls_service_add_with_mock():
    product_id = str(uuid4())
    mock_service = Mock()
    mock_service.add.return_value = Product(
        id=product_id,
        name="Phone",
        definition="Nice phone",
        price=1000.0,
        image="phone.png",
    )
    app.dependency_overrides[get_product_service] = lambda: mock_service

    with TestClient(app) as client:
        response = client.post(
            "/products/",
            json={
                "name": "Phone",
                "definition": "Nice phone",
                "price": 1000.0,
                "image": "phone.png",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    mock_service.add.assert_called_once()
    called_product = mock_service.add.call_args.args[0]
    assert called_product.name == "Phone"
    assert called_product.definition == "Nice phone"


def test_get_product_returns_stubbed_product():
    product_id = str(uuid4())
    stub_service = Mock()
    stub_service.search.return_value = Product(
        id=product_id,
        name="Tablet",
        definition="10 inch tablet",
        price=450.0,
        image="tablet.png",
    )
    app.dependency_overrides[get_product_service] = lambda: stub_service

    with TestClient(app) as client:
        response = client.get(f"/products/{product_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Tablet"


def test_get_product_returns_404_when_service_returns_none():
    product_id = str(uuid4())
    stub_service = Mock()
    stub_service.search.return_value = None
    app.dependency_overrides[get_product_service] = lambda: stub_service

    with TestClient(app) as client:
        response = client.get(f"/products/{product_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_edit_product_returns_400_when_service_raises():
    product_id = str(uuid4())
    mock_service = Mock()
    mock_service.edit.side_effect = ValueError("Product not found")
    app.dependency_overrides[get_product_service] = lambda: mock_service

    with TestClient(app) as client:
        response = client.put(
            "/products/",
            json={
                "id": product_id,
                "name": "Missing product",
                "definition": "No data",
                "price": 12.0,
                "image": None,
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found"


def test_remove_product_returns_404_when_service_raises():
    product_id = str(uuid4())
    mock_service = Mock()
    mock_service.remove.side_effect = ValueError("Product not found")
    app.dependency_overrides[get_product_service] = lambda: mock_service

    with TestClient(app) as client:
        response = client.delete(f"/products/{product_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product_returns_removed_product_body():
    product_id = str(uuid4())
    stub_service = Mock()
    stub_service.remove.return_value = Product(
        id=product_id,
        name="Console",
        definition="Game console",
        price=399.0,
        image="console.png",
    )
    app.dependency_overrides[get_product_service] = lambda: stub_service

    with TestClient(app) as client:
        response = client.delete(f"/products/{product_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Console"


def test_create_then_get_product_integration(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Monitor",
            "definition": "27 inch monitor",
            "price": 299.99,
            "image": "monitor.png",
        },
    )

    assert create_response.status_code == 200
    created_product = create_response.json()

    get_response = client.get(f"/products/{created_product['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == created_product["id"]
    assert get_response.json()["name"] == "Monitor"


def test_create_edit_then_get_product_integration(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Router",
            "definition": "Wi-Fi router",
            "price": 89.99,
            "image": "router.png",
        },
    )
    created_product = create_response.json()

    edit_response = client.put(
        "/products/",
        json={
            "id": created_product["id"],
            "name": "Router AX",
            "definition": "Wi-Fi 6 router",
            "price": 129.99,
            "image": None,
        },
    )

    assert edit_response.status_code == 200
    assert edit_response.json()["name"] == "Router AX"
    assert edit_response.json()["image"] is None

    get_response = client.get(f"/products/{created_product['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Router AX"
    assert get_response.json()["price"] == 129.99


def test_create_delete_then_get_returns_404_integration(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "SSD",
            "definition": "Fast storage",
            "price": 109.99,
            "image": "ssd.png",
        },
    )
    created_product = create_response.json()

    delete_response = client.delete(f"/products/{created_product['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == created_product["id"]

    get_response = client.get(f"/products/{created_product['id']}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Product not found"
