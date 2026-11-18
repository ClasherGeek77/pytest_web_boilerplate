import logging

from lib.web.base_page import BasePage

logger = logging.getLogger(__name__)


class CartLocators:
    item_name = "//*[@data-test='inventory-item-name']"
    item_price = "//*[@data-test='inventory-item-price']"


class CartPage(BasePage):
    path = "/cart.html"

    def item_names(self):
        return self.texts(CartLocators.item_name)

    def item_prices(self):
        return [
            el.text
            for el in self.driver.find_elements("xpath", CartLocators.item_price)
        ]

    def remove(self, slug):
        logger.info(f"removing {slug} from the cart")
        self.click(f"//*[@data-test='remove-{slug}']")
        return self

    def continue_shopping(self):
        logger.info("back to the products")
        self.click("//*[@data-test='continue-shopping']")
        from lib.web.pages.inventory_page import InventoryPage

        return InventoryPage(self.driver, self.timeout).wait_to_be_here()

    def go_to_checkout_step_one(self):
        logger.info("starting the checkout")
        self.click("//*[@data-test='checkout']")
        from lib.web.pages.checkout_step_one_page import CheckoutStepOnePage

        return CheckoutStepOnePage(self.driver, self.timeout).wait_to_be_here()
