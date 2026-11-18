from lib.utils import money_to_text


def test_the_products_are_listed_sorted_by_name(inventory_page, testdata, assertion):
    names = inventory_page.product_names()

    assertion.assert_length(
        actual_array=names,
        expected_length=testdata.product_count,
        label="products",
    )
    assertion.assert_equal(
        actual_result=names,
        expected_result=testdata.catalog_az,
        label="product order",
    )


def test_each_product_shows_the_price_from_the_catalog(
    inventory_page, testdata, assertion
):
    # one slug per name, the app puts the slug in the data-test attributes
    for slug, product in testdata.products.items():
        assertion.assert_equal(
            actual_result=inventory_page.item_price(slug),
            expected_result=money_to_text(product["price"]),
            label=f"price of {slug}",
        )


def test_adding_to_the_cart_shows_the_badge(inventory_page, assertion):
    slug = "sauce-labs-backpack"
    inventory_page.add_to_cart(slug)

    assertion.assert_equal(
        actual_result=inventory_page.badge_count(),
        expected_result=1,
        label="cart badge",
    )


def test_removing_the_same_product_empties_the_cart_again(inventory_page, assertion):
    slug = "sauce-labs-backpack"
    inventory_page.add_to_cart(slug)

    inventory_page.remove_from_cart(slug)

    assertion.assert_equal(
        actual_result=inventory_page.badge_count(),
        expected_result=0,
        label="cart badge after removing",
    )


def test_sorting_by_price_shows_the_extremes_first(inventory_page, testdata, assertion):
    inventory_page.sort_by(testdata.sort_price_high_to_low)

    names = inventory_page.product_names()

    assertion.assert_equal(
        actual_result=names[0],
        expected_result=testdata.most_expensive_product,
        label="first product sorted high to low",
    )

    inventory_page.sort_by(testdata.sort_price_low_to_high)

    names = inventory_page.product_names()

    assertion.assert_equal(
        actual_result=names[0],
        expected_result=testdata.cheapest_product,
        label="first product sorted low to high",
    )
