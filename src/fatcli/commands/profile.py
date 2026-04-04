from datetime import datetime, timedelta

import typer
from rich.console import Console

from . import get_fatsecret

console = Console()


def profile(
    weight: float | None = typer.Option(None, "--weight", help="Log weight in kg"),
    goal: float | None = typer.Option(None, "--goal", help="Set goal weight in kg"),
    date: str | None = typer.Option(
        None, "--date", help="Date for weight (YYYY-MM-DD, default: today)"
    ),
) -> None:
    """Get profile info or log weight (with --weight)."""
    fs = get_fatsecret()

    if weight is not None:
        date_dt = None
        if date:
            try:
                date_dt = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                console.print("[red]Error: Date must be in YYYY-MM-DD format[/red]")
                raise typer.Exit(1)

        fs.weight_update(
            current_weight_kg=weight,
            date=date_dt,
            goal_weight_kg=goal,
        )

        console.print(f"[green]Weight logged: {weight} kg[/green]")
        if goal:
            console.print(f"[green]Goal weight updated: {goal} kg[/green]")
        return

    profile_data = fs.profile_get()

    if not profile_data:
        console.print("[yellow]No profile data found.[/yellow]")
        return

    if not isinstance(profile_data, dict):
        console.print(str(profile_data))
        return

    height_cm = float(profile_data.get("height_cm", 0))
    weight_kg = float(profile_data.get("last_weight_kg", 0))
    goal_kg = float(profile_data.get("goal_weight_kg", 0))
    date_int = profile_data.get("last_weight_date_int", "")

    if date_int:
        last_weight_date = datetime(1970, 1, 1) + timedelta(days=int(date_int))
        date_str = last_weight_date.strftime("%Y-%m-%d")
    else:
        date_str = "Unknown"

    bmi = weight_kg / ((height_cm / 100) ** 2) if height_cm > 0 else 0
    diff_from_goal = weight_kg - goal_kg

    console.print("[bold]Profile[/bold]")
    console.print(f"  Height:        [cyan]{height_cm:.0f} cm[/cyan]")
    console.print(
        f"  Current Weight: [cyan]{weight_kg:.1f} kg[/cyan] (as of {date_str})"
    )
    console.print(f"  Goal Weight:    [green]{goal_kg:.1f} kg[/green]")
    console.print(
        f"  Difference:     "
        f"{'[red]' if diff_from_goal > 0 else '[green]'}{diff_from_goal:+.1f} kg[/]"
    )
    console.print(f"  BMI:            [cyan]{bmi:.1f}[/cyan]")
    if 18.5 <= bmi < 25:
        console.print("  Status:         [green]Normal range[/green]")
    elif bmi < 18.5:
        console.print("  Status:         [yellow]Underweight[/yellow]")
    else:
        console.print("  Status:         [red]Overweight[/red]")
