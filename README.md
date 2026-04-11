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

## Installation

Install in development mode:

```bash
pip install -e .
```

With development dependencies (pytest, pytest-httpx, ruff):

```bash
pip install -e ".[dev]"
```

After installation, the `1panel` command is available globally.

## Configuration

The CLI reads configuration from environment variables first, then falls back to `config/local.json`.

### Environment Variables (preferred)

```bash
export ONEPANEL_BASE_URL="https://panel.example.com"
export ONEPANEL_API_KEY="your-api-key"
```

### Supported Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ONEPANEL_BASE_URL` | (required) | 1Panel instance base URL |
| `ONEPANEL_API_KEY` | (required) | 1Panel API key |
| `ONEPANEL_TIMEOUT` | `20` | HTTP request timeout in seconds |
| `ONEPANEL_VERIFY_TLS` | `true` | Whether to verify TLS certificates |
| `ONEPANEL_SWAGGER_CACHE_TTL_SECONDS` | `600` | Swagger spec cache TTL |

**Backward compatibility:** The legacy `1PANEL_` prefix (e.g. `1PANEL_BASE_URL`, `1PANEL_API_KEY`) is still supported. The `ONEPANEL_` prefix takes priority when both are set.

### Local Config File

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

See [references/api-auth.md](references/api-auth.md) for detailed authentication notes.

## CLI Command Reference

### Domain Commands

```bash
1panel website list              # List websites
1panel website overview          # Website overview with HTTPS and proxy details
1panel app list                  # List installed applications
1panel container list            # List container names
1panel dashboard                 # Show current dashboard metrics
1panel host list                 # Search hosts with pagination
1panel host tree                 # Show host tree structure
1panel host commands             # List saved host commands
1panel firewall status           # Show firewall base status
```

All domain commands support `--raw` to print the full API response.

### API Discovery and Raw Access

```bash
1panel api discover              # Discover Swagger endpoints
1panel api discover --match website
1panel api schema SCHEMA_NAME    # View a Swagger schema definition
1panel api template METHOD PATH  # Generate a request template
1panel api call --method GET --path /websites/list
```

### Configuration and Connectivity

```bash
1panel config show               # Show resolved configuration
1panel config cache              # Show Swagger cache info
1panel ping                      # Check API connectivity
```

## Command Model

The CLI is intentionally split into two layers.

### 1. Domain Commands

Use these first for routine diagnostics:

- `website ...` — website management
- `dashboard` — system metrics
- `app ...` — installed applications
- `container ...` — Docker containers
- `host ...` — remote hosts and saved commands
- `firewall ...` — firewall status

These commands return normalized, safe summaries instead of raw payload dumps by default.

### 2. Full Swagger Coverage

Use these when the task is unfamiliar or when preparing a write:

- `api discover` — find endpoints
- `api schema` — inspect schemas
- `api template` — generate request body templates
- `api call` — execute API calls with optional confirmation gates

Typical flow:

1. Discover the endpoint from Swagger
2. Inspect request and response schema
3. Generate a request template
4. Execute a controlled API call

## Safe Write Workflow

Write operations are intentionally gated.

Without `--confirm`, a non-safe request prints the execution plan instead of sending the write. This makes it easier to inspect the target URL, request body, and whether the CLI considers the request a write.

Examples:

```bash
1panel api call --method POST --path /websites/update --body-file payload.json
1panel api call --method POST --path /websites/update --body-file payload.json --confirm
```

## Development

Run the test suite:

```bash
pip install -e ".[dev]"
pytest
```

Lint with ruff:

```bash
ruff check src/ tests/
```

## Related Files

- [SKILL.md](SKILL.md): skill instructions for Codex-style execution
- [references/api-auth.md](references/api-auth.md): auth and config rules
- [references/api-workflows.md](references/api-workflows.md): read/write workflow guidance
- [references/api-coverage.md](references/api-coverage.md): full-coverage Swagger workflow

## License

MIT. See [LICENSE](LICENSE).
