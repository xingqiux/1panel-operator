from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Dashboard metrics.")

_SUMMARY_KEYS = [
    "shotTime", "uptime", "load1", "load5", "load15",
    "memoryTotal", "memoryAvailable", "memoryUsedPercent",
    "cpuUsedPercent", "netBytesSent", "netBytesRecv",
]


@app.callback(invoke_without_command=True)
def current(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show current dashboard metrics."""
    client = get_client(ctx)
    response = client.request("POST", "/dashboard/current", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    summary = {k: data.get(k) for k in _SUMMARY_KEYS}
    print_json(summary)
