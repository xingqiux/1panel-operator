from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Docker containers.")


@app.command("list")
def list_containers(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List container names."""
    client = get_client(ctx)
    response = client.request("POST", "/containers/list", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    rows = normalized.get("data", [])
    if not isinstance(rows, list):
        rows = []
    items = [{"name": name} for name in rows if isinstance(name, str)]
    print_json({"count": len(items), "items": items})
