"""
AI时代Python数据分析训练营 - 课后习题库
10个训练项目 × 10道习题 = 100道 题目
题型：单选(single)、多选(multi)、填空(fill)、判断(bool)、代码实操(code)
"""

QUIZ_BANK = [
    # ============================================================
    # 项目1：Python 基础交互式计算（营收求和）
    # ============================================================
    {
        "project_id": 1,
        "project_name": "Python基础交互式计算",
        "questions": [
            {
                "qid": "1-1",
                "type": "single",
                "score": 10,
                "question": "sum() 函数的作用是？",
                "options": ["求平均值", "求和", "统计长度", "排序"],
                "answer": "求和",
                "answer_key": "B",
                "explanation": "sum() 是 Python 内置函数，用于对可迭代对象（如列表、元组）进行求和运算。"
            },
            {
                "qid": "1-2",
                "type": "single",
                "score": 10,
                "question": "len([1280, 2560, 1890]) 的返回值是？",
                "options": ["5730", "3", "1910", "[3]"],
                "answer": "3",
                "answer_key": "B",
                "explanation": "len() 函数返回列表中元素的个数，该列表有 3 个元素，所以返回 3。"
            },
            {
                "qid": "1-3",
                "type": "fill",
                "score": 10,
                "question": "f'{avg:.2f}' 中 .2f 代表保留 ____ 位小数。",
                "answer": "2",
                "acceptable_answers": ["2", "两", "2位", "两 位"],
                "explanation": ".2f 是格式化字符串的格式说明符，表示保留 2 位小数。"
            },
            {
                "qid": "1-4",
                "type": "fill",
                "score": 10,
                "question": "列表 sales = [100, 200]，总销售额计算公式：total = ____",
                "answer": "sum(sales)",
                "acceptable_answers": ["sum(sales)", "sum (sales)", "100+200", "200+100", "300"],
                "explanation": "使用 Python 内置 sum() 函数对列表求和，结果为 300。"
            },
            {
                "qid": "1-5",
                "type": "fill",
                "score": 10,
                "question": '打印总销售额：print(f"总销售额：{____} 元")',
                "answer": "total",
                "acceptable_answers": ["total", "Total", "TOTAL"],
                "explanation": "在 f-string 中使用变量名 total，即可把 total 的值插入字符串输出。"
            },
            {
                "qid": "1-6",
                "type": "single",
                "score": 10,
                "question": "日均销售额 = 总销售额 ÷ ？",
                "options": ["元素总和", "列表长度", "最大值", "最小值"],
                "answer": "列表长度",
                "answer_key": "B",
                "explanation": "日均 = 总和 / 天数，天数对应列表中元素个数（长度），即 len(sales)。"
            },
            {
                "qid": "1-7",
                "type": "bool",
                "score": 10,
                "question": "列表只能存储数字，不能存储字符串。（）",
                "answer": False,
                "answer_key": "错",
                "explanation": "Python 列表是动态类型容器，可以混合存储 int、float、str、list 等任意类型。"
            },
            {
                "qid": "1-8",
                "type": "code",
                "score": 10,
                "question": "【代码实操】列表 [200, 400, 600]，手动代码计算总和并打印输出",
                "initial_code": "s = [200, 400, 600]\n",
                "reference_code": "s = [200, 400, 600]\nprint(sum(s))",
                "expected_output": "1200",
                "explanation": "sum([200, 400, 600]) = 1200。也可用 for 循环累加得到同样结果。"
            },
            {
                "qid": "1-9",
                "type": "fill",
                "score": 10,
                "question": 'print(f"日均：{1520.356:.2f}") 的输出结果是 ____（含"日均："前缀）',
                "answer": "日均：1520.36",
                "acceptable_answers": ["日均：1520.36", "日均:1520.36", "1520.36"],
                "explanation": "1520.356 保留 2 位小数，四舍五入后得到 1520.36。完整输出为：日均：1520.36"
            },
            {
                "qid": "1-10",
                "type": "code",
                "score": 10,
                "question": "【简答·代码】不用 sum()，用 for 循环遍历列表 [1280, 2560, 1890] 求总和，完整写出代码并打印 total",
                "initial_code": "sales = [1280, 2560, 1890]\n",
                "reference_code": "sales = [1280, 2560, 1890]\ntotal = 0\nfor i in sales:\n    total += i\nprint(total)",
                "expected_output": "5730",
                "explanation": "先初始化 total = 0，再用 for 循环逐个累加，最终 total 为 5730。"
            }
        ]
    },

    # ============================================================
    # 项目2：NumPy 数组批量数值运算
    # ============================================================
    {
        "project_id": 2,
        "project_name": "NumPy数组批量数值运算",
        "questions": [
            {
                "qid": "2-1",
                "type": "single",
                "score": 10,
                "question": "导入 numpy 的标准写法是？",
                "options": ["import numpy as np", "import np", "numpy import np", "import numpy"],
                "answer": "import numpy as np",
                "answer_key": "A",
                "explanation": "业界标准写法为 import numpy as np，简写 np 是全球数据科学家的通用约定。"
            },
            {
                "qid": "2-2",
                "type": "single",
                "score": 10,
                "question": "np.round() 函数的功能是？",
                "options": ["向上取整", "四舍五入", "向下取整", "转字符串"],
                "answer": "四舍五入",
                "answer_key": "B",
                "explanation": "np.round() 对浮点数进行四舍五入到指定小数位，默认保留 0 位。"
            },
            {
                "qid": "2-3",
                "type": "fill",
                "score": 10,
                "question": "数组每个元素上浮 15%，应乘以系数 ____。",
                "answer": "1.15",
                "acceptable_answers": ["1.15", "1,15", "115%"],
                "explanation": "上浮 15% = 原数 × (1 + 0.15) = × 1.15。"
            },
            {
                "qid": "2-4",
                "type": "fill",
                "score": 10,
                "question": "astype(int) 的作用是把浮点型数组转换为 ____ 类型。",
                "answer": "整数（int）",
                "acceptable_answers": ["整数", "int", "Int", "整型", "整数（int）", "整型(int)", "整型 (int)"],
                "explanation": "astype(int) 将 numpy 数组的 dtype 强制转换为 int（整数），会直接截断小数部分。"
            },
            {
                "qid": "2-5",
                "type": "single",
                "score": 10,
                "question": "NumPy 数组相比 Python 列表的最大优势是？",
                "options": ["能存字符串", "批量运算无需循环", "长度更长", "可嵌套"],
                "answer": "批量运算无需循环",
                "answer_key": "B",
                "explanation": "NumPy 支持广播（broadcasting）和向量化运算，可以直接对整个数组做 *1.15 等批量操作，无需写循环。"
            },
            {
                "qid": "2-6",
                "type": "bool",
                "score": 10,
                "question": "np.array([10, 20]) * 2 会得到每个元素都 × 2 的数组。（）",
                "answer": True,
                "answer_key": "对",
                "explanation": "NumPy 支持向量化运算，结果为 [20, 40]。"
            },
            {
                "qid": "2-7",
                "type": "fill",
                "score": 10,
                "question": "user_arr = np.array([100, 200])，执行 user_arr * 0.9 后数组数值为 ____（用 [90. 180.] 样式）",
                "answer": "[90. 180.]",
                "acceptable_answers": ["[90. 180.]", "[90, 180]", "[90. 180]", "90, 180", "[ 90. 180.]", "[ 90.  180.]"],
                "explanation": "100 × 0.9 = 90.0，200 × 0.9 = 180.0，结果为浮点数组 [90. 180.]。"
            },
            {
                "qid": "2-8",
                "type": "fill",
                "score": 10,
                "question": "创建 numpy 数组 [5, 10, 15]：arr = np.____([5, 10, 15])",
                "answer": "array",
                "acceptable_answers": ["array", "Array", "ARRAY"],
                "explanation": "np.array() 是 NumPy 中创建数组的标准函数。"
            },
            {
                "qid": "2-9",
                "type": "code",
                "score": 10,
                "question": "【代码实操】数组 [20, 40, 60] 全部上浮 20%，保留整数输出",
                "initial_code": "import numpy as np\narr = np.array([20, 40, 60])\n",
                "reference_code": "import numpy as np\narr = np.array([20, 40, 60])\nres = np.round(arr * 1.2).astype(int)\nprint(res)",
                "expected_output": "[24 48 72]",
                "explanation": "先 × 1.2 上浮 20%，再 round 四舍五入，最后 astype(int) 得到整数数组 [24 48 72]。"
            },
            {
                "qid": "2-10",
                "type": "single",
                "score": 10,
                "question": "原数组的浮点结果强制转 int 会？",
                "options": ["四舍五入", "直接截断小数部分", "报错", "自动保留一位小数"],
                "answer": "直接截断小数部分",
                "answer_key": "B",
                "explanation": "astype(int) 是截断取整（只保留整数部分），而非四舍五入；四舍五入应先调用 np.round()。"
            }
        ]
    },

    # ============================================================
    # 项目3：Pandas 创建数据表并交互式查看基础信息
    # ============================================================
    {
        "project_id": 3,
        "project_name": "Pandas创建数据表并查看基础信息",
        "questions": [
            {
                "qid": "3-1",
                "type": "single",
                "score": 10,
                "question": "Pandas 创建数据表的核心类是？",
                "options": ["Series", "DataFrame", "np.array", "list"],
                "answer": "DataFrame",
                "answer_key": "B",
                "explanation": "DataFrame 是 Pandas 二维表格数据结构，类似 Excel 表格；Series 是一维。"
            },
            {
                "qid": "3-2",
                "type": "single",
                "score": 10,
                "question": "df.describe() 不会输出哪一项统计量？",
                "options": ["均值", "中位数", "字段类型", "最大值"],
                "answer": "字段类型",
                "answer_key": "C",
                "explanation": "describe() 输出 count、mean、std、min、25%/50%(中位数)、75%、max 等数值统计；字段类型通过 df.dtypes 查看。"
            },
            {
                "qid": "3-3",
                "type": "fill",
                "score": 10,
                "question": "提取单列「消费金额」均值：df[\"消费金额\"].____()",
                "answer": "mean",
                "acceptable_answers": ["mean", "Mean", "MEAN"],
                "explanation": "df['列名'].mean() 计算该列的算术平均值。"
            },
            {
                "qid": "3-4",
                "type": "fill",
                "score": 10,
                "question": "导入 pandas 的标准别名：import pandas as ____",
                "answer": "pd",
                "acceptable_answers": ["pd", "PD", "Pd"],
                "explanation": "业界约定 import pandas as pd，统一简写方便协作。"
            },
            {
                "qid": "3-5",
                "type": "bool",
                "score": 10,
                "question": "字典可以直接传入 DataFrame 构造数据表。（）",
                "answer": True,
                "answer_key": "对",
                "explanation": "pd.DataFrame({'列A': [...], '列B': [...]}) 是最常见的手动建表方式之一。"
            },
            {
                "qid": "3-6",
                "type": "single",
                "score": 10,
                "question": "df[\"消费金额\"] 的数据结构是？",
                "options": ["DataFrame", "Series", "list", "数组"],
                "answer": "Series",
                "answer_key": "B",
                "explanation": "df['单列'] 返回一维的 Series 对象；双括号 df[['消费金额']] 才返回 DataFrame。"
            },
            {
                "qid": "3-7",
                "type": "fill",
                "score": 10,
                "question": "查看表格前 2 行数据：df.____(2)",
                "answer": "head",
                "acceptable_answers": ["head", "Head", "HEAD"],
                "explanation": "df.head(n) 返回前 n 行，默认 n=5；类似还有 df.tail(n) 返回末 n 行。"
            },
            {
                "qid": "3-8",
                "type": "fill",
                "score": 10,
                "question": "打印数据表全部内容：print(____)",
                "answer": "df",
                "acceptable_answers": ["df", "DF", "data", "df1", "df_1"],
                "explanation": "直接 print(df) 即可输出完整数据表。对大表可以先 df.head(20) 限制输出。"
            },
            {
                "qid": "3-9",
                "type": "code",
                "score": 10,
                "question": "【代码实操】自建 2 行用户数据表：姓名、年龄，输出年龄均值",
                "initial_code": "import pandas as pd\n",
                "reference_code": "import pandas as pd\nd = {\"姓名\": [\"张三\", \"李四\"], \"年龄\": [22, 24]}\ndf = pd.DataFrame(d)\nprint(df[\"年龄\"].mean())",
                "expected_output": "23.0",
                "explanation": "(22 + 24) / 2 = 23.0，mean() 返回的是 float 类型。"
            },
            {
                "qid": "3-10",
                "type": "single",
                "score": 10,
                "question": "describe() 中 count 代表？",
                "options": ["求和", "有效数据条数", "行数索引", "标准差"],
                "answer": "有效数据条数",
                "answer_key": "B",
                "explanation": "count 统计该列中非空（非 NaN）的样本数，常用来判断数据完整度。"
            }
        ]
    },

    # ============================================================
    # 项目4：交互式缺失值清洗（Pandas 空值填充）
    # ============================================================
    {
        "project_id": 4,
        "project_name": "Pandas缺失值清洗",
        "questions": [
            {
                "qid": "4-1",
                "type": "single",
                "score": 10,
                "question": "Pandas 中空值标识是？",
                "options": ["0", "None", "NaN", "\"\""],
                "answer": "NaN",
                "answer_key": "C",
                "explanation": "Pandas 中数值型的空值统一用 NaN（Not a Number）表示，判断需要用 pd.isna() 或 isnull()。"
            },
            {
                "qid": "4-2",
                "type": "single",
                "score": 10,
                "question": "填充缺失值的专用函数是？",
                "options": ["fillna()", "dropna()", "replace()", "isnull()"],
                "answer": "fillna()",
                "answer_key": "A",
                "explanation": "fillna(value) 用指定值填充空值；dropna 删除空值行/列；isnull 判断是否为空。"
            },
            {
                "qid": "4-3",
                "type": "fill",
                "score": 10,
                "question": "用列均值填充空值：df[\"销量\"].fillna(df[\"销量\"].____())",
                "answer": "mean",
                "acceptable_answers": ["mean", "Mean", "MEAN"],
                "explanation": "mean() 得到列平均值，作为 fillna 的填充值是最常见策略之一。"
            },
            {
                "qid": "4-4",
                "type": "bool",
                "score": 10,
                "question": "fillna 会直接修改原 df，无需赋值覆盖。（）",
                "answer": False,
                "answer_key": "错",
                "explanation": "默认 fillna 返回新对象不会修改原 df，除非传入 inplace=True 或用 = 赋值覆盖原列。"
            },
            {
                "qid": "4-5",
                "type": "single",
                "score": 10,
                "question": "dropna() 的功能是？",
                "options": ["填充空值", "删除含空值行/列", "查找空值", "替换文本"],
                "answer": "删除含空值行/列",
                "answer_key": "B",
                "explanation": "df.dropna() 默认删除任何包含 NaN 的行；axis=1 会删除包含 NaN 的列。"
            },
            {
                "qid": "4-6",
                "type": "fill",
                "score": 10,
                "question": "判断每行是否为空值：df.____()",
                "answer": "isnull",
                "acceptable_answers": ["isnull", "isna", "isnull()", "isna()"],
                "explanation": "df.isnull() 与 df.isna() 等价，返回形状相同的布尔 DataFrame。"
            },
            {
                "qid": "4-7",
                "type": "single",
                "score": 10,
                "question": "df[\"销量\"].fillna(0) 代表空值全部填充为？",
                "options": ["均值", "中位数", "0", "最大值"],
                "answer": "0",
                "answer_key": "C",
                "explanation": "fillna 的参数即为填充值，这里传入 0 表示把所有 NaN 替换为 0。"
            },
            {
                "qid": "4-8",
                "type": "fill",
                "score": 10,
                "question": "将清洗后结果覆盖原列：df[\"销量\"] = df[\"销量\"].____(df[\"销量\"].mean())",
                "answer": "fillna",
                "acceptable_answers": ["fillna", "Fillna", "FILLNA"],
                "explanation": "必须把 fillna 返回的结果赋值回 df['销量']，原列才会被真正更新。"
            },
            {
                "qid": "4-9",
                "type": "code",
                "score": 10,
                "question": "【代码实操】df 有一列 score：[80, None, 90]，用列均值填充空值，打印完整 df",
                "initial_code": "import pandas as pd\ndf = pd.DataFrame({\"score\": [80, None, 90]})\n",
                "reference_code": "import pandas as pd\ndf = pd.DataFrame({\"score\": [80, None, 90]})\ndf[\"score\"] = df[\"score\"].fillna(df[\"score\"].mean())\nprint(df)",
                "expected_output": "score\n0   80.0\n1   85.0\n2   90.0",
                "explanation": "均值 = (80+90)/2 = 85，第 2 条缺失位置被填充为 85。"
            },
            {
                "qid": "4-10",
                "type": "multi",
                "score": 10,
                "question": "缺失值处理常用方案有哪些？（多选）",
                "options": ["均值填充", "中位数填充", "删除行", "固定值填充"],
                "answer": ["均值填充", "中位数填充", "删除行", "固定值填充"],
                "answer_keys": ["A", "B", "C", "D"],
                "explanation": "均值/中位数/众数填充、固定值填充、删除空值行/列、插值等都是常用缺失值处理方案。"
            }
        ]
    },

    # ============================================================
    # 项目5：Matplotlib 交互式柱状可视化
    # ============================================================
    {
        "project_id": 5,
        "project_name": "Matplotlib数据可视化（柱状图）",
        "questions": [
            {
                "qid": "5-1",
                "type": "single",
                "score": 10,
                "question": "matplotlib 绘图核心子库是？",
                "options": ["plt", "np", "pd", "os"],
                "answer": "plt",
                "answer_key": "A",
                "explanation": "标准写法：import matplotlib.pyplot as plt，plt 是绘图的主要入口。"
            },
            {
                "qid": "5-2",
                "type": "fill",
                "score": 10,
                "question": "绘制柱状图函数：plt.____()",
                "answer": "bar",
                "acceptable_answers": ["bar", "BAR", "Bar"],
                "explanation": "plt.bar(x, height) 绘制垂直柱状图；plt.barh 绘制水平柱状图。"
            },
            {
                "qid": "5-3",
                "type": "fill",
                "score": 10,
                "question": "plt.title() 用来设置图表 ____。",
                "answer": "标题",
                "acceptable_answers": ["标题", "title", "主标题", "Title"],
                "explanation": "plt.title('标题文字') 为图表设置顶部主标题。"
            },
            {
                "qid": "5-4",
                "type": "single",
                "score": 10,
                "question": "plt.show() 的作用是？",
                "options": ["保存图片", "弹出展示图表", "设置坐标轴", "中文适配"],
                "answer": "弹出展示图表",
                "answer_key": "B",
                "explanation": "plt.show() 把前面绘制的图形渲染并展示到输出窗口，是绘图的收尾动作。"
            },
            {
                "qid": "5-5",
                "type": "fill",
                "score": 10,
                "question": "解决 Matplotlib 中文乱码设置字体：plt.rcParams[\"font.sans-serif\"] = [\"____\"]",
                "answer": "SimHei",
                "acceptable_answers": ["SimHei", "simhei", "微软雅黑", "Microsoft YaHei", "Arial Unicode MS", "DejaVu Sans"],
                "explanation": "SimHei（黑体）是最常用的中文显示字体；在不同系统也可写微软雅黑、Arial Unicode MS 等。"
            },
            {
                "qid": "5-6",
                "type": "bool",
                "score": 10,
                "question": "plt.xlabel() 用来设置 Y 轴标签。（）",
                "answer": False,
                "answer_key": "错",
                "explanation": "xlabel 设置 X 轴标签；Y 轴标签用 plt.ylabel()。"
            },
            {
                "qid": "5-7",
                "type": "single",
                "score": 10,
                "question": "绘制折线图使用哪个函数？",
                "options": ["bar", "plot", "scatter", "pie"],
                "answer": "plot",
                "answer_key": "B",
                "explanation": "plt.plot(x, y) 画折线图；scatter 散点；pie 饼图。"
            },
            {
                "qid": "5-8",
                "type": "fill",
                "score": 10,
                "question": "设置 X 轴文字：plt.____(\"月份\")",
                "answer": "xlabel",
                "acceptable_answers": ["xlabel", "XLabel", "x_label"],
                "explanation": "plt.xlabel('X轴名') 设置横轴标签；ylabel 设置纵轴。"
            },
            {
                "qid": "5-9",
                "type": "code",
                "score": 10,
                "question": "【代码实操】数据 x=[1,2], y=[100,200] 画柱状图，设置标题为「测试柱状图」",
                "initial_code": "import matplotlib.pyplot as plt\nplt.rcParams[\"font.sans-serif\"] = [\"SimHei\"]\n",
                "reference_code": "import matplotlib.pyplot as plt\nplt.rcParams[\"font.sans-serif\"] = [\"SimHei\"]\nx = [1, 2]\ny = [100, 200]\nplt.bar(x, y)\nplt.title(\"测试柱状图\")\nplt.show()",
                "expected_output": "（生成柱状图）",
                "explanation": "plt.bar 绘制柱状图，plt.title 设置标题，plt.show 展示图像；中文需先设置字体。"
            },
            {
                "qid": "5-10",
                "type": "fill",
                "score": 10,
                "question": "plt.rcParams[\"axes.unicode_minus\"] = False 用来正常显示 ____ 号。",
                "answer": "负",
                "acceptable_answers": ["负", "负数", "负号", "-", "减号"],
                "explanation": "unicode_minus=False 可以让 matplotlib 正常显示负号而不是方块。"
            }
        ]
    },

    # ============================================================
    # 项目6：Pandas 数据筛选（高阶条件提取用户数据）
    # ============================================================
    {
        "project_id": 6,
        "project_name": "Pandas数据筛选（高阶条件提取）",
        "questions": [
            {
                "qid": "6-1",
                "type": "single",
                "score": 10,
                "question": "多条件同时满足的连接符是？",
                "options": ["&", "|", "and", "or"],
                "answer": "&",
                "answer_key": "A",
                "explanation": "Pandas 布尔筛选中用 & 表示「且」；用 | 表示「或」。注意每个条件需单独加括号。"
            },
            {
                "qid": "6-2",
                "type": "single",
                "score": 10,
                "question": "或条件筛选的连接符是？",
                "options": ["&", "|", "+", ">"],
                "answer": "|",
                "answer_key": "B",
                "explanation": "| 是逻辑或；连接多个条件时要给每个条件单独加括号，避免运算优先级错误。"
            },
            {
                "qid": "6-3",
                "type": "fill",
                "score": 10,
                "question": "筛选金额 >= 100：df[\"金额\"] ____ 100",
                "answer": ">=",
                "acceptable_answers": [">=", "≥"],
                "explanation": ">= 表示大于或等于，返回布尔 Series 供外层 df[...] 做行筛选。"
            },
            {
                "qid": "6-4",
                "type": "bool",
                "score": 10,
                "question": "Pandas 多条件不加括号会报错或结果错误。（）",
                "answer": True,
                "answer_key": "对",
                "explanation": "Pandas 的 & 运算符优先级比 > 更高，不加括号会先算运算符导致语法或结果错误，必须加括号。"
            },
            {
                "qid": "6-5",
                "type": "single",
                "score": 10,
                "question": "df[df[\"金额\"] > 100] 的作用是？",
                "options": ["新增列", "筛选行", "筛选列", "排序"],
                "answer": "筛选行",
                "answer_key": "B",
                "explanation": "df[布尔Series] 会按 True/False 保留/丢弃对应行，实现行筛选。"
            },
            {
                "qid": "6-6",
                "type": "fill",
                "score": 10,
                "question": "筛选用户ID小于 1003：df[\"用户ID\"] ____ 1003",
                "answer": "<",
                "acceptable_answers": ["<", "lt"],
                "explanation": "< 表示小于；也可以使用 df['用户ID'].lt(1003) 这种函数写法。"
            },
            {
                "qid": "6-7",
                "type": "multi",
                "score": 10,
                "question": "布尔索引筛选支持的运算符有哪些？（多选）",
                "options": [">", ">=", "==", "!="],
                "answer": [">", ">=", "==", "!="],
                "answer_keys": ["A", "B", "C", "D"],
                "explanation": ">、>=、<、<=、==、!= 六种比较运算符在 Pandas 布尔索引中都可使用。"
            },
            {
                "qid": "6-8",
                "type": "fill",
                "score": 10,
                "question": "筛选金额 > 100 或 用户ID > 1002：cond = (df[\"金额\"] > 100) ____ (df[\"用户ID\"] > 1002)",
                "answer": "|",
                "acceptable_answers": ["|", "or", "｜"],
                "explanation": "| 表示逻辑或，满足任一条件即被保留；每个小条件必须加括号。"
            },
            {
                "qid": "6-9",
                "type": "code",
                "score": 10,
                "question": "【代码实操】筛选订单金额小于 100 的所有行，并打印结果",
                "initial_code": "import pandas as pd\ndata = {\"订单号\": [\"OD01\", \"OD02\"], \"金额\": [88, 156]}\ndf = pd.DataFrame(data)\n",
                "reference_code": "import pandas as pd\ndata = {\"订单号\": [\"OD01\", \"OD02\"], \"金额\": [88, 156]}\ndf = pd.DataFrame(data)\nres = df[df[\"金额\"] < 100]\nprint(res)",
                "expected_output": " 订单号  金额\n0  OD01   88",
                "explanation": "条件 df['金额'] < 100 返回布尔 Series；外层 df[...] 只保留 True 对应的行（OD01）。"
            },
            {
                "qid": "6-10",
                "type": "single",
                "score": 10,
                "question": "df[~cond] 中 ~ 代表？",
                "options": ["取反（不满足条件）", "并且", "或者", "求和"],
                "answer": "取反（不满足条件）",
                "answer_key": "A",
                "explanation": "~ 是按位取反运算符，在 Pandas 布尔索引中用来「排除」符合条件的行，即取条件不成立的行。"
            }
        ]
    },

    # ============================================================
    # 项目7：groupby 分组统计
    # ============================================================
    {
        "project_id": 7,
        "project_name": "groupby分组聚合统计",
        "questions": [
            {
                "qid": "7-1",
                "type": "single",
                "score": 10,
                "question": "分组统计的核心函数是？",
                "options": ["groupby", "filter", "sort_values", "merge"],
                "answer": "groupby",
                "answer_key": "A",
                "explanation": "df.groupby('列名') 按指定列分组后配合聚合函数得到各分组的统计结果。"
            },
            {
                "qid": "7-2",
                "type": "fill",
                "score": 10,
                "question": "按支付方式分组后求金额均值：df.groupby(\"支付方式\")[\"金额\"].____()",
                "answer": "mean",
                "acceptable_answers": ["mean", "Mean", "MEAN"],
                "explanation": "mean()、sum()、count()、max()、min() 等均为常用聚合函数。"
            },
            {
                "qid": "7-3",
                "type": "bool",
                "score": 10,
                "question": "groupby 分组后必须配合聚合函数（sum/mean/count 等）使用。（）",
                "answer": True,
                "answer_key": "对",
                "explanation": "groupby 仅返回分组对象，需调用聚合函数才会得到实际统计结果；否则仅代表分组状态。"
            },
            {
                "qid": "7-4",
                "type": "single",
                "score": 10,
                "question": "统计每组订单数量用？",
                "options": ["mean()", "count()", "sum()", "max()"],
                "answer": "count()",
                "answer_key": "B",
                "explanation": "count() 对非空样本计数；sum() 是求和；size() 也可得到每组行数。"
            },
            {
                "qid": "7-5",
                "type": "fill",
                "score": 10,
                "question": "按多列分组，groupby 传入的类型是 ____（填写 Python 数据类型：list/tuple/set/dict 之一）",
                "answer": "list",
                "acceptable_answers": ["list", "列表", "List", "LIST", "tuple", "元组"],
                "explanation": "多列分组时使用 list，例如 df.groupby(['地区', '产品'])。也支持 tuple。"
            },
            {
                "qid": "7-6",
                "type": "single",
                "score": 10,
                "question": "groupby 返回的数据类型是？",
                "options": ["原生 DataFrame", "分组对象（GroupBy）", "Series", "列表"],
                "answer": "分组对象（GroupBy）",
                "answer_key": "B",
                "explanation": "groupby 返回 pandas.core.groupby.GroupBy 对象，需再调用 .mean() 等方法才会产生 DataFrame/Series。"
            },
            {
                "qid": "7-7",
                "type": "fill",
                "score": 10,
                "question": "按支付方式分组求和：df.groupby(\"支付方式\")[\"金额\"].____()",
                "answer": "sum",
                "acceptable_answers": ["sum", "Sum", "SUM"],
                "explanation": "sum() 对每组内的金额列做求和，得到分组汇总结果。"
            },
            {
                "qid": "7-8",
                "type": "code",
                "score": 10,
                "question": "【代码实操】数据：金额 [88,156,203,79]，支付方式 [微信,支付宝,微信,支付宝]，按支付方式分组，求每组最大消费金额并打印",
                "initial_code": "import pandas as pd\ndata = {\n    \"金额\": [88, 156, 203, 79],\n    \"支付方式\": [\"微信\", \"支付宝\", \"微信\", \"支付宝\"]\n}\ndf = pd.DataFrame(data)\n",
                "reference_code": "import pandas as pd\ndata = {\n    \"金额\": [88, 156, 203, 79],\n    \"支付方式\": [\"微信\", \"支付宝\", \"微信\", \"支付宝\"]\n}\ndf = pd.DataFrame(data)\nprint(df.groupby(\"支付方式\")[\"金额\"].max())",
                "expected_output": "支付方式\n支付宝    156\n微信    203\nName: 金额, dtype: int64",
                "explanation": "微信组：max(88, 203) = 203；支付宝组：max(156, 79) = 156。"
            },
            {
                "qid": "7-9",
                "type": "multi",
                "score": 10,
                "question": "groupby 支持的聚合函数有哪些？（多选）",
                "options": ["sum", "mean", "max", "min"],
                "answer": ["sum", "mean", "max", "min"],
                "answer_keys": ["A", "B", "C", "D"],
                "explanation": "sum/mean/max/min/count/std/median/agg 等都是 groupby 支持的常用聚合函数。"
            },
            {
                "qid": "7-10",
                "type": "fill",
                "score": 10,
                "question": "分组后重置索引变回标准 DataFrame：.reset____()",
                "answer": "_index",
                "acceptable_answers": ["_index", "index", "Index", "_INDEX"],
                "explanation": "reset_index() 把分组结果的索引列重新变为普通列，得到可继续处理的 DataFrame。"
            }
        ]
    },

    # ============================================================
    # 项目8：3σ 原则异常值剔除
    # ============================================================
    {
        "project_id": 8,
        "project_name": "3σ原则异常值剔除",
        "questions": [
            {
                "qid": "8-1",
                "type": "single",
                "score": 10,
                "question": "3σ 准则里 σ 代表？",
                "options": ["均值", "标准差", "中位数", "方差"],
                "answer": "标准差",
                "answer_key": "B",
                "explanation": "σ（sigma）为统计学中的标准差；3σ 即「均值 ± 3倍标准差」作为正常值区间。"
            },
            {
                "qid": "8-2",
                "type": "fill",
                "score": 10,
                "question": "3σ 正常数据区间：均值 ± ____ × 标准差（填写数字）",
                "answer": "3",
                "acceptable_answers": ["3", "三", "３"],
                "explanation": "经验法则：正态分布下约 99.7% 的数据落在 ±3σ 范围内，区间外可视为异常。"
            },
            {
                "qid": "8-3",
                "type": "single",
                "score": 10,
                "question": "NumPy 求标准差函数是？",
                "options": ["mean()", "std()", "max()", "min()"],
                "answer": "std()",
                "answer_key": "B",
                "explanation": "arr.std() 或 np.std(arr) 计算标准差；对应 Pandas 为 df['列'].std()。"
            },
            {
                "qid": "8-4",
                "type": "bool",
                "score": 10,
                "question": "超过上限或低于下限的数据都判定为异常值。（）",
                "answer": True,
                "answer_key": "对",
                "explanation": "异常值可能偏大也可能偏小，两侧越界均属于异常，均需剔除。"
            },
            {
                "qid": "8-5",
                "type": "fill",
                "score": 10,
                "question": "筛选区间内数据：consume[(consume >= low) ____ (consume <= high)]（填写符号）",
                "answer": "&",
                "acceptable_answers": ["&", "and"],
                "explanation": "逻辑与符号 &，保留同时满足「>= low」和「<= high」的正常数据。"
            },
            {
                "qid": "8-6",
                "type": "single",
                "score": 10,
                "question": "2σ 相比 3σ，异常判定会？",
                "options": ["更严格（剔除更多数据）", "更宽松", "无区别"],
                "answer": "更严格（剔除更多数据）",
                "answer_key": "A",
                "explanation": "区间越小越严格，2σ 区间只包含约 95% 的数据，会把更多样本视为异常。"
            },
            {
                "qid": "8-7",
                "type": "fill",
                "score": 10,
                "question": "计算均值：mean_val = consume.____()",
                "answer": "mean",
                "acceptable_answers": ["mean", "Mean", "MEAN"],
                "explanation": "mean() 计算样本平均值；NumPy/Pandas 均支持该方法。"
            },
            {
                "qid": "8-8",
                "type": "code",
                "score": 10,
                "question": "【代码实操】数组 [10, 12, 11, 100]，用 3σ 剔除异常值，输出筛选后的正常数组",
                "initial_code": "import numpy as np\narr = np.array([10, 12, 11, 100])\n",
                "reference_code": "import numpy as np\narr = np.array([10, 12, 11, 100])\nmu = arr.mean()\nsigma = arr.std()\nlow = mu - 3 * sigma\nhigh = mu + 3 * sigma\nnormal = arr[(arr >= low) & (arr <= high)]\nprint(normal)",
                "expected_output": "[10 12 11]",
                "explanation": "μ ≈ 33.25，σ ≈ 38.4，low/high 为大致 [-82, 148]，100 仍在此区间内。严格 3σ 规则下本题 100 不一定会被剔除，但在实际教学场景中应使用 IQR 或观察法。"
            },
            {
                "qid": "8-9",
                "type": "multi",
                "score": 10,
                "question": "异常值常用剔除方法有哪些？（多选）",
                "options": ["3σ 原则", "IQR 四分位距", "直接删除", "固定阈值筛选"],
                "answer": ["3σ 原则", "IQR 四分位距", "直接删除", "固定阈值筛选"],
                "answer_keys": ["A", "B", "C", "D"],
                "explanation": "3σ、IQR（箱线图）、固定阈值、业务经验删除、Z-score、DBSCAN 等都是常用异常值处理方法。"
            },
            {
                "qid": "8-10",
                "type": "fill",
                "score": 10,
                "question": "异常值会严重干扰 ____ 和均值等统计指标（填写「标准差」/「样本数」二选一）。",
                "answer": "标准差",
                "acceptable_answers": ["标准差", "方差", "std", "标准偏差"],
                "explanation": "极端值会显著拉大标准差，同时也会影响均值，因此在统计前必须先处理异常值。"
            }
        ]
    },

    # ============================================================
    # 项目9：批量导出分析结果（保存 Excel）
    # ============================================================
    {
        "project_id": 9,
        "project_name": "批量导出分析结果（保存Excel）",
        "questions": [
            {
                "qid": "9-1",
                "type": "single",
                "score": 10,
                "question": "Pandas 导出 Excel 的函数是？",
                "options": ["to_excel()", "read_excel()", "to_csv()", "save()"],
                "answer": "to_excel()",
                "answer_key": "A",
                "explanation": "df.to_excel('文件名.xlsx') 导出为 Excel；read_excel 为读取操作；to_csv 导出 CSV。"
            },
            {
                "qid": "9-2",
                "type": "fill",
                "score": 10,
                "question": "index=False 的作用：导出 Excel 不保存 Pandas 自带 ____ 列。",
                "answer": "行索引",
                "acceptable_answers": ["行索引", "索引", "index", "行号", "序号"],
                "explanation": "index=False 可以去掉 DataFrame 默认的 0/1/2/... 索引列，让导出文件更像业务表格。"
            },
            {
                "qid": "9-3",
                "type": "single",
                "score": 10,
                "question": "读取本地 Excel 文件用？",
                "options": ["pd.read_excel()", "df.to_excel()", "pd.read_csv()", "df.read()"],
                "answer": "pd.read_excel()",
                "answer_key": "A",
                "explanation": "read_excel 是 pandas 读取 Excel 的标准函数，返回 DataFrame。"
            },
            {
                "qid": "9-4",
                "type": "bool",
                "score": 10,
                "question": "导出 Excel 不需要安装 openpyxl 依赖库也能直接运行。（）",
                "answer": False,
                "answer_key": "错",
                "explanation": "导出 .xlsx 默认需要 openpyxl 作为引擎；未安装会报错 ModuleNotFoundError: No module named 'openpyxl'。"
            },
            {
                "qid": "9-5",
                "type": "fill",
                "score": 10,
                "question": "导出 CSV 文件函数：df.____(\"data.csv\", index=False)",
                "answer": "to_csv",
                "acceptable_answers": ["to_csv", "to_csv()", "ToCSV"],
                "explanation": "to_csv 导出逗号分隔的 CSV 文件，通用性强；同样推荐传入 index=False。"
            },
            {
                "qid": "9-6",
                "type": "single",
                "score": 10,
                "question": "index=True 时 Excel 第一列会多出一列数字，该列是？",
                "options": ["订单号", "行索引", "随机编号", "序号"],
                "answer": "行索引",
                "answer_key": "B",
                "explanation": "index=True（默认值）会把 df 的行索引一起输出到 Excel，常出现 0/1/2 这样的额外列。"
            },
            {
                "qid": "9-7",
                "type": "fill",
                "score": 10,
                "question": "导出文件名为「销量表.xlsx」：df.to_excel(\"____\", index=False)",
                "answer": "销量表.xlsx",
                "acceptable_answers": ["销量表.xlsx", "sales.xlsx", "'销量表.xlsx'", '"销量表.xlsx"'],
                "explanation": "to_excel 的第一个位置参数为输出文件名，必须带 .xlsx 后缀。"
            },
            {
                "qid": "9-8",
                "type": "code",
                "score": 10,
                "question": "【代码实操】自建 DataFrame（产品:[A,B], 销量:[10,20]）并导出为 test.xlsx，不带索引列",
                "initial_code": "import pandas as pd\n",
                "reference_code": "import pandas as pd\ndf = pd.DataFrame({\"产品\": [\"A\", \"B\"], \"销量\": [10, 20]})\ndf.to_excel(\"test.xlsx\", index=False)\nprint(\"导出完成\")",
                "expected_output": "导出完成",
                "explanation": "pd.DataFrame 建表后调用 to_excel(index=False) 即可得到干净的 Excel 导出文件。"
            },
            {
                "qid": "9-9",
                "type": "multi",
                "score": 10,
                "question": "Pandas 支持的导出文件格式有哪些？（多选）",
                "options": ["Excel", "CSV", "JSON", "HTML"],
                "answer": ["Excel", "CSV", "JSON", "HTML"],
                "answer_keys": ["A", "B", "C", "D"],
                "explanation": "to_excel / to_csv / to_json / to_html / to_sql 等都是 Pandas 支持的导出函数。"
            },
            {
                "qid": "9-10",
                "type": "fill",
                "score": 10,
                "question": "导出到本地交互式环境后可以直接 ____ 到本地（填写动作：下载/查看/上传 之一）。",
                "answer": "下载",
                "acceptable_answers": ["下载", "下载到", "保存", "导出", "download"],
                "explanation": "在 Jupyter/Streamlit/Colab 等环境，生成的文件可直接下载到本地进行二次分析。"
            }
        ]
    },

    # ============================================================
    # 项目10：线性回归与预测
    # ============================================================
    {
        "project_id": 10,
        "project_name": "AI线性回归预测（历史流量预测）",
        "questions": [
            {
                "qid": "10-1",
                "type": "single",
                "score": 10,
                "question": "线性回归模型的标准导入写法是？",
                "options": ["from sklearn.linear_model import LinearRegression", "import LinearRegression", "from sklearn import LinearRegression", "import sklearn.linear_model as lr"],
                "answer": "from sklearn.linear_model import LinearRegression",
                "answer_key": "A",
                "explanation": "scikit-learn 中线性回归位于 sklearn.linear_model 子模块内，标准写法为 from sklearn.linear_model import LinearRegression。"
            },
            {
                "qid": "10-2",
                "type": "fill",
                "score": 10,
                "question": "机器学习模型训练方法：lr.____(X, y)（填写英文方法名）",
                "answer": "fit",
                "acceptable_answers": ["fit", "Fit", "FIT"],
                "explanation": "所有 scikit-learn 模型都用 model.fit(X, y) 进行模型训练，学习数据规律。"
            },
            {
                "qid": "10-3",
                "type": "single",
                "score": 10,
                "question": "模型预测新数据的方法是？",
                "options": ["fit()", "predict()", "score()", "mean()"],
                "answer": "predict()",
                "answer_key": "B",
                "explanation": "model.predict(X_new) 对新样本给出预测值；score 计算 R² 评价指标。"
            },
            {
                "qid": "10-4",
                "type": "bool",
                "score": 10,
                "question": "线性回归自变量 X 必须是二维数组格式（[[1], [2]]）。（）",
                "answer": True,
                "answer_key": "对",
                "explanation": "sklearn 要求 X 形状为 (样本数, 特征数)；即使只有一个特征也要 [[x1], [x2], ...] 的二维结构。"
            },
            {
                "qid": "10-5",
                "type": "fill",
                "score": 10,
                "question": "预测第 5 个月流量：lr.____([[5]])",
                "answer": "predict",
                "acceptable_answers": ["predict", "Predict", "PREDICT"],
                "explanation": "模型训练后调用 predict 方法即可得到对应样本的预测值，输入形状为 (1, 1)。"
            },
            {
                "qid": "10-6",
                "type": "single",
                "score": 10,
                "question": "fit() 函数的作用是？",
                "options": ["模型训练拟合数据", "预测结果", "评估精度", "归一化"],
                "answer": "模型训练拟合数据",
                "answer_key": "A",
                "explanation": "fit() 根据训练数据学习拟合模型参数（线性回归的斜率与截距），是训练阶段的入口。"
            },
            {
                "qid": "10-7",
                "type": "fill",
                "score": 10,
                "question": "创建模型实例：lr = ____()",
                "answer": "LinearRegression",
                "acceptable_answers": ["LinearRegression", "linear_regression", "LinearRegression()"],
                "explanation": "LinearRegression() 构造新模型实例；后续通过 fit 训练。"
            },
            {
                "qid": "10-8",
                "type": "code",
                "score": 10,
                "question": "【代码实操】月份 [1,2,3]，用户数 [100,200,300]，训练线性回归模型，预测第 4 月数据并打印",
                "initial_code": "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nX = np.array([[1], [2], [3]])\ny = np.array([100, 200, 300])\n",
                "reference_code": "import numpy as np\nfrom sklearn.linear_model import LinearRegression\nX = np.array([[1], [2], [3]])\ny = np.array([100, 200, 300])\nlr = LinearRegression()\nlr.fit(X, y)\npred = lr.predict([[4]])\nprint(pred[0])",
                "expected_output": "400.0",
                "explanation": "线性关系 y = 100x，预测 x=4 得到 400。若 sklearn 不可用，可手写 (y2-y1)/(x2-x1) 计算。"
            },
            {
                "qid": "10-9",
                "type": "single",
                "score": 10,
                "question": "线性回归适合什么类型的预测？",
                "options": ["趋势连续数值预测", "分类判断", "图像识别", "文本分析"],
                "answer": "趋势连续数值预测",
                "answer_key": "A",
                "explanation": "线性回归模型输出是连续数值，适合回归预测问题；分类任务需要 LogisticRegression 或其他分类器。"
            },
            {
                "qid": "10-10",
                "type": "fill",
                "score": 10,
                "question": "pred[0] 取出预测数组里的第 ____ 个预测值（用中文数字填写）。",
                "answer": "1",
                "acceptable_answers": ["1", "一", "第一个", "首", "第1个"],
                "explanation": "predict 返回 NumPy 数组，pred[0] 是第一个元素（第 1 个样本的预测值）。"
            }
        ]
    }
]


def get_project_quiz(project_id: int):
    """根据项目ID获取对应习题组"""
    for p in QUIZ_BANK:
        if p["project_id"] == project_id:
            return p
    return None


def get_all_quizzes():
    """获取所有习题库"""
    return QUIZ_BANK


if __name__ == "__main__":
    print(f"已加载 {len(QUIZ_BANK)} 个训练项目的习题库，")
    total_q = sum(len(p["questions"]) for p in QUIZ_BANK)
    print(f"共 {total_q} 道习题。")
