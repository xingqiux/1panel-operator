---
name: 1panel-operator
description: Operate and debug a 1Panel instance through its authenticated API and Swagger definition. Use when the user wants to inspect, diagnose, or change 1Panel-managed resources such as websites, reverse proxies, app installs, containers, host settings, or dashboard state. Prefer the bundled Python scripts over ad-hoc curl. For write operations, always inspect current state first, present the intended API action, and require explicit user confirmation before executing.
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

Full official API coverage still comes from the Swagger discovery → schema lookup → request-template generation → raw call loop described in `references/api-coverage.md`, but that loop is now the fallback path, not the default path.

Use the skill in this priority order:

1. `task ...` for common user intents
2. domain commands such as `websites ...`, `apps ...`, `containers ...`, `hosts ...`
3. `discover/schema/template/call` only when the task is unfamiliar or is preparing a write

## Quick Start

1. 先读取 `references/api-auth.md`，确认认证规则和配置来源。
2. 阅读 `references/api-coverage.md`，确认如何从 Swagger 探测端点、查看 schema、准备请求模板和执行原始调用。
3. 如果当前仓库存在某个实例专属的本地上下文文件，例如 `references/instance-context.local.md`，只在需要该实例细节时再读取。
4. 优先使用 `python3 scripts/panel_cli.py ...`，不要临时手写 token 和 curl。
5. 对常见读任务，先尝试 `task` 或领域命令，不要先跑 `--help`、`discover`、`schema`、`template`。
6. 写操作前必须：
   - 先读取现状
   - 说明将调用的接口、方法、目标资源和副作用
   - 等用户明确确认后，再用带 `--confirm` 的命令执行

## Preferred Workflow

### 只读任务

- 常见读任务先走 `task`
- 如果问题只是“列出网站”或“当前有哪些站点”，优先 `websites list` 或 `task website-overview --no-https --no-proxies`
- 如果问题是“当前网站配置是怎样的”，使用 `task website-overview`
- 如果问题聚焦到单个站点，使用 `task website-inspect --domain ...`
- 如果 `task` 没覆盖，再走领域命令
- 只有领域命令也不够时，才进入 `discover/schema/template/call`
- 不要为了常见读任务先跑 `--help`

### 写操作任务

- 先定位资源当前状态
- 给出最小必要的 API 变更计划
- 用户确认后，执行写请求
- 执行完再回读一次结果核验

## Key Commands

```bash
python3 scripts/panel_cli.py config show
python3 scripts/panel_cli.py config cache
python3 scripts/panel_cli.py task website-overview
python3 scripts/panel_cli.py task website-overview --no-https --no-proxies
python3 scripts/panel_cli.py task website-inspect --domain docker.example.com
python3 scripts/panel_cli.py dashboard current
python3 scripts/panel_cli.py websites list
python3 scripts/panel_cli.py apps list
python3 scripts/panel_cli.py containers list
python3 scripts/panel_cli.py discover endpoints --match website
```

写操作示例：

```bash
python3 scripts/panel_cli.py call POST /websites/update --body-file payload.json
python3 scripts/panel_cli.py call POST /websites/update --body-file payload.json --confirm
python3 scripts/panel_cli.py call POST /containers/list --body '{}' --assume-read
```

第一条命令用于展示计划，第二条才真正执行。第三条用于 Swagger 已确认的“只读但使用 POST”的接口。

## Task Budget

对常见读任务，默认预算如下：

- 最多 1 个 `task` 命令
- 如果必须补充，最多再加 1 个领域命令
- 过程说明最多 1 句
- 不要逐条播报内部子请求、Swagger 关键词或中间整理步骤
- 禁止先跑 `--help`
- 禁止先跑 `discover/schema/template`

## Resource Map

当前已从目标 Swagger 定义中确认到的高频资源域：

- `Dashboard`：`/dashboard/current`
- `Apps`：`/apps/installed/list`、`/apps/installed/search`、`/apps/install`
- `Containers`：`/containers/list`、`/containers/search`、`/containers/operate`
- `Websites`：`/websites/list`、`/websites/search`、`/websites/update`、`/websites/proxies`
- `Hosts`：`/hosts/search`、`/hosts/tool/*`、`/hosts/ssh/*`

更完整的调用约定和错误处理，见 `references/api-workflows.md`。
