# Website Domain

- 接口数：`3`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/domains` | Create website domain | `#/definitions/request.WebsiteDomainCreate` | `#/definitions/model.WebsiteDomain` |
| `POST` | `/websites/domains/del` | Delete website domain | `#/definitions/request.WebsiteDomainDelete` | `-` |
| `GET` | `/websites/domains/{websiteId}` | Search website domains by websiteId | `-` | `#/definitions/model.WebsiteDomain` |
