"""
Configuration management for freview.
"""

import tomllib
from pathlib import Path
from typing import List, Pattern
from dataclasses import dataclass, field
import re


@dataclass
class ReviewConfig:
    """Configuration for freview analysis."""

    # Model directories to scan
    model_dirs: List[str] = field(default_factory=lambda: ["models", "app/models", "src/models"])

    # File patterns to include/exclude
    include_patterns: List[str] = field(default_factory=lambda: ["*.py"])
    exclude_patterns: List[str] = field(default_factory=lambda: ["__pycache__", "*.pyc", "test_*"])

    # Naming conventions
    class_name_pattern: str = r"^[A-Z][a-zA-Z0-9]+$"
    table_name_pattern: str = r"^[a-z][a-z0-9_]*$"

    # Checks to skip
    skip_checks: List[str] = field(default_factory=list)

    # Severity levels
    error_as_warning: bool = False
    warning_as_error: bool = False

    # Output configuration
    max_issues_per_file: int = 50
    show_success_messages: bool = True

    # Model analysis settings
    check_repr_methods: bool = True
    check_str_methods: bool = True
    require_docstrings: bool = False

    @property
    def class_name_regex(self) -> Pattern[str]:
        """Compiled regex for class name validation."""
        return re.compile(self.class_name_pattern)

    @property
    def table_name_regex(self) -> Pattern[str]:
        """Compiled regex for table name validation."""
        return re.compile(self.table_name_pattern)


def load_config(project_path: Path) -> ReviewConfig:
    """
    Load configuration from project directory.

    Looks for .freview.toml in the project root.
    """
    config = ReviewConfig()
    config_file = project_path / ".freview.toml"

    if not config_file.exists():
        return config

    try:
        with open(config_file, "rb") as f:
            data = tomllib.load(f)

        # Extract freview section
        freview_config = data.get("freview", {})

        # Update config with file values
        for key, value in freview_config.items():
            if hasattr(config, key):
                setattr(config, key, value)

    except Exception as e:
        # If config file is malformed, use defaults
        print(f"Warning: Could not load config file: {e}")

    return config


def create_default_config(project_path: Path) -> Path:
    """Create a default .freview.toml configuration file."""
    config_path = project_path / ".freview.toml"

    default_config = """# FReview Configuration File
# https://github.com/ronoh48/freview

[freview]
# Directories to scan for models (relative to project root)
model_dirs = ["models", "app/models", "src/models"]

# File patterns
include_patterns = ["*.py"]
exclude_patterns = ["__pycache__", "*.pyc", "test_*", "*_test.py"]

# Naming convention patterns (regex)
class_name_pattern = "^[A-Z][a-zA-Z0-9]+$"
table_name_pattern = "^[a-z][a-z0-9_]*$"

# Skip specific checks
# Available: unused_models, circular_imports, repr_methods, str_methods
skip_checks = []

# Severity settings
error_as_warning = false
warning_as_error = false

# Output settings
max_issues_per_file = 50
show_success_messages = true

# Model analysis settings
check_repr_methods = true
check_str_methods = true
require_docstrings = false
"""

    config_path.write_text(default_config)
    return config_path


def get_effective_model_dirs(config: ReviewConfig, project_path: Path) -> List[Path]:
    """Get the actual model directories that exist in the project."""
    model_dirs = []

    for dir_pattern in config.model_dirs:
        model_path = project_path / dir_pattern
        if model_path.exists() and model_path.is_dir():
            model_dirs.append(model_path)

    return model_dirs
