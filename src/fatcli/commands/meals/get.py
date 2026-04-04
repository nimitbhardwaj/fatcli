import re

import typer
from rich.console import Console

from fatcli.commands import get_fatsecret

console = Console()


def get(
    date: str = typer.Option(..., "--date", help="Date (YYYY-MM-DD)"),
    summary: bool = typer.Option(False, "--summary", help="Show macro summary only"),
) -> None:
    """Get meals eaten on a date."""
    from datetime import datetime

    try:
        date_dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        console.print("[red]Error: Date must be in YYYY-MM-DD format[/red]")
        raise typer.Exit(1)

    fs = get_fatsecret()
    entries = fs.food_entries_get(date=date_dt)

    if not entries:
        console.print(f"[yellow]No meals found for {date}.[/yellow]")
        return

    if not isinstance(entries, list):
        entries = [entries]

    if summary:
        _print_summary(entries, date)
        return

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        _print_entry(entry)


def _print_summary(entries: list, date: str) -> None:
    total_cal = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0
    total_fiber = 0.0
    total_sodium = 0.0
    total_sugar = 0.0

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        total_cal += float(entry.get("calories", 0))
        total_protein += float(entry.get("protein", 0))
        total_carbs += float(entry.get("carbohydrate", 0))
        total_fat += float(entry.get("fat", 0))
        total_fiber += float(entry.get("fiber", 0))
        total_sodium += float(entry.get("sodium", 0))
        total_sugar += float(entry.get("sugar", 0))

    console.print(f"[bold]Macro Summary for {date}[/bold]")
    console.print(f"  [red]Cal:[/red]   {total_cal:.0f}")
    console.print(f"  [blue]Protein:[/blue] {total_protein:.1f}g")
    console.print(f"  [green]Carbs:[/green]  {total_carbs:.1f}g")
    console.print(f"  [yellow]Fat:[/yellow]   {total_fat:.1f}g")
    console.print(f"  [dim]Fiber:[/dim]   {total_fiber:.1f}g")
    console.print(f"  [dim]Sodium:[/dim]  {total_sodium:.0f}mg")
    console.print(f"  [dim]Sugar:[/dim]   {total_sugar:.1f}g")


def _print_entry(entry: dict) -> None:
    entry_id = entry.get("food_entry_id", "")
    food_name = entry.get("food_entry_name", "")
    cal = float(entry.get("calories", 0))
    protein = float(entry.get("protein", 0))
    carbs = float(entry.get("carbohydrate", 0))
    fat = float(entry.get("fat", 0))
    fiber = float(entry.get("fiber", 0))
    sodium = float(entry.get("sodium", 0))
    sugar = float(entry.get("sugar", 0))

    desc = entry.get("food_entry_description", "")
    if food_name in desc:
        desc = desc.replace(food_name, "").strip(" ,")
    desc = desc.replace(":custom:", "").replace("  ", " ")
    desc = re.sub(r"(\d+)\s+\d+\s+(\w)", r"\1 \2", desc)

    meal = entry.get("meal", "").capitalize()
    food_display = f"[green]{food_name}[/green]"
    if desc:
        food_display += f" [dim]({desc})[/dim]"

    console.print(
        f"[cyan]{entry_id}[/cyan] "
        f"[magenta]{meal:10}[/magenta] {food_display}"
        f"  [red]Cal:[/red] {cal:.0f}"
        f"  [blue]P:[/blue] {protein:.1f}g"
        f"  [green]C:[/green] {carbs:.1f}g"
        f"  [yellow]F:[/yellow] {fat:.1f}g"
        f"  [dim]Fib:[/dim] {fiber:.1f}g"
        f"  [dim]Sod:[/dim] {sodium:.0f}mg"
        f"  [dim]Sug:[/dim] {sugar:.1f}g"
    )
