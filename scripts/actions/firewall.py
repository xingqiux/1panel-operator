from __future__ import annotations

from typing import Any, Dict

from panel_client import PanelClient


def firewall_base_info(client: PanelClient) -> Dict[str, Any]:
    response = client.request("GET", "/hosts/firewall/base")
    payload = response["body"].get("json", {})
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    summary = {
        "name": data.get("name"),
        "status": data.get("status"),
        "pingStatus": data.get("pingStatus"),
        "version": data.get("version"),
    }
    return {
        "summary": summary,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }
