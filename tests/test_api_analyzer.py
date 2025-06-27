"""
Tests for API analysis functionality.
"""

from pathlib import Path
from freview.api_analyzer import analyze_api_patterns, APIVisitor
import ast


def test_analyze_basic_api(temp_project):
    """Test analysis of basic API routes."""
    # Create a basic API file
    (temp_project / "app.py").write_text(
        """
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    \"\"\"Get all users.\"\"\"
    return jsonify({"users": []})

@app.route('/api/users', methods=['POST'])
def create_user():
    \"\"\"Create a new user.\"\"\"
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
"""
    )

    results = analyze_api_patterns(temp_project)
    
    # Should find the API file
    assert len(results) >= 1
    
    # Should find routes
    app_py_results = None
    for file_path, issues in results.items():
        if isinstance(file_path, Path) and file_path.name == "app.py":
            app_py_results = issues
            break
    
    assert app_py_results is not None
    
    # Should have positive results for good practices
    success_issues = [i for i in app_py_results if i.startswith("✅")]
    assert len(success_issues) > 0


def test_analyze_blueprint_api(temp_project):
    """Test analysis of blueprint-based API."""
    # Create blueprints directory
    blueprints_dir = temp_project / "blueprints"
    blueprints_dir.mkdir()
    
    # Create a blueprint file
    (blueprints_dir / "auth_bp.py").write_text(
        """
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Missing input validation
    return jsonify({"token": "fake_token"})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Missing authentication check
    return jsonify({"message": "Logged out"})
"""
    )

    results = analyze_api_patterns(temp_project)
    
    # Should find the blueprint file
    assert len(results) >= 1
    
    # Should find issues
    blueprint_results = None
    for file_path, issues in results.items():
        if isinstance(file_path, Path) and "auth_bp.py" in str(file_path):
            blueprint_results = issues
            break
    
    assert blueprint_results is not None
    
    # Should find blueprint
    blueprint_found = any("blueprint" in issue.lower() for issue in blueprint_results)
    assert blueprint_found


def test_analyze_api_with_issues(temp_project):
    """Test analysis of API with various issues."""
    (temp_project / "bad_api.py").write_text(
        """
from flask import Flask

app = Flask(__name__)

@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # No authentication, no error handling, no validation
    # This is a dangerous operation
    return "User deleted"

@app.route('/admin/settings', methods=['POST'])
def admin_settings():
    # Admin route without authentication
    return "Settings updated"
"""
    )

    results = analyze_api_patterns(temp_project)
    
    # Should find issues
    assert len(results) >= 1
    
    # Should flag authentication issues
    issues = list(results.values())[0]
    auth_issues = [i for i in issues if "authentication" in i.lower()]
    assert len(auth_issues) > 0


def test_api_visitor_basic():
    """Test basic APIVisitor functionality."""
    code = """
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/test', methods=['GET', 'POST'])
def test_route():
    '''Test route with docstring'''
    return "OK"
"""

    visitor = APIVisitor(Path("test.py"))
    tree = ast.parse(code)
    visitor.visit(tree)

    # Should find one route
    assert len(visitor.routes) == 1
    route = visitor.routes[0]
    assert route.path == '/test'
    assert 'GET' in route.methods
    assert 'POST' in route.methods
    assert route.has_docstring

    # Should find one blueprint
    assert len(visitor.blueprints) == 1
    blueprint = visitor.blueprints[0]
    assert blueprint.name == 'api'
    assert blueprint.url_prefix == '/api'


def test_no_api_routes_found(temp_project):
    """Test behavior when no API routes are found."""
    # Create a file without routes
    (temp_project / "models.py").write_text(
        """
from flask_sqlalchemy import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
"""
    )

    results = analyze_api_patterns(temp_project)
    
    # Should return a message about no routes found
    assert len(results) == 1
    issues = list(results.values())[0]
    assert any("No Flask route files found" in issue for issue in issues)
