import typer
from rich.console import Console
from rich.table import Table

from fatcli.commands import get_fatsecret

console = Console()


def search(
    query: str = typer.Argument(..., help="Food to search for"),
    max_results: int = typer.Option(10, "--max", help="Max results to show"),
) -> None:
    """Search for foods in Fatsecret database."""
    fs = get_fatsecret()
    results = fs.foods_search(search_expression=query, max_results=max_results)

    if not results:
        console.print(f"[yellow]No foods found for '{query}'[/yellow]")
        return

    if not isinstance(results, list):
        results = [results]

    table = Table(title=f"Search results for '{query}'")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Food Name", style="green")

    for food in results:
        if isinstance(food, dict):
            food_id = food.get("food_id", "")
            food_name = food.get("food_name", "")
            table.add_row(food_id, food_name)

    console.print(table)
    console.print("\n[dim]To add a food, run: fatcli meals add <food_id>[/dim]")
