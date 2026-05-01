# 末日回响写作站

一个简洁、美观的在线写作与分享平台。支持 Markdown 编辑、文章管理、用户评论、站内信和表情包功能。

## 功能特性

- 📝 **Markdown 写作** — 基于 EasyMDE 的所见即所得编辑体验
- 🏠 **个人主页** — 每位作者拥有独立主页，展示所有作品
- 💬 **评论系统** — 支持点赞、回复，可插入表情包
- ✉️ **站内信** — 用户间私信聊天，支持表情包发送
- 📚 **文章合集** — 将文章归类整理为合集
- 🔍 **全文搜索** — 同时搜索文章和用户
- 🔄 **排序切换** — 按最新 / 最热 / 编号排列文章
- 🌓 **夜间模式** — 跟随系统或手动切换
- 🎨 **暖氧主题** — 米白底色、暖橙棕点缀，宋体为主的舒适阅读体验
- 📱 **响应式设计** — 桌面端瀑布流、手机端自适应
- ⚡ **自动加载** — 优雅的加载动画

## 快速开始

### 环境要求

- Python 3.8+
- 依赖库：`flask`, `waitress`, `markdown`

### 安装运行

```bash
# 安装依赖
pip install flask waitress markdown

# 启动服务
cd simple-writer
python3 server.py
```

服务默认运行在 `http://localhost:5000`。

### 生产部署

```bash
# 使用 Waitress 作为生产服务器
python3 server.py
```

## 项目结构

```
simple-writer/
├── server.py              # 主服务
├── users/
│   └── users.json         # 用户数据
├── docs/                  # 文章存储
│   ├── {id}.meta.json     # 文章元信息
│   └── {id}.txt           # 文章内容
├── comments/              # 评论数据
├── collections/           # 合集数据
├── templates/             # Jinja2 模板
│   ├── index.html         # 首页
│   ├── read.html          # 文章阅读页
│   ├── edit.html          # 编辑页
│   ├── messages.html      # 站内信
│   ├── user.html          # 用户主页
│   ├── collection.html    # 合集详情
│   └── collections.html   # 合集列表
├── static/
│   ├── favicon.ico
│   ├── covers/            # 文章封面
│   └── uploads/           # 用户上传
└── users/avatars/         # 用户头像
```

## 技术栈

- **后端** — Flask + Waitress
- **模板** — Jinja2
- **编辑器** — EasyMDE (Markdown)
- **存储** — JSON 文件（零依赖数据库）

## 开源协议

[MIT License](LICENSE)
