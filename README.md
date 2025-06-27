# 🔍 FReview

**Comprehensive Code Review Tool for Flask Projects**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Compatible-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

A comprehensive code review tool for Flask applications that analyzes project structure, SQLAlchemy models, API patterns, and database configurations to ensure best practices and identify potential issues.

## ✨ Features

| Analysis Area | Purpose | Status |
|---------------|---------|--------|
| 🏗️ **Project Structure** | Validates Flask project organization, required files, and configuration | ✅ |
| 🧠 **SQLAlchemy Models** | Deep analysis of model definitions, relationships, constraints, and best practices | ✅ |
| 🌐 **API Patterns** | Reviews Flask routes, blueprints, REST conventions, authentication, and error handling | ✅ |
| 🗄️ **Database Analysis** | Examines migrations, configurations, query patterns, and performance optimizations | ✅ |
| 📝 **Multiple Reports** | Console output with optional Markdown/JSON reports for documentation | ✅ |
| 🎨 **Rich Terminal UI** | Beautiful, colored output with emojis and professional formatting | ✅ |

### 🔍 Detailed Analysis Capabilities

#### 🏗️ Project Structure Analysis
- ✅ Entry point validation (app.py, main.py, etc.)
- ✅ Directory organization (models/, views/, templates/, static/)
- ✅ Configuration management (config.py, .env files)
- ✅ Blueprint structure detection
- ✅ Testing setup validation
- ✅ Documentation presence

#### 🧠 SQLAlchemy Model Analysis  
- ✅ Model class structure and naming conventions
- ✅ Table naming and column definitions
- ✅ Primary key and foreign key validation
- ✅ Relationship definitions and circular dependency detection
- ✅ Model methods (`__repr__`, `__str__`) validation
- ✅ Model inheritance and mixins analysis

#### 🌐 API Pattern Analysis
- ✅ Route detection and Blueprint organization
- ✅ REST API convention compliance
- ✅ HTTP method usage patterns
- ✅ Authentication and authorization checks
- ✅ Input validation and error handling
- ✅ API versioning and documentation
- ✅ Security vulnerability detection

#### 🗄️ Database Analysis
- ✅ Migration setup (Alembic/Flask-Migrate)
- ✅ Database configuration validation
- ✅ Connection pooling and performance settings
- ✅ Query pattern analysis and N+1 detection
- ✅ Index usage and optimization suggestions
- ✅ Security (hardcoded credentials detection)

## 🚀 Installation

FReview installs **globally** on your machine, making the `freview` command available from any directory. Choose the installation method that works best for your setup:

### 🎯 Method 1: One-Line Installation (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/Chatelo/freview/main/install_freview.sh | bash
```

This script automatically detects the best installation method and installs FReview globally.

### ⚡ Method 2: Using uv (Fast & Modern)

```bash
uv tool install git+https://github.com/Chatelo/freview.git
```

**Global Installation**: Makes `freview` command available system-wide

### 🔧 Method 3: Using pipx (Recommended for CLI tools)

```bash
pipx install git+https://github.com/Chatelo/freview.git
```

**Global Installation**: Isolated dependencies with global `freview` command access

### 📦 Method 4: Using pip

```bash
pip install --user git+https://github.com/Chatelo/freview.git
```

**Global Installation**: Traditional Python package installation with global access

### 🛠️ Method 5: Manual Installation Script

Download and run the installation script with specific method:

```bash
# Download the script
curl -O https://raw.githubusercontent.com/Chatelo/freview/main/install_freview.sh
chmod +x install_freview.sh

# Install with specific method
./install_freview.sh pipx    # Using pipx
./install_freview.sh uv      # Using uv  
./install_freview.sh pip     # Using pip
./install_freview.sh auto    # Auto-detect (default)
```

### 🧪 Method 6: Development Installation

For contributors or testing:

```bash
git clone https://github.com/Chatelo/freview.git
cd freview
pip install -e .
```

### ✅ Verify Installation

After installation, verify that FReview is working globally:

```bash
# Check version (works from any directory)
freview --version

# Show help (works from any directory)  
freview --help

# Test on a project (run from anywhere)
freview review /path/to/your/flask/project
```

## 💻 Usage

### Basic Usage
```bash
freview review path_to_flask_project
```

### Advanced Options
```bash
# Generate reports in multiple formats
freview review myproject --markdown --json --output-dir reports/

# Skip specific analysis areas
freview review myproject --skip-api --skip-db

# Verbose output for debugging
freview review myproject --verbose

# Analyze only specific components
freview review myproject --skip-structure --skip-models  # API & DB only
```

### Available Options
- `--markdown, -m`: Generate Markdown report
- `--json, -j`: Generate JSON report  
- `--output-dir, -o`: Specify output directory for reports
- `--verbose, -v`: Enable verbose output
- `--skip-structure`: Skip project structure analysis
- `--skip-models`: Skip SQLAlchemy model analysis
- `--skip-api`: Skip API pattern analysis
- `--skip-db`: Skip database analysis

### What FReview Analyzes:

• 🏗️ **Project Structure**: Entry points, organization, configuration
• 🧠 **SQLAlchemy Models**: Definitions, relationships, best practices  
• 🌐 **API Patterns**: Routes, blueprints, REST conventions, security
• �️ **Database**: Migrations, configurations, query patterns
• 📊 **Comprehensive Reports**: Actionable insights and recommendations

## 📊 Report Output

After scanning, you'll find detailed analysis results in your terminal with color-coded insights:

```
🔍 Reviewing Flask Project
📁 Project Path: /home/user/my-flask-app

🏗️ Project Structure Analysis
✅ Structure looks good
✅ Found app.py entry point
✅ Configuration management detected

🧠 SQLAlchemy Model Analysis

📄 models/user.py
✅ User: Core model requirements satisfied
✅ User: Uses foreign key constraints (2 found)
✅ User: Defines relationships (3 found)
ℹ️  User: Consider adding __repr__ method for better debugging

📄 models/post.py
❌ Post: Missing __tablename__ attribute
⚠️  Post: Class name should be PascalCase
🔐 Post: Consider adding input validation

🌐 API Pattern Analysis

📄 views/auth.py
✅ Found 5 route(s) in auth.py
✅ Good: Project uses 3 blueprint(s)
⚠️  Route 'delete_user' should include error handling
🔐 Route 'admin_panel' may need authentication

🗄️ Database Analysis

📄 MIGRATIONS
✅ Found 12 migration file(s)
✅ Alembic configuration file present
⚠️  Migration 003_add_indexes.py contains potentially dangerous operation

📄 config.py
✅ Database URI configuration present
🔐 Warning: Potential hardcoded database credentials
💡 Use environment variables: os.environ.get('DATABASE_URL')

📝 Saved Markdown report: review_report.md
📄 Saved JSON report: review_report.json
```

### Report Formats

#### Console Output
- **Rich terminal display** with colors and emojis
- **Real-time progress** indicators
- **Categorized findings** by analysis area

#### Markdown Report (`--markdown`)
- **Structured documentation** with sections for each analysis area
- **Actionable recommendations** and best practices
- **Code examples** and implementation guides
- **Priority-based issue categorization**

#### JSON Report (`--json`)
- **Machine-readable format** for CI/CD integration
- **Detailed metadata** for each finding
- **Programmatic access** to analysis results
- **Custom tooling integration** support

## � What's New in v2.0

### 🌐 API Pattern Analysis
- **Route Detection**: Automatically finds Flask routes and blueprints
- **REST Compliance**: Validates REST API conventions and best practices
- **Security Review**: Checks authentication, input validation, and error handling
- **Architecture Analysis**: Reviews API versioning, blueprint organization

### 🗄️ Database Analysis  
- **Migration Management**: Validates Alembic/Flask-Migrate setup
- **Configuration Security**: Detects hardcoded credentials and security issues
- **Performance Optimization**: Identifies N+1 queries and indexing opportunities
- **Connection Analysis**: Reviews database pooling and connection settings

### 📈 Enhanced Reporting
- **Multi-format Output**: Console, Markdown, and JSON reports
- **Actionable Insights**: Specific recommendations with implementation guides
- **Priority Classification**: Error, warning, and informational categorization
- **Cross-component Analysis**: Identifies relationships between different areas

## �🛠️ Exception Handling

FReview gracefully handles various scenarios:

• ❌ **Missing Dependencies**: Continues analysis when optional components are unavailable
• 📁 **Invalid Structure**: Provides guidance for incomplete or non-standard project layouts  
• 🔧 **Flexible Analysis**: Individual analysis components can be skipped via CLI options
• 🚨 **Error Recovery**: Detailed error reporting with suggestions for resolution

## 📝 Important Notes

> ⚠️ **Disclaimer:** FReview is designed for code reviews and educational purposes, not as a definitive standard for production readiness.

> 💡 **Purpose:** It serves as a helpful starting point for evaluating code quality and establishing best practices in your team's codebase.

> � **Continuous Improvement:** Regular updates include new analysis patterns and enhanced detection capabilities.

## 🎉 Happy Reviewing!

Found this helpful? Give it a ⭐ on GitHub!

### 🔧 Installation Troubleshooting

If you encounter issues during installation:

**Command not found after installation:**

```bash
# Restart your terminal or reload your shell configuration
source ~/.bashrc    # For bash
source ~/.zshrc     # For zsh
```

**Permission errors with pip:**

```bash
# Use --user flag to install in user directory
pip install --user git+https://github.com/Chatelo/freview.git
```

**Python version compatibility:**

• Minimum required: Python 3.9+
• Check your version: `python --version`

**For corporate networks:**

```bash
# If behind proxy, configure git and pip accordingly
git config --global http.proxy http://proxy:port
pip install --proxy http://proxy:port --user git+https://github.com/Chatelo/freview.git
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

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and releases.