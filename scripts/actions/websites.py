from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

from panel_client import PanelClient


def _website_summary(row: Dict[str, Any]) -> Dict[str, Any]:
    domains = row.get("domains") or []
    ssl_info = row.get("webSiteSSL") or {}
    return {
        "id": row.get("id"),
        "primaryDomain": row.get("primaryDomain"),
        "alias": row.get("alias"),
        "status": row.get("status"),
        "type": row.get("type"),
        "protocol": row.get("protocol"),
        "httpConfig": row.get("httpConfig"),
        "proxy": row.get("proxy"),
        "proxyType": row.get("proxyType"),
        "group": row.get("group"),
        "webSiteGroupId": row.get("webSiteGroupId"),
        "domainCount": len(domains),
        "ipv6": row.get("IPV6"),
        "accessLog": row.get("accessLog"),
        "errorLog": row.get("errorLog"),
        "defaultServer": row.get("defaultServer"),
        "createdAt": row.get("createdAt"),
        "updatedAt": row.get("updatedAt"),
        "sslExpireDate": ssl_info.get("expireDate"),
        "sslStatus": ssl_info.get("status"),
        "sslProvider": ssl_info.get("provider"),
        "sslAutoRenew": ssl_info.get("autoRenew"),
    }


def list_websites(client: PanelClient) -> Dict[str, Any]:
    response = client.request("GET", "/websites/list")
    payload = response["body"].get("json", {})
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    items: List[Dict[str, Any]] = []
    for row in rows:
        items.append(_website_summary(row))
    return {
        "count": len(items),
        "items": items,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def get_website(client: PanelClient, website_id: int) -> Dict[str, Any]:
    response = client.request("GET", f"/websites/{website_id}")
    payload = response["body"].get("json", {})
    row = payload.get("data", {}) if isinstance(payload, dict) else {}
    return {
        "item": _website_summary(row) if isinstance(row, dict) else {},
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def find_website_summary(client: PanelClient, domain: str) -> Dict[str, Any]:
    listing = list_websites(client)
    for item in listing["items"]:
        if item.get("primaryDomain") == domain or item.get("alias") == domain:
            return {
                "item": item,
                "status_code": listing["status_code"],
                "url": listing["url"],
                "raw": listing["raw"],
            }
    raise ValueError(f"Website not found for domain: {domain}")


def get_website_https_summary(client: PanelClient, website_id: int) -> Dict[str, Any]:
    response = client.request("GET", f"/websites/{website_id}/https")
    payload = response["body"].get("json", {})
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    ssl_info = data.get("SSL") or {}
    dns_account = ssl_info.get("dnsAccount") or {}
    summary = {
        "enable": data.get("enable"),
        "hsts": data.get("hsts"),
        "httpConfig": data.get("httpConfig"),
        "sslProtocols": data.get("SSLProtocol"),
        "sslExpireDate": ssl_info.get("expireDate"),
        "sslStatus": ssl_info.get("status"),
        "sslProvider": ssl_info.get("provider"),
        "sslAutoRenew": ssl_info.get("autoRenew"),
        "sslOrganization": ssl_info.get("organization"),
        "dnsProvider": dns_account.get("type"),
        "dnsAccountName": dns_account.get("name"),
    }
    return {
        "summary": summary,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def get_website_proxies_summary(client: PanelClient, website_id: int) -> Dict[str, Any]:
    response = client.request("POST", "/websites/proxies", body={"id": website_id})
    payload = response["body"].get("json", {})
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    proxies: List[Dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        proxies.append(
            {
                "id": row.get("id"),
                "name": row.get("name"),
                "match": row.get("match"),
                "modifier": row.get("modifier"),
                "enable": row.get("enable"),
                "proxyPass": row.get("proxyPass"),
                "proxyHost": row.get("proxyHost"),
                "cache": row.get("cache"),
                "cacheTime": row.get("cacheTime"),
                "cacheUnit": row.get("cacheUnit"),
                "sni": row.get("sni"),
                "filePath": row.get("filePath"),
            }
        )
    return {
        "items": proxies,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def resolve_website_id(client: PanelClient, website_id: int | None = None, domain: str | None = None) -> int:
    if website_id is not None:
        return website_id
    if not domain:
        raise ValueError("Provide website_id or domain.")
    matched = find_website_summary(client, domain)
    return int(matched["item"]["id"])


def website_inspect(
    client: PanelClient,
    website_id: int | None = None,
    domain: str | None = None,
    include_https: bool = True,
    include_proxies: bool = True,
) -> Dict[str, Any]:
    if website_id is not None:
        resolved_id = website_id
    elif domain:
        matched = find_website_summary(client, domain)
        resolved_id = int(matched["item"]["id"])
    else:
        raise ValueError("Provide website_id or domain.")

    jobs: List[tuple[str, int]] = [("base", resolved_id)]
    if include_https:
        jobs.append(("https", resolved_id))
    if include_proxies:
        jobs.append(("proxies", resolved_id))

    loaders = {
        "base": get_website,
        "https": get_website_https_summary,
        "proxies": get_website_proxies_summary,
    }
    results: Dict[str, Dict[str, Any]] = {}
    max_workers = max(1, min(len(jobs), 3))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(loaders[kind], client, current_id): kind for kind, current_id in jobs}
        for future in as_completed(future_map):
            kind = future_map[future]
            results[kind] = future.result()

    base = results["base"]
    item = dict(base["item"])
    if include_https:
        item["https"] = results["https"]["summary"]
    if include_proxies:
        item["proxies"] = results["proxies"]["items"]
    return {
        "item": item,
        "status_code": base["status_code"],
        "url": base["url"],
        "raw": base["raw"],
    }


def website_overview(
    client: PanelClient,
    include_https: bool = True,
    include_proxies: bool = True,
    workers: int = 4,
) -> Dict[str, Any]:
    listing = list_websites(client)
    items = [dict(item) for item in listing["items"]]

    def enrich(kind: str, website_id: int) -> tuple[str, int, Any]:
        if kind == "https":
            return kind, website_id, get_website_https_summary(client, website_id)["summary"]
        return kind, website_id, get_website_proxies_summary(client, website_id)["items"]

    jobs: List[tuple[str, int]] = []
    for item in items:
        website_id = int(item["id"])
        if include_https:
            jobs.append(("https", website_id))
        if include_proxies:
            jobs.append(("proxies", website_id))

    if jobs:
        max_workers = max(1, min(workers, len(jobs)))
        item_by_id = {int(item["id"]): item for item in items}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {executor.submit(enrich, kind, website_id): (kind, website_id) for kind, website_id in jobs}
            for future in as_completed(future_map):
                kind, website_id = future_map[future]
                target = item_by_id[website_id]
                try:
                    _, _, value = future.result()
                    target[kind] = value
                except Exception as exc:  # pragma: no cover - best effort summary
                    target[f"{kind}Error"] = str(exc)

    return {
        "count": len(items),
        "items": items,
        "status_code": listing["status_code"],
        "url": listing["url"],
        "raw": listing["raw"],
    }
