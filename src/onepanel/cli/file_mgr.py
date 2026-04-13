from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="File management commands.")


def _extract_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        rows = data.get("items")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def _file_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": row.get("name"),
        "isDir": row.get("isDir"),
        "size": row.get("size"),
        "mode": row.get("mode"),
        "user": row.get("user"),
        "group": row.get("group"),
        "modTime": row.get("modTime"),
    }


@app.command("list")
def list_files(
    ctx: typer.Context,
    path: str = typer.Argument("/opt", help="Directory path to list."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List files in a directory."""
    client = get_client(ctx)
    body: dict[str, Any] = {
        "path": path,
        "expand": True,
        "page": page,
        "pageSize": page_size,
    }
    response = client.request("POST", "/files/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = _extract_rows(data)
    items = [_file_summary(row) for row in rows]
    print_json({"path": path, "count": len(items), "items": items})


@app.command("tree")
def tree_files(
    ctx: typer.Context,
    path: str = typer.Argument("/opt", help="Directory path to show as a tree."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show a directory tree."""
    client = get_client(ctx)
    response = client.request("POST", "/files/tree", body={"path": path})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", [])
    if not isinstance(data, (list, dict)):
        data = []
    print_json(data)
