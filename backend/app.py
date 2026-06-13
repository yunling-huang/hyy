"""
AI时代Python数据分析训练营 - FastAPI后端服务
提供代码执行、评分、进度管理等功能
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import uvicorn
import uuid

from database import Base, engine, get_db, UserProgress, LearningRecord, Leaderboard
from executor import executor, scoring_engine, ai_feedback

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI数据分析训练营API",
    description="Python数据分析训练营 - 代码执行与学习管理系统",
    version="1.0.0"
)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== API请求/响应模型 ==============

class CodeRunRequest(BaseModel):
    """代码执行请求"""
    code: str
    project_id: int
    user_id: str


class CodeRunResponse(BaseModel):
    """代码执行响应"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float


class ScoreRequest(BaseModel):
    """评分请求"""
    project_id: int
    user_id: str
    code: str
    output: str
    is_success: bool


class ProgressRequest(BaseModel):
    """进度保存请求"""
    user_id: str
    project_id: int
    project_name: str
    code: str
    score: float
    completed: bool


# ============== 项目配置 ==============

PROJECTS_CONFIG = [
    {
        "id": 1,
        "name": "Python基础交互式计算",
        "subtitle": "营收求和练习",
        "description": "某门店3天销售额分别为 [1280, 2560, 1890]，用Python列表遍历计算总销售额、日均销售额，交互式打印结果。",
        "difficulty": "⭐",
        "category": "Python基础",
        "estimated_time": "10分钟",
        "initial_code": '''sales = [1280, 2560, 1890]
total = sum(sales)
avg = total / len(sales)
print(f"总销售额：{total} 元")
print(f"日均销售额：{avg:.2f} 元")
''',
        "key_concepts": ["列表操作", "循环遍历", "格式化输出", "类型转换"]
    },
    {
        "id": 2,
        "name": "NumPy数组批量运算",
        "subtitle": "用户量翻倍计算",
        "description": "导入numpy，构建数组 user_arr = np.array([120, 245, 368, 412])，每个用户量上浮15%，保留整数输出新数组。",
        "difficulty": "⭐",
        "category": "NumPy基础",
        "estimated_time": "10分钟",
        "initial_code": '''import numpy as np

user_arr = np.array([120, 245, 368, 412])
new_user = np.round(user_arr * 1.15).astype(int)
print("上浮15%后的用户数组：", new_user)
''',
        "key_concepts": ["NumPy数组", "向量运算", "类型转换", "数学函数"]
    },
    {
        "id": 3,
        "name": "Pandas创建数据表",
        "subtitle": "电商订单分析",
        "description": "用Pandas构建电商订单DataFrame，字段：订单号、用户ID、消费金额；手动录入3行数据，交互式输出数据表整体信息 + 消费金额均值。",
        "difficulty": "⭐⭐",
        "category": "Pandas基础",
        "estimated_time": "15分钟",
        "initial_code": '''import pandas as pd

data = {
    "订单号": ["OD001", "OD002", "OD003"],
    "用户ID": [1001, 1002, 1003],
    "消费金额": [99.5, 199.0, 49.9]
}
df = pd.DataFrame(data)
print("订单数据表：")
print(df)
print("\\n数据表基础描述统计：")
print(df.describe())
print(f"\\n平均消费金额：{df['消费金额'].mean():.2f}")
''',
        "key_concepts": ["Pandas数据结构", "DataFrame创建", "描述统计", "数据预览"]
    },
    {
        "id": 4,
        "name": "缺失值清洗实战",
        "subtitle": "Pandas空值填充",
        "description": "数据集存在消费金额缺失：df = pd.DataFrame({\"商品\":[\"A\",\"B\",\"C\",\"D\"], \"销量\":[120, None, 95, None]})，用均值填充销量空值，交互式输出清洗前后表格。",
        "difficulty": "⭐⭐",
        "category": "数据清洗",
        "estimated_time": "15分钟",
        "initial_code": '''import pandas as pd

df = pd.DataFrame({"商品":["A","B","C","D"], "销量":[120, None, 95, None]})
print("清洗前数据：")
print(df)

df["销量"] = df["销量"].fillna(df["销量"].mean())
print("\\n均值填充空值后数据：")
print(df)
''',
        "key_concepts": ["缺失值检测", "均值填充", "数据清洗", "fillna方法"]
    },
    {
        "id": 5,
        "name": "Matplotlib数据可视化",
        "subtitle": "月度流量柱状图",
        "description": "网站月度流量：月份 [1,2,3,4]，访问量 [3200,4500,3800,5200]，绘制柱状图，标题为「训练营网站月度访问量」，交互式展示图片。",
        "difficulty": "⭐⭐",
        "category": "数据可视化",
        "estimated_time": "15分钟",
        "initial_code": '''import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

months = [1, 2, 3, 4]
visits = [3200, 4500, 3800, 5200]

plt.figure(figsize=(10, 6))
plt.bar(months, visits, color='#3498db', width=0.6)
plt.title("训练营网站月度访问量", fontsize=14)
plt.xlabel("月份", fontsize=12)
plt.ylabel("访问量", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("图表已生成：柱状图展示了4个月的访问量数据")
print(f"最高访问量：{max(visits)} (第{months[visits.index(max(visits))]}月)")
print(f"平均访问量：{sum(visits)/len(visits):.0f}")
''',
        "key_concepts": ["Matplotlib基础", "柱状图", "图表美化", "中文显示"]
    },
    {
        "id": 6,
        "name": "Pandas数据筛选",
        "subtitle": "条件查询实战",
        "description": "创建员工数据表（姓名、部门、工资、工龄），练习使用布尔索引筛选高工资员工，筛选特定部门员工，多重条件筛选。",
        "difficulty": "⭐⭐",
        "category": "Pandas进阶",
        "estimated_time": "15分钟",
        "initial_code": '''import pandas as pd

data = {
    "姓名": ["张三", "李四", "王五", "赵六", "钱七", "孙八"],
    "部门": ["技术部", "市场部", "技术部", "财务部", "市场部", "技术部"],
    "工资": [8500, 6800, 12000, 7500, 5800, 15000],
    "工龄": [3, 2, 5, 4, 1, 6]
}
df = pd.DataFrame(data)

print("原始数据：")
print(df)

# 筛选工资大于8000的员工
high_salary = df[df["工资"] > 8000]
print("\\n高工资员工：")
print(high_salary)

# 筛选技术部员工
tech_staff = df[df["部门"] == "技术部"]
print("\\n技术部员工：")
print(tech_staff)

# 多重条件筛选
result = df[(df["工资"] > 7000) & (df["工龄"] >= 3)]
print("\\n工资>7000且工龄>=3年的员工：")
print(result)
''',
        "key_concepts": ["数据筛选", "条件查询", "布尔索引", "数据子集"]
    },
    {
        "id": 7,
        "name": "数据分组聚合分析",
        "subtitle": "groupby实战应用",
        "description": "使用销售数据练习groupby分组聚合操作：按地区分组统计销售额、按产品分组统计数量、多维度分组分析。",
        "difficulty": "⭐⭐⭐",
        "category": "数据分析",
        "estimated_time": "20分钟",
        "initial_code": '''import pandas as pd
import numpy as np

data = {
    "日期": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"] * 3,
    "地区": ["北京", "上海", "广州", "北京", "上海", "广州"] * 2 + ["北京", "上海", "广州"],
    "产品": ["手机", "电脑", "平板", "手机", "电脑", "平板", "电脑", "手机", "平板", "电脑", "手机", "平板", "手机", "电脑", "平板"],
    "销售额": [12000, 8500, 6800, 15000, 9200, 7200, 8800, 11500, 6500, 9500, 13000, 7000, 14000, 9800, 7500],
    "销量": [12, 5, 8, 15, 6, 9, 6, 11, 7, 5, 13, 8, 14, 7, 9]
}
df = pd.DataFrame(data)

print("原始销售数据：")
print(df.head())

# 按地区分组统计
region_stats = df.groupby("地区").agg({
    "销售额": ["sum", "mean", "max"],
    "销量": "sum"
}).round(0)
print("\\n按地区统计：")
print(region_stats)

# 按产品分组统计
product_stats = df.groupby("产品").agg({
    "销售额": ["sum", "mean"],
    "销量": "sum"
}).round(0)
print("\\n按产品统计：")
print(product_stats)

# 按地区+产品双重分组
combined = df.groupby(["地区", "产品"])["销售额"].sum().unstack()
print("\\n地区-产品销售矩阵：")
print(combined)
''',
        "key_concepts": ["分组聚合", "groupby", "多维度统计", "数据透视"]
    },
    {
        "id": 8,
        "name": "时间序列数据处理",
        "subtitle": "日期处理与趋势分析",
        "description": "使用Pandas处理时间序列数据：日期转换、时间索引、按日期排序、滚动窗口计算移动平均线、时间频率转换。",
        "difficulty": "⭐⭐⭐",
        "category": "数据分析",
        "estimated_time": "20分钟",
        "initial_code": '''import pandas as pd
import numpy as np

# 创建时间序列数据
dates = pd.date_range(start="2024-01-01", periods=30)
data = {
    "日期": dates,
    "销售额": np.random.randint(5000, 20000, size=30) + np.linspace(1000, 5000, 30),
    "访客数": np.random.randint(200, 800, size=30)
}
df = pd.DataFrame(data)

print("时间序列数据（前10行）：")
print(df.head(10))

# 将日期设为索引
df_indexed = df.set_index("日期")

# 按日期范围筛选
jan_data = df[(df["日期"] >= "2024-01-10") & (df["日期"] <= "2024-01-20")]
print("\\n1月10日-20日数据：")
print(f"销售额总计：{jan_data['销售额'].sum():,.0f}")

# 7日移动平均
df["7日移动平均"] = df["销售额"].rolling(window=7).mean()

# 计算周统计
df["周"] = df["日期"].dt.isocalendar().week
weekly_stats = df.groupby("周")["销售额"].agg(["sum", "mean"]).round(0)
print("\\n每周销售统计：")
print(weekly_stats)

print(f"\\n总销售额：{df['销售额'].sum():,.0f}")
print(f"日均销售额：{df['销售额'].mean():,.0f}")
print(f"最高销售额日期：{df.loc[df['销售额'].idxmax(), '日期']}")
''',
        "key_concepts": ["日期处理", "时间索引", "时序分析", "滚动窗口"]
    },
    {
        "id": 9,
        "name": "数据可视化进阶",
        "subtitle": "多图表组合展示",
        "description": "练习多种图表类型：折线图、饼图、散点图、热力图，并练习多图布局（subplot），创建完整的数据仪表板。",
        "difficulty": "⭐⭐⭐",
        "category": "数据可视化",
        "estimated_time": "25分钟",
        "initial_code": '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建示例数据
months = ["1月", "2月", "3月", "4月", "5月", "6月"]
sales = [45000, 52000, 48000, 61000, 58000, 72000]
categories = ["电子产品", "服装", "食品", "图书", "家居"]
category_sales = [35, 25, 20, 10, 10]

# 创建多图布局
fig = plt.figure(figsize=(14, 10))

# 图1：折线图
ax1 = plt.subplot(2, 2, 1)
ax1.plot(months, sales, marker='o', linewidth=2, color='#e74c3c')
ax1.set_title("月度销售趋势", fontsize=12)
ax1.set_xlabel("月份")
ax1.set_ylabel("销售额")
ax1.grid(True, alpha=0.3)
for i, v in enumerate(sales):
    ax1.text(i, v + 1500, str(v), ha='center')

# 图2：饼图
ax2 = plt.subplot(2, 2, 2)
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
ax2.pie(category_sales, labels=categories, autopct='%1.0f%%', colors=colors,
        shadow=True, startangle=90)
ax2.set_title("产品类别销售占比", fontsize=12)

# 图3：柱状图
ax3 = plt.subplot(2, 2, 3)
ax3.bar(months, sales, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c'])
ax3.set_title("月度销售额对比", fontsize=12)
ax3.set_xlabel("月份")
ax3.set_ylabel("销售额")
plt.setp(ax3.get_xticklabels(), rotation=15)

# 图4：面积图
ax4 = plt.subplot(2, 2, 4)
ax4.stackplot(months, sales, colors=['#3498db'], alpha=0.7)
ax4.set_title("销售额面积图", fontsize=12)
ax4.set_xlabel("月份")

plt.suptitle("销售数据可视化仪表板", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

print("可视化仪表板已生成，包含4种图表类型：")
print("1. 折线图 - 展示销售趋势")
print("2. 饼图 - 展示类别占比")
print("3. 柱状图 - 对比月度销售")
print("4. 面积图 - 展示整体销售体量")
''',
        "key_concepts": ["多图布局", "图表美化", "多种图表", "可视化设计"]
    },
    {
        "id": 10,
        "name": "综合数据分析报告",
        "subtitle": "从数据到洞察",
        "description": "综合运用所学知识：创建完整销售数据集、进行数据清洗、统计分析、可视化展示，并生成关键业务洞察和建议。",
        "difficulty": "⭐⭐⭐⭐",
        "category": "综合实战",
        "estimated_time": "30分钟",
        "initial_code": '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============= 1. 创建数据集 =============
np.random.seed(42)
n = 200
data = {
    "订单ID": [f"ORD{i:06d}" for i in range(1, n+1)],
    "日期": pd.date_range(start="2024-01-01", periods=n),
    "地区": np.random.choice(["北京", "上海", "广州", "深圳", "杭州"], n),
    "产品类别": np.random.choice(["电子产品", "服装", "食品", "图书", "家居"], n),
    "销售金额": np.random.randint(100, 5000, n).astype(float),
    "数量": np.random.randint(1, 10, n),
    "客户等级": np.random.choice(["普通", "银卡", "金卡", "钻石"], n)
}
df = pd.DataFrame(data)

# 添加一些缺失值（练习清洗）
df.loc[np.random.choice(n, 10), "销售金额"] = np.nan

print("=" * 60)
print("📊 综合数据分析报告")
print("=" * 60)

# ============= 2. 数据概览 =============
print("\\n【数据概览】")
print(f"总记录数: {len(df)} 条")
print(f"字段数量: {len(df.columns)} 个")
print(f"数据时间范围: {df['日期'].min()} 到 {df['日期'].max()}")

# ============= 3. 数据清洗 =============
print("\\n【数据清洗】")
missing_count = df["销售金额"].isnull().sum()
print(f"缺失值数量: {missing_count}")

# 用中位数填充缺失值
median_value = df["销售金额"].median()
df["销售金额"] = df["销售金额"].fillna(median_value)
print(f"已用中位数 {median_value:.0f} 填充缺失值")

# 计算总销售额
df["总销售额"] = df["销售金额"] * df["数量"]

# ============= 4. 核心指标 =============
print("\\n" + "=" * 40)
print("【核心业务指标】")
print("=" * 40)

total_revenue = df["总销售额"].sum()
total_quantity = df["数量"].sum()
avg_order_value = df["总销售额"].mean()
unique_regions = df["地区"].nunique()

print(f"总销售额: ¥{total_revenue:,.2f}")
print(f"总销售数量: {total_quantity} 件")
print(f"平均订单金额: ¥{avg_order_value:,.2f}")
print(f"覆盖地区数: {unique_regions} 个")

# ============= 5. 地区分析 =============
print("\\n【地区销售分析 TOP3】")
region_sales = df.groupby("地区")["总销售额"].sum().sort_values(ascending=False)
for region, value in region_sales.head(3).items():
    print(f"  {region}: ¥{value:,.2f} ({value/total_revenue*100:.1f}%)")

# ============= 6. 产品分析 =============
print("\\n【产品类别分析】")
category_data = df.groupby("产品类别").agg({
    "总销售额": "sum",
    "数量": "sum"
}).sort_values("总销售额", ascending=False)
for category, row in category_data.iterrows():
    print(f"  {category}: 销售额¥{row['总销售额']:,.0f}, 数量{row['数量']}件")

# ============= 7. 客户等级分析 =============
print("\\n【客户等级分析】")
customer_data = df.groupby("客户等级")["总销售额"].sum().sort_values(ascending=False)
for level, value in customer_data.items():
    print(f"  {level}客户: ¥{value:,.0f}")

# ============= 8. 数据洞察 =============
print("\\n" + "=" * 40)
print("【关键洞察与建议】")
print("=" * 40)

top_region = region_sales.index[0]
top_category = category_data.index[0]
print(f"1. 重点地区：{top_region}贡献最大销售额，应加大营销投入")
print(f"2. 优势品类：{top_category}销售领先，可作为核心产品推广")
print(f"3. 优化建议：高价值客户（金卡/钻石）应提供专属服务")
print(f"4. 增长机会：关注销售较低的地区，制定市场拓展策略")

print("\\n" + "=" * 60)
print("✅ 数据分析完成！共处理 {len(df)} 条订单数据")
print("=" * 60)
''',
        "key_concepts": ["数据分析流程", "综合应用", "数据洞察", "报告生成"]
    }
]


# ============== API路由 ==============

@app.get("/")
def root():
    """根路径测试"""
    return {"message": "欢迎使用AI数据分析训练营API", "version": "1.0.0"}


@app.get("/projects")
def get_projects():
    """获取所有项目列表"""
    return {
        "success": True,
        "total": len(PROJECTS_CONFIG),
        "projects": PROJECTS_CONFIG
    }


@app.get("/projects/{project_id}")
def get_project_detail(project_id: int):
    """获取单个项目详情"""
    for project in PROJECTS_CONFIG:
        if project["id"] == project_id:
            return {"success": True, "project": project}
    raise HTTPException(status_code=404, detail="项目不存在")


@app.post("/run-code")
def run_code(request: CodeRunRequest):
    """执行用户代码"""
    try:
        # 验证代码安全性
        is_valid, msg = executor.validate_code(request.code)
        if not is_valid:
            return {
                "success": False,
                "output": "",
                "error": msg,
                "execution_time": 0
            }

        # 准备上下文 - 导入常见数据分析库
        import pandas as pd
        import numpy as np

        # 创建一个安全的执行环境
        namespace = {
            'pd': pd,
            'np': np,
            '__name__': '__main__'
        }

        # 执行代码
        success, output, error, exec_time = executor.execute(
            request.code,
            context=namespace
        )

        return {
            "success": success,
            "output": output,
            "error": error,
            "execution_time": exec_time
        }

    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": f"系统错误: {str(e)}",
            "execution_time": 0
        }


@app.post("/score")
def score_code(request: ScoreRequest):
    """对用户答案进行评分"""
    try:
        result = scoring_engine.score_project(
            request.project_id,
            request.code,
            request.output,
            request.is_success
        )
        return {"success": True, "score_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评分失败: {str(e)}")


@app.post("/ai-feedback")
def get_ai_feedback(project_id: int, code: str, score: float, output: str = ""):
    """获取AI反馈建议"""
    try:
        feedback = ai_feedback.generate_feedback(project_id, code, score, output)
        return {"success": True, "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取反馈失败: {str(e)}")


@app.post("/save-progress")
def save_progress(request: ProgressRequest, db: Session = Depends(get_db)):
    """保存用户进度"""
    try:
        # 查找是否已有记录
        existing = db.query(UserProgress).filter(
            UserProgress.user_id == request.user_id,
            UserProgress.project_id == request.project_id
        ).first()

        if existing:
            # 更新记录
            existing.score = max(existing.score, request.score)
            existing.completed = 1 if request.completed else existing.completed
            existing.code = request.code
        else:
            # 创建新记录
            progress = UserProgress(
                user_id=request.user_id,
                project_id=request.project_id,
                project_name=request.project_name,
                score=request.score,
                completed=1 if request.completed else 0,
                attempts=1,
                code=request.code
            )
            db.add(progress)

        db.commit()
        return {"success": True, "message": "进度已保存"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")


@app.get("/progress/{user_id}")
def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    """获取用户所有学习进度"""
    try:
        progress_list = db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).all()

        completed_count = sum(1 for p in progress_list if p.completed)
        total_score = sum(p.score for p in progress_list)

        return {
            "success": True,
            "total_projects": len(PROJECTS_CONFIG),
            "completed_count": completed_count,
            "total_score": total_score,
            "progress": [
                {
                    "project_id": p.project_id,
                    "project_name": p.project_name,
                    "score": p.score,
                    "completed": bool(p.completed),
                    "attempts": p.attempts
                }
                for p in progress_list
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/record-learning")
def record_learning(user_id: str, project_id: int, action: str,
                     code: str = "", score: float = 0, db: Session = Depends(get_db)):
    """记录学习行为"""
    try:
        record = LearningRecord(
            user_id=user_id,
            project_id=project_id,
            action=action,
            code=code,
            score=score
        )
        db.add(record)
        db.commit()
        return {"success": True, "message": "学习记录已保存"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leaderboard/{project_id}")
def get_leaderboard(project_id: int, db: Session = Depends(get_db)):
    """获取项目排行榜"""
    try:
        entries = db.query(UserProgress).filter(
            UserProgress.project_id == project_id,
            UserProgress.score > 0
        ).order_by(UserProgress.score.desc()).limit(20).all()

        return {
            "success": True,
            "project_id": project_id,
            "leaderboard": [
                {
                    "rank": idx + 1,
                    "user_id": e.user_id[:8] + "...",
                    "score": e.score,
                    "attempts": e.attempts
                }
                for idx, e in enumerate(entries)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """获取整体统计数据"""
    try:
        total_users = db.query(UserProgress.user_id).distinct().count()
        total_attempts = db.query(UserProgress).count()
        avg_score = db.query(UserProgress).filter(UserProgress.score > 0).with_entities(
            db.query(UserProgress.score).filter(UserProgress.score > 0).scalar_subquery()
        ).count() or 0

        return {
            "success": True,
            "stats": {
                "total_projects": len(PROJECTS_CONFIG),
                "total_users": total_users,
                "total_attempts": total_attempts
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
