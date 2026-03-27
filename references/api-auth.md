# 1Panel API Auth

## 通用入口约定

- Swagger UI：`<base_url>/1panel/swagger/index.html`
- Swagger 定义：`<base_url>/1panel/swagger/doc.json`
- Swagger `basePath`：`/api/v1`

`index.html` 只是 UI；真正的接口定义要以 `doc.json` 为准。

## Token 规则

认证采用 1Panel 的自定义 token：

```text
Token = md5("1panel" + API-Key + UnixTimestamp)
```

请求头固定为：

- `1Panel-Token`
- `1Panel-Timestamp`

时间戳是秒级 Unix 时间戳。

## 配置来源

脚本优先从环境变量读取：

- `1PANEL_BASE_URL`
- `1PANEL_API_KEY`
- `1PANEL_TIMEOUT`
- `1PANEL_VERIFY_TLS`

如果环境变量缺失，则回退到 `config/local.json`。

## 当前 skill 默认本地配置

开发目录内允许存在：

- `config/local.json`
- `config/local.example.json`

公开版本中：

- `config/local.example.json` 只保留占位值
- `config/local.json` 只作为本地开发覆盖使用，并由 `.gitignore` 忽略
- 某个具体实例的上下文说明应放在 `references/*.local.md` 中，本地保留，避免进入开源仓库

## 常见失败原因

- `401`：token、timestamp、api key 不匹配
- `404`：路径没按 `/api/v1` 基础路径拼接，或接口版本不对
- TLS 错误：证书链或安全入口导致
- 看得到 Swagger UI 但接口失败：说明入口页面存在，不代表 API 路径一定正确，必须以 `doc.json` 中的路径为准
