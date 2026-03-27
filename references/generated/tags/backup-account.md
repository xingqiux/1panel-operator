# Backup Account

- 接口数：`17`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/settings/backup` | Create backup account | `#/definitions/dto.BackupOperate` | `-` |
| `POST` | `/settings/backup/backup` | Backup system data | `#/definitions/dto.CommonBackup` | `-` |
| `POST` | `/settings/backup/del` | Delete backup account | `#/definitions/dto.OperateByID` | `-` |
| `GET` | `/settings/backup/onedrive` | Load OneDrive info | `-` | `#/definitions/dto.OneDriveInfo` |
| `POST` | `/settings/backup/record/del` | Delete backup record | `#/definitions/dto.BatchDeleteReq` | `-` |
| `POST` | `/settings/backup/record/download` | Download backup record | `#/definitions/dto.DownloadRecord` | `-` |
| `POST` | `/settings/backup/record/search` | Page backup records | `#/definitions/dto.RecordSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/settings/backup/record/search/bycronjob` | Page backup records by cronjob | `#/definitions/dto.RecordSearchByCronjob` | `#/definitions/dto.PageResult` |
| `POST` | `/settings/backup/record/size` | Load backup records size | `#/definitions/dto.RecordSearch` | `#/definitions/dto.BackupFile` |
| `POST` | `/settings/backup/record/size/bycronjob` | Load backup records size for cronjob | `#/definitions/dto.RecordSearchByCronjob` | `#/definitions/dto.BackupFile` |
| `POST` | `/settings/backup/recover` | Recover system data | `#/definitions/dto.CommonRecover` | `-` |
| `POST` | `/settings/backup/recover/byupload` | Recover system data by upload | `#/definitions/dto.CommonRecover` | `-` |
| `POST` | `/settings/backup/refresh/onedrive` | Refresh OneDrive token | `-` | `-` |
| `GET` | `/settings/backup/search` | List backup accounts | `-` | `#/definitions/dto.BackupInfo` |
| `POST` | `/settings/backup/search` | List buckets | `#/definitions/dto.ForBuckets` | `-` |
| `POST` | `/settings/backup/search/files` | List files from backup accounts | `#/definitions/dto.BackupSearchFile` | `-` |
| `POST` | `/settings/backup/update` | Update backup account | `#/definitions/dto.BackupOperate` | `-` |
