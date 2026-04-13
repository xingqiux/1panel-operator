from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Installed applications.")


def _summary(row: dict[str, Any]) -> dict[str, Any]:
    """Extract summary fields from a single app install row."""
    return {
        "id": row.get("id"),
        "key": row.get("key"),
        "name": row.get("name"),
        "version": row.get("version"),
        "status": row.get("status"),
        "appName": row.get("appName"),
        "containerName": row.get("containerName"),
        "createdAt": row.get("createdAt"),
        "updatedAt": row.get("updatedAt"),
    }


@app.command("list")
def list_apps(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List installed applications."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/apps/installed/search", body=body)
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
    items = [_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("info")
def info_cmd(
    ctx: typer.Context,
    key: str = typer.Argument(..., help="App key, e.g. openresty, mysql."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Check if an app is installed."""
    client = get_client(ctx)
    response = client.request("POST", "/apps/installed/check", body={"key": key})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "key": key,
        "isExist": data.get("isExist"),
        "name": data.get("name"),
        "version": data.get("version"),
        "containerName": data.get("containerName"),
        "createdAt": data.get("createdAt"),
        "lastBackupAt": data.get("lastBackupAt"),
        "appInstallId": data.get("appInstallId"),
    })
