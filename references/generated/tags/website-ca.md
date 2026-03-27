# Website CA

- 接口数：`7`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/ca` | Create website ca | `#/definitions/request.WebsiteCACreate` | `#/definitions/request.WebsiteCACreate` |
| `POST` | `/websites/ca/del` | Delete website ca | `#/definitions/request.WebsiteCommonReq` | `-` |
| `POST` | `/websites/ca/download` | Download CA file | `#/definitions/request.WebsiteResourceReq` | `-` |
| `POST` | `/websites/ca/obtain` | Obtain SSL | `#/definitions/request.WebsiteCAObtain` | `-` |
| `POST` | `/websites/ca/renew` | Renew Obtain SSL | `#/definitions/request.WebsiteCAObtain` | `-` |
| `POST` | `/websites/ca/search` | Page website ca | `#/definitions/request.WebsiteCASearch` | `#/definitions/dto.PageResult` |
| `GET` | `/websites/ca/{id}` | Get website ca | `-` | `#/definitions/response.WebsiteCADTO` |
