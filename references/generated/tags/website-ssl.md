# Website SSL

- 接口数：`10`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/ssl` | Create website ssl | `#/definitions/request.WebsiteSSLCreate` | `#/definitions/request.WebsiteSSLCreate` |
| `POST` | `/websites/ssl/del` | Delete website ssl | `#/definitions/request.WebsiteBatchDelReq` | `-` |
| `POST` | `/websites/ssl/download` | Download SSL file | `#/definitions/request.WebsiteResourceReq` | `-` |
| `POST` | `/websites/ssl/obtain` | Apply  ssl | `#/definitions/request.WebsiteSSLApply` | `-` |
| `POST` | `/websites/ssl/resolve` | Resolve website ssl | `#/definitions/request.WebsiteDNSReq` | `#/definitions/response.WebsiteDNSRes` |
| `POST` | `/websites/ssl/search` | Page website ssl | `#/definitions/request.WebsiteSSLSearch` | `#/definitions/response.WebsiteSSLDTO` |
| `POST` | `/websites/ssl/update` | Update Website ssl | `#/definitions/request.WebsiteSSLUpdate` | `-` |
| `POST` | `/websites/ssl/upload` | Upload Website ssl | `#/definitions/request.WebsiteSSLUpload` | `-` |
| `GET` | `/websites/ssl/website/{websiteId}` | Search website ssl by website id | `-` | `#/definitions/response.WebsiteSSLDTO` |
| `GET` | `/websites/ssl/{id}` | Search website ssl by id | `-` | `#/definitions/response.WebsiteSSLDTO` |
