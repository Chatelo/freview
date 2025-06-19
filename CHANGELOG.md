# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Reordered installation methods in README.md - uv method is now the 2nd installation option

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
