# Container Volume

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/containers/volume` | List Container Volumes | `-` | `#/definitions/dto.Options` |
| `POST` | `/containers/volume` | Create Container Volume | `#/definitions/dto.VolumeCreate` | `-` |
| `POST` | `/containers/volume/del` | Delete Container Volume | `#/definitions/dto.BatchDelete` | `-` |
| `POST` | `/containers/volume/search` | Page Container Volumes | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
