from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Hosts and host commands.")


@app.command("list")
def list_hosts(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(100, help="Items per page."),
) -> None:
    """Search hosts with pagination."""
    client = get_client(ctx)
    body = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/hosts/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = data.get("items", []) if isinstance(data, dict) else []
    items = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        items.append({
            "id": row.get("id"),
            "name": row.get("name"),
            "addr": row.get("addr"),
            "user": row.get("user"),
            "port": row.get("port"),
            "groupBelong": row.get("groupBelong"),
            "createdAt": row.get("createdAt"),
        })
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("tree")
def host_tree(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show host tree structure."""
    client = get_client(ctx)
    response = client.request("POST", "/hosts/tree", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    tree = normalized.get("data", [])
    if not isinstance(tree, list):
        tree = []
    print_json(tree)


@app.command("commands")
def list_commands(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List saved host commands."""
    client = get_client(ctx)
    response = client.request("GET", "/hosts/command")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    rows = normalized.get("data", [])
    if not isinstance(rows, list):
        rows = []
    items = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        items.append({
            "id": row.get("id"),
            "name": row.get("name"),
            "command": row.get("command"),
            "groupBelong": row.get("groupBelong"),
        })
    print_json({"count": len(items), "items": items})
