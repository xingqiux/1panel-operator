# Website HTTPS

- 接口数：`2`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/websites/{id}/https` | Load https conf | `-` | `#/definitions/response.WebsiteHTTPS` |
| `POST` | `/websites/{id}/https` | Update https conf | `#/definitions/request.WebsiteHTTPSOp` | `#/definitions/response.WebsiteHTTPS` |
