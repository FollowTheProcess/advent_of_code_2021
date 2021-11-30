ROOT := justfile_directory()
SRC := join(ROOT, "aoc")
TESTS := join(ROOT, "tests")

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
    black .

# Lint all source code
lint:
    flake8 .
    isort .
    mypy

# Run tests and linting in one go
check: lint test

# Create a virtualenv and install dependencies
install:
    poetry install

# Update dependencies
update:
    poetry update
