FROM python:3.11-slim

# 基础信息
LABEL maintainer="AI数据分析训练营 <2035730477@qq.com>"
LABEL description="AI 时代 Python数据分析训练营 - 10 训练项目 + 100 课后习题"

# 设置 Python 环境变量（避免交互式提示 + 缓冲输出）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false

WORKDIR /app

# 安装系统依赖（matplotlib 需要字体库，显示中文）
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        fonts-noto-cjk \
        fonts-wqy-microhei \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 先复制 requirements，方便 Docker 缓存
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 暴露端口
EXPOSE 8501

# 默认启动命令
CMD ["streamlit", "run", "frontend/app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501"]
