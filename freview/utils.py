from pathlib import Path
from typing import Dict, List

def write_markdown_report(project_path: Path, structure_issues: List[str], model_report: Dict[Path, List[str]]):
    report_path = project_path / "review_report.md"
    with report_path.open("w") as f:
        f.write(f"# Flask Project Review Report\n\n")

        f.write("## Project Structure\n\n")
        if structure_issues:
            for issue in structure_issues:
                f.write(f"- {issue}\n")
        else:
            f.write("✅ Project structure looks good!\n")

        f.write("\n## Model Checks\n")
        for file_path, issues in model_report.items():
            relative_path = file_path.relative_to(project_path)
            f.write(f"\n### {relative_path}\n")
            for issue in issues:
                f.write(f"- {issue}\n")
