# Database Common

- 接口数：`3`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/databases/common/info` | Load base info | `#/definitions/dto.OperationWithNameAndType` | `#/definitions/dto.DBBaseInfo` |
| `POST` | `/databases/common/load/file` | Load Database conf | `#/definitions/dto.OperationWithNameAndType` | `-` |
| `POST` | `/databases/common/update/conf` | Update conf by upload file | `#/definitions/dto.DBConfUpdateByFile` | `-` |
