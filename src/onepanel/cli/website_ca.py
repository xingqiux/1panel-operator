from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Website CA certificate commands.")


def _ca_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "keyType": row.get("keyType"),
        "commonName": row.get("commonName"),
        "organization": row.get("organization"),
        "country": row.get("country"),
        "status": row.get("status"),
        "createdAt": row.get("createdAt"),
    }


@app.command("list")
def list_cas(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search CAs with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/websites/ca/search", body=body)
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
    items = [_ca_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("show")
def show_ca(
    ctx: typer.Context,
    ca_id: int = typer.Argument(..., help="CA ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show one CA by ID."""
    client = get_client(ctx)
    response = client.request("GET", f"/websites/ca/{ca_id}")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))

