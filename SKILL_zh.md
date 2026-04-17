---
name: 1panel-operator
description: 通过认证 API 和 Swagger 定义操作和调试 1Panel 实例。当用户想要检查、诊断或更改 1Panel 管理的资源（如网站、反向代理、应用安装、容器、主机设置或仪表板状态）时使用。优先使用捆绑的 CLI 而不是临时 curl。对于写操作，始终先检查当前状态，展示预期的 API 操作，并在执行前要求明确的用户确认。
---

使用此技能通过 API 操作 1Panel，而不是描述产品。

## 前置条件

CLI 必须在使用前安装。在技能目录中运行一次：

```bash
pip install -e /path/to/1panel-operator
```

安装后，`1panel` 命令全局可用。如果找不到 `1panel`，先回退到 `pip install -e <skill_root>`。

## 激活行为

当技能被显式调用时：

- 不要宣布技能已加载。
- 除非用户询问，否则不要重述整个工作流。
- 除非用户要求示例，否则不要列出示例请求或功能菜单。
- 如果用户已经给出具体任务，直接执行。
- 如果没有提供具体任务，用 2-3 个简短句子回复：
  - 第 1 句：简要说明此技能用于通过 API 查询、诊断和更改 1Panel 管理的资源
  - 第 2 句：简要说明主要资源范围（如网站、容器、应用、主机和系统设置）
  - 第 3 句：请用户说明目标资源或期望的更改
- 保持激活回复通用和中性。
- 不要在激活回复中包含实例特定的示例、域名或示例用户请求。

## 完整 API 覆盖

完整的官方 API 覆盖仍然来自 `references/api-coverage.md` 中描述的 Swagger 发现、模式查找、请求模板生成和原始调用循环，但该循环现在是回退路径，而不是默认路径。

按此优先顺序使用技能：

1. 领域命令如 `1panel website ...`、`1panel app ...`、`1panel container ...`、`1panel host ...`
2. 仅当任务不熟悉或准备写操作时使用 `1panel api discover/schema/template/call`

## 快速入门

1. 阅读 `references/api-auth.md` 确认认证规则和配置来源。
2. 阅读 `references/api-coverage.md` 了解 Swagger 端点发现、模式查找、请求模板和原始调用。
3. 如果存在本地上下文文件（如 `references/instance-context.local.md`），仅在需要实例特定详情时阅读。
4. 使用 `1panel ...` 命令。不要手写令牌和 curl。
5. 对于常见读任务，首先尝试领域命令。不要从 `--help`、`discover`、`schema` 或 `template` 开始。
6. 在任何写操作之前：
   - 先检查当前状态
   - 描述 API 端点、方法、目标资源和副作用
   - 等待明确的用户确认
   - 使用 `--confirm` 执行

## 首选工作流

### 只读任务

- 对于常见读任务，首先使用领域命令
- 如果问题是"列出网站"或"有哪些站点"，使用 `1panel website list`
- 如果问题是"当前网站配置"，使用 `1panel website overview`
- 如果关注单个站点，使用 `1panel website overview --domain ...`
- 仅当领域命令不足时才回退到 `1panel api discover/schema/template/call`

### 写操作

- 定位目标资源的当前状态
- 展示最小必要的 API 更改计划
- 用户确认后，执行写操作
- 重新读取结果以验证

## 关键命令

### 核心
```bash
1panel ping                      # 检查 API 连通性
1panel config show               # 显示已解析的配置
```

### 网站
```bash
1panel website list              # 列出网站
1panel website overview          # 网站概览（含 HTTPS/代理）
1panel website ssl list          # 列出 SSL 证书
1panel website domain list       # 列出域名
```

### 容器
```bash
1panel container list            # 列出容器（含状态/镜像）
1panel container stats           # 容器资源使用
1panel container image list      # 列出 Docker 镜像
1panel container compose list    # 列出 Compose 堆栈
1panel container network list    # 列出网络
1panel container volume list     # 列出卷
```

### 数据库
```bash
1panel database list             # 列出数据库
1panel database mysql-status     # MySQL 状态
1panel database redis-status     # Redis 状态
```

### 系统和安全
```bash
1panel dashboard                 # 仪表板指标
1panel host list                 # 列出主机
1panel system info               # 系统设置
1panel firewall status           # 防火墙状态
1panel firewall rules            # 列出防火墙规则
1panel fail2ban status           # Fail2ban 状态
1panel ssh status                # SSH 状态
```

### 服务
```bash
1panel app list                  # 已安装应用
1panel openresty status          # OpenResty 状态
1panel ftp list                  # FTP 用户
1panel runtime list              # 应用运行时
1panel cronjob list              # 计划任务
1panel backup list               # 备份账户
1panel ai gpu                    # GPU 状态
1panel logs login                # 登录日志
```

### 文件
```bash
1panel file list PATH            # 列出文件
1panel file tree PATH            # 目录树
```

### API 发现
```bash
1panel api discover --match website
```

写操作示例：

```bash
1panel api call POST /websites/update --body-file payload.json
1panel api call POST /websites/update --body-file payload.json --confirm
1panel api call POST /containers/list --body '{}' --assume-read
```

第一个命令显示执行计划。第二个实际执行。第三个用于 Swagger 确认的使用 POST 的只读端点。

## 任务预算

对于常见读任务，默认预算是：

- 最多 1 个领域命令
- 如果需要补充，最多 1 个额外命令
- 最多 1 句过程解释
- 不要叙述内部子请求、Swagger 关键字或中间处理步骤
- 不要从 `--help` 开始
- 不要从 `discover/schema/template` 开始

## 资源映射

从目标 Swagger 定义确认的高频资源域：

| 域 | 关键端点 |
|----|----------|
| Dashboard | `/dashboard/base/os`, `/dashboard/base/all/all` |
| Apps | `/apps/installed/search`, `/apps/installed/{id}` |
| Containers | `/containers/search`, `/containers/list/stats` |
| Websites | `/websites/list`, `/websites/{id}/https`, `/websites/proxies` |
| SSL/CA/ACME | `/websites/ssl/search`, `/websites/ca/search`, `/websites/acme/search` |
| Databases | `/databases/search`, `/databases/mysql/search`, `/databases/redis/status` |
| Hosts | `/hosts/search`, `/hosts/tool/*`, `/hosts/ssh/*` |
| Firewall | `/hosts/firewall/base`, `/hosts/firewall/search` |
| Fail2ban | `/toolbox/fail2ban/base`, `/toolbox/fail2ban/search` |
| Services | `/openresty`, `/toolbox/ftp/base`, `/runtimes/search` |
| System | `/settings/info`, `/settings/ssl/info`, `/settings/snapshot/search` |
| Logs | `/logs/login`, `/logs/operation`, `/logs/system` |
| Files | `/files/search`, `/files/tree` |
| AI | `/ai/gpu`, `/ai/ollama/models` |

更详细的调用约定和错误处理，见 `references/api-workflows.md`。
