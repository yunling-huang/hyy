"""
代码执行引擎 - 安全沙箱环境
"""
import pandas as pd
import numpy as np
import sys
import io
import traceback
import time
from typing import Dict, Any, Tuple

class CodeExecutor:
    """代码执行器"""

    def __init__(self):
        self.allowed_modules = [
            'pandas', 'numpy', 'sklearn', 'matplotlib',
            'seaborn', 'plotly', 'scipy', 'statsmodels'
        ]
        self.df_store = {}  # 存储DataFrame供后续使用

    def execute(self, code: str, context: Dict[str, Any] = None) -> Tuple[bool, str, str, float]:
        """
        执行用户代码
        返回: (success, output, error, execution_time)
        """
        start_time = time.time()

        # 创建安全的执行环境
        safe_globals = {
            '__builtins__': self._get_safe_builtins(),
            'pd': pd,
            'np': np,
            'df': None,  # 将在上下文中提供
            'data': context.get('data') if context else None,
        }

        # 添加上下文中的数据
        if context:
            for key, value in context.items():
                if key != 'data':
                    safe_globals[key] = value

        # 创建输出捕获
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        try:
            # 执行代码
            exec(code, safe_globals)

            # 获取输出
            output = output_buffer.getvalue()

            # 检查是否有图表生成
            import matplotlib.pyplot as plt
            if plt.get_fignums():
                output += "\n[图表已生成]"

            execution_time = time.time() - start_time
            return True, output, "", execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            error = traceback.format_exc()
            return False, "", error, execution_time

        finally:
            output_buffer.close()
            error_buffer.close()

    def _get_safe_builtins(self):
        """获取安全的内置函数"""
        safe_builtins = {}
        for name in ['len', 'str', 'int', 'float', 'list', 'dict', 'tuple', 'set', 'print',
                     'range', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'reversed',
                     'any', 'all', 'sum', 'min', 'max', 'abs', 'round', 'open', 'isinstance',
                     'type', 'hasattr', 'getattr', 'setattr', 'True', 'False', 'None']:
            safe_builtins[name] = __builtins__[name]
        return safe_builtins

    def validate_code(self, code: str) -> Tuple[bool, str]:
        """
        验证代码安全性
        """
        dangerous_patterns = [
            'import os',
            'import sys',
            'import subprocess',
            'import socket',
            'import requests',
            'import urllib',
            'open(',
            'eval(',
            'exec(',
            '__import__',
            'os.system',
            'os.popen',
            'subprocess.',
            'socket.',
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                return False, f"禁止使用: {pattern}"

        return True, "代码安全"

# 全局执行器实例
executor = CodeExecutor()
