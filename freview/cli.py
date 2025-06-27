import typer
import logging
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from freview.project_analyzer import analyze_project_structure
from freview.model_checker import analyze_models
from freview.api_analyzer import analyze_api_patterns
from freview.database_analyzer import analyze_database_patterns
from freview.utils import write_markdown_report, write_json_report
from freview import __version__

console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"freview version {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="freview",
    help="Flask Project Review Tool - Comprehensive analysis of project structure, SQLAlchemy models, API patterns, and database configurations",
    rich_markup_mode="rich",
    add_completion=False,
)


@app.command()
def review(
    path: str = typer.Argument(..., help="Path to the Flask project to review"),
    markdown: bool = typer.Option(False, "--markdown", "-m", help="Generate Markdown report"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Generate JSON report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    output_dir: Optional[str] = typer.Option(
        None, "--output-dir", "-o", help="Output directory for reports"
    ),
    skip_api: bool = typer.Option(False, "--skip-api", help="Skip API analysis"),
    skip_db: bool = typer.Option(False, "--skip-db", help="Skip database analysis"),
    skip_models: bool = typer.Option(False, "--skip-models", help="Skip model analysis"),
    skip_structure: bool = typer.Option(False, "--skip-structure", help="Skip structure analysis"),
):
    """Review Flask project structure, SQLAlchemy models, API patterns, and database configurations with comprehensive analysis."""

    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    project_path = Path(path).resolve()
    if not project_path.exists():
        console.print(f"[red]❌ Path does not exist:[/red] {project_path}")
        raise typer.Exit(1)

    if not project_path.is_dir():
        console.print(f"[red]❌ Path is not a directory:[/red] {project_path}")
        raise typer.Exit(1)

    # Create output directory if specified
    output_path = Path(output_dir) if output_dir else project_path
    if output_dir and not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    console.print(Panel.fit("🔍 Reviewing Flask Project", style="bold blue"))
    console.print(f"[dim]📁 Project Path:[/dim] {project_path}\n")

    try:
        # Analyze project with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:

            # Structure analysis
            structure_issues = []
            if not skip_structure:
                progress.add_task("Analyzing project structure...", total=None)
                structure_issues = analyze_project_structure(project_path)

            # Model analysis
            model_issues = {}
            if not skip_models:
                progress.add_task("Analyzing SQLAlchemy models...", total=None)
                model_issues = analyze_models(project_path)

            # API analysis
            api_issues = {}
            if not skip_api:
                progress.add_task("Analyzing API patterns...", total=None)
                api_issues = analyze_api_patterns(project_path)

            # Database analysis
            db_issues = {}
            if not skip_db:
                progress.add_task("Analyzing database patterns...", total=None)
                db_issues = analyze_database_patterns(project_path)

        # Display results with rich formatting
        if not skip_structure:
            _display_structure_results(structure_issues)
        if not skip_models:
            _display_model_results(model_issues, project_path)
        if not skip_api:
            _display_api_results(api_issues, project_path)
        if not skip_db:
            _display_database_results(db_issues, project_path)

        # Generate reports
        if markdown:
            report_path = write_markdown_report(output_path, structure_issues, model_issues, api_issues, db_issues)
            console.print(f"\n[green]📝 Markdown report saved:[/green] {report_path}")

        if json_output:
            report_path = write_json_report(output_path, structure_issues, model_issues, api_issues, db_issues)
            console.print(f"\n[green]📝 JSON report saved:[/green] {report_path}")

    except Exception as e:
        console.print(f"[red]❌ Error during analysis:[/red] {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


def _display_structure_results(issues: List[str]):
    """Display structure analysis results with rich formatting."""
    console.print("\n[bold]📁 Project Structure Analysis[/bold]")

    if not issues:
        console.print("✅ [green]Project structure looks good![/green]")
        return

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Icon", style="yellow", no_wrap=True)
    table.add_column("Issue", style="dim")

    for issue in issues:
        if "Missing" in issue and "optional" not in issue:
            table.add_row("❌", f"[red]{issue}[/red]")
        else:
            table.add_row("⚠️", f"[yellow]{issue}[/yellow]")

    console.print(table)


def _display_model_results(model_issues: dict, project_path: Path):
    """Display model analysis results with rich formatting."""
    console.print("\n[bold]🧠 SQLAlchemy Model Analysis[/bold]")

    if not model_issues:
        console.print("[yellow]⚠️ No model files found in the project[/yellow]")
        return

    for file_path, issues in model_issues.items():
        relative_path = file_path.relative_to(project_path)

        console.print(f"\n[bold cyan]📄 {relative_path}[/bold cyan]")

        if not issues:
            console.print("  [dim]No issues found[/dim]")
            continue

        for issue in issues:
            if issue.startswith("❌"):
                console.print(f"  [red]{issue}[/red]")
            elif issue.startswith("⚠️"):
                console.print(f"  [yellow]{issue}[/yellow]")
            elif issue.startswith("✅"):
                console.print(f"  [green]{issue}[/green]")
            elif issue.startswith("ℹ️"):
                console.print(f"  [blue]{issue}[/blue]")
            else:
                console.print(f"  [dim]{issue}[/dim]")


def _display_api_results(api_issues: dict, project_path: Path):
    """Display API analysis results with rich formatting."""
    console.print("\n[bold]🌐 API Pattern Analysis[/bold]")

    if not api_issues:
        console.print("[yellow]⚠️ No API patterns detected in the project[/yellow]")
        return

    for file_path, issues in api_issues.items():
        if isinstance(file_path, Path):
            try:
                relative_path = file_path.relative_to(project_path)
                console.print(f"\n[bold cyan]📄 {relative_path}[/bold cyan]")
            except ValueError:
                # Handle special analysis keys like "API_ARCHITECTURE"
                console.print(f"\n[bold cyan]📊 {file_path.name}[/bold cyan]")
        else:
            # Handle string keys
            console.print(f"\n[bold cyan]📊 {str(file_path)}[/bold cyan]")

        if not issues:
            console.print("  [dim]No issues found[/dim]")
            continue

        for issue in issues:
            if issue.startswith("❌"):
                console.print(f"  [red]{issue}[/red]")
            elif issue.startswith("⚠️"):
                console.print(f"  [yellow]{issue}[/yellow]")
            elif issue.startswith("✅"):
                console.print(f"  [green]{issue}[/green]")
            elif issue.startswith("🔐") or issue.startswith("🛡️"):
                console.print(f"  [magenta]{issue}[/magenta]")
            elif issue.startswith("💡"):
                console.print(f"  [blue]{issue}[/blue]")
            elif issue.startswith("📈") or issue.startswith("🏗️"):
                console.print(f"  [cyan]{issue}[/cyan]")
            else:
                console.print(f"  [dim]{issue}[/dim]")


def _display_database_results(db_issues: dict, project_path: Path):
    """Display database analysis results with rich formatting."""
    console.print("\n[bold]🗄️ Database Analysis[/bold]")

    if not db_issues:
        console.print("[yellow]⚠️ No database patterns detected in the project[/yellow]")
        return

    for file_path, issues in db_issues.items():
        if isinstance(file_path, Path):
            try:
                relative_path = file_path.relative_to(project_path)
                console.print(f"\n[bold cyan]📄 {relative_path}[/bold cyan]")
            except ValueError:
                # Handle special analysis keys
                console.print(f"\n[bold cyan]📊 {file_path.name}[/bold cyan]")
        else:
            # Handle string keys
            console.print(f"\n[bold cyan]📊 {str(file_path)}[/bold cyan]")

        if not issues:
            console.print("  [dim]No issues found[/dim]")
            continue

        for issue in issues:
            if issue.startswith("❌"):
                console.print(f"  [red]{issue}[/red]")
            elif issue.startswith("⚠️"):
                console.print(f"  [yellow]{issue}[/yellow]")
            elif issue.startswith("✅"):
                console.print(f"  [green]{issue}[/green]")
            elif issue.startswith("🔐"):
                console.print(f"  [magenta]{issue}[/magenta]")
            elif issue.startswith("💡"):
                console.print(f"  [blue]{issue}[/blue]")
            elif issue.startswith("ℹ️"):
                console.print(f"  [cyan]{issue}[/cyan]")
            else:
                console.print(f"  [dim]{issue}[/dim]")


@app.command()
def version():
    """Show the version of freview."""
    from freview import __version__

    console.print(f"freview version {__version__}")


@app.command()
def init(
    path: str = typer.Argument(".", help="Path to initialize configuration in"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing configuration"),
):
    """Initialize a .freview.toml configuration file in the project."""
    from freview.config import create_default_config

    project_path = Path(path).resolve()
    if not project_path.exists():
        console.print(f"[red]❌ Path does not exist:[/red] {project_path}")
        raise typer.Exit(1)

    config_path = project_path / ".freview.toml"

    if config_path.exists() and not force:
        console.print(f"[yellow]⚠️ Configuration file already exists:[/yellow] {config_path}")
        console.print("Use --force to overwrite the existing configuration.")
        raise typer.Exit(1)

    try:
        created_path = create_default_config(project_path)
        console.print(f"[green]✅ Created configuration file:[/green] {created_path}")
        console.print("\n[dim]You can now customize the settings in .freview.toml[/dim]")
    except Exception as e:
        console.print(f"[red]❌ Error creating configuration:[/red] {e}")
        raise typer.Exit(1)


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-V", callback=version_callback, is_eager=True, help="Show version and exit"
    ),
):
    """
    FReview - Flask Project Review Tool

    Analyze Flask project structure and SQLAlchemy models to ensure best practices.
    """
    pass


if __name__ == "__main__":
    app()
