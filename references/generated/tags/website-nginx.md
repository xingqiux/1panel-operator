# Website Nginx

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/config` | Load nginx conf | `#/definitions/request.NginxScopeReq` | `#/definitions/response.WebsiteNginxConfig` |
| `POST` | `/websites/config/update` | Update nginx conf | `#/definitions/request.NginxConfigUpdate` | `-` |
| `POST` | `/websites/nginx/update` | Update website nginx conf | `#/definitions/request.WebsiteNginxUpdate` | `-` |
| `GET` | `/websites/{id}/config/{type}` | Search website nginx by id | `-` | `#/definitions/response.FileInfo` |
