import logging

from lib.web.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutOverviewLocators:
    item_total = "//*[@data-test='subtotal-label']"
    tax = "//*[@data-test='tax-label']"
    grand_total = "//*[@data-test='total-label']"
    payment = "//*[@data-test='payment-info-value']"
    shipping = "//*[@data-test='shipping-info-value']"
    finish = "//*[@data-test='finish']"


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"

    # the lines read "Item total: $29.99" and the like, the test compares
    # the whole sentence against what the app's own math predicts
    def item_total_text(self):
        return self.text(CheckoutOverviewLocators.item_total)

    def tax_text(self):
        return self.text(CheckoutOverviewLocators.tax)

    def grand_total_text(self):
        return self.text(CheckoutOverviewLocators.grand_total)

    def payment_info(self):
        return self.text(CheckoutOverviewLocators.payment)

    def shipping_info(self):
        return self.text(CheckoutOverviewLocators.shipping)

    def finish(self):
        logger.info("finishing the order")
        self.click(CheckoutOverviewLocators.finish)
        from lib.web.pages.checkout_complete_page import CheckoutCompletePage

        return CheckoutCompletePage(self.driver, self.timeout).wait_to_be_here()
