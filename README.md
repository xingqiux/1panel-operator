# 1Panel Operator

`1panel-operator` is a task-first skill and CLI for inspecting and operating a 1Panel instance through its authenticated API.

It is designed for two use cases:

- as a Codex-compatible skill that helps an agent work against 1Panel safely
- as a standalone Python CLI for direct API inspection, Swagger discovery, and controlled write operations

The project avoids ad-hoc `curl` workflows, keeps instance-specific data out of the repository, and uses a task-first model for common read operations so routine diagnostics do not turn into multi-step Swagger exploration.

## Why This Exists

1Panel exposes a large API surface through Swagger/OpenAPI, but day-to-day tasks usually fall into two categories:

- common read tasks such as checking websites, containers, hosts, firewall state, or dashboard metrics
- controlled write tasks that need current-state inspection, explicit planning, and confirmation before execution

This repository provides both:

- fast, task-oriented commands for common reads
- full Swagger-backed coverage for unfamiliar reads and all writes

## Highlights

- Task-first commands for common workflows such as website overview and single-site inspection
- Domain commands for websites, dashboard, apps, containers, hosts, host commands, and firewall state
- Raw API access through a single CLI with request planning and confirmation gates
- Swagger discovery, schema lookup, request-template generation, and on-disk Swagger caching
- Open-source-safe defaults:
  - `config/local.json` is ignored
  - public example config stays generic
  - instance-specific notes belong in local-only files
- No third-party Python runtime dependencies in the core CLI

## Repository Layout

```text
.
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── config/
│   └── local.example.json
├── references/
│   ├── api-auth.md
│   ├── api-coverage.md
│   ├── api-workflows.md
│   └── generated/
└── scripts/
    ├── panel_cli.py
    ├── panel_client.py
    ├── panel_config.py
    ├── panel_auth.py
    ├── build_swagger_artifacts.py
    └── actions/
```

## Requirements

- Python 3.10 or later
- A reachable 1Panel base URL
- A valid 1Panel API key

## Configuration

The CLI reads configuration from environment variables first, then falls back to `config/local.json`.

Supported environment variables:

- `1PANEL_BASE_URL`
- `1PANEL_API_KEY`
- `1PANEL_TIMEOUT`
- `1PANEL_VERIFY_TLS`
- `1PANEL_SWAGGER_CACHE_TTL`

Create a local config file from the example:

```bash
cp config/local.example.json config/local.json
```

Example:

```json
{
  "base_url": "https://panel.example.com",
  "api_key": "replace-with-local-api-key",
  "timeout": 20,
  "verify_tls": true,
  "swagger_cache_ttl_seconds": 600
}
```

`config/local.json` is ignored by Git and is intended only for local development.

## Authentication Model

1Panel authentication is handled automatically by the CLI.

The token model is:

```text
md5("1panel" + API-Key + UnixTimestamp)
```

The CLI sends:

- `1Panel-Token`
- `1Panel-Timestamp`

See [references/api-auth.md](references/api-auth.md) for the detailed authentication notes used by the skill.

## Quick Start

Check resolved configuration:

```bash
python3 scripts/panel_cli.py config show
python3 scripts/panel_cli.py config cache
```

Check API connectivity:

```bash
python3 scripts/panel_cli.py ping
```

Run common read tasks:

```bash
python3 scripts/panel_cli.py task website-overview
python3 scripts/panel_cli.py task website-overview --no-https --no-proxies
python3 scripts/panel_cli.py task website-inspect --domain example.com
python3 scripts/panel_cli.py dashboard current
python3 scripts/panel_cli.py websites list
python3 scripts/panel_cli.py apps list
python3 scripts/panel_cli.py containers list
python3 scripts/panel_cli.py hosts list
python3 scripts/panel_cli.py firewall base
```

## Command Model

The CLI is intentionally split into two layers.

### 1. Task and Domain Commands

Use these first for routine diagnostics:

- `task ...`
- `websites ...`
- `dashboard ...`
- `apps ...`
- `containers ...`
- `hosts ...`
- `host-commands ...`
- `firewall ...`

These commands return normalized, safe summaries instead of raw payload dumps by default.

### 2. Full Swagger Coverage

Use these when the task is unfamiliar or when preparing a write:

- `discover ...`
- `schema ...`
- `template ...`
- `call ...`

Typical flow:

1. Discover the endpoint from Swagger
2. Inspect request and response schema
3. Generate a request template
4. Execute a controlled API call

Examples:

```bash
python3 scripts/panel_cli.py discover swagger-url
python3 scripts/panel_cli.py discover endpoints --match website
python3 scripts/panel_cli.py schema show request.WebsiteCreate
python3 scripts/panel_cli.py template POST /websites
```

## Safe Write Workflow

Write operations are intentionally gated.

Without `--confirm`, a non-safe request prints the execution plan instead of sending the write. This makes it easier to inspect the target URL, request body, and whether the CLI considers the request a write.

Examples:

```bash
python3 scripts/panel_cli.py call POST /websites/update --body-file payload.json
python3 scripts/panel_cli.py call POST /websites/update --body-file payload.json --confirm
```

If a Swagger-confirmed read endpoint uses `POST`, you can allow it explicitly:

```bash
python3 scripts/panel_cli.py call POST /containers/list --body '{}' --assume-read
```

## Response Behavior

The raw `call` command supports multiple output modes:

- default: normalized payload with `data` and lightweight metadata
- `--data-only`: print only the normalized `data` field
- `--raw-response`: print the legacy raw response structure

This makes the CLI easier to use both for humans and for LLM-driven automation.

## Generated Swagger Artifacts

The repository can generate generic API reference artifacts under `references/generated/`.

To rebuild them:

```bash
python3 scripts/build_swagger_artifacts.py
```

Generated outputs include:

- tag-level summaries
- path-level indexes
- schema name lists
- machine-readable JSON indexes

The generator rewrites the source URL to a generic placeholder so the output is safer to publish.

## Open-Source Hygiene

This repository is intended to be publishable.

Before pushing, keep these rules:

- do not commit `config/local.json`
- do not commit instance-specific notes in `references/*.local.md`
- keep example config values generic
- avoid embedding private domains, base URLs, or credentials in generated docs

## Related Files

- [SKILL.md](SKILL.md): skill instructions for Codex-style execution
- [references/api-auth.md](references/api-auth.md): auth and config rules
- [references/api-workflows.md](references/api-workflows.md): read/write workflow guidance
- [references/api-coverage.md](references/api-coverage.md): full-coverage Swagger workflow

## License

MIT. See [LICENSE](LICENSE).
