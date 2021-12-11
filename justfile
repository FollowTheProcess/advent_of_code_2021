ROOT := justfile_directory()
SRC := join(ROOT, "src")
TESTS := join(ROOT, "tests")

set dotenv-load := true

# By default, print the list of recipes
_default:
    @just --list

# Show justfile variables
show:
    @just --evaluate

# Run the tests
test:
    pytest {{ TESTS }}

# Format all source code with black
fmt:
    black {{ ROOT }}

# Lint all source code
lint: fmt
    flake8 {{ ROOT }}
    isort {{ ROOT }}
    mypy

# Run tests and linting in one go
check: lint test

# Create a new day (int) folder and its tests
new day:
    python scripts/new.py {{ day }}

# Run a day's (int) code
run day:
    python scripts/run.py {{ day }}

# Create a virtualenv and install dependencies
install:
    poetry install

# Update dependencies
update:
    poetry update
