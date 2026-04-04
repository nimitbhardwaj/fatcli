from datetime import datetime

import typer
from rich.console import Console

from fatcli.commands import get_fatsecret

console = Console()


def add(
    food_id: str = typer.Argument(..., help="Food ID from search"),
    serving_id: str = typer.Option(
        ..., "--serving", help="Serving ID (from food info)"
    ),
    units: float = typer.Option(..., "--units", help="Number of servings"),
    meal: str = typer.Option(
        ..., "--meal", help="Meal type (breakfast/lunch/dinner/other)"
    ),
    date: str | None = typer.Option(
        None, "--date", help="Date (YYYY-MM-DD, default: today)"
    ),
) -> None:
    """Add a food entry to your diary."""
    date_dt = None
    if date:
        try:
            date_dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Error: Date must be in YYYY-MM-DD format[/red]")
            raise typer.Exit(1)

    fs = get_fatsecret()

    food_info = fs.food_get(food_id)
    food_name = (
        food_info.get("food_name", "Unknown")
        if isinstance(food_info, dict)
        else "Unknown"
    )

    fs.food_entry_create(
        food_id=food_id,
        food_entry_name=food_name,
        serving_id=serving_id,
        number_of_units=units,
        meal=meal.lower(),
        date=date_dt,
    )

    console.print(f"[green]Added: {food_name} ({units}x) to {meal}[/green]")
