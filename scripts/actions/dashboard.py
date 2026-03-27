from __future__ import annotations

from typing import Any, Dict

from panel_client import PanelClient


def current_dashboard(client: PanelClient) -> Dict[str, Any]:
    response = client.request("POST", "/dashboard/current", body={})
    payload = response["body"].get("json", {})
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    summary = {
        "shotTime": data.get("shotTime"),
        "uptime": data.get("uptime"),
        "load1": data.get("load1"),
        "load5": data.get("load5"),
        "load15": data.get("load15"),
        "memoryTotal": data.get("memoryTotal"),
        "memoryAvailable": data.get("memoryAvailable"),
        "memoryUsedPercent": data.get("memoryUsedPercent"),
        "cpuUsedPercent": data.get("cpuUsedPercent"),
        "netBytesSent": data.get("netBytesSent"),
        "netBytesRecv": data.get("netBytesRecv"),
    }
    return {
        "summary": summary,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }
