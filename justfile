ROOT := justfile_directory()
SRC := join(ROOT, "src")
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
lint: fmt
    flake8 .
    isort .
    mypy

# Run tests and linting in one go
check: lint test

# Create a new day folder and its tests
new day:
    mkdir -p src/{{ day }}
    touch src/{{ day }}/__init__.py
    touch src/{{ day }}/{{ day }}.py
    touch src/{{ day }}/{{ day }}.txt
    touch tests/test_{{ day }}.py

# Create a virtualenv and install dependencies
install:
    poetry install

# Update dependencies
update:
    poetry update
