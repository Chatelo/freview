# Version Management Guide

This document outlines how to manage versions of FReview and maintain backward compatibility.

## 📋 Version Strategy

FReview follows [Semantic Versioning (SemVer)](https://semver.org/):

- **MAJOR** version (X.0.0): Breaking changes, new architecture
- **MINOR** version (0.X.0): New features, backward compatible
- **PATCH** version (0.0.X): Bug fixes, backward compatible

## 🏷️ Current Release Strategy

### Version 2.0.0 (Current)
- **Comprehensive Analysis Platform**: Added API and Database analysis
- **Enhanced CLI**: New options and selective analysis capabilities  
- **Multi-format Reports**: Console, Markdown, and JSON output
- **Breaking Changes**: Enhanced default behavior and report formats

### Version 1.x (Legacy)
- **Basic Analysis**: Project structure and SQLAlchemy models only
- **Simple CLI**: Basic review command with minimal options
- **Console Output**: Rich terminal display only

## 🔄 Maintaining Version Compatibility

### Git Branch Strategy

```bash
# Main development branch
main                    # Latest development (v2.x)

# Version branches  
v1.x-maintenance       # v1.x maintenance and bug fixes
v2.x-stable           # v2.x stable releases

# Release tags
v1.0.0, v1.1.0, v1.2.0   # v1.x releases
v2.0.0, v2.1.0, v2.2.0   # v2.x releases
```

### Global Installation by Version

FReview installs globally and becomes available system-wide with the `freview` command:

```bash
# Latest version (v2.x) - installs globally
uv tool install git+https://github.com/Chatelo/freview.git

# Specific version - installs globally  
uv tool install git+https://github.com/Chatelo/freview.git@v2.0.0

# Legacy v1.x (maintenance branch) - installs globally
uv tool install git+https://github.com/Chatelo/freview.git@v1.x-maintenance

# Specific legacy version - installs globally
uv tool install git+https://github.com/Chatelo/freview.git@v1.2.0

# Alternative with pipx (also global installation)
pipx install git+https://github.com/Chatelo/freview.git@v2.0.0
```

After installation, `freview` command is available globally from any directory.

## 🛠️ Developer Guide

### Creating New Releases

#### For Major Releases (X.0.0)
1. **Update version numbers** in multiple files:
   ```bash
   # Update version in pyproject.toml
   sed -i 's/version = ".*"/version = "2.0.0"/' pyproject.toml
   
   # Update version in __init__.py
   sed -i 's/__version__ = ".*"/__version__ = "2.0.0"/' freview/__init__.py
   ```

2. **Update documentation**:
   - README.md feature descriptions
   - CHANGELOG.md with detailed changes
   - CLI help text and descriptions

3. **Create release branch and tag**:
   ```bash
   git checkout -b release/v2.0.0
   git add .
   git commit -m "Release v2.0.0: Comprehensive analysis platform"
   git tag -a v2.0.0 -m "Version 2.0.0 - Major feature release"
   git push origin v2.0.0
   ```

#### For Minor Releases (0.X.0)
1. Update version numbers
2. Update CHANGELOG.md
3. Tag and release:
   ```bash
   git tag -a v2.1.0 -m "Version 2.1.0 - New features"
   git push origin v2.1.0
   ```

#### For Patch Releases (0.0.X)
1. Update version numbers
2. Update CHANGELOG.md with bug fixes
3. Tag and release:
   ```bash
   git tag -a v2.0.1 -m "Version 2.0.1 - Bug fixes"
   git push origin v2.0.1
   ```

### Maintaining Legacy Versions

#### v1.x Maintenance
For critical bug fixes in v1.x:

```bash
# Switch to maintenance branch
git checkout v1.x-maintenance

# Apply fixes
git cherry-pick <commit-hash>  # or manual fixes

# Update version (patch only)
sed -i 's/__version__ = "1\..*"/__version__ = "1.2.1"/' freview/__init__.py

# Release
git tag -a v1.2.1 -m "Version 1.2.1 - Critical bug fixes"
git push origin v1.2.1
```

## 📦 Distribution Strategy

### Multiple Installation Channels

All installation methods provide **global access** to the `freview` command:

#### Latest Version (Default)
```bash
# Always installs latest from main branch globally
uv tool install git+https://github.com/Chatelo/freview.git
pipx install git+https://github.com/Chatelo/freview.git
```

#### Version-Specific Installation
```bash
# Install specific version globally
uv tool install git+https://github.com/Chatelo/freview.git@v2.0.0

# Install from maintenance branch globally (gets latest patches)
uv tool install git+https://github.com/Chatelo/freview.git@v1.x-maintenance
```

#### PyPI Distribution (Future)
When published to PyPI:
```bash
# Latest version - global installation
pip install freview

# Specific version - global installation
pip install freview==2.0.0

# Version range - global installation
pip install "freview>=1.0,<2.0"  # v1.x only
pip install "freview>=2.0"        # v2.x and newer
```

**Note**: All methods install FReview globally. After installation, you can run `freview` from any directory.

## 🔄 Migration Strategies

### v1.x to v2.x Migration

#### For Users Who Want v1.x Behavior
```bash
# Use skip options to get v1.x-like output
freview review myproject --skip-api --skip-db

# Or install v1.x maintenance version
uv tool uninstall freview
uv tool install git+https://github.com/Chatelo/freview.git@v1.x-maintenance
```

#### For CI/CD Pipelines
```bash
# Pin to specific version in CI (installs globally in CI environment)
- name: Install FReview
  run: uv tool install git+https://github.com/Chatelo/freview.git@v2.0.0

# Or use version ranges when PyPI is available (global installation)
- name: Install FReview  
  run: pip install "freview>=2.0,<3.0"

# Then use globally available command
- name: Run Analysis
  run: freview review . --json --output-dir reports/
```

### Configuration-Based Compatibility

Future versions could include config files:

```yaml
# .freview.yml
version_compatibility: "1.x"  # Emulate v1.x behavior
analysis:
  skip_api: true
  skip_database: true
  legacy_output: true
```

## 🚨 Breaking Change Policy

### What Constitutes a Breaking Change
- **CLI Interface Changes**: Removing options, changing defaults
- **Output Format Changes**: Major report structure modifications  
- **API Changes**: Function signatures, return formats (for programmatic use)
- **Minimum Requirements**: Python version, dependency changes

### How We Handle Breaking Changes
1. **Major Version Bump**: Always increment major version
2. **Migration Guide**: Provide clear upgrade instructions
3. **Deprecation Warnings**: Add warnings before removing features
4. **Legacy Support**: Maintain previous major version for critical fixes

## 📋 Release Checklist

### Pre-Release
- [ ] Update version numbers in all files
- [ ] Update CHANGELOG.md with detailed changes
- [ ] Update README.md if features changed
- [ ] Run full test suite
- [ ] Test installation methods
- [ ] Review CLI help text

### Release
- [ ] Create release branch
- [ ] Tag release with proper message
- [ ] Push tags to remote
- [ ] Create GitHub release with notes
- [ ] Update installation script if needed

### Post-Release
- [ ] Verify installation works from tag
- [ ] Update documentation links
- [ ] Announce in appropriate channels
- [ ] Monitor for issues

## 🔗 References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Python Packaging User Guide](https://packaging.python.org/)
