# Container Network

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/containers/network` | List networks | `-` | `#/definitions/dto.Options` |
| `POST` | `/containers/network` | Create network | `#/definitions/dto.NetworkCreate` | `-` |
| `POST` | `/containers/network/del` | Delete network | `#/definitions/dto.BatchDelete` | `-` |
| `POST` | `/containers/network/search` | Page networks | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
