from __future__ import annotations

from typing import Any

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
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
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
            "status": row.get("status"),
            "description": row.get("description"),
            "authMode": row.get("authMode"),
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


@app.command("ssh-status")
def ssh_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show SSH configuration."""
    client = get_client(ctx)
    response = client.request("POST", "/hosts/ssh/search", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "status": data.get("status"),
        "port": data.get("port"),
        "listenAddress": data.get("listenAddress"),
        "passwordAuthentication": data.get("passwordAuthentication"),
        "pubkeyAuthentication": data.get("pubkeyAuthentication"),
        "permitRootLogin": data.get("permitRootLogin"),
        "useDNS": data.get("useDNS"),
    })


@app.command("ssh-logs")
def ssh_logs(
    ctx: typer.Context,
    status: str = typer.Option("All", help="Filter: All, Success, Failed."),
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(100, help="Items per page."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Search SSH login logs."""
    client = get_client(ctx)
    body: dict[str, Any] = {"Status": status, "page": page, "pageSize": page_size}
    response = client.request("POST", "/hosts/ssh/log", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "successfulCount": data.get("successfulCount"),
        "failedCount": data.get("failedCount"),
        "totalCount": data.get("totalCount"),
        "logs": data.get("logs", []),
    })


@app.command("tool-status")
def tool_status(
    ctx: typer.Context,
    tool_type: str = typer.Argument(..., help="Tool name, e.g. supervisord."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Check host tool status."""
    client = get_client(ctx)
    response = client.request("POST", "/hosts/tool", body={"type": tool_type})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "type": tool_type,
        "isExist": data.get("isExist"),
        "version": data.get("version"),
        "status": data.get("status"),
        "config": data.get("config"),
    })
