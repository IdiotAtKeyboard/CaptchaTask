import allure
import pytest
import subprocess
import time
import requests
from pathlib import Path
from pages.home_page import HomePage
from pages.contact_form_page import ContactFormPage
from tests.data_client import DataServiceClient

ALLURE_RESULTS_DIR = Path(__file__).parent.parent / "allure-results"
DATA_SERVICE_DIR = Path(__file__).parent.parent / "data-service"
DATA_SERVICE_URL = "http://127.0.0.1:5000/"


def pytest_sessionstart(session):
    if ALLURE_RESULTS_DIR.exists():
        for item in ALLURE_RESULTS_DIR.iterdir():
            if item.is_file():
                item.unlink()
    else:
        ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def data_service():
    """Start data service before tests and stop after (skipped if DATA_SERVICE_URL is set)"""
    import os
    if os.getenv('DATA_SERVICE_URL'):
        print(f"\n>>> Using external data service at {os.getenv('DATA_SERVICE_URL')}")
        yield
        return

    print("\n>>> Installing data service dependencies...")

    # Install data-service dependencies using poetry
    install_process = subprocess.run(
        ["poetry", "install"],
        cwd=DATA_SERVICE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if install_process.returncode != 0:
        raise RuntimeError("Failed to install data-service dependencies")

    print(">>> Starting data service...")

    # Start Flask service in background using poetry
    service_process = subprocess.Popen(
        ["poetry", "run", "python", "app.py"],
        cwd=DATA_SERVICE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for service to be ready
    max_retries = 30
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(f"{DATA_SERVICE_URL}/users", timeout=1)
            if response.status_code == 200:
                print(f">>> Data service is ready at {DATA_SERVICE_URL}")
                break
        except requests.exceptions.RequestException:
            retry_count += 1
            time.sleep(0.5)

    if retry_count >= max_retries:
        service_process.terminate()
        raise RuntimeError(f"Data service failed to start at {DATA_SERVICE_URL}")

    yield

    # Cleanup: stop service
    print("\n>>> Stopping data service...")
    service_process.terminate()
    try:
        service_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        service_process.kill()
    print(">>> Data service stopped")


@pytest.fixture(scope="session")
def test_users():
    client = DataServiceClient()
    return client.get_users({"labels": ["ES", "male"]})


def pytest_generate_tests(metafunc):
    if "parametrize_from_service" in metafunc.fixturenames:
        client = DataServiceClient()
        users = client.get_users({"labels": ["ES", "male"]})

        test_data = [(u['name'], u['email'], u['company']) for u in users]
        test_ids = [u['id'] for u in users]

        metafunc.parametrize(
            "name,email,company",
            test_data,
            ids=test_ids
        )


@pytest.fixture
def parametrize_from_service(test_users):
    """Fixture that enables dynamic parametrization from service"""
    pass


@pytest.fixture
def contact_form(page):
    home = HomePage(page)
    home.open()
    home.click_get_in_touch()
    return ContactFormPage(page)
