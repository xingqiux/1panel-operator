# Website

- 接口数：`31`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/runtimes/del` | Delete runtime | `#/definitions/request.RuntimeDelete` | `-` |
| `POST` | `/websites` | Create website | `#/definitions/request.WebsiteCreate` | `-` |
| `POST` | `/websites/auths` | Get AuthBasic conf | `#/definitions/request.NginxAuthReq` | `#/definitions/response.NginxAuthRes` |
| `POST` | `/websites/auths/update` | Get AuthBasic conf | `#/definitions/request.NginxAuthUpdate` | `-` |
| `POST` | `/websites/check` | Check before create website | `#/definitions/request.WebsiteInstallCheckReq` | `#/definitions/response.WebsitePreInstallCheck` |
| `POST` | `/websites/default/html/update` | Update default html | `#/definitions/request.WebsiteHtmlUpdate` | `-` |
| `GET` | `/websites/default/html/{type}` | Get default html | `-` | `#/definitions/response.WebsiteHtmlRes` |
| `POST` | `/websites/default/server` | Change default server | `#/definitions/request.WebsiteDefaultUpdate` | `-` |
| `POST` | `/websites/del` | Delete website | `#/definitions/request.WebsiteDelete` | `-` |
| `POST` | `/websites/dir` | Get website dir | `#/definitions/request.WebsiteCommonReq` | `#/definitions/response.WebsiteDirConfig` |
| `POST` | `/websites/dir/permission` | Update Site Dir permission | `#/definitions/request.WebsiteUpdateDirPermission` | `-` |
| `POST` | `/websites/dir/update` | Update Site Dir | `#/definitions/request.WebsiteUpdateDir` | `-` |
| `POST` | `/websites/leech` | Get AntiLeech conf | `#/definitions/request.NginxCommonReq` | `#/definitions/response.NginxAntiLeechRes` |
| `POST` | `/websites/leech/update` | Update AntiLeech conf | `#/definitions/request.NginxAntiLeechUpdate` | `-` |
| `GET` | `/websites/list` | List websites | `-` | `#/definitions/response.WebsiteDTO` |
| `POST` | `/websites/log` | Operate website log | `#/definitions/request.WebsiteLogReq` | `#/definitions/response.WebsiteLog` |
| `POST` | `/websites/operate` | Operate website | `#/definitions/request.WebsiteOp` | `-` |
| `GET` | `/websites/options` | List website names | `-` | `#/definitions/response.WebsiteOption` |
| `GET` | `/websites/php/config/{id}` | Load website php conf | `-` | `#/definitions/response.PHPConfig` |
| `POST` | `/websites/proxies` | Get proxy conf | `#/definitions/request.WebsiteProxyReq` | `#/definitions/request.WebsiteProxyConfig` |
| `POST` | `/websites/proxies/del` | Delete proxy conf | `#/definitions/request.WebsiteProxyDel` | `-` |
| `POST` | `/websites/proxies/update` | Update proxy conf | `#/definitions/request.WebsiteProxyConfig` | `-` |
| `POST` | `/websites/proxy/file` | Update proxy file | `#/definitions/request.NginxProxyUpdate` | `-` |
| `POST` | `/websites/redirect` | Get redirect conf | `#/definitions/request.WebsiteProxyReq` | `#/definitions/response.NginxRedirectConfig` |
| `POST` | `/websites/redirect/file` | Update redirect file | `#/definitions/request.NginxRedirectUpdate` | `-` |
| `POST` | `/websites/redirect/update` | Update redirect conf | `#/definitions/request.NginxRedirectReq` | `-` |
| `POST` | `/websites/rewrite` | Get rewrite conf | `#/definitions/request.NginxRewriteReq` | `#/definitions/response.NginxRewriteRes` |
| `POST` | `/websites/rewrite/update` | Update rewrite conf | `#/definitions/request.NginxRewriteUpdate` | `-` |
| `POST` | `/websites/search` | Page websites | `#/definitions/request.WebsiteSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/websites/update` | Update website | `#/definitions/request.WebsiteUpdate` | `-` |
| `GET` | `/websites/{id}` | Search website by id | `-` | `#/definitions/response.WebsiteDTO` |
