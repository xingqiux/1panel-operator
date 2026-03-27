# FTP

- 接口数：`8`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/toolbox/ftp` | Create FTP user | `#/definitions/dto.FtpCreate` | `-` |
| `GET` | `/toolbox/ftp/base` | Load FTP base info | `-` | `#/definitions/dto.FtpBaseInfo` |
| `POST` | `/toolbox/ftp/del` | Delete FTP user | `#/definitions/dto.BatchDeleteReq` | `-` |
| `POST` | `/toolbox/ftp/log/search` | Load FTP operation log | `#/definitions/dto.FtpLogSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/toolbox/ftp/operate` | Operate FTP | `#/definitions/dto.Operate` | `-` |
| `POST` | `/toolbox/ftp/search` | Page FTP user | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/toolbox/ftp/sync` | Sync FTP user | `#/definitions/dto.BatchDeleteReq` | `-` |
| `POST` | `/toolbox/ftp/update` | Update FTP user | `#/definitions/dto.FtpUpdate` | `-` |
