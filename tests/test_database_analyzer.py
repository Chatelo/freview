"""
Tests for database analysis functionality.
"""

from pathlib import Path
from freview.database_analyzer import analyze_database_patterns


def test_analyze_migrations(temp_project):
    """Test analysis of database migrations."""
    # Create migrations directory structure
    migrations_dir = temp_project / "migrations"
    migrations_dir.mkdir()
    
    # Create env.py
    (migrations_dir / "env.py").write_text(
        """
from alembic import context
from sqlalchemy import engine_from_config

def run_migrations():
    pass
"""
    )
    
    # Create versions directory with a migration
    versions_dir = migrations_dir / "versions"
    versions_dir.mkdir()
    
    (versions_dir / "001_initial_migration.py").write_text(
        """
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(80), nullable=False)
    )

def downgrade():
    op.drop_table('users')
"""
    )
    
    # Create alembic.ini
    (temp_project / "alembic.ini").write_text(
        """
[alembic]
script_location = migrations
sqlalchemy.url = sqlite:///test.db
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should find migrations analysis
    assert len(results) >= 1
    
    # Should have positive results for good migration setup
    migration_results = None
    for file_path, issues in results.items():
        if "migrations" in str(file_path).lower():
            migration_results = issues
            break
    
    assert migration_results is not None
    success_issues = [i for i in migration_results if i.startswith("✅")]
    assert len(success_issues) > 0


def test_analyze_database_config(temp_project):
    """Test analysis of database configuration."""
    # Create config file with good database settings
    (temp_project / "config.py").write_text(
        """
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 20
    SQLALCHEMY_MAX_OVERFLOW = 30
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should find config analysis
    assert len(results) >= 1
    
    # Should find good configuration practices
    config_results = None
    for file_path, issues in results.items():
        if isinstance(file_path, Path) and file_path.name == "config.py":
            config_results = issues
            break
    
    assert config_results is not None
    
    # Should detect good practices
    good_practices = [i for i in config_results if i.startswith("✅")]
    assert len(good_practices) > 0


def test_analyze_bad_database_config(temp_project):
    """Test analysis of problematic database configuration."""
    # Create config with hardcoded credentials
    (temp_project / "config.py").write_text(
        """
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password123@localhost/mydb'
    # Missing other important settings
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should find issues
    config_results = None
    for file_path, issues in results.items():
        if isinstance(file_path, Path) and file_path.name == "config.py":
            config_results = issues
            break
    
    assert config_results is not None
    
    # Should flag security issues
    security_issues = [i for i in config_results if "hardcoded" in i.lower()]
    assert len(security_issues) > 0


def test_analyze_database_usage(temp_project):
    """Test analysis of database usage patterns."""
    # Create a file with database operations
    (temp_project / "services.py").write_text(
        """
from flask_sqlalchemy import db
from app.models import User

def get_users():
    return User.query.all()

def create_user(username):
    try:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

def bulk_create_users(users_data):
    # Good: using bulk operations
    db.session.bulk_insert_mappings(User, users_data)
    db.session.commit()
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should find database usage
    assert len(results) >= 1
    
    # Should find at least some analysis
    total_issues = sum(len(issues) for issues in results.values())
    assert total_issues > 0


def test_analyze_problematic_database_usage(temp_project):
    """Test analysis of problematic database usage."""
    # Create a file with potential N+1 query problem
    (temp_project / "bad_queries.py").write_text(
        """
from app.models import User, Post

def get_user_posts():
    users = User.query.all()  # First query
    result = []
    for user in users:
        posts = user.posts.all()  # N additional queries!
        result.append({
            'user': user.username,
            'posts': [p.title for p in posts]
        })
    return result

def unsafe_query():
    # Raw SQL without proper escaping
    user_id = request.args.get('id')
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.session.execute(query)
    return result.fetchall()
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should find issues
    assert len(results) >= 1
    
    # Should detect potential problems
    total_issues = sum(len(issues) for issues in results.values())
    assert total_issues > 0


def test_no_database_patterns_found(temp_project):
    """Test behavior when no database patterns are found."""
    # Create a file without database usage
    (temp_project / "utils.py").write_text(
        """
def format_date(date):
    return date.strftime('%Y-%m-%d')

def calculate_age(birth_date):
    from datetime import date
    return (date.today() - birth_date).days // 365
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should return a message about no database patterns
    assert len(results) == 1
    issues = list(results.values())[0]
    assert any("No database patterns detected" in issue for issue in issues)


def test_missing_migrations(temp_project):
    """Test detection of missing migrations setup."""
    # Create a project without migrations
    (temp_project / "app.py").write_text(
        """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
"""
    )

    results = analyze_database_patterns(temp_project)
    
    # Should recommend setting up migrations
    migration_recommendations = None
    for file_path, issues in results.items():
        if "MIGRATIONS" in str(file_path):
            migration_recommendations = issues
            break
    
    assert migration_recommendations is not None
    assert any("No migrations directory found" in issue for issue in migration_recommendations)
