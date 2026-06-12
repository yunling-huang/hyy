"""
FastAPI主应用 - AI时代Python数据分析训练营后端
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import numpy as np
import json

from backend.models import Base, engine, get_db, UserProgress, LearningRecord, Leaderboard
from backend.schemas import (
    CodeRunRequest, CodeRunResponse, ScoreRequest, ScoreResponse,
    ProgressRequest, ProgressResponse, LeaderboardEntry, ProjectInfo,
    AIFeedbackRequest, AIFeedbackResponse
)
from backend.executor import executor
from backend.scoring import scoring_engine
from backend.data_generator import data_generator

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI数据分析训练营API",
    description="10个交互式数据分析训练项目的后端服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 项目元数据
PROJECTS = [
    {
        "id": 1,
        "name": "AI对话日志清洗工坊",
        "description": "使用Pandas清洗100条脏数据（含空值、乱码、重复）",
        "category": "数据清洗",
        "difficulty": "入门",
        "estimated_time": "15分钟"
    },
    {
        "id": 2,
        "name": "电商转化漏斗生成器",
        "description": "计算用户行为转化率并绘制漏斗图",
        "category": "聚合分析",
        "difficulty": "入门",
        "estimated_time": "20分钟"
    },
    {
        "id": 3,
        "name": "异常值侦探游戏",
        "description": "使用IQR/Z-score方法找出销售额曲线中的5个异常点",
        "category": "数据质量",
        "difficulty": "基础",
        "estimated_time": "25分钟"
    },
    {
        "id": 4,
        "name": "房价预测训练营",
        "description": "使用sklearn构建房价预测模型并优化参数",
        "category": "机器学习",
        "difficulty": "进阶",
        "estimated_time": "30分钟"
    },
    {
        "id": 5,
        "name": "微博情感分析器",
        "description": "训练朴素贝叶斯模型进行情感分类",
        "category": "NLP入门",
        "difficulty": "进阶",
        "estimated_time": "30分钟"
    },
    {
        "id": 6,
        "name": "用户分群画像系统",
        "description": "使用K-Means对会员进行聚类分群",
        "category": "聚类",
        "difficulty": "进阶",
        "estimated_time": "25分钟"
    },
    {
        "id": 7,
        "name": "大模型数据补全助手",
        "description": "调用大模型API补全残缺客户记录",
        "category": "LLM调用",
        "difficulty": "进阶",
        "estimated_time": "20分钟"
    },
    {
        "id": 8,
        "name": "服务器智能监控模拟器",
        "description": "实时检测CPU异常并预测下一个值",
        "category": "时间序列",
        "difficulty": "进阶",
        "estimated_time": "30分钟"
    },
    {
        "id": 9,
        "name": "购物篮推荐引擎",
        "description": "挖掘商品关联规则并生成推荐",
        "category": "关联规则",
        "difficulty": "中级",
        "estimated_time": "25分钟"
    },
    {
        "id": 10,
        "name": "AI数据分析报告生成器",
        "description": "一键生成完整的数据分析报告",
        "category": "综合",
        "difficulty": "中级",
        "estimated_time": "30分钟"
    }
]

# 数据缓存
DATA_CACHE = {}

@app.get("/")
async def root():
    """根路径"""
    return {"message": "AI数据分析训练营API", "version": "1.0.0"}

@app.get("/projects", response_model=List[ProjectInfo])
async def get_projects():
    """获取所有项目列表"""
    return PROJECTS

@app.get("/projects/{project_id}", response_model=ProjectInfo)
async def get_project(project_id: int):
    """获取单个项目信息"""
    for p in PROJECTS:
        if p["id"] == project_id:
            return p
    raise HTTPException(status_code=404, message="项目不存在")

@app.post("/run_code", response_model=CodeRunResponse)
async def run_code(request: CodeRunRequest):
    """执行用户代码"""
    # 验证代码安全性
    is_safe, msg = executor.validate_code(request.code)
    if not is_safe:
        return CodeRunResponse(
            success=False,
            output="",
            error=f"安全检查失败: {msg}"
        )

    # 获取项目数据
    context = DATA_CACHE.get(request.project_id, {})

    # 执行代码
    success, output, error, exec_time = executor.execute(request.code, context)

    return CodeRunResponse(
        success=success,
        output=output,
        error=error,
        execution_time=round(exec_time, 3)
    )

@app.post("/score", response_model=ScoreResponse)
async def score_answer(request: ScoreRequest):
    """评分用户答案"""
    score = 0.0
    max_score = 100.0
    feedback = ""
    hints = []

    try:
        if request.project_id == 1:
            # 数据清洗评分
            if 'user_df' in request.result:
                original_data = data_generator.generate_dirty_chat_logs()
                original_df = pd.DataFrame(original_data)
                user_df = pd.DataFrame(request.result['user_df'])
                score, feedback, hints = scoring_engine.evaluate_data_cleaning(user_df, original_df)

        elif request.project_id == 2:
            # 漏斗分析评分
            if 'funnel_data' in request.result:
                score, feedback, hints = scoring_engine.evaluate_funnel_analysis(request.result['funnel_data'])

        elif request.project_id == 3:
            # 异常值检测评分
            if 'anomalies' in request.result:
                true_anomalies = [10, 35, 60, 75, 90]
                score, feedback = scoring_engine.evaluate_anomaly_detection(
                    request.result['anomalies'], true_anomalies
                )

        elif request.project_id == 4:
            # 房价预测评分
            if 'mse' in request.result:
                score, feedback, hints = scoring_engine.evaluate_ml_model(request.result['mse'])

        elif request.project_id == 5:
            # 情感分析评分
            if 'y_pred' in request.result and 'y_true' in request.result:
                score, feedback = scoring_engine.evaluate_sentiment_analysis(
                    request.result['y_true'], request.result['y_pred']
                )

        elif request.project_id == 6:
            # 聚类评分
            if 'k' in request.result:
                score, feedback, hints = scoring_engine.evaluate_clustering(request.result['k'])

        elif request.project_id == 9:
            # 关联规则评分
            if 'rules' in request.result:
                score, feedback = scoring_engine.evaluate_association_rules(request.result['rules'])

    except Exception as e:
        feedback = f"评分过程出错: {str(e)}"

    return ScoreResponse(
        score=score,
        max_score=max_score,
        feedback=feedback,
        hints=hints
    )

@app.post("/save_progress", response_model=ProgressResponse)
async def save_progress(request: ProgressRequest, db: Session = Depends(get_db)):
    """保存用户进度"""
    try:
        # 查找现有进度
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == request.user_id,
            UserProgress.project_id == request.project_id
        ).first()

        if progress:
            # 更新
            progress.code = request.code
            progress.score = max(progress.score, request.score)
            progress.completed = max(progress.completed, 1 if request.completed else 0)
            progress.attempts += 1
            progress.metadata = request.metadata
        else:
            # 创建新进度
            progress = UserProgress(
                user_id=request.user_id,
                project_id=request.project_id,
                project_name=request.project_name,
                code=request.code,
                score=request.score,
                completed=1 if request.completed else 0,
                metadata=request.metadata
            )
            db.add(progress)

        db.commit()

        # 记录学习行为
        record = LearningRecord(
            user_id=request.user_id,
            project_id=request.project_id,
            action="save_progress",
            code=request.code,
            result=request.metadata,
            score=request.score
        )
        db.add(record)
        db.commit()

        return ProgressResponse(success=True, message="进度已保存")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_progress/{user_id}", response_model=List[dict])
async def get_progress(user_id: str, db: Session = Depends(get_db)):
    """获取用户进度"""
    progress_list = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()

    return [
        {
            "project_id": p.project_id,
            "project_name": p.project_name,
            "score": p.score,
            "completed": bool(p.completed),
            "attempts": p.attempts,
            "code": p.code
        }
        for p in progress_list
    ]

@app.get("/leaderboard/{project_id}", response_model=List[LeaderboardEntry])
async def get_leaderboard(project_id: int, db: Session = Depends(get_db)):
    """获取项目排行榜"""
    entries = db.query(Leaderboard).filter(
        Leaderboard.project_id == project_id
    ).order_by(Leaderboard.score.desc()).limit(20).all()

    return [
        LeaderboardEntry(
            user_id=e.user_id,
            score=e.score,
            metric_name=e.metric_name,
            rank=i+1
        )
        for i, e in enumerate(entries)
    ]

@app.post("/submit_score")
async def submit_score(
    user_id: str,
    project_id: int,
    score: float,
    metric_name: str,
    metadata: dict,
    db: Session = Depends(get_db)
):
    """提交分数到排行榜"""
    try:
        entry = Leaderboard(
            user_id=user_id,
            project_id=project_id,
            score=score,
            metric_name=metric_name,
            metadata=metadata
        )
        db.add(entry)
        db.commit()
        return {"success": True, "message": "分数已提交"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai_feedback", response_model=AIFeedbackResponse)
async def get_ai_feedback(request: AIFeedbackRequest):
    """获取AI反馈（模拟模式）"""
    # 模拟AI反馈
    suggestions = []

    if request.project_id == 1:
        if 'dropna' in request.user_code or 'fillna' in request.user_code:
            suggestions.append("很好！你使用了合适的方法处理空值")
        else:
            suggestions.append("建议使用 dropna() 或 fillna() 处理空值")

        if 'duplicated' in request.user_code:
            suggestions.append("已正确检测重复数据")

    elif request.project_id == 4:
        if 'LinearRegression' in request.user_code:
            suggestions.append("使用线性回归是不错的选择")

        if 'fit' in request.user_code:
            suggestions.append("模型已成功训练")

        suggestions.append("注意调整学习率可以获得更好的MSE")

    code_quality_score = 75.0  # 默认分数

    feedback = f"""代码审查反馈:
1. 整体结构清晰
2. {'使用了向量化操作，性能较好' if 'apply' not in request.user_code else '建议尽量使用向量化操作替代循环'}
3. 代码可读性良好

改进建议:
""" + "\n".join(f"- {s}" for s in suggestions)

    return AIFeedbackResponse(
        feedback=feedback,
        suggestions=suggestions,
        code_quality_score=code_quality_score
    )

@app.get("/data/{project_id}")
async def get_project_data(project_id: int):
    """获取项目数据"""
    if project_id in DATA_CACHE:
        return DATA_CACHE[project_id]

    try:
        if project_id == 1:
            data = data_generator.generate_dirty_chat_logs()
            df = pd.DataFrame(data)
            DATA_CACHE[project_id] = {"data": df.to_dict(), "original_df": df.to_dict()}
        elif project_id == 2:
            df = data_generator.generate_ecommerce_funnel()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "original_df": df.to_dict()}
        elif project_id == 3:
            df = data_generator.generate_sales_with_anomalies()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "anomaly_indices": [10, 35, 60, 75, 90]}
        elif project_id == 4:
            df = data_generator.generate_housing_data()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "target_col": "price"}
        elif project_id == 5:
            df = data_generator.generate_weibo_comments()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "label_col": "label"}
        elif project_id == 6:
            df = data_generator.generate_customer_segments()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "features": ["total_amount", "purchase频率", "recency_days"]}
        elif project_id == 7:
            df = data_generator.generate_incomplete_customer_data()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "missing_cols": ["age", "occupation", "income"]}
        elif project_id == 8:
            df = data_generator.generate_server_metrics()
            DATA_CACHE[project_id] = {"data": df.to_dict(), "anomaly_indices": [50, 100, 150]}
        elif project_id == 9:
            df = data_generator.generate_supermarket_orders()
            DATA_CACHE[project_id] = {"data": df.to_dict()}
        elif project_id == 10:
            df = data_generator.get_sample_csv_data()
            DATA_CACHE[project_id] = {"data": df.to_dict()}

        return DATA_CACHE[project_id]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
