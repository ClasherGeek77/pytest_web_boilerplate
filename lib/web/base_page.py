import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from lib.constants import environment_data

logger = logging.getLogger(__name__)

XPATH = By.XPATH


class BasePage:
    # each page says where it lives, open and the click waits use it
    path = "/"

    def __init__(self, driver, timeout):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def url(self):
        return environment_data["base_url"] + self.path

    def open(self):
        logger.info(f"opening {self.url()}")
        self.driver.get(self.url())
        return self

    def current_url(self):
        return self.driver.current_url

    # waits for the url to change, so the next check never sees the old page
    def wait_to_be_here(self):
        logger.info(f"waiting for {self.url()}")
        target = self.url()
        self.wait.until(lambda driver: driver.current_url == target)
        return self

    def click(self, xpath):
        logger.info(f"clicking {xpath}")
        self.wait.until(EC.element_to_be_clickable((XPATH, xpath))).click()

    def fill(self, xpath, value):
        logger.info(f"typing into {xpath}")
        field = self.wait.until(EC.presence_of_element_located((XPATH, xpath)))
        field.clear()
        field.send_keys(value)

    # a heading can break over two lines on the page, the test only wants the words
    def text(self, xpath):
        logger.info(f"reading {xpath}")
        element = self.wait.until(EC.presence_of_element_located((XPATH, xpath)))
        return " ".join(element.text.split())

    def texts(self, xpath):
        logger.info(f"reading all {xpath}")
        self.wait.until(EC.presence_of_element_located((XPATH, xpath)))
        return [
            " ".join(el.text.split()) for el in self.driver.find_elements(XPATH, xpath)
        ]

    def select_option(self, xpath, value):
        logger.info(f"selecting {value} in {xpath}")
        Select(
            self.wait.until(EC.presence_of_element_located((XPATH, xpath)))
        ).select_by_value(value)

    def is_shown(self, xpath, seconds=3):
        logger.info(f"checking shown: {xpath}")
        try:
            WebDriverWait(self.driver, seconds).until(
                EC.visibility_of_element_located((XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False

    def badge_count(self):
        # no badge element at all means an empty cart
        if not self.is_shown("//*[@data-test='shopping-cart-badge']", seconds=2):
            return 0
        return int(self.text("//*[@data-test='shopping-cart-badge']"))

    def go_to_cart(self):
        logger.info("opening the cart from the header")
        self.click("//*[@data-test='shopping-cart-link']")
        from lib.web.pages.cart_page import CartPage

        return CartPage(self.driver, self.timeout).wait_to_be_here()

    def open_menu_and_logout(self):
        logger.info("logging out through the side menu")
        # the hamburger icon is covered by the burger-menu library's own
        # invisible button, that button is what actually opens the drawer
        self.click("//button[@id='react-burger-menu-btn']")
        self.click("//*[@data-test='logout-sidebar-link']")
        from lib.web.pages.login_page import LoginPage

        return LoginPage(self.driver, self.timeout).wait_to_be_here()
