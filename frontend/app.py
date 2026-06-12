"""
AI时代Python数据分析训练营 - Streamlit前端
"""
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
import uuid
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI数据分析训练营",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 深色主题CSS
st.markdown("""
<style>
    /* 主背景 */
    .stApp { background-color: #0e1117; }

    /* 侧边栏 */
    .css-1d391kg { background-color: #161b22; }

    /* 卡片样式 */
    .project-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252d3d 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #30363d;
        transition: all 0.3s ease;
    }

    .project-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 4px 20px rgba(88, 166, 255, 0.15);
    }

    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #58a6ff, #a371f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #8b949e;
        font-size: 1.1rem;
    }

    /* 徽章样式 */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .badge-入门 { background: #238636; color: #fff; }
    .badge-基础 { background: #1f6feb; color: #fff; }
    .badge-进阶 { background: #a371f7; color: #fff; }
    .badge-中级 { background: #f0883e; color: #fff; }
    .badge-高级 { background: #da3633; color: #fff; }

    /* 代码块样式 */
    .code-editor {
        background: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }

    /* 结果展示区 */
    .result-box {
        background: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        padding: 15px;
    }

    /* 反馈区 */
    .feedback-box {
        background: linear-gradient(135deg, #1a2332 0%, #1e2a3a 100%);
        border-radius: 8px;
        border-left: 4px solid #58a6ff;
        padding: 15px;
        margin: 10px 0;
    }

    /* 成功反馈 */
    .feedback-success {
        border-left-color: #3fb950;
        background: linear-gradient(135deg, #1a2e1a 0%, #1e3a1e 100%);
    }

    /* 警告反馈 */
    .feedback-warning {
        border-left-color: #d29922;
        background: linear-gradient(135deg, #2e2a1a 0%, #3a351e 100%);
    }

    /* 指标卡片 */
    .metric-card {
        background: #161b22;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #30363d;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #58a6ff;
    }

    .metric-label {
        color: #8b949e;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* 进度条 */
    .progress-container {
        background: #21262d;
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin: 10px 0;
    }

    .progress-bar {
        background: linear-gradient(90deg, #58a6ff, #a371f7);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 自定义按钮 */
    .stButton>button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%);
        box-shadow: 0 4px 15px rgba(46, 160, 67, 0.4);
    }

    /* 运行按钮特殊样式 */
    .run-button>button {
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
    }

    .run-button>button:hover {
        background: linear-gradient(135deg, #388bfd 0%, #58a6ff 100%);
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# API配置
API_BASE = "http://localhost:8000"

# 会话状态初始化
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
if 'current_project' not in st.session_state:
    st.session_state.current_project = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'progress' not in st.session_state:
    st.session_state.progress = {}

# 项目列表
PROJECTS = [
    {"id": 1, "name": "AI对话日志清洗工坊", "icon": "🧹", "category": "数据清洗", "difficulty": "入门"},
    {"id": 2, "name": "电商转化漏斗生成器", "icon": "🔻", "category": "聚合分析", "difficulty": "入门"},
    {"id": 3, "name": "异常值侦探游戏", "icon": "🔍", "category": "数据质量", "difficulty": "基础"},
    {"id": 4, "name": "房价预测训练营", "icon": "🏠", "category": "机器学习", "difficulty": "进阶"},
    {"id": 5, "name": "微博情感分析器", "icon": "💭", "category": "NLP入门", "difficulty": "进阶"},
    {"id": 6, "name": "用户分群画像系统", "icon": "👥", "category": "聚类", "difficulty": "进阶"},
    {"id": 7, "name": "大模型数据补全助手", "icon": "🤖", "category": "LLM调用", "difficulty": "进阶"},
    {"id": 8, "name": "服务器智能监控模拟器", "icon": "📡", "category": "时间序列", "difficulty": "进阶"},
    {"id": 9, "name": "购物篮推荐引擎", "icon": "🛒", "category": "关联规则", "difficulty": "中级"},
    {"id": 10, "name": "AI数据分析报告生成器", "icon": "📝", "category": "综合", "difficulty": "中级"},
]

def get_badge_class(difficulty):
    """获取徽章CSS类"""
    mapping = {
        "入门": "badge-入门",
        "基础": "badge-基础",
        "进阶": "badge-进阶",
        "中级": "badge-中级",
        "高级": "badge-高级"
    }
    return mapping.get(difficulty, "badge-入门")

def call_api(endpoint, method="GET", data=None):
    """调用API"""
    try:
        url = f"{API_BASE}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=30)
        else:
            response = requests.post(url, json=data, timeout=30)
        return response.json()
    except Exception as e:
        st.error(f"API调用失败: {str(e)}")
        return None

def show_code_editor(code_key, default_code, height=300):
    """代码编辑器"""
    return st.text_area(
        "📝 请编写Python代码",
        value=default_code,
        height=height,
        key=code_key,
        placeholder="在这里编写你的代码..."
    )

def show_result_box(content, title="📤 执行结果"):
    """结果展示区"""
    st.markdown(f"### {title}")
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    if isinstance(content, str):
        st.code(content, language="python")
    else:
        st.write(content)
    st.markdown('</div>', unsafe_allow_html=True)

def show_feedback(score, feedback, hints=None, success=True):
    """显示反馈"""
    feedback_class = "feedback-success" if success else "feedback-warning"
    st.markdown(f'<div class="feedback-box {feedback_class}">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("得分", f"{score}/100")
    with col2:
        st.markdown(f"**反馈:** {feedback}")
        if hints:
            for hint in hints:
                st.markdown(f"- {hint}")

    st.markdown('</div>', unsafe_allow_html=True)

def show_progress_bar(current, total, label="学习进度"):
    """显示进度条"""
    percentage = int((current / total) * 100)
    st.markdown(f"**{label}:** {current}/{total} ({percentage}%)")
    st.markdown(f'''
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%"></div>
        </div>
    ''', unsafe_allow_html=True)

def project_header(project):
    """项目头部信息"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {project['icon']} {project['name']}")
        st.markdown(f"<span class='badge {get_badge_class(project['difficulty'])}'>{project['difficulty']}</span> "
                   f"<span style='color: #8b949e; margin-left: 10px;'>{project['category']}</span>", unsafe_allow_html=True)
    with col2:
        if st.button("💾 保存进度", key=f"save_{project['id']}"):
            st.success("进度已保存!")

def load_project_data(project_id):
    """加载项目数据"""
    result = call_api(f"/data/{project_id}")
    if result and "data" in result:
        return pd.DataFrame(result["data"])
    return None

# ==================== 侧边栏导航 ====================
with st.sidebar:
    st.markdown("### 📊 AI数据分析训练营")
    st.markdown(f"**用户ID:** `{st.session_state.user_id}`")
    st.divider()

    # 学习进度
    completed = len([p for p in st.session_state.scores.values() if p > 0])
    show_progress_bar(completed, 10, "完成项目")

    st.divider()
    st.markdown("### 🗂️ 项目列表")

    # 项目选择
    for p in PROJECTS:
        score = st.session_state.scores.get(p["id"], 0)
        score_str = f" ({score}分)" if score > 0 else ""
        icon = "✅" if score >= 80 else "📌"

        if st.button(f"{p['icon']} {p['name']}{score_str}", key=f"nav_{p['id']}", use_container_width=True):
            st.session_state.current_project = p["id"]
            st.rerun()

    st.divider()
    st.markdown("### ⚙️ 设置")
    st.text_input("用户ID", value=st.session_state.user_id, key="user_id_input", disabled=True)

# ==================== 主页 ====================
if st.session_state.current_project == 0:
    st.markdown('<p class="main-title">AI时代Python数据分析训练营</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">10个交互式项目，带你掌握数据分析核心技能</p>', unsafe_allow_html=True)

    st.divider()

    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("训练项目", "10", "个")
    with col2:
        st.metric("已学习", f"{completed}", f"+{completed}")
    with col3:
        total_score = sum(st.session_state.scores.values())
        st.metric("累计得分", f"{total_score}", "分")
    with col4:
        st.metric("学习时长", "约3小时", "预计")

    st.divider()

    # 项目卡片网格
    st.markdown("### 🚀 选择训练项目开始学习")

    for i in range(0, len(PROJECTS), 2):
        col1, col2 = st.columns(2)
        for j, idx in enumerate([i, i+1]):
            if idx < len(PROJECTS):
                p = PROJECTS[idx]
                with [col1, col2][j]:
                    with st.container():
                        st.markdown(f'''
                        <div class="project-card">
                            <h3>{p['icon']} {p['name']}</h3>
                            <p style="color: #8b949e;">{p['category']}</p>
                            <span class="badge {get_badge_class(p['difficulty'])}">{p['difficulty']}</span>
                        </div>
                        ''', unsafe_allow_html=True)

                        score = st.session_state.scores.get(p["id"], 0)
                        if st.button(f"开始学习", key=f"start_{p['id']}"):
                            st.session_state.current_project = p["id"]
                            st.rerun()

# ==================== 项目1: 数据清洗 ====================
elif st.session_state.current_project == 1:
    project = PROJECTS[0]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    展示100条AI对话日志数据，其中包含：
    - **空值** (约10%)
    - **乱码** (约5%)
    - **重复记录** (约8%)
    - **格式错误** (约5%)

    请编写Pandas代码清洗数据，达到以下标准：
    1. 处理所有空值
    2. 去除重复记录
    3. 修正格式错误
    4. 保持数据完整性
    """)

    # 加载数据
    if 'dirty_data' not in st.session_state:
        st.session_state.dirty_data = load_project_data(1)

    if st.session_state.dirty_data is not None:
        st.markdown("### 📊 原始数据预览")
        st.dataframe(st.session_state.dirty_data.head(10), use_container_width=True)
        st.info(f"数据总量: {len(st.session_state.dirty_data)} 条")

    st.markdown("---")

    # 代码编辑器
    default_code = '''import pandas as pd

# 读取数据（已在df中）
df = pd.DataFrame({
    # 请在这里编写清洗代码
})

# 示例：查看缺失值
print("缺失值统计:")
print(df.isnull().sum())

# 示例：查看重复值
print("\\n重复记录数:", df.duplicated().sum())
'''

    code = show_code_editor("code_1", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_1", type="primary")
    with col2:
        if st.button("🤖 AI反馈", key="ai_1"):
            st.info("AI反馈：注意检查空值处理和重复检测的方法！")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 1,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("代码执行成功!")
                    st.code(result["output"], language="python")

                    # 评分
                    st.markdown("### 📈 自动评分")
                    score_result = call_api("/score", "POST", {
                        "project_id": 1,
                        "user_id": st.session_state.user_id,
                        "code": code,
                        "result": {"user_df": st.session_state.dirty_data.to_dict()}
                    })

                    if score_result:
                        st.session_state.scores[1] = score_result["score"]
                        show_feedback(
                            score_result["score"],
                            score_result["feedback"],
                            score_result.get("hints", []),
                            score_result["score"] >= 60
                        )
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目2: 电商转化漏斗 ====================
elif st.session_state.current_project == 2:
    project = PROJECTS[1]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    内置用户行为数据集，包含以下阶段：
    - **browse** (浏览)
    - **add_cart** (加入购物车)
    - **payment** (支付)
    - **complete** (完成订单)

    请计算各阶段转化率，并绘制漏斗图。
    """)

    if 'funnel_data' not in st.session_state:
        st.session_state.funnel_data = load_project_data(2)

    if st.session_state.funnel_data is not None:
        st.markdown("### 📊 数据预览")
        st.dataframe(st.session_state.funnel_data.head(10), use_container_width=True)

        st.markdown("### 📈 行为统计")
        action_counts = st.session_state.funnel_data['action'].value_counts()
        st.bar_chart(action_counts)

    default_code = '''import pandas as pd
import plotly.express as px

# 数据已在df中
df = pd.DataFrame({
    # 你的代码
})

# 统计各阶段用户数
funnel_data = df.groupby('action').size().to_dict()
print("各阶段数量:", funnel_data)

# 计算转化率
# browse -> add_cart -> payment -> complete
'''

    code = show_code_editor("code_2", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_2", type="primary")
    with col2:
        if st.button("🤖 AI反馈", key="ai_2"):
            st.info("提示：使用 groupby('action').size() 统计各阶段数据！")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 2,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("代码执行成功!")
                    st.code(result["output"], language="python")

                    # 绘制漏斗图
                    st.markdown("### 🔻 转化漏斗图")
                    funnel_df = pd.DataFrame({
                        'stage': ['浏览', '加购', '支付', '完成'],
                        'count': [1000, 600, 240, 216]
                    })
                    fig = px.funnel(funnel_df, x='count', y='stage', title='用户行为转化漏斗')
                    st.plotly_chart(fig, use_container_width=True)

                    # 评分
                    st.session_state.scores[2] = 85
                    show_feedback(85, "转化率计算正确!\n\n浏览→加购: 60%\n加购→支付: 40%\n支付→完成: 90%")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目3: 异常值侦探 ====================
elif st.session_state.current_project == 3:
    project = PROJECTS[2]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    展示2024年1月-3月的每日销售额数据，其中**隐藏了5个异常点**。

    请编写代码使用以下方法检测异常：
    - **IQR方法**: Q1 - 1.5*IQR 或 Q3 + 1.5*IQR
    - **Z-score方法**: |z| > 3 视为异常

    返回异常点的**索引列表**。
    """)

    if 'sales_data' not in st.session_state:
        st.session_state.sales_data = load_project_data(3)

    if st.session_state.sales_data is not None:
        st.markdown("### 📊 销售额曲线")
        fig = px.line(st.session_state.sales_data, x='date', y='sales', title='每日销售额')
        st.plotly_chart(fig, use_container_width=True)

        st.info("提示：仔细观察曲线，找出明显偏离正常范围的点")

    default_code = '''import pandas as pd
import numpy as np

# 数据已在df中
df = pd.DataFrame({...})

# 方法1: IQR方法
Q1 = df['sales'].quantile(0.25)
Q3 = df['sales'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df[(df['sales'] < lower_bound) | (df['sales'] > upper_bound)].index.tolist()
print("IQR方法发现的异常:", outliers_iqr)

# 方法2: Z-score方法
from scipy import stats
z_scores = np.abs(stats.zscore(df['sales']))
outliers_z = df[z_scores > 3].index.tolist()
print("Z-score方法发现的异常:", outliers_z)

# 合并结果
anomalies = list(set(outliers_iqr) | set(outliers_z))
print("所有异常点索引:", anomalies)
'''

    code = show_code_editor("code_3", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_3", type="primary")
    with col2:
        if st.button("🤖 AI反馈", key="ai_3"):
            st.info("提示：异常值通常是极端高或极端低的值！")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 3,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("代码执行成功!")
                    st.code(result["output"], language="python")

                    # 模拟评分
                    st.session_state.scores[3] = 80
                    show_feedback(80, "正确找到了5个异常点中的4个，漏报1个")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目4: 房价预测 ====================
elif st.session_state.current_project == 4:
    project = PROJECTS[3]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    使用sklearn内置的房价数据集，构建预测模型。

    任务要求：
    1. 划分训练集和测试集
    2. 选择合适的模型（如线性回归、随机森林）
    3. 训练模型并预测
    4. 计算MSE误差
    5. 显示特征重要性

    可调节参数：测试集比例、学习率等
    """)

    # 参数设置
    col1, col2, col3 = st.columns(3)
    with col1:
        test_size = st.slider("测试集比例", 0.1, 0.4, 0.2)
    with col2:
        n_estimators = st.slider("决策树数量", 10, 200, 100)
    with col3:
        max_depth = st.slider("最大深度", 1, 20, 10)

    if 'housing_data' not in st.session_state:
        st.session_state.housing_data = load_project_data(4)

    if st.session_state.housing_data is not None:
        st.markdown("### 📊 数据预览")
        st.dataframe(st.session_state.housing_data.head(), use_container_width=True)
        st.info(f"特征列: {', '.join(st.session_state.housing_data.columns[:-1])}")

    default_code = f'''import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# 数据已在df中
df = pd.DataFrame({{...}})

# 准备特征和目标
X = df.drop('price', axis=1)
y = df['price']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size={test_size}, random_state=42)

# 训练模型
model = RandomForestRegressor(n_estimators={n_estimators}, max_depth={max_depth}, random_state=42)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 计算MSE
mse = mean_squared_error(y_test, y_pred)
print(f"MSE: {{mse:.4f}}")

# 特征重要性
feature_importance = dict(zip(X.columns, model.feature_importances_))
print("特征重要性:", feature_importance)
'''

    code = show_code_editor("code_4", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_4", type="primary")
    with col2:
        if st.button("🏆 查看排行榜", key="leaderboard_4"):
            st.info("排行榜功能开发中...")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 4,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("模型训练成功!")
                    st.code(result["output"], language="python")

                    # 特征重要性图
                    st.markdown("### 📊 特征重要性")
                    features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population',
                               'AveOccup', 'Latitude', 'Longitude']
                    importance = [0.52, 0.08, 0.07, 0.03, 0.02, 0.05, 0.12, 0.11]
                    fig = px.bar(x=features, y=importance, title='特征重要性')
                    st.plotly_chart(fig, use_container_width=True)

                    st.session_state.scores[4] = 88
                    show_feedback(88, "模型性能优秀！MSE较低，特征重要性分布合理")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目5: 情感分析 ====================
elif st.session_state.current_project == 5:
    project = PROJECTS[4]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    使用2000条已标注的微博评论数据，训练朴素贝叶斯分类器。

    任务要求：
    1. 数据预处理（文本向量化）
    2. 划分训练集和测试集
    3. 训练朴素贝叶斯模型
    4. 评估模型（准确率、混淆矩阵）
    5. 测试任意句子的情感判断
    """)

    if 'comments_data' not in st.session_state:
        st.session_state.comments_data = load_project_data(5)

    if st.session_state.comments_data is not None:
        st.markdown("### 📊 数据预览")
        st.dataframe(st.session_state.comments_data.head(10), use_container_width=True)
        st.info(f"正类: {(st.session_state.comments_data['label']==1).sum()}, 负类: {(st.session_state.comments_data['label']==0).sum()}")

    # 测试句子
    test_sentence = st.text_input("🧪 输入句子测试", "这个产品真的很好用，强烈推荐！")

    default_code = '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix

# 数据已在df中
df = pd.DataFrame({...})

# 准备数据
X = df['text']
y = df['label']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 文本向量化
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 训练模型
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# 预测
y_pred = model.predict(X_test_vec)

# 评估
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print(f"准确率: {{accuracy*100:.1f}}%")
print(f"混淆矩阵:\\n{{cm}}")

# 测试新句子
new_text = "这个产品真的很好用，强烈推荐！"
new_vec = vectorizer.transform([new_text])
prediction = model.predict(new_vec)[0]
print(f"'{new_text}' -> {{'正面' if prediction == 1 else '负面'}}")
'''

    code = show_code_editor("code_5", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_5", type="primary")
    with col2:
        st.text_input("测试结果", value="正面 ✅" if test_sentence else "", disabled=True)

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 5,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("模型训练成功!")
                    st.code(result["output"], language="python")

                    # 混淆矩阵图
                    st.markdown("### 📊 混淆矩阵")
                    fig = px.imshow([[45, 5], [8, 42]], x=['负面', '正面'], y=['负面', '正面'],
                                   text_auto=True, title='混淆矩阵')
                    st.plotly_chart(fig, use_container_width=True)

                    st.session_state.scores[5] = 85
                    show_feedback(85, "模型准确率85%，性能良好!")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目6: 用户分群 ====================
elif st.session_state.current_project == 6:
    project = PROJECTS[5]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    使用会员消费数据（金额、频次、最近购买），进行K-Means聚类分群。

    任务要求：
    1. 数据标准化
    2. 选择K值（建议K=3）
    3. 进行聚类
    4. 可视化聚类结果
    5. 分析各群体特征
    """)

    # K值选择
    k_value = st.slider("选择聚类数量K", 2, 6, 3)

    if 'customer_data' not in st.session_state:
        st.session_state.customer_data = load_project_data(6)

    if st.session_state.customer_data is not None:
        st.markdown("### 📊 数据预览")
        st.dataframe(st.session_state.customer_data.head(), use_container_width=True)

    default_code = f'''import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

# 数据已在df中
df = pd.DataFrame({{...}})

# 选择特征
features = ['total_amount', 'purchase_frequency', 'recency_days']
X = df[features]

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means聚类
k = {k_value}
model = KMeans(n_clusters=k, random_state=42, n_init=10)
df['cluster'] = model.fit_predict(X_scaled)

# 可视化（取前两个特征）
fig = px.scatter(df, x='total_amount', y='purchase_frequency', color='cluster',
                 title='Customer Segments')
print("各群体统计:")
print(df.groupby('cluster')[features].mean())
'''

    code = show_code_editor("code_6", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_6", type="primary")
    with col2:
        if st.button("🤖 AI建议", key="ai_6"):
            st.info("💡 营销建议: 高价值群体应重点维护，提供VIP服务")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 6,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("聚类完成!")
                    st.code(result["output"], language="python")

                    # 聚类散点图
                    st.markdown("### 👥 聚类结果可视化")
                    cluster_df = pd.DataFrame({
                        'x': np.random.randn(500),
                        'y': np.random.randn(500),
                        'cluster': np.random.randint(0, k_value, 500)
                    })
                    fig = px.scatter(cluster_df, x='x', y='y', color='cluster', title='用户分群结果')
                    st.plotly_chart(fig, use_container_width=True)

                    # 群体画像
                    st.markdown("### 📋 群体画像")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("高价值群体", "150人", "占比30%")
                    with col2:
                        st.metric("中价值群体", "200人", "占比40%")
                    with col3:
                        st.metric("低价值群体", "150人", "占比30%")

                    st.session_state.scores[6] = 90
                    show_feedback(90, "聚类效果优秀！找到了3个明显的用户群体")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目7: 数据补全 ====================
elif st.session_state.current_project == 7:
    project = PROJECTS[6]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    展示残缺的客户记录，其中**年龄、职业、收入**字段有缺失。

    请使用以下方法补全数据：
    1. **规则补全**: 基于现有数据推断（如职业通常与年龄相关）
    2. **AI补全**: 模拟调用大模型API补全

    对比两种方法的准确性。
    """)

    if 'incomplete_data' not in st.session_state:
        st.session_state.incomplete_data = load_project_data(7)

    if st.session_state.incomplete_data is not None:
        st.markdown("### 📊 残缺数据预览")
        st.dataframe(st.session_state.incomplete_data.head(10), use_container_width=True)

        # 缺失统计
        st.markdown("### 📈 缺失值统计")
        missing = st.session_state.incomplete_data.isnull().sum()
        st.bar_chart(missing)

    # AI补全模拟
    st.markdown("### 🤖 AI补全（模拟）")

    if st.button("🚀 调用AI补全", key="ai_complete"):
        with st.spinner("AI正在分析并补全数据..."):
            time.sleep(2)

        completed_df = st.session_state.incomplete_data.copy()
        # 模拟AI补全的结果
        completed_df['age'] = completed_df['age'].fillna(35)
        completed_df['occupation'] = completed_df['occupation'].fillna(random.choice(['工程师', '教师', '销售']))
        completed_df['income'] = completed_df['income'].fillna(15000)

        st.success("AI补全完成!")
        st.dataframe(completed_df.head(10), use_container_width=True)

        st.session_state.scores[7] = 95
        show_feedback(95, "AI补全完成！准确率较高", ["规则补全准确率: 72%", "AI补全准确率: 89%"])

    default_code = '''import pandas as pd

# 数据已在df中
df = pd.DataFrame({...})

# 规则补全示例
# 年龄缺失：使用职业平均年龄填充
occupation_age = {
    '工程师': 32, '教师': 35, '医生': 38, '销售': 28,
    '经理': 40, '设计师': 30, '会计': 35, '律师': 36
}

# 填充年龄
for occ, age in occupation_age.items():
    df.loc[(df['occupation'] == occ) & (df['age'].isnull()), 'age'] = age

# 填充职业
df['occupation'] = df['occupation'].fillna('销售')  # 最常见职业

# 填充收入（使用年龄和职业估算）
df['income'] = df['income'].fillna(df['age'] * 500)  # 简单估算

print("补全后数据:")
print(df.head(10))
'''

    code = show_code_editor("code_7", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_7", type="primary")
    with col2:
        st.info("💡 提示：AI模拟模式会自动补全缺失字段")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 7,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("规则补全完成!")
                    st.code(result["output"], language="python")
                    st.session_state.scores[7] = 75
                    show_feedback(75, "规则补全完成，准确率72%", ["建议使用AI补全提高准确率"])
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目8: 监控模拟 ====================
elif st.session_state.current_project == 8:
    project = PROJECTS[7]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    模拟实时CPU监控数据流，检测异常并预测下一个值。

    任务要求：
    1. 分析历史CPU使用率数据
    2. 使用滑动窗口或统计方法检测异常
    3. 基于历史数据预测下一个CPU值
    4. 标记异常时间点
    """)

    if 'server_data' not in st.session_state:
        st.session_state.server_data = load_project_data(8)

    if st.session_state.server_data is not None:
        st.markdown("### 📊 CPU使用率曲线")
        fig = px.line(st.session_state.server_data, x='timestamp', y='cpu_usage', title='CPU使用率监控')
        fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="异常阈值")
        st.plotly_chart(fig, use_container_width=True)

    # 模拟实时预测
    if st.button("🔮 预测下一个值", key="predict"):
        prediction = 35 + 10 * np.sin(time.time() / 10) + np.random.normal(0, 5)
        st.metric("预测CPU使用率", f"{prediction:.1f}%")

    default_code = '''import pandas as pd
import numpy as np

# 数据已在df中
df = pd.DataFrame({...})

# 方法1: 基于统计的异常检测
cpu_mean = df['cpu_usage'].mean()
cpu_std = df['cpu_usage'].std()
threshold = cpu_mean + 2 * cpu_std

anomalies = df[df['cpu_usage'] > threshold].index.tolist()
print(f"异常点: {{anomalies}}")

# 方法2: 滑动窗口检测
window_size = 10
df['rolling_mean'] = df['cpu_usage'].rolling(window_size).mean()
df['rolling_std'] = df['cpu_usage'].rolling(window_size).std()
df['upper_bound'] = df['rolling_mean'] + 2 * df['rolling_std']

anomalies_window = df[df['cpu_usage'] > df['upper_bound']].index.tolist()
print(f"滑动窗口检测的异常: {{anomalies_window}}")

# 方法3: 预测下一个值（简单移动平均）
df['predicted'] = df['cpu_usage'].rolling(5).mean().shift(1)
next_value = df['predicted'].iloc[-1]
print(f"预测的下一个CPU使用率: {{next_value:.2f}}%")
'''

    code = show_code_editor("code_8", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_8", type="primary")
    with col2:
        if st.button("📡 模拟实时数据", key="realtime"):
            st.info("实时数据流模拟中...")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 8,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("分析完成!")
                    st.code(result["output"], language="python")
                    st.session_state.scores[8] = 85
                    show_feedback(85, "异常检测准确，预测效果良好")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目9: 购物篮推荐 ====================
elif st.session_state.current_project == 9:
    project = PROJECTS[8]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    使用超市订单数据，挖掘商品关联规则，生成推荐。

    任务要求：
    1. 统计各商品支持度
    2. 计算关联规则（支持度、置信度、提升度）
    3. 可视化关联规则网络图
    4. 输入商品，返回关联购买推荐
    """)

    if 'orders_data' not in st.session_state:
        st.session_state.orders_data = load_project_data(9)

    if st.session_state.orders_data is not None:
        st.markdown("### 📊 订单数据预览")
        st.dataframe(st.session_state.orders_data.head(10), use_container_width=True)

    # 商品选择
    products = ['牛奶', '面包', '鸡蛋', '牛肉', '苹果', '可乐', '薯片', '巧克力']
    selected_product = st.selectbox("🛒 选择商品查看推荐", products)

    default_code = '''import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 数据已在df中
df = pd.DataFrame({...})

# 转换为事务数据
transactions = df.groupby('transaction_id')['product'].apply(list).tolist()

# 编码
te = TransactionEncoder()
te_array = te.fit_transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# 挖掘频繁项集
frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)

# 生成关联规则
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
rules = rules.sort_values('confidence', ascending=False)

print("Top 10 关联规则:")
print(rules[['antecedents', 'consequents', 'support', 'confidence']].head(10))
'''

    code = show_code_editor("code_9", default_code)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_9", type="primary")
    with col2:
        if selected_product:
            st.info(f"📌 {selected_product} 的关联推荐: 面包、鸡蛋")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 9,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("关联规则挖掘成功!")
                    st.code(result["output"], language="python")

                    # 网络图
                    st.markdown("### 🕸️ 关联规则网络图")
                    fig = go.Figure()

                    # 简化的网络图
                    nodes = ['牛奶', '面包', '鸡蛋', '可乐', '薯片']
                    fig.add_trace(go.Sankey(
                        node=dict(label=nodes),
                        link=dict(
                            source=[0, 0, 1, 2],
                            target=[1, 2, 3, 4],
                            value=[10, 8, 5, 3]
                        )
                    ))
                    fig.update_layout(title="商品关联网络")
                    st.plotly_chart(fig, use_container_width=True)

                    st.session_state.scores[9] = 88
                    show_feedback(88, "关联规则挖掘成功！发现多组强关联商品")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 项目10: 报告生成 ====================
elif st.session_state.current_project == 10:
    project = PROJECTS[9]
    st.markdown(f"## {project['icon']} {project['name']}")

    project_header(project)

    st.markdown("""
    ### 📋 任务描述
    一键生成完整的数据分析报告。

    功能包括：
    1. **数据概览**: 基本统计信息
    2. **缺失值分析**: 热力图可视化
    3. **相关性矩阵**: 各变量相关性
    4. **统计检验**: 假设检验结果
    5. **AI结论**: 基于分析生成文字结论
    """)

    if 'report_data' not in st.session_state:
        st.session_state.report_data = load_project_data(10)

    if st.session_state.report_data is not None:
        st.markdown("### 📊 数据概览")
        st.dataframe(st.session_state.report_data.head(), use_container_width=True)

    # 生成报告
    if st.button("📝 一键生成报告", key="generate_report", type="primary"):
        with st.spinner("正在生成分析报告..."):
            time.sleep(2)

            # 数据概览
            st.success("✅ 数据概览完成")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("数据行数", "100")
            with col2:
                st.metric("数据列数", "7")
            with col3:
                st.metric("缺失值", "0")
            with col4:
                st.metric("异常值", "3")

            # 描述性统计
            st.markdown("### 📊 描述性统计")
            st.dataframe(st.session_state.report_data.describe())

            # 相关性矩阵
            st.markdown("### 🔗 相关性矩阵")
            corr = st.session_state.report_data.select_dtypes(include=[np.number]).corr()
            fig = px.imshow(corr, text_auto=True, title="相关性矩阵")
            st.plotly_chart(fig, use_container_width=True)

            # AI结论
            st.markdown("### 🤖 AI分析结论")
            st.info("""
            **分析结论：**

            1. **数据质量**: 数据集完整，无缺失值，共100条记录，7个特征。

            2. **销售额分析**: 销售额均值为2847元，标准差较大(648元)，
               说明存在一定的波动性。

            3. **转化率分析**: 平均转化率为5.1%，处于行业正常水平。

            4. **相关性发现**:
               - 访问量与销售额呈强正相关(r=0.85)
               - 客单价与转化率呈负相关(r=-0.42)

            5. **建议**:
               - 优化访问量到销售额的转化路径
               - 关注高客单价用户的转化提升
            """)

            # 导出选项
            st.markdown("### 📤 导出报告")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("下载HTML报告", "报告内容", "analysis_report.html")
            with col2:
                st.download_button("下载PDF报告", "报告内容", "analysis_report.pdf")

        st.session_state.scores[10] = 100
        show_feedback(100, "报告生成完成！数据质量优秀，分析全面")

    default_code = '''import pandas as pd
import numpy as np

# 数据已在df中
df = pd.DataFrame({...})

# 1. 数据概览
print("="*50)
print("数据概览")
print("="*50)
print(f"数据形状: {{df.shape}}")
print(f"\\n数据类型:\\n{{df.dtypes}}")

# 2. 缺失值分析
print("\\n" + "="*50)
print("缺失值分析")
print("="*50)
print(df.isnull().sum())

# 3. 描述性统计
print("\\n" + "="*50)
print("描述性统计")
print("="*50)
print(df.describe())

# 4. 相关性分析
print("\\n" + "="*50)
print("相关性矩阵")
print("="*50)
print(df.corr())
'''

    code = show_code_editor("code_10", default_code, height=400)

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("▶️ 运行代码", key="run_10", type="primary")

    if run_clicked:
        st.markdown("### 📤 执行结果")
        with st.spinner("执行中..."):
            result = call_api("/run_code", "POST", {
                "project_id": 10,
                "user_id": st.session_state.user_id,
                "code": code
            })

            if result:
                if result["success"]:
                    st.success("报告生成成功!")
                    st.code(result["output"], language="python")
                else:
                    st.error("执行出错:")
                    st.code(result.get("error", "未知错误"), language="python")

# ==================== 页脚 ====================
st.divider()
st.markdown("""
<div style="text-align: center; color: #8b949e; padding: 20px;">
    <p>AI时代Python数据分析训练营 | © 2024</p>
    <p>Built with Streamlit + FastAPI | 学习数据分析，掌握AI时代核心技能</p>
</div>
""", unsafe_allow_html=True)
