from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="System settings, SSL info, snapshots, and groups.")

_INFO_FIELDS = (
    "userName",
    "email",
    "systemIP",
    "panelName",
    "theme",
    "language",
    "serverPort",
    "securityEntrance",
    "expirationTime",
)
_SSL_INFO_FIELDS = (
    "domain",
    "timeout",
    "primaryDomain",
    "provider",
    "rootPath",
    "cert",
    "key",
    "sslID",
)
_SNAPSHOT_FIELDS = (
    "id",
    "name",
    "description",
    "from",
    "status",
    "version",
    "createdAt",
)
_GROUP_FIELDS = ("id", "name", "type")


def _summary(row: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: row.get(field) for field in fields if field in row}


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


@app.command("info")
def info_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show system setting information."""
    client = get_client(ctx)
    response = client.request("POST", "/settings/search", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json(_summary(data, _INFO_FIELDS))


@app.command("interface")
def interface_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show system interface addresses."""
    client = get_client(ctx)
    response = client.request("GET", "/settings/interface")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))


@app.command("basedir")
def basedir_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show the local base directory."""
    client = get_client(ctx)
    response = client.request("GET", "/settings/basedir")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))


@app.command("ssl-info")
def ssl_info_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show system certificate information."""
    client = get_client(ctx)
    response = client.request("GET", "/settings/ssl/info")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json(_summary(data, _SSL_INFO_FIELDS))


@app.command("snapshot-list")
def snapshot_list_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List system snapshots with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/settings/snapshot/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = _extract_rows(data)
    items = [_summary(row, _SNAPSHOT_FIELDS) for row in rows]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("group-list")
def group_list_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List host groups."""
    client = get_client(ctx)
    response = client.request("POST", "/groups/search", body={"type": "host"})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", [])
    rows = _extract_rows(data)
    items = [_summary(row, _GROUP_FIELDS) for row in rows]
    print_json({"count": len(items), "items": items})
