# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-06-27

### 🚀 Major Release - Comprehensive Analysis Platform

This release transforms FReview from a basic structure and model checker into a comprehensive Flask project analysis platform.

### 🌟 Major New Features

#### 🌐 API Pattern Analysis
- **NEW**: Flask route detection and analysis
- **NEW**: Blueprint organization validation  
- **NEW**: REST API convention checking
- **NEW**: HTTP method usage pattern analysis
- **NEW**: Authentication and authorization validation
- **NEW**: Input validation and error handling checks
- **NEW**: API versioning detection and recommendations
- **NEW**: Security vulnerability detection in routes

#### 🗄️ Database Analysis
- **NEW**: Alembic/Flask-Migrate setup validation
- **NEW**: Migration file analysis and safety checks
- **NEW**: Database configuration security review
- **NEW**: Connection pooling and performance settings analysis
- **NEW**: Query pattern detection (N+1 queries, etc.)
- **NEW**: Index usage and optimization suggestions  
- **NEW**: Hardcoded credential detection

#### 📈 Enhanced Reporting & CLI
- **NEW**: Multi-format output (Console, Markdown, JSON)
- **NEW**: Selective analysis with skip options (`--skip-api`, `--skip-db`, etc.)
- **NEW**: Enhanced CLI with comprehensive options
- **NEW**: Actionable recommendations with implementation guides
- **NEW**: Cross-component analysis and relationship detection

### 🛠️ Improvements

#### Enhanced Model Analysis
- **IMPROVED**: More sophisticated relationship analysis
- **IMPROVED**: Better circular dependency detection
- **IMPROVED**: Enhanced model validation patterns

#### Better Project Structure Analysis  
- **IMPROVED**: More comprehensive directory validation
- **IMPROVED**: Configuration management detection
- **IMPROVED**: Testing setup validation

#### User Experience
- **IMPROVED**: Richer terminal output with better categorization
- **IMPROVED**: More descriptive error messages and suggestions
- **IMPROVED**: Performance optimizations for large projects

### 🔧 Technical Changes
- **ADDED**: New `api_analyzer.py` module with comprehensive route analysis
- **ADDED**: New `database_analyzer.py` module with migration and config analysis
- **ENHANCED**: `cli.py` with new command options and better progress tracking
- **ENHANCED**: `utils.py` with multi-format report generation
- **UPDATED**: All documentation to reflect new capabilities

### 📖 Documentation
- **UPDATED**: README.md with comprehensive feature documentation
- **UPDATED**: CLI help text and command descriptions
- **ADDED**: Detailed usage examples and advanced options
- **ADDED**: Report format specifications and examples

### ⚡ Breaking Changes
- **CLI**: New default behavior includes API and database analysis
- **Reports**: Enhanced report format with additional sections
- **Output**: More verbose console output by default

### 🔄 Migration Guide from v1.x
To upgrade from v1.x:
1. The core functionality remains the same
2. New analysis areas are enabled by default
3. Use `--skip-api --skip-db` to get v1.x-like behavior
4. Report formats have been enhanced but remain compatible

## [1.0.0] - 2025-06-19

### Added
- Initial release of FReview - Flask code review tool
- Project structure analysis for Flask applications
- SQLAlchemy model validation and best practices checking
- Multiple output formats (console, Markdown, JSON reports)
- Rich terminal UI with colored output and emojis
- Multiple installation methods:
  - One-line installation script
  - pipx installation (recommended for CLI tools)
  - uv installation (fast modern tooling)
  - pip installation (traditional method)
  - Manual installation script with method selection
  - Development installation for contributors
- Comprehensive error handling and graceful failure modes
- Support for Python 3.9+ versions
- MIT License

### Features
- 🏗️ **Project Structure Validation**: Ensures proper Flask project organization
- 🧠 **SQLAlchemy Model Analysis**: Deep inspection of model definitions, relationships, and constraints
- 📝 **Multiple Output Formats**: Console, Markdown, and JSON report generation
- 🎨 **Rich Terminal UI**: Beautiful colored output with emojis and professional formatting
- ⚡ **Fast Analysis**: Efficient code scanning and review process
- 🛠️ **Flexible Configuration**: Adaptable to different project structures
- 📊 **Detailed Reports**: Comprehensive analysis with actionable insights

### Documentation
- Complete README.md with installation and usage instructions
- Contributing guidelines (CONTRIBUTING.md)
- MIT License file
- Installation script with auto-detection capabilities
- Comprehensive test suite with pytest

### Dependencies
- typer>=0.9.0 (CLI framework)
- rich>=10.0.0 (terminal formatting)

### Supported Python Versions
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

[Unreleased]: https://github.com/Chatelo/freview/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Chatelo/freview/releases/tag/v1.0.0
