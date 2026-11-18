import logging

from lib.web.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginLocators:
    username_field = "//input[@data-test='username']"
    # an xpath, not a secret
    password_field = "//input[@data-test='password']"  # nosec B105
    login_button = "//input[@data-test='login-button']"
    error = "//*[@data-test='error']"


class LoginPage(BasePage):
    path = "/"

    def login(self, username, password):
        logger.info(f"logging in as {username}")
        self.fill(LoginLocators.username_field, username)
        self.fill(LoginLocators.password_field, password)
        self.click(LoginLocators.login_button)
        from lib.web.pages.inventory_page import InventoryPage

        return InventoryPage(self.driver, self.timeout).wait_to_be_here()

    # a login the app refuses: fields left out stay empty on purpose,
    # the page does not move, so wait for its own error line instead
    def try_login(self, username=None, password=None):
        logger.info(f"trying to log in as {username}")
        if username is not None:
            self.fill(LoginLocators.username_field, username)
        if password is not None:
            self.fill(LoginLocators.password_field, password)
        self.click(LoginLocators.login_button)
        self.is_shown(LoginLocators.error, seconds=self.timeout)
        return self

    def error_text(self):
        return self.text(LoginLocators.error)
