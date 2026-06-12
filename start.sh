#!/bin/bash
# AI数据分析训练营 - 启动脚本

echo "=========================================="
echo "AI时代Python数据分析训练营 启动中..."
echo "=========================================="

# 检查依赖
echo "检查依赖..."
python3 -c "import fastapi, streamlit, pandas, numpy, sklearn, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 缺少必要依赖，请运行: pip install -r requirements.txt"
    exit 1
fi

# 启动后端服务
echo "启动后端API服务 (端口 8000)..."
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端服务
echo "启动Streamlit前端 (端口 8501)..."
streamlit run frontend/app.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "服务已启动!"
echo "前端: http://localhost:8501"
echo "后端API: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "=========================================="
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
wait
