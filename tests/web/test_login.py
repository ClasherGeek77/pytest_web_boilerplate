import pytest


def test_login_with_standard_user_opens_the_products(testdata, login_page, assertion):
    inventory = login_page.open().login(testdata.standard_user, testdata.password)

    assertion.assert_equal(
        actual_result=inventory.current_url(),
        expected_result=inventory.url(),
        label="page url",
    )
    assertion.assert_equal(
        actual_result=inventory.title_text(),
        expected_result=testdata.inventory_title,
        label="inventory title",
    )


# the data-driven pattern from the reference repo: one table of refused
# logins, expectation constants named by attribute, ids keep the report readable
@pytest.mark.parametrize(
    ("username_attr", "password_attr", "error_attr"),
    [
        (None, None, "error_username_required"),
        ("standard_user", None, "error_password_required"),
        ("standard_user", "wrong_password", "error_no_match"),
        ("locked_out_user", "password", "error_locked_out"),
    ],
    ids=["no-username", "no-password", "no-match", "locked-out"],
)
def test_refused_logins_show_their_own_error(
    testdata, login_page, assertion, username_attr, password_attr, error_attr
):
    username = getattr(testdata, username_attr) if username_attr else None
    password = getattr(testdata, password_attr) if password_attr else None

    login_page.open().try_login(username=username, password=password)

    assertion.assert_equal(
        actual_result=login_page.error_text(),
        expected_result=getattr(testdata, error_attr),
        label="login error",
    )


def test_logging_out_returns_to_the_login_page(inventory_page, assertion):
    login = inventory_page.open_menu_and_logout()

    assertion.assert_equal(
        actual_result=login.current_url(),
        expected_result=login.url(),
        label="login url",
    )
