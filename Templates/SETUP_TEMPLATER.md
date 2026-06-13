# 在 Obsidian 中安装并配置 Templater（自动插入 frontmatter）

下面的步骤会帮助你在 Obsidian 中安装 Templater 并配置为在新建文件时自动插入 YAML frontmatter（示例模板已在 `Templates/frontmatter.md`）。

1) 安装 Templater
- 打开 Obsidian → Settings → Community plugins → 关闭 Safe mode（若尚未关闭）。
- 点击 Browse，搜索 `Templater`，点击 Install，然后在 Installed 插件中启用它。

2) 设置模板文件夹
- Settings → Templater → Template folder location：选择或填入 `Templates`（或你希望放模板的文件夹）。

3) 模板内容（已创建）
- 我已在仓库创建： [Templates/frontmatter.md](Templates/frontmatter.md)

  内容为：

  ---
  title: <% tp.file.title() %>
  ---

  说明：`<% tp.file.title() %>` 会把文件名自动填入 `title` 字段。

4) 在新文件时自动应用模板（两种可靠方法）

- 方法 A：使用 Templater 的“Trigger on new file”（如果你的 Templater 版本支持）
  - Settings → Templater → 打开 `Trigger on new file`（或类似的“Run on new file”开关）。
  - 在可用的输入框中填写模板路径 `Templates/frontmatter.md`（有些版本会要求相对路径）。
  - 测试：在 Vault 中创建新文件，检查 frontmatter 是否被插入并且 `title` 被填为文件名。

- 方法 B（推荐，兼容性最强）：使用 QuickAdd 创建新笔记并自动应用 Templater 模板
  - 安装并启用 QuickAdd（Community plugins → Browse → QuickAdd）。
  - Settings → QuickAdd → Add a Macro/Choice：选择 `Template`（或 Capture→Template 类型），把 `Templates/frontmatter.md` 设为模板文件。
  - 如果有选项 `Use Templater` 或 `Run Templater on template`，务必打开它，以便模板中的 `<% %>` 表达式被处理。
  - 可选：将此 QuickAdd choice 绑定热键（Settings → Hotkeys → 搜索 QuickAdd）。

5) 绑定热键（可选）
- Settings → Hotkeys，搜索 `QuickAdd: <你的 choice 名称>` 或 `Templater: Insert template`，设定快捷键（例如 Ctrl+Alt+N）。

6) 验证与排错
- 若 `title` 为空：确认使用的是 `tp.file.title()`，并且模板由 Templater 渲染（QuickAdd 中需勾选“Use Templater”）。
- 若 Templater UI 未见“Trigger on new file”选项：使用 QuickAdd 方法，兼容性最高。

附：如果你希望，我可以生成一个 QuickAdd 的示例 `data.json` 片段或帮你写入 `.obsidian/plugins/quickadd/data.json`（注意：直接修改 Vault 的插件数据会覆盖本地设置，请先备份）。
