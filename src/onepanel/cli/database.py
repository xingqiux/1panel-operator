from __future__ import annotations

from collections.abc import Callable
from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Database, MySQL, PostgreSQL, and Redis commands.")


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


def _print_list(
    normalized: dict[str, Any],
    summary: Callable[[dict[str, Any]], dict[str, Any]],
    include_total: bool = True,
) -> None:
    data = normalized.get("data", {})
    rows = _extract_rows(data)
    items = [summary(row) for row in rows]
    payload: dict[str, Any] = {"count": len(items), "items": items}
    if include_total:
        payload["total"] = data.get("total") if isinstance(data, dict) else None
    print_json(payload)


def _print_data(normalized: dict[str, Any], raw: bool) -> None:
    print_json(normalized if raw else normalized.get("data"))


def _database_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "type": row.get("type"),
        "version": row.get("version"),
        "from": row.get("from"),
        "address": row.get("address"),
        "port": row.get("port"),
        "status": row.get("status"),
        "createdAt": row.get("createdAt"),
    }


def _mysql_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "mysqlName": row.get("mysqlName"),
        "format": row.get("format"),
        "username": row.get("username"),
        "permission": row.get("permission"),
        "description": row.get("description"),
        "createdAt": row.get("createdAt"),
    }


def _pg_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "pgName": row.get("pgName"),
        "format": row.get("format"),
        "username": row.get("username"),
        "description": row.get("description"),
        "createdAt": row.get("createdAt"),
    }


def _redis_command_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "command": row.get("command"),
    }


@app.command("list")
def list_databases(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search databases with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/databases/db/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    _print_list(normalized, _database_summary)


@app.command("show")
def show_database(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Database name."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show one database by name."""
    client = get_client(ctx)
    response = client.request("GET", f"/databases/db/{name}")
    normalized = client.normalize_response_payload(response)
    _print_data(normalized, raw)


@app.command("mysql-list")
def mysql_list(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search MySQL databases with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/databases/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    _print_list(normalized, _mysql_summary)


@app.command("mysql-status")
def mysql_status(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="MySQL database name."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show MySQL database status."""
    client = get_client(ctx)
    response = client.request("POST", "/databases/status", body={"name": name, "type": "mysql"})
    normalized = client.normalize_response_payload(response)
    _print_data(normalized, raw)


@app.command("pg-list")
def pg_list(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """Search PostgreSQL databases with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/databases/pg/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    _print_list(normalized, _pg_summary)


@app.command("redis-status")
def redis_status(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Redis database name."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Redis status."""
    client = get_client(ctx)
    response = client.request("POST", "/databases/redis/status", body={"name": name})
    normalized = client.normalize_response_payload(response)
    _print_data(normalized, raw)


@app.command("redis-conf")
def redis_conf(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Redis database name."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Redis configuration."""
    client = get_client(ctx)
    response = client.request("POST", "/databases/redis/conf", body={"name": name})
    normalized = client.normalize_response_payload(response)
    _print_data(normalized, raw)


@app.command("redis-commands")
def redis_commands(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List saved Redis commands."""
    client = get_client(ctx)
    response = client.request("GET", "/hosts/command/redis")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    rows = _extract_rows(normalized.get("data"))
    items = [_redis_command_summary(row) for row in rows]
    print_json({"count": len(items), "items": items})
