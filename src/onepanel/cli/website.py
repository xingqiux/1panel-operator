from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import typer

from onepanel.cli import get_client, print_json
from onepanel.client import PanelClient

app = typer.Typer(help="Website-focused convenience commands.")


def _website_summary(row: dict[str, Any]) -> dict[str, Any]:
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


def _get_website(client: PanelClient, website_id: int) -> dict[str, Any]:
    response = client.request("GET", f"/websites/{website_id}")
    payload = response["body"].get("json", {})
    row = payload.get("data", {}) if isinstance(payload, dict) else {}
    return {
        "item": _website_summary(row) if isinstance(row, dict) else {},
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


def _find_website_by_domain(client: PanelClient, domain: str) -> dict[str, Any]:
    listing = _list_websites_raw(client)
    for item in listing["items"]:
        if item.get("primaryDomain") == domain or item.get("alias") == domain:
            return {
                "item": item,
                "status_code": listing["status_code"],
                "url": listing["url"],
                "raw": listing["raw"],
            }
    raise ValueError(f"Website not found for domain: {domain}")


def _get_https_summary(client: PanelClient, website_id: int) -> dict[str, Any]:
    response = client.request("GET", f"/websites/{website_id}/https")
    payload = response["body"].get("json", {})
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    ssl_info = data.get("SSL") or {}
    dns_account = ssl_info.get("dnsAccount") or {}
    return {
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


def _get_proxies_summary(client: PanelClient, website_id: int) -> list[dict[str, Any]]:
    response = client.request("POST", "/websites/proxies", body={"id": website_id})
    payload = response["body"].get("json", {})
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    proxies: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        proxies.append({
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
        })
    return proxies


def _resolve_website_id(client: PanelClient, website_id: int | None, domain: str | None) -> int:
    if website_id is not None:
        return website_id
    if not domain:
        raise ValueError("Provide --id or --domain.")
    matched = _find_website_by_domain(client, domain)
    return int(matched["item"]["id"])


def _list_websites_raw(client: PanelClient) -> dict[str, Any]:
    response = client.request("GET", "/websites/list")
    payload = response["body"].get("json", {})
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    items = [_website_summary(row) for row in rows]
    return {
        "count": len(items),
        "items": items,
        "status_code": response["status_code"],
        "url": response["url"],
        "raw": payload,
    }


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print the raw API payload."),
) -> None:
    """List websites with a safe summary."""
    client = get_client(ctx)
    result = _list_websites_raw(client)
    if raw:
        print_json(result["raw"])
        return
    print_json({
        "count": result["count"],
        "items": result["items"],
        "status_code": result["status_code"],
        "url": result["url"],
    })


@app.command("overview")
def overview(
    ctx: typer.Context,
    no_https: bool = typer.Option(False, "--no-https", help="Skip HTTPS config lookups."),
    no_proxies: bool = typer.Option(False, "--no-proxies", help="Skip proxy rule lookups."),
    workers: int = typer.Option(4, "--workers", help="Parallel worker count for detail lookups."),
    raw: bool = typer.Option(False, "--raw", help="Print only the raw website list payload."),
) -> None:
    """Load the current website configuration overview."""
    client = get_client(ctx)
    include_https = not no_https
    include_proxies = not no_proxies

    listing = _list_websites_raw(client)
    if raw:
        print_json(listing["raw"])
        return

    items = [dict(item) for item in listing["items"]]

    def enrich(kind: str, wid: int) -> tuple[str, int, Any]:
        if kind == "https":
            return kind, wid, _get_https_summary(client, wid)
        return kind, wid, _get_proxies_summary(client, wid)

    jobs: list[tuple[str, int]] = []
    for item in items:
        wid = int(item["id"])
        if include_https:
            jobs.append(("https", wid))
        if include_proxies:
            jobs.append(("proxies", wid))

    if jobs:
        max_workers = max(1, min(workers, len(jobs)))
        item_by_id = {int(item["id"]): item for item in items}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(enrich, kind, wid): (kind, wid)
                for kind, wid in jobs
            }
            for future in as_completed(future_map):
                kind, wid = future_map[future]
                target = item_by_id[wid]
                try:
                    _, _, value = future.result()
                    target[kind] = value
                except Exception as exc:
                    target[f"{kind}Error"] = str(exc)

    print_json({
        "count": len(items),
        "items": items,
        "status_code": listing["status_code"],
        "url": listing["url"],
    })


@app.command("inspect")
def inspect(
    ctx: typer.Context,
    domain: str = typer.Option(None, "--domain", help="Primary domain or alias."),
    id: int = typer.Option(None, "--id", help="Website ID."),
    no_https: bool = typer.Option(False, "--no-https", help="Skip HTTPS config lookups."),
    no_proxies: bool = typer.Option(False, "--no-proxies", help="Skip proxy rule lookups."),
    raw: bool = typer.Option(False, "--raw", help="Print the raw website detail payload."),
) -> None:
    """Inspect one website with safe detail summaries."""
    client = get_client(ctx)
    include_https = not no_https
    include_proxies = not no_proxies

    resolved_id = _resolve_website_id(client, id, domain)

    jobs: list[tuple[str, int]] = [("base", resolved_id)]
    if include_https:
        jobs.append(("https", resolved_id))
    if include_proxies:
        jobs.append(("proxies", resolved_id))

    loaders: dict[str, Any] = {
        "base": lambda c, wid: _get_website(c, wid),
        "https": lambda c, wid: {"summary": _get_https_summary(c, wid)},
        "proxies": lambda c, wid: {"items": _get_proxies_summary(c, wid)},
    }
    results: dict[str, dict[str, Any]] = {}
    max_workers = max(1, min(len(jobs), 3))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(loaders[kind], client, wid): kind
            for kind, wid in jobs
        }
        for future in as_completed(future_map):
            kind = future_map[future]
            results[kind] = future.result()

    base = results["base"]
    if raw:
        print_json(base["raw"])
        return

    item = dict(base["item"])
    if include_https:
        item["https"] = results["https"]["summary"]
    if include_proxies:
        item["proxies"] = results["proxies"]["items"]

    print_json({
        "item": item,
        "status_code": base["status_code"],
        "url": base["url"],
    })


# Sub-module registration (added as sub-modules are implemented)
from onepanel.cli import website_ssl  # noqa: E402

app.add_typer(website_ssl.app, name="ssl")
