import os
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_checkout_cart(client: TestClient):
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
