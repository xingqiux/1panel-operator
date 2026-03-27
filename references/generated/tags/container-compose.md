# Container Compose

- 接口数：`6`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/containers/compose` | Create compose | `#/definitions/dto.ComposeCreate` | `-` |
| `POST` | `/containers/compose/operate` | Operate compose | `#/definitions/dto.ComposeOperation` | `-` |
| `POST` | `/containers/compose/search` | Page composes | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `GET` | `/containers/compose/search/log` | Container Compose logs | `-` | `-` |
| `POST` | `/containers/compose/test` | Test compose | `#/definitions/dto.ComposeCreate` | `-` |
| `POST` | `/containers/compose/update` | Update Container Compose | `#/definitions/dto.ComposeUpdate` | `-` |
