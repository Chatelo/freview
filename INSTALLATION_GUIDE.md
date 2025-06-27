# FReview Installation & Version Guide

## 🌟 Global Installation - Available Everywhere

FReview installs **globally** on your system. After installation, the `freview` command works from any directory, allowing you to analyze Flask projects anywhere on your system.

## 🚀 Quick Start (Latest Version)

```bash
# Install latest FReview v2.x globally (recommended)
uv tool install git+https://github.com/Chatelo/freview.git

# Or using pipx (also global installation)
pipx install git+https://github.com/Chatelo/freview.git

# Verify global installation - works from any directory
cd /tmp
freview --version  # Should show v2.0.0+

# Test global access
freview review /path/to/any/flask/project
```

## 📋 Version Comparison

| Feature | v1.x (Legacy) | v2.x (Current) |
|---------|---------------|----------------|
| **Project Structure Analysis** | ✅ | ✅ Enhanced |
| **SQLAlchemy Model Analysis** | ✅ | ✅ Enhanced |
| **API Pattern Analysis** | ❌ | ✅ **NEW** |
| **Database Analysis** | ❌ | ✅ **NEW** |
| **Multi-format Reports** | Console only | Console + Markdown + JSON |
| **Selective Analysis** | ❌ | ✅ Skip options |
| **Rich CLI Options** | Basic | ✅ Comprehensive |

## 🔄 Installation Options

### Latest Version (v2.x) - Recommended
```bash
# Install latest comprehensive version
uv tool install git+https://github.com/Chatelo/freview.git

# Usage with full analysis
freview review myproject

# Usage with v1.x-like behavior  
freview review myproject --skip-api --skip-db
```

### Legacy Version (v1.x) - Maintenance Only
```bash
# Install v1.x maintenance version
uv tool install git+https://github.com/Chatelo/freview.git@v1.x-maintenance

# Or specific v1.x version
uv tool install git+https://github.com/Chatelo/freview.git@v1.0.1
```

### Specific Version
```bash
# Install exact version
uv tool install git+https://github.com/Chatelo/freview.git@v2.0.0

# Upgrade existing installation
uv tool upgrade freview
```

## 💻 Global Usage Examples

Since FReview is installed globally, you can use it from anywhere:

### v2.x Full Analysis (Default) - From Any Directory
```bash
# Analyze from any location
cd /tmp
freview review ~/my-flask-project

# Analyze current directory
cd /my/project
freview review .

# Analyze with full path from anywhere
freview review /home/user/flask-apps/api-server
```

### v2.x Selective Analysis - Global Access
```bash
# Models and structure only (v1.x-like) - works from anywhere
freview review /path/to/project --skip-api --skip-db

# API and database only - global command
freview review ~/flask-app --skip-structure --skip-models

# Everything except API - run from any directory
freview review /var/www/flask-site --skip-api
```

### v2.x Report Generation - Global Output
```bash
# Generate reports to any location
mkdir /tmp/analysis-reports
freview review ~/project --markdown --json --output-dir /tmp/analysis-reports

# Console only from anywhere (default)
freview review /path/to/any/flask/project

# Verbose output with global access
freview review ~/my-apps/flask-api --verbose
```

## 🛠️ Migration from v1.x to v2.x

### Option 1: Upgrade and Use Skip Flags
```bash
# Uninstall v1.x
uv tool uninstall freview

# Install v2.x
uv tool install git+https://github.com/Chatelo/freview.git

# Use with v1.x behavior
freview review myproject --skip-api --skip-db
```

### Option 2: Keep v1.x for Legacy Projects
```bash
# Install v1.x as freview-legacy (if needed)
uv tool install --force git+https://github.com/Chatelo/freview.git@v1.x-maintenance

# Install v2.x for new projects
uv tool install git+https://github.com/Chatelo/freview.git
```

### Option 3: Project-Specific Installation
```bash
# For legacy projects
cd legacy-project
uv run --from git+https://github.com/Chatelo/freview.git@v1.x-maintenance freview review .

# For new projects  
cd new-project
uv run --from git+https://github.com/Chatelo/freview.git freview review .
```

## 🔧 CI/CD Integration

### GitHub Actions Example
```yaml
name: Code Review
on: [push, pull_request]

jobs:
  freview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Install specific version for reproducible builds
      - name: Install FReview
        run: uv tool install git+https://github.com/Chatelo/freview.git@v2.0.0
        
      # Run comprehensive analysis
      - name: Run FReview
        run: freview review . --json --output-dir reports/
        
      # Upload reports as artifacts
      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: freview-reports
          path: reports/
```

### Docker Integration
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install FReview
RUN pip install uv && \
    uv tool install git+https://github.com/Chatelo/freview.git@v2.0.0

# Copy project
COPY . /app
WORKDIR /app

# Run analysis
CMD ["freview", "review", ".", "--json", "--output-dir", "/reports"]
```

## 🚨 Troubleshooting

### Version Conflicts
```bash
# Check current version
freview --version

# Uninstall and reinstall
uv tool uninstall freview
uv tool install git+https://github.com/Chatelo/freview.git

# Clear tool cache if needed
uv cache clean
```

### Command Not Found
```bash
# Ensure uv tools are in PATH
echo 'export PATH="$HOME/.local/share/uv/tools/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or use uv run directly
uv run --from git+https://github.com/Chatelo/freview.git freview --version
```

### Legacy Project Support
```bash
# If v2.x doesn't work well with old project
uv tool install git+https://github.com/Chatelo/freview.git@v1.x-maintenance

# Or use skip flags
freview review . --skip-api --skip-db --skip-structure
```

## 📞 Support

- **Documentation**: [README.md](README.md)
- **Version History**: [CHANGELOG.md](CHANGELOG.md)  
- **Version Management**: [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)
- **Issues**: [GitHub Issues](https://github.com/Chatelo/freview/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/Chatelo/freview/discussions)

## 🔗 Quick Links

- **Latest Release**: [v2.0.0](https://github.com/Chatelo/freview/releases/tag/v2.0.0)
- **Legacy Branch**: [v1.x-maintenance](https://github.com/Chatelo/freview/tree/v1.x-maintenance)
- **Installation Script**: [install_freview.sh](install_freview.sh)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
