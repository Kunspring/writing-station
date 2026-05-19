#!/bin/bash
# ==============================================================
#  写作站 - 一键部署脚本
#  用法: bash deploy.sh
#  说明: 从零搭建，自动安装依赖、创建目录、启动服务
# ==============================================================

set -e

# ── 颜色 ──
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  写作站一键部署脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 1. 检查 Python 版本
echo -e "\n${YELLOW}[1/5] 检查环境...${NC}"
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  echo -e "${RED}✗ 未找到 Python，请先安装 Python 3.8+${NC}"
  exit 1
fi
echo "  使用: $PYTHON"
$PYTHON --version

# 2. 创建必要目录
echo -e "\n${YELLOW}[2/5] 创建目录结构...${NC}"
mkdir -p docs comments collections users static/covers static/uploads/videos static/uploads/stickers users/avatars novel
echo "  目录已就绪"

# 3. 安装 Python 依赖
echo -e "\n${YELLOW}[3/5] 安装依赖...${NC}"
if [ ! -f "requirements.txt" ]; then
  echo -e "${RED}✗ 缺少 requirements.txt，请确认在项目根目录执行${NC}"
  exit 1
fi
$PYTHON -m pip install -r requirements.txt -q
echo "  依赖安装完成"

# 4. 生成密钥（首次运行）
echo -e "\n${YELLOW}[4/5] 初始化...${NC}"
if [ ! -f ".secret_key" ]; then
  $PYTHON -c "import secrets; open('.secret_key','w').write(secrets.token_hex(32))"
  echo "  已生成密钥文件 .secret_key"
else
  echo "  密钥已存在，跳过"
fi

# 5. 启动服务
echo -e "\n${YELLOW}[5/5] 启动写作站...${NC}"
PORT=${PORT:-5000}

# 检查端口是否被占用
if lsof -i :$PORT -sTCP:LISTEN 2>/dev/null; then
  echo -e "${YELLOW}  端口 $PORT 已被占用，是否强制启动？${NC}"
  echo -e "${YELLOW}  - 按 Ctrl+C 取消，再运行 PORT=其他值 bash deploy.sh${NC}"
  echo -e "${YELLOW}  - 或等待 3 秒自动尝试...${NC}"
  sleep 3
fi

echo -e "\n${GREEN}✔ 部署完成！${NC}"
echo -e "${GREEN}  访问地址: http://localhost:$PORT${NC}"
echo -e "${GREEN}  后台运行: nohup python3 server.py >> output.log 2>&1 &${NC}"
echo -e "${GREEN}  停止服务: kill \$(cat /tmp/writing-station.pid 2>/dev/null) 2>/dev/null${NC}"
echo -e "${YELLOW}  首次使用请注册管理员账号，然后编辑 users/users.json 设置 role=admin${NC}"
echo ""

# 启动
$PYTHON server.py
