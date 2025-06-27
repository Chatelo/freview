"""
Database analysis for Flask applications.

This module analyzes database patterns, migrations, and configurations
to identify optimization opportunities and potential issues.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field


@dataclass
class MigrationInfo:
    """Information about a database migration."""
    
    version: str
    file_path: Path
    has_upgrade: bool = False
    has_downgrade: bool = False
    operations: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class IndexInfo:
    """Information about database indexes."""
    
    name: str
    table: str
    columns: List[str]
    unique: bool = False
    file_path: Optional[Path] = None


@dataclass
class DatabaseConfig:
    """Information about database configuration."""
    
    database_uri: Optional[str] = None
    pool_size: Optional[int] = None
    max_overflow: Optional[int] = None
    pool_timeout: Optional[int] = None
    engine_options: Dict[str, str] = field(default_factory=dict)


class DatabaseVisitor(ast.NodeVisitor):
    """AST visitor for analyzing database patterns."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.database_calls: List[str] = []
        self.query_patterns: List[str] = []
        self.indexes: List[IndexInfo] = []
        self.config_items: Dict[str, str] = {}
        self.imports: Set[str] = set()
        self.transactions: List[str] = []
    
    def visit_Import(self, node):
        """Track imports for database libraries."""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Track from imports."""
        if node.module:
            for alias in node.names:
                self.imports.add(f"{node.module}.{alias.name}")
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Analyze function calls for database patterns."""
        call_name = self._get_call_name(node)
        
        # Track database queries
        if self._is_query_call(call_name):
            self.query_patterns.append(call_name)
        
        # Track transaction patterns
        if self._is_transaction_call(call_name):
            self.transactions.append(call_name)
        
        # Track index creation
        if self._is_index_call(call_name):
            index_info = self._extract_index_info(node)
            if index_info:
                self.indexes.append(index_info)
        
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Look for configuration assignments."""
        if isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id.upper()
                    if any(db_term in var_name for db_term in 
                          ["DATABASE", "DB", "SQL", "URI", "POOL"]):
                        self.config_items[var_name] = str(node.value.value)
        
        self.generic_visit(node)
    
    def _get_call_name(self, call: ast.Call) -> str:
        """Get the name of a function call."""
        if isinstance(call.func, ast.Name):
            return call.func.id
        elif isinstance(call.func, ast.Attribute):
            return f"{self._expr_to_string(call.func.value)}.{call.func.attr}"
        else:
            return "unknown"
    
    def _is_query_call(self, call_name: str) -> bool:
        """Check if a call represents a database query."""
        query_patterns = [
            "query", "select", "filter", "join", "execute", "fetchall", 
            "fetchone", "first", "all", "get", "get_or_404"
        ]
        return any(pattern in call_name.lower() for pattern in query_patterns)
    
    def _is_transaction_call(self, call_name: str) -> bool:
        """Check if a call represents a transaction operation."""
        transaction_patterns = [
            "commit", "rollback", "begin", "transaction", "session"
        ]
        return any(pattern in call_name.lower() for pattern in transaction_patterns)
    
    def _is_index_call(self, call_name: str) -> bool:
        """Check if a call creates an index."""
        return "index" in call_name.lower() and "create" in call_name.lower()
    
    def _extract_index_info(self, call: ast.Call) -> Optional[IndexInfo]:
        """Extract index information from a call."""
        # This is a simplified implementation
        # In practice, you'd need to handle various SQLAlchemy index patterns
        return None
    
    def _expr_to_string(self, expr: ast.expr) -> str:
        """Convert expression AST to string."""
        if isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Attribute):
            return f"{self._expr_to_string(expr.value)}.{expr.attr}"
        else:
            return "unknown"


def analyze_database_patterns(project_path: Path) -> Dict[Path, List[str]]:
    """
    Analyze database patterns in a Flask project.
    
    Args:
        project_path: Path to the Flask project root
    
    Returns:
        Dictionary mapping file paths to lists of issues/recommendations
    """
    report = {}
    
    # Analyze migrations
    migrations_report = _analyze_migrations(project_path)
    if migrations_report:
        report.update(migrations_report)
    
    # Analyze database configuration
    config_report = _analyze_database_config(project_path)
    if config_report:
        report.update(config_report)
    
    # Analyze database usage patterns
    usage_report = _analyze_database_usage(project_path)
    if usage_report:
        report.update(usage_report)
    
    # Analyze query patterns
    query_report = _analyze_query_patterns(project_path)
    if query_report:
        report.update(query_report)
    
    if not report:
        report[project_path / "DATABASE_ANALYSIS"] = [
            "ℹ️  No database patterns detected",
            "💡 If using SQLAlchemy, ensure proper configuration and migration setup"
        ]
    
    return report


def _analyze_migrations(project_path: Path) -> Dict[Path, List[str]]:
    """Analyze Alembic migrations."""
    report = {}
    
    # Look for migrations directory
    migration_dirs = [
        project_path / "migrations",
        project_path / "alembic",
        project_path / "db" / "migrations"
    ]
    
    migrations_dir = None
    for dir_path in migration_dirs:
        if dir_path.exists() and dir_path.is_dir():
            migrations_dir = dir_path
            break
    
    if not migrations_dir:
        report[project_path / "MIGRATIONS"] = [
            "⚠️  No migrations directory found",
            "💡 Consider setting up Alembic for database migrations",
            "💡 Run: flask db init (with Flask-Migrate)"
        ]
        return report
    
    issues = []
    
    # Check for versions directory
    versions_dir = migrations_dir / "versions"
    if not versions_dir.exists():
        issues.append("⚠️  No migrations/versions directory found")
    else:
        # Analyze migration files
        migration_files = list(versions_dir.glob("*.py"))
        migration_files = [f for f in migration_files if f.name != "__init__.py"]
        
        if not migration_files:
            issues.append("⚠️  No migration files found")
        else:
            issues.append(f"✅ Found {len(migration_files)} migration file(s)")
            
            # Analyze individual migrations
            for migration_file in migration_files:
                migration_issues = _analyze_migration_file(migration_file)
                issues.extend(migration_issues)
    
    # Check for alembic.ini
    alembic_ini = migrations_dir.parent / "alembic.ini"
    if not alembic_ini.exists():
        issues.append("⚠️  No alembic.ini configuration file found")
    else:
        issues.append("✅ Alembic configuration file present")
    
    # Check for env.py
    env_py = migrations_dir / "env.py"
    if not env_py.exists():
        issues.append("⚠️  No env.py file found in migrations directory")
    else:
        issues.append("✅ Migration environment file present")
    
    if issues:
        report[migrations_dir] = issues
    
    return report


def _analyze_migration_file(migration_file: Path) -> List[str]:
    """Analyze a single migration file."""
    issues = []
    
    try:
        with open(migration_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for upgrade function
        if "def upgrade():" not in content:
            issues.append(f"⚠️  Migration {migration_file.name} missing upgrade() function")
        
        # Check for downgrade function
        if "def downgrade():" not in content:
            issues.append(f"⚠️  Migration {migration_file.name} missing downgrade() function")
        
        # Check for potentially dangerous operations
        dangerous_patterns = [
            "drop_table", "drop_column", "alter_column.*nullable=False"
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"⚠️  Migration {migration_file.name} contains potentially dangerous operation: {pattern}")
        
        # Check for index creation
        if "create_index" in content:
            issues.append(f"✅ Migration {migration_file.name} includes index creation")
        
        # Check for foreign key constraints
        if "foreign_key" in content.lower() or "foreignkey" in content:
            issues.append(f"✅ Migration {migration_file.name} includes foreign key constraints")
        
    except Exception as e:
        issues.append(f"❌ Error analyzing migration {migration_file.name}: {str(e)}")
    
    return issues


def _analyze_database_config(project_path: Path) -> Dict[Path, List[str]]:
    """Analyze database configuration."""
    report = {}
    
    # Look for configuration files
    config_files = [
        project_path / "config.py",
        project_path / "app" / "config.py",
        project_path / "settings.py",
        project_path / ".env",
        project_path / "app.py"
    ]
    
    found_config = False
    
    for config_file in config_files:
        if config_file.exists():
            issues = _analyze_config_file(config_file)
            if issues:
                report[config_file] = issues
                found_config = True
    
    if not found_config:
        report[project_path / "DATABASE_CONFIG"] = [
            "⚠️  No database configuration found",
            "💡 Create a config.py file with DATABASE_URI",
            "💡 Consider using environment variables for sensitive data"
        ]
    
    return report


def _analyze_config_file(config_file: Path) -> List[str]:
    """Analyze a configuration file for database settings."""
    issues = []
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for database URI
        if not any(term in content.upper() for term in ["DATABASE_URI", "SQLALCHEMY_DATABASE_URI"]):
            issues.append("⚠️  No database URI configuration found")
        else:
            issues.append("✅ Database URI configuration present")
            
            # Check for hardcoded credentials
            if any(term in content for term in ["password=", "passwd=", "://user:"]):
                issues.append("🔐 Warning: Potential hardcoded database credentials")
                issues.append("💡 Use environment variables: os.environ.get('DATABASE_URL')")
        
        # Check for connection pool settings
        pool_settings = ["SQLALCHEMY_POOL_SIZE", "SQLALCHEMY_POOL_TIMEOUT", "SQLALCHEMY_MAX_OVERFLOW"]
        found_pool_settings = [setting for setting in pool_settings if setting in content]
        
        if found_pool_settings:
            issues.append(f"✅ Connection pool settings configured: {', '.join(found_pool_settings)}")
        else:
            issues.append("💡 Consider configuring connection pool settings for production")
        
        # Check for SQLAlchemy settings
        sqlalchemy_settings = [
            "SQLALCHEMY_TRACK_MODIFICATIONS",
            "SQLALCHEMY_ECHO",
            "SQLALCHEMY_RECORD_QUERIES"
        ]
        
        found_settings = [setting for setting in sqlalchemy_settings if setting in content]
        if found_settings:
            issues.append(f"✅ SQLAlchemy settings configured: {', '.join(found_settings)}")
        
        # Check for environment-based configuration
        if "os.environ" in content or "getenv" in content:
            issues.append("✅ Environment-based configuration detected")
        else:
            issues.append("💡 Consider using environment variables for configuration")
        
    except Exception as e:
        issues.append(f"❌ Error analyzing config file: {str(e)}")
    
    return issues


def _analyze_database_usage(project_path: Path) -> Dict[Path, List[str]]:
    """Analyze database usage patterns in the codebase."""
    report = {}
    
    # Find Python files that might use the database
    python_files = list(project_path.glob("**/*.py"))
    python_files = [f for f in python_files if "__pycache__" not in str(f)]
    
    db_usage_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check if file uses database
            db_patterns = [
                "from flask_sqlalchemy",
                "import sqlalchemy",
                "db.session",
                "query(",
                ".filter(",
                ".commit()",
                ".rollback()"
            ]
            
            if any(pattern in content for pattern in db_patterns):
                db_usage_files.append(file_path)
        
        except Exception:
            continue
    
    # Analyze database usage in each file
    for file_path in db_usage_files:
        issues = _analyze_db_usage_file(file_path)
        if issues:
            report[file_path] = issues
    
    if db_usage_files:
        # Overall database usage analysis
        overall_issues = []
        overall_issues.append(f"✅ Database usage detected in {len(db_usage_files)} file(s)")
        
        # Check for common patterns across files
        all_content = ""
        for file_path in db_usage_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    all_content += f.read()
            except Exception:
                continue
        
        # Check for session management
        if "db.session.close()" not in all_content:
            overall_issues.append("💡 Consider explicit session management with db.session.close()")
        
        # Check for bulk operations
        if "bulk_insert" in all_content or "bulk_update" in all_content:
            overall_issues.append("✅ Bulk operations detected - good for performance")
        
        # Check for lazy loading
        if "lazy=" in all_content:
            overall_issues.append("✅ Lazy loading configuration detected")
        
        report[project_path / "DATABASE_USAGE"] = overall_issues
    
    return report


def _analyze_db_usage_file(file_path: Path) -> List[str]:
    """Analyze database usage in a single file."""
    issues = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        tree = ast.parse(content)
        visitor = DatabaseVisitor(file_path)
        visitor.visit(tree)
        
        # Check query patterns
        if visitor.query_patterns:
            issues.append(f"✅ Found {len(visitor.query_patterns)} database query pattern(s)")
            
            # Check for N+1 query problems
            if content.count(".query") > 5 and "join" not in content.lower():
                issues.append("⚠️  Potential N+1 query problem - consider using joins")
        
        # Check transaction handling
        if visitor.transactions:
            issues.append(f"✅ Transaction handling detected ({len(visitor.transactions)} patterns)")
        elif any(pattern in content for pattern in ["db.session.add", "db.session.delete"]):
            issues.append("⚠️  Database modifications without explicit transaction handling")
        
        # Check for raw SQL
        if "execute(" in content and any(quote in content for quote in ['"SELECT', "'SELECT", '"INSERT', "'INSERT"]):
            issues.append("⚠️  Raw SQL detected - consider using SQLAlchemy ORM")
            issues.append("🔐 Ensure raw SQL is protected against injection attacks")
        
        # Check for proper error handling
        if "try:" in content and any(db_op in content for db_op in ["db.session.commit", "query"]):
            issues.append("✅ Error handling around database operations detected")
        elif any(db_op in content for db_op in ["db.session.commit", "db.session.add"]):
            issues.append("💡 Consider adding error handling around database operations")
        
    except Exception as e:
        issues.append(f"❌ Error analyzing database usage: {str(e)}")
    
    return issues


def _analyze_query_patterns(project_path: Path) -> Dict[Path, List[str]]:
    """Analyze query patterns for optimization opportunities."""
    report = {}
    
    # This would analyze query patterns across the application
    # For now, we'll provide general recommendations
    
    query_issues = []
    
    # Look for model files to understand relationships
    model_files = list(project_path.glob("**/models/*.py"))
    model_files.extend(project_path.glob("**/models.py"))
    
    if model_files:
        relationship_count = 0
        for model_file in model_files:
            try:
                with open(model_file, "r", encoding="utf-8") as f:
                    content = f.read()
                relationship_count += content.count("relationship(")
            except Exception:
                continue
        
        if relationship_count > 0:
            query_issues.append(f"✅ Found {relationship_count} model relationship(s)")
            query_issues.append("💡 Consider eager loading for frequently accessed relationships")
            query_issues.append("💡 Use lazy='select' or lazy='joined' appropriately")
        
        # General query optimization recommendations
        query_issues.extend([
            "💡 Query Optimization Tips:",
            "   • Use database indexes on frequently queried columns",
            "   • Consider query.options(selectinload()) for relationships",
            "   • Use pagination for large result sets",
            "   • Monitor slow query logs in production",
            "   • Consider database connection pooling"
        ])
    
    if query_issues:
        report[project_path / "QUERY_OPTIMIZATION"] = query_issues
    
    return report
