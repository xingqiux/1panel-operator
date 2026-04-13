# 1Panel Operator

[中文文档](README_zh.md)

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

### Core Commands

```bash
1panel ping                      # Check API connectivity
1panel config show               # Show resolved configuration
1panel config cache              # Show Swagger cache info
```

### Website Commands

```bash
1panel website list              # List websites
1panel website overview          # Website overview with HTTPS and proxy details
1panel website inspect           # Inspect one website in detail
1panel website ssl list          # List SSL certificates
1panel website ca list           # List CA certificates
1panel website acme list         # List ACME accounts
1panel website dns list          # List DNS accounts
1panel website domain list       # List domains for a website
```

### Container Commands

```bash
1panel container list            # List containers with state/image/ports
1panel container stats           # Show container resource usage
1panel container image list      # List Docker images
1panel container compose list    # List Compose stacks
1panel container network list    # List Docker networks
1panel container volume list     # List Docker volumes
1panel container docker status   # Show Docker daemon status
```

### Application Commands

```bash
1panel app list                  # List installed applications
1panel app show ID               # Show application details
```

### Database Commands

```bash
1panel database list             # List all databases
1panel database show NAME        # Show database details
1panel database mysql-list       # List MySQL databases
1panel database mysql-status     # Show MySQL status
1panel database pg-list          # List PostgreSQL databases
1panel database redis-status     # Show Redis status
1panel database redis-conf       # Show Redis configuration
1panel database redis-commands   # List saved Redis commands
```

### System & Host Commands

```bash
1panel dashboard                 # Show dashboard metrics
1panel host list                 # Search hosts with pagination
1panel host tree                 # Show host tree structure
1panel host commands             # List saved host commands
1panel host ssh-status           # Show SSH configuration
1panel host ssh-logs             # Search SSH login logs
1panel host tool-status          # Check host tool status
1panel system info               # Show system settings
1panel system ssl-info           # Show system certificate info
1panel system snapshot-list      # List system snapshots
1panel system group-list         # List host groups
1panel device info               # Show device base info
```

### Security Commands

```bash
1panel firewall status           # Show firewall base status
1panel firewall rules            # List firewall rules
1panel fail2ban status           # Show Fail2ban status
1panel fail2ban conf             # Show Fail2ban configuration
1panel fail2ban list             # List banned/ignored IPs
1panel ssh status                # Show SSH status
1panel ssh conf                  # Show raw SSH config
1panel ssh logs                  # Search SSH login logs
1panel clam status               # Show ClamAV status
1panel clam list                 # List ClamAV scan definitions
1panel clam records              # List ClamAV scan records
```

### Service Commands

```bash
1panel openresty status          # Show OpenResty status
1panel openresty config          # Show OpenResty config
1panel ftp status                # Show FTP status
1panel ftp list                  # List FTP users
1panel ftp logs                  # List FTP operation logs
1panel runtime list              # List application runtimes
1panel runtime show ID           # Show runtime details
1panel cronjob list              # List scheduled cron jobs
1panel cronjob show ID           # Show cron job details
1panel backup list               # List backup accounts
1panel backup records            # List backup records
1panel ai gpu                    # Show GPU/XPU status
1panel ai models                 # List Ollama models
```

### Log Commands

```bash
1panel logs login                # Search login logs
1panel logs operation            # Search operation logs
1panel logs system               # Load system logs
1panel logs files                # List system log files
```

### File Management

```bash
1panel file list PATH            # List files in a directory
1panel file tree PATH            # Show directory tree
```

### API Discovery and Raw Access

```bash
1panel api discover              # Discover Swagger endpoints
1panel api discover --match website
1panel api schema SCHEMA_NAME    # View a Swagger schema definition
1panel api template METHOD PATH  # Generate a request template
1panel api call --method GET --path /websites/list
```

All domain commands support `--raw` to print the full API response.

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
