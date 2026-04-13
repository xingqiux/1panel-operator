from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Docker daemon status and configuration.")


@app.command("status")
def docker_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Docker daemon status."""
    client = get_client(ctx)
    response = client.request("GET", "/containers/docker/status")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))


@app.command("config")
def docker_config(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Docker daemon config (daemon.json)."""
    client = get_client(ctx)
    response = client.request("GET", "/containers/daemonjson")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}

    print_json({
        "registryMirrors": data.get("registryMirrors"),
        "liveRestore": data.get("liveRestore"),
        "iptables": data.get("iptables"),
        "cgroupDriver": data.get("cgroupDriver"),
        "logMaxSize": data.get("logMaxSize"),
        "logMaxFile": data.get("logMaxFile"),
    })
