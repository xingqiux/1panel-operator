# Monitor

- 接口数：`2`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/hosts/monitor/clean` | Clean monitor datas | `-` | `-` |
| `POST` | `/hosts/monitor/search` | Load monitor datas | `#/definitions/dto.MonitorSearch` | `#/definitions/dto.MonitorData` |
