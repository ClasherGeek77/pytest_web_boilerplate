from lib.utils import money_to_text


def test_the_cart_shows_the_added_products(inventory_page, testdata, assertion):
    inventory_page.add_to_cart("sauce-labs-backpack")

    cart = inventory_page.go_to_cart()

    backpack = testdata.products["sauce-labs-backpack"]
    assertion.assert_equal(
        actual_result=cart.item_names(),
        expected_result=[backpack["name"]],
        label="cart items",
    )
    assertion.assert_equal(
        actual_result=cart.item_prices(),
        expected_result=[money_to_text(backpack["price"])],
        label="cart prices",
    )


def test_continue_shopping_keeps_the_cart_content(inventory_page, testdata, assertion):
    inventory_page.add_to_cart("sauce-labs-onesie")
    cart = inventory_page.go_to_cart()

    back_to_products = cart.continue_shopping()

    assertion.assert_equal(
        actual_result=back_to_products.badge_count(),
        expected_result=1,
        label="cart badge",
    )
    onesie = testdata.products["sauce-labs-onesie"]
    assertion.assert_equal(
        actual_result=back_to_products.item_name("sauce-labs-onesie"),
        expected_result=onesie["name"],
        label="product name",
    )


def test_removing_in_the_cart_empties_the_badge(inventory_page, assertion):
    inventory_page.add_to_cart("sauce-labs-bike-light")
    cart = inventory_page.go_to_cart()

    cart.remove("sauce-labs-bike-light")

    assertion.assert_equal(
        actual_result=cart.badge_count(),
        expected_result=0,
        label="cart badge after removing",
    )
