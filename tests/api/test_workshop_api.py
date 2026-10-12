"""Workshop tests for the HTTP API."""

import pytest


pytestmark = pytest.mark.api


def test_create_returns_201_json_and_location(client, car_payload):
    response = client.post("/api/cars", json=car_payload)

    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"

    created = response.json()

    assert created == {"id": created["id"], **car_payload}
    assert created["id"] > 0
    assert response.headers["location"] == f"/api/cars/{created['id']}"


def test_invalid_year_is_not_saved(client):
    invalid_car = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 1800,
        "color": "Silver",
    }

    response = client.post("/api/cars", json=invalid_car)

    assert response.status_code == 422
    assert client.get("/api/cars").json() == []