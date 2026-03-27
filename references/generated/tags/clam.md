# Clam

- 接口数：`13`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/toolbox/clam` | Create clam | `#/definitions/dto.ClamCreate` | `-` |
| `GET` | `/toolbox/clam/base` | Load clam base info | `-` | `#/definitions/dto.ClamBaseInfo` |
| `POST` | `/toolbox/clam/del` | Delete clam | `#/definitions/dto.ClamDelete` | `-` |
| `POST` | `/toolbox/clam/file/search` | Load clam file | `#/definitions/dto.ClamFileReq` | `-` |
| `POST` | `/toolbox/clam/file/update` | Update clam file | `#/definitions/dto.UpdateByNameAndFile` | `-` |
| `POST` | `/toolbox/clam/handle` | Handle clam scan | `#/definitions/dto.OperateByID` | `-` |
| `POST` | `/toolbox/clam/operate` | Operate Clam | `#/definitions/dto.Operate` | `-` |
| `POST` | `/toolbox/clam/record/clean` | Clean clam record | `#/definitions/dto.OperateByID` | `-` |
| `POST` | `/toolbox/clam/record/log` | Load clam record detail | `#/definitions/dto.ClamLogReq` | `-` |
| `POST` | `/toolbox/clam/record/search` | Page clam record | `#/definitions/dto.ClamLogSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/toolbox/clam/search` | Page clam | `#/definitions/dto.SearchClamWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/toolbox/clam/status/update` | Update clam status | `#/definitions/dto.ClamUpdateStatus` | `-` |
| `POST` | `/toolbox/clam/update` | Update clam | `#/definitions/dto.ClamUpdate` | `-` |
