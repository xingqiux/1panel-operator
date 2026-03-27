# Logs

- 接口数：`5`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/logs/clean` | Clean operation logs | `#/definitions/dto.CleanLog` | `-` |
| `POST` | `/logs/login` | Page login logs | `#/definitions/dto.SearchLgLogWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/logs/operation` | Page operation logs | `#/definitions/dto.SearchOpLogWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/logs/system` | Load system logs | `-` | `-` |
| `GET` | `/logs/system/files` | Load system log files | `-` | `-` |
