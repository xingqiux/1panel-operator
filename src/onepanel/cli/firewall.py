from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Firewall status.")


@app.command("status")
def firewall_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show firewall base status."""
    client = get_client(ctx)
    response = client.request("GET", "/hosts/firewall/base")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    summary = {
        "name": data.get("name"),
        "status": data.get("status"),
        "pingStatus": data.get("pingStatus"),
        "version": data.get("version"),
    }
    print_json(summary)
