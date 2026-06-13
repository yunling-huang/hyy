#!/usr/bin/env bash
# =============================================================
# 🧊 AI 时代 Python 数据分析训练营 - 一键部署脚本
# 用法：
#   ./deploy.sh                  → 交互式选择
#   ./deploy.sh local            → 本地直接运行
#   ./deploy.sh docker           → Docker 构建 + 运行
#   ./deploy.sh push YOUR_TOKEN  → 推送到 GitHub
# =============================================================
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

MODE=${1:-""}
TOKEN=${2:-""}

echo -e "${GREEN}
╔═══════════════════════════════════════════════════════════════╗
║                    🧊 AI 时代 Python数据分析训练营 - 一键部署         ║
╚═══════════════════════════════════════════════════════════════╝${NC}
"

# =============================================================
# 安装依赖
# =============================================================
install_deps() {
    echo -e "${YELLOW}[1/3]${NC} 检查 / 安装 Python 依赖..."
    if ! python3 -c "import streamlit, pandas, numpy, matplotlib" >/dev/null 2>&1; then
        echo "  → 安装依赖中..."
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt
        echo -e "  ✅ 依赖安装完成"
    else
        echo -e "  ✅ 依赖已就绪"
    fi
}

# =============================================================
# 模式 1：本地直接运行
# =============================================================
run_local() {
    install_deps
    echo ""
    echo -e "${GREEN}▶ 启动 Streamlit 服务（8501 端口)...${NC}"
    echo -e "  访问地址： http://localhost:8501"
    echo -e "  按 Ctrl+C 停止服务"
    exec streamlit run frontend/app.py \
        --server.port 8501 \
        --server.address 0.0.0.0 \
        --server.headless true \
        --server.enableCORS false \
        --browser.gatherUsageStats false
}

# =============================================================
# 模式 2：Docker 构建 + 运行
# =============================================================
run_docker() {
    echo -e "${YELLOW}[1/3]${NC} 检查 Docker..."
    if ! command -v docker >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker 未安装。请先安装：https://docs.docker.com/engine/install/${NC}"
        exit 1
    fi
    echo -e "  ✅ $(docker --version)"

    echo ""
    echo -e "${YELLOW}[2/3]${NC} 构建镜像 py-camp..."
    docker build -t py-camp:latest .

    if docker ps -a --format '{{.Names}}' | grep -q "^py-camp$"; then
        echo "  → 清理旧容器..."
        docker rm -f py-camp >/dev/null 2>&1
    fi

    echo ""
    echo -e "${YELLOW}[3/3]${NC} 启动容器（端口 8501)...${NC}"
    docker run -d --name py-camp -p 8501:8501 --restart unless-stopped py-camp:latest

    echo ""
    echo -e "${GREEN}✅ 部署完成！${NC}"
    echo -e "  访问地址：http://localhost:8501"
    echo -e "  查看状态：docker ps"
    echo -e "  查看日志：docker logs -f py-camp"
}

# =============================================================
# 模式 3：推送到 GitHub
# =============================================================
push_to_github() {
    echo -e "${YELLOW}[1/3]${NC} 提交本地变更..."
    git add -A
    if [ -n "$(git status --porcelain)" ]; then
        git commit -m "feat: AI时代Python数据分析训练营（10训练项目+100课后习题）"
    else
        echo "  → 暂无变更，跳过 commit"
    fi

    # 获取当前 origin 或使用默认仓库
    if git remote get-url origin >/dev/null 2>&1; then
        CURRENT_URL=$(git remote get-url origin)
        echo "  → 当前 origin：$CURRENT_URL"
    else
        CURRENT_URL="https://github.com/yunling-huang/Lars.git"
        git remote add origin "$CURRENT_URL"
        echo "  → 已设置 origin：$CURRENT_URL"
    fi

    echo ""
    if [ -z "$TOKEN" ]; then
        echo -e "${YELLOW}[2/3]${NC} 请提供 GitHub Personal Access Token："
        echo "  获取步骤：https://github.com/settings/tokens → Generate new token (classic) → 勾选 repo"
        echo "  或通过命令行参数：./deploy.sh push ghp_xxxxxxxxxxxxxxxxxxxx"
        read -rp "Token（ghp_ 开头）： " TOKEN
        if [ -z "$TOKEN" ]; then
            echo -e "${RED}❌ 未提供 token，已取消${NC}"
            exit 1
        fi
    fi

    # 验证 token
    echo ""
    echo -e "${YELLOW}[2/3]${NC} 验证 Token..."
    API_RESPONSE=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user -o /dev/null -w "%{http_code}")
    if [ "$API_RESPONSE" = "200" ]; then
        echo -e "  ✅ Token 有效"
    else
        echo -e "${RED}❌ Token 无效（状态码 $API_RESPONSE），请确认："
        echo "  1. token 是以 ghp_ 开头的字符串"
        echo "  2. 生成时勾选了 repo 权限"
        echo "  3. token 未过期"
        exit 1
    fi

    # 构造带 token 的 URL
    PUSH_URL="https://$TOKEN@github.com/yunling-huang/Lars.git"
    git remote set-url origin "$PUSH_URL"

    echo ""
    echo -e "${YELLOW}[3/3]${NC} 推送到 GitHub..."
    git push -u origin main 2>&1

    # 恢复不带 token 的 origin
    git remote set-url origin "https://github.com/yunling-huang/Lars.git"

    echo ""
    echo -e "${GREEN}✅ 推送成功！${NC}"
    echo -e "  仓库地址：https://github.com/yunling-huang/Lars"
    echo ""
    echo "🚀 下一步部署到云端："
    echo "  🎉 方式一（推荐）：Streamlit Community Cloud"
    echo "     打开 https://streamlit.io/cloud → New app → 选择仓库"
    echo "     → Branch: main → Main file: frontend/app.py → Deploy!"
    echo ""
    echo "  🐳 方式二：Docker"
    echo "     本地服务器：docker build -t py-camp . && docker run -d -p 8501:8501 py-camp"
    echo ""
    echo "  ☁️  方式三：自建云服务器（Ubuntu）"
    echo "     git clone https://github.com/yunling-huang/Lars.git"
    echo "     cd Lars && pip install -r requirements.txt"
    echo "     streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"
}

# =============================================================
# 主逻辑
# =============================================================
case "$MODE" in
    local)
        run_local
        ;;
    docker)
        run_docker
        ;;
    push)
        push_to_github
        ;;
    "")
        echo "可用模式："
        echo "  ./deploy.sh local                 → 本地运行 http://localhost:8501"
        echo "  ./deploy.sh docker                → Docker 构建 + 运行"
        echo "  ./deploy.sh push  [GITHUB_TOKEN]  → 推送到 GitHub"
        echo ""
        read -rp "请输入模式： " mode_choice
        case "$mode_choice" in
            1|local) run_local ;;
            2|docker) run_docker ;;
            3|push) push_to_github ;;
            *) echo -e "${RED}❌ 无效选择${NC}"; exit 1 ;;
        esac
        ;;
    *)
        echo -e "${RED}❌ 未知模式：$MODE${NC}"
        echo "支持：local / docker / push"
        exit 1
        ;;
esac
