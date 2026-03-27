# App

- 接口数：`23`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/apps/checkupdate` | Get app list update | `-` | `#/definitions/response.AppUpdateRes` |
| `GET` | `/apps/detail/{appId}/{version}/{type}` | Search app detail by appid | `-` | `#/definitions/response.AppDetailDTO` |
| `GET` | `/apps/details/{id}` | Get app detail by id | `-` | `#/definitions/response.AppDetailDTO` |
| `GET` | `/apps/ignored` | Get Ignore App | `-` | `#/definitions/response.IgnoredApp` |
| `POST` | `/apps/install` | Install app | `#/definitions/request.AppInstallCreate` | `#/definitions/model.AppInstall` |
| `POST` | `/apps/installed/check` | Check app installed | `#/definitions/request.AppInstalledInfo` | `#/definitions/response.AppInstalledCheck` |
| `POST` | `/apps/installed/conf` | Search default config by key | `#/definitions/dto.OperationWithNameAndType` | `-` |
| `GET` | `/apps/installed/conninfo/{key}` | Search app password by key | `#/definitions/dto.OperationWithNameAndType` | `#/definitions/response.DatabaseConn` |
| `GET` | `/apps/installed/delete/check/{appInstallId}` | Check before delete | `-` | `#/definitions/dto.AppResource` |
| `POST` | `/apps/installed/ignore` | ignore App Update | `#/definitions/request.AppInstalledIgnoreUpgrade` | `-` |
| `GET` | `/apps/installed/list` | List app installed | `-` | `#/definitions/dto.AppInstallInfo` |
| `POST` | `/apps/installed/loadport` | Search app port by key | `#/definitions/dto.OperationWithNameAndType` | `-` |
| `POST` | `/apps/installed/op` | Operate installed app | `#/definitions/request.AppInstalledOperate` | `-` |
| `POST` | `/apps/installed/params/update` | Change app params | `#/definitions/request.AppInstalledUpdate` | `-` |
| `GET` | `/apps/installed/params/{appInstallId}` | Search params by appInstallId | `-` | `#/definitions/response.AppConfig` |
| `POST` | `/apps/installed/port/change` | Change app port | `#/definitions/request.PortUpdate` | `-` |
| `POST` | `/apps/installed/search` | Page app installed | `#/definitions/request.AppInstalledSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/apps/installed/sync` | Sync app installed | `-` | `-` |
| `POST` | `/apps/installed/update/versions` | Search app update version by install id | `-` | `#/definitions/dto.AppVersion` |
| `POST` | `/apps/search` | List apps | `#/definitions/request.AppSearch` | `#/definitions/response.AppRes` |
| `GET` | `/apps/services/{key}` | Search app service by key | `-` | `#/definitions/response.AppService` |
| `POST` | `/apps/sync` | Sync app list | `-` | `-` |
| `GET` | `/apps/{key}` | Search app by key | `-` | `#/definitions/response.AppDTO` |
