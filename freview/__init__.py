"""
FReview - Flask Project Review Tool

A comprehensive code review tool for Flask applications that analyzes
project structure and SQLAlchemy models to ensure best practices.
"""

__version__ = "1.0.0"
__author__ = "Benard Ronoh"
__email__ = "ronohbenard48@gmail.com"

from .project_analyzer import analyze_project_structure
from .model_checker import analyze_models
from .utils import write_markdown_report, write_json_report
from .config import ReviewConfig, load_config
from .cli import app as cli_app

__all__ = [
    "analyze_project_structure",
    "analyze_models",
    "write_markdown_report",
    "write_json_report",
    "ReviewConfig",
    "load_config",
    "cli_app",
]
