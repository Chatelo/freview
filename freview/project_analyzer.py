from pathlib import Path
from typing import List, Dict
import tomllib


def analyze_project_structure(project_path: Path) -> List[str]:
    """
    Analyze Flask project structure for common patterns and best practices.

    Args:
        project_path: Path to the Flask project root

    Returns:
        List of issues found during analysis
    """
    issues: list[str] = []

    # Check for Flask application entry points
    _check_entry_points(project_path, issues)

    # Check for models organization
    _check_models_structure(project_path, issues)

    # Check for templates and static files
    _check_template_static_structure(project_path, issues)

    # Check for configuration management
    _check_configuration(project_path, issues)

    # Check for blueprints organization
    _check_blueprints_structure(project_path, issues)

    # Check for testing structure
    _check_testing_structure(project_path, issues)

    # Check for documentation
    _check_documentation(project_path, issues)

    return issues


def _check_entry_points(project_path: Path, issues: List[str]) -> None:
    """Check for Flask application entry points."""
    entry_files = ["app.py", "run.py", "main.py", "wsgi.py"]
    app_dirs = ["app", "src", "application"]

    # Check for entry files in root
    found_entry = any((project_path / f).exists() for f in entry_files)

    # Check for entry files in common app directories
    if not found_entry:
        for app_dir in app_dirs:
            app_path = project_path / app_dir
            if app_path.exists() and app_path.is_dir():
                if any((app_path / f).exists() for f in entry_files):
                    found_entry = True
                    break

    if not found_entry:
        issues.append(
            "Missing Flask application entry point: expected one of app.py, run.py, main.py, or wsgi.py"
        )


def _check_models_structure(project_path: Path, issues: List[str]) -> None:
    """Check for SQLAlchemy models organization."""
    model_locations = [
        project_path / "models",
        project_path / "app" / "models",
        project_path / "src" / "models",
        project_path / "application" / "models",
    ]

    models_found = False
    for model_dir in model_locations:
        if model_dir.exists() and model_dir.is_dir():
            models_found = True
            if not (model_dir / "__init__.py").exists():
                issues.append(
                    f"Missing '__init__.py' in '{model_dir.relative_to(project_path)}' directory"
                )
            break

    # Also check for single models.py file
    single_model_files = [
        project_path / "models.py",
        project_path / "app" / "models.py",
        project_path / "src" / "models.py",
    ]

    if not models_found:
        if any(f.exists() for f in single_model_files):
            models_found = True

    if not models_found:
        issues.append(
            "No models directory or models.py file found - consider organizing your SQLAlchemy models"
        )


def _check_template_static_structure(project_path: Path, issues: List[str]) -> None:
    """Check for templates and static files organization."""
    template_locations = [
        project_path / "templates",
        project_path / "app" / "templates",
        project_path / "src" / "templates",
    ]

    static_locations = [
        project_path / "static",
        project_path / "app" / "static",
        project_path / "src" / "static",
    ]

    # Check templates
    if not any(loc.exists() for loc in template_locations):
        issues.append("Missing 'templates/' directory - required for Flask template rendering")

    # Check static files
    if not any(loc.exists() for loc in static_locations):
        issues.append("Missing 'static/' directory - recommended for CSS, JS, and image files")


def _check_configuration(project_path: Path, issues: List[str]) -> None:
    """Check for configuration management."""
    config_files = [
        project_path / "config.py",
        project_path / "settings.py",
        project_path / "app" / "config.py",
        project_path / "src" / "config.py",
    ]

    env_files = [
        project_path / ".env",
        project_path / ".env.example",
        project_path / "environment.yaml",
    ]

    has_config = any(f.exists() for f in config_files)
    has_env = any(f.exists() for f in env_files)

    if not has_config and not has_env:
        issues.append("Missing configuration management - consider adding config.py or .env file")

    # Check for requirements management
    req_files = [
        project_path / "requirements.txt",
        project_path / "pyproject.toml",
        project_path / "Pipfile",
        project_path / "poetry.lock",
    ]

    if not any(f.exists() for f in req_files):
        issues.append(
            "Missing dependency management file - consider adding requirements.txt or pyproject.toml"
        )


def _check_blueprints_structure(project_path: Path, issues: List[str]) -> None:
    """Check for Flask blueprints organization."""
    blueprint_indicators = []

    # Look for common blueprint patterns
    common_dirs = ["views", "blueprints", "api", "admin", "auth"]
    app_dirs = [project_path, project_path / "app", project_path / "src"]

    for app_dir in app_dirs:
        if not app_dir.exists():
            continue

        for bp_dir in common_dirs:
            bp_path = app_dir / bp_dir
            if bp_path.exists() and bp_path.is_dir():
                # Check if directory contains Python files (potential blueprints)
                py_files = list(bp_path.glob("*.py"))
                if py_files:
                    blueprint_indicators.append(bp_path)

    # This is informational rather than an issue
    if blueprint_indicators:
        # Could be enhanced to actually verify blueprint registration
        pass  # Not adding as issue since blueprints are optional


def _check_testing_structure(project_path: Path, issues: List[str]) -> None:
    """Check for testing setup."""
    test_locations = [
        project_path / "tests",
        project_path / "test",
        project_path / "testing",
    ]

    test_files = list(project_path.rglob("test_*.py")) + list(project_path.rglob("*_test.py"))

    has_test_dir = any(loc.exists() and loc.is_dir() for loc in test_locations)
    has_test_files = len(test_files) > 0

    if not has_test_dir and not has_test_files:
        issues.append(
            "No testing structure found - consider adding a 'tests/' directory with test files"
        )


def _check_documentation(project_path: Path, issues: List[str]) -> None:
    """Check for basic documentation."""
    doc_files = [
        project_path / "README.md",
        project_path / "README.rst",
        project_path / "README.txt",
        project_path / "docs" / "README.md",
    ]

    if not any(f.exists() for f in doc_files):
        issues.append("Missing README file - consider adding project documentation")


def get_project_info(project_path: Path) -> Dict[str, any]:
    """
    Extract project information for enhanced analysis.

    Returns:
        Dictionary containing project metadata
    """
    info = {
        "name": project_path.name,
        "path": str(project_path),
        "python_files": list(project_path.rglob("*.py")),
        "has_flask": False,
        "flask_version": None,
        "dependencies": [],
        "structure_type": "unknown",
    }

    # Check for Flask imports in Python files
    flask_patterns = ["from flask import", "import flask"]
    for py_file in info["python_files"][:10]:  # Check first 10 files for performance
        try:
            content = py_file.read_text(encoding="utf-8")
            if any(pattern in content for pattern in flask_patterns):
                info["has_flask"] = True
                break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Try to read dependencies
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        try:
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
                deps = pyproject.get("project", {}).get("dependencies", [])
                info["dependencies"] = deps
        except Exception:
            pass

    requirements_path = project_path / "requirements.txt"
    if requirements_path.exists():
        try:
            info["dependencies"] = requirements_path.read_text().strip().split("\n")
        except Exception:
            pass

    # Determine structure type
    if (project_path / "app").exists():
        info["structure_type"] = "application_factory"
    elif (project_path / "src").exists():
        info["structure_type"] = "src_layout"
    else:
        info["structure_type"] = "simple"

    return info
