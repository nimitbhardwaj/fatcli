import typer
from rich.console import Console

from fatcli.commands import get_fatsecret

console = Console()


def delete(
    entry_id: str = typer.Argument(..., help="Entry ID to delete"),
) -> None:
    """Delete a food entry from your diary."""
    fs = get_fatsecret()
    fs.food_entry_delete(food_entry_id=entry_id)
    console.print(f"[green]Deleted entry {entry_id}[/green]")
