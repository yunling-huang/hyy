"""
数据集生成器 - 所有训练项目的数据
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataGenerator:
    """数据生成器类"""

    @staticmethod
    def generate_dirty_chat_logs():
        """项目1: 生成脏数据（AI对话日志）"""
        np.random.seed(42)
        n = 100

        # 正常数据模板
        base_data = {
            'user_id': [f'user_{i:03d}' for i in range(1, n+1)],
            'timestamp': [
                (datetime.now() - timedelta(minutes=random.randint(1, 10000))).strftime('%Y-%m-%d %H:%M:%S')
                for _ in range(n)
            ],
            'message': [
                '你好，我想查询订单', '请问退款多久到账', '产品很好用，满意',
                '发货太慢了', '能不能改地址', '已收到货，很满意',
                '什么时候发货', '产品有质量问题', '服务态度很好'
            ] * 11 + ['感谢客服'] * 1,
            'sentiment': np.random.choice(['positive', 'negative', 'neutral'], n),
            'platform': np.random.choice(['app', 'web', 'mini_app'], n)
        }

        df = pd.DataFrame(base_data)

        # 添加脏数据
        # 1. 空值 (10%)
        null_indices = np.random.choice(n, 10, replace=False)
        for idx in null_indices:
            col = np.random.choice(['message', 'sentiment', 'platform'])
            df.loc[idx, col] = np.nan

        # 2. 乱码 (5%)
        garbage_indices = np.random.choice(n, 5, replace=False)
        for idx in garbage_indices:
            df.loc[idx, 'message'] = '锟斤拷烫烫烫' + ''.join(random.choices('abcdef', k=5))

        # 3. 重复 (8%)
        dup_indices = np.random.choice(n, 8, replace=False)
        df.loc[dup_indices] = df.iloc[dup_indices[0]]

        # 4. 时间格式错误 (5%)
        error_time_indices = np.random.choice(n, 5, replace=False)
        for idx in error_time_indices:
            df.loc[idx, 'timestamp'] = '2023-13-45 25:99:99'

        return df.to_dict('records')

    @staticmethod
    def generate_ecommerce_funnel():
        """项目2: 电商转化漏斗数据"""
        # 模拟用户行为数据
        behaviors = []
        user_ids = [f'user_{i:04d}' for i in range(1, 1001)]

        for user_id in user_ids:
            # 浏览
            behaviors.append({
                'user_id': user_id,
                'action': 'browse',
                'product_id': random.randint(1, 50),
                'timestamp': datetime.now() - timedelta(days=random.randint(1, 30))
            })

            # 加购 (60%转化)
            if random.random() < 0.6:
                behaviors.append({
                    'user_id': user_id,
                    'action': 'add_cart',
                    'product_id': random.randint(1, 50),
                    'timestamp': datetime.now() - timedelta(days=random.randint(1, 30))
                })

                # 支付 (40%转化 from 加购)
                if random.random() < 0.4:
                    behaviors.append({
                        'user_id': user_id,
                        'action': 'payment',
                        'product_id': random.randint(1, 50),
                        'timestamp': datetime.now() - timedelta(days=random.randint(1, 30))
                    })

                    # 完成 (90%转化 from 支付)
                    if random.random() < 0.9:
                        behaviors.append({
                            'user_id': user_id,
                            'action': 'complete',
                            'product_id': random.randint(1, 50),
                            'timestamp': datetime.now() - timedelta(days=random.randint(1, 30))
                        })

        return pd.DataFrame(behaviors)

    @staticmethod
    def generate_sales_with_anomalies():
        """项目3: 带异常值的销售数据"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')

        # 正常销售模式：周末高，工作日低
        sales = []
        for date in dates:
            if date.weekday() >= 5:  # 周末
                base = 15000 + np.random.normal(0, 2000)
            else:  # 工作日
                base = 8000 + np.random.normal(0, 1500)
            sales.append(base)

        sales = np.array(sales)

        # 注入5个异常点
        anomaly_indices = [10, 35, 60, 75, 90]
        anomaly_values = [45000, 500, 38000, 1200, 42000]

        for idx, val in zip(anomaly_indices, anomaly_values):
            sales[idx] = val

        return pd.DataFrame({
            'date': dates,
            'sales': sales,
            'is_anomaly': [i in anomaly_indices for i in range(len(dates))]
        })

    @staticmethod
    def generate_housing_data():
        """项目4: 房价预测数据集（基于sklearn内置数据增强）"""
        from sklearn.datasets import fetch_california_housing
        housing = fetch_california_housing()
        df = pd.DataFrame(housing.data, columns=housing.feature_names)
        df['price'] = housing.target * 100000  # 转换为美元
        return df

    @staticmethod
    def generate_weibo_comments():
        """项目5: 微博评论数据"""
        np.random.seed(42)
        n = 2000

        positive_comments = [
            '这个产品真的很好用，强烈推荐！', '服务态度一级棒，会再来',
            '物流很快，包装也很好', '性价比超高，值得购买',
            '效果很明显，满意', '客服很耐心解答问题',
            '质量很好，和描述一致', '非常满意的一次购物体验',
            '推荐给大家，真的很不错', '下次还会回购的'
        ] * 100

        negative_comments = [
            '太差了，完全不值这个价', '质量有问题，失望',
            '物流太慢了，等了很久', '服务态度差，不推荐',
            '和图片差距太大', '性价比太低，不划算',
            '退换货太麻烦了', '再也不买了',
            '虚假宣传，误导消费者', '后悔买了这个'
        ] * 100

        comments = positive_comments[:1000] + negative_comments[:1000]

        df = pd.DataFrame({
            'id': range(1, n+1),
            'text': comments,
            'label': [1]*1000 + [0]*1000
        })

        return df.sample(frac=1, random_state=42).reset_index(drop=True)

    @staticmethod
    def generate_customer_segments():
        """项目6: 会员消费数据"""
        np.random.seed(42)
        n = 500

        # 模拟不同群体的消费特征
        data = []

        # 高价值会员
        for _ in range(150):
            data.append({
                'customer_id': f'C{len(data)+1:04d}',
                'total_amount': np.random.normal(8000, 2000),
                'purchase频率': np.random.normal(15, 5),
                'recency_days': np.random.normal(20, 10),
                'category': '高价值'
            })

        # 中价值会员
        for _ in range(200):
            data.append({
                'customer_id': f'C{len(data)+1:04d}',
                'total_amount': np.random.normal(3000, 1000),
                'purchase频率': np.random.normal(8, 3),
                'recency_days': np.random.normal(45, 15),
                'category': '中价值'
            })

        # 低价值会员
        for _ in range(150):
            data.append({
                'customer_id': f'C{len(data)+1:04d}',
                'total_amount': np.random.normal(500, 300),
                'purchase频率': np.random.normal(2, 1),
                'recency_days': np.random.normal(90, 30),
                'category': '低价值'
            })

        return pd.DataFrame(data)

    @staticmethod
    def generate_incomplete_customer_data():
        """项目7: 残缺客户数据"""
        np.random.seed(42)
        n = 50

        occupations = ['工程师', '教师', '医生', '销售', '经理', '设计师', '会计', '律师']
        cities = ['北京', '上海', '深圳', '广州', '杭州', '成都']

        data = {
            'customer_id': [f'C{i:04d}' for i in range(1, n+1)],
            'name': [f'客户{i}' for i in range(1, n+1)],
            'email': [f'user{i}@example.com' for i in range(1, n+1)],
            'phone': [f'138{np.random.randint(10000000, 99999999)}' for _ in range(n)],
            'city': np.random.choice(cities, n),
        }

        # 部分字段缺失
        data['age'] = [np.random.randint(18, 65) if random.random() > 0.3 else None for _ in range(n)]
        data['occupation'] = [random.choice(occupations) if random.random() > 0.25 else None for _ in range(n)]
        data['income'] = [np.random.randint(5000, 50000) if random.random() > 0.2 else None for _ in range(n)]

        return pd.DataFrame(data)

    @staticmethod
    def generate_server_metrics():
        """项目8: 服务器监控数据"""
        np.random.seed(42)
        n = 200

        timestamps = pd.date_range(start='2024-01-01', periods=n, freq='h')

        # 正常CPU使用率（带周期性）
        cpu_base = 30 + 20 * np.sin(np.linspace(0, 8*np.pi, n)) + np.random.normal(0, 5, n)

        # 注入异常
        anomaly_indices = [50, 100, 150]
        for idx in anomaly_indices:
            cpu_base[idx] = 95 + np.random.normal(0, 2)

        return pd.DataFrame({
            'timestamp': timestamps,
            'cpu_usage': np.clip(cpu_base, 0, 100),
            'memory_usage': np.clip(40 + 20*np.random.random(n), 0, 100),
            'disk_io': np.clip(30 + 15*np.random.random(n), 0, 100)
        })

    @staticmethod
    def generate_supermarket_orders():
        """项目9: 超市订单数据"""
        np.random.seed(42)

        products = [
            ('牛奶', '乳制品'), ('面包', '烘焙'), ('鸡蛋', '蛋类'), ('牛肉', '肉类'),
            ('苹果', '水果'), ('香蕉', '水果'), ('洗发水', '日用品'), ('牙膏', '日用品'),
            ('可乐', '饮料'), ('薯片', '零食'), ('巧克力', '零食'), ('大米', '粮油'),
            ('面粉', '粮油'), ('土豆', '蔬菜'), ('西红柿', '蔬菜'), ('鸡胸肉', '肉类'),
            ('酸奶', '乳制品'), ('果汁', '饮料'), ('洗衣液', '日用品'), ('纸巾', '日用品')
        ]

        transactions = []
        for trans_id in range(1, 501):
            n_items = np.random.randint(1, 6)
            items = random.sample(products, n_items)
            for product, category in items:
                transactions.append({
                    'transaction_id': trans_id,
                    'product': product,
                    'category': category,
                    'quantity': np.random.randint(1, 4),
                    'price': np.random.uniform(5, 50)
                })

        return pd.DataFrame(transactions)

    @staticmethod
    def get_sample_csv_data():
        """项目10: 样本CSV数据"""
        np.random.seed(42)
        return pd.DataFrame({
            '日期': pd.date_range('2024-01-01', periods=100),
            '销售额': np.random.uniform(1000, 5000, 100) + 2000,
            '访问量': np.random.randint(100, 1000, 100),
            '转化率': np.random.uniform(0.01, 0.1, 100),
            '客户数': np.random.randint(10, 100, 100),
            '客单价': np.random.uniform(50, 500, 100),
            '类别': np.random.choice(['A', 'B', 'C'], 100)
        })

# 数据生成器实例
data_generator = DataGenerator()
