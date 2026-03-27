# Container Docker

- 接口数：`8`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/containers/daemonjson` | Load docker daemon.json | `-` | `#/definitions/dto.DaemonJsonConf` |
| `GET` | `/containers/daemonjson/file` | Load docker daemon.json | `-` | `-` |
| `POST` | `/containers/daemonjson/update` | Update docker daemon.json | `#/definitions/dto.SettingUpdate` | `-` |
| `POST` | `/containers/daemonjson/update/byfile` | Update docker daemon.json by upload file | `#/definitions/dto.DaemonJsonUpdateByFile` | `-` |
| `POST` | `/containers/docker/operate` | Operate docker | `#/definitions/dto.DockerOperation` | `-` |
| `GET` | `/containers/docker/status` | Load docker status | `-` | `-` |
| `POST` | `/containers/ipv6option/update` | Update docker daemon.json ipv6 option | `#/definitions/dto.LogOption` | `-` |
| `POST` | `/containers/logoption/update` | Update docker daemon.json log option | `#/definitions/dto.LogOption` | `-` |
