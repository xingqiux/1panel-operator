# Database Mysql

- 接口数：`14`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/databases` | Create mysql database | `#/definitions/dto.MysqlDBCreate` | `-` |
| `POST` | `/databases/bind` | Bind user of mysql database | `#/definitions/dto.BindUser` | `-` |
| `POST` | `/databases/change/access` | Change mysql access | `#/definitions/dto.ChangeDBInfo` | `-` |
| `POST` | `/databases/change/password` | Change mysql password | `#/definitions/dto.ChangeDBInfo` | `-` |
| `POST` | `/databases/del` | Delete mysql database | `#/definitions/dto.MysqlDBDelete` | `-` |
| `POST` | `/databases/del/check` | Check before delete mysql database | `#/definitions/dto.MysqlDBDeleteCheck` | `-` |
| `POST` | `/databases/description/update` | Update mysql database description | `#/definitions/dto.UpdateDescription` | `-` |
| `POST` | `/databases/load` | Load mysql database from remote | `#/definitions/dto.MysqlLoadDB` | `-` |
| `GET` | `/databases/options` | List mysql database names | `#/definitions/dto.PageInfo` | `#/definitions/dto.MysqlOption` |
| `POST` | `/databases/remote` | Load mysql remote access | `#/definitions/dto.OperationWithNameAndType` | `-` |
| `POST` | `/databases/search` | Page mysql databases | `#/definitions/dto.MysqlDBSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/databases/status` | Load mysql status info | `#/definitions/dto.OperationWithNameAndType` | `#/definitions/dto.MysqlStatus` |
| `POST` | `/databases/variables` | Load mysql variables info | `#/definitions/dto.OperationWithNameAndType` | `#/definitions/dto.MysqlVariables` |
| `POST` | `/databases/variables/update` | Update mysql variables | `#/definitions/dto.MysqlVariablesUpdate` | `-` |
