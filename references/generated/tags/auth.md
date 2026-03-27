# Auth

- 接口数：`7`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `GET` | `/auth/captcha` | Load captcha | `-` | `#/definitions/dto.CaptchaResponse` |
| `GET` | `/auth/demo` | Check System isDemo | `-` | `-` |
| `GET` | `/auth/intl` | Check System isIntl | `-` | `-` |
| `GET` | `/auth/language` | Load System Language | `-` | `-` |
| `POST` | `/auth/login` | User login | `#/definitions/dto.Login` | `#/definitions/dto.UserLoginInfo` |
| `POST` | `/auth/logout` | User logout | `-` | `-` |
| `POST` | `/auth/mfalogin` | User login with mfa | `#/definitions/dto.MFALogin` | `#/definitions/dto.UserLoginInfo` |
