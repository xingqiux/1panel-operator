from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="ClamAV antivirus commands.")


def _clam_data(normalized: dict[str, Any]) -> dict[str, Any]:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return data


def _page_items(normalized: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = _clam_data(normalized)
    rows = data.get("items", [])
    if not isinstance(rows, list):
        rows = []
    items = [row for row in rows if isinstance(row, dict)]
    return data, items


def _list_summary(row: dict[str, Any]) -> dict[str, Any]:
    """Extract summary fields from a single ClamAV scan row."""
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "path": row.get("path"),
        "infectedStrategy": row.get("infectedStrategy"),
        "status": row.get("status"),
        "createdAt": row.get("createdAt"),
    }


def _record_summary(row: dict[str, Any]) -> dict[str, Any]:
    """Extract summary fields from a single ClamAV record row."""
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "clamID": row.get("clamID"),
        "status": row.get("status"),
        "startTime": row.get("startTime"),
        "endTime": row.get("endTime"),
    }


@app.command("status")
def clam_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show ClamAV base status."""
    client = get_client(ctx)
    response = client.request("GET", "/toolbox/clam/base")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _clam_data(normalized)
    print_json({
        "isExist": data.get("isExist"),
        "isActive": data.get("isActive"),
        "version": data.get("version"),
        "freshVersion": data.get("freshVersion"),
    })


@app.command("list")
def clam_list(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List ClamAV scan definitions with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/toolbox/clam/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data, rows = _page_items(normalized)
    items = [_list_summary(row) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("records")
def clam_records(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List ClamAV scan records with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/toolbox/clam/record/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data, rows = _page_items(normalized)
    items = [_record_summary(row) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})
