from lib.utils import checkout_totals


def test_finishing_an_order_shows_the_documented_totals(
    inventory_page, testdata, assertion
):
    slugs = ["sauce-labs-backpack", "sauce-labs-onesie"]
    for slug in slugs:
        inventory_page.add_to_cart(slug)
    cart = inventory_page.go_to_cart()
    expected = checkout_totals(
        [testdata.products[slug]["price"] for slug in slugs],
        testdata.tax_rate,
    )

    overview = cart.go_to_checkout_step_one().fill_and_continue(
        testdata.checkout_first_name,
        testdata.checkout_last_name,
        testdata.checkout_postal_code,
    )

    assertion.assert_equal(
        actual_result=overview.item_total_text(),
        expected_result="Item total: " + expected["item_total"],
        label="item total",
    )
    assertion.assert_equal(
        actual_result=overview.tax_text(),
        expected_result="Tax: " + expected["tax"],
        label="tax",
    )
    assertion.assert_equal(
        actual_result=overview.grand_total_text(),
        expected_result="Total: " + expected["grand_total"],
        label="grand total",
    )
    assertion.assert_equal(
        actual_result=overview.payment_info(),
        expected_result=testdata.overview_payment_info,
        label="payment info",
    )
    assertion.assert_equal(
        actual_result=overview.shipping_info(),
        expected_result=testdata.overview_shipping_info,
        label="shipping info",
    )

    complete = overview.finish()

    assertion.assert_equal(
        actual_result=complete.header_text(),
        expected_result=testdata.complete_header,
        label="complete header",
    )


def test_an_ordered_cart_is_empty_afterwards(inventory_page, testdata, assertion):
    inventory_page.add_to_cart("sauce-labs-backpack")
    overview = (
        inventory_page.go_to_cart()
        .go_to_checkout_step_one()
        .fill_and_continue(
            testdata.checkout_first_name,
            testdata.checkout_last_name,
            testdata.checkout_postal_code,
        )
    )

    complete = overview.finish()

    assertion.assert_equal(
        actual_result=complete.badge_count(),
        expected_result=0,
        label="cart badge after finishing",
    )


def test_cancelling_the_customer_form_returns_to_the_cart(
    inventory_page, testdata, assertion
):
    inventory_page.add_to_cart("sauce-labs-fleece-jacket")
    step_one = inventory_page.go_to_cart().go_to_checkout_step_one()

    cart = step_one.cancel()

    jacket = testdata.products["sauce-labs-fleece-jacket"]
    assertion.assert_equal(
        actual_result=cart.item_names(),
        expected_result=[jacket["name"]],
        label="cart items",
    )
