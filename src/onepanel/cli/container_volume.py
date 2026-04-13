from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Docker volumes.")


def _volume_summary(row: dict[str, Any]) -> dict[str, Any]:
    mountpoint = row.get("mountpoint")
    if mountpoint is None:
        mountpoint = row.get("mountPoint") or row.get("Mountpoint") or row.get("MountPoint")
    return {
        "name": row.get("name"),
        "driver": row.get("driver"),
        "mountpoint": mountpoint,
        "createdAt": row.get("createdAt"),
    }


@app.command("list")
def list_volumes(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search volumes with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/containers/volume/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = data.get("items", [])
    if not isinstance(rows, list):
        rows = []
    items = [_volume_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("options")
def options(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List volume options."""
    client = get_client(ctx)
    response = client.request("GET", "/containers/volume")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", [])
    if not isinstance(data, list) and not isinstance(data, dict):
        data = []
    print_json(data)
