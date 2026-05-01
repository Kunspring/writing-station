# 末日回响写作站

> 一个属于自己的写作角落。

## 这是什么

轻量、优雅的在线写作平台。没有数据库——文章就是文件，简单直接。

写 Markdown、发评论、收站内信、整理合集。几个人一起用也行，自己安静写也行。

## 功能

- **Markdown 写作** — 所见即所得
- **评论系统** — 点赞、回复、表情包
- **站内信** — 和站内朋友私聊
- **文章合集** — 把你的作品归类
- **全文搜索** — 搜文章也搜人
- **排序切换** — 最新 / 最热 / 编号
- **夜间模式** — 手动切换
- **响应式** — 手机也能舒服看
- **暖氧主题** — 米白底色，宋体阅读

## 技术栈

Python · Flask · Waitress · Jinja2 · EasyMDE

**零数据库**，所有内容存 JSON 文件。

## 快速开始

```bash
pip install flask waitress markdown
cd simple-writer
python3 server.py
```

服务跑在 `http://localhost:5000`。

## 项目结构

```
simple-writer/
├── server.py              # 后端
├── docs/                  # 文章
├── comments/              # 评论
├── collections/           # 合集
├── templates/             # 页面模板
└── static/                # 静态文件
```

---

MIT License · 大二学生独立开发
