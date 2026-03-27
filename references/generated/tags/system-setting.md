# System Setting

- 接口数：`29`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/settings/api/config/generate/key` | Generate api key | `-` | `-` |
| `POST` | `/settings/api/config/update` | Update api config | `#/definitions/dto.ApiInterfaceConfig` | `-` |
| `GET` | `/settings/basedir` | Load local base dir | `-` | `-` |
| `POST` | `/settings/bind/update` | Update system bind info | `#/definitions/dto.BindInfo` | `-` |
| `POST` | `/settings/expired/handle` | Reset system password expired | `#/definitions/dto.PasswordUpdate` | `-` |
| `GET` | `/settings/interface` | Load system address | `-` | `-` |
| `POST` | `/settings/menu/update` | Update system setting | `#/definitions/dto.SettingUpdate` | `-` |
| `POST` | `/settings/mfa` | Load mfa info | `#/definitions/dto.MfaCredential` | `#/definitions/mfa.Otp` |
| `POST` | `/settings/mfa/bind` | Bind mfa | `#/definitions/dto.MfaCredential` | `-` |
| `POST` | `/settings/password/update` | Update system password | `#/definitions/dto.PasswordUpdate` | `-` |
| `POST` | `/settings/port/update` | Update system port | `#/definitions/dto.PortUpdate` | `-` |
| `POST` | `/settings/proxy/update` | Update proxy setting | `#/definitions/dto.ProxyUpdate` | `-` |
| `POST` | `/settings/search` | Load system setting info | `-` | `#/definitions/dto.SettingInfo` |
| `GET` | `/settings/search/available` | Load system available status | `-` | `-` |
| `POST` | `/settings/snapshot` | Create system snapshot | `#/definitions/dto.SnapshotCreate` | `-` |
| `POST` | `/settings/snapshot/del` | Delete system backup | `#/definitions/dto.SnapshotBatchDelete` | `-` |
| `POST` | `/settings/snapshot/description/update` | Update snapshot description | `#/definitions/dto.UpdateDescription` | `-` |
| `POST` | `/settings/snapshot/import` | Import system snapshot | `#/definitions/dto.SnapshotImport` | `-` |
| `POST` | `/settings/snapshot/recover` | Recover system backup | `#/definitions/dto.SnapshotRecover` | `-` |
| `POST` | `/settings/snapshot/rollback` | Rollback system backup | `#/definitions/dto.SnapshotRecover` | `-` |
| `POST` | `/settings/snapshot/search` | Page system snapshot | `#/definitions/dto.PageSnapshot` | `#/definitions/dto.PageResult` |
| `POST` | `/settings/snapshot/size` | Load system snapshot size | `#/definitions/dto.PageSnapshot` | `#/definitions/dto.SnapshotFile` |
| `POST` | `/settings/snapshot/status` | Load Snapshot status | `#/definitions/dto.OperateByID` | `#/definitions/dto.SnapshotStatus` |
| `POST` | `/settings/ssl/download` | Download system cert | `-` | `-` |
| `GET` | `/settings/ssl/info` | Load system cert info | `-` | `#/definitions/dto.SSLInfo` |
| `POST` | `/settings/ssl/update` | Update system ssl | `#/definitions/dto.SSLUpdate` | `-` |
| `POST` | `/settings/update` | Update system setting | `#/definitions/dto.SettingUpdate` | `-` |
| `GET` | `/settings/upgrade` | Load release notes by version | `#/definitions/dto.Upgrade` | `-` |
| `POST` | `/settings/upgrade` | Upgrade | `#/definitions/dto.Upgrade` | `-` |
