# Host tool

- 接口数：`8`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/hosts/tool` | Get tool status | `#/definitions/request.HostToolReq` | `#/definitions/response.HostToolRes` |
| `POST` | `/hosts/tool/config` | Get tool config | `#/definitions/request.HostToolConfig` | `#/definitions/response.HostToolConfig` |
| `POST` | `/hosts/tool/create` | Create Host tool Config | `#/definitions/request.HostToolCreate` | `-` |
| `POST` | `/hosts/tool/log` | Get tool logs | `#/definitions/request.HostToolLogReq` | `-` |
| `POST` | `/hosts/tool/operate` | Operate tool | `#/definitions/request.HostToolReq` | `-` |
| `GET` | `/hosts/tool/supervisor/process` | Get Supervisor process config | `-` | `#/definitions/response.SupervisorProcessConfig` |
| `POST` | `/hosts/tool/supervisor/process` | Create Supervisor process | `#/definitions/request.SupervisorProcessConfig` | `-` |
| `POST` | `/hosts/tool/supervisor/process/file` | Get Supervisor process config | `#/definitions/request.SupervisorProcessFileReq` | `-` |
