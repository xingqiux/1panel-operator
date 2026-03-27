# System Group

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/groups` | Create system group | `#/definitions/dto.GroupCreate` | `-` |
| `POST` | `/groups/del` | Delete system group | `#/definitions/dto.OperateByID` | `-` |
| `POST` | `/groups/search` | List system groups | `#/definitions/dto.GroupSearch` | `#/definitions/dto.GroupInfo` |
| `POST` | `/groups/update` | Update system group | `#/definitions/dto.GroupUpdate` | `-` |
