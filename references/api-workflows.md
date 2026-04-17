# 1Panel API Workflows

## 1. 查询类任务

适用于：

- 查看面板概览
- 列出网站、容器、应用、主机配置
- 排查某个资源当前状态

推荐顺序：

1. 先判断这是不是常见读任务
2. 如果是常见读任务，优先使用现成的领域命令
3. 如果领域命令没覆盖，再进入 Swagger 探索
4. 只有不熟悉的接口，才进入 `discover/schema/template/call`

常见读任务示例：

- “列出网站” -> `1panel website list`
- “当前网站配置是怎样的” -> `1panel website overview`
- “只看网站基础列表，不要 SSL/代理细节” -> `1panel website overview --no-https --no-proxies`
- “看某个站点的当前配置” -> `1panel website inspect --domain example.com`
- `1panel website overview`
- `1panel website inspect --domain example.com`
- `1panel dashboard`
- `1panel app list`
- `1panel container list`

查询类任务预算：

- 最多 2 次 CLI 调用
- 默认不逐条汇报内部 API 子请求
- 默认不允许 `--help`
- 默认不允许先 `discover`

## 2. 写操作任务

适用于：

- 创建、修改、删除网站
- 操作容器、镜像、应用安装
- 更新主机配置或 1Panel 管理对象

固定流程：

1. 先读当前状态
2. 明确目标 API 路径、HTTP 方法、请求体
3. 先跑一次不带 `--confirm` 的命令，让 CLI 输出计划
4. 用户明确确认后，再带 `--confirm` 执行
5. 执行完回读结果

如果某个接口在 Swagger 中明确是查询用途，但方法是 `POST`，可以用 `--assume-read` 执行，不需要 `--confirm`。

## 3. 发现接口

不要假设接口路径。

优先做法：

- 先从 `doc.json` 里搜索 tag、path、summary
- 根据资源关键字筛选，如 `website`、`container`、`app`、`host`
- 只有在 Swagger 里确认了路径、方法和请求体后，才发写请求
- 如果问题本身已经是常见读任务，不要回到这里

## 4. 输出要求

当你代表用户执行 1Panel 操作时，输出应包含：

- 当前目标实例
- 使用的接口路径和方法
- 请求是否属于写操作
- 风险或副作用
- 执行后的结果摘要

## 5. 禁止事项

- 不要在对话里反复手写 token
- 不要跳过现状查询直接修改资源
- 不要在未确认的情况下执行 `POST`、`PUT`、`DELETE`
- 不要只看 Swagger UI 页面而不读 `doc.json`
- 不要把常见读任务变成 Swagger 探索任务
