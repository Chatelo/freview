# FReview - Flask Project Review Tool

A comprehensive code review tool for Flask applications that analyzes project structure and SQLAlchemy models to ensure best practices and identify potential issues.

## Quick Start

Install and run FReview in seconds:

```bash
# Install FReview
curl -sSL https://raw.githubusercontent.com/Chatelo/freview/main/install_freview.sh | bash

# Review a Flask project
freview review /path/to/your/flask/project
```

## Features

- 🏗️ **Project Structure Analysis**: Validates Flask project organization and required files
- 🧠 **SQLAlchemy Model Review**: Deep analysis of model definitions, relationships, and constraints
- 📝 **Multiple Output Formats**: Console output with optional Markdown reports
- 🎨 **Rich Terminal UI**: Beautiful, colored output with emojis and formatting
- ⚡ **Fast AST Parsing**: Efficient static analysis without code execution
- 🔍 **Comprehensive Checks**: Validates naming conventions, relationships, and best practices

## Installation

### Quick Install (Recommended)

Install FReview with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/Chatelo/freview/main/install_freview.sh | bash
```

This script will:
- Install [uv](https://github.com/astral-sh/uv) if needed (fastest Python package manager)
- Install FReview globally using the best available method (uv → pipx → pip)
- **Automatically configure your PATH** (no manual shell restart needed!)
- Verify the installation works correctly
- Show usage instructions

**Security-conscious?** Download and inspect the script first:
```bash
curl -sSL https://raw.githubusercontent.com/Chatelo/freview/main/install_freview.sh -o install_freview.sh
# Review the script contents
cat install_freview.sh
# Run it
bash install_freview.sh
```

### Manual Installation

#### Global Installation

##### Using uv (Fastest)
```bash
# Install uv first (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install FReview globally
uv tool install freview
```

##### Using pipx (Recommended for pip users)
```bash
# Install pipx if needed
pip install --user pipx
pipx ensurepath

# Install FReview
pipx install freview
```

##### Using pip
```bash
# Install globally with pip
pip install --user freview
```

### Development Installation

#### Using uv
```bash
# Clone and install for development
git clone https://github.com/your-username/freview.git
cd freview
uv sync
```

#### Using pip
```bash
# Install from source in development mode
git clone https://github.com/your-username/freview.git
cd freview
pip install -e .
```

### Verify Installation

After installation, verify it works:

```bash
# Check version (multiple ways)
freview --version
freview -V  
freview version

# Show help
freview --help

# Test on a sample project
freview review /path/to/any/flask/project
```

## Usage

### Global Installation
Once installed globally, you can use `freview` from anywhere:

```bash
# Review any Flask project
freview review /path/to/your/flask/project

# Generate a Markdown report
freview review /path/to/your/flask/project --markdown

# Generate a JSON report
freview review /path/to/your/flask/project --json

# Show version
freview version
freview --version

# Initialize configuration in a project
freview init /path/to/your/flask/project

# Enable shell completion (optional)
freview --install-completion
```

### Development Usage
If you're working with the source code:

```bash
# Review a Flask project
uv run freview review /path/to/your/flask/project

# Generate reports
uv run freview review /path/to/your/flask/project --markdown --json
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

### Using Make Commands

```bash
# Run all quality checks
make all-checks

# Run tests
make test

# Format and lint code
make format lint

# Run type checking
make type-check
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

## Installation Troubleshooting

If you encounter issues during installation:

**Command not found after installation:**
```bash
# Restart your terminal or reload your shell configuration
source ~/.bashrc    # For bash
source ~/.zshrc     # For zsh
```

**Permission errors with pip:**
```bash
# The script automatically uses --user flag, but if you install manually:
pip install --user freview
```

**Python version compatibility:**
- Minimum required: Python 3.9+
- Check your version: `python --version`

**For corporate networks:**
```bash
# If behind proxy, configure git and pip accordingly
git config --global http.proxy http://proxy:port
pip install --proxy http://proxy:port --user freview
```

## Uninstalling FReview

If you need to remove FReview from your system:

### If installed with uv
```bash
uv tool uninstall freview
```

### If installed with pipx
```bash
pipx uninstall freview
```

### If installed with pip
```bash
pip uninstall freview
```

### Clean up shell configuration (optional)
If you want to remove the PATH entries that were automatically added:

```bash
# For bash users - edit ~/.bashrc and remove the freview PATH line
nano ~/.bashrc

# For zsh users - edit ~/.zshrc and remove the freview PATH line  
nano ~/.zshrc

# For fish users - edit ~/.config/fish/config.fish
nano ~/.config/fish/config.fish
```

Look for and remove lines like:
- `export PATH="$HOME/.local/bin:$PATH"`
- `export PATH="$HOME/.local/share/uv/tools/bin:$PATH"`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- Basic project structure analysis
- SQLAlchemy model validation
- Markdown report generation