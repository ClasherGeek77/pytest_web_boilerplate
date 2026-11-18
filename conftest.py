import logging
import os
import subprocess  # nosec B404
import sys
import time
from urllib.parse import urlparse

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service

from lib.assertion import Assertion
from lib.constants import constant_data, environment_data
from lib.web.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


class TestData:
    def __init__(self):
        self.standard_user = constant_data["standard_user"]
        self.locked_out_user = constant_data["locked_out_user"]
        self.password = constant_data["password"]
        self.wrong_password = constant_data["wrong_password"]
        self.error_locked_out = constant_data["error_locked_out"]
        self.error_no_match = constant_data["error_no_match"]
        self.error_username_required = constant_data["error_username_required"]
        self.error_password_required = constant_data["error_password_required"]
        self.products = constant_data["products"]
        self.product_count = constant_data["product_count"]
        self.catalog_az = constant_data["catalog_az"]
        self.cheapest_product = constant_data["cheapest_product"]
        self.most_expensive_product = constant_data["most_expensive_product"]
        self.inventory_title = constant_data["inventory_title"]
        self.tax_rate = constant_data["tax_rate"]
        self.checkout_first_name = constant_data["checkout_first_name"]
        self.checkout_last_name = constant_data["checkout_last_name"]
        self.checkout_postal_code = constant_data["checkout_postal_code"]
        self.overview_payment_info = constant_data["overview_payment_info"]
        self.overview_shipping_info = constant_data["overview_shipping_info"]
        self.complete_header = constant_data["complete_header"]
        self.sort_price_low_to_high = constant_data["sort_price_low_to_high"]
        self.sort_price_high_to_low = constant_data["sort_price_high_to_low"]


def clone_is_up():
    try:
        requests.get(environment_data["base_url"], timeout=2)
        return True
    except requests.RequestException:
        return False


# the saucedemo clone normally runs on its own (see README), but when nothing
# answers the session starts it from SAUCEDEMO_CLONE_DIR and stops it again
@pytest.fixture(autouse=True, scope="session")
def saucedemo_clone():
    if clone_is_up():
        logger.info(f"saucedemo clone is answering on {environment_data['base_url']}")
        yield
        return
    clone_dir = environment_data["clone_dir"]
    if not os.path.isdir(clone_dir):
        raise RuntimeError(
            f"nothing on {environment_data['base_url']} and no clone at {clone_dir}, "
            "start the server or fix SAUCEDEMO_CLONE_DIR in test.env"
        )
    port = urlparse(environment_data["base_url"]).port or 50000
    logger.info(f"starting the saucedemo clone from {clone_dir} on port {port}")
    # one local dev server with fixed arguments, nothing from user input
    # the process must outlive this line, the yield and terminate end it
    process = subprocess.Popen(  # pylint: disable=consider-using-with  # nosec B603
        [sys.executable, "server.py", "--port", str(port)],
        cwd=clone_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    deadline = time.time() + 15
    while time.time() < deadline and not clone_is_up():
        time.sleep(0.3)
    if not clone_is_up():
        process.terminate()
        raise RuntimeError("the saucedemo clone did not answer within 15 seconds")
    yield
    process.terminate()
    process.wait(timeout=10)


# one Chrome session for the whole run (the heavy part on 8 gb),
# Chrome 128 + chromedriver 128 pinned by path, see README
# dependency through the argument, nothing else uses it
@pytest.fixture(scope="session")
def driver(saucedemo_clone):  # pylint: disable=unused-argument
    options = ChromeOptions()
    if environment_data["headless"]:
        options.add_argument("--headless=new")
    options.binary_location = environment_data["chrome_bin"]
    options.add_argument("--window-size=1280,1200")
    service = Service(
        executable_path=environment_data["chromedriver_bin"],
        log_output=subprocess.DEVNULL,
    )
    # selenium re-exports Chrome lazily, pylint's astroid cannot see that
    client = webdriver.Chrome(  # pylint: disable=not-callable
        service=service, options=options
    )
    client.implicitly_wait(0)  # every wait in this project is explicit
    yield client
    client.quit()


# the cart is localStorage and the session is a cookie, both get cleared
# before every test to keep the tests independent, like the old tab-per-test
@pytest.fixture(autouse=True)
def clean_state(driver):
    driver.get(environment_data["base_url"])
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    yield


@pytest.fixture
def testdata():
    return TestData()


@pytest.fixture
def assertion():
    return Assertion()


@pytest.fixture(name="logger")
def step_logger():
    return logging.getLogger("test")


@pytest.fixture
def login_page(driver):
    return LoginPage(driver, environment_data["ui_timeout"])


# for the tests that need the store itself, login is setup, not the subject
@pytest.fixture
def inventory_page(testdata, login_page):
    return login_page.open().login(testdata.standard_user, testdata.password)
