# FReview - Flask Project Review Tool

A comprehensive code review tool for Flask applications that analyzes project structure and SQLAlchemy models to ensure best practices and identify potential issues.

## Features

- 🏗️ **Project Structure Analysis**: Validates Flask project organization and required files
- 🧠 **SQLAlchemy Model Review**: Deep analysis of model definitions, relationships, and constraints
- 📝 **Multiple Output Formats**: Console output with optional Markdown reports
- 🎨 **Rich Terminal UI**: Beautiful, colored output with emojis and formatting
- ⚡ **Fast AST Parsing**: Efficient static analysis without code execution
- 🔍 **Comprehensive Checks**: Validates naming conventions, relationships, and best practices

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/your-username/freview.git
cd freview
uv sync
```

### Using pip

```bash
# Install from PyPI (when published)
pip install freview

# Or install from source
git clone https://github.com/your-username/freview.git
cd freview
pip install -e .
```

## Usage

### Basic Usage

```bash
# Review a Flask project
freview review /path/to/your/flask/project

# Generate a Markdown report
freview review /path/to/your/flask/project --markdown
```

### What it Checks

#### Project Structure
- ✅ Entry point files (app.py, run.py, main.py)
- ✅ Models directory structure
- ✅ Templates and static directories
- ✅ Configuration files (.env, config.py)
- ✅ Blueprint organization

#### SQLAlchemy Models
- ✅ Table name conventions (snake_case)
- ✅ Class name conventions (PascalCase)
- ✅ Primary key definitions
- ✅ Foreign key relationships
- ✅ Column constraints and indexing
- ✅ Enum usage
- ✅ Default values
- ✅ Relationship definitions
- ⚠️ Circular import detection
- ⚠️ Unused model detection

## Example Output

```
🔍 Reviewing /home/user/my-flask-app

📁 Structure Checks:
✅ Structure looks good

🧠 Model Checks:

📄 models/user.py
- ✅ User: Core model checks passed
- ✅ User: ForeignKey used
- ✅ User: relationship used
- ℹ️ User: nullable=False

📄 models/post.py
- ❌ Post: Missing __tablename__
- ⚠️ Post: Class name should be PascalCase

📝 Saved Markdown report: review_report.md
```

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/your-username/freview.git
cd freview

# Install with development dependencies using uv
uv sync

# Run tests
uv run pytest

# Format code
uv run black .

# Type checking
uv run mypy freview/

# Lint code
uv run flake8 freview/

# Run the tool directly
uv run freview --help
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=freview --cov-report=html

# Run specific test file
uv run pytest tests/test_model_checker.py
```

## Configuration

Create a `.freview.toml` file in your project root to customize analysis:

```toml
[freview]
# Custom model directories to scan
model_dirs = ["models", "app/models", "src/models"]

# Skip certain checks
skip_checks = ["unused_models", "circular_imports"]

# Custom naming patterns
class_name_pattern = "^[A-Z][a-zA-Z0-9]+$"
table_name_pattern = "^[a-z_]+$"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- Basic project structure analysis
- SQLAlchemy model validation
- Markdown report generation