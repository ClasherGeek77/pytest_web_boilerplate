#!/bin/bash
set -e
cd "$(dirname "$0")"

PYTHON_VERSION=$(cat .python-version)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f1,2)

# the venv needs exactly the python minor version in .python-version; if it is
# not on your PATH as python3.x, point TEST_PYTHON at it:
#   TEST_PYTHON=/path/to/python3.11 ./first_setup.sh
TEST_PYTHON=${TEST_PYTHON:-}

PYTHON=""
for candidate in "python$PYTHON_MINOR" "$TEST_PYTHON" python3; do
    if command -v "$candidate" > /dev/null &&
        [ "$("$candidate" -c 'import sys; print("%d.%d" % sys.version_info[:2])')" = "$PYTHON_MINOR" ]; then
        PYTHON="$candidate"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "no python $PYTHON_MINOR found. Install it (https://www.python.org/downloads/) or run: TEST_PYTHON=/path/to/python$PYTHON_MINOR ./first_setup.sh"
    exit 1
fi

if [ -d .venv ]; then
    VENV_MINOR=$(.venv/bin/python -c 'import sys; print("%d.%d" % sys.version_info[:2])')
    if [ "$VENV_MINOR" != "$PYTHON_MINOR" ]; then
        echo ".venv uses Python $VENV_MINOR, rebuilding it with Python $PYTHON_MINOR"
        rm -rf .venv
    fi
fi

if [ ! -d .venv ]; then
    echo "Creating .venv from $PYTHON"
    "$PYTHON" -m venv .venv
fi

echo "Installing requirements"
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -r requirements.pip

echo "Setup done, next run ./run_test.sh"
