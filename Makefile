.PHONY: help install test lint format type-check clean run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=freview --cov-report=html --cov-report=term-missing

lint: ## Run linting
	uv run flake8 freview/

format: ## Format code
	uv run black freview/ tests/

format-check: ## Check code formatting
	uv run black --check freview/ tests/

type-check: ## Run type checking
	uv run mypy freview/

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

run: ## Run the CLI tool
	uv run freview --help

dev-install: ## Install in development mode
	uv pip install -e .

all-checks: format lint type-check test ## Run all quality checks

build: ## Build the package
	uv build

publish: ## Publish to PyPI (requires setup)
	uv publish

install-global: build ## Install globally with uv tool
	uv tool uninstall freview || true
	uv tool install ./dist/freview-*-py3-none-any.whl

test-global: install-global ## Test global installation
	freview --version
	freview -V
	freview version
	@echo "Global installation test passed!"

test-install-script: ## Test the installation script
	@echo "Testing installation script..."
	./install_freview.sh
	@echo "Installation script test completed!"

uninstall-global: ## Uninstall global installation
	uv tool uninstall freview
