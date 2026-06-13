"""
AI时代Python数据分析训练营 - 首页/项目页/习题页 统一渲染
科技感深色主题，10个交互式训练项目 × 10道课后习题
"""
import streamlit as st
import pandas as pd
import numpy as np
import uuid
import io
import sys
import os
import time
import matplotlib
matplotlib.use("Agg")  # 服务端不显示窗口
import matplotlib.pyplot as plt
import json

# 确保从项目根目录加载子模块
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from frontend.quiz_engine import render_question, render_progress_panel, run_code_sandbox
from backend.quiz_bank import QUIZ_BANK, get_project_quiz


# ============================================================
# 10 个训练项目配置（与后端保持一致，精简描述字段以便显示）
# ============================================================
PROJECTS = [
    {
        "id": 1, "name": "Python基础交互式计算", "subtitle": "营收求和练习",
        "icon": "🐍", "difficulty": "⭐",
        "description": "某门店3天销售额分别为 [1280, 2560, 1890]，用Python列表遍历计算总销售额、日均销售额，交互式打印结果。",
        "concepts": ["列表操作", "循环遍历", "格式化输出"],
        "initial_code": (
            "sales = [1280, 2560, 1890]\n"
            "total = sum(sales)\n"
            "avg = total / len(sales)\n"
            "print(f'总销售额：{total} 元')\n"
            "print(f'日均销售额：{avg:.2f} 元')"
        ),
    },
    {
        "id": 2, "name": "NumPy数组批量运算", "subtitle": "用户量翻倍计算",
        "icon": "🔢", "difficulty": "⭐",
        "description": "导入 numpy，构建数组 arr = np.array([120, 245, 368, 412])，每个用户量上浮 15%，保留整数输出新数组。",
        "concepts": ["NumPy数组", "向量运算", "类型转换"],
        "initial_code": (
            "import numpy as np\n\n"
            "user_arr = np.array([120, 245, 368, 412])\n"
            "new_user = np.round(user_arr * 1.15).astype(int)\n"
            "print('上浮15%后的用户数组：', new_user)"
        ),
    },
    {
        "id": 3, "name": "Pandas创建数据表", "subtitle": "电商订单分析",
        "icon": "📋", "difficulty": "⭐⭐",
        "description": "用Pandas构建电商订单DataFrame，字段：订单号、用户ID、消费金额；手动录入3行数据，交互式输出数据表整体信息 + 消费金额均值。",
        "concepts": ["DataFrame", "描述统计", "数据预览"],
        "initial_code": (
            "import pandas as pd\n\n"
            "data = {\n"
            "    '订单号': ['OD01', 'OD02', 'OD03'],\n"
            "    '用户ID': [1001, 1002, 1003],\n"
            "    '消费金额': [99.5, 199.0, 49.9]\n"
            "}\n"
            "df = pd.DataFrame(data)\n"
            "print('订单数据表：')\n"
            "print(df)\n"
            "print('\\n数据表基础描述统计：')\n"
            "print(df.describe())\n"
            "print(f'\\n平均消费金额：{df[\"消费金额\"].mean():.2f}')"
        ),
    },
    {
        "id": 4, "name": "缺失值清洗实战", "subtitle": "Pandas空值填充",
        "icon": "🧹", "difficulty": "⭐⭐",
        "description": "数据集存在消费金额缺失：df = pd.DataFrame({'商品': ['A','B','C','D'], '销量': [120, None, 95, None]})，用均值填充销量空值，交互式输出清洗前后表格。",
        "concepts": ["缺失值", "均值填充", "数据清洗"],
        "initial_code": (
            "import pandas as pd\n\n"
            "df = pd.DataFrame({'商品': ['A', 'B', 'C', 'D'], '销量': [120, None, 95, None]})\n"
            "print('清洗前数据：')\n"
            "print(df)\n\n"
            "df['销量'] = df['销量'].fillna(df['销量'].mean())\n"
            "print('\\n均值填充空值后数据：')\n"
            "print(df)"
        ),
    },
    {
        "id": 5, "name": "Matplotlib数据可视化", "subtitle": "月度流量柱状图",
        "icon": "📊", "difficulty": "⭐⭐",
        "description": "网站月度流量：月份 [1,2,3,4]，访问量 [3200,4500,3800,5200]，绘制柱状图，标题为「训练营网站月度访问量」。",
        "concepts": ["柱状图", "图表美化", "中文显示"],
        "initial_code": (
            "import matplotlib.pyplot as plt\n\n"
            "plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']\n"
            "plt.rcParams['axes.unicode_minus'] = False\n\n"
            "months = [1, 2, 3, 4]\n"
            "visits = [3200, 4500, 3800, 5200]\n"
            "plt.figure(figsize=(8, 5))\n"
            "plt.bar(months, visits, color='#00d4ff')\n"
            "plt.title('训练营网站月度访问量')\n"
            "plt.xlabel('月份')\n"
            "plt.ylabel('访问量')\n"
            "plt.grid(True, alpha=0.3)\n"
            "plt.show()\n\n"
            "print(f'最高访问量：{max(visits)}，平均访问量：{sum(visits)/len(visits):.0f}')"
        ),
    },
    {
        "id": 6, "name": "Pandas数据筛选", "subtitle": "高阶条件提取",
        "icon": "🔍", "difficulty": "⭐⭐",
        "description": "员工数据表（姓名、部门、工资、工龄），练习布尔索引筛选高工资员工、特定部门员工、多重条件筛选。",
        "concepts": ["布尔索引", "多条件筛选", "数据子集"],
        "initial_code": (
            "import pandas as pd\n\n"
            "data = {\n"
            "    '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],\n"
            "    '部门': ['技术部', '市场部', '技术部', '财务部', '市场部', '技术部'],\n"
            "    '工资': [8500, 6800, 12000, 7500, 5800, 15000],\n"
            "    '工龄': [3, 2, 5, 4, 1, 6]\n"
            "}\n"
            "df = pd.DataFrame(data)\n\n"
            "print('高工资员工(工资>8000)：')\n"
            "print(df[df['工资'] > 8000])\n"
            "print('\\n技术部员工：')\n"
            "print(df[df['部门'] == '技术部'])\n"
            "print('\\n工资>7000且工龄>=3年：')\n"
            "print(df[(df['工资'] > 7000) & (df['工龄'] >= 3)])"
        ),
    },
    {
        "id": 7, "name": "groupby分组聚合", "subtitle": "多维度统计分析",
        "icon": "📊", "difficulty": "⭐⭐⭐",
        "description": "销售数据练习 groupby 分组聚合操作：按地区分组统计销售额、按产品分组、按地区+产品双重分组。",
        "concepts": ["groupby", "聚合函数", "多维度统计"],
        "initial_code": (
            "import pandas as pd\n\n"
            "data = {\n"
            "    '地区': ['北京', '上海', '广州', '北京', '上海', '广州', '北京', '上海', '广州'],\n"
            "    '产品': ['手机', '电脑', '平板', '电脑', '手机', '平板', '手机', '电脑', '平板'],\n"
            "    '销售额': [12000, 8500, 6800, 15000, 9200, 7200, 13000, 9800, 7500],\n"
            "    '销量': [12, 5, 8, 15, 6, 9, 13, 7, 9]\n"
            "}\n"
            "df = pd.DataFrame(data)\n\n"
            "print('==== 按地区统计销售额 ====')\n"
            "print(df.groupby('地区')['销售额'].sum())\n"
            "print('\\n==== 按产品统计销量 ====')\n"
            "print(df.groupby('产品')['销量'].sum())\n"
            "print('\\n==== 地区-产品矩阵 ====')\n"
            "print(df.groupby(['地区', '产品'])['销售额'].sum().unstack())"
        ),
    },
    {
        "id": 8, "name": "3σ原则异常值剔除", "subtitle": "极端数据检测",
        "icon": "⚡", "difficulty": "⭐⭐⭐",
        "description": "使用3σ原则识别并剔除消费金额中的异常值，学习标准差、区间筛选的方法。",
        "concepts": ["标准差", "3σ准则", "区间筛选"],
        "initial_code": (
            "import numpy as np\n\n"
            "consume = np.array([20, 25, 18, 22, 28, 200, 19, 24, 26, 23, 21, 25])\n"
            "mu = consume.mean()\n"
            "sigma = consume.std()\n"
            "low, high = mu - 3 * sigma, mu + 3 * sigma\n"
            "print(f'均值={mu:.2f}, 标准差={sigma:.2f}')\n"
            "print(f'正常区间: [{low:.2f}, {high:.2f}]')\n\n"
            "normal = consume[(consume >= low) & (consume <= high)]\n"
            "anomaly = consume[(consume < low) | (consume > high)]\n"
            "print(f'正常数据：{normal}')\n"
            "print(f'异常数据：{anomaly}')"
        ),
    },
    {
        "id": 9, "name": "批量导出分析结果", "subtitle": "保存Excel/CSV",
        "icon": "📤", "difficulty": "⭐⭐",
        "description": "练习将分析结果导出为 Excel / CSV 文件，理解 index=False 的作用与 openpyxl 依赖。",
        "concepts": ["to_excel", "to_csv", "index 参数"],
        "initial_code": (
            "import pandas as pd\n\n"
            "data = {\n"
            "    '产品': ['A', 'B', 'C', 'D'],\n"
            "    '销量': [120, 200, 150, 90],\n"
            "    '销售额': [12000, 18000, 15000, 7200]\n"
            "}\n"
            "df = pd.DataFrame(data)\n\n"
            "print('原始数据表：')\n"
            "print(df)\n\n"
            "df.to_csv('sales_report.csv', index=False, encoding='utf-8-sig')\n"
            "print('\\n✅ CSV 已导出: sales_report.csv')\n\n"
            "try:\n"
            "    df.to_excel('sales_report.xlsx', index=False)\n"
            "    print('✅ Excel 已导出: sales_report.xlsx')\n"
            "except Exception as e:\n"
            "    print(f'(跳过 Excel 导出: {e})')"
        ),
    },
    {
        "id": 10, "name": "AI线性回归预测", "subtitle": "历史流量预测",
        "icon": "🤖", "difficulty": "⭐⭐⭐⭐",
        "description": "综合运用：用 scikit-learn 的 LinearRegression 基于历史月份-流量数据训练模型，预测下月访问量。",
        "concepts": ["线性回归", "模型训练", "预测"],
        "initial_code": (
            "import numpy as np\n"
            "from sklearn.linear_model import LinearRegression\n\n"
            "# 历史数据：月份[1..6]，访问量[100..600]\n"
            "X = np.array([[1], [2], [3], [4], [5], [6]])\n"
            "y = np.array([120, 180, 250, 310, 400, 480])\n\n"
            "model = LinearRegression()\n"
            "model.fit(X, y)\n\n"
            "print(f'斜率: {model.coef_[0]:.2f}')\n"
            "print(f'截距: {model.intercept_:.2f}')\n"
            "print(f'R² 拟合度: {model.score(X, y):.4f}')\n\n"
            "next_month = [[7]]\n"
            "pred = model.predict(next_month)[0]\n"
            "print(f'\\n🔮 第7个月预测访问量: {pred:.0f}')"
        ),
    },
]


# ============================================================
# Session 初始化
# ============================================================
def init_session():
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())[:10]
    if "page" not in st.session_state:
        st.session_state.page = "home"  # home / project_N / quiz_N
    if "quiz" not in st.session_state:
        st.session_state.quiz = {}  # 习题得分缓存：{project_id: {...}}
    if "projects_done" not in st.session_state:
        st.session_state.projects_done = set()


# ============================================================
# 全局样式
# ============================================================
def apply_styles():
    st.markdown(
        """
        <style>
            .stApp { background-color: #0e1117; }
            .app-title {
                font-size: 2.3rem !important; font-weight: 800; text-align: center;
                background: linear-gradient(135deg, #00d4ff, #ff00ff, #00ff88);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .app-sub { color:#889; text-align:center; font-size:1rem; margin-bottom:1.2rem; }
            .project-card {
                background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
                border:1px solid #30363d; border-radius: 12px; padding: 18px 20px;
                transition: all .25s ease; cursor: pointer; margin-bottom: 14px;
            }
            .project-card:hover { border-color:#00d4ff; transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,212,255,.15); }
            .badge { display:inline-block; padding:3px 10px; border-radius:20px;
                     font-size:.72rem; font-weight:600; margin-right:6px;
                     background: linear-gradient(135deg,#00d4ff,#ff00ff); color:#0d1117; }
            .badge2 { display:inline-block; padding:3px 10px; border-radius:20px;
                      font-size:.72rem; font-weight:600; margin-right:6px;
                      background:#30363d; color:#c9d1d9; }
            .metric-box { background: linear-gradient(135deg,#161b22,#1a1f2e);
                           border:1px solid #30363d; border-radius:12px; padding:18px 10px; text-align:center; }
            .metric-value { font-size:1.6rem; font-weight:700; color:#00d4ff; margin:4px 0; }
            .metric-label { color:#889; font-size:.82rem; }
            hr { border-color:#21262d; }
            .result-box { background:#0d1117; border:1px solid #21262d;
                          border-left:4px solid #00d4ff; border-radius:8px;
                          padding:14px 16px; font-family: Consolas, Monaco, monospace; margin-top:10px; }
            .ok { border-left-color:#00ff88; }
            .bad { border-left-color:#ff4444; }
            .section-title { color:#00d4ff; font-weight:700; font-size:1.15rem; margin-top: 6px; }
        </style>
        """, unsafe_allow_html=True,
    )


# ============================================================
# 侧边栏导航
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🧊 AI数据分析训练营")
        st.markdown(f"<div style='color:#889; font-size:.82rem;'>用户ID: "
                    f"<code>{st.session_state.user_id}</code></div>", unsafe_allow_html=True)
        st.markdown("---")

        # 总览统计
        total_score = sum(
            v for pid in st.session_state.projects_done for v in
            [sum(s for k, s in st.session_state.quiz.get(pid, {}).items() if k.endswith("_score") and isinstance(s, int))]
        )
        done_count = len(st.session_state.projects_done)

        st.markdown("### 📈 学习进度")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("已完成项目", f"{done_count}/10")
        with c2:
            st.metric("累计得分", f"{total_score}")

        pct = int((done_count / 10) * 100)
        st.markdown(
            f"""
            <div style='background:#21262d; height:10px; border-radius:8px; margin:8px 0 16px; overflow:hidden;'>
                <div style='background: linear-gradient(90deg,#00d4ff,#ff00ff); width:{pct}%; height:100%; transition: width .5s;'></div>
            </div>
            <div style='text-align:center; color:#00ff88; font-weight:600;'>{pct}%</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # 导航按钮
        if st.button("🏠 返回首页", use_container_width=True, key="go_home"):
            st.session_state.page = "home"
            st.rerun()

        st.markdown("### 📚 训练项目导航")
        for p in PROJECTS:
            cols = st.columns([5, 1])
            with cols[0]:
                label = f"{p['icon']} P{p['id']:02d} {p['name']}"
                if p["id"] in st.session_state.projects_done:
                    label += " ✅"
                if st.button(label, key=f"nav_p{p['id']}", use_container_width=True):
                    st.session_state.page = f"project_{p['id']}"
                    st.rerun()
            with cols[1]:
                if st.button("📝", key=f"nav_q{p['id']}", help="进入课后习题"):
                    st.session_state.page = f"quiz_{p['id']}"
                    st.rerun()

        st.markdown("---")
        st.markdown("<div style='color:#889; font-size:.75rem; line-height:1.6;'>"
                    "🚀 每个训练项目包含：<br>"
                    "1) 交互式代码运行环境<br>"
                    "2) 10道课后习题（单选/多选/填空/判断/代码）<br>"
                    "3) 自动判分 + 解析</div>", unsafe_allow_html=True)


# ============================================================
# 页面：首页
# ============================================================
def render_home():
    st.markdown("<div class='app-title'>✨ AI时代 · Python数据分析训练营</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-sub'>10个实战训练项目 · 每项目 10 道课后习题 · 在线交互 + 自动判分</div>",
                unsafe_allow_html=True)
    st.markdown("---")

    # 指标展示
    cols = st.columns(4)
    labels = [("📘", "训练项目", "10"), ("🧠", "课后习题", "100"),
              ("🎯", "题型丰富", "5 种"), ("🤖", "智能判分", "自动")]
    for col, (icon, k, v) in zip(cols, labels):
        with col:
            st.markdown(
                f"""
                <div class='metric-box'>
                    <div style='font-size:1.6rem;'>{icon}</div>
                    <div class='metric-value'>{v}</div>
                    <div class='metric-label'>{k}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # 项目卡片（两列）
    st.markdown("### 🎯 选择训练项目开始学习")
    grid = st.columns(2)
    for idx, p in enumerate(PROJECTS):
        col = grid[idx % 2]
        with col:
            done = p["id"] in st.session_state.projects_done
            concepts_html = " ".join(
                [f"<span class='badge2'>{c}</span>" for c in p["concepts"]]
            )
            st.markdown(
                f"""
                <div class='project-card'>
                    <div style='display:flex; justify-content: space-between; align-items:center;'>
                        <div>
                            <span style='font-size:1.4rem;'>{p['icon']}</span>
                            <span style='font-size:1.1rem; font-weight:700; color:#00d4ff; margin-left:8px;'>
                                P{p['id']:02d} {p['name']}
                            </span>
                        </div>
                        {'<span style="color:#00ff88; font-size:.8rem; font-weight:700;">✅ 已完成</span>' if done else ''}
                    </div>
                    <div style='color:#889; font-size:.85rem; margin:6px 0;'>{p['subtitle']}</div>
                    <div style='margin: 8px 0;'>
                        <span class='badge'>难度 {p['difficulty']}</span>
                        {concepts_html}
                    </div>
                    <div style='color:#ccc; font-size:.88rem; line-height:1.7; margin-top:8px;'>
                        {p['description'][:80]}{'...' if len(p['description']) > 80 else ''}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚀 进入项目", key=f"pgo_{p['id']}", use_container_width=True):
                    st.session_state.page = f"project_{p['id']}"
                    st.rerun()
            with c2:
                if st.button("📝 课后习题", key=f"qgo_{p['id']}", use_container_width=True):
                    st.session_state.page = f"quiz_{p['id']}"
                    st.rerun()
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)


# ============================================================
# 页面：项目（交互式代码运行）
# ============================================================
def render_project(pid: int):
    p = next((x for x in PROJECTS if x["id"] == pid), None)
    if not p:
        st.error("项目不存在")
        return

    st.markdown(f"### {p['icon']} P{p['id']:02d} {p['name']} · {p['subtitle']}")
    st.caption(p["description"])
    st.markdown("---")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 💻 代码编辑器")
        code_key = f"project_code_{pid}"
        if code_key not in st.session_state:
            st.session_state[code_key] = p["initial_code"]
        user_code = st.text_area(
            "代码编辑区", value=st.session_state[code_key], height=360,
            key=f"ta_{pid}", label_visibility="collapsed",
        )
        cc1, cc2, cc3 = st.columns([1, 1, 1])
        with cc1:
            if st.button("▶️ 运行代码", key=f"run_p{pid}", type="primary", use_container_width=True):
                with st.spinner("执行中..."):
                    ok, out, err = run_code_sandbox(user_code)
                st.session_state[f"res_{pid}"] = (ok, out, err)
        with cc2:
            if st.button("🔄 重置为示例", key=f"reset_p{pid}", use_container_width=True):
                st.session_state[code_key] = p["initial_code"]
                st.rerun()
        with cc3:
            if st.button("📝 进入课后习题", key=f"goquiz_p{pid}", use_container_width=True):
                st.session_state.page = f"quiz_{pid}"
                st.rerun()

    with col2:
        st.markdown("#### 📖 任务要求与知识点")
        concepts_html = " ".join(
            [f"<span class='badge2'>{c}</span>" for c in p["concepts"]]
        )
        st.markdown(
            f"""
            <div class='project-card'>
                <div style='color:#00d4ff; font-weight:700;'>🎯 任务目标</div>
                <div style='color:#ccc; margin-top:8px; line-height:1.7;'>{p['description']}</div>
                <div style='margin-top:12px;'>{concepts_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("💡 查看参考答案代码", expanded=False):
            st.code(p["initial_code"], language="python")

    # 执行结果
    if f"res_{pid}" in st.session_state:
        ok, out, err = st.session_state[f"res_{pid}"]
        st.markdown("#### 📤 执行结果")
        if ok:
            st.markdown(
                f"<div class='result-box ok'><b style='color:#00ff88;'>✅ 执行成功</b><br>"
                f"<pre style='white-space:pre-wrap; color:#e6e6e6; margin-top:8px;'>{out or '(无输出)'}</pre></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='result-box bad'><b style='color:#ff4444;'>❌ 执行异常</b><br>"
                f"<pre style='white-space:pre-wrap; color:#ffcccc; margin-top:8px;'>{err}</pre></div>",
                unsafe_allow_html=True,
            )


# ============================================================
# 页面：课后习题
# ============================================================
def render_quiz(pid: int):
    quiz_data = get_project_quiz(pid)
    if not quiz_data:
        st.error("未找到该项目的习题")
        return

    pname = quiz_data["project_name"]
    questions = quiz_data["questions"]
    full_score = sum(q.get("score", 10) for q in questions)

    st.markdown(f"### 📝 P{pid:02d} {pname} · 课后习题")
    st.caption(f"共 {len(questions)} 题，满分 {full_score} 分。可随时查看解析或重做。")

    # 初始化此项目的练习 session
    if pid not in st.session_state.quiz:
        st.session_state.quiz[pid] = {}

    # 顶部进度
    render_progress_panel(st.session_state.quiz[pid], len(questions), full_score)

    # 题目逐个渲染
    for idx, q in enumerate(questions):
        render_question(q, idx, st.session_state.quiz[pid])

    # 操作按钮
    col_done, col_reset, col_back = st.columns([1, 1, 1])
    with col_done:
        if st.button("🏆 标记本项目已完成", key=f"done_{pid}", type="primary", use_container_width=True):
            st.session_state.projects_done.add(pid)
            st.success("✅ 已标记完成！可前往其他项目继续学习。")
    with col_reset:
        if st.button("🔄 重置答题记录", key=f"reset_quiz_{pid}", use_container_width=True):
            st.session_state.quiz[pid] = {}
            st.success("已重置，可重新作答")
            st.rerun()
    with col_back:
        if st.button("🚀 返回项目页", key=f"back_p_{pid}", use_container_width=True):
            st.session_state.page = f"project_{pid}"
            st.rerun()


# ============================================================
# 主入口
# ============================================================
def main():
    st.set_page_config(page_title="AI数据分析训练营", page_icon="🧊",
                       layout="wide", initial_sidebar_state="expanded")
    apply_styles()
    init_session()
    render_sidebar()

    page = st.session_state.page
    if page == "home":
        render_home()
    elif page.startswith("project_"):
        pid = int(page.split("_")[1])
        render_project(pid)
    elif page.startswith("quiz_"):
        pid = int(page.split("_")[1])
        render_quiz(pid)
    else:
        render_home()


if __name__ == "__main__":
    main()
