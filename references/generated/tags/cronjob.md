# Cronjob

- 接口数：`10`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/cronjobs` | Create cronjob | `#/definitions/dto.CronjobCreate` | `-` |
| `POST` | `/cronjobs/del` | Delete cronjob | `#/definitions/dto.CronjobBatchDelete` | `-` |
| `POST` | `/cronjobs/download` | Download cronjob records | `#/definitions/dto.CronjobDownload` | `-` |
| `POST` | `/cronjobs/handle` | Handle cronjob once | `#/definitions/dto.OperateByID` | `-` |
| `POST` | `/cronjobs/records/clean` | Clean job records | `#/definitions/dto.CronjobClean` | `-` |
| `POST` | `/cronjobs/records/log` | Load Cronjob record log | `#/definitions/dto.OperateByID` | `-` |
| `POST` | `/cronjobs/search` | Page cronjobs | `#/definitions/dto.PageCronjob` | `#/definitions/dto.PageResult` |
| `POST` | `/cronjobs/search/records` | Page job records | `#/definitions/dto.SearchRecord` | `#/definitions/dto.PageResult` |
| `POST` | `/cronjobs/status` | Update cronjob status | `#/definitions/dto.CronjobUpdateStatus` | `-` |
| `POST` | `/cronjobs/update` | Update cronjob | `#/definitions/dto.CronjobUpdate` | `-` |
