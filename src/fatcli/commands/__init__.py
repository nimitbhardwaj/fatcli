import json

from fatsecret import Fatsecret
from rich.console import Console

from fatcli.settings import settings

console = Console()

SESSION_FILE = settings.config_dir / "session_token"


def get_session() -> tuple[str, str] | None:
    if not SESSION_FILE.exists():
        return None
    with open(SESSION_FILE) as f:
        data = json.load(f)
    return data.get("access_token"), data.get("access_secret")


def get_fatsecret() -> Fatsecret:
    if not settings.consumer_key or not settings.consumer_secret:
        console.print(
            "[red]Error: FATSECRET_CONSUMER_KEY and FATSECRET_CONSUMER_SECRET "
            "must be set[/red]"
        )
        raise SystemExit(1)

    session = get_session()
    if not session:
        console.print("[red]Error: Not authenticated. Run 'fatcli init' first.[/red]")
        raise SystemExit(1)

    access_token, access_secret = session
    return Fatsecret(
        settings.consumer_key,
        settings.consumer_secret,
        session_token=(access_token, access_secret),
    )
