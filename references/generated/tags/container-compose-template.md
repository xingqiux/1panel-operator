# Container Compose-template

- 接口数：`5`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/containers/template` | List compose templates | `-` | `#/definitions/dto.ComposeTemplateInfo` |
| `POST` | `/containers/template` | Create compose template | `#/definitions/dto.ComposeTemplateCreate` | `-` |
| `POST` | `/containers/template/del` | Delete compose template | `#/definitions/dto.BatchDelete` | `-` |
| `POST` | `/containers/template/search` | Page compose templates | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/containers/template/update` | Update compose template | `#/definitions/dto.ComposeTemplateUpdate` | `-` |
