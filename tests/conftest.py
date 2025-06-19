"""
Test configuration and fixtures for freview tests.
"""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from freview.config import ReviewConfig


@pytest.fixture
def temp_project():
    """Create a temporary project directory for testing."""
    with TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / "test_project"
        project_path.mkdir()
        yield project_path


@pytest.fixture
def sample_flask_project(temp_project):
    """Create a sample Flask project structure."""
    # Create basic structure
    (temp_project / "app.py").write_text(
        """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
"""
    )

    # Create models directory
    models_dir = temp_project / "models"
    models_dir.mkdir()
    (models_dir / "__init__.py").write_text("")

    # Create a sample model
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
"""
    )

    # Create templates directory
    (temp_project / "templates").mkdir()

    # Create static directory
    (temp_project / "static").mkdir()

    return temp_project


@pytest.fixture
def default_config():
    """Return a default ReviewConfig instance."""
    return ReviewConfig()
