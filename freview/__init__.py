"""
FReview - Flask Project Review Tool

A comprehensive code review tool for Flask applications that analyzes
project structure, SQLAlchemy models, API patterns, and database
configurations to ensure best practices and identify potential issues.
"""

__version__ = "2.0.0"
__author__ = "Benard Ronoh"
__email__ = "ronohbenard48@gmail.com"

from .project_analyzer import analyze_project_structure
from .model_checker import analyze_models
from .api_analyzer import analyze_api_patterns
from .database_analyzer import analyze_database_patterns
from .utils import write_markdown_report, write_json_report
from .config import ReviewConfig, load_config
from .cli import app as cli_app

__all__ = [
    "analyze_project_structure",
    "analyze_models",
    "analyze_api_patterns",
    "analyze_database_patterns",
    "write_markdown_report",
    "write_json_report",
    "ReviewConfig",
    "load_config",
    "cli_app",
]
