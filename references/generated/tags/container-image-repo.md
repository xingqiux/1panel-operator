# Container Image-repo

- 接口数：`6`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/containers/repo` | List image repos | `-` | `#/definitions/dto.ImageRepoOption` |
| `POST` | `/containers/repo` | Create image repo | `#/definitions/dto.ImageRepoDelete` | `-` |
| `POST` | `/containers/repo/del` | Delete image repo | `#/definitions/dto.ImageRepoDelete` | `-` |
| `POST` | `/containers/repo/search` | Page image repos | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `GET` | `/containers/repo/status` | Load repo status | `#/definitions/dto.OperateByID` | `-` |
| `POST` | `/containers/repo/update` | Update image repo | `#/definitions/dto.ImageRepoUpdate` | `-` |
