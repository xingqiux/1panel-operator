# Command

- 接口数：`6`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/hosts/command` | List commands | `-` | `#/definitions/dto.CommandInfo` |
| `POST` | `/hosts/command` | Create command | `#/definitions/dto.CommandOperate` | `-` |
| `POST` | `/hosts/command/del` | Delete command | `#/definitions/dto.BatchDeleteReq` | `-` |
| `POST` | `/hosts/command/search` | Page commands | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `GET` | `/hosts/command/tree` | Tree commands | `-` | `#/definitions/dto.CommandTree` |
| `POST` | `/hosts/command/update` | Update command | `#/definitions/dto.CommandOperate` | `-` |
