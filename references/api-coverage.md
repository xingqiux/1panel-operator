# 1Panel API Coverage

The CLI is designed to reach every API path that exists in the Swagger/OpenAPI definition. That full-coverage loop is for unfamiliar reads and all writes, not for common read-only questions.

For common read-only questions, prefer task-oriented or domain-oriented commands first:

- `1panel website overview`
- `1panel website overview --no-https --no-proxies`
- `1panel website inspect --domain example.com`
- `1panel dashboard`
- `1panel website list`
- `1panel app list`
- `1panel container list`

Only fall back to the full Swagger loop when those commands do not cover the request.

Think of the full-coverage loop as four steps:

1. **Swagger discovery** – run `1panel api discover --match <keyword>` (optionally `--tag`) to enumerate operations from the active Swagger cache and confirm the method & path.
2. **Schema lookup** – use `1panel api schema list --match <keyword>` to find the right definition, then `1panel api schema show <definition>` to inspect the accepted request schema and response shape.
3. **Request-template generation** – run `1panel api template METHOD /path` to build the request body template, then fill values inline with `--body` or by editing a file and passing `--body-file payload.json`. Use `--dry-run` or the standard `plan` output to verify the method, URL, query string, and summary of the change before actually hitting the API.
4. **Raw call** – execute `1panel api call METHOD /path --body-file payload.json --confirm` (or add `--assume-read` for verified read-only POSTs). The raw `call` command is what unlocks the full API surface once you have a body template and path.

The repository can also keep a generated API catalog under `references/generated/`:

- `catalog.md` for a tag-level index
- `swagger-index.md` for a verbose readable index
- `swagger-by-tag.json` and `swagger-by-path.json` for machine-oriented lookups

Those generated files should stay generic and must not leak private instance names or internal domains.

Read the discovery/schema/template output before every write, and always replay the plan output for confirmation.

For day-to-day diagnostics there are curated convenience commands that wrap common domains:

- `1panel website overview`
- `1panel website inspect`
- `1panel website list`
- `1panel app list`
- `1panel container list`
- `1panel dashboard`
- `1panel host list`
- `1panel firewall status`

Each wrapper hits a known safe endpoint or an internal read-only aggregator and can optionally show the raw payload with `--raw`. Use them for quick checks, and only revert to the four-step coverage loop (discovery → schema → template → raw call) when the task is unfamiliar or is preparing a write.
