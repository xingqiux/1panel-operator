# Fail2ban

- 接口数：`7`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/toolbox/fail2ban/base` | Load fail2ban base info | `-` | `#/definitions/dto.Fail2BanBaseInfo` |
| `GET` | `/toolbox/fail2ban/load/conf` | Load fail2ban conf | `-` | `-` |
| `POST` | `/toolbox/fail2ban/operate` | Operate fail2ban | `#/definitions/dto.Operate` | `-` |
| `POST` | `/toolbox/fail2ban/operate/sshd` | Operate sshd of fail2ban | `#/definitions/dto.Operate` | `-` |
| `POST` | `/toolbox/fail2ban/search` | Page fail2ban ip list | `#/definitions/dto.Fail2BanSearch` | `-` |
| `POST` | `/toolbox/fail2ban/update` | Update fail2ban conf | `#/definitions/dto.Fail2BanUpdate` | `-` |
| `POST` | `/toolbox/fail2ban/update/byconf` | Update fail2ban conf by file | `#/definitions/dto.UpdateByFile` | `-` |
