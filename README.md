# 末日回响写作站

> 一个属于自己的写作角落。

轻量、优雅的在线写作平台。没有数据库——文章就是文件，简单直接。

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

Python · Flask · Jinja2 · EasyMDE · **零数据库**

## 🚀 一键部署

```bash
# 1. 下载
git clone https://github.com/Kunspring/writing-station.git
cd writing-station

# 2. 一键部署（自动完成全部步骤）
bash deploy.sh
```

`deploy.sh` 会自动：
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

## 首次使用

1. 访问 `http://localhost:5000`，注册一个账号
2. 编辑 `users/users.json`，找到你的账号，把 `"role"` 改为 `"admin"`
3. 刷新页面，获得完整管理权限

## 项目结构

```
writing-station/
├── server.py              # 后端（Flask）
├── requirements.txt       # Python 依赖
├── deploy.sh              # 一键部署脚本
├── templates/             # 页面模板
├── docs/                  # 文章内容（用户数据，不纳入Git）
├── comments/              # 评论数据
├── collections/           # 合集配置
├── users/                 # 用户数据
├── static/                # 静态文件
│   ├── covers/            # 封面图片
│   └── uploads/           # 用户上传
└── novel/                 # 小说
```

## 环境要求

- Python 3.8+
- Linux / macOS / WSL
