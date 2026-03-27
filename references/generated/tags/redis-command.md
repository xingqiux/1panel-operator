# Redis Command

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/hosts/command/redis` | List redis commands | `-` | `#/definitions/dto.RedisCommand` |
| `POST` | `/hosts/command/redis` | Save redis command | `#/definitions/dto.RedisCommand` | `-` |
| `POST` | `/hosts/command/redis/del` | Delete redis command | `#/definitions/dto.BatchDeleteReq` | `-` |
| `POST` | `/hosts/command/redis/search` | Page redis commands | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
