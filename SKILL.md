---
name: 1panel-operator
description: Operate and debug a 1Panel instance through its authenticated API and Swagger definition. Use when the user wants to inspect, diagnose, or change 1Panel-managed resources such as websites, reverse proxies, app installs, containers, host settings, or dashboard state. Prefer the bundled CLI over ad-hoc curl. For write operations, always inspect current state first, present the intended API action, and require explicit user confirmation before executing.
---

Use this skill to operate 1Panel through the API instead of describing the product.

## Activation Behavior

When the skill is invoked explicitly:

- Do not announce that the skill has been loaded.
- Do not restate the whole workflow unless the user asks for it.
- Do not list example requests or capability menus unless the user asks for examples.
- If the user already gave a concrete task, execute it directly.
- If no concrete task was provided, reply with 2-3 short sentences:
  - sentence 1: briefly state that this skill is for querying, diagnosing, and changing 1Panel-managed resources through the API
  - sentence 2: briefly state the main resource scope in generic terms, such as websites, containers, apps, hosts, and system settings
  - sentence 3: ask the user to state the target resource or desired change
- Keep that activation reply generic and neutral.
- Do not include instance-specific examples, domain names, or sample user requests in the activation reply.

## Full API Coverage

Full official API coverage still comes from the Swagger discovery, schema lookup, request-template generation, and raw call loop described in `references/api-coverage.md`, but that loop is now the fallback path, not the default path.

Use the skill in this priority order:

1. domain commands such as `1panel website ...`, `1panel app ...`, `1panel container ...`, `1panel host ...`
2. `1panel api discover/schema/template/call` only when the task is unfamiliar or is preparing a write

## Quick Start

1. Read `references/api-auth.md` to confirm auth rules and config sources.
2. Read `references/api-coverage.md` to understand Swagger endpoint discovery, schema lookup, request templates, and raw calls.
3. If a local context file exists (e.g. `references/instance-context.local.md`), only read it when instance-specific details are needed.
4. Use `1panel ...` commands. Do not hand-write tokens and curl.
5. For common read tasks, try domain commands first. Do not start with `--help`, `discover`, `schema`, or `template`.
6. Before any write operation:
   - Inspect current state first
   - Describe the API endpoint, method, target resource, and side effects
   - Wait for explicit user confirmation
   - Execute with `--confirm`

## Preferred Workflow

### Read-Only Tasks

- For common read tasks, use domain commands first
- If the question is "list websites" or "what sites exist", use `1panel website list`
- If the question is "current website configuration", use `1panel website overview`
- If focused on a single site, use `1panel website overview --domain ...`
- Only fall back to `1panel api discover/schema/template/call` when domain commands are insufficient

### Write Operations

- Locate the current state of the target resource
- Present the minimal necessary API change plan
- After user confirmation, execute the write
- Re-read the result to verify

## Key Commands

```bash
1panel config show
1panel config cache
1panel website list
1panel website overview
1panel dashboard
1panel app list
1panel container list
1panel host list
1panel host tree
1panel host commands
1panel firewall status
1panel api discover --match website
```

Write operation examples:

```bash
1panel api call --method POST --path /websites/update --body-file payload.json
1panel api call --method POST --path /websites/update --body-file payload.json --confirm
1panel api call --method POST --path /containers/list --body '{}' --assume-read
```

The first command shows the execution plan. The second actually executes. The third is for Swagger-confirmed read-only endpoints that use POST.

## Task Budget

For common read tasks, the default budget is:

- At most 1 domain command
- If supplementation is needed, at most 1 additional command
- At most 1 sentence of process explanation
- Do not narrate internal sub-requests, Swagger keywords, or intermediate processing steps
- Do not start with `--help`
- Do not start with `discover/schema/template`

## Resource Map

High-frequency resource domains confirmed from the target Swagger definition:

- `Dashboard`: `/dashboard/current`
- `Apps`: `/apps/installed/list`, `/apps/installed/search`, `/apps/install`
- `Containers`: `/containers/list`, `/containers/search`, `/containers/operate`
- `Websites`: `/websites/list`, `/websites/search`, `/websites/update`, `/websites/proxies`
- `Hosts`: `/hosts/search`, `/hosts/tool/*`, `/hosts/ssh/*`
- `Firewall`: `/hosts/firewall/base`

For more detailed calling conventions and error handling, see `references/api-workflows.md`.
