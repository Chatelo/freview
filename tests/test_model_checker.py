"""
Tests for model analysis functionality.
"""

from pathlib import Path
from freview.model_checker import analyze_models, ModelVisitor
import ast


def test_analyze_good_model(temp_project):
    """Test analysis of a well-structured model."""
    models_dir = temp_project / "models"
    models_dir.mkdir()

    # Create a good model
    (models_dir / "user.py").write_text(
        """
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
        
    def __str__(self):
        return self.username
"""
    )

    results = analyze_models(temp_project)

    # Should find the model file
    assert len(results) == 1

    # Should have mostly positive results
    issues = list(results.values())[0]
    success_issues = [i for i in issues if i.startswith("✅")]
    assert len(success_issues) > 0


def test_analyze_bad_model(temp_project):
    """Test analysis of a poorly structured model."""
    models_dir = temp_project / "models"
    models_dir.mkdir()

    # Create a bad model
    (models_dir / "bad_model.py").write_text(
        """
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class badModel(db.Model):  # Bad naming
    # Missing __tablename__
    
    username = db.Column(db.String(80))  # No primary key
"""
    )

    results = analyze_models(temp_project)

    # Should find issues
    assert len(results) == 1
    issues = list(results.values())[0]

    # Should have naming issue
    naming_issues = [i for i in issues if "PascalCase" in i]
    assert len(naming_issues) > 0

    # Should have missing __tablename__ issue
    tablename_issues = [i for i in issues if "__tablename__" in i]
    assert len(tablename_issues) > 0

    # Should have missing primary key issue
    pk_issues = [i for i in issues if "primary key" in i]
    assert len(pk_issues) > 0


def test_model_visitor_basic():
    """Test basic ModelVisitor functionality."""
    code = """
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
"""

    visitor = ModelVisitor(Path("test.py"))
    tree = ast.parse(code)
    visitor.visit(tree)

    # Should find one model
    assert len(visitor.models) == 1
    assert visitor.models[0].name == "User"
    assert visitor.models[0].has_tablename
    assert visitor.models[0].has_primary_key


def test_no_models_found(temp_project):
    """Test behavior when no models are found."""
    results = analyze_models(temp_project)

    # Should return a message about no models found
    assert len(results) == 1
    issues = list(results.values())[0]
    assert any("No Python model files found" in issue for issue in issues)
