# Makefile for demoviz development

.PHONY: test test-v test-cov test-fast test-core test-matplotlib test-seaborn install-dev clean lint format check

# Default Python interpreter
PYTHON ?= python

# Test commands
test:
	$(PYTHON) -m pytest tests/ -x

test-v:
	$(PYTHON) -m pytest tests/ -v

test-cov:
	$(PYTHON) -m pytest tests/ --cov=demoviz --cov-report=html --cov-report=term-missing

test-fast:
	$(PYTHON) -m pytest tests/ -x --ff

test-core:
	$(PYTHON) -m pytest tests/test_core.py -v

test-matplotlib:
	$(PYTHON) -m pytest tests/test_matplotlib_integration.py -v

test-seaborn:
	$(PYTHON) -m pytest tests/test_seaborn_integration.py -v

# Run specific test by name
test-name:
	$(PYTHON) -m pytest tests/ -k "$(NAME)" -v

# Development setup
install-dev:
	pip install -e ".[dev]"

install-test:
	pip install -e ".[dev]" pytest pytest-cov

# Code quality
lint:
	flake8 demoviz tests

format:
	black demoviz tests

format-check:
	black --check demoviz tests

check: format-check lint test

# Build and distribution
build:
	$(PYTHON) -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Documentation (if you add docs later)
docs:
	cd docs && make html

docs-clean:
	cd docs && make clean

# Release workflow
check-release: clean check test-cov
	@echo "✅ Ready for release!"

# Help
help:
	@echo "Available commands:"
	@echo "  test          - Run all tests"
	@echo "  test-v        - Run tests with verbose output"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  test-fast     - Run tests with fail-fast and failed-first"
	@echo "  test-core     - Run only core tests"
	@echo "  test-matplotlib - Run only matplotlib integration tests"
	@echo "  test-seaborn  - Run only seaborn integration tests"
	@echo "  test-name     - Run specific test (use NAME=test_name)"
	@echo "  install-dev   - Install package in development mode"
	@echo "  lint          - Run linter"
	@echo "  format        - Format code with black"
	@echo "  format-check  - Check code formatting"
	@echo "  check         - Run all quality checks"
	@echo "  build         - Build distribution packages"
	@echo "  clean         - Clean build artifacts"
	@echo "  help          - Show this help message"