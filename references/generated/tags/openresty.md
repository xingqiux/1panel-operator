# OpenResty

- 接口数：`6`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/openresty` | Load OpenResty conf | `-` | `#/definitions/response.NginxFile` |
| `POST` | `/openresty/clear` | Clear OpenResty proxy cache | `-` | `-` |
| `POST` | `/openresty/file` | Update OpenResty conf by upload file | `#/definitions/request.NginxConfigFileUpdate` | `-` |
| `POST` | `/openresty/scope` | Load partial OpenResty conf | `#/definitions/request.NginxScopeReq` | `#/definitions/response.NginxParam` |
| `GET` | `/openresty/status` | Load OpenResty status info | `-` | `#/definitions/response.NginxStatus` |
| `POST` | `/openresty/update` | Update OpenResty conf | `#/definitions/request.NginxConfigUpdate` | `-` |
