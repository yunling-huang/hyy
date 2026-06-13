#!/usr/bin/env bash
# =============================================================
# 🧊 AI 时代 Python数据分析训练营 - 一键部署脚本
# 支持：本机运行 / Docker 构建 / GitHub 推送（可选）
# =============================================================
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${GREEN}
╔═══════════════════════════════════════════════════════════════╗
║                    🧊 AI 时代 Python数据分析训练营 - 一键部署         ║
╚═══════════════════════════════════════════════════════════════╝${NC}
"
echo -e "${BLUE}项目目录：${PROJECT_DIR}${NC}"
echo ""

# =============================================================
# 1. 依赖安装
# =============================================================
echo -e "${YELLOW}[1/5]${NC} 检查 / 安装 Python 依赖..."
if ! python3 -c "import streamlit, pandas, numpy, matplotlib" >/dev/null 2>&1; then
    echo "  → 正在安装依赖（首次运行较慢，请耐心等待）..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    echo -e "  ✅ 依赖安装完成"
else
    echo -e "  ✅ 依赖已就绪"
fi

# =============================================================
# 2. 本地运行模式选择
# =============================================================
echo ""
echo -e "${YELLOW}[2/5]${NC} 选择部署模式："
echo ""
echo "  1) 🚀 本地直接运行（默认）"
echo "  2) 🐳 Docker 构建 + 运行"
echo "  3) 📦 推送到 GitHub（之后再部署到云)"
echo ""
read -rp "请选择 1 / 2 / 3： " choice
choice=${choice:-1}

# =============================================================
# 模式 1：本地直接运行
# =============================================================
if [ "$choice" = "1" ]; then
    echo ""
    echo -e "${GREEN}▶ 启动本地 Streamlit 服务（8501 端口)...${NC}"
    echo -e "  访问地址： http://localhost:8501"
    echo -e "  按 Ctrl+C 停止服务"
    exec streamlit run frontend/app.py \
        --server.port 8501 \
        --server.address 0.0.0.0 \
        --server.headless true \
        --server.enableCORS false \
        --browser.gatherUsageStats false

# =============================================================
# 模式 2：Docker 构建 + 运行
# =============================================================
elif [ "$choice" = "2" ]; then
    echo ""
    echo -e "${YELLOW}[3/5]${NC} 检查 Docker 环境..."
    if ! command -v docker >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker 未安装或未启动，请先安装 Docker：https://docs.docker.com/engine/install/ ${NC}"
        exit 1
    fi

    echo -e "  ✅ Docker 版本：$(docker --version)"

    read -rp "请输入镜像名 [py-camp： " IMAGE_NAME
IMAGE_NAME=${IMAGE_NAME:-py-camp}

    echo ""
    echo -e "${YELLOW}[4/5]${NC} 构建 Docker 镜像..."
    docker build -t "${IMAGE_NAME}":latest .
    echo -e "  ✅ 镜像构建完成：${IMAGE_NAME}"

    # 清理已有同名容器
    if docker ps -a --format '{{.Names}}' | grep -q "^${IMAGE_NAME}$"; then
        echo "  → 清理已有同名容器..."
        docker rm -f "${IMAGE_NAME}" >/dev/null 2>&1
    fi

    echo ""
    echo -e "${YELLOW}[5/5]${NC} 启动容器（端口 8501)...${NC}"
    docker run -d --name "${IMAGE_NAME}" \
        -p 8501:8501 \
        --restart unless-stopped \
        "${IMAGE_NAME}":latest

    echo ""
    echo -e "${GREEN}✅ 部署完成！${NC}"
    echo -e "  访问地址：http://localhost:8501"
    echo -e "  查看状态：docker ps"
    echo -e "  查看日志：docker logs -f ${IMAGE_NAME}"
    echo -e "  停止容器：docker stop ${IMAGE_NAME}"

# =============================================================
# 模式 3：Git 推送（先本地提交，再推到 GitHub）
# =============================================================
elif [ "$choice" = "3" ]; then
    echo ""
    echo -e "${YELLOW}[3/5]${NC} 准备提交到 GitHub..."
    echo ""
    # 提交
    git add -A
    if [ -z "$(git status --porcelain)" ]; then
        echo "  → 没有变更，跳过 commit"
    else
        read -rp "请输入 commit 信息（feat: AI 时代 Python 数据分析训练营）： " commit_msg
        commit_msg=${commit_msg:-"feat: AI 时代 Python 数据分析训练营（10 训练项目 + 100 习题）}
        git commit -m "$commit_msg"
    fi

    echo ""
    echo -e "${YELLOW}[4/5]${NC} 设置远程仓库..."
    if git remote get-url origin >/dev/null 2>&1; then
        echo "  → 已有 origin：$(git remote get-url origin)"
        read -rp "是否更换 origin？(y/n，默认 n：" change_origin
        if [ "$change_origin" = "y" ]; then
            read -rp "请输入新的 GitHub 仓库地址：https://github.com/用户名/仓库名.git"
            git remote set-url origin "$new_url"
        fi
    else
            read -rp "请输入你的 GitHub 仓库地址（例如 https://github.com/用户名/仓库名.git）：" github_url
            if [ -z "$github_url" ]; then
                echo -e "${RED}❌ 未提供仓库地址，已取消${NC}"
                exit 1
            fi
            git remote add origin "$github_url"
    fi

    echo ""
    echo -e "${YELLOW}[5/5]${NC} 推送到 GitHub..."
    git push -u origin main || git push -u origin master || {
        echo ""
        echo -e "${YELLOW}提示：如 push 失败，请检查仓库权限或输入正确 GitHub token。${NC}"
        echo "  Token 获取：https://github.com/settings/tokens (勾选 repo 权限)"
        echo "  可重新运行本脚本重试"
        exit 1
    }

    echo ""
    echo -e "${GREEN}✅ 推送成功！${NC}"
    echo -e "  访问仓库：$(git remote get-url origin | sed 's/\.git$//')"
    echo ""
    echo "下一步："
    echo "  🎉 把链接发给小伙伴，或前往该仓库"
    echo "  🌩 云部署建议："
    echo "  - Streamlit Community Cloud：https://streamlit.io/cloud"
    echo "  - Railway / Render / Heroku：把 git 地址直接粘贴进去"
    echo "  - 自建云服务器：docker build / systemd 进程管理"

else
    echo -e "${RED}❌ 无效的选择${NC}"
    exit 1
fi
