"""Workshop browser tests for the complete user workflow."""

import re

import pytest
from playwright.sync_api import expect


pytestmark = pytest.mark.e2e


def test_user_can_create_a_car(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Corolla")
    page.get_by_label("Year", exact=True).fill("2024")
    page.get_by_label("Color", exact=False).fill("Silver")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(
        page.get_by_role("heading", name="Toyota Corolla")
    ).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()

    page.get_by_role("link", name="Edit car").click()
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()

    expect(
        page.get_by_role("heading", name="Honda Accord")
    ).to_be_visible()

    page.reload()

    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")