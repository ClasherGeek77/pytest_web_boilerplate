#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    echo "No .venv yet, run ./first_setup.sh once first"
    exit 1
fi

export PATH="$PWD/.venv/bin:$PATH"

# the checks look at this project only, the untouched copy of the api
# boilerplate in ./pytest_boilerplate_api/ is not part of it (see README)
echo "Security check (bandit)"
bandit --recursive . --ini .bandit --exclude ./.venv,./pytest_boilerplate_api --quiet

echo "Format check (black)"
black --check lib tests conftest.py

echo "Lint check (pylint)"
pylint --rcfile=.pylintrc lib tests conftest.py
