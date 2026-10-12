"""Workshop unit tests for CarInput validation."""

import pytest
from pydantic import ValidationError

from app.schemas import CarInput


pytestmark = pytest.mark.unit


def test_strips_surrounding_whitespace():
    car = CarInput(
        make=" Toyota ",
        model=" Corolla ",
        year=2024,
        color=" Silver ",
    )

    assert car.model_dump() == {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "color": "Silver",
    }


def test_blank_model_is_rejected():
    with pytest.raises(ValidationError):
        CarInput(
            make="Toyota",
            model=" ",
            year=2024,
            color="Silver",
        )