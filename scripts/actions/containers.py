from __future__ import annotations

from typing import Any, Dict, List

from panel_client import PanelClient


def list_containers(client: PanelClient) -> Dict[str, Any]:
    response = client.request("POST", "/containers/list", body={})
    payload = response["body"].get("json", {})
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    items: List[Dict[str, Any]] = []
    for name in rows:
        items.append({"name": name})
    return {
        "count": len(items),
        "items": items,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }
