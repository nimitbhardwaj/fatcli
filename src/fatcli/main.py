import typer
from rich.console import Console
from typer import main as typer_main

from fatcli.commands.init import init as init_cmd
from fatcli.commands.meals import meals_app
from fatcli.commands.profile import profile as profile_cmd

console = Console()

app = typer.Typer(
    invoke_without_command=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.callback()
def callback(ctx: typer.Context) -> None:
    """Fatsecret CLI - Manage your Fatsecret account and nutrition data."""
    if ctx.invoked_subcommand is None:
        console.print("\n[bold cyan]Welcome to Fatsecret CLI![/bold cyan]\n")
        console.print("[bold]Quick Start:[/bold]\n")
        console.print(
            "  1. [green]fatcli init[/green]              "
            "- Authenticate with Fatsecret API"
        )
        console.print(
            "  2. [green]fatcli profile[/green]          - View your profile and goals"
        )
        console.print(
            "  3. [green]fatcli meals get --date TODAY[/green]  - View today's meals"
        )
        console.print(
            "  4. [green]fatcli meals search <food>[/green]     - Search for foods"
        )
        console.print("\n[bold]Commands:[/bold]")
        console.print("  [green]init[/green]     - Authenticate with Fatsecret")
        console.print("  [green]profile[/green] - View/edit profile and log weight")
        console.print("  [green]meals[/green]   - View, search, add, or delete meals")
        console.print("\n[dim]Run 'fatcli <command> --help' for more info.[/dim]\n")


app.command()(init_cmd)
app.command()(profile_cmd)
app.add_typer(meals_app, name="meals")


def main() -> None:
    typer_main.get_command(app)
    app()
