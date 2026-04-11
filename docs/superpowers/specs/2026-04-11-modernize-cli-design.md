# 1Panel Operator — 现代化 CLI 重写设计

## 概述

将 1panel-operator 从散落的 `scripts/` 脚本重写为标准 Python 包，使用现代工具链（typer + httpx + pydantic），重新设计 CLI 命令层次，补齐错误处理、测试、日志等基础设施。

目标受众：开源社区 + 个人运维工具。

## 依赖

| 库 | 用途 |
|---|---|
| `typer[all]` | CLI 框架（含 rich 输出 + shell 补全） |
| `httpx` | HTTP 客户端（连接池、超时、async-ready） |
| `pydantic>=2` | 配置校验 + 响应模型 |
| `structlog` | 结构化日志 |
| `pytest` | 测试框架 |
| `pytest-httpx` | HTTP mock |

## 包结构

```
1panel-operator/
├── pyproject.toml
├── src/
│   └── onepanel/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py       # app = typer.Typer(), 注册子命令
│       │   ├── main.py           # ping, config
│       │   ├── website.py        # website list/overview/inspect
│       │   ├── app.py            # app list
│       │   ├── container.py      # container list
│       │   ├── host.py           # host list/tree/commands
│       │   ├── firewall.py       # firewall status
│       │   ├── dashboard.py      # dashboard
│       │   └── api.py            # api discover/schema/template/call
│       ├── client.py             # httpx-based PanelClient
│       ├── config.py             # pydantic BaseSettings
│       ├── auth.py               # token 生成
│       ├── models.py             # ApiResult 统一响应信封
│       ├── swagger.py            # Swagger 解析与缓存
│       └── log.py                # 日志配置
├── tests/
│   ├── conftest.py               # fixtures: mock client, sample responses
│   ├── test_auth.py
│   ├── test_config.py
│   ├── test_client.py
│   ├── test_swagger.py
│   └── test_cli/
│       ├── test_website.py
│       ├── test_app.py
│       ├── test_container.py
│       └── test_api.py
├── config/
│   └── local.example.json
├── SKILL.md
└── README.md
```

入口点：`pyproject.toml` 中声明 `[project.scripts] 1panel = "onepanel.cli:app"`

## CLI 命令层次

```
1panel ping
1panel config show [--reveal-key]
1panel config cache

1panel website list [--raw]
1panel website overview [--no-https] [--no-proxies] [--workers N]
1panel website inspect (--domain X | --id N) [--no-https] [--no-proxies]

1panel app list [--raw]
1panel container list [--raw]

1panel host list [--raw] [--page N] [--page-size N]
1panel host tree [--raw]
1panel host commands [--raw]

1panel dashboard [--raw]
1panel firewall status [--raw]

1panel api discover [--match X] [--tag X] [--limit N]
1panel api schema list [--match X]
1panel api schema show <name>
1panel api template <method> <path>
1panel api call <method> <path> [--body X] [--body-file X]
                                [--confirm] [--assume-read]
                                [--data-only] [--raw] [--dry-run]
```

全局选项：`--verbose` / `--debug` / `--output json|table`

### 与现有命令的映射

| 旧命令 | 新命令 | 说明 |
|---|---|---|
| `task website-overview` | `website overview` | 合并，消除重复入口 |
| `task website-inspect` | `website inspect` | 合并 |
| `websites list` | `website list` | 单数命名 |
| `host-commands list/tree` | `host commands` | 收入 host 子命令 |
| `discover endpoints` | `api discover` | Swagger 工具收拢 |
| `schema show` | `api schema show` | 收拢 |
| `template` | `api template` | 收拢 |
| `call` | `api call` | 收拢 |
| `firewall base` | `firewall status` | 更直观的命名 |

## 核心架构

### 配置（config.py）

```python
from pydantic_settings import BaseSettings

class PanelConfig(BaseSettings):
    base_url: str
    api_key: str
    timeout: int = 20
    verify_tls: bool = True
    swagger_cache_ttl_seconds: int = 600

    model_config = SettingsConfigDict(
        env_prefix="ONEPANEL_",
        json_file="config/local.json",
    )
```

环境变量前缀从 `1PANEL_` 改为 `ONEPANEL_`（`1` 开头不是合法 Python 标识符，pydantic 也不友好）。保留对旧前缀的兼容。

### 认证（auth.py）

保持现有逻辑不变：`md5("1panel" + api_key + timestamp)`。

### Client（client.py）

```python
class PanelClient:
    def __init__(self, config: PanelConfig):
        self._http = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            verify=config.verify_tls,
        )
        self._config = config
        self._swagger = SwaggerCache(self, config.swagger_cache_ttl_seconds)

    def request(self, method, path, **kwargs) -> ApiResult:
        # 统一: 注入 auth headers → 发请求 → 解析 → 返回 ApiResult
        ...

    def plan(self, method, path, **kwargs) -> dict:
        # 写操作计划（不执行）
        ...
```

### 统一响应信封（models.py）

```python
from pydantic import BaseModel

class ApiResult(BaseModel):
    ok: bool
    data: Any = None
    count: int | None = None
    meta: dict = {}       # status_code, url, timing_ms
    error: str | None = None
```

所有 CLI 命令最终输出 `ApiResult`，CLI 层决定格式化方式（JSON / table / data-only）。

### Swagger（swagger.py）

从 `client.py` 中剥离，独立模块：
- `SwaggerCache` — 磁盘缓存 + TTL
- `SwaggerParser` — 端点发现、schema 解析、模板生成
- `SwaggerOperation` dataclass 保留

### 日志（log.py）

```python
import structlog

def setup_logging(verbose: bool = False, debug: bool = False):
    level = "DEBUG" if debug else "INFO" if verbose else "WARNING"
    structlog.configure(...)
```

CLI 全局回调中调用 `setup_logging()`。

## 错误处理

三层策略：

1. **Client 层** — `httpx` 异常统一包装为 `PanelAPIError`，附带 status_code + response body
2. **业务层（CLI commands）** — 不需要 try/except，让异常自然上抛
3. **CLI 入口** — typer 的全局 error handler 捕获并格式化输出

```python
# cli/__init__.py
@app.callback()
def main(verbose: bool = False, debug: bool = False):
    setup_logging(verbose, debug)

# 全局异常处理通过 typer 的 exception handler 或 rich 的 traceback
```

## 测试策略

| 层 | 工具 | 覆盖范围 |
|---|---|---|
| auth | pytest | token 生成正确性 |
| config | pytest | 环境变量 > 文件 > 默认值优先级 |
| client | pytest-httpx | HTTP 请求构造、响应解析、错误处理 |
| swagger | pytest | schema 解析、模板生成、缓存 TTL |
| CLI | typer.testing.CliRunner | 命令解析、输出格式、退出码 |

测试 fixtures 从 `references/generated/` 中的真实 Swagger 数据提取。

## 迁移计划

1. 旧代码保留在 `scripts/` 直到新 CLI 功能对齐
2. `SKILL.md` 在新 CLI 就绪后更新命令引用
3. `README.md` 同步更新
4. 旧 `scripts/` 目录在确认稳定后删除

## 开源就绪

- `pyproject.toml` 含完整 metadata（description, license, classifiers, urls）
- `py.typed` marker
- GitHub Actions CI（lint + test）
- `.pre-commit-config.yaml`（ruff lint + format）
