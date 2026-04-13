from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="FTP user and log commands.")


def _ftp_data(normalized: dict[str, Any]) -> dict[str, Any]:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return data


def _page_items(normalized: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = _ftp_data(normalized)
    rows = data.get("items", [])
    if not isinstance(rows, list):
        rows = []
    items = [row for row in rows if isinstance(row, dict)]
    return data, items


def _ftp_status_summary(data: dict[str, Any]) -> dict[str, Any]:
    status = data.get("status")
    if status is None:
        # Keep a human-readable status even when the backend only reports booleans.
        status = "active" if data.get("isActive") else "inactive"
    return {
        "isExist": data.get("isExist"),
        "isActive": data.get("isActive"),
        "status": status,
    }


def _ftp_user_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "user": row.get("user"),
        "path": row.get("path"),
        "status": row.get("status"),
        "description": row.get("description"),
        "createdAt": row.get("createdAt"),
    }


def _ftp_log_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "ip": row.get("ip"),
        "user": row.get("user"),
        "time": row.get("time"),
        "operation": row.get("operation"),
        "status": row.get("status"),
        "size": row.get("size"),
    }


@app.command("status")
def ftp_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show FTP base status."""
    client = get_client(ctx)
    response = client.request("GET", "/toolbox/ftp/base")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _ftp_data(normalized)
    print_json(_ftp_status_summary(data))


@app.command("list")
def ftp_list(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List FTP users with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/toolbox/ftp/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data, rows = _page_items(normalized)
    items = [_ftp_user_summary(row) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("logs")
def ftp_logs(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List FTP operation logs with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/toolbox/ftp/log/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data, rows = _page_items(normalized)
    items = [_ftp_log_summary(row) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})
