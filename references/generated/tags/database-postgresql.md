# Database Postgresql

- 接口数：`9`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/databases/pg` | Create postgresql database | `#/definitions/dto.PostgresqlDBCreate` | `-` |
| `POST` | `/databases/pg/bind` | Bind postgresql user | `#/definitions/dto.PostgresqlBindUser` | `-` |
| `POST` | `/databases/pg/del` | Delete postgresql database | `#/definitions/dto.PostgresqlDBDelete` | `-` |
| `POST` | `/databases/pg/del/check` | Check before delete postgresql database | `#/definitions/dto.PostgresqlDBDeleteCheck` | `-` |
| `POST` | `/databases/pg/description` | Update postgresql database description | `#/definitions/dto.UpdateDescription` | `-` |
| `POST` | `/databases/pg/password` | Change postgresql password | `#/definitions/dto.ChangeDBInfo` | `-` |
| `POST` | `/databases/pg/privileges` | Change postgresql privileges | `#/definitions/dto.ChangeDBInfo` | `-` |
| `POST` | `/databases/pg/search` | Page postgresql databases | `#/definitions/dto.PostgresqlDBSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/databases/pg/{database}/load` | Load postgresql database from remote | `#/definitions/dto.PostgresqlLoadDB` | `-` |
