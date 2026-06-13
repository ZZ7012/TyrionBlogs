# Tyrion's Blogs

个人学习笔记，如有不对的地方，还望批评指正。

## 目录结构

```
TyrionBlogs/
├── src/
│   ├── .vuepress/          # VuePress 配置（导航/侧边栏/主题）
│   ├── posts/Autosar/      # 博客文章（由 sync 脚本从 Obsidian 同步）
│   │   ├── BSW/            # 基础软件层
│   │   ├── Security/       # 安全模块
│   │   ├── MCAL/           # 微控制器抽象层
│   │   └── 架构设计/        # 实战方案
│   └── README.md           # 博客首页
├── sync_obsidian_to_vuepress.py  # Obsidian → VuePress 同步脚本
└── package.json
```

## 使用

```bash
# 安装依赖
pnpm install

# 从 Obsidian 同步文章
pnpm run docs:sync

# 本地预览
pnpm run docs:dev

# 构建
pnpm run docs:build
```

## 工作流

```
Obsidian 写笔记 → docs:sync 同步 → docs:dev 预览 → git push → GitHub Actions 自动部署
```
