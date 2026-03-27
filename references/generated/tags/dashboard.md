# Dashboard

- 接口数：`4`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/dashboard/base/os` | Load os info | `-` | `#/definitions/dto.OsInfo` |
| `GET` | `/dashboard/base/{ioOption}/{netOption}` | Load dashboard base info | `-` | `#/definitions/dto.DashboardBase` |
| `POST` | `/dashboard/current` | Load dashboard current info | `#/definitions/dto.DashboardReq` | `#/definitions/dto.DashboardCurrent` |
| `POST` | `/dashboard/system/restart/{operation}` | System restart panel | `-` | `-` |
