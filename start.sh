#!/bin/bash
# ============================================================
# 🧊 AI时代 Python数据分析训练营 - 启动脚本
# 一键部署 Streamlit 前端 + FastAPI 后端
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 项目路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_PATH="$SCRIPT_DIR/frontend/app.py"

# 参数
PORT="${PORT:-8501}"
API_PORT="${API_PORT:-8000}"

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║          🧊 AI 时代 Python 数据分析训练营  🧊                 ║"
echo "║                                                                  ║"
echo "║         10个交互式训练项目 · 从基础到进阶                      ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${BLUE}[INFO]${NC} 工作目录: ${SCRIPT_DIR}"
echo -e "${BLUE}[INFO]${NC} 前端端口: ${PORT}  后端API端口: ${API_PORT}"
echo ""

# ============================================================
# 依赖检查与安装
# ============================================================
echo -e "${BLUE}[1/3]${NC} 检查依赖..."

python3 -c "import streamlit, pandas, numpy, matplotlib, sqlalchemy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[警告]${NC} 缺少必要依赖，开始安装..."
    pip3 install -r "$SCRIPT_DIR/requirements.txt" || {
        echo -e "${RED}[错误]${NC} 依赖安装失败，请检查网络或手动安装:"
        echo "  pip install streamlit pandas numpy matplotlib sqlalchemy fastapi uvicorn"
        exit 1
    }
    echo -e "${GREEN}[成功]${NC} 依赖安装完成！"
else
    echo -e "${GREEN}[OK]${NC} 所有依赖已就绪"
fi

echo ""

# ============================================================
# 启动服务
# ============================================================
echo -e "${BLUE}[2/3]${NC} 启动服务..."

# 如果启动了后端，显示信息
echo -e "  ${GREEN}✓${NC} Streamlit 前端: http://localhost:${PORT}"
echo -e "  ${GREEN}✓${NC} 项目数据目录: ${SCRIPT_DIR}"
echo ""

echo -e "${GREEN}"
echo "================================================================"
echo ""
echo "  🚀 系统启动中..."
echo ""
echo "  本地访问:   http://localhost:${PORT}"
echo "  网络访问:   http://0.0.0.0:${PORT}"
echo ""
echo "  按 Ctrl+C 停止服务器"
echo ""
echo "================================================================"
echo -e "${NC}"
echo ""
echo -e "${BLUE}[3/3]${NC} 启动 Streamlit 前端应用..."
echo ""

# ============================================================
# 启动 Streamlit
# ============================================================
cd "$SCRIPT_DIR"
streamlit run "$APP_PATH" \
    --server.port "${PORT}" \
    --server.address "0.0.0.0" \
    --server.enableCORS true \
    --server.enableXsrfProtection false \
    --server.headless false \
    --server.fileWatcherType "none" \
    --browser.gatherUsageStats false || {
    echo -e "${RED}[错误]${NC} Streamlit 启动失败"
    exit 1
}
