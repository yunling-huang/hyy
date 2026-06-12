# AI时代Python数据分析训练营

FastAPI后端 + Streamlit前端 + SQLite数据库

## 快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动后端API服务
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 3. 启动前端
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### 4. 访问
- 前端：http://localhost:8501
- 后端API文档：http://localhost:8000/docs

## 项目列表

1. AI对话日志清洗工坊 - 数据清洗
2. 电商转化漏斗生成器 - 聚合分析
3. 异常值侦探游戏 - 数据质量
4. 房价预测训练营 - 机器学习
5. 微博情感分析器 - NLP入门
6. 用户分群画像系统 - 聚类
7. 大模型数据补全助手 - LLM调用
8. 服务器智能监控模拟器 - 时间序列
9. 购物篮推荐引擎 - 关联规则
10. AI数据分析报告生成器 - 综合

## 技术栈

- 前端：Streamlit
- 后端：FastAPI + Pandas
- 数据库：SQLite
- 机器学习：scikit-learn
- 图表：Plotly
