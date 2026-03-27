# Host

- 接口数：`8`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/hosts` | Create host | `#/definitions/dto.HostOperate` | `#/definitions/dto.HostInfo` |
| `POST` | `/hosts/del` | Delete host | `#/definitions/dto.BatchDeleteReq` | `-` |
| `POST` | `/hosts/search` | Page host | `#/definitions/dto.SearchHostWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/hosts/test/byid/{id}` | Test host conn by host id | `-` | `-` |
| `POST` | `/hosts/test/byinfo` | Test host conn by info | `#/definitions/dto.HostConnTest` | `-` |
| `POST` | `/hosts/tree` | Load host tree | `#/definitions/dto.SearchForTree` | `#/definitions/dto.HostTree` |
| `POST` | `/hosts/update` | Update host | `#/definitions/dto.HostOperate` | `-` |
| `POST` | `/hosts/update/group` | Update host group | `#/definitions/dto.ChangeHostGroup` | `-` |
