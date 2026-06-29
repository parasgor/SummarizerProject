.PHONY: help setup install clean test test-cov test-fast lint format check docs run-example help

# Python interpreter
PYTHON := python3
PIP := pip3

# Directories
SRC_DIR := src
TEST_DIR := tests
EXAMPLES_DIR := examples

# Help target
help:
	@echo "Summarizer Agent - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make setup          - Setup development environment"
	@echo "  make install        - Install dependencies"
	@echo "  make install-dev    - Install dependencies with dev tools"
	@echo "  make clean          - Remove build artifacts and cache files"
	@echo "  make test           - Run all tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make test-fast      - Run tests without coverage"
	@echo "  make lint           - Run linting checks (flake8)"
	@echo "  make format         - Format code (black, isort)"
	@echo "  make format-check   - Check code formatting without changes"
	@echo "  make type-check     - Run type checking (mypy)"
	@echo "  make check          - Run all checks (lint, type-check, format-check)"
	@echo "  make docs           - Generate documentation"
	@echo "  make run-basic      - Run basic usage example"
	@echo "  make run-advanced   - Run advanced usage example"
	@echo "  make run-batch      - Run batch processing example"
	@echo ""

# Setup development environment
setup:
	@echo "Setting up development environment..."
	@chmod +x setup.sh
	@./setup.sh

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# Install with dev dependencies
install-dev:
	@echo "Installing dependencies with dev tools..."
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov pytest-mock black flake8 mypy isort

# Clean up
clean:
	@echo "Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/
	@echo "✓ Cleanup complete"

# Run tests
test:
	@echo "Running tests with coverage..."
	$(PYTHON) -m pytest $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=html

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage report..."
	$(PYTHON) -m pytest $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run tests fast (no coverage)
test-fast:
	@echo "Running tests..."
	$(PYTHON) -m pytest $(TEST_DIR)/ -v

# Run linting
lint:
	@echo "Running linting checks..."
	@flake8 $(SRC_DIR)/ $(TEST_DIR)/ $(EXAMPLES_DIR)/ --count --statistics

# Format code
format:
	@echo "Formatting code..."
	@black $(SRC_DIR)/ $(TEST_DIR)/ $(EXAMPLES_DIR)/ setup.py
	@isort $(SRC_DIR)/ $(TEST_DIR)/ $(EXAMPLES_DIR)/ setup.py
	@echo "✓ Code formatted"

# Check code formatting
format-check:
	@echo "Checking code formatting..."
	@black --check $(SRC_DIR)/ $(TEST_DIR)/ $(EXAMPLES_DIR)/ setup.py
	@isort --check-only $(SRC_DIR)/ $(TEST_DIR)/ $(EXAMPLES_DIR)/ setup.py
	@echo "✓ Code formatting is correct"

# Type checking
type-check:
	@echo "Running type checks..."
	@mypy $(SRC_DIR)/ --ignore-missing-imports
	@echo "✓ Type checking passed"

# Run all checks
check: lint format-check type-check test
	@echo "✓ All checks passed!"

# Generate documentation
docs:
	@echo "Generating documentation..."
	@echo "Documentation can be found in README.md"

# Run examples
run-basic:
	@echo "Running basic usage example..."
	$(PYTHON) $(EXAMPLES_DIR)/basic_usage.py

run-advanced:
	@echo "Running advanced usage example..."
	$(PYTHON) $(EXAMPLES_DIR)/advanced_usage.py

run-batch:
	@echo "Running batch processing example..."
	$(PYTHON) $(EXAMPLES_DIR)/batch_processing.py

# Default target
.DEFAULT_GOAL := help
