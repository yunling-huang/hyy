"""
代码执行引擎 - 安全沙箱环境
提供代码验证、执行和结果捕获功能
"""
import sys
import io
import traceback
import time
import ast
from typing import Dict, Any, Tuple, List


class CodeExecutor:
    """代码安全执行器"""

    def __init__(self):
        self.max_execution_time = 10  # 最大执行时间(秒)
        self.max_memory = 100 * 1024 * 1024  # 100MB

    def validate_code(self, code: str) -> Tuple[bool, str]:
        """
        验证代码安全性
        检查是否有危险操作：文件访问、系统命令、网络请求等
        """
        if not code or not code.strip():
            return False, "代码不能为空"

        # 1. AST语法检查
        try:
            ast.parse(code)
        except SyntaxError as e:
            return False, f"语法错误: {str(e)}"

        # 2. 危险模块和函数检测
        dangerous_patterns = [
            ('import os', '禁止导入os模块'),
            ('import sys', '禁止直接操作sys模块'),
            ('import subprocess', '禁止执行系统命令'),
            ('subprocess.', '禁止执行系统命令'),
            ('os.system', '禁止执行系统命令'),
            ('os.popen', '禁止执行系统命令'),
            ('eval(', '禁止使用eval'),
            ('exec(', '禁止使用exec'),
            ('open(', '禁止文件操作'),
            ('file(', '禁止文件操作'),
            ('__import__', '禁止动态导入'),
            ('socket.', '禁止网络操作'),
            ('requests.', '禁止网络请求'),
            ('urllib', '禁止网络请求'),
            ('http.client', '禁止网络请求'),
            ('shutil.', '禁止文件系统操作'),
            ('tempfile.', '禁止临时文件操作'),
        ]

        for pattern, message in dangerous_patterns:
            if pattern in code:
                return False, f"安全限制: {message}"

        return True, "代码验证通过"

    def execute(self, code: str, context: Dict[str, Any] = None) -> Tuple[bool, str, str, float]:
        """
        执行用户代码
        返回: (成功, 输出内容, 错误内容, 执行时间)
        """
        start_time = time.time()

        # 创建执行上下文
        exec_globals = {
            '__builtins__': self._get_safe_builtins(),
            '__name__': '__main__',
        }

        # 添加额外的上下文数据
        if context:
            exec_globals.update(context)

        # 捕获输出
        output_buffer = io.StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = output_buffer
        sys.stderr = output_buffer

        success = True
        error_msg = ""

        try:
            # 使用exec执行代码
            exec(code, exec_globals)
            # 如果是表达式，尝试eval获取结果
            try:
                result = eval(code, exec_globals)
                if result is not None:
                    print(result)
            except:
                pass

        except Exception as e:
            success = False
            error_msg = traceback.format_exc()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        execution_time = round(time.time() - start_time, 3)
        output = output_buffer.getvalue()
        output_buffer.close()

        return success, output, error_msg, execution_time

    def _get_safe_builtins(self) -> Dict:
        """获取安全的内置函数"""
        safe_builtins = {}
        allowed_names = [
            'print', 'len', 'str', 'int', 'float', 'bool', 'list', 'dict',
            'tuple', 'set', 'range', 'enumerate', 'zip', 'map', 'filter',
            'sorted', 'reversed', 'any', 'all', 'sum', 'min', 'max', 'abs',
            'round', 'pow', 'divmod', 'type', 'isinstance', 'hasattr',
            'getattr', 'setattr', 'True', 'False', 'None', 'Exception',
            'ValueError', 'TypeError', 'KeyError', 'IndexError',
        ]
        for name in allowed_names:
            if name in __builtins__:
                safe_builtins[name] = __builtins__[name]
        return safe_builtins


class ScoringEngine:
    """评分引擎 - 对用户代码进行智能评分"""

    def __init__(self):
        pass

    def score_project(self, project_id: int, user_code: str,
                       exec_output: str, is_success: bool) -> Dict[str, Any]:
        """
        根据项目ID评分用户答案
        返回: {'score': 分数, 'max_score': 100, 'feedback': 反馈信息, 'passed': 是否通过}
        """
        if not is_success:
            return {
                'score': 0,
                'max_score': 100,
                'feedback': '❌ 代码执行失败，请检查语法和逻辑错误',
                'passed': False
            }

        # 根据不同项目定制评分逻辑
        scoring_func = getattr(self, f'_score_project_{project_id}', None)
        if scoring_func:
            return scoring_func(user_code, exec_output)
        else:
            return self._default_scoring(user_code, exec_output)

    def _default_scoring(self, user_code: str, output: str) -> Dict[str, Any]:
        """默认评分"""
        score = 70
        feedback_parts = []

        if 'print' in user_code:
            score += 10
            feedback_parts.append('✓ 正确使用了打印语句')
        if output and len(output) > 0:
            score += 20
            feedback_parts.append('✓ 代码产生了有效输出')

        return {
            'score': min(score, 100),
            'max_score': 100,
            'feedback': '\n'.join(feedback_parts),
            'passed': score >= 60
        }

    def _score_project_1(self, code: str, output: str) -> Dict[str, Any]:
        """项目1: Python基础-营收求和"""
        score = 0
        feedback = []

        # 检查关键元素
        if '1280' in code and '2560' in code and '1890' in code:
            score += 30
            feedback.append('✓ 正确录入了销售数据')

        if 'sum' in code or 'for' in code or '+' in code:
            score += 25
            feedback.append('✓ 使用了求和计算')

        if 'len' in code or '/3' in code or '/ 3' in code:
            score += 15
            feedback.append('✓ 正确计算了日均销售额')

        if '5730' in output:
            score += 20
            feedback.append('✓ 总销售额计算正确 (5730元)')

        if '1910' in output or '1910.00' in output:
            score += 10
            feedback.append('✓ 日均销售额计算正确 (1910.00元)')

        return {
            'score': min(score, 100),
            'max_score': 100,
            'feedback': '\n'.join(feedback) if feedback else '代码执行完成',
            'passed': score >= 60
        }

    def _score_project_2(self, code: str, output: str) -> Dict[str, Any]:
        """项目2: NumPy数组-用户量翻倍"""
        score = 0
        feedback = []

        if 'numpy' in code.lower() or 'np.' in code:
            score += 20
            feedback.append('✓ 正确使用了numpy')

        if 'array' in code:
            score += 15
            feedback.append('✓ 创建了numpy数组')

        if '* 1.15' in code or '*1.15' in code or '1.15' in code:
            score += 25
            feedback.append('✓ 正确应用了15%的上浮')

        if '138' in output and '282' in output:
            score += 25
            feedback.append('✓ 计算结果正确')

        if 'int' in code or 'astype' in code or 'round' in code:
            score += 15
            feedback.append('✓ 正确处理了整数转换')

        return {
            'score': min(score, 100),
            'max_score': 100,
            'feedback': '\n'.join(feedback) if feedback else '代码执行完成',
            'passed': score >= 60
        }

    def _score_project_3(self, code: str, output: str) -> Dict[str, Any]:
        """项目3: Pandas创建数据表"""
        score = 0
        feedback = []

        if 'pandas' in code.lower() or 'pd.' in code:
            score += 20
            feedback.append('✓ 正确导入了pandas')

        if 'DataFrame' in code:
            score += 25
            feedback.append('✓ 创建了DataFrame数据表')

        if '订单号' in code or '订单' in code or '用户' in code:
            score += 20
            feedback.append('✓ 正确构建了订单数据')

        if 'mean' in code or 'describe' in code:
            score += 15
            feedback.append('✓ 进行了统计计算')

        if '116.13' in output or '116' in output:
            score += 20
            feedback.append('✓ 平均消费金额计算正确')

        return {
            'score': min(score, 100),
            'max_score': 100,
            'feedback': '\n'.join(feedback) if feedback else '代码执行完成',
            'passed': score >= 60
        }

    def _score_project_4(self, code: str, output: str) -> Dict[str, Any]:
        """项目4: Pandas缺失值清洗"""
        score = 0
        feedback = []

        if 'pandas' in code.lower() or 'pd.' in code:
            score += 15
            feedback.append('✓ 正确导入了pandas')

        if 'DataFrame' in code:
            score += 15
            feedback.append('✓ 创建了数据表')

        if 'fillna' in code:
            score += 30
            feedback.append('✓ 正确使用了fillna方法')
        elif 'mean' in code:
            score += 15
            feedback.append('✓ 计算了均值')

        if '120' in output and '95' in output:
            score += 20
            feedback.append('✓ 原始数据保留正确')

        if '107.5' in output or '107' in output:
            score += 20
            feedback.append('✓ 均值填充正确 (107.5)')

        return {
            'score': min(score, 100),
            'max_score': 100,
            'feedback': '\n'.join(feedback) if feedback else '代码执行完成',
            'passed': score >= 60
        }

    def _score_project_5(self, code: str, output: str) -> Dict[str, Any]:
        """项目5: Matplotlib柱状图"""
        score = 0
        feedback = []

        if 'matplotlib' in code.lower() or 'plt' in code:
            score += 25
            feedback.append('✓ 正确导入了matplotlib')

        if 'bar' in code:
            score += 25
            feedback.append('✓ 创建了柱状图')

        if 'title' in code:
            score += 15
            feedback.append('✓ 添加了图表标题')

        if '3200' in code and '4500' in code and '3800' in code and '5200' in code:
            score += 15
            feedback.append('✓ 正确录入了流量数据')

        if 'xlabel' in code and 'ylabel' in code:
            score += 10
            feedback.append('✓ 添加了坐标轴标签')

        if 'show' in code or 'savefig' in code:
            score += 10
            feedback.append('✓ 正确展示了图表')

        return {
            'score': min(score, 100),
            'max_score': 100,
            'feedback': '\n'.join(feedback) if feedback else '代码执行完成',
            'passed': score >= 60
        }

    def _score_project_6(self, code: str, output: str) -> Dict[str, Any]:
        """项目6: Pandas数据筛选"""
        return self._default_scoring(code, output)

    def _score_project_7(self, code: str, output: str) -> Dict[str, Any]:
        """项目7: 数据分组聚合"""
        return self._default_scoring(code, output)

    def _score_project_8(self, code: str, output: str) -> Dict[str, Any]:
        """项目8: 时间序列分析"""
        return self._default_scoring(code, output)

    def _score_project_9(self, code: str, output: str) -> Dict[str, Any]:
        """项目9: 数据可视化进阶"""
        return self._default_scoring(code, output)

    def _score_project_10(self, code: str, output: str) -> Dict[str, Any]:
        """项目10: 综合数据分析报告"""
        return self._default_scoring(code, output)


class AIFeedbackEngine:
    """AI反馈引擎 - 模拟AI给出代码改进建议"""

    def generate_feedback(self, project_id: int, user_code: str,
                          score: float, output: str) -> Dict[str, Any]:
        """生成智能反馈"""
        suggestions = []
        quality_score = min(score + 10, 95)  # 代码质量评分略低于功能分

        # 通用建议
        if 'print' not in user_code and 'plt' not in user_code:
            suggestions.append('建议添加print语句来输出中间结果，便于调试和理解')

        if len(user_code.strip().split('\n')) < 3:
            suggestions.append('代码略显简短，可以考虑增加注释或拆分更多步骤')

        if '#' not in user_code:
            suggestions.append('良好的代码应该有适当的注释，便于他人理解')

        # 项目特定建议
        project_specific = {
            1: ['可以使用列表推导式和sum()函数让代码更简洁',
                '建议使用f-string来格式化输出，语法更清晰'],
            2: ['NumPy数组操作比Python列表更快，适合批量运算',
                '可以使用np.where()来处理条件筛选'],
            3: ['建议学习pandas的数据结构: Series和DataFrame',
                '可以用df.info()或df.describe()来快速了解数据概况'],
            4: ['除了mean()，还可以使用median()中位数或ffill()前向填充',
                '可以用df.isnull().sum()来检查每列的缺失值数量'],
            5: ['建议尝试不同的图表类型: plt.plot折线图、plt.pie饼图等',
                '可以设置颜色、图例和样式来美化图表'],
            6: ["可以使用条件筛选: df[df['列名'] > 值]",
                '学习使用df.loc和df.iloc进行行列选择'],
            7: ['groupby是pandas的核心功能之一，建议深入学习',
                '可以配合agg()进行多种聚合计算'],
            8: ['Pandas提供了强大的日期处理功能: to_datetime',
                '可以使用resample进行时间频率转换'],
            9: ['Plotly可以生成交互式图表，体验更好',
                'Seaborn提供了更高级的统计可视化功能'],
            10: ['建议系统化学习数据分析流程: 采集->清洗->分析->可视化',
                '可以将分析结果整理成Jupyter Notebook报告']
        }

        suggestions.extend(project_specific.get(project_id, []))

        # 根据分数给出评价
        if score >= 90:
            praise = '🌟 非常优秀！代码逻辑清晰，计算准确。'
        elif score >= 70:
            praise = '👍 做得不错！还有一些优化空间。'
        elif score >= 60:
            praise = '✅ 基本完成了任务，继续加油！'
        else:
            praise = '📝 需要更多练习，建议参考示例代码。'

        return {
            'praise': praise,
            'suggestions': suggestions,
            'quality_score': quality_score,
            'knowledge_points': self._get_knowledge_points(project_id)
        }

    def _get_knowledge_points(self, project_id: int) -> List[str]:
        """获取项目知识点"""
        points = {
            1: ['Python列表操作', '循环遍历', '格式化输出', '类型转换'],
            2: ['NumPy数组', '向量运算', '类型转换', '数学函数'],
            3: ['Pandas数据结构', 'DataFrame创建', '描述统计', '数据预览'],
            4: ['缺失值检测', '均值填充', '数据清洗', 'fillna方法'],
            5: ['Matplotlib基础', '柱状图', '图表美化', '中文显示'],
            6: ['数据筛选', '条件查询', '布尔索引', '数据子集'],
            7: ['分组聚合', 'groupby', '多维度统计', '数据透视'],
            8: ['日期处理', '时间索引', '时序分析', 'resample'],
            9: ['多图布局', '交互式图表', '图表美化', '数据可视化'],
            10: ['数据分析流程', '综合应用', '报告生成', '数据洞察']
        }
        return points.get(project_id, ['数据分析基础', 'Python编程', '数据处理'])


# 全局单例实例
executor = CodeExecutor()
scoring_engine = ScoringEngine()
ai_feedback = AIFeedbackEngine()
