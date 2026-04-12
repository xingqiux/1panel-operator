from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Website ACME account commands.")


def _acme_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "email": row.get("email"),
        "type": row.get("type"),
        "url": row.get("url"),
        "keyType": row.get("keyType"),
    }


@app.command("list")
def list_acme_accounts(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search ACME accounts with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/websites/acme/search", body=body)
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
    items = [_acme_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})

