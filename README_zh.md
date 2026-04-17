# 1Panel Operator

`1panel-operator` 是一个任务优先的技能和 CLI 工具，用于通过认证 API 检查和操作 1Panel 实例。

它为两种使用场景设计：

- 作为 Codex 兼容的技能，帮助 AI 代理安全地操作 1Panel
- 作为独立的 Python CLI，用于直接 API 检查、Swagger 发现和受控写操作

本项目避免临时的 `curl` 工作流，将实例特定数据保持在仓库之外，并对常见读操作使用任务优先模型，使日常诊断不会变成多步骤的 Swagger 探索。

## 为什么存在这个项目

1Panel 通过 Swagger/OpenAPI 暴露了大量 API 接口，但日常任务通常分为两类：

- 常见读任务：如检查网站、容器、主机、防火墙状态或仪表板指标
- 受控写任务：需要当前状态检查、明确规划和执行前确认

本仓库提供两者：

- 快速、任务导向的常见读操作命令
- 完整的 Swagger 支持，覆盖不熟悉的读操作和所有写操作

## 特性亮点

- 任务优先命令：网站概览、单站点检查等常见工作流
- 领域命令：网站、仪表板、应用、容器、数据库、主机、防火墙、安全等
- 原始 API 访问：单一 CLI 带请求规划和确认门控
- Swagger 发现、模式查找、请求模板生成和磁盘 Swagger 缓存
- 开源安全默认值：
  - `config/local.json` 被 Git 忽略
  - 公开示例配置保持通用
  - 实例特定备注存放在本地文件中

## 安装

开发模式安装：

```bash
pip install -e .
```

带开发依赖（pytest, pytest-httpx, ruff）：

```bash
pip install -e ".[dev]"
```

安装后，`1panel` 命令全局可用。

## 配置

CLI 首先从环境变量读取配置，然后回退到 `config/local.json`。

### 环境变量（推荐）

```bash
export ONEPANEL_BASE_URL="https://panel.example.com"
export ONEPANEL_API_KEY="your-api-key"
```

### 支持的变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ONEPANEL_BASE_URL` | (必需) | 1Panel 实例基础 URL |
| `ONEPANEL_API_KEY` | (必需) | 1Panel API 密钥 |
| `ONEPANEL_TIMEOUT` | `20` | HTTP 请求超时（秒） |
| `ONEPANEL_VERIFY_TLS` | `true` | 是否验证 TLS 证书 |
| `ONEPANEL_SWAGGER_CACHE_TTL_SECONDS` | `600` | Swagger 规范缓存 TTL |

**向后兼容**：旧的 `1PANEL_` 前缀（如 `1PANEL_BASE_URL`、`1PANEL_API_KEY`）仍然支持。当两者都设置时，`ONEPANEL_` 前缀优先。

## 认证模型

1Panel 认证由 CLI 自动处理。

令牌模型：

```text
md5("1panel" + API-Key + UnixTimestamp)
```

CLI 发送：

- `1Panel-Token`
- `1Panel-Timestamp`

详见 [references/api-auth.md](references/api-auth.md)。

## CLI 命令参考

### 核心命令

```bash
1panel ping                      # 检查 API 连通性
1panel config show               # 显示已解析的配置
1panel config cache              # 显示 Swagger 缓存信息
```

### 网站命令

```bash
1panel website list              # 列出网站
1panel website overview          # 网站概览（含 HTTPS 和代理详情）
1panel website inspect           # 详细检查单个网站
1panel website ssl list          # 列出 SSL 证书
1panel website ca list           # 列出 CA 证书
1panel website acme list         # 列出 ACME 账户
1panel website dns list          # 列出 DNS 账户
1panel website domain list       # 列出网站的域名
```

### 容器命令

```bash
1panel container list            # 列出容器（含状态/镜像/端口）
1panel container stats           # 显示容器资源使用
1panel container image list      # 列出 Docker 镜像
1panel container compose list    # 列出 Compose 堆栈
1panel container network list    # 列出 Docker 网络
1panel container volume list     # 列出 Docker 卷
1panel container docker status   # 显示 Docker 守护进程状态
```

### 应用命令

```bash
1panel app list                  # 列出已安装应用
1panel app show ID               # 显示应用详情
```

### 数据库命令

```bash
1panel database list             # 列出所有数据库
1panel database show NAME        # 显示数据库详情
1panel database mysql-list       # 列出 MySQL 数据库
1panel database mysql-status     # 显示 MySQL 状态
1panel database pg-list          # 列出 PostgreSQL 数据库
1panel database redis-status     # 显示 Redis 状态
1panel database redis-conf       # 显示 Redis 配置
1panel database redis-commands   # 列出保存的 Redis 命令
```

### 系统和主机命令

```bash
1panel dashboard                 # 显示仪表板指标
1panel host list                 # 分页搜索主机
1panel host tree                 # 显示主机树结构
1panel host commands             # 列出保存的主机命令
1panel host ssh-status           # 显示 SSH 配置
1panel host ssh-logs             # 搜索 SSH 登录日志
1panel host tool-status          # 检查主机工具状态
1panel system info               # 显示系统设置
1panel system ssl-info           # 显示系统证书信息
1panel system snapshot-list      # 列出系统快照
1panel system group-list         # 列出主机组
1panel device info               # 显示设备基础信息
```

### 安全命令

```bash
1panel firewall status           # 显示防火墙基础状态
1panel firewall rules            # 列出防火墙规则
1panel fail2ban status           # 显示 Fail2ban 状态
1panel fail2ban conf             # 显示 Fail2ban 配置
1panel fail2ban list             # 列出封禁/忽略的 IP
1panel ssh status                # 显示 SSH 状态
1panel ssh conf                  # 显示原始 SSH 配置
1panel ssh logs                  # 搜索 SSH 登录日志
1panel clam status               # 显示 ClamAV 状态
1panel clam list                 # 列出 ClamAV 扫描定义
1panel clam records              # 列出 ClamAV 扫描记录
```

### 服务命令

```bash
1panel openresty status          # 显示 OpenResty 状态
1panel openresty config          # 显示 OpenResty 配置
1panel ftp status                # 显示 FTP 状态
1panel ftp list                  # 列出 FTP 用户
1panel ftp logs                  # 列出 FTP 操作日志
1panel runtime list              # 列出应用运行时
1panel runtime show ID           # 显示运行时详情
1panel cronjob list              # 列出计划任务
1panel cronjob show ID           # 显示计划任务详情
1panel backup list               # 列出备份账户
1panel backup records            # 列出备份记录
1panel ai gpu                    # 显示 GPU/XPU 状态
1panel ai models                 # 列出 Ollama 模型
```

### 日志命令

```bash
1panel logs login                # 搜索登录日志
1panel logs operation            # 搜索操作日志
1panel logs system               # 加载系统日志
1panel logs files                # 列出系统日志文件
```

### 文件管理

```bash
1panel file list PATH            # 列出目录中的文件
1panel file tree PATH            # 显示目录树
```

### API 发现和原始访问

```bash
1panel api discover              # 发现 Swagger 端点
1panel api discover --match website
1panel api schema list --match website
1panel api schema show request.WebsiteCreate
1panel api template POST /websites  # 生成请求模板
1panel api call GET /websites/list
```

所有领域命令都支持 `--raw` 以打印完整 API 响应。

## 命令模型

CLI 故意分为两层。

### 1. 领域命令

日常诊断首选：

- `website ...` — 网站管理
- `container ...` — Docker 容器
- `database ...` — 数据库管理
- `dashboard` — 系统指标
- `app ...` — 已安装应用
- `host ...` — 远程主机和保存的命令
- `firewall ...` — 防火墙状态
- `fail2ban ...` — Fail2ban 管理
- `ssh ...` — SSH 管理
- `system ...` — 系统设置
- `logs ...` — 日志查询
- `file ...` — 文件管理

这些命令默认返回规范化的安全摘要，而不是原始负载转储。

### 2. 完整 Swagger 覆盖

当任务不熟悉或准备写操作时使用：

- `api discover` — 查找端点
- `api schema` — 检查模式
- `api template` — 生成请求体模板
- `api call` — 执行 API 调用（带可选确认门控）

典型流程：

1. 从 Swagger 发现端点
2. 检查请求和响应模式
3. 生成请求模板
4. 执行受控 API 调用

## 安全写工作流

写操作是故意门控的。

没有 `--confirm` 时，非安全请求打印执行计划而不是发送写操作。这使得检查目标 URL、请求体和 CLI 是否认为请求是写操作变得更容易。

示例：

```bash
1panel api call POST /websites/update --body-file payload.json
1panel api call POST /websites/update --body-file payload.json --confirm
```

## 开发

运行测试套件：

```bash
pip install -e ".[dev]"
pytest
```

使用 ruff 检查：

```bash
ruff check src/ tests/
```

## 相关文件

- [SKILL.md](SKILL.md): Codex 风格执行的技能说明
- [SKILL_zh.md](SKILL_zh.md): 技能说明（中文）
- [references/api-auth.md](references/api-auth.md): 认证和配置规则
- [references/api-workflows.md](references/api-workflows.md): 读/写工作流指南
- [references/api-coverage.md](references/api-coverage.md): 完整覆盖 Swagger 工作流

## 许可证

MIT。详见 [LICENSE](LICENSE)。
