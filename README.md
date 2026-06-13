# 🧊 AI 时代 Python数据分析训练营

> 10 个交互式训练项目 + 100 道课后习题，基于 Streamlit + Pandas 纯 Python 项目

| 特性 | 说明 |
|---|---|
| 前端 | **Streamlit**（纯 Python，无需写 HTML/JS） |
| 后端 | **Pandas / NumPy 内置代码执行引擎 |
| 数据库 | **SQLite**（可选，存储学习进度） |
| 主题 | 深色科技感主题 |
| 题库 | 10 个训练项目，每题含 10 道课后习题（单选 / 多选 / 判断 / 填空 / 代码实操） |
| 判分 | 自动判分 + 解析说明 |

## 🚀 快速启动（3 步）

### 方式 1：本地直接运行（推荐先跑通再部署）
```bash
# 1. 克隆或进入项目目录
cd data_analysis_camp

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动 Streamlit
streamlit run frontend/app.py
# 浏览器自动打开 http://localhost:8501
```

### 方式 2：一键部署到云端（详见底部 👇

## 📚 10 个训练项目

1. 🐍 **Python 基础交互式计算** —— 营收求和、列表遍历
2. 🔢 **NumPy 数组批量运算** —— 用户量翻倍、向量化计算
3. 📋 **Pandas 创建数据表** —— 订单表、描述统计、均值计算
4. 🧹 **缺失值清洗实战** —— 空值填充 / 删除
5. 📊 **Matplotlib 数据可视化** —— 柱状图、中文渲染
6. 🔍 **Pandas 数据筛选** —— 布尔索引、多条件组合
7. 📊 **groupby 分组聚合** —— 分组汇总统计
8. ⚡ **3σ 异常值剔除** —— 标准差、极端值识别
9. 📤 **批量导出分析结果** —— Excel / CSV 导出
10. 🤖 **AI 线性回归预测** —— 基于历史流量预测下月访问量

每个项目都包含：
- 描述区 + 代码编辑器 + 一键运行 + 结果展示 + AI 反馈
- 10 道课后习题（单选 / 多选 / 判断 / 填空 / 代码实操）

## 📂 项目结构

```
data_analysis_camp/
├── .streamlit/
│   └── config.toml          # Streamlit 深色主题 + 配置
├── backend/
│   ├── executor.py        # 代码执行沙箱 + 判分引擎
│   ├── quiz_bank.py      # 100 道课后习题题库
│   ├── scoring.py        # 评分引擎（得分规则定义）
│   └── database.py     # SQLite 数据库模型（进度/排行榜）
├── frontend/
│   ├── app.py           # Streamlit 主应用（首页 / 项目页 / 习题页）
│   └── quiz_engine.py   # 题目渲染 + 判分 UI
├── data/                   # 内置数据集目录
├── requirements.txt        # Python 依赖清单
├── start.sh            # 一键启动脚本（Linux / 单文件）
└── README.md
```

## ☁️ 一键部署到云端

### 方案 A：Streamlit Community Cloud（5 分钟免费）

1. 推送到 GitHub（见下方「推送到 GitHub）
2. 打开 https://streamlit.io/cloud → Sign up with GitHub
3. 点 **New app** → 选择你的仓库 → Branch: `main` → Main file path: `frontend/app.py`
4. 点 **Deploy!** 自动识别 `requirements.txt` 安装依赖
5. 得到形如 `https://<你的项目>.streamlit.app` 的公开访问链接

### 方案 B：Docker 部署（任意云服务器）

```bash
# 构建
docker build -t py-camp .

# 运行
docker run -d -p 8501:8501 --name camp --restart always py-camp
```

浏览器访问 http://服务器IP:8501

### 方案 C：Ubuntu / CentOS 云服务器

```bash
# 1. 拉取代码
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动（推荐使用 systemd 管理进程）
```

## 📤 推送到 GitHub

```bash
# 初始化（如未执行过）
cd data_analysis_camp
git init
git add -A
git commit -m "feat: AI 时代 Python 数据分析训练营（10 训练项目 + 100 习题）"

# 关联远程仓库（请替换为你自己的地址）
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

## 🧠 设计亮点

- **交互式代码运行**：内置代码执行引擎，提交后自动判分
- **AI 反馈**：对代码质量、知识点掌握情况给出反馈
- **学习进度追踪**：记录已完成项目和得分
- **深色科技感主题**：渐变配色、发光边框
- **全中文界面**：适合国内教学/培训场景

## 📝 License

MIT License - 可自由使用、修改、分发

---

> 🎉 开始你的数据分析之旅吧！
