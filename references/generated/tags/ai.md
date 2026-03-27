# AI

- 接口数：`10`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/ai/domain/bind` | Bind domain | `#/definitions/dto.OllamaBindDomain` | `-` |
| `POST` | `/ai/domain/get` | Get bind domain | `#/definitions/dto.OllamaBindDomainReq` | `#/definitions/dto.OllamaBindDomainRes` |
| `GET` | `/ai/gpu/load` | Load gpu / xpu info | `-` | `-` |
| `POST` | `/ai/ollama/model` | Create Ollama model | `#/definitions/dto.OllamaModelName` | `-` |
| `POST` | `/ai/ollama/model/close` | Close Ollama model conn | `#/definitions/dto.OllamaModelName` | `-` |
| `POST` | `/ai/ollama/model/del` | Delete Ollama model | `#/definitions/dto.ForceDelete` | `-` |
| `POST` | `/ai/ollama/model/load` | Page Ollama models | `#/definitions/dto.OllamaModelName` | `-` |
| `POST` | `/ai/ollama/model/recreate` | Rereate Ollama model | `#/definitions/dto.OllamaModelName` | `-` |
| `POST` | `/ai/ollama/model/search` | Page Ollama models | `#/definitions/dto.SearchWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/ai/ollama/model/sync` | Sync Ollama model list | `-` | `#/definitions/dto.OllamaModelDropList` |
