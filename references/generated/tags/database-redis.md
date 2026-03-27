# Database Redis

- 接口数：`7`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/databases/redis/conf` | Load redis conf | `#/definitions/dto.OperationWithName` | `#/definitions/dto.RedisConf` |
| `POST` | `/databases/redis/conf/update` | Update redis conf | `#/definitions/dto.RedisConfUpdate` | `-` |
| `POST` | `/databases/redis/install/cli` | Install redis-cli | `-` | `-` |
| `POST` | `/databases/redis/password` | Change redis password | `#/definitions/dto.ChangeRedisPass` | `-` |
| `POST` | `/databases/redis/persistence/conf` | Load redis persistence conf | `#/definitions/dto.OperationWithName` | `#/definitions/dto.RedisPersistence` |
| `POST` | `/databases/redis/persistence/update` | Update redis persistence conf | `#/definitions/dto.RedisConfPersistenceUpdate` | `-` |
| `POST` | `/databases/redis/status` | Load redis status info | `#/definitions/dto.OperationWithName` | `#/definitions/dto.RedisStatus` |
