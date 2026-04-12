from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Firewall rules and status.")


def _rule_summary(row: dict[str, Any]) -> dict[str, Any]:
    """Extract summary fields from a single firewall rule row."""
    return {
        "id": row.get("id"),
        "strategy": row.get("strategy"),
        "port": row.get("port"),
        "protocol": row.get("protocol"),
        "address": row.get("address"),
        "description": row.get("description"),
    }


@app.command("status")
def firewall_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show firewall base status."""
    client = get_client(ctx)
    response = client.request("GET", "/hosts/firewall/base")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    summary = {
        "name": data.get("name"),
        "status": data.get("status"),
        "pingStatus": data.get("pingStatus"),
        "version": data.get("version"),
    }
    print_json(summary)


@app.command("rules")
def rules_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List firewall rules."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/hosts/firewall/search", body=body)
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
    items = [_rule_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("fail2ban")
def fail2ban_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Fail2ban status."""
    client = get_client(ctx)
    response = client.request("GET", "/toolbox/fail2ban/base")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "isEnable": data.get("isEnable"),
        "isActive": data.get("isActive"),
        "isExist": data.get("isExist"),
        "version": data.get("version"),
        "maxRetry": data.get("maxRetry"),
        "banTime": data.get("banTime"),
        "findTime": data.get("findTime"),
    })


@app.command("fail2ban-ips")
def fail2ban_ips(
    ctx: typer.Context,
    status: str = typer.Option("banned", "--status", help="Filter: banned, ignore."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List Fail2ban banned/ignored IPs."""
    client = get_client(ctx)
    body: dict[str, Any] = {"status": status, "page": page, "pageSize": page_size}
    response = client.request("POST", "/toolbox/fail2ban/search", body=body)
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))
