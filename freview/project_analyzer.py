from pathlib import Path

def analyze_project_structure(project_path: Path):
    issues = []

    # Basic structure expectations
    expected_files = ["run.py", "main.py", "app.py", "config.py"]
    expected_dirs = ["models", "templates", "static"]

    # At least one expected file should exist
    if not any((project_path / f).exists() for f in expected_files):
        issues.append("Missing entry file: expected one of run.py, main.py, or app.py")

    # Check for models directory
    model_dir = project_path / "models"
    if not model_dir.exists():
        issues.append("Missing 'models/' directory")
    elif not (model_dir / "__init__.py").exists():
        issues.append("Missing '__init__.py' in 'models/' directory")

    # Check for optional but recommended directories
    for d in expected_dirs[1:]:  # templates, static
        if not (project_path / d).exists():
            issues.append(f"Missing optional '{d}/' directory")

    # Check for .env or config presence
    if not (project_path / ".env").exists() and not (project_path / "config.py").exists():
        issues.append("Missing configuration file (.env or config.py)")

    return issues
