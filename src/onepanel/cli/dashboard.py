from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Dashboard metrics and system overview.")


@app.callback(invoke_without_command=True)
def default(
    ctx: typer.Context,
) -> None:
    """Show combined OS info and live metrics."""
    if ctx.invoked_subcommand is not None:
        return

    client = get_client(ctx)
    os_resp = client.request("GET", "/dashboard/base/os")
    os_norm = client.normalize_response_payload(os_resp)
    os_data = os_norm.get("data", {})
    if not isinstance(os_data, dict):
        os_data = {}

    metrics_resp = client.request("GET", "/dashboard/base/all/all")
    metrics_norm = client.normalize_response_payload(metrics_resp)
    metrics_data = metrics_norm.get("data", {})
    if not isinstance(metrics_data, dict):
        metrics_data = {}

    print_json({
        "os": {
            "platform": os_data.get("platform"),
            "platformFamily": os_data.get("platformFamily"),
            "kernelArch": os_data.get("kernelArch"),
            "kernelVersion": os_data.get("kernelVersion"),
            "hostname": os_data.get("hostname"),
        },
        "metrics": {
            "uptime": metrics_data.get("uptime"),
            "load1": metrics_data.get("load1"),
            "load5": metrics_data.get("load5"),
            "load15": metrics_data.get("load15"),
            "cpuUsedPercent": metrics_data.get("cpuUsedPercent"),
            "cpuCores": metrics_data.get("cpuCores"),
            "memoryTotal": metrics_data.get("memoryTotal"),
            "memoryAvailable": metrics_data.get("memoryAvailable"),
            "memoryUsedPercent": metrics_data.get("memoryUsedPercent"),
            "ioReadBytes": metrics_data.get("ioReadBytes"),
            "ioWriteBytes": metrics_data.get("ioWriteBytes"),
            "netBytesSent": metrics_data.get("netBytesSent"),
            "netBytesRecv": metrics_data.get("netBytesRecv"),
            "shotTime": metrics_data.get("shotTime"),
        },
    })


@app.command("os")
def os_info(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show OS information."""
    client = get_client(ctx)
    response = client.request("GET", "/dashboard/base/os")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "platform": data.get("platform"),
        "platformFamily": data.get("platformFamily"),
        "platformVersion": data.get("platformVersion"),
        "kernelArch": data.get("kernelArch"),
        "kernelVersion": data.get("kernelVersion"),
        "hostname": data.get("hostname"),
    })


@app.command("metrics")
def metrics(
    ctx: typer.Context,
    io: str = typer.Option("all", help="IO device filter."),
    net: str = typer.Option("all", help="Network interface filter."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show live system metrics."""
    client = get_client(ctx)
    response = client.request("GET", f"/dashboard/base/{io}/{net}")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "uptime": data.get("uptime"),
        "load1": data.get("load1"),
        "load5": data.get("load5"),
        "load15": data.get("load15"),
        "cpuUsedPercent": data.get("cpuUsedPercent"),
        "cpuCores": data.get("cpuCores"),
        "memoryTotal": data.get("memoryTotal"),
        "memoryAvailable": data.get("memoryAvailable"),
        "memoryUsedPercent": data.get("memoryUsedPercent"),
        "ioReadBytes": data.get("ioReadBytes"),
        "ioWriteBytes": data.get("ioWriteBytes"),
        "netBytesSent": data.get("netBytesSent"),
        "netBytesRecv": data.get("netBytesRecv"),
        "shotTime": data.get("shotTime"),
    })


@app.command("monitor")
def monitor(
    ctx: typer.Context,
    start_time: int = typer.Option(0, help="Start timestamp."),
    end_time: int = typer.Option(0, help="End timestamp."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Search historical monitor data."""
    client = get_client(ctx)
    body: dict[str, Any] = {}
    if start_time:
        body["startTime"] = start_time
    if end_time:
        body["endTime"] = end_time
    response = client.request("POST", "/hosts/monitor/search", body=body)
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))
