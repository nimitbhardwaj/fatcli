import json

import typer
from fatsecret import Fatsecret
from rich.console import Console
from rich.prompt import Prompt

from fatcli.settings import settings

console = Console()

SESSION_FILE = settings.config_dir / "session_token"
OAUTH_TEMP_FILE = settings.config_dir / ".oauth_temp"


def init(
    pin: str | None = typer.Option(
        None, "--pin", help="PIN from FatSecret authorization"
    ),
    url_only: bool = typer.Option(
        False, "--url-only", help="Only print authorization URL"
    ),
) -> None:
    """Authenticate with Fatsecret API.

    Step 1: Get authorization URL
        fatcli init --url-only

    Step 2: Submit PIN to complete
        fatcli init --pin 123456

    Interactive mode (both steps):
        fatcli init
    """
    if not settings.consumer_key or not settings.consumer_secret:
        console.print(
            "[red]Error: FATSECRET_CONSUMER_KEY and FATSECRET_CONSUMER_SECRET "
            "must be set[/red]"
        )
        raise typer.Exit(1)

    fs = Fatsecret(settings.consumer_key, settings.consumer_secret)

    if url_only:
        auth_url = fs.get_authorize_url()
        console.print(f"[blue]{auth_url}[/blue]")

        oauth_temp = {
            "request_token": fs.request_token,
            "request_token_secret": fs.request_token_secret,
        }
        OAUTH_TEMP_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OAUTH_TEMP_FILE, "w") as f:
            json.dump(oauth_temp, f)
        return

    if pin:
        if not OAUTH_TEMP_FILE.exists():
            console.print(
                "[red]Error: No pending authorization. "
                "Run 'fatcli init --url-only' first.[/red]"
            )
            raise typer.Exit(1)

        with open(OAUTH_TEMP_FILE) as f:
            oauth_temp = json.load(f)

        fs = Fatsecret(settings.consumer_key, settings.consumer_secret)
        fs.request_token = oauth_temp["request_token"]
        fs.request_token_secret = oauth_temp["request_token_secret"]

        access_token, access_secret = fs.authenticate(pin)
        OAUTH_TEMP_FILE.unlink(missing_ok=True)
    else:
        auth_url = fs.get_authorize_url()
        console.print(
            f"[bold]Authorization Required[/bold]\n"
            f"Browse to this URL:\n[blue]{auth_url}[/blue]\n"
        )
        pin = Prompt.ask("Enter the PIN from FatSecret")

        access_token, access_secret = fs.authenticate(pin)

    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump({"access_token": access_token, "access_secret": access_secret}, f)

    console.print(
        f"[green]Authentication successful! Session saved to {SESSION_FILE}[/green]"
    )
