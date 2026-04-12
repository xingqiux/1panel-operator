from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Docker containers.")


def _summary(row: dict[str, Any]) -> dict[str, Any]:
    """Extract summary fields from a single container row."""
    container_id = row.get("containerID") or ""
    if not isinstance(container_id, str):
        container_id = str(container_id)
    return {
        "id": container_id[:12],
        "name": row.get("name"),
        "state": row.get("state"),
        "image": row.get("imageName"),
        "ports": row.get("ports"),
        "uptime": row.get("runTime"),
        "createdAt": row.get("createTime"),
    }


@app.command("list")
def list_containers(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List containers with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/containers/search", body=body)
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


@app.command("stats")
def stats_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show container resource usage stats."""
    client = get_client(ctx)
    response = client.request("GET", "/containers/list/stats")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "total": data.get("total"),
        "running": data.get("running"),
        "stopped": data.get("stopped"),
        "created": data.get("created"),
    })


# Sub-module registration (added as sub-modules are implemented)
from onepanel.cli import container_image  # noqa: E402
from onepanel.cli import container_compose  # noqa: E402
from onepanel.cli import container_network  # noqa: E402
from onepanel.cli import container_volume  # noqa: E402
# from onepanel.cli import container_docker  # noqa: E402
app.add_typer(container_image.app, name="image")
app.add_typer(container_compose.app, name="compose")
app.add_typer(container_network.app, name="network")
app.add_typer(container_volume.app, name="volume")
# app.add_typer(container_docker.app, name="docker")
