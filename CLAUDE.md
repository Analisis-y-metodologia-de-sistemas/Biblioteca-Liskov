# CLAUDE.md - Development Configuration & Guidelines

This file contains essential development configuration, linting rules, formatting standards, and build restrictions for the Biblioteca Liskov project.

## 🎯 Project Overview

Educational library management system implementing Clean Architecture with comprehensive testing and CI/CD pipeline.

## 📋 Code Quality Standards

### Line Length & Formatting
- **Maximum line length**: 127 characters (configured in pyproject.toml)
- **Code formatter**: Black with 127-character line length
- **Import organizer**: isort with black profile
- **Target Python version**: 3.11+

### Linting Configuration (flake8)
```ini
[tool.flake8]
max-line-length = 127
max-complexity = 10
select = ["E", "W", "F", "C90"]
ignore = [
    "E203",  # whitespace before ':'  (conflicts with black)
    "E501",  # line too long (handled by black)
    "W503",  # line break before binary operator (conflicts with black)
]
exclude = [
    ".git", "__pycache__", "build", "dist", ".venv", "venv", ".tox", ".eggs",
]
per-file-ignores = [
    "__init__.py:F401",
    "tests/*:F401,F811",
]
```

### Test Coverage Requirements
- **Minimum coverage**: 40% (configured in pyproject.toml)
- **Current coverage**: 47.10% (exceeds requirement)
- **Coverage focus**: Core business logic (src/) rather than UI/presentation layers
- **Coverage command**: `pytest --cov=src --cov-report=term-missing --cov-fail-under=40`

## 🔧 Build & CI/CD Configuration

### Required Commands for Development
```bash
# Code formatting
black . --line-length 127 --target-version py311

# Import organization
isort . --profile black --line-length 127

# Linting
flake8 --max-line-length=127 --max-complexity=10

# Type checking
mypy src/ --ignore-missing-imports --no-strict-optional

# Security scanning
bandit -r src/ -ll

# Dependency vulnerability check
safety check

# Run tests with coverage
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=40
```

### Development Dependencies
Install with: `pip install -e ".[dev]"`

From pyproject.toml:
```toml
[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "bandit>=1.7.5",
    "safety>=2.3.0",
    "pylint>=2.17.0",
]
```

## 🚫 Build Restrictions & Common Issues

### Linting Violations to Avoid
1. **F401**: Unused imports - Remove all unused imports from src/ files
2. **E501**: Line too long - Keep lines under 127 characters
3. **F841**: Unused variables - Remove or use assigned variables
4. **F541**: F-strings without placeholders - Use regular strings instead
5. **E402**: Module imports not at top - Move imports to file beginning

### Acceptable Patterns in Test Files
- **E402** in test files for sys.path manipulation (required for testing)
- **F401** for test-specific imports that may appear unused
- **F841** for test variables used for assertion setup

### Security Restrictions
- **SQL Injection Prevention**: All database queries must use parameterized queries
- **Input Validation**: Validate all user inputs, especially for database operations
- **No Hardcoded Secrets**: Never commit passwords, tokens, or sensitive data
- **Bandit Security Scan**: Must pass with no high/medium severity issues

### Cross-Platform Compatibility
- **No OS-specific dependencies**: Must run on Mac, Windows, and Linux
- **Use native Python features**: Avoid external dependencies for basic functionality
- **ANSI color codes**: Use terminal detection for color support

## 🏗️ Architecture Constraints

### Clean Architecture Compliance
- **Domain Layer**: Pure business logic, no external dependencies
- **Application Layer**: Use cases and service interfaces
- **Infrastructure Layer**: Repository implementations, database access
- **Presentation Layer**: Console UI, menu systems

### Dependency Rules
- **Domain**: Cannot depend on any other layer
- **Application**: Can depend only on Domain
- **Infrastructure**: Can depend on Application and Domain
- **Presentation**: Can depend on Application and Domain (not Infrastructure directly)

## 🧪 Testing Requirements

### Test Structure
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for full workflows
└── domain/         # Domain entity and value object tests
```

### Test Coverage Focus Areas
1. **Domain entities** (96.94% coverage)
2. **Application services** (99.36% coverage)
3. **Repository implementations** (88.77% coverage)
4. **Authentication service** (91.86% coverage)

### Test Commands
```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=src --cov-report=html

# Run specific test categories
python -m pytest -m unit
python -m pytest -m integration
```

## 🔄 CI/CD Pipeline Requirements

### GitHub Actions Workflow Checks
1. **Code formatting** (black) - must pass
2. **Import sorting** (isort) - must pass
3. **Linting** (flake8) - must pass with project config
4. **Type checking** (mypy) - warnings allowed
5. **Security scanning** (bandit) - no high/medium issues
6. **Dependency check** (safety) - warnings allowed
7. **Test execution** - all 160 tests must pass
8. **Coverage verification** - must exceed 40%

### Build Artifacts
- **Test results** with coverage reports
- **Security scan reports** (bandit, safety)
- **Package build** (wheel and source distribution)

## 📝 Pre-commit Guidelines

Before pushing code, ensure:
```bash
# 1. Format code
black . --line-length 127

# 2. Organize imports
isort . --profile black

# 3. Check linting
flake8 --max-line-length=127

# 4. Run tests
python -m pytest --cov=src

# 5. Check security
bandit -r src/ -ll
```

## 🎓 Educational Context

This project serves as an educational example of:
- **Clean Architecture** implementation
- **Professional Python development** practices
- **Comprehensive testing** strategies
- **CI/CD pipeline** configuration
- **Code quality standards** enforcement

All configurations prioritize learning and best practices over maximum coverage or complexity.

---

**Last updated**: 2025-09-14
**Project version**: 1.0.0
**Python version**: 3.11+