from __future__ import annotations

from typing import Any, Dict, List

from panel_client import PanelClient


def search_hosts(client: PanelClient, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
    body = {
        "page": page,
        "pageSize": page_size,
    }
    response = client.request("POST", "/hosts/search", body=body)
    payload = response["body"].get("json", {})
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    rows = data.get("items", []) if isinstance(data, dict) else []
    hosts: List[Dict[str, Any]] = []
    for row in rows:
        hosts.append(
            {
                "id": row.get("id"),
                "name": row.get("name"),
                "addr": row.get("addr"),
                "user": row.get("user"),
                "groupBelong": row.get("groupBelong"),
                "port": row.get("port"),
                "createdAt": row.get("createdAt"),
            }
        )
    return {
        "count": len(hosts),
        "total": data.get("total") if isinstance(data, dict) else None,
        "page": page,
        "pageSize": page_size,
        "items": hosts,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def host_tree(client: PanelClient, info: str | None = None) -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    if info:
        body["info"] = info
    response = client.request("POST", "/hosts/tree", body=body)
    payload = response["body"].get("json", {})
    data = payload.get("data", []) if isinstance(payload, dict) else []
    tree = data if isinstance(data, list) else []
    return {
        "tree": tree,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }
