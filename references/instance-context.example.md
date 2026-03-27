# Instance Context Template

这个文件是给某个具体 1Panel 实例准备的本地上下文模板。

公开仓库只保留这个模板，不提交真实实例信息。

## Example Fields

- 面板入口：`https://panel.example.com`
- Swagger UI：`https://panel.example.com/1panel/swagger/index.html`
- Swagger JSON：`https://panel.example.com/1panel/swagger/doc.json`
- 当前环境用途：开发 / 测试 / 生产
- 资源约束：例如内存、磁盘、并发限制
- 已知高风险对象：例如网站代理、容器、数据库、系统设置
- 特殊操作约束：例如必须先停机、必须先备份、只能夜间执行

## Usage

如果你本地要保留某个真实实例的细节，可以复制为：

- `references/instance-context.local.md`

该文件应被 `.gitignore` 忽略，只在本地开发时使用。
