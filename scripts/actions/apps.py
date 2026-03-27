from __future__ import annotations

from typing import Any, Dict, List

from panel_client import PanelClient


def list_apps(client: PanelClient) -> Dict[str, Any]:
    response = client.request("GET", "/apps/installed/list")
    payload = response["body"].get("json", {})
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    items: List[Dict[str, Any]] = []
    for row in rows:
        items.append(
            {
                "id": row.get("id"),
                "key": row.get("key"),
                "name": row.get("name"),
            }
        )
    return {
        "count": len(items),
        "items": items,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }
