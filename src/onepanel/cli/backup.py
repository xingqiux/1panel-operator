from __future__ import annotations

from collections.abc import Callable
from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Backup accounts and records.")


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


def _print_rows(
    normalized: dict[str, Any],
    summary: Callable[[dict[str, Any]], dict[str, Any]],
    include_total: bool = False,
) -> None:
    data = normalized.get("data", {})
    rows = _extract_rows(data)
    items = [summary(row) for row in rows]
    payload: dict[str, Any] = {"count": len(items), "items": items}
    if include_total:
        payload["total"] = data.get("total") if isinstance(data, dict) else None
    print_json(payload)


def _backup_account_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "type": row.get("type"),
        "bucket": row.get("bucket"),
        "varsJson": row.get("varsJson"),
    }


def _backup_record_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "type": row.get("type"),
        "source": row.get("source"),
        "backupType": row.get("backupType"),
        "fileName": row.get("fileName"),
        "size": row.get("size"),
        "createdAt": row.get("createdAt"),
    }


@app.command("list")
def list_backup_accounts(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List backup accounts."""
    client = get_client(ctx)
    response = client.request("GET", "/settings/backup/search")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    _print_rows(normalized, _backup_account_summary)


@app.command("records")
def list_backup_records(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List backup records with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/settings/backup/record/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    _print_rows(normalized, _backup_record_summary, include_total=True)
