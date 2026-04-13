from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Website SSL certificate commands.")


def _ssl_summary(row: dict[str, Any]) -> dict[str, Any]:
    """Extract summary fields from a single SSL row."""
    return {
        "id": row.get("id"),
        "primaryDomain": row.get("primaryDomain"),
        "provider": row.get("provider"),
        "status": row.get("status"),
        "type": row.get("type"),
        "organization": row.get("organization"),
        "expireDate": row.get("expireDate"),
        "autoRenew": row.get("autoRenew"),
    }


@app.command("list")
def list_ssl(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search SSL certificates with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/websites/ssl/search", body=body)
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
    items = [_ssl_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("show")
def show_ssl(
    ctx: typer.Context,
    ssl_id: int = typer.Argument(..., help="SSL certificate ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show one SSL certificate by ID."""
    client = get_client(ctx)
    response = client.request("GET", f"/websites/ssl/{ssl_id}")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))


@app.command("by-website")
def ssl_by_website(
    ctx: typer.Context,
    website_id: int = typer.Argument(..., help="Website ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show SSL certificate details for one website."""
    client = get_client(ctx)
    response = client.request("GET", f"/websites/ssl/website/{website_id}")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))

