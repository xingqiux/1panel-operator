# SSH

- 接口数：`8`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/hosts/conffile/update` | Update host SSH setting by file | `#/definitions/dto.SSHConf` | `-` |
| `GET` | `/hosts/ssh/conf` | Load host SSH conf | `-` | `-` |
| `POST` | `/hosts/ssh/generate` | Generate host SSH secret | `#/definitions/dto.GenerateSSH` | `-` |
| `POST` | `/hosts/ssh/log` | Load host SSH logs | `#/definitions/dto.SearchSSHLog` | `#/definitions/dto.SSHLog` |
| `POST` | `/hosts/ssh/operate` | Operate SSH | `#/definitions/dto.Operate` | `-` |
| `POST` | `/hosts/ssh/search` | Load host SSH setting info | `-` | `#/definitions/dto.SSHInfo` |
| `POST` | `/hosts/ssh/secret` | Load host SSH secret | `#/definitions/dto.GenerateLoad` | `-` |
| `POST` | `/hosts/ssh/update` | Update host SSH setting | `#/definitions/dto.SSHUpdate` | `-` |
