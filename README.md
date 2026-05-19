
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1-lightgrey?style=flat&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/database-zero-brightgreen?style=flat" alt="Zero DB">
  <img src="https://img.shields.io/github/license/Kunspring/writing-station" alt="License">
</p>

<br>

<div align="center">

# 🌅 末日回响写作站 · Apocalypse Echo Writing Station

_一个属于自己的写作角落 · A writing corner of your own._

**中文** · [English](#english)

</div>

---

<div lang="zh-CN">

## 📖 这是什么

轻量、优雅的在线写作平台。**没有数据库**——文章就是文件，简单直接。

写 Markdown、发评论、收站内信、整理合集。几个人一起用也行，自己安静写也行。

## ✨ 功能

| 功能 | 说明 |
|------|------|
| **Markdown 写作** | 所见即所得编辑器（EasyMDE） |
| **评论系统** | 点赞、回复、表情包、贴纸 |
| **站内信** | 和站内朋友私聊 |
| **文章合集** | 把你的作品归类 |
| **全文搜索** | 搜文章也搜人 |
| **排序切换** | 最新 / 最热 / 编号 |
| **夜间模式** | 一键切换 |
| **响应式** | 手机也能舒服看 |
| **暖氧主题** | 米白底色，宋体阅读 |

## 🛠 技术栈

**Python** · **Flask** · **Jinja2** · **EasyMDE** · **Waitress**

> 🚫 零数据库 — 所有内容存 JSON 文件，备份即复制文件夹。

## 🚀 一键部署

```bash
# 1. 下载
git clone https://github.com/Kunspring/writing-station.git
cd writing-station

# 2. 一键部署（自动完成全部步骤）
bash deploy.sh
```

`deploy.sh` 会自动完成：

1. ✅ 检查 Python 环境
2. ✅ 创建所有必要目录
3. ✅ 安装 Python 依赖
4. ✅ 生成密钥文件
5. ✅ 启动服务

服务跑在 **`http://localhost:5000`**

### 自定义端口

```bash
PORT=8080 bash deploy.sh
```

### 后台运行

```bash
nohup python3 server.py >> output.log 2>&1 &
```

### 手动分步安装

```bash
pip install -r requirements.txt
python3 server.py
```

## 📝 首次使用

1. 访问 `http://localhost:5000`，注册一个账号
2. 编辑 `users/users.json`，找到你的账号，把 `"role"` 改为 `"admin"`
3. 刷新页面，获得完整管理权限

## 📁 项目结构

```
writing-station/
├── server.py              # 后端（Flask）
├── requirements.txt       # Python 依赖
├── deploy.sh              # 一键部署脚本
├── templates/             # 页面模板
├── docs/                  # 文章内容（用户数据）
├── comments/              # 评论数据
├── collections/           # 合集配置
├── users/                 # 用户数据
├── static/                # 静态文件
│   ├── covers/            # 封面图片
│   └── uploads/           # 用户上传
└── novel/                 # 小说
```

## ⚙ 环境要求

- Python 3.8+
- Linux / macOS / WSL

</div>

---

<h1 id="english" align="center">🇬🇧 English</h1>

<div lang="en">

## 📖 What is this

A lightweight, elegant online writing platform. **No database** — every article is a plain text file. Simple and straightforward.

Write in Markdown, comment, send private messages, organize into collections. Use it solo or with friends.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Markdown Editor** | WYSIWYG via EasyMDE |
| **Comment System** | Likes, replies, emoji, stickers |
| **In-site Messaging** | Chat with other users |
| **Collections** | Categorize your articles |
| **Full-text Search** | Search articles & users |
| **Sort** | Newest / Hottest / By ID |
| **Dark Mode** | Toggle at will |
| **Responsive** | Works great on mobile |
| **Warm Theme** | Cream background, Song typeface |

## 🛠 Tech Stack

**Python** · **Flask** · **Jinja2** · **EasyMDE** · **Waitress**

> 🚫 Zero database — everything is stored as JSON files. Backup = copy the folder.

## 🚀 One-Click Deploy

```bash
# 1. Clone
git clone https://github.com/Kunspring/writing-station.git
cd writing-station

# 2. Deploy (automatic)
bash deploy.sh
```

`deploy.sh` handles everything:

1. ✅ Check Python environment
2. ✅ Create required directories
3. ✅ Install Python dependencies
4. ✅ Generate secret key
5. ✅ Start the server

Visit **`http://localhost:5000`** 🎉

### Custom Port

```bash
PORT=8080 bash deploy.sh
```

### Run in Background

```bash
nohup python3 server.py >> output.log 2>&1 &
```

### Manual Setup

```bash
pip install -r requirements.txt
python3 server.py
```

## 📝 First-Time Setup

1. Open `http://localhost:5000` and register an account
2. Edit `users/users.json`, find your account and set `"role"` to `"admin"`
3. Refresh the page — you're now an admin

## 📁 Project Structure

```
writing-station/
├── server.py              # Backend (Flask)
├── requirements.txt       # Python dependencies
├── deploy.sh              # One-click deploy script
├── templates/             # HTML templates
├── docs/                  # Article content (user data)
├── comments/              # Comment data
├── collections/           # Collection configs
├── users/                 # User data
├── static/                # Static files
│   ├── covers/            # Cover images
│   └── uploads/           # User uploads
└── novel/                 # Novel drafts
```

## ⚙ Requirements

- Python 3.8+
- Linux / macOS / WSL

---

<div align="center">

<sub>Made with ⚡ by Kunspring | [Report Issue](https://github.com/Kunspring/writing-station/issues)</sub>

</div>
</div>
