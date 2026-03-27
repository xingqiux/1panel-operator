# Device

- 接口数：`11`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/toolbox/clean` | Clean system | `-` | `-` |
| `POST` | `/toolbox/device/base` | Load device base info | `-` | `#/definitions/dto.DeviceBaseInfo` |
| `POST` | `/toolbox/device/check/dns` | Check device DNS conf | `#/definitions/dto.SettingUpdate` | `-` |
| `POST` | `/toolbox/device/conf` | load conf | `#/definitions/dto.OperationWithName` | `-` |
| `POST` | `/toolbox/device/update/byconf` | Update device conf by file | `#/definitions/dto.UpdateByNameAndFile` | `-` |
| `POST` | `/toolbox/device/update/conf` | Update device | `#/definitions/dto.SettingUpdate` | `-` |
| `POST` | `/toolbox/device/update/host` | Update device hosts | `-` | `-` |
| `POST` | `/toolbox/device/update/passwd` | Update device passwd | `#/definitions/dto.ChangePasswd` | `-` |
| `POST` | `/toolbox/device/update/swap` | Update device swap | `#/definitions/dto.SwapHelper` | `-` |
| `GET` | `/toolbox/device/zone/options` | list time zone options | `-` | `-` |
| `POST` | `/toolbox/scan` | Scan system | `-` | `#/definitions/dto.CleanData` |
