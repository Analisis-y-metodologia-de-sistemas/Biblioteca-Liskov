# Makefile for Biblioteca Liskov - Clean Architecture Project
# Usage: make [target]

.PHONY: help install install-dev test test-cov lint format check-format security architecture clean build docs serve-docs

# Default target
help: ## Show this help message
	@echo "🏗️  Biblioteca Liskov - Development Commands"
	@echo "============================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🎯 Quick Start:"
	@echo "   make install-dev  # Install all dependencies"
	@echo "   make test        # Run tests"
	@echo "   make lint        # Run linting"
	@echo "   make ci          # Run full CI pipeline locally"

# Installation targets
install: ## Install production dependencies
	@echo "📦 Installing production dependencies..."
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "🔗 Setting up pre-commit hooks..."
	pre-commit install
	@echo "✅ Development environment ready!"

# Testing targets
test: ## Run tests with coverage
	@echo "🧪 Running test suite..."
	python -m pytest tests/ -v --tb=short --cov=src --cov-report=term-missing

test-fast: ## Run tests without coverage (faster)
	@echo "⚡ Running fast tests..."
	python -m pytest tests/ -v --tb=short -x

test-cov: ## Run tests and generate HTML coverage report
	@echo "🧪 Running tests with detailed coverage..."
	python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report generated in htmlcov/"

test-watch: ## Run tests in watch mode
	@echo "👀 Running tests in watch mode..."
	python -m pytest tests/ -f --tb=short

# Code quality targets
lint: ## Run all linting checks
	@echo "🔍 Running linting checks..."
	@echo "📐 Checking with flake8..."
	flake8 src/ tests/
	@echo "🎨 Checking code formatting..."
	black --check --diff src/ tests/
	@echo "📋 Checking import sorting..."
	isort --check-only --diff src/ tests/
	@echo "🔒 Running security scan..."
	bandit -r src/ -ll
	@echo "📊 Type checking..."
	mypy src/ --ignore-missing-imports
	@echo "✅ All linting checks passed!"

format: ## Auto-format code
	@echo "🎨 Formatting code..."
	black src/ tests/
	isort src/ tests/
	@echo "✅ Code formatted!"

check-format: ## Check code formatting without making changes
	@echo "🔍 Checking code formatting..."
	black --check src/ tests/
	isort --check-only src/ tests/

security: ## Run security analysis
	@echo "🔒 Running security analysis..."
	bandit -r src/ -ll -f json -o security-report.json
	bandit -r src/ -ll
	safety check --json --output safety-report.json
	safety check

architecture: ## Check Clean Architecture dependencies
	@echo "🏗️  Checking Clean Architecture compliance..."
	python scripts/check_architecture.py

# Combined quality checks
quality: lint architecture ## Run all quality checks

# CI pipeline simulation
ci: clean install-dev quality test-cov ## Run full CI pipeline locally
	@echo "🎉 Full CI pipeline completed successfully!"

# Maintenance targets
clean: ## Clean up generated files
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -f security-report.json
	rm -f safety-report.json
	@echo "✅ Cleanup completed!"

# Build targets
build: clean ## Build package
	@echo "🏗️  Building package..."
	python -m build
	@echo "✅ Package built in dist/"

check-build: build ## Build and check package
	@echo "🔍 Checking package integrity..."
	python -m twine check dist/*
	@echo "✅ Package check passed!"

# Documentation targets
docs: ## Build documentation
	@echo "📚 Building documentation..."
	mkdocs build
	@echo "✅ Documentation built in site/"

serve-docs: ## Serve documentation locally
	@echo "📚 Serving documentation at http://127.0.0.1:8000"
	mkdocs serve

# Development utilities
run: ## Run the main application
	@echo "🚀 Running Biblioteca Liskov..."
	python -m src.main

run-dev: ## Run application in development mode
	@echo "🔧 Running in development mode..."
	PYTHONPATH=. python src/main.py

shell: ## Start interactive Python shell with project context
	@echo "🐍 Starting Python shell..."
	PYTHONPATH=. python -i -c "import sys; sys.path.insert(0, '.'); print('Biblioteca Liskov shell ready!')"

# Git hooks and pre-commit
hooks: ## Install git hooks
	@echo "🔗 Installing git hooks..."
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "✅ Git hooks installed!"

check-hooks: ## Run pre-commit on all files
	@echo "🔍 Running pre-commit on all files..."
	pre-commit run --all-files

# Database utilities (when implemented)
migrate: ## Run database migrations
	@echo "🗄️  Running database migrations..."
	python -m src.infrastructure.database.migrate

reset-db: ## Reset database (CAUTION: destroys data)
	@echo "⚠️  Resetting database..."
	@read -p "Are you sure? This will destroy all data. [y/N]: " confirm && [ "$$confirm" = "y" ]
	rm -f data/biblioteca.db
	$(MAKE) migrate
	@echo "✅ Database reset completed!"

# Release utilities
version: ## Show current version
	@echo "📋 Current version:"
	@python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

# Status and information
status: ## Show project status
	@echo "📊 Project Status"
	@echo "=================="
	@echo "🐍 Python version: $$(python --version)"
	@echo "📦 Installed packages:"
	@pip list | grep -E "(pytest|black|flake8|mypy)"
	@echo "🔗 Git status:"
	@git status --porcelain | head -5
	@echo "📁 Project structure:"
	@tree src/ -I "__pycache__|*.pyc" 2>/dev/null || find src/ -type f -name "*.py" | head -10

# Default Python environment variables
export PYTHONPATH := $(PWD)
export PYTHONDONTWRITEBYTECODE := 1