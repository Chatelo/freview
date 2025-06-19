"""
Tests for project structure analysis.
"""

import pytest
from freview.project_analyzer import analyze_project_structure


def test_analyze_complete_project(sample_flask_project):
    """Test analysis of a complete Flask project."""
    issues = analyze_project_structure(sample_flask_project)

    # Should have some issues since we're not creating all the files in fixture
    assert len(issues) >= 2  # Will have recommendations for missing files

    # Should not complain about missing entry point
    entry_issues = [i for i in issues if "entry point" in i.lower()]
    assert len(entry_issues) == 0

    # Should not complain about missing models
    model_issues = [i for i in issues if "models" in i.lower()]
    assert len(model_issues) == 0


def test_analyze_minimal_project(temp_project):
    """Test analysis of a minimal project."""
    # Create just an app.py file
    (temp_project / "app.py").write_text("from flask import Flask\napp = Flask(__name__)")

    issues = analyze_project_structure(temp_project)

    # Should have several issues for missing components
    assert len(issues) > 0

    # Should complain about missing models
    model_issues = [i for i in issues if "models" in i.lower()]
    assert len(model_issues) > 0


def test_analyze_empty_project(temp_project):
    """Test analysis of an empty project."""
    issues = analyze_project_structure(temp_project)

    # Should have many issues for missing everything
    assert len(issues) > 3

    # Should complain about missing entry point
    entry_issues = [i for i in issues if "entry point" in i.lower()]
    assert len(entry_issues) > 0

    # Should complain about missing templates
    template_issues = [i for i in issues if "templates" in i.lower()]
    assert len(template_issues) > 0


def test_analyze_blueprint_structure(temp_project):
    """Test detection of blueprint structure."""
    # Create app with blueprints
    (temp_project / "app.py").write_text("from flask import Flask\napp = Flask(__name__)")

    # Create blueprints directory
    blueprints_dir = temp_project / "blueprints"
    blueprints_dir.mkdir()
    (blueprints_dir / "auth.py").write_text(
        "from flask import Blueprint\nauth = Blueprint('auth', __name__)"
    )

    issues = analyze_project_structure(temp_project)

    # Should still work with blueprint structure
    assert isinstance(issues, list)
