#!/bin/bash
cd "$(dirname "$0")"

# what runs, edit here or give an argument, variants:
#   TEST_PATH="tests/"                                                          everything
#   TEST_PATH="tests/web/"                                                      all web tests
#   TEST_PATH="tests/web/test_login.py"                                         one file
#   TEST_PATH="tests/web/test_login.py::test_wrong_password_is_refused"         one test
#   TEST_PATH="tests/ -k checkout"                                              tests whose name contains "checkout"
#   TEST_PATH="tests/ -x"                                                       stop at the first failure
TEST_PATH="tests/"

# report file name, written to reports/, edit this line to change it, variants:
#   REPORT_NAME=""                  default: report_<run timestamp>_<test path>.html, filled in at run time
#   REPORT_NAME="smoke.html"        a fixed name (overwritten by the next run)
REPORT_NAME=""

export TEST_PATH REPORT_NAME

exec ./run_engine.sh "$@"
