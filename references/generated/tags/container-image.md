# Container Image

- 接口数：`10`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/containers/image` | load images options | `-` | `#/definitions/dto.Options` |
| `GET` | `/containers/image/all` | List all images | `-` | `#/definitions/dto.ImageInfo` |
| `POST` | `/containers/image/build` | Build image | `#/definitions/dto.ImageBuild` | `-` |
| `POST` | `/containers/image/load` | Load image | `#/definitions/dto.ImageLoad` | `-` |
| `POST` | `/containers/image/pull` | Pull image | `#/definitions/dto.ImagePull` | `-` |
| `POST` | `/containers/image/push` | Push image | `#/definitions/dto.ImagePush` | `-` |
| `POST` | `/containers/image/remove` | Delete image | `#/definitions/dto.BatchDelete` | `-` |
| `POST` | `/containers/image/save` | Save image | `#/definitions/dto.ImageSave` | `-` |
| `POST` | `/containers/image/search` | Page images | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/containers/image/tag` | Tag image | `#/definitions/dto.ImageTag` | `-` |
