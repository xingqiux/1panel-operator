# PHP Extensions

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/runtimes/php/extensions` | Create Extensions | `#/definitions/request.PHPExtensionsCreate` | `-` |
| `POST` | `/runtimes/php/extensions/del` | Delete Extensions | `#/definitions/request.PHPExtensionsDelete` | `-` |
| `POST` | `/runtimes/php/extensions/search` | Page Extensions | `#/definitions/request.PHPExtensionsSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/runtimes/php/extensions/update` | Update Extensions | `#/definitions/request.PHPExtensionsUpdate` | `-` |
