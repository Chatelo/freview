# 🔍 FReview

**Automated Code Review Tool for Flask Projects**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Compatible-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

A comprehensive code review tool for Flask applications that analyzes project structure and SQLAlchemy models to ensure best practices and identify potential issues.

## ✨ Features

| Tool | Purpose | Status |
|------|---------|--------|
| 🏗️ Project Structure | Validates Flask project organization and required files | ✅ |
| 🧠 SQLAlchemy Models | Deep analysis of model definitions, relationships, and constraints | ✅ |
| 📝 Multiple Output | Console output with optional Markdown/JSON reports | ✅ |
| 🎨 Rich Terminal UI | Beautiful, colored output with emojis and formatting | ✅ |

## 🚀 Installation

FReview can be installed globally on your machine using multiple methods. Choose the one that works best for your setup:

### 🎯 Method 1: One-Line Installation (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/Chatelo/freview/main/install_freview.sh | bash
```

This script automatically detects the best installation method available on your system.

### ⚡ Method 2: Using uv

```bash
uv tool install git+https://github.com/Chatelo/freview.git
```

Best for: Fast installation with modern Python tooling

### 🔧 Method 3: Using pipx (Recommended for CLI tools)

```bash
pipx install git+https://github.com/Chatelo/freview.git
```

Best for: Global CLI tool installation with isolated dependencies

### 📦 Method 4: Using pip

```bash
pip install --user git+https://github.com/Chatelo/freview.git
```

Best for: Traditional Python package installation

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

After installation, verify that FReview is working:

```bash
freview --version
freview --help
```

## 💻 Usage

```bash
freview review path_to_flask_project
```

### What FReview Does:

• 🔍 Analyzes project structure
• 🧠 Reviews SQLAlchemy models  
• 📊 Generates comprehensive reports

## 📊 Report Output

After scanning, you'll find detailed analysis results in your terminal:

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

## 🛠️ Exception Handling

FReview gracefully handles various scenarios:

• ❌ Missing Tools: When analysis dependencies are not available
• 📁 Invalid Structure: When directory structure is incomplete or invalid  
• 🔧 Flexible Analysis: Continues analysis even when some checks fail

## 📝 Important Notes

> ⚠️ **Disclaimer:** FReview is designed for code reviews and educational purposes, not as a definitive standard for production readiness.

> 💡 **Purpose:** It serves as a helpful starting point for evaluating code quality and establishing best practices in your team's codebase.

## 🚀 Future Enhancements

We're planning to expand FReview with additional features:

• 📄 Configuration Files: Enhanced validation for Flask configs
• ⚠️ Error Handling: Proper error handler detection
• 🔒 Security Controls: Enhanced security validations  
• 📑 Interactive Reports: Beautiful web-based report output

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

### v1.0.0
- Initial release
- Basic project structure analysis
- SQLAlchemy model validation
- Markdown report generation