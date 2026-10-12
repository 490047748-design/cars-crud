"""Workshop integration tests for the SQLite database."""

from pathlib import Path

import pytest

from app import database
from app.schemas import CarInput


pytestmark = pytest.mark.integration


@pytest.fixture
def db(database_path: Path) -> Path:
    database.initialize(database_path)
    return database_path


def test_car_can_be_saved_and_read(db):
    car_input = CarInput(
        make="Toyota",
        model="Corolla",
        year=2024,
        color="Silver",
    )

    created = database.create_car(db, car_input)
    loaded = database.get_car(db, created.id)

    assert loaded == created


def test_deleting_one_car_keeps_the_other(db):
    first = database.create_car(
        db,
        CarInput(make="Toyota", model="Corolla", year=2024),
    )
    second = database.create_car(
        db,
        CarInput(make="Honda", model="Civic", year=2023),
    )

    assert database.delete_car(db, first.id) is True
    assert database.get_car(db, first.id) is None
    assert database.get_car(db, second.id) == second
    assert database.list_cars(db) == [second]