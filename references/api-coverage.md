# 1Panel API Coverage

The CLI is designed to reach every API path that exists in the Swagger/OpenAPI definition. That full-coverage loop is for unfamiliar reads and all writes, not for common read-only questions.

For common read-only questions, prefer task-oriented or domain-oriented commands first:

- `task website-overview`
- `task website-overview --no-https --no-proxies`
- `task website-inspect --domain example.com`
- `dashboard current`
- `websites list`
- `apps list`
- `containers list`

Only fall back to the full Swagger loop when those commands do not cover the request.

Think of the full-coverage loop as four steps:

1. **Swagger discovery** – run `1panel api discover swagger-url` to resolve the active `doc.json`, then use `discover endpoints --match <keyword>` (optionally `--tag`) to enumerate operations and confirm the method & path.
2. **Schema lookup** – once you know the path, open the `doc.json` payload or inspect the `components` node to see the accepted request schema and response shape. The CLI downloads that JSON automatically via `PanelClient.swagger_spec()`, so you can copy/paste example objects or follow the property names defined there.
3. **Request-template generation** – build the request body from the schema, either inline with `--body` or by editing a file and passing `--body-file payload.json`. Use `--dry-run` or the standard `plan` output to verify the method, URL, query string, and summary of the change before actually hitting the API.
4. **Raw call** – execute `1panel api call METHOD /path --body-file payload.json --confirm` (or add `--assume-read` for verified read-only POSTs). The raw `call` command is what unlocks the full API surface once you have a body template and path.

The repository can also keep a generated API catalog under `references/generated/`:

- `catalog.md` for a tag-level index
- `swagger-index.md` for a verbose readable index
- `swagger-by-tag.json` and `swagger-by-path.json` for machine-oriented lookups

Those generated files should stay generic and must not leak private instance names or internal domains.

Read the discovery/schema/template output before every write, and always replay the plan output for confirmation.

For day-to-day diagnostics there are curated convenience commands that wrap common domains:

- `task website-overview`
- `task website-inspect`
- `websites list`
- `apps list`
- `containers list`
- `dashboard current`
- `hosts list`
- `firewall base`

Each wrapper hits a known safe endpoint or an internal read-only aggregator and can optionally show the raw payload with `--raw`. Use them for quick checks, and only revert to the four-step coverage loop (discovery → schema → template → raw call) when the task is unfamiliar or is preparing a write.
