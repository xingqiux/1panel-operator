# Website Acme

- 接口数：`3`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/websites/acme` | Create website acme account | `#/definitions/request.WebsiteAcmeAccountCreate` | `#/definitions/response.WebsiteAcmeAccountDTO` |
| `POST` | `/websites/acme/del` | Delete website acme account | `#/definitions/request.WebsiteResourceReq` | `-` |
| `POST` | `/websites/acme/search` | Page website acme accounts | `#/definitions/dto.PageInfo` | `#/definitions/dto.PageResult` |
