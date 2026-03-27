# Website DNS

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/dns` | Create website dns account | `#/definitions/request.WebsiteDnsAccountCreate` | `-` |
| `POST` | `/websites/dns/del` | Delete website dns account | `#/definitions/request.WebsiteResourceReq` | `-` |
| `POST` | `/websites/dns/search` | Page website dns accounts | `#/definitions/dto.PageInfo` | `#/definitions/dto.PageResult` |
| `POST` | `/websites/dns/update` | Update website dns account | `#/definitions/request.WebsiteDnsAccountUpdate` | `-` |
