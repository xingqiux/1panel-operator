# File

- 接口数：`31`

| Method | Path | Summary | Body Schema | Response Schema |
| --- | --- | --- | --- | --- |
| `POST` | `/files` | Create file | `#/definitions/request.FileCreate` | `-` |
| `POST` | `/files/batch/check` | Batch check file exist | `#/definitions/request.FilePathsCheck` | `#/definitions/response.ExistFileInfo` |
| `POST` | `/files/batch/del` | Batch delete file | `#/definitions/request.FileBatchDelete` | `-` |
| `POST` | `/files/batch/role` | Batch change file mode and owner | `#/definitions/request.FileRoleReq` | `-` |
| `POST` | `/files/check` | Check file exist | `#/definitions/request.FilePathCheck` | `-` |
| `POST` | `/files/chunkdownload` | Chunk Download file | `#/definitions/request.FileDownload` | `-` |
| `POST` | `/files/chunkupload` | Chunk upload file | `-` | `-` |
| `POST` | `/files/compress` | Compress file | `#/definitions/request.FileCompress` | `-` |
| `POST` | `/files/content` | Load file content | `#/definitions/request.FileContentReq` | `#/definitions/response.FileInfo` |
| `POST` | `/files/decompress` | Decompress file | `#/definitions/request.FileDeCompress` | `-` |
| `POST` | `/files/del` | Delete file | `#/definitions/request.FileDelete` | `-` |
| `GET` | `/files/download` | Download file | `-` | `-` |
| `POST` | `/files/favorite` | Create favorite | `#/definitions/request.FavoriteCreate` | `#/definitions/model.Favorite` |
| `POST` | `/files/favorite/del` | Delete favorite | `#/definitions/request.FavoriteDelete` | `-` |
| `POST` | `/files/favorite/search` | List favorites | `#/definitions/dto.PageInfo` | `#/definitions/dto.PageResult` |
| `POST` | `/files/mode` | Change file mode | `#/definitions/request.FileCreate` | `-` |
| `POST` | `/files/move` | Move file | `#/definitions/request.FileMove` | `-` |
| `POST` | `/files/owner` | Change file owner | `#/definitions/request.FileRoleUpdate` | `-` |
| `POST` | `/files/read` | Read file by Line | `#/definitions/request.FileReadByLineReq` | `#/definitions/response.FileLineContent` |
| `POST` | `/files/recycle/clear` | Clear Recycle Bin files | `-` | `-` |
| `POST` | `/files/recycle/reduce` | Reduce Recycle Bin files | `#/definitions/request.RecycleBinReduce` | `-` |
| `POST` | `/files/recycle/search` | List Recycle Bin files | `#/definitions/dto.PageInfo` | `#/definitions/dto.PageResult` |
| `GET` | `/files/recycle/status` | Get Recycle Bin status | `-` | `-` |
| `POST` | `/files/rename` | Change file name | `#/definitions/request.FileRename` | `-` |
| `POST` | `/files/save` | Update file content | `#/definitions/request.FileEdit` | `-` |
| `POST` | `/files/search` | List files | `#/definitions/request.FileOption` | `#/definitions/response.FileInfo` |
| `POST` | `/files/size` | Load file size | `#/definitions/request.DirSizeReq` | `#/definitions/response.DirSizeRes` |
| `POST` | `/files/tree` | Load files tree | `#/definitions/request.FileOption` | `#/definitions/response.FileTree` |
| `POST` | `/files/upload` | Upload file | `-` | `-` |
| `POST` | `/files/upload/search` | Page file | `#/definitions/request.SearchUploadWithPage` | `#/definitions/dto.PageResult` |
| `POST` | `/files/wget` | Wget file | `#/definitions/request.FileWget` | `#/definitions/response.FileWgetRes` |
