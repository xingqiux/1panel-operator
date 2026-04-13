from __future__ import annotations

from collections.abc import Callable
from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Log commands.")


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


def _print_text_or_json(value: Any) -> None:
    if isinstance(value, str):
        typer.echo(value)
        return
    print_json(value)


def _print_page(
    normalized: dict[str, Any],
    summary: Callable[[dict[str, Any]], dict[str, Any]],
) -> None:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = _extract_rows(data)
    items = [summary(row) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


def _login_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "ip": row.get("ip"),
        "address": row.get("address"),
        "agent": row.get("agent"),
        "status": row.get("status"),
        "message": row.get("message"),
        "createdAt": row.get("createdAt"),
    }


def _operation_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "group": row.get("group"),
        "source": row.get("source"),
        "action": row.get("action"),
        "ip": row.get("ip"),
        "status": row.get("status"),
        "message": row.get("message"),
        "createdAt": row.get("createdAt"),
    }


@app.command("login")
def login_logs(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search login logs."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/logs/login", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    _print_page(normalized, _login_summary)


@app.command("operation")
def operation_logs(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search operation logs."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/logs/operation", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    _print_page(normalized, _operation_summary)


@app.command("system")
def system_logs(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Load system logs."""
    client = get_client(ctx)
    response = client.request("POST", "/logs/system", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    _print_text_or_json(normalized.get("data"))


@app.command("files")
def system_log_files(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List system log files."""
    client = get_client(ctx)
    response = client.request("GET", "/logs/system/files")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    _print_text_or_json(normalized.get("data"))
