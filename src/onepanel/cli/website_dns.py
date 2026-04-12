from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Website DNS account commands.")


def _dns_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "type": row.get("type"),
    }


@app.command("list")
def list_dns_accounts(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search DNS accounts with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/websites/dns/search", body=body)
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
    items = [_dns_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})
