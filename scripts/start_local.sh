#!/bin/bash

# 智能食物记录 App - 本地部署启动脚本 (macOS/Linux)

# 颜色定义
GREEN='\033[92m'
RED='\033[91m'
YELLOW='\033[93m'
BLUE='\033[94m'
RESET='\033[0m'
BOLD='\033[1m'

echo -e "${BOLD}${BLUE}"
echo "╔════════════════════════════════════════════════╗"
echo "║     智能食物记录 App - 本地部署启动脚本         ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${RESET}"

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python环境
echo -e "${BLUE}检查Python环境...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ 未找到Python3，请先安装Python 3.8+${RESET}"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt-get install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Python环境正常: $PYTHON_VERSION${RESET}"

# 检查Node.js环境
echo -e "${BLUE}检查Node.js环境...${RESET}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ 未找到Node.js，请先安装Node.js 16+${RESET}"
    echo "  下载地址: https://nodejs.org/"
    echo "  macOS: brew install node"
    echo "  Ubuntu: sudo apt-get install nodejs npm"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js环境正常: $NODE_VERSION${RESET}"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ 未找到npm${RESET}"
    exit 1
fi

# 获取本机IP地址
echo -e "${BLUE}获取本机IP地址...${RESET}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")
else
    # Linux
    IP=$(hostname -I | awk '{print $1}' || echo "127.0.0.1")
fi
echo -e "${GREEN}✓ 本机IP地址: $IP${RESET}"

echo ""
echo "═════════════════════════════════════════════════"
echo " 开始安装依赖并初始化数据库..."
echo "═════════════════════════════════════════════════"
echo ""

# 进入后端目录
cd "$SCRIPT_DIR/backend"

# 检查.env文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}○ 创建.env配置文件...${RESET}"
    cat > .env << EOF
# GLM API配置（必填）
GLM_API_KEY=your_glm_api_key_here

# 环境模式（production: 生产简化错误 / development: 开发详细错误）
ENV_MODE=production
EOF
    echo -e "${YELLOW}  已创建.env文件，请编辑填写GLM_API_KEY${RESET}"
    echo ""
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo -e "${BLUE}创建Python虚拟环境...${RESET}"
    python3 -m venv venv
    echo -e "${GREEN}✓ 虚拟环境创建完成${RESET}"
fi

# 激活虚拟环境
echo -e "${BLUE}激活虚拟环境...${RESET}"
source venv/bin/activate

# 升级pip
echo -e "${BLUE}升级pip...${RESET}"
pip install --upgrade pip > /dev/null 2>&1

# 安装Python依赖
echo -e "${BLUE}安装Python依赖...${RESET}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Python依赖安装失败${RESET}"
    exit 1
fi
echo -e "${GREEN}✓ Python依赖安装完成${RESET}"

# 初始化数据库
echo -e "${BLUE}初始化数据库（导入105种食物）...${RESET}"
python init_extended_database.py
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 数据库初始化失败${RESET}"
    exit 1
fi
echo -e "${GREEN}✓ 数据库初始化完成${RESET}"

echo ""
echo "═════════════════════════════════════════════════"
echo " 准备启动服务..."
echo "═════════════════════════════════════════════════"
echo ""

# 启动后端服务（后台运行）
echo -e "${BLUE}启动后端服务（端口8000）...${RESET}"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ 后端服务启动中... (PID: $BACKEND_PID)${RESET}"

# 等待后端启动
sleep 3

# 进入前端目录
cd "$SCRIPT_DIR/frontend"

# 安装前端依赖
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}安装前端依赖（首次运行）...${RESET}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ 前端依赖安装失败${RESET}"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    echo -e "${GREEN}✓ 前端依赖安装完成${RESET}"
fi

# 启动前端服务（后台运行）
echo -e "${BLUE}启动前端服务（端口5173）...${RESET}"
nohup npm run dev -- --host 0.0.0.0 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ 前端服务启动中... (PID: $FRONTEND_PID)${RESET}"

echo ""
echo -e "${BOLD}${GREEN}"
echo "╔════════════════════════════════════════════════╗"
echo "║            服务启动完成！                        ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${RESET}"
echo -e "${GREEN}✓ 所有服务已启动${RESET}"
echo ""
echo "┌─────────────────────────────────────────────┐"
echo "│  访问地址:                                  │"
echo "│                                            │"
echo "│  电脑浏览器:                                │"
echo "│    http://localhost:5173                   │"
echo "│                                            │"
echo "│  手机浏览器（确保连接同一WiFi）:             │"
echo "│    http://$IP:5173                         │"
echo "│                                            │"
echo "│  API文档:                                   │"
echo "│    http://localhost:8000/docs               │"
echo "└─────────────────────────────────────────────┘"
echo ""
echo -e "${YELLOW}提示:${RESET}"
echo "  - 服务已在后台运行"
echo "  - 查看日志: tail -f backend.log 或 tail -f frontend.log"
echo "  - 停止服务: kill $BACKEND_PID $FRONTEND_PID"
echo "  - 或运行: ./stop_local.sh"
echo ""
echo -e "${YELLOW}如遇问题，请查看 MOBILE_TEST_GUIDE.md${RESET}"
echo ""

# 创建停止脚本
cat > "$SCRIPT_DIR/stop_local.sh" << EOF
#!/bin/bash
echo "停止服务..."
cd "\$(dirname "\$0")"
pkill -f "uvicorn app.main:app"
pkill -f "vite"
echo "服务已停止"
EOF
chmod +x "$SCRIPT_DIR/stop_local.sh"

echo "已创建停止脚本: ./stop_local.sh"
echo ""
