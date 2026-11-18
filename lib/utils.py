import logging

logger = logging.getLogger(__name__)


# money the way the app prints it: "$29.99"
def money_to_text(amount):
    return f"${amount:.2f}"


# text the app prints back as a float: "$29.99" -> 29.99
def text_to_money(text):
    return float(text.replace("$", "").strip())


# one place that knows the app's checkout math, so a test never
# repeats the formula: item total, tax on it, delivery free
def checkout_totals(prices, tax_rate):
    item_total = round(sum(prices), 2)
    tax = round(item_total * tax_rate, 2)
    grand_total = round(item_total + tax, 2)
    return {
        "item_total": money_to_text(item_total),
        "tax": money_to_text(tax),
        "grand_total": money_to_text(grand_total),
    }
