import typer
from rich.console import Console

from fatcli.commands.meals.add import add
from fatcli.commands.meals.delete import delete
from fatcli.commands.meals.get import get
from fatcli.commands.meals.info import info
from fatcli.commands.meals.search import search

console = Console()

meals_app = typer.Typer(
    invoke_without_command=True,
    rich_markup_mode="rich",
)


@meals_app.callback()
def meals_callback(ctx: typer.Context) -> None:
    """Manage meals - view, search, add, or delete food entries."""
    if ctx.invoked_subcommand is None:
        console.print("\n[bold cyan]Meals Commands[/bold cyan]\n")
        console.print("[bold]View meals:[/bold]")
        console.print(
            "  [green]fatcli meals get --date 2026-04-04[/green]        "
            "View meals for a date"
        )
        console.print(
            "  [green]fatcli meals get --date 2026-04-04 --summary[/green] "
            "Show macro summary only\n"
        )
        console.print("[bold]Find food:[/bold]")
        console.print(
            "  [green]fatcli meals search chicken[/green]             Search foods"
        )
        console.print(
            "  [green]fatcli meals info 1641[/green]                 "
            "Get food details with servings\n"
        )
        console.print("[bold]Add food:[/bold]")
        console.print(
            "  [green]fatcli meals add 1641 --serving 50321 --units 1 "
            "--meal lunch[/green]\n"
        )
        console.print("[bold]Remove food:[/bold]")
        console.print(
            "  [green]fatcli meals delete 23112601131[/green]         "
            "Delete entry by ID\n"
        )
        console.print("[dim]Tip: Use 'fatcli meals get --date TODAY'[/dim]")
        console.print("[dim]to view today's meals.[/dim]")


meals_app.command()(get)
meals_app.command()(search)
meals_app.command()(add)
meals_app.command()(info)
meals_app.command()(delete)

__all__ = ["meals_app", "get", "search", "add", "info", "delete"]
