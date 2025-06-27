import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def write_markdown_report(
    output_path: Path, 
    structure_issues: List[str], 
    model_report: Dict[Path, List[str]],
    api_report: Dict[Path, List[str]] = None,
    db_report: Dict[Path, List[str]] = None
) -> Path:
    """Write a comprehensive Markdown report."""
    if api_report is None:
        api_report = {}
    if db_report is None:
        db_report = {}
        
    report_path = output_path / "freview_report.md"

    with report_path.open("w") as f:
        f.write("# Flask Project Review Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Summary section
        total_issues = (len(structure_issues) + 
                       sum(len(issues) for issues in model_report.values()) +
                       sum(len(issues) for issues in api_report.values()) +
                       sum(len(issues) for issues in db_report.values()))
        total_files = len(model_report) + len(api_report) + len(db_report)

        f.write("## Summary\n\n")
        f.write(f"- **Total Files Analyzed**: {total_files}\n")
        f.write(f"- **Total Issues Found**: {total_issues}\n")
        f.write(f"- **Structure Issues**: {len(structure_issues)}\n")
        f.write(f"- **Model Issues**: {sum(len(issues) for issues in model_report.values())}\n")
        f.write(f"- **API Issues**: {sum(len(issues) for issues in api_report.values())}\n")
        f.write(f"- **Database Issues**: {sum(len(issues) for issues in db_report.values())}\n\n")

        # Project structure section
        f.write("## Project Structure Analysis\n\n")
        if structure_issues:
            for issue in structure_issues:
                severity = "🔴" if "Missing" in issue and "optional" not in issue else "🟡"
                f.write(f"{severity} {issue}\n")
        else:
            f.write("✅ Project structure looks good!\n")

        # Model analysis section
        f.write("\n## SQLAlchemy Model Analysis\n\n")
        if not model_report:
            f.write("⚠️ No model files found in the project.\n")
        else:
            for file_path, issues in model_report.items():
                f.write(f"### {file_path.name}\n\n")
                f.write(f"**File**: `{file_path}`\n\n")

                if not issues:
                    f.write("✅ No issues found.\n\n")
                    continue

                # Categorize issues
                errors = [i for i in issues if i.startswith("❌")]
                warnings = [i for i in issues if i.startswith("⚠️")]
                info = [i for i in issues if i.startswith("ℹ️")]
                success = [i for i in issues if i.startswith("✅")]

                if errors:
                    f.write("**Errors:**\n")
                    for issue in errors:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if warnings:
                    f.write("**Warnings:**\n")
                    for issue in warnings:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if info:
                    f.write("**Information:**\n")
                    for issue in info:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if success:
                    f.write("**Passed Checks:**\n")
                    for issue in success:
                        f.write(f"- {issue}\n")
                    f.write("\n")

        # API analysis section
        f.write("\n## API Pattern Analysis\n\n")
        if not api_report:
            f.write("ℹ️ No API patterns analyzed or found.\n")
        else:
            for file_path, issues in api_report.items():
                # Handle both Path objects and special keys
                if isinstance(file_path, Path):
                    section_name = file_path.name
                    file_display = f"`{file_path}`"
                else:
                    section_name = str(file_path)
                    file_display = section_name
                
                f.write(f"### {section_name}\n\n")
                f.write(f"**Analysis**: {file_display}\n\n")

                if not issues:
                    f.write("✅ No issues found.\n\n")
                    continue

                # Categorize API issues
                errors = [i for i in issues if i.startswith("❌")]
                warnings = [i for i in issues if i.startswith("⚠️")]
                security = [i for i in issues if i.startswith("🔐") or i.startswith("🛡️")]
                recommendations = [i for i in issues if i.startswith("💡")]
                success = [i for i in issues if i.startswith("✅")]

                if errors:
                    f.write("**Errors:**\n")
                    for issue in errors:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if warnings:
                    f.write("**Warnings:**\n")
                    for issue in warnings:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if security:
                    f.write("**Security & Best Practices:**\n")
                    for issue in security:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if recommendations:
                    f.write("**Recommendations:**\n")
                    for issue in recommendations:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if success:
                    f.write("**Passed Checks:**\n")
                    for issue in success:
                        f.write(f"- {issue}\n")
                    f.write("\n")

        # Database analysis section
        f.write("\n## Database Analysis\n\n")
        if not db_report:
            f.write("ℹ️ No database patterns analyzed or found.\n")
        else:
            for file_path, issues in db_report.items():
                # Handle both Path objects and special keys
                if isinstance(file_path, Path):
                    section_name = file_path.name
                    file_display = f"`{file_path}`"
                else:
                    section_name = str(file_path)
                    file_display = section_name
                
                f.write(f"### {section_name}\n\n")
                f.write(f"**Analysis**: {file_display}\n\n")

                if not issues:
                    f.write("✅ No issues found.\n\n")
                    continue

                # Categorize database issues
                errors = [i for i in issues if i.startswith("❌")]
                warnings = [i for i in issues if i.startswith("⚠️")]
                security = [i for i in issues if i.startswith("🔐")]
                recommendations = [i for i in issues if i.startswith("💡")]
                info = [i for i in issues if i.startswith("ℹ️")]
                success = [i for i in issues if i.startswith("✅")]

                if errors:
                    f.write("**Errors:**\n")
                    for issue in errors:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if warnings:
                    f.write("**Warnings:**\n")
                    for issue in warnings:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if security:
                    f.write("**Security:**\n")
                    for issue in security:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if recommendations:
                    f.write("**Recommendations:**\n")
                    for issue in recommendations:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if info:
                    f.write("**Information:**\n")
                    for issue in info:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                if success:
                    f.write("**Passed Checks:**\n")
                    for issue in success:
                        f.write(f"- {issue}\n")
                    f.write("\n")

        # Recommendations section
        f.write("## Overall Recommendations\n\n")
        f.write(_generate_recommendations(structure_issues, model_report, api_report, db_report))

    return report_path


def write_json_report(
    output_path: Path, 
    structure_issues: List[str], 
    model_report: Dict[Path, List[str]],
    api_report: Dict[Path, List[str]] = None,
    db_report: Dict[Path, List[str]] = None
) -> Path:
    """Write a JSON report for programmatic consumption."""
    if api_report is None:
        api_report = {}
    if db_report is None:
        db_report = {}
        
    report_path = output_path / "freview_report.json"

    # Convert Path objects to strings for JSON serialization
    serializable_model_report = {
        str(file_path): issues for file_path, issues in model_report.items()
    }
    serializable_api_report = {
        str(file_path): issues for file_path, issues in api_report.items()
    }
    serializable_db_report = {
        str(file_path): issues for file_path, issues in db_report.items()
    }

    total_issues = (len(structure_issues) + 
                   sum(len(issues) for issues in model_report.values()) +
                   sum(len(issues) for issues in api_report.values()) +
                   sum(len(issues) for issues in db_report.values()))

    report_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "tool_version": "1.0.0",
            "total_files_analyzed": len(model_report) + len(api_report) + len(db_report),
            "total_issues": total_issues,
        },
        "structure_analysis": {
            "issues": structure_issues,
            "status": "passed" if not structure_issues else "failed",
        },
        "model_analysis": {
            "files": serializable_model_report,
            "summary": {
                "files_with_issues": len([f for f, issues in model_report.items() if issues]),
                "total_model_issues": sum(len(issues) for issues in model_report.values()),
            },
        },
        "api_analysis": {
            "files": serializable_api_report,
            "summary": {
                "files_with_issues": len([f for f, issues in api_report.items() if issues]),
                "total_api_issues": sum(len(issues) for issues in api_report.values()),
            },
        },
        "database_analysis": {
            "files": serializable_db_report,
            "summary": {
                "files_with_issues": len([f for f, issues in db_report.items() if issues]),
                "total_database_issues": sum(len(issues) for issues in db_report.values()),
            },
        },
    }

    with report_path.open("w") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    return report_path


def _generate_recommendations(
    structure_issues: List[str], 
    model_report: Dict[Path, List[str]],
    api_report: Dict[Path, List[str]] = None,
    db_report: Dict[Path, List[str]] = None
) -> str:
    """Generate actionable recommendations based on the analysis."""
    if api_report is None:
        api_report = {}
    if db_report is None:
        db_report = {}
        
    recommendations = []

    # Structure recommendations
    if any("Missing entry file" in issue for issue in structure_issues):
        recommendations.append(
            "- Create a main application entry point (app.py, run.py, or main.py) to bootstrap your Flask application."
        )

    if any("Missing 'models/'" in issue for issue in structure_issues):
        recommendations.append(
            "- Create a dedicated 'models/' directory to organize your SQLAlchemy models."
        )

    if any("configuration file" in issue for issue in structure_issues):
        recommendations.append(
            "- Add configuration management with either a config.py file or .env file for environment variables."
        )

    # Model recommendations
    has_missing_tablename = any(
        any("Missing __tablename__" in issue for issue in issues)
        for issues in model_report.values()
    )
    if has_missing_tablename:
        recommendations.append(
            "- Add __tablename__ attribute to all SQLAlchemy models to explicitly define table names."
        )

    has_missing_pk = any(
        any("No primary key defined" in issue for issue in issues)
        for issues in model_report.values()
    )
    if has_missing_pk:
        recommendations.append(
            "- Ensure all models have a primary key field, typically an 'id' column with primary_key=True."
        )

    has_circular_imports = any(
        any("Circular import detected" in issue for issue in issues)
        for issues in model_report.values()
    )
    if has_circular_imports:
        recommendations.append(
            "- Resolve circular imports by using string-based relationship definitions or restructuring your models."
        )

    # API recommendations
    has_missing_auth = any(
        any("may need authentication" in issue for issue in issues)
        for issues in api_report.values()
    )
    if has_missing_auth:
        recommendations.append(
            "- Implement authentication for sensitive API endpoints using Flask-Login, JWT, or similar."
        )

    has_missing_validation = any(
        any("should validate input" in issue for issue in issues)
        for issues in api_report.values()
    )
    if has_missing_validation:
        recommendations.append(
            "- Add input validation to API endpoints using Flask-WTF, marshmallow, or similar libraries."
        )

    has_missing_error_handling = any(
        any("should include error handling" in issue for issue in issues)
        for issues in api_report.values()
    )
    if has_missing_error_handling:
        recommendations.append(
            "- Implement proper error handling in API routes with try-catch blocks and meaningful error responses."
        )

    has_versioning_suggestion = any(
        any("Consider API versioning" in issue for issue in issues)
        for issues in api_report.values()
    )
    if has_versioning_suggestion:
        recommendations.append(
            "- Implement API versioning (e.g., /api/v1/) for better API evolution and backward compatibility."
        )

    # Database recommendations
    has_migration_issues = any(
        any("No migrations directory found" in issue for issue in issues)
        for issues in db_report.values()
    )
    if has_migration_issues:
        recommendations.append(
            "- Set up database migrations with Flask-Migrate: pip install Flask-Migrate && flask db init"
        )

    has_config_issues = any(
        any("No database configuration found" in issue for issue in issues)
        for issues in db_report.values()
    )
    if has_config_issues:
        recommendations.append(
            "- Configure database connection in config.py with SQLALCHEMY_DATABASE_URI."
        )

    has_security_issues = any(
        any("hardcoded database credentials" in issue for issue in issues)
        for issues in db_report.values()
    )
    if has_security_issues:
        recommendations.append(
            "- Move database credentials to environment variables for security."
        )

    has_n_plus_one = any(
        any("N+1 query problem" in issue for issue in issues)
        for issues in db_report.values()
    )
    if has_n_plus_one:
        recommendations.append(
            "- Optimize database queries by using joins and eager loading to avoid N+1 query problems."
        )

    # General recommendations
    recommendations.extend(
        [
            "- Consider using Flask-Migrate for database migrations.",
            "- Implement model validation using SQLAlchemy validators or Flask-WTF.",
            "- Add comprehensive docstrings to your models and methods.",
            "- Consider implementing model mixins for common functionality (timestamps, soft deletes, etc.).",
        ]
    )

    return (
        "\n".join(recommendations)
        if recommendations
        else "No specific recommendations at this time."
    )
