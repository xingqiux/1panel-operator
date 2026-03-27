# Firewall

- 接口数：`10`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/hosts/firewall/base` | Load firewall base info | `-` | `#/definitions/dto.FirewallBaseInfo` |
| `POST` | `/hosts/firewall/batch` | Batch create group | `#/definitions/dto.BatchRuleOperate` | `-` |
| `POST` | `/hosts/firewall/forward` | Update firewall port group | `#/definitions/dto.ForwardRuleOperate` | `-` |
| `POST` | `/hosts/firewall/ip` | Create firewall group | `#/definitions/dto.AddrRuleOperate` | `-` |
| `POST` | `/hosts/firewall/operate` | Page firewall status | `#/definitions/dto.FirewallOperation` | `-` |
| `POST` | `/hosts/firewall/port` | Create firewall port group | `#/definitions/dto.PortRuleOperate` | `-` |
| `POST` | `/hosts/firewall/search` | Page firewall rules | `#/definitions/dto.RuleSearch` | `#/definitions/dto.PageResult` |
| `POST` | `/hosts/firewall/update/addr` | Update address group | `#/definitions/dto.AddrRuleUpdate` | `-` |
| `POST` | `/hosts/firewall/update/description` | Update rule description | `#/definitions/dto.UpdateFirewallDescription` | `-` |
| `POST` | `/hosts/firewall/update/port` | Update firewall group | `#/definitions/dto.PortRuleUpdate` | `-` |
