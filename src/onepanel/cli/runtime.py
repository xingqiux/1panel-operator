from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Application runtime commands.")


def _normalize_response(client: Any, response: Any) -> Any:
    if not isinstance(response, dict):
        return response
    return client.normalize_response_payload(response)


def _extract_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        rows = data.get("items")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
        rows = data.get("list")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def _runtime_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "appDetailId": row.get("appDetailId"),
        "type": row.get("type"),
        "image": row.get("image"),
        "status": row.get("status"),
        "version": row.get("version"),
        "createdAt": row.get("createdAt"),
    }


@app.command("list")
def list_runtimes(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List runtimes with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/runtimes/search", body=body)
    normalized = _normalize_response(client, response)
    if raw or not isinstance(normalized, dict):
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = _extract_rows(data)
    items = [_runtime_summary(row) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("show")
def show_runtime(
    ctx: typer.Context,
    runtime_id: int = typer.Argument(..., help="Runtime ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show one runtime by ID."""
    client = get_client(ctx)
    response = client.request("GET", f"/runtimes/{runtime_id}")
    normalized = _normalize_response(client, response)
    if raw or not isinstance(normalized, dict):
        print_json(normalized)
        return
    print_json(normalized.get("data"))
