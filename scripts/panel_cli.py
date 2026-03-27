from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from actions.apps import list_apps
from actions.containers import list_containers
from actions.dashboard import current_dashboard
from actions.firewall import firewall_base_info
from actions.host_commands import command_tree, list_host_commands
from actions.hosts import host_tree, search_hosts
from actions.websites import list_websites, website_inspect, website_overview
from panel_client import PanelAPIError, PanelClient, SAFE_METHODS
from panel_config import PanelConfigError, load_config


def parse_key_values(items: list[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE format, got: {item}")
        key, value = item.split("=", 1)
        result[key] = value
    return result


def load_body(args: argparse.Namespace) -> Any | None:
    if args.body and args.body_file:
        raise ValueError("Use either --body or --body-file, not both.")
    if args.body:
        return json.loads(args.body)
    if args.body_file:
        return json.loads(Path(args.body_file).read_text(encoding="utf-8"))
    return None


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_config(client: PanelClient, args: argparse.Namespace) -> int:
    if args.config_command == "show":
        payload = {
            "base_url": client.config.base_url,
            "api_key": client.config.api_key if args.reveal_key else client.config.masked_api_key,
            "timeout": client.config.timeout,
            "verify_tls": client.config.verify_tls,
            "swagger_cache_ttl_seconds": client.config.swagger_cache_ttl_seconds,
            "source": client.config.source,
        }
        print_json(payload)
        return 0
    if args.config_command == "cache":
        print_json(client.cache_info())
        return 0
    else:
        raise ValueError(f"Unsupported config subcommand: {args.config_command}")


def cmd_ping(client: PanelClient, args: argparse.Namespace) -> int:
    response = client.ping()
    print_json(
        {
            "ok": True,
            "probe": "GET /websites/list",
            "status_code": response["status_code"],
            "url": response["url"],
        }
    )
    return 0


def cmd_discover(client: PanelClient, args: argparse.Namespace) -> int:
    if args.discover_command == "swagger-url":
        print(client.swagger_url())
        return 0

    if args.discover_command == "tags":
        print_json(client.list_tags())
        return 0

    if args.discover_command == "endpoints":
        operations = client.list_operations(match=args.match, tag=args.tag)
        payload = [
            {
                "method": op.method,
                "path": op.path,
                "summary": op.summary,
                "tags": op.tags,
                "body_schema_ref": op.body_schema_ref,
                "path_params": op.path_params,
                "query_params": op.query_params,
                "response_schema_ref": op.response_schema_ref,
            }
            for op in operations[: args.limit]
        ]
        print_json(payload)
        return 0

    if args.discover_command == "operation":
        operation = client.get_operation(args.path, method=args.method)
        print_json(
            {
                "method": operation.method,
                "path": operation.path,
                "summary": operation.summary,
                "tags": operation.tags,
                "body_schema_ref": operation.body_schema_ref,
                "path_params": operation.path_params,
                "query_params": operation.query_params,
                "response_schema_ref": operation.response_schema_ref,
            }
        )
        return 0

    raise ValueError(f"Unsupported discover subcommand: {args.discover_command}")


def cmd_schema(client: PanelClient, args: argparse.Namespace) -> int:
    if args.schema_command == "list":
        print_json(client.list_schema_names(match=args.match)[: args.limit])
        return 0
    if args.schema_command == "show":
        print_json(client.get_schema(args.name))
        return 0
    if args.schema_command == "template":
        print_json(client.build_schema_template(args.name, max_depth=args.max_depth))
        return 0
    raise ValueError(f"Unsupported schema subcommand: {args.schema_command}")


def cmd_template(client: PanelClient, args: argparse.Namespace) -> int:
    print_json(client.build_operation_template(args.path, args.method))
    return 0


def cmd_call(client: PanelClient, args: argparse.Namespace) -> int:
    method = args.method.upper()
    body = load_body(args)
    query = parse_key_values(args.query or [])
    headers = parse_key_values(args.header or [])
    plan = client.plan(method, args.path, body=body, query=query)
    if args.assume_read:
        plan["write_operation"] = False

    if args.dry_run or (method not in SAFE_METHODS and not args.confirm and not args.assume_read):
        print_json(plan)
        return 0 if args.dry_run else 2

    response = client.request(method, args.path, body=body, query=query, extra_headers=headers)
    if args.raw_response:
        print_json(
            {
                "status_code": response["status_code"],
                "url": response["url"],
                "body": response["body"].get("json", response["body"].get("text")),
            }
        )
        return 0

    normalized = client.normalize_response_payload(response)
    if args.data_only:
        print_json(normalized.get("data"))
        return 0
    print_json(normalized)
    return 0


def cmd_resource(client: PanelClient, args: argparse.Namespace) -> int:
    if args.command == "dashboard" and args.resource_command == "current":
        result = current_dashboard(client)
        if args.raw:
            print_json(result["raw"])
            return 0
        print_json(
            {
                "summary": result["summary"],
                "status_code": result["status_code"],
                "url": result["url"],
            }
        )
        return 0
    if args.command == "websites" and args.resource_command == "list":
        result = list_websites(client)
    elif args.command == "websites" and args.resource_command == "overview":
        result = website_overview(
            client,
            include_https=not args.no_https,
            include_proxies=not args.no_proxies,
            workers=args.workers,
        )
    elif args.command == "websites" and args.resource_command == "inspect":
        result = website_inspect(
            client,
            website_id=args.id,
            domain=args.domain,
            include_https=not args.no_https,
            include_proxies=not args.no_proxies,
        )
    elif args.command == "apps" and args.resource_command == "list":
        result = list_apps(client)
    elif args.command == "containers" and args.resource_command == "list":
        result = list_containers(client)
    elif args.command == "hosts" and args.resource_command == "list":
        result = search_hosts(client, page=args.page, page_size=args.page_size)
    elif args.command == "hosts" and args.resource_command == "tree":
        result = host_tree(client, info=args.info)
        if args.raw:
            print_json(result["raw"])
            return 0
        print_json({"tree": result["tree"], "status_code": result["status_code"], "url": result["url"]})
        return 0
    elif args.command == "host-commands" and args.resource_command == "list":
        result = list_host_commands(client)
    elif args.command == "host-commands" and args.resource_command == "tree":
        result = command_tree(client)
        if args.raw:
            print_json(result["raw"])
            return 0
        print_json({"tree": result["tree"], "status_code": result["status_code"], "url": result["url"]})
        return 0
    elif args.command == "firewall" and args.resource_command == "base":
        result = firewall_base_info(client)
        if args.raw:
            print_json(result["raw"])
            return 0
        print_json({"summary": result["summary"], "status_code": result["status_code"], "url": result["url"]})
        return 0
    elif args.command == "task" and args.resource_command == "website-overview":
        result = website_overview(
            client,
            include_https=not args.no_https,
            include_proxies=not args.no_proxies,
            workers=args.workers,
        )
    elif args.command == "task" and args.resource_command == "website-inspect":
        result = website_inspect(
            client,
            website_id=args.id,
            domain=args.domain,
            include_https=not args.no_https,
            include_proxies=not args.no_proxies,
        )
    else:
        raise ValueError(f"Unsupported resource command: {args.command} {args.resource_command}")

    if args.raw:
        print_json(result["raw"])
        return 0

    if "item" in result:
        print_json(
            {
                "item": result["item"],
                "status_code": result["status_code"],
                "url": result["url"],
            }
        )
        return 0

    print_json(
        {
            "count": result["count"],
            "items": result["items"],
            "status_code": result["status_code"],
            "url": result["url"],
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate a 1Panel instance through its API.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    config_parser = subparsers.add_parser("config", help="Show resolved configuration.")
    config_sub = config_parser.add_subparsers(dest="config_command", required=True)
    config_show = config_sub.add_parser("show", help="Show the current configuration.")
    config_show.add_argument("--reveal-key", action="store_true", help="Print the full API key.")
    config_sub.add_parser("cache", help="Show Swagger cache status.")

    subparsers.add_parser("ping", help="Check connectivity using a safe API probe.")

    discover_parser = subparsers.add_parser("discover", help="Inspect Swagger-defined operations.")
    discover_sub = discover_parser.add_subparsers(dest="discover_command", required=True)
    discover_sub.add_parser("swagger-url", help="Print the resolved Swagger JSON URL.")
    discover_sub.add_parser("tags", help="List Swagger tags with operation counts.")
    endpoints_parser = discover_sub.add_parser("endpoints", help="List API endpoints from Swagger.")
    endpoints_parser.add_argument("--match", help="Filter by path, summary, or tag keyword.")
    endpoints_parser.add_argument("--tag", help="Filter by Swagger tag.")
    endpoints_parser.add_argument("--limit", type=int, default=100, help="Maximum number of endpoints to print.")
    operation_parser = discover_sub.add_parser("operation", help="Show one Swagger operation in detail.")
    operation_parser.add_argument("path", help="Exact API path, for example /websites/update.")
    operation_parser.add_argument("--method", help="HTTP method when a path has multiple operations.")

    schema_parser = subparsers.add_parser("schema", help="Inspect Swagger definitions.")
    schema_sub = schema_parser.add_subparsers(dest="schema_command", required=True)
    schema_list = schema_sub.add_parser("list", help="List schema definition names.")
    schema_list.add_argument("--match", help="Filter schema names by keyword.")
    schema_list.add_argument("--limit", type=int, default=100, help="Maximum number of schemas to print.")
    schema_show = schema_sub.add_parser("show", help="Print one schema definition.")
    schema_show.add_argument("name", help="Definition name or #/definitions/ref.")
    schema_template = schema_sub.add_parser("template", help="Generate a JSON template from one schema.")
    schema_template.add_argument("name", help="Definition name or #/definitions/ref.")
    schema_template.add_argument("--max-depth", type=int, default=4, help="Maximum schema recursion depth.")

    template_parser = subparsers.add_parser("template", help="Generate a request template from one Swagger operation.")
    template_parser.add_argument("method", help="HTTP method.")
    template_parser.add_argument("path", help="Exact API path.")

    call_parser = subparsers.add_parser("call", help="Execute a raw API request.")
    call_parser.add_argument("method", help="HTTP method, for example GET or POST.")
    call_parser.add_argument("path", help="API path like /websites/list or a full URL.")
    call_parser.add_argument("--query", action="append", help="Query string KEY=VALUE.")
    call_parser.add_argument("--header", action="append", help="Extra header KEY=VALUE.")
    call_parser.add_argument("--body", help="Inline JSON request body.")
    call_parser.add_argument("--body-file", help="Path to a JSON file for the request body.")
    call_parser.add_argument("--confirm", action="store_true", help="Allow write operations to execute.")
    call_parser.add_argument(
        "--assume-read",
        action="store_true",
        help="Allow non-GET requests that have been verified as read-only in Swagger.",
    )
    call_parser.add_argument("--data-only", action="store_true", help="Print only the normalized data field.")
    call_parser.add_argument("--raw-response", action="store_true", help="Print the unnormalized legacy response shape.")
    call_parser.add_argument("--dry-run", action="store_true", help="Print the planned request without executing it.")

    websites_parser = subparsers.add_parser("websites", help="Website-focused convenience commands.")
    websites_sub = websites_parser.add_subparsers(dest="resource_command", required=True)
    websites_list = websites_sub.add_parser("list", help="List websites with a safe summary.")
    websites_list.add_argument("--raw", action="store_true", help="Print the raw API payload.")
    websites_overview = websites_sub.add_parser("overview", help="Load the current website configuration overview.")
    websites_overview.add_argument("--no-https", action="store_true", help="Skip HTTPS config lookups.")
    websites_overview.add_argument("--no-proxies", action="store_true", help="Skip proxy rule lookups.")
    websites_overview.add_argument("--workers", type=int, default=4, help="Parallel worker count for detail lookups.")
    websites_overview.add_argument("--raw", action="store_true", help="Print only the raw website list payload.")
    websites_inspect = websites_sub.add_parser("inspect", help="Inspect one website with safe detail summaries.")
    websites_inspect.add_argument("--id", type=int, help="Website ID.")
    websites_inspect.add_argument("--domain", help="Primary domain or alias.")
    websites_inspect.add_argument("--no-https", action="store_true", help="Skip HTTPS config lookups.")
    websites_inspect.add_argument("--no-proxies", action="store_true", help="Skip proxy rule lookups.")
    websites_inspect.add_argument("--raw", action="store_true", help="Print the raw website detail payload.")

    dashboard_parser = subparsers.add_parser("dashboard", help="Dashboard-focused convenience commands.")
    dashboard_sub = dashboard_parser.add_subparsers(dest="resource_command", required=True)
    dashboard_current = dashboard_sub.add_parser("current", help="Load current dashboard metrics.")
    dashboard_current.add_argument("--raw", action="store_true", help="Print the raw API payload.")

    apps_parser = subparsers.add_parser("apps", help="App-focused convenience commands.")
    apps_sub = apps_parser.add_subparsers(dest="resource_command", required=True)
    apps_list = apps_sub.add_parser("list", help="List installed apps.")
    apps_list.add_argument("--raw", action="store_true", help="Print the raw API payload.")

    containers_parser = subparsers.add_parser("containers", help="Container-focused convenience commands.")
    containers_sub = containers_parser.add_subparsers(dest="resource_command", required=True)
    containers_list = containers_sub.add_parser("list", help="List container names.")
    containers_list.add_argument("--raw", action="store_true", help="Print the raw API payload.")

    hosts_parser = subparsers.add_parser("hosts", help="Host-focused convenience commands.")
    hosts_sub = hosts_parser.add_subparsers(dest="resource_command", required=True)
    hosts_list = hosts_sub.add_parser("list", help="List managed hosts.")
    hosts_list.add_argument("--page", type=int, default=1, help="Page number.")
    hosts_list.add_argument("--page-size", type=int, default=100, help="Page size.")
    hosts_list.add_argument("--raw", action="store_true", help="Print the raw API payload.")
    hosts_tree_cmd = hosts_sub.add_parser("tree", help="Load the host tree.")
    hosts_tree_cmd.add_argument("--info", help="Optional filter info.")
    hosts_tree_cmd.add_argument("--raw", action="store_true", help="Print the raw API payload.")

    host_commands_parser = subparsers.add_parser("host-commands", help="Saved host command helpers.")
    host_commands_sub = host_commands_parser.add_subparsers(dest="resource_command", required=True)
    host_commands_list = host_commands_sub.add_parser("list", help="List saved host commands.")
    host_commands_list.add_argument("--raw", action="store_true", help="Print the raw API payload.")
    host_commands_tree = host_commands_sub.add_parser("tree", help="Load the host command tree.")
    host_commands_tree.add_argument("--raw", action="store_true", help="Print the raw API payload.")

    firewall_parser = subparsers.add_parser("firewall", help="Firewall-focused convenience commands.")
    firewall_sub = firewall_parser.add_subparsers(dest="resource_command", required=True)
    firewall_base = firewall_sub.add_parser("base", help="Load firewall base info.")
    firewall_base.add_argument("--raw", action="store_true", help="Print the raw API payload.")

    task_parser = subparsers.add_parser("task", help="Task-oriented entrypoints for common user requests.")
    task_sub = task_parser.add_subparsers(dest="resource_command", required=True)
    task_website_overview = task_sub.add_parser("website-overview", help="Answer '当前网站配置是怎样的' in one command.")
    task_website_overview.add_argument("--no-https", action="store_true", help="Skip HTTPS config lookups.")
    task_website_overview.add_argument("--no-proxies", action="store_true", help="Skip proxy rule lookups.")
    task_website_overview.add_argument("--workers", type=int, default=4, help="Parallel worker count for detail lookups.")
    task_website_overview.add_argument("--raw", action="store_true", help="Print the raw website list payload.")
    task_website_inspect = task_sub.add_parser("website-inspect", help="Inspect one website in one task command.")
    task_website_inspect.add_argument("--id", type=int, help="Website ID.")
    task_website_inspect.add_argument("--domain", help="Primary domain or alias.")
    task_website_inspect.add_argument("--no-https", action="store_true", help="Skip HTTPS config lookups.")
    task_website_inspect.add_argument("--no-proxies", action="store_true", help="Skip proxy rule lookups.")
    task_website_inspect.add_argument("--raw", action="store_true", help="Print the raw website detail payload.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config()
        client = PanelClient(config)

        if args.command == "config":
            return cmd_config(client, args)
        if args.command == "ping":
            return cmd_ping(client, args)
        if args.command == "discover":
            return cmd_discover(client, args)
        if args.command == "schema":
            return cmd_schema(client, args)
        if args.command == "template":
            return cmd_template(client, args)
        if args.command == "call":
            return cmd_call(client, args)
        if args.command in {"dashboard", "websites", "apps", "containers", "hosts", "host-commands", "firewall", "task"}:
            return cmd_resource(client, args)

        raise ValueError(f"Unsupported command: {args.command}")
    except (PanelConfigError, PanelAPIError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        if isinstance(exc, PanelAPIError) and exc.payload is not None:
            print_json({"error_payload": exc.payload})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
