import allure
import pytest
from pathlib import Path
from pages.home_page import HomePage
from pages.contact_form_page import ContactFormPage

ALLURE_RESULTS_DIR = Path(__file__).parent.parent / "allure-results"


def pytest_sessionstart(session):
    if ALLURE_RESULTS_DIR.exists():
        for item in ALLURE_RESULTS_DIR.iterdir():
            if item.is_file():
                item.unlink()
    else:
        ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    allure.attach(
        page.screenshot(full_page=True),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    page.close()


@pytest.fixture
def contact_form(page):
    home = HomePage(page)
    home.open()
    home.click_get_in_touch()
    return ContactFormPage(page)
