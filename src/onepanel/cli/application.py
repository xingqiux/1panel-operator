from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Installed applications.")


@app.command("list")
def list_apps(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List installed applications."""
    client = get_client(ctx)
    response = client.request("GET", "/apps/installed/list")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    rows = normalized.get("data", [])
    if not isinstance(rows, list):
        rows = []
    items = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        items.append({
            "id": row.get("id"),
            "key": row.get("key"),
            "name": row.get("name"),
            "version": row.get("version"),
            "status": row.get("status"),
            "createdAt": row.get("createdAt"),
        })
    print_json({"count": len(items), "items": items})
