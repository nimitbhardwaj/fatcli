import typer
from rich.console import Console
from rich.table import Table

from fatcli.commands import get_fatsecret

console = Console()


def info(
    food_id: str = typer.Argument(..., help="Food ID from search"),
) -> None:
    """Get detailed info about a food (servings, macros)."""
    fs = get_fatsecret()
    food_info = fs.food_get(food_id)

    if not food_info or not isinstance(food_info, dict):
        console.print("[red]Could not fetch food info[/red]")
        return

    food_name = food_info.get("food_name", "Unknown")
    console.print(f"[bold green]{food_name}[/bold green]\n")

    servings = food_info.get("servings", {}).get("serving", [])
    if not isinstance(servings, list):
        servings = [servings]

    table = Table(title="Available servings")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Cal", style="red", no_wrap=True, justify="right")
    table.add_column("P", style="blue", no_wrap=True, justify="right")
    table.add_column("C", style="green", no_wrap=True, justify="right")
    table.add_column("F", style="yellow", no_wrap=True, justify="right")

    for serving in servings:
        if isinstance(serving, dict):
            sid = serving.get("serving_id", "")
            desc = serving.get("serving_description", "")
            cal = serving.get("calories", "0")
            protein = serving.get("protein", "0")
            carbs = serving.get("carbohydrate", "0")
            fat = serving.get("fat", "0")
            table.add_row(sid, desc, cal, protein, carbs, fat)

    console.print(table)
    console.print(
        "\n[dim]To add: fatcli meals add <food_id> --serving <id> "
        "--units <num> --meal <type>[/dim]"
    )
