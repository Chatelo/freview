"""
API analysis for Flask applications.

This module analyzes Flask routes, blueprints, and API patterns to identify
potential issues and suggest improvements.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class RouteInfo:
    """Information about a Flask route."""
    
    name: str
    path: str
    methods: List[str]
    function_name: str
    blueprint: Optional[str] = None
    has_docstring: bool = False
    has_error_handling: bool = False
    has_input_validation: bool = False
    has_authentication: bool = False
    line_number: int = 0
    decorators: List[str] = field(default_factory=list)


@dataclass
class BlueprintInfo:
    """Information about a Flask blueprint."""
    
    name: str
    url_prefix: Optional[str] = None
    routes: List[RouteInfo] = field(default_factory=list)
    file_path: Optional[Path] = None


class APIVisitor(ast.NodeVisitor):
    """AST visitor for analyzing Flask API patterns."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.routes: List[RouteInfo] = []
        self.blueprints: List[BlueprintInfo] = []
        self.imports: Set[str] = set()
        self.current_class = None
        self.current_blueprint = None
    
    def visit_Import(self, node):
        """Track imports to understand Flask usage."""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Track from imports."""
        if node.module:
            for alias in node.names:
                self.imports.add(f"{node.module}.{alias.name}")
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Look for blueprint assignments."""
        if isinstance(node.value, ast.Call):
            if self._is_blueprint_call(node.value):
                self._extract_blueprint_info(node)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Analyze function definitions for routes."""
        route_info = self._extract_route_info(node)
        if route_info:
            self.routes.append(route_info)
        self.generic_visit(node)
    
    def _is_blueprint_call(self, call: ast.Call) -> bool:
        """Check if a call creates a Flask Blueprint."""
        if isinstance(call.func, ast.Name):
            return call.func.id == "Blueprint"
        elif isinstance(call.func, ast.Attribute):
            return call.func.attr == "Blueprint"
        return False
    
    def _extract_blueprint_info(self, node: ast.Assign):
        """Extract blueprint information from assignment."""
        if not isinstance(node.value, ast.Call):
            return
        
        call = node.value
        blueprint_name = None
        url_prefix = None
        
        # Get blueprint name from first argument
        if call.args and isinstance(call.args[0], ast.Constant):
            blueprint_name = call.args[0].value
        
        # Look for url_prefix in keywords
        for keyword in call.keywords:
            if keyword.arg == "url_prefix" and isinstance(keyword.value, ast.Constant):
                url_prefix = keyword.value.value
        
        if blueprint_name:
            blueprint = BlueprintInfo(
                name=blueprint_name,
                url_prefix=url_prefix,
                file_path=self.file_path
            )
            self.blueprints.append(blueprint)
            self.current_blueprint = blueprint_name
    
    def _extract_route_info(self, node: ast.FunctionDef) -> Optional[RouteInfo]:
        """Extract route information from a function definition."""
        route_decorators = self._find_route_decorators(node.decorator_list)
        if not route_decorators:
            return None
        
        # Get the primary route decorator
        route_decorator = route_decorators[0]
        path, methods = self._parse_route_decorator(route_decorator)
        
        route_info = RouteInfo(
            name=node.name,
            path=path,
            methods=methods,
            function_name=node.name,
            blueprint=self.current_blueprint,
            has_docstring=ast.get_docstring(node) is not None,
            line_number=node.lineno,
            decorators=[self._decorator_to_string(d) for d in node.decorator_list]
        )
        
        # Analyze function body for patterns
        self._analyze_route_body(node, route_info)
        
        return route_info
    
    def _find_route_decorators(self, decorators: List[ast.expr]) -> List[ast.expr]:
        """Find route-related decorators."""
        route_decorators = []
        
        for decorator in decorators:
            if self._is_route_decorator(decorator):
                route_decorators.append(decorator)
        
        return route_decorators
    
    def _is_route_decorator(self, decorator: ast.expr) -> bool:
        """Check if a decorator is a route decorator."""
        if isinstance(decorator, ast.Name):
            return decorator.id in ["route"]
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr in ["route", "get", "post", "put", "delete", "patch"]
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id in ["route"]
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr in ["route", "get", "post", "put", "delete", "patch"]
        return False
    
    def _parse_route_decorator(self, decorator: ast.expr) -> Tuple[str, List[str]]:
        """Parse route decorator to extract path and methods."""
        path = "/"
        methods = ["GET"]
        
        if isinstance(decorator, ast.Call):
            # Get path from first argument
            if decorator.args and isinstance(decorator.args[0], ast.Constant):
                path = decorator.args[0].value
            
            # Get methods from keywords
            for keyword in decorator.keywords:
                if keyword.arg == "methods":
                    if isinstance(keyword.value, ast.List):
                        methods = []
                        for elt in keyword.value.elts:
                            if isinstance(elt, ast.Constant):
                                methods.append(elt.value)
        
        return path, methods
    
    def _analyze_route_body(self, node: ast.FunctionDef, route_info: RouteInfo):
        """Analyze the route function body for patterns."""
        # Look for error handling patterns
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Try):
                route_info.has_error_handling = True
            elif isinstance(stmt, ast.Call):
                # Look for validation patterns
                if self._is_validation_call(stmt):
                    route_info.has_input_validation = True
                # Look for authentication patterns
                if self._is_auth_call(stmt):
                    route_info.has_authentication = True
    
    def _is_validation_call(self, call: ast.Call) -> bool:
        """Check if a call represents input validation."""
        validation_patterns = [
            "validate", "check", "verify", "parse_args", "get_json"
        ]
        
        if isinstance(call.func, ast.Attribute):
            return any(pattern in call.func.attr.lower() for pattern in validation_patterns)
        elif isinstance(call.func, ast.Name):
            return any(pattern in call.func.id.lower() for pattern in validation_patterns)
        
        return False
    
    def _is_auth_call(self, call: ast.Call) -> bool:
        """Check if a call represents authentication."""
        auth_patterns = [
            "login_required", "auth", "authenticate", "check_token", "verify_token"
        ]
        
        if isinstance(call.func, ast.Attribute):
            return any(pattern in call.func.attr.lower() for pattern in auth_patterns)
        elif isinstance(call.func, ast.Name):
            return any(pattern in call.func.id.lower() for pattern in auth_patterns)
        
        return False
    
    def _decorator_to_string(self, decorator: ast.expr) -> str:
        """Convert decorator AST to string representation."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{self._expr_to_string(decorator.value)}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            func_name = self._expr_to_string(decorator.func)
            return f"{func_name}(...)"
        else:
            return "unknown"
    
    def _expr_to_string(self, expr: ast.expr) -> str:
        """Convert expression AST to string."""
        if isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Attribute):
            return f"{self._expr_to_string(expr.value)}.{expr.attr}"
        else:
            return "unknown"


def analyze_api_patterns(project_path: Path) -> Dict[Path, List[str]]:
    """
    Analyze Flask API patterns in a project.
    
    Args:
        project_path: Path to the Flask project root
    
    Returns:
        Dictionary mapping file paths to lists of issues/recommendations
    """
    report = {}
    all_routes: List[RouteInfo] = []
    all_blueprints: List[BlueprintInfo] = []
    
    # Find Python files that might contain routes
    route_files = _find_route_files(project_path)
    
    if not route_files:
        report[project_path / "API_ANALYSIS"] = [
            "⚠️  No Flask route files found",
            "💡 Recommendation: Create route files with @app.route or Blueprint definitions"
        ]
        return report
    
    # Analyze each route file
    for file_path in route_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            tree = ast.parse(content)
            visitor = APIVisitor(file_path)
            visitor.visit(tree)
            
            # Generate issues for this file
            issues = _analyze_file_routes(visitor, file_path, project_path)
            if issues:
                report[file_path] = issues
            
            all_routes.extend(visitor.routes)
            all_blueprints.extend(visitor.blueprints)
            
        except Exception as e:
            report[file_path] = [f"❌ Error analyzing file: {str(e)}"]
    
    # Cross-file analysis
    _analyze_api_architecture(all_routes, all_blueprints, report, project_path)
    
    return report


def _find_route_files(project_path: Path) -> List[Path]:
    """Find Python files that might contain Flask routes."""
    route_files: List[Path] = []
    
    # Common patterns for route files
    patterns = [
        "**/*views.py",
        "**/routes*.py", 
        "**/api*.py",
        "**/blueprint*.py",
        "**/endpoints*.py",
        "app.py",
        "main.py",
        "application.py"
    ]
    
    for pattern in patterns:
        route_files.extend(project_path.glob(pattern))
    
    # Also look in common directories
    common_dirs = ["views", "routes", "api", "blueprints", "endpoints"]
    for dir_name in common_dirs:
        route_dir = project_path / dir_name
        if route_dir.exists() and route_dir.is_dir():
            route_files.extend(route_dir.glob("*.py"))
    
    # Remove duplicates and __init__.py files
    route_files = [f for f in set(route_files) if f.name != "__init__.py"]
    
    return route_files


def _analyze_file_routes(visitor: APIVisitor, file_path: Path, project_path: Path) -> List[str]:
    """Analyze routes in a single file."""
    issues = []
    
    # Check if this file has Flask imports
    flask_imports = [imp for imp in visitor.imports if "flask" in imp.lower()]
    if not flask_imports and visitor.routes:
        issues.append("⚠️  Routes found but no Flask imports detected")
    
    # Analyze each route
    for route in visitor.routes:
        # Check for REST conventions
        if not _follows_rest_conventions(route):
            issues.append(f"💡 Route '{route.path}' could follow REST conventions better")
        
        # Check for documentation
        if not route.has_docstring:
            issues.append(f"📝 Route '{route.function_name}' missing docstring")
        
        # Check for error handling
        if not route.has_error_handling and route.methods != ["GET"]:
            issues.append(f"🛡️  Route '{route.function_name}' should include error handling")
        
        # Check for input validation on data-modifying routes
        data_methods = ["POST", "PUT", "PATCH"]
        if any(method in route.methods for method in data_methods) and not route.has_input_validation:
            issues.append(f"🔍 Route '{route.function_name}' should validate input data")
        
        # Check for authentication on sensitive routes
        if _is_sensitive_route(route) and not route.has_authentication:
            issues.append(f"🔐 Route '{route.function_name}' may need authentication")
    
    # Check blueprints
    for blueprint in visitor.blueprints:
        if not blueprint.url_prefix:
            issues.append(f"🏗️  Blueprint '{blueprint.name}' should have a url_prefix")
    
    # Success messages
    if visitor.routes:
        issues.append(f"✅ Found {len(visitor.routes)} route(s) in {file_path.name}")
    
    if visitor.blueprints:
        issues.append(f"✅ Found {len(visitor.blueprints)} blueprint(s) in {file_path.name}")
    
    return issues


def _follows_rest_conventions(route: RouteInfo) -> bool:
    """Check if a route follows REST conventions."""
    path = route.path.lower()
    methods = route.methods
    
    # Basic REST patterns
    rest_patterns = [
        (r"/api/\w+/?$", ["GET", "POST"]),  # Collection
        (r"/api/\w+/\d+/?$", ["GET", "PUT", "DELETE"]),  # Resource
        (r"/api/\w+/<\w+>/?$", ["GET", "PUT", "DELETE"]),  # Resource with variable
    ]
    
    for pattern, expected_methods in rest_patterns:
        if re.match(pattern, path):
            return any(method in expected_methods for method in methods)
    
    return True  # Default to true for non-API routes


def _is_sensitive_route(route: RouteInfo) -> bool:
    """Check if a route handles sensitive operations."""
    sensitive_patterns = [
        "delete", "remove", "admin", "user", "auth", "login", "password",
        "create", "update", "edit", "modify"
    ]
    
    path_lower = route.path.lower()
    function_lower = route.function_name.lower()
    
    return any(pattern in path_lower or pattern in function_lower 
              for pattern in sensitive_patterns)


def _analyze_api_architecture(routes: List[RouteInfo], blueprints: List[BlueprintInfo], 
                            report: Dict[Path, List[str]], project_path: Path):
    """Analyze overall API architecture patterns."""
    if not routes:
        return
    
    architecture_issues = []
    
    # Check for API versioning
    versioned_routes = [r for r in routes if re.search(r'/v\d+/', r.path)]
    if not versioned_routes and len(routes) > 5:
        architecture_issues.append("📈 Consider API versioning (e.g., /api/v1/)")
    
    # Check for consistent error handling patterns
    error_handled_routes = [r for r in routes if r.has_error_handling]
    if len(error_handled_routes) < len(routes) * 0.5:
        architecture_issues.append("🛡️  Less than 50% of routes have error handling")
    
    # Check for blueprint organization
    blueprint_routes = [r for r in routes if r.blueprint]
    if len(blueprint_routes) < len(routes) * 0.7 and len(routes) > 10:
        architecture_issues.append("🏗️  Consider organizing routes into blueprints")
    
    # Check for authentication patterns
    auth_routes = [r for r in routes if r.has_authentication]
    sensitive_routes = [r for r in routes if _is_sensitive_route(r)]
    if len(sensitive_routes) > 0 and len(auth_routes) < len(sensitive_routes) * 0.8:
        architecture_issues.append("🔐 Many sensitive routes lack authentication")
    
    # Check HTTP method distribution
    method_usage = {}
    for route in routes:
        for method in route.methods:
            method_usage[method] = method_usage.get(method, 0) + 1
    
    if method_usage.get("GET", 0) > len(routes) * 0.8:
        architecture_issues.append("💡 Consider using more HTTP methods (POST, PUT, DELETE)")
    
    # Success messages
    if blueprints:
        architecture_issues.append(f"✅ Good: Project uses {len(blueprints)} blueprint(s)")
    
    if versioned_routes:
        architecture_issues.append("✅ Good: API versioning detected")
    
    if len(auth_routes) > 0:
        architecture_issues.append(f"✅ Good: {len(auth_routes)} route(s) have authentication")
    
    if architecture_issues:
        report[project_path / "API_ARCHITECTURE"] = architecture_issues
