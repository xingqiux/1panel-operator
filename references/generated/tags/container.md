# Container

- 接口数：`16`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/containers` | Create container | `#/definitions/dto.ContainerOperate` | `-` |
| `POST` | `/containers/clean/log` | Clean container log | `#/definitions/dto.OperationWithName` | `-` |
| `POST` | `/containers/commit` | Commit Container | `#/definitions/dto.ContainerCommit` | `-` |
| `POST` | `/containers/download/log` | Download Container logs | `#/definitions/dto.ContainerLog` | `-` |
| `POST` | `/containers/info` | Load container info | `#/definitions/dto.OperationWithName` | `#/definitions/dto.ContainerOperate` |
| `POST` | `/containers/inspect` | Container inspect | `#/definitions/dto.InspectReq` | `-` |
| `POST` | `/containers/list` | List containers | `-` | `-` |
| `POST` | `/containers/load/log` | Load container log | `#/definitions/dto.OperationWithNameAndType` | `-` |
| `POST` | `/containers/operate` | Operate Container | `#/definitions/dto.ContainerOperation` | `-` |
| `POST` | `/containers/prune` | Clean container | `#/definitions/dto.ContainerPrune` | `#/definitions/dto.ContainerPruneReport` |
| `POST` | `/containers/rename` | Rename Container | `#/definitions/dto.ContainerRename` | `-` |
| `POST` | `/containers/search` | Page containers | `#/definitions/dto.PageContainer` | `#/definitions/dto.PageResult` |
| `POST` | `/containers/search/log` | Container logs | `-` | `-` |
| `GET` | `/containers/stats/{id}` | Container stats | `-` | `#/definitions/dto.ContainerStats` |
| `POST` | `/containers/update` | Update container | `#/definitions/dto.ContainerOperate` | `-` |
| `POST` | `/containers/upgrade` | Upgrade container | `#/definitions/dto.ContainerUpgrade` | `-` |
