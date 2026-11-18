import logging

from selenium.webdriver.common.by import By

from lib.web.base_page import XPATH, BasePage

logger = logging.getLogger(__name__)


class InventoryLocators:
    title = "//*[@data-test='title']"
    item = "//*[@data-test='inventory-item']"
    item_name = "//*[@data-test='inventory-item-name']"
    item_price = "//*[@data-test='inventory-item-price']"
    sort = "//*[@data-test='product-sort-container']"


class InventoryPage(BasePage):
    path = "/inventory.html"

    # one card of the list, found by the image its slug gives it
    def _card(self, slug):
        img = self.wait.until(
            lambda driver: driver.find_element(
                By.XPATH, f"//img[@data-test='inventory-item-{slug}-img']"
            )
        )
        return img.find_element(
            By.XPATH, "./ancestor::div[@data-test='inventory-item']"
        )

    def item_name(self, slug):
        return " ".join(
            self._card(slug)
            .find_element(By.XPATH, ".//*[@data-test='inventory-item-name']")
            .text.split()
        )

    def item_price(self, slug):
        return (
            self._card(slug)
            .find_element(By.XPATH, ".//*[@data-test='inventory-item-price']")
            .text
        )

    def add_to_cart(self, slug):
        logger.info(f"adding {slug} to the cart")
        self.click(f"//*[@data-test='add-to-cart-{slug}']")
        return self

    def remove_from_cart(self, slug):
        logger.info(f"removing {slug} from the cart")
        self.click(f"//*[@data-test='remove-{slug}']")
        return self

    def product_names(self):
        return self.texts(InventoryLocators.item_name)

    def product_prices(self):
        return [
            el.text
            for el in self.driver.find_elements(XPATH, InventoryLocators.item_price)
        ]

    def title_text(self):
        return self.text(InventoryLocators.title)

    def sort_by(self, order):
        logger.info(f"sorting products by {order}")
        self.select_option(InventoryLocators.sort, order)
        return self
