from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Scheduled cron job commands.")


def _response_data(response: Any) -> dict[str, Any]:
    if not isinstance(response, dict):
        return {}
    data = response.get("data", {})
    if isinstance(data, dict):
        return data
    return {}


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


def _cronjob_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "type": row.get("type"),
        "specType": row.get("specType"),
        "spec": row.get("spec"),
        "status": row.get("status"),
        "lastRecordTime": row.get("lastRecordTime"),
        "createdAt": row.get("createdAt"),
    }


@app.command("list")
def list_cronjobs(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List scheduled cron jobs with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/cronjobs/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _response_data(normalized)
    rows = _extract_rows(data)
    items = [_cronjob_summary(row) for row in rows]
    print_json({
        "count": len(items),
        "total": data.get("total"),
        "items": items,
    })


@app.command("show")
def show_cronjob(
    ctx: typer.Context,
    cronjob_id: int = typer.Argument(..., help="Cronjob ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show one cron job by ID."""
    client = get_client(ctx)
    response = client.request("GET", f"/cronjobs/{cronjob_id}")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _response_data(normalized)
    print_json(data)
