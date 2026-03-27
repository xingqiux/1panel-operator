# Runtime

- 接口数：`9`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/runtimes` | Create runtime | `#/definitions/request.RuntimeCreate` | `#/definitions/model.Runtime` |
| `POST` | `/runtimes/node/modules` | Get Node modules | `#/definitions/request.NodeModuleReq` | `#/definitions/response.NodeModule` |
| `POST` | `/runtimes/node/modules/operate` | Operate Node modules | `#/definitions/request.NodeModuleReq` | `-` |
| `POST` | `/runtimes/node/package` | Get Node package scripts | `#/definitions/request.NodePackageReq` | `#/definitions/response.PackageScripts` |
| `POST` | `/runtimes/operate` | Operate runtime | `#/definitions/request.RuntimeOperate` | `-` |
| `POST` | `/runtimes/search` | List runtimes | `#/definitions/request.RuntimeSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/runtimes/sync` | Sync runtime status | `-` | `-` |
| `POST` | `/runtimes/update` | Update runtime | `#/definitions/request.RuntimeUpdate` | `-` |
| `GET` | `/runtimes/{id}` | Get runtime | `-` | `#/definitions/response.RuntimeDTO` |
