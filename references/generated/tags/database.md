# Database

- 接口数：`9`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/databases/db` | Create database | `#/definitions/dto.DatabaseCreate` | `-` |
| `POST` | `/databases/db/check` | Check database | `#/definitions/dto.DatabaseCreate` | `-` |
| `POST` | `/databases/db/del` | Delete database | `#/definitions/dto.DatabaseDelete` | `-` |
| `GET` | `/databases/db/item/{type}` | Retrieve database list based on type | `-` | `#/definitions/dto.DatabaseItem` |
| `GET` | `/databases/db/list/{type}` | List databases | `-` | `#/definitions/dto.DatabaseOption` |
| `POST` | `/databases/db/search` | Page databases | `#/definitions/dto.DatabaseSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/databases/db/update` | Update database | `#/definitions/dto.DatabaseUpdate` | `-` |
| `GET` | `/databases/db/{name}` | Get databases | `-` | `#/definitions/dto.DatabaseInfo` |
| `POST` | `/db/remote/del/check` | Check before delete remote database | `#/definitions/dto.OperateByID` | `-` |
