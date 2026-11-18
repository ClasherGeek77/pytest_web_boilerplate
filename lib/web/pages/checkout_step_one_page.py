import logging

from lib.web.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutStepOneLocators:
    first_name = "//input[@data-test='firstName']"
    last_name = "//input[@data-test='lastName']"
    postal_code = "//input[@data-test='postalCode']"
    continue_button = "//*[@data-test='continue']"
    cancel_button = "//*[@data-test='cancel']"


class CheckoutStepOnePage(BasePage):
    path = "/checkout-step-one.html"

    def fill_and_continue(self, first_name, last_name, postal_code):
        logger.info(f"checkout info: {first_name} {last_name}, code {postal_code}")
        self.fill(CheckoutStepOneLocators.first_name, first_name)
        self.fill(CheckoutStepOneLocators.last_name, last_name)
        self.fill(CheckoutStepOneLocators.postal_code, postal_code)
        self.click(CheckoutStepOneLocators.continue_button)
        from lib.web.pages.checkout_overview_page import CheckoutOverviewPage

        return CheckoutOverviewPage(self.driver, self.timeout).wait_to_be_here()

    def cancel(self):
        logger.info("cancelling the checkout")
        self.click(CheckoutStepOneLocators.cancel_button)
        from lib.web.pages.cart_page import CartPage

        return CartPage(self.driver, self.timeout).wait_to_be_here()
