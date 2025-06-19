import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class ModelVisitor(ast.NodeVisitor):
    def __init__(self, file_path: Path):
        self.issues = []
        self.base_classes = []
        self.class_names = set()
        self.imported_models: Set[str] = set()
        self.imported_modules: Set[str] = set()
        self.current_file = file_path

    def visit_ImportFrom(self, node):
        if node.module:
            self.imported_modules.add(node.module)
        for alias in node.names:
            self.imported_models.add(alias.name)

    def visit_ClassDef(self, node):
        class_name = node.name
        self.class_names.add(class_name)

        base_names = [
            b.id if isinstance(b, ast.Name) else b.attr if isinstance(b, ast.Attribute) else None
            for b in node.bases
        ]

        self.base_classes.extend(base_names)
        if not any("Model" in base for base in base_names if base):
            return

        has_tablename = False
        has_pk = False
        has_column = False
        has_relationship = False
        has_foreignkey = False
        has_enum = False
        has_default = False

        if not re.match(r'^[A-Z][a-zA-Z0-9]+$', class_name):
            self.issues.append(f"⚠️ {class_name}: Class name should be PascalCase")

        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name) and target.id == "__tablename__":
                        has_tablename = True
                        if isinstance(stmt.value, ast.Str):
                            if not re.match(r'^[a-z_]+$', stmt.value.s):
                                self.issues.append(f"⚠️ {class_name}: __tablename__ should be snake_case")

            if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                call = stmt.value
                if isinstance(call.func, ast.Attribute):
                    if call.func.attr == "Column":
                        has_column = True
                        for kw in call.keywords:
                            if kw.arg == "primary_key" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                has_pk = True
                            if kw.arg == "nullable" and isinstance(kw.value, ast.Constant):
                                self.issues.append(f"ℹ️ {class_name}: nullable={kw.value.value}")
                            if kw.arg == "unique" and isinstance(kw.value, ast.Constant):
                                self.issues.append(f"ℹ️ {class_name}: unique={kw.value.value}")
                            if kw.arg == "index" and isinstance(kw.value, ast.Constant):
                                self.issues.append(f"ℹ️ {class_name}: index={kw.value.value}")
                            if kw.arg == "default":
                                has_default = True

                        for arg in call.args:
                            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute):
                                if arg.func.attr == "Enum":
                                    has_enum = True
                            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute):
                                if arg.func.attr == "ForeignKey":
                                    has_foreignkey = True

                    elif call.func.attr == "relationship":
                        has_relationship = True

        if not has_tablename:
            self.issues.append(f"❌ {class_name}: Missing __tablename__")
        if not has_column:
            self.issues.append(f"❌ {class_name}: No fields defined with db.Column")
        if not has_pk:
            self.issues.append(f"❌ {class_name}: No primary key defined")
        if has_foreignkey:
            self.issues.append(f"✅ {class_name}: ForeignKey used")
        if has_relationship:
            self.issues.append(f"✅ {class_name}: relationship used")
        if has_enum:
            self.issues.append(f"✅ {class_name}: Enum type used")
        if has_default:
            self.issues.append(f"✅ {class_name}: Default value specified")
        if has_tablename and has_column and has_pk:
            self.issues.append(f"✅ {class_name}: Core model checks passed")

        for base in base_names:
            if base and base not in ("Model",):
                self.issues.append(f"ℹ️ {class_name}: Inherits from mixin or base class '{base}'")

def analyze_models(project_path: Path) -> Dict[Path, List[str]]:
    report = {}
    all_classes = set()
    all_imports = set()
    import_graph: Dict[str, Set[str]] = {}

    model_files = list(project_path.rglob("models/*.py"))

    for file_path in model_files:
        if file_path.name == "__init__.py":
            continue

        visitor = ModelVisitor(file_path)
        try:
            tree = ast.parse(file_path.read_text())
            visitor.visit(tree)
            all_classes.update(visitor.class_names)
            all_imports.update(visitor.imported_models)
            report[file_path] = visitor.issues or ["⚠️ No SQLAlchemy model classes found"]
            import_graph[str(file_path)] = visitor.imported_modules
        except SyntaxError as e:
            report[file_path] = [f"❌ Syntax error: {e}"]

    unused_models = all_classes - all_imports
    for file_path in model_files:
        for unused in sorted(unused_models):
            report.setdefault(file_path, []).append(f"⚠️ Unused model: {unused}")

    def detect_cycles(graph: Dict[str, Set[str]]) -> List[Tuple[str, str]]:
        cycles = []
        for source, targets in graph.items():
            for target in targets:
                for rev_source, rev_targets in graph.items():
                    if rev_source != source and source in rev_targets and target in rev_source:
                        cycles.append((source, rev_source))
        return cycles

    cycles = detect_cycles(import_graph)
    for file_path in model_files:
        for a, b in cycles:
            if str(file_path) in (a, b):
                report.setdefault(file_path, []).append(f"⚠️ Circular import detected between: {a} ↔ {b}")

    return report
