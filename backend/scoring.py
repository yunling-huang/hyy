"""
评分引擎 - 各项目的评分逻辑
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List

class ScoringEngine:
    """评分引擎"""

    @staticmethod
    def evaluate_data_cleaning(user_df: pd.DataFrame, original_df: pd.DataFrame) -> Tuple[float, str, List[str]]:
        """
        项目1: 数据清洗评分
        """
        score = 0
        max_score = 100
        feedback = []
        hints = []

        # 检查缺失值处理
        null_count = user_df.isnull().sum().sum()
        original_null_count = original_df.isnull().sum().sum()

        if null_count == 0:
            score += 30
            feedback.append("✓ 成功处理所有空值")
        elif null_count < original_null_count:
            score += 15
            feedback.append("△ 部分空值未处理")
            hints.append("使用 df.dropna() 删除空值行，或 df.fillna() 填充空值")
        else:
            feedback.append("✗ 空值处理不当")

        # 检查重复值处理
        dup_count = user_df.duplicated().sum()
        if dup_count == 0:
            score += 30
            feedback.append("✓ 成功去除重复数据")
        else:
            feedback.append(f"✗ 仍有 {dup_count} 条重复记录")
            hints.append("使用 df.drop_duplicates() 去除重复")

        # 检查数据完整性
        if len(user_df) > 50:  # 删除空行和重复后应该少于100
            score += 20
            feedback.append("✓ 数据行数合理")
        else:
            hints.append("注意保留有效数据行")

        # 检查是否保持了必要列
        essential_cols = ['user_id', 'message', 'sentiment']
        if all(col in user_df.columns for col in essential_cols):
            score += 20
            feedback.append("✓ 保持必要的数据列")
        else:
            hints.append("确保保留 user_id, message, sentiment 等关键列")

        # 生成反馈
        final_feedback = "\n".join(feedback) if feedback else "数据清洗完成"

        return score, final_feedback, hints

    @staticmethod
    def evaluate_funnel_analysis(user_result: Dict[str, int]) -> Tuple[float, str, List[str]]:
        """
        项目2: 漏斗分析评分
        """
        score = 0
        max_score = 100
        feedback = []
        hints = []

        expected_stages = ['browse', 'add_cart', 'payment', 'complete']
        expected_rates = {'browse': 100, 'add_cart': 60, 'payment': 40, 'complete': 90}

        if all(stage in user_result for stage in expected_stages):
            # 计算转化率
            rates = {}
            for i, stage in enumerate(expected_stages):
                if i == 0:
                    rates[stage] = 100
                else:
                    prev_stage = expected_stages[i-1]
                    if user_result.get(prev_stage, 0) > 0:
                        rates[stage] = (user_result.get(stage, 0) / user_result.get(prev_stage, 0)) * 100
                    else:
                        rates[stage] = 0

            # 与预期对比
            total_diff = sum(abs(rates.get(stage, 0) - expected_rates[stage]) for stage in expected_stages)
            accuracy = max(0, 100 - total_diff)

            score = accuracy
            feedback.append(f"转化率计算准确度: {accuracy:.1f}%")

            # 找出最低转化环节
            min_stage = min(rates, key=rates.get)
            if rates[min_stage] < 50:
                hints.append(f"'{min_stage}'环节转化率最低，建议重点优化")

        else:
            score = 50
            feedback.append("请确保计算所有阶段的数据")
            hints.append("使用 groupby().size() 统计各阶段用户数")

        return score, "\n".join(feedback), hints

    @staticmethod
    def evaluate_anomaly_detection(user_anomalies: List[int], true_anomalies: List[int]) -> Tuple[float, str]:
        """
        项目3: 异常值检测评分
        """
        true_set = set(true_anomalies)
        user_set = set(user_anomalies)

        # 正确检测
        true_positives = len(true_set & user_set)
        # 误报
        false_positives = len(user_set - true_set)
        # 漏报
        false_negatives = len(true_set - user_set)

        score = (true_positives * 20) - (false_positives * 10) - (false_negatives * 15)
        score = max(0, min(100, score))

        if true_positives == len(true_anomalies) and false_positives == 0:
            feedback = "完美！你找到了所有异常值且没有误报"
        elif true_positives == len(true_anomalies):
            feedback = f"找到了所有异常值，但有 {false_positives} 个误报"
        elif true_positives > 0:
            feedback = f"找到了 {true_positives} 个异常值，漏报 {false_negatives} 个，误报 {false_positives} 个"
        else:
            feedback = "未找到任何异常值，请检查检测方法"

        return score, feedback

    @staticmethod
    def evaluate_ml_model(mse: float, feature_importance: Dict[str, float] = None) -> Tuple[float, str, List[str]]:
        """
        项目4: 机器学习模型评分
        """
        score = 0
        feedback = []
        hints = []

        # MSE评分 (MSE越低越好)
        if mse < 0.5:
            score = 100
            feedback.append("优秀！模型误差非常低")
        elif mse < 1.0:
            score = 80
            feedback.append("良好，模型性能不错")
        elif mse < 2.0:
            score = 60
            feedback.append("一般，建议调整参数")
            hints.append("尝试增加决策树深度或调整学习率")
        else:
            score = 40
            feedback.append("模型误差较大")
            hints.append("可以尝试: 1) 增加模型复杂度 2) 调整测试集比例 3) 使用特征工程")

        if feature_importance:
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
            feedback.append(f"重要特征: {', '.join([f[0] for f in top_features])}")

        return score, "\n".join(feedback), hints

    @staticmethod
    def evaluate_sentiment_analysis(y_true: List[int], y_pred: List[int]) -> Tuple[float, str]:
        """
        项目5: 情感分析评分
        """
        from sklearn.metrics import accuracy_score, confusion_matrix

        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)

        score = accuracy * 100

        feedback = f"准确率: {accuracy*100:.1f}%\n"
        feedback += f"混淆矩阵:\n正类预测正确: {cm[1,1]}, 负类预测正确: {cm[0,0]}"

        if accuracy > 0.85:
            feedback += "\n优秀！模型泛化能力很强"
        elif accuracy > 0.75:
            feedback += "\n良好，仍有提升空间"
        else:
            feedback += "\n建议增加训练迭代次数或调整参数"

        return score, feedback

    @staticmethod
    def evaluate_clustering(k_chosen: int, true_k: int = 3) -> Tuple[float, str, List[str]]:
        """
        项目6: 聚类分析评分
        """
        score = 0
        feedback = []
        hints = []

        if k_chosen == true_k:
            score = 100
            feedback.append("完美！选择了正确的聚类数量")
        elif abs(k_chosen - true_k) == 1:
            score = 70
            feedback.append("接近正确聚类数")
            hints.append("可使用肘部法则或轮廓系数确定最优K值")
        elif abs(k_chosen - true_k) <= 3:
            score = 50
            feedback.append(f"聚类数选择偏离较大（选择{k_chosen}，建议{true_k}）")
            hints.append("观察聚类散点图，K=3时应有明显的群体分离")
        else:
            score = 30
            feedback.append("聚类数选择不当")

        return score, "\n".join(feedback), hints

    @staticmethod
    def evaluate_llm_completion(user_completions: pd.DataFrame, ground_truth: pd.DataFrame) -> Tuple[float, str]:
        """
        项目7: LLM数据补全评分
        """
        score = 0
        feedback = []

        # 比较缺失字段的补全准确率
        accuracy_by_field = {}

        for col in ['age', 'occupation', 'income']:
            if col in user_completions.columns and col in ground_truth.columns:
                mask = ground_truth[col].notna()
                if mask.sum() > 0:
                    # 数值字段允许一定误差
                    if col == 'age':
                        exact_match = (user_completions.loc[mask, col] == ground_truth.loc[mask, col]).mean()
                    elif col == 'income':
                        # 允许20%误差
                        ratio = user_completions.loc[mask, col] / ground_truth.loc[mask, col].replace(0, 1)
                        exact_match = ((ratio > 0.8) & (ratio < 1.2)).mean()
                    else:
                        exact_match = (user_completions.loc[mask, col] == ground_truth.loc[mask, col]).mean()

                    accuracy_by_field[col] = exact_match

        if accuracy_by_field:
            avg_accuracy = np.mean(list(accuracy_by_field.values()))
            score = avg_accuracy * 100

            for field, acc in accuracy_by_field.items():
                feedback.append(f"{field}: {acc*100:.1%}准确率")

        return score, "\n".join(feedback)

    @staticmethod
    def evaluate_anomaly_detection_streaming(predicted: List[int], actual: List[int]) -> Tuple[float, str]:
        """
        项目8: 实时异常检测评分
        """
        from sklearn.metrics import precision_recall_f1_support

        if len(predicted) != len(actual):
            return 50, "预测长度与实际不符"

        precision, recall, f1, _ = precision_recall_f1_support(actual, predicted, average='binary')

        score = f1 * 100

        feedback = f"精确率: {precision*100:.1f}%, 召回率: {recall*100:.1f}%, F1: {f1*100:.1f}%"

        return score, feedback

    @staticmethod
    def evaluate_association_rules(rules: List[Dict], min_confidence: float = 0.5) -> Tuple[float, str]:
        """
        项目9: 关联规则评分
        """
        score = 0
        feedback = []

        if not rules:
            return 0, "未生成任何关联规则"

        # 评估规则质量
        valid_rules = [r for r in rules if r.get('confidence', 0) >= min_confidence]

        if len(valid_rules) >= 5:
            score += 40  # 规则数量得分

        # 规则置信度平均分
        avg_confidence = np.mean([r.get('confidence', 0) for r in rules])
        score += avg_confidence * 40

        # 支持度
        avg_support = np.mean([r.get('support', 0) for r in rules])
        score += min(avg_support * 100, 20)  # 最多20分

        feedback.append(f"生成了 {len(rules)} 条规则")
        feedback.append(f"平均置信度: {avg_confidence*100:.1f}%")
        feedback.append(f"平均支持度: {avg_support*100:.1f}%")

        if avg_confidence > 0.7:
            feedback.append("规则质量优秀！")

        return min(score, 100), "\n".join(feedback)

# 评分引擎实例
scoring_engine = ScoringEngine()
