from __future__ import annotations

from typing import Any, Dict, List

from panel_client import PanelClient


def list_host_commands(client: PanelClient) -> Dict[str, Any]:
    response = client.request("GET", "/hosts/command")
    payload = response["body"].get("json", {})
    data = payload.get("data")
    rows = data if isinstance(data, list) else []
    items: List[Dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        items.append(
            {
                "id": row.get("id"),
                "name": row.get("name"),
                "groupBelong": row.get("groupBelong"),
                "groupID": row.get("groupID"),
                "command": row.get("command"),
            }
        )
    return {
        "count": len(items),
        "items": items,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def command_tree(client: PanelClient) -> Dict[str, Any]:
    response = client.request("GET", "/hosts/command/tree")
    payload = response["body"].get("json", {})
    data = payload.get("data")
    tree = data if isinstance(data, list) else []
    return {
        "tree": tree,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }
