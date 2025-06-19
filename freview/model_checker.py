import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Information about a SQLAlchemy model class."""

    name: str
    file_path: Path
    has_tablename: bool = False
    has_primary_key: bool = False
    has_columns: bool = False
    relationships: Optional[List[str]] = None
    foreign_keys: Optional[List[str]] = None
    tablename: Optional[str] = None
    base_classes: Optional[List[str]] = None

    def __post_init__(self):
        if self.relationships is None:
            self.relationships = []
        if self.foreign_keys is None:
            self.foreign_keys = []
        if self.base_classes is None:
            self.base_classes = []


class ModelVisitor(ast.NodeVisitor):
    """Enhanced AST visitor for SQLAlchemy model analysis."""

    def __init__(self, file_path: Path):
        self.issues = []
        self.models: List[ModelInfo] = []
        self.imports: Set[str] = set()
        self.current_file = file_path
        self.class_methods: Dict[str, List[str]] = {}

    def visit_Import(self, node):
        """Track regular imports."""
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        """Track from imports."""
        if node.module:
            self.imports.add(node.module)

            for alias in node.names:
                self.imports.add(alias.name)
                # Track specific SQLAlchemy imports
                if node.module in ["sqlalchemy", "flask_sqlalchemy"]:
                    self.imports.add(f"{node.module}.{alias.name}")

    def visit_ClassDef(self, node):
        """Analyze class definitions for SQLAlchemy models."""
        class_name = node.name

        # Extract base class names
        base_names = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_names.append(base.attr)

        # Check if this looks like a SQLAlchemy model
        is_model = any(
            "Model" in base or "Base" in base or "DeclarativeBase" in base for base in base_names
        )

        if not is_model:
            # Continue visiting for nested classes
            self.generic_visit(node)
            return

        # Create model info
        model_info = ModelInfo(
            name=class_name, file_path=self.current_file, base_classes=base_names
        )

        # Analyze class body
        self._analyze_model_class(node, model_info)
        self.models.append(model_info)

        # Generate issues for this model
        self._generate_model_issues(model_info)

        # Continue visiting
        self.generic_visit(node)

    def _analyze_model_class(self, node: ast.ClassDef, model_info: ModelInfo):
        """Analyze the contents of a model class."""
        methods = []

        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                methods.append(stmt.name)

            elif isinstance(stmt, ast.Assign):
                self._analyze_assignment(stmt, model_info)

        self.class_methods[model_info.name] = methods

    def _analyze_assignment(self, stmt: ast.Assign, model_info: ModelInfo):
        """Analyze assignment statements in model classes."""
        for target in stmt.targets:
            if isinstance(target, ast.Name):
                var_name = target.id

                # Check for __tablename__
                if var_name == "__tablename__":
                    model_info.has_tablename = True
                    if isinstance(stmt.value, ast.Constant):
                        if isinstance(stmt.value.value, str):
                            model_info.tablename = stmt.value.value
                    # Fallback for older Python versions
                    elif hasattr(stmt.value, "s"):  # ast.Str (deprecated)
                        if isinstance(stmt.value.s, str):
                            model_info.tablename = stmt.value.s

                # Check for Column definitions
                elif isinstance(stmt.value, ast.Call):
                    self._analyze_column_call(stmt.value, model_info, var_name)

    def _analyze_column_call(self, call: ast.Call, model_info: ModelInfo, var_name: str):
        """Analyze Column() and relationship() calls."""
        if isinstance(call.func, ast.Attribute):
            func_name = call.func.attr

            if func_name == "Column":
                model_info.has_columns = True

                # Check for primary key
                for keyword in call.keywords:
                    if (
                        keyword.arg == "primary_key"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ):
                        model_info.has_primary_key = True

                # Check for foreign keys in column args
                for arg in call.args:
                    if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute):
                        if arg.func.attr == "ForeignKey":
                            if arg.args and isinstance(arg.args[0], (ast.Str, ast.Constant)):
                                fk_ref = (
                                    arg.args[0].s
                                    if isinstance(arg.args[0], ast.Str)
                                    else arg.args[0].value
                                )
                                model_info.foreign_keys.append(fk_ref)

            elif func_name == "relationship":
                # Extract relationship target
                if call.args and isinstance(call.args[0], (ast.Str, ast.Constant)):
                    rel_target = (
                        call.args[0].s if isinstance(call.args[0], ast.Str) else call.args[0].value
                    )
                    model_info.relationships.append(rel_target)

    def _generate_model_issues(self, model_info: ModelInfo):
        """Generate issues for a model based on analysis."""
        class_name = model_info.name

        # Naming convention checks
        if not re.match(r"^[A-Z][a-zA-Z0-9]+$", class_name):
            self.issues.append(f"⚠️ {class_name}: Class name should be PascalCase")

        # Core requirements
        if not model_info.has_tablename:
            self.issues.append(f"❌ {class_name}: Missing __tablename__ attribute")
        elif model_info.tablename and not re.match(r"^[a-z][a-z0-9_]*$", model_info.tablename):
            self.issues.append(f"⚠️ {class_name}: __tablename__ should be snake_case")

        if not model_info.has_columns:
            self.issues.append(f"❌ {class_name}: No columns defined with db.Column()")

        if not model_info.has_primary_key:
            self.issues.append(f"❌ {class_name}: No primary key defined")

        # Positive feedback
        if model_info.has_tablename and model_info.has_columns and model_info.has_primary_key:
            self.issues.append(f"✅ {class_name}: Core model requirements satisfied")

        if model_info.foreign_keys:
            self.issues.append(
                f"✅ {class_name}: Uses foreign key constraints ({len(model_info.foreign_keys)} found)"
            )

        if model_info.relationships:
            self.issues.append(
                f"✅ {class_name}: Defines relationships ({len(model_info.relationships)} found)"
            )

        # Method checks
        methods = self.class_methods.get(class_name, [])
        if "__repr__" not in methods:
            self.issues.append(
                f"ℹ️ {class_name}: Consider adding __repr__ method for better debugging"
            )

        if "__str__" not in methods:
            self.issues.append(
                f"ℹ️ {class_name}: Consider adding __str__ method for string representation"
            )

        # Base class information
        interesting_bases = [b for b in model_info.base_classes if b not in ("Model", "Base")]
        if interesting_bases:
            self.issues.append(f"ℹ️ {class_name}: Inherits from {', '.join(interesting_bases)}")


def analyze_models(project_path: Path) -> Dict[Path, List[str]]:
    """
    Analyze SQLAlchemy models in a Flask project.

    Args:
        project_path: Path to the Flask project root

    Returns:
        Dictionary mapping file paths to lists of issues found
    """
    report = {}
    all_models: List[ModelInfo] = []

    # Find model files
    model_files = _find_model_files(project_path)

    if not model_files:
        # No model files found
        return {project_path: ["⚠️ No Python model files found in the project"]}

    # Analyze each model file
    for file_path in model_files:
        try:
            visitor = ModelVisitor(file_path)
            tree = ast.parse(file_path.read_text(encoding="utf-8"))
            visitor.visit(tree)

            all_models.extend(visitor.models)

            if visitor.issues:
                report[file_path] = visitor.issues
            else:
                report[file_path] = ["ℹ️ No SQLAlchemy models found in this file"]

        except SyntaxError as e:
            report[file_path] = [f"❌ Syntax error: {e.msg} at line {e.lineno}"]
        except UnicodeDecodeError:
            report[file_path] = ["❌ Unable to read file - encoding issues"]
        except Exception as e:
            report[file_path] = [f"❌ Error analyzing file: {str(e)}"]

    # Cross-model analysis
    _analyze_model_relationships(all_models, report, project_path)

    return report


def _find_model_files(project_path: Path) -> List[Path]:
    """Find Python files that might contain SQLAlchemy models."""
    model_files: List[Path] = []

    # Look in common model directories
    model_dirs = [
        project_path / "models",
        project_path / "app" / "models",
        project_path / "src" / "models",
        project_path / "application" / "models",
    ]

    for model_dir in model_dirs:
        if model_dir.exists() and model_dir.is_dir():
            model_files.extend(model_dir.glob("*.py"))

    # Look for single model files
    single_files = [
        project_path / "models.py",
        project_path / "app" / "models.py",
        project_path / "src" / "models.py",
    ]

    for file_path in single_files:
        if file_path.exists():
            model_files.append(file_path)

    # Remove __init__.py files and duplicates
    model_files = [f for f in model_files if f.name != "__init__.py"]
    return list(set(model_files))


def _analyze_model_relationships(
    models: List[ModelInfo], report: Dict[Path, List[str]], project_path: Path
):
    """Analyze relationships between models."""
    if not models:
        return

    model_names = {model.name for model in models}

    # Check for unused models (models not referenced in relationships)
    referenced_models = set()
    for model in models:
        referenced_models.update(model.relationships)

    unused_models = model_names - referenced_models

    # Add unused model warnings to the first file (arbitrary choice)
    if unused_models and models:
        first_file = models[0].file_path
        for unused in sorted(unused_models):
            report.setdefault(first_file, []).append(
                f"⚠️ Model '{unused}' is not referenced in any relationships"
            )

    # Check for potential relationship issues
    for model in models:
        for rel_target in model.relationships:
            if rel_target not in model_names:
                report.setdefault(model.file_path, []).append(
                    f"⚠️ {model.name}: Relationship target '{rel_target}' not found in analyzed models"
                )

    # Simple circular dependency detection
    model_deps = {}
    for model in models:
        model_deps[model.name] = set(model.relationships)

    # Find cycles (basic implementation)
    for model_name, deps in model_deps.items():
        for dep in deps:
            if dep in model_deps and model_name in model_deps[dep]:
                # Found a circular dependency
                model_file = next((m.file_path for m in models if m.name == model_name), None)
                if model_file:
                    report.setdefault(model_file, []).append(
                        f"⚠️ Potential circular relationship between '{model_name}' and '{dep}'"
                    )
