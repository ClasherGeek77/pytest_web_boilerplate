from lib.web.base_page import BasePage


class CheckoutCompleteLocators:
    header = "//*[@data-test='complete-header']"


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"

    def header_text(self):
        return self.text(CheckoutCompleteLocators.header)
