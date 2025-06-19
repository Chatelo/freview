import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def write_markdown_report(
    output_path: Path, structure_issues: List[str], model_report: Dict[Path, List[str]]
) -> Path:
    """Write a comprehensive Markdown report."""
    report_path = output_path / "freview_report.md"

    with report_path.open("w") as f:
        f.write("# Flask Project Review Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Summary section
        total_issues = len(structure_issues) + sum(len(issues) for issues in model_report.values())
        total_files = len(model_report)

        f.write("## Summary\n\n")
        f.write(f"- **Total Files Analyzed**: {total_files}\n")
        f.write(f"- **Total Issues Found**: {total_issues}\n")
        f.write(f"- **Structure Issues**: {len(structure_issues)}\n")
        f.write(f"- **Model Issues**: {sum(len(issues) for issues in model_report.values())}\n\n")

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

        # Recommendations section
        f.write("## Recommendations\n\n")
        f.write(_generate_recommendations(structure_issues, model_report))

    return report_path


def write_json_report(
    output_path: Path, structure_issues: List[str], model_report: Dict[Path, List[str]]
) -> Path:
    """Write a JSON report for programmatic consumption."""
    report_path = output_path / "freview_report.json"

    # Convert Path objects to strings for JSON serialization
    serializable_model_report = {
        str(file_path): issues for file_path, issues in model_report.items()
    }

    report_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "tool_version": "1.0.0",
            "total_files_analyzed": len(model_report),
            "total_issues": len(structure_issues)
            + sum(len(issues) for issues in model_report.values()),
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
    }

    with report_path.open("w") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    return report_path


def _generate_recommendations(
    structure_issues: List[str], model_report: Dict[Path, List[str]]
) -> str:
    """Generate actionable recommendations based on the analysis."""
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
