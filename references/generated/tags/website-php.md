# Website PHP

- 接口数：`3`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/php/config` | Update website php conf | `#/definitions/request.WebsitePHPConfigUpdate` | `-` |
| `POST` | `/websites/php/update` | Update php conf | `#/definitions/request.WebsitePHPFileUpdate` | `-` |
| `POST` | `/websites/php/version` | Update php version | `#/definitions/request.WebsitePHPVersionReq` | `-` |
