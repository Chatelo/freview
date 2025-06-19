# Contributing to FReview

Thank you for your interest in contributing to FReview! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- OR [pipx](https://github.com/pypa/pipx) for global installation testing

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/ronoh48/freview.git
   cd freview
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run tests**
   ```bash
   make test
   ```

4. **Run the tool**
   ```bash
   # For development
   uv run freview --help
   
   # Test global installation
   uv tool install . --force
   freview --help
   ```

## Development Workflow

### Using uv

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management:

```bash
# Install dependencies
uv sync

# Run commands in the virtual environment (development)
uv run freview review /path/to/project
uv run pytest
uv run black freview/

# Test global installation
uv tool install . --force
freview review /path/to/project

# Add new dependencies
uv add package-name

# Add development dependencies  
uv add --dev package-name
```

### Make Commands

We provide a Makefile with common development tasks:

```bash
# Show all available commands
make help

# Install dependencies
make install

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Check code formatting
make format-check

# Run linting
make lint

# Run type checking
make type-check

# Run all quality checks
make all-checks

# Clean build artifacts
make clean
```

### Code Quality

We maintain high code quality standards:

- **Formatting**: Code is formatted with [Black](https://github.com/psf/black)
- **Linting**: Code is linted with [Flake8](https://flake8.pycqa.org/)
- **Type Checking**: Type hints are checked with [MyPy](https://mypy-lang.org/)
- **Testing**: Tests are written with [pytest](https://pytest.org/)

Run all quality checks before submitting:

```bash
make all-checks
```

## Project Structure

```
freview/
├── freview/                 # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── model_checker.py    # SQLAlchemy model analysis
│   ├── project_analyzer.py # Flask project structure analysis
│   └── utils.py            # Utility functions
├── tests/                  # Test suite
│   ├── conftest.py        # Test configuration
│   ├── test_model_checker.py
│   └── test_project_analyzer.py
├── pyproject.toml          # Project configuration
├── Makefile               # Development commands
└── README.md              # Project documentation
```

## Adding Features

When adding new features:

1. **Write tests first** - We follow TDD practices
2. **Update documentation** - Keep README and docstrings current
3. **Follow code style** - Use Black formatting and type hints
4. **Add error handling** - Provide helpful error messages
5. **Update CLI help** - Keep command help text accurate

### Adding New Checks

To add new analysis checks:

1. **For project structure**: Add to `project_analyzer.py`
2. **For models**: Add to `model_checker.py`
3. **Add tests**: Create corresponding test cases
4. **Update CLI**: Add any new options to `cli.py`

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
uv run pytest tests/test_model_checker.py

# Run specific test
uv run pytest tests/test_model_checker.py::test_analyze_good_model
```

### Writing Tests

- Use pytest fixtures for common test data
- Test both success and failure cases
- Mock external dependencies when appropriate
- Keep tests focused and readable

## Documentation

- Use clear, concise docstrings
- Include type hints for all functions
- Update README.md when adding features
- Include examples in docstrings when helpful

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes** following the guidelines above
4. **Run quality checks** with `make all-checks`
5. **Update documentation** as needed
6. **Create a pull request** with a clear description

### Pull Request Checklist

- [ ] Tests pass (`make test`)
- [ ] Code is formatted (`make format-check`)
- [ ] Code is linted (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Documentation is updated
- [ ] CHANGELOG is updated (if applicable)

## Release Process

Releases are managed by maintainers:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create and push a git tag
4. GitHub Actions will build and publish to PyPI

## Getting Help

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Code**: Follow the patterns established in the existing codebase

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Please be respectful and inclusive in all interactions.
