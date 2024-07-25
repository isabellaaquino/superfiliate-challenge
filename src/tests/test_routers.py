from fastapi.testclient import TestClient
import pytest

from schemas.config.rules import CollectionDiscountConfig

# PRO: Unit tests with different scenarios.
# Maybe one improvement here would be adding more edge-cases to the test suite,
# something like a list with 100 items, etc.

def override_config_discount():
    data = {
        "discount_rule": {"min_qty": 2, "discount_percentage": 10},
        "excluded_collections": ["KETO"],
    }
    return CollectionDiscountConfig(**data)


def override_config_min_qty():
    data = {
        "discount_rule": {"min_qty": 3, "discount_percentage": 5.0},
        "excluded_collections": ["KETO"],
    }
    return CollectionDiscountConfig(**data)


def override_config_excluded_collection():
    data = {
        "discount_rule": {"min_qty": 2, "discount_percentage": 5.0},
        "excluded_collections": ["BEST-SELLERS"],
    }
    return CollectionDiscountConfig(**data)


def test_checkout_cart_happy_path_default_settings(client: TestClient):
    cart_data = {
        "cart": {
            "reference": "2d832fe0-6c96-4515-9be7-4c00983539c1",
            "lineItems": [
                {
                    "name": "Peanut Butter",
                    "price": "39.0",
                    "collection": "BEST-SELLERS",
                },
                {"name": "Banana Cake", "price": "34.99", "collection": "DEFAULT"},
                {"name": "Cocoa", "price": "34.99", "collection": "KETO"},
                {"name": "Fruity", "price": "32", "collection": "DEFAULT"},
            ],
        }
    }
    expected_final_price = 130.38
    expected_items_list = [
        {"name": "Peanut Butter", "collection": "BEST-SELLERS", "price": 35.1},
        {"name": "Banana Cake", "collection": "DEFAULT", "price": 31.49},
        {"name": "Fruity", "collection": "DEFAULT", "price": 28.8},
        {
            "name": "Cocoa",
            "collection": "KETO",  # KETO MAINTAINS INITIAL PRICE SINCE IT IS FROM AN EXCLUDED COLLECTION
            "price": 34.99,
        },
    ]
    response = client.post("/cart/checkout", json=cart_data)
    assert response.status_code == 200
    data = response.json()["cart"]
    assert data["price"] == expected_final_price
    assert data["items"] == expected_items_list


def test_checkout_cart_all_excluded(client: TestClient):
    cart_data = {
        "cart": {
            "reference": "2d832fe0-6c96-4515-9be7-4c00983539c1",
            "lineItems": [
                {
                    "name": "Peanut Butter",
                    "price": "39.0",
                    "collection": "KETO",
                },
                {"name": "Banana Cake", "price": "34.99", "collection": "KETO"},
                {"name": "Cocoa", "price": "34.99", "collection": "KETO"},
                {"name": "Fruity", "price": "32", "collection": "KETO"},
            ],
        }
    }
    expected_final_price = 140.98  # 39 + 34.99 + 34.99 + 32
    expected_items_list = [
        {
            "name": "Peanut Butter",
            "price": 39.0,
            "collection": "KETO",
        },
        {"name": "Banana Cake", "price": 34.99, "collection": "KETO"},
        {"name": "Cocoa", "price": 34.99, "collection": "KETO"},
        {"name": "Fruity", "price": 32.0, "collection": "KETO"},
    ]
    response = client.post("/cart/checkout", json=cart_data)
    assert response.status_code == 200
    data = response.json()["cart"]
    assert data["price"] == expected_final_price
    assert data["items"] == expected_items_list


@pytest.mark.parametrize(
    "client", [{"get_config": override_config_discount}], indirect=True
)
def test_checkout_cart_with_bigger_discount(client: TestClient):
    # Progressive discount = 10, min_qty = 2.
    # Discount will be applied to every box BUT KETO
    # Discount = 20% (10 + 10, since there are 3 valid boxes)
    cart_data = {
        "cart": {
            "reference": "2d832fe0-6c96-4515-9be7-4c00983539c1",
            "lineItems": [
                {
                    "name": "Peanut Butter",
                    "price": "39.0",
                    "collection": "BEST-SELLERS",
                },
                {"name": "Banana Cake", "price": "34.99", "collection": "DEFAULT"},
                {"name": "Cocoa", "price": "34.99", "collection": "KETO"},
                {"name": "Fruity", "price": "32", "collection": "DEFAULT"},
            ],
        }
    }
    expected_final_price = 119.78  # (39.0 + 34.99 + 32) * 0.8 + 34.99
    expected_items_list = [
        {
            "name": "Peanut Butter",
            "price": 31.2,
            "collection": "BEST-SELLERS",
        },
        {"name": "Banana Cake", "price": 27.99, "collection": "DEFAULT"},
        {"name": "Fruity", "price": 25.6, "collection": "DEFAULT"},
        {"name": "Cocoa", "price": 34.99, "collection": "KETO"},
    ]
    response = client.post("/cart/checkout", json=cart_data)
    assert response.status_code == 200
    data = response.json()["cart"]
    assert data["price"] == expected_final_price
    assert data["items"] == expected_items_list


@pytest.mark.parametrize(
    "client", [{"get_config": override_config_min_qty}], indirect=True
)
def test_checkout_cart_with_bigger_min_qt(client: TestClient):
    # Progressive discount = 10, min_qty = 3.
    # Discount will be applied to every box BUT KETO
    # Discount = 5% (since min_qty = 3, discount will only start counting from the third valid box)
    cart_data = {
        "cart": {
            "reference": "2d832fe0-6c96-4515-9be7-4c00983539c1",
            "lineItems": [
                {
                    "name": "Peanut Butter",
                    "price": "39.0",
                    "collection": "BEST-SELLERS",
                },
                {"name": "Banana Cake", "price": "34.99", "collection": "DEFAULT"},
                {"name": "Cocoa", "price": "34.99", "collection": "KETO"},
                {"name": "Fruity", "price": "32", "collection": "DEFAULT"},
            ],
        }
    }
    expected_final_price = 135.68  # (39.0 + 34.99 + 32) * 0.95 + 34.99
    expected_items_list = [
        {
            "name": "Peanut Butter",
            "price": 37.05,
            "collection": "BEST-SELLERS",
        },
        {"name": "Banana Cake", "price": 33.24, "collection": "DEFAULT"},
        {"name": "Fruity", "price": 30.4, "collection": "DEFAULT"},
        {"name": "Cocoa", "price": 34.99, "collection": "KETO"},
    ]
    response = client.post("/cart/checkout", json=cart_data)
    assert response.status_code == 200
    data = response.json()["cart"]
    assert data["price"] == expected_final_price
    assert data["items"] == expected_items_list


@pytest.mark.parametrize(
    "client", [{"get_config": override_config_excluded_collection}], indirect=True
)
def test_checkout_cart_with_different_excluded_collection(client: TestClient):
    # Progressive discount = 5, min_qty = 2.
    # Discount will be applied to every box BUT BEST-SELLERS
    # Discount = 10% (5 + 5, since there are 3 valid boxes)
    cart_data = {
        "cart": {
            "reference": "2d832fe0-6c96-4515-9be7-4c00983539c1",
            "lineItems": [
                {
                    "name": "Peanut Butter",
                    "price": "39.0",
                    "collection": "BEST-SELLERS",
                },
                {"name": "Banana Cake", "price": "34.99", "collection": "DEFAULT"},
                {"name": "Cocoa", "price": "34.99", "collection": "KETO"},
                {"name": "Fruity", "price": "32", "collection": "DEFAULT"},
            ],
        }
    }
    expected_final_price = 130.78  # (34.99 + 34.99 + 32) * 0.9 + 39.0
    expected_items_list = [
        {"name": "Banana Cake", "price": 31.49, "collection": "DEFAULT"},
        {"name": "Cocoa", "price": 31.49, "collection": "KETO"},
        {"name": "Fruity", "price": 28.8, "collection": "DEFAULT"},
        {
            "name": "Peanut Butter",
            "price": 39.0,
            "collection": "BEST-SELLERS",
        },
    ]
    response = client.post("/cart/checkout", json=cart_data)
    assert response.status_code == 200
    data = response.json()["cart"]
    assert data["price"] == expected_final_price
    assert data["items"] == expected_items_list
