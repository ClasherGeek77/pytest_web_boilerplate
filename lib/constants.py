import os

_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# dynamic, changes between runs or environments
environment_data = {
    # the local saucedemo clone, ../saucedemo_clone/server.py, see README
    "base_url": os.environ.get("BASE_URL", "http://localhost:50000"),
    "headless": os.environ.get("HEADLESS", "1") == "1",
    "ui_timeout": int(os.environ.get("UI_TIMEOUT", "15")),
    # the browser and its driver are pinned by path: Chrome
    # 128.0.6613.120 and chromedriver 128.0.6613.137, the last pair that
    # runs on macOS 10.15, see README
    "chrome_bin": os.environ.get(
        "CHROME_BIN",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ),
    "chromedriver_bin": os.path.abspath(
        os.environ.get(
            "CHROMEDRIVER_BIN", os.path.join(_project_dir, "tools", "chromedriver")
        )
    ),
    # where the clone lives, only needed when BASE_URL answers nothing
    "clone_dir": os.path.abspath(
        os.environ.get(
            "SAUCEDEMO_CLONE_DIR",
            os.path.join(_project_dir, "..", "saucedemo_clone"),
        )
    ),
}

# static, never changes between runs or environments
constant_data = {
    # accounts built into the app bundle: everyone takes the same password,
    # locked_out_user is the only one the app rejects by name
    "standard_user": "standard_user",
    "locked_out_user": "locked_out_user",
    "password": "secret_sauce",
    "wrong_password": "not_the_real_password",
    # login errors, the app's own sentences
    "error_locked_out": "Epic sadface: Sorry, this user has been locked out.",
    "error_no_match": (
        "Epic sadface: Username and password do not match any user in this service"
    ),
    "error_username_required": "Epic sadface: Username is required",
    "error_password_required": "Epic sadface: Password is required",
    # the six products of the standard catalog, slug is what the app uses
    # in its data-test attributes (add-to-cart-<slug>), price as displayed
    "products": {
        "sauce-labs-backpack": {"name": "Sauce Labs Backpack", "price": 29.99},
        "sauce-labs-bike-light": {"name": "Sauce Labs Bike Light", "price": 9.99},
        "sauce-labs-bolt-t-shirt": {"name": "Sauce Labs Bolt T-Shirt", "price": 15.99},
        "sauce-labs-fleece-jacket": {
            "name": "Sauce Labs Fleece Jacket",
            "price": 49.99,
        },
        "sauce-labs-onesie": {"name": "Sauce Labs Onesie", "price": 7.99},
        "test.allthethings()-t-shirt-(red)": {
            "name": "Test.allTheThings() T-Shirt (Red)",
            "price": 15.99,
        },
    },
    "product_count": 6,
    "catalog_az": [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)",
    ],
    "cheapest_product": "Sauce Labs Onesie",
    "most_expensive_product": "Sauce Labs Fleece Jacket",
    "inventory_title": "Products",
    # the checkout math inside the app: tax is a rate on the item total,
    # and delivery is free ("Free Pony Express Delivery!")
    "tax_rate": 0.08,
    "checkout_first_name": "Auto",
    "checkout_last_name": "Test",
    "checkout_postal_code": "12345",
    "overview_payment_info": "SauceCard #31337",
    "overview_shipping_info": "Free Pony Express Delivery!",
    "complete_header": "Thank you for your order!",
    # sort orders of the product dropdown the tests use
    "sort_price_low_to_high": "lohi",
    "sort_price_high_to_low": "hilo",
}
