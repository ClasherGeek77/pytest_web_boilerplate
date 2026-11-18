# pytest_web_boilerplate

## what it is

a starter project for browser tests with Python, pytest and Selenium (Chrome). it ships with 17 working tests against a local copy of the saucedemo shop (login, product list, cart, checkout), so you can run something real in minutes and then copy the structure for your own site.

- tests are plain pytest functions, one file per area in `tests/web/`
- every page of the shop is a page-object class with its xpaths at the top of the file
- every check goes through one `assertion` helper that logs each step
- the target is the saucedemo clone, http://localhost:50000, so no internet, no rate limits, nothing to break for real users

source: https://github.com/ClasherGeek77/pytest_web_boilerplate (the `legacy` branch holds the full history of its predecessor, selenium_parallel_execution_framework).

## when to use it

use it when you want to learn or start a Selenium + pytest suite with a clean layout (fixtures, page objects, constants, reports).

not for:

- api tests: use https://github.com/ClasherGeek77/pytest_api_boilerplate
- the same web tests in Katalon Studio: use https://github.com/ClasherGeek77/katalon_web_boilerplate
- phone apps: use https://github.com/ClasherGeek77/pytest_android_boilerplate or https://github.com/ClasherGeek77/pytest_ios_boilerplate
- parallel runs, docker, ci: left out on purpose, this repo is the simple single-browser version

## what you need

| thing | version | where |
|---|---|---|
| Python | 3.11 (the line in `.python-version`, 3.11.14; `first_setup.sh` refuses other lines) | https://www.python.org/downloads/ |
| Google Chrome | any current Chrome; if you are on macOS 10.15 use Chrome 128.0.6613.138 | https://www.google.com/chrome/ |
| ChromeDriver | the same major version as your Chrome | https://googlechromelabs.github.io/chrome-for-testing/ |
| the saucedemo clone | any commit, Python 3 standard library only | https://github.com/ClasherGeek77/saucedemo_clone |
| git, bash | any | Mac and Linux; on Windows use WSL |

the python packages (pytest 7.4.4, pytest-html 4.1.1, selenium 4.52.0, requests, black, bandit, pylint) are pinned in `requirements.pip` and installed by `first_setup.sh`.

`tools/install_chromedriver.sh` is the macOS Intel shortcut: it downloads ChromeDriver 128.0.6613.137 (mac-x64) into `tools/chromedriver`, and installs Chrome 128 from Google's legacy macOS 10.15 link only when `/Applications/Google Chrome.app` is missing. on Linux, Apple silicon or a current macOS, skip it: install current Chrome, download the matching driver from the Chrome for Testing page above, and point the suite at both (see "settings"). that path is not verified here, only the Chrome 128 pair was run.

## quick start

1. get the target and start it. the suite looks for it next to this repo, so clone both into the same folder:

```bash
git clone https://github.com/ClasherGeek77/saucedemo_clone.git
git clone https://github.com/ClasherGeek77/pytest_web_boilerplate.git
cd saucedemo_clone
python3 server.py
```

you should see `saucedemo clone on http://localhost:50000  (Ctrl-C to stop)`. leave it running and open http://localhost:50000 in a browser: you get the saucedemo login page. (`python3 server.py --port 8080` changes the port; then set `BASE_URL` too.)

this step is optional: if nothing answers on `BASE_URL`, the test session starts `server.py` itself from `../saucedemo_clone` and stops it after the run.

2. in a second terminal, set this repo up once:

```bash
cd pytest_web_boilerplate
./tools/install_chromedriver.sh     # macOS Intel only, see "what you need"
./first_setup.sh                    # builds .venv from requirements.pip
```

you should see `Setup done, next run ./run_test.sh`.

3. run it:

```bash
./run_test.sh
```

Chrome runs headless (no window) and every step is logged. the run ends with `17 passed` (about 25 seconds on the last full run). the HTML report is written to `reports/report_<timestamp>_tests.html`, open it in a browser.

check what exists without running anything:

```bash
.venv/bin/python -m pytest --collect-only -q
```

you should see `17 tests collected` (login 6, inventory 5, cart 3, checkout 3).

one test, with the real output of a run:

```bash
./run_test.sh tests/web/test_login.py::test_logging_out_returns_to_the_login_page
```

you should see log lines like `logging in as standard_user`, `clicking //button[@id='react-burger-menu-btn']`, `checking login url: got http://localhost:50000/, expected http://localhost:50000/` and finally `1 passed in 3.78s`.

## run one test, or a few

`run_test.sh` takes any pytest argument; an argument replaces the default `TEST_PATH="tests/"` at the top of the script. the variants:

```bash
./run_test.sh tests/web/                                                            # all web tests
./run_test.sh tests/web/test_login.py                                               # one file
./run_test.sh tests/web/test_login.py::test_logging_out_returns_to_the_login_page   # one test
./run_test.sh "tests/web/test_login.py::test_refused_logins_show_their_own_error[locked-out]"   # one row of a table test
./run_test.sh tests/ -k checkout                                                    # names containing "checkout"
./run_test.sh tests/ -x                                                             # stop at the first failure
```

to change the default for every run, edit `TEST_PATH` at the top of `run_test.sh` (it accepts the same text, e.g. `TEST_PATH="tests/ -k checkout"`). `REPORT_NAME` there sets a fixed report name such as `smoke.html`; empty means `report_<timestamp>_<test path>.html`.

`./checks.sh` runs bandit (security), black (format) and pylint (lint) over `lib`, `tests` and `conftest.py`.

## settings

plain `KEY=value` lines in `test.env`, loaded by `run_test.sh`; the tests read them through `lib/constants.py`.

| key | default | meaning |
|---|---|---|
| `BASE_URL` | `http://localhost:50000` | where the saucedemo clone answers. this is how the suite finds the target |
| `HEADLESS` | `1` | `0` shows the browser window |
| `CHROME_BIN` | the macOS path of Google Chrome | path of the Chrome binary, e.g. `/usr/bin/google-chrome` on Linux. put the value in double quotes if it contains spaces |
| `CHROMEDRIVER_BIN` | `tools/chromedriver` | path of the driver; uncomment and set it when the driver lives elsewhere |
| `UI_TIMEOUT` | `15` | seconds a normal wait accepts |
| `SAUCEDEMO_CLONE_DIR` | `../saucedemo_clone` | where the clone lives, only used when nothing answers on `BASE_URL` |

## how to read the code

```
conftest.py            fixtures: saucedemo_clone, driver, clean_state, login_page, inventory_page, testdata, assertion, logger
lib/constants.py       environment_data (from test.env) and constant_data (accounts, catalog, error sentences, tax rate)
lib/utils.py           money formatting and the checkout math, so a test never repeats a formula
lib/assertion.py       the only place with a bare `assert`; every check is logged
lib/web/base_page.py   BasePage: open, url, wait_to_be_here, click, fill, text(s), select_option, is_shown, badge_count, go_to_cart, open_menu_and_logout
lib/web/pages/         one file and one class per page (login, inventory, cart, checkout step one, overview, complete), xpaths in a Locators class on top
tests/web/             test_login, test_inventory, test_cart, test_checkout
```

what happens around a test:

- `saucedemo_clone` (session, automatic): uses the clone when `BASE_URL` answers, otherwise starts it and stops it after the run.
- `driver` (session): one Chrome for the whole run, headless unless `HEADLESS=0`, no implicit waits (every wait in the code is explicit).
- `clean_state` (before every test, automatic): clears cookies, localStorage and sessionStorage, so tests do not depend on order.
- `login_page` gives a `LoginPage`; `inventory_page` gives the store already logged in as `standard_user`, for tests where login is only setup.
- `testdata` carries the values from `constant_data` as attributes (`testdata.standard_user`, `testdata.products`, `testdata.tax_rate`), so a test never types a magic string.
- page methods return the next page object (`login()` returns the `InventoryPage`), so a test reads as a story.

every locator is an xpath and lives in the page that owns it:

```python
class LoginLocators:
    username_field = "//input[@data-test='username']"
    login_button = "//input[@data-test='login-button']"
```

where the expected values come from: the catalog, the six usernames (password `secret_sauce`), the routes, the error sentences, the 8% tax with free delivery and the `data-test` attributes were read from the clone's app bundle and checked against the rendered pages. `Sauce Labs Backpack` is $29.99 in this clone (the old public site said $15.99). if the clone is re-mirrored and a test breaks, change `constant_data` only.

## how to add a test

example: after adding a product, its card shows a remove button and the cart badge says 1. every file named below exists.

1. value: put anything static in `constant_data` in `lib/constants.py`, and expose it in `TestData` in `conftest.py` (copy a line, `self.x = constant_data["x"]`). the six products are already there as `testdata.products`.
2. locator: add the xpath to the page that owns the screen, in its `Locators` class, e.g. `InventoryLocators` in `lib/web/pages/inventory_page.py`.
3. action: add a method on that page class that uses the `BasePage` verbs (`click`, `fill`, `text`, `is_shown`) and returns the next page or `self`. see `remove_from_cart` in `inventory_page.py`:

```python
def remove_from_cart(self, slug):
    logger.info(f"removing {slug} from the cart")
    self.click(f"//*[@data-test='remove-{slug}']")
    return self
```

4. test: add a function to the matching file in `tests/web/` (or a new `test_<area>.py`). ask for the fixtures you need as arguments, nothing to import. this is `test_adding_to_the_cart_shows_the_badge` in `tests/web/test_inventory.py`:

```python
def test_adding_to_the_cart_shows_the_badge(inventory_page, assertion):
    slug = "sauce-labs-backpack"
    inventory_page.add_to_cart(slug)

    assertion.assert_equal(
        actual_result=inventory_page.badge_count(),
        expected_result=1,
        label="cart badge",
    )
```

   several refused cases of one rule belong in one `@pytest.mark.parametrize` table, see `test_refused_logins_show_their_own_error` in `tests/web/test_login.py`.
5. run just that test, then the checks:

```bash
./run_test.sh tests/web/test_inventory.py::test_adding_to_the_cart_shows_the_badge
./checks.sh
```

a new page means a new file in `lib/web/pages/` (copy `login_page.py`, give it a `path`), and a fixture in `conftest.py` if tests need it directly.

## if it breaks

| symptom | cause | fix |
|---|---|---|
| `no python 3.11 found` | `first_setup.sh` needs the Python 3.11 line | install it, or `TEST_PYTHON=/path/to/python3.11 ./first_setup.sh` |
| `No .venv yet, run ./first_setup.sh once first` | setup not done | run `./first_setup.sh` |
| `nothing on http://localhost:50000 and no clone at ...` | the clone is not running and not next to this repo | start it (quick start step 1) or set `SAUCEDEMO_CLONE_DIR` in `test.env` |
| `the saucedemo clone did not answer within 15 seconds` | the port is taken, or Python cannot start `server.py` | run `python3 server.py` in the clone folder by hand and read its error |
| a chromedriver "No such file" / "Unable to obtain driver" error | no driver at `tools/chromedriver` | run `./tools/install_chromedriver.sh` (macOS Intel) or set `CHROMEDRIVER_BIN` in `test.env` |
| `This version of ChromeDriver only supports Chrome version N` | driver and Chrome majors differ | install the matching driver, or the pinned Chrome 128 pair |
| `cannot find Chrome binary` | Chrome is not at the default macOS path | set `CHROME_BIN` in `test.env` |
| `TimeoutException` on a click or a read | page slower than `UI_TIMEOUT`, or the clone changed | raise `UI_TIMEOUT`; set `HEADLESS=0` in `test.env` and watch |
| an assertion fails on a price or a name | the clone was re-mirrored | update `constant_data` in `lib/constants.py` |
| `checks.sh` fails in black or pylint | style finding in new code | `.venv/bin/black lib tests conftest.py`, then fix what pylint lists |

debugging many failures: reproduce one failing step as a small standalone snippet, fix it, re-run only that test, and run the whole suite last.

## next

- same layout for api tests: https://github.com/ClasherGeek77/pytest_api_boilerplate
- the target you just ran against: https://github.com/ClasherGeek77/saucedemo_clone
- the same shop tested with Katalon Studio: https://github.com/ClasherGeek77/katalon_web_boilerplate
- load tests with Locust: https://github.com/ClasherGeek77/locust_boilerplate
