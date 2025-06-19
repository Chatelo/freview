import typer
from pathlib import Path
from freview.project_analyzer import analyze_project_structure
from freview.model_checker import analyze_models
from freview.utils import write_markdown_report

app = typer.Typer()

@app.command()
def review(path: str, markdown: bool = typer.Option(False, help="Generate Markdown report")):
    """Review Flask project structure and SQLAlchemy models."""
    project_path = Path(path).resolve()
    if not project_path.exists():
        typer.echo(f"❌ Path does not exist: {project_path}")
        raise typer.Exit()

    typer.echo(f"🔍 Reviewing {project_path}\n")

    structure_issues = analyze_project_structure(project_path)
    model_issues = analyze_models(project_path)

    typer.echo("📁 Structure Checks:")
    if structure_issues:
        for issue in structure_issues:
            typer.echo(f"- {issue}")
    else:
        typer.echo("✅ Structure looks good")

    typer.echo("\n🧠 Model Checks:")
    for file, results in model_issues.items():
        typer.echo(f"\n📄 {file.relative_to(project_path)}")
        for r in results:
            typer.echo(f"- {r}")

    if markdown:
        write_markdown_report(project_path, structure_issues, model_issues)
        typer.echo("\n📝 Saved Markdown report: review_report.md")

if __name__ == "__main__":
    app()
