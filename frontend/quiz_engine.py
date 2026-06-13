"""
AI时代Python数据分析训练营 - 课后习题交互引擎
提供：题目渲染、自动判分、进度统计、代码执行沙箱
"""
import streamlit as st
import re
import io
import sys
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Tuple, Optional


# ------------------------------------------------------------
# 工具函数：答案标准化、模糊匹配
# ------------------------------------------------------------
def normalize(text: Any) -> str:
    """将任意类型标准化为可比较字符串"""
    if text is None:
        return ""
    if isinstance(text, bool):
        return "对" if text else "错"
    if isinstance(text, (list, tuple, set)):
        return "|".join(sorted([str(x).strip() for x in text if str(x).strip()]))
    s = str(text).strip()
    # 统一中英文标点、空格大小写
    s = s.replace(" ", "").replace("　", "")
    s = s.replace("，", ",").replace("。", ".").replace("！", "!").replace("？", "?")
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    s = s.replace("：", ":").replace("；", ";")
    s = s.replace("<", "").replace(">", "")
    # 中文数字转阿拉伯数字（简单支持 0-9）
    zh_map = {"零": "0", "一": "1", "二": "2", "两": "2", "三": "3",
              "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
    for k, v in zh_map.items():
        s = s.replace(k, v)
    return s.lower()


def fuzzy_match(user_input: Any, answers: List[str]) -> bool:
    """模糊匹配用户输入与参考答案列表"""
    user_norm = normalize(user_input)
    if not user_norm:
        return False
    for ans in answers:
        ans_norm = normalize(ans)
        if user_norm == ans_norm:
            return True
        # 去除符号后的纯文本匹配
        u = re.sub(r"[^\w\u4e00-\u9fa5]", "", user_norm)
        a = re.sub(r"[^\w\u4e00-\u9fa5]", "", ans_norm)
        if u and a and (u == a):
            return True
        # 包含关系（答案是用户输入的子串）
        if len(ans_norm) >= 2 and (ans_norm in user_norm or user_norm in ans_norm):
            return True
    return False


# ------------------------------------------------------------
# 代码安全沙箱
# ------------------------------------------------------------
def run_code_sandbox(code: str, context: Optional[Dict] = None) -> Tuple[bool, str, str]:
    """执行用户代码，捕获输出与错误"""
    if context is None:
        context = {"pd": pd, "np": np}
    output_buf = io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = output_buf, output_buf
    ok, err = True, ""
    try:
        exec(code, context)
    except Exception as e:
        ok, err = False, f"{type(e).__name__}: {str(e)}"
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
    return ok, output_buf.getvalue().strip(), err


# ------------------------------------------------------------
# 判分引擎
# ------------------------------------------------------------
def judge_question(q: Dict, user_answer: Any, code_output: str = "",
                   code_success: bool = True) -> Tuple[int, str]:
    """根据题目类型自动判分，返回 (得分, 评语)"""
    qtype = q.get("type")
    score_max = q.get("score", 10)

    # 未作答
    if user_answer is None or (isinstance(user_answer, str) and not user_answer.strip()):
        if qtype != "code":
            return 0, "❌ 未作答"

    if qtype == "single":
        # 单选：直接比较 answer / answer_key
        corrects = [q.get("answer", "")] + q.get("acceptable_answers", [])
        if "answer_key" in q:
            corrects.append(q["answer_key"])
        if fuzzy_match(user_answer, corrects):
            return score_max, f"✅ 正确（{q.get('answer_key', q.get('answer'))}）"
        return 0, f"❌ 错误，正确答案：{q.get('answer_key', q.get('answer'))}"

    if qtype == "multi":
        # 多选：需要集合等价
        user_set = set(normalize(x) for x in (user_answer or []))
        correct_set = set(normalize(x) for x in q.get("answer", []))
        if user_set == correct_set:
            return score_max, "✅ 完全正确"
        if user_set and correct_set and user_set.issubset(correct_set):
            # 漏选但不错 - 半分
            return score_max // 2, f"⚠️ 漏选，正确答案：{q.get('answer')}"
        return 0, f"❌ 错误，正确答案：{q.get('answer')}"

    if qtype == "bool":
        # 判断题
        corrects = [q.get("answer_key", ""), q.get("answer", "")]
        # 将 True/False 转为字符串以便比较
        if isinstance(q.get("answer"), bool):
            corrects.append("对" if q["answer"] else "错")
        if fuzzy_match(user_answer, corrects):
            return score_max, f"✅ 判断正确（{q.get('answer_key')}）"
        return 0, f"❌ 判断错误，正确答案：{q.get('answer_key')}"

    if qtype == "fill":
        # 填空题
        corrects = [q.get("answer", "")] + q.get("acceptable_answers", [])
        if fuzzy_match(user_answer, corrects):
            return score_max, "✅ 填空正确"
        return 0, f"❌ 错误，参考答案：{q.get('answer')}"

    if qtype == "code":
        # 代码实操：代码成功执行 + 输出包含预期关键字 即算对
        if not code_success:
            return 0, f"❌ 代码执行异常：{code_output}"
        expected = q.get("expected_output", "").strip()
        if not expected:
            # 未指定预期输出，只要执行成功就给分
            return score_max, "✅ 代码执行成功"
        # 模糊匹配：输出中是否包含预期字符串（去掉空格）
        if normalize(expected) in normalize(code_output) or normalize(code_output) in normalize(expected):
            return score_max, "✅ 输出与预期一致"
        # 包含预期的数字（如 5730、23.0）也算对
        nums_expected = re.findall(r"\d+(?:\.\d+)?", expected)
        if nums_expected and all(n in code_output for n in nums_expected[:2]):
            return score_max, "✅ 关键输出正确"
        # 有输出但与预期不符 - 给半分鼓励
        if code_output:
            return score_max // 2, f"⚠️ 执行成功但输出与预期不符：{code_output[:50]}"
        return 0, "❌ 无输出"

    return 0, "❌ 未知题型"


# ------------------------------------------------------------
# 题目渲染组件
# ------------------------------------------------------------
def render_question(q: Dict, idx: int, quiz_session: Dict) -> None:
    """渲染单个题目到 Streamlit 界面"""
    qid = q.get("qid", f"q{idx}")
    qtype = q.get("type")
    score = q.get("score", 10)
    type_labels = {
        "single": "单选题",
        "multi": "多选题",
        "fill": "填空题",
        "bool": "判断题",
        "code": "代码实操题",
    }

    # 题头
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(
            f"""
            <div style='background: linear-gradient(90deg, rgba(0,212,255,0.12), rgba(255,0,255,0.05));
                 padding: 14px 18px; border-radius: 10px; border-left: 4px solid #00d4ff;'>
                <div style='color:#00d4ff; font-weight: 700; font-size: 0.9rem;'>
                    Q{idx + 1} · {type_labels.get(qtype, qtype)}（{score} 分）
                </div>
                <div style='margin-top: 8px; color: #f0f0f0; font-size: 1rem; line-height: 1.7;'>
                    {q.get('question', '')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        current_score = quiz_session.get(f"{qid}_score", "—")
        st.markdown(
            f"""
            <div style='text-align:center; padding: 16px 8px; background: #1a1f2e;
                        border-radius: 10px; border: 1px solid #30363d;'>
                <div style='color:#888; font-size:0.75rem;'>得分</div>
                <div style='color:#00ff88; font-size:1.5rem; font-weight:700;'>
                    {current_score}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 答题区
    key = f"ans_{qid}"
    feedback = None
    if qtype == "single":
        options = q.get("options", [])
        labels = [f"{chr(65 + i)}. {opt}" for i, opt in enumerate(options)]
        sel = st.radio("请选择答案：", labels, key=key, horizontal=False, label_visibility="collapsed")
        user_answer = options[labels.index(sel)] if sel else ""
        feedback = q.get("explanation", "")

    elif qtype == "multi":
        options = q.get("options", [])
        labels = [f"{chr(65 + i)}. {opt}" for i, opt in enumerate(options)]
        sels = st.multiselect("请选择全部正确答案（可多选）：", labels, key=key,
                              placeholder="点击选择至少一个选项")
        user_answer = [opt for lab, opt in zip(labels, options) if lab in sels]
        feedback = q.get("explanation", "")

    elif qtype == "fill":
        user_answer = st.text_input("请填写答案：", key=key, placeholder="在此输入你的答案...")
        feedback = q.get("explanation", "")

    elif qtype == "bool":
        labels = ["对（True）", "错（False）"]
        sel = st.radio("请判断：", labels, key=key, horizontal=True, label_visibility="collapsed")
        user_answer = "对" if sel == labels[0] else "错"
        feedback = q.get("explanation", "")

    elif qtype == "code":
        st.markdown("**📝 代码编辑区**")
        init = q.get("initial_code", "")
        user_code = st.text_area("在下方编写/修改代码：", value=init, height=160,
                                 key=f"code_{qid}", label_visibility="collapsed")
        user_answer = user_code

        # 代码运行按钮
        col_run, col_ref = st.columns([1, 1])
        with col_run:
            if st.button(f"▶️ 运行并提交 (Q{idx + 1})", key=f"run_{qid}", use_container_width=True,
                         type="primary"):
                ok, out, err = run_code_sandbox(user_code)
                if ok:
                    st.markdown(
                        f"""
                        <div style='background:#0f1d14; padding: 12px 16px; border-radius: 8px;
                                    border-left: 4px solid #00ff88; margin-top: 10px;'>
                            <div style='color:#00ff88; font-weight:700;'>✅ 执行成功</div>
                            <pre style='color:#e6e6e6; white-space: pre-wrap; margin: 8px 0 0;
                                 background:#0b130d; padding: 10px; border-radius: 6px;'>{out or '(无输出)'}</pre>
                        </div>
                        """, unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div style='background:#1d0f0f; padding: 12px 16px; border-radius: 8px;
                                    border-left: 4px solid #ff4444; margin-top: 10px;'>
                            <div style='color:#ff4444; font-weight:700;'>❌ 执行异常</div>
                            <pre style='color:#ffaaaa; white-space: pre-wrap; margin: 8px 0 0;
                                 background:#130808; padding: 10px; border-radius: 6px;'>{err}</pre>
                        </div>
                        """, unsafe_allow_html=True,
                    )
                got, msg = judge_question(q, user_code, code_output=out, code_success=ok)
                quiz_session[f"{qid}_score"] = got
                quiz_session[f"{qid}_msg"] = msg
                quiz_session[f"{qid}_judged"] = True

        with col_ref:
            with st.expander(f"💡 查看参考答案 (Q{idx + 1})", expanded=False):
                ref_code = q.get("reference_code", "")
                if ref_code:
                    st.code(ref_code, language="python")
                exp_out = q.get("expected_output", "")
                if exp_out:
                    st.markdown(f"**预期输出：**\n```\n{exp_out}\n```")

        feedback = q.get("explanation", "")

    else:
        st.warning("未知题型")
        user_answer = ""

    # 非代码题：提供独立的提交按钮
    if qtype != "code":
        col_submit, col_ans = st.columns([1, 1])
        with col_submit:
            if st.button(f"✅ 提交本题答案 (Q{idx + 1})", key=f"submit_{qid}", use_container_width=True):
                got, msg = judge_question(q, user_answer)
                quiz_session[f"{qid}_score"] = got
                quiz_session[f"{qid}_msg"] = msg
                quiz_session[f"{qid}_judged"] = True

        with col_ans:
            with st.expander(f"💡 查看参考答案与解析 (Q{idx + 1})", expanded=False):
                if qtype in ("single", "bool"):
                    st.markdown(f"**正确答案：** `{q.get('answer_key')} （{q.get('answer')}）`")
                elif qtype == "multi":
                    st.markdown(f"**正确答案：** `{', '.join(q.get('answer_keys', []))}`")
                elif qtype == "fill":
                    st.markdown(f"**参考答案：** `{q.get('answer')}`")
                if feedback:
                    st.markdown(f"**📖 解析：**\n\n{feedback}")

    # 显示得分与反馈信息（提交后）
    if quiz_session.get(f"{qid}_judged"):
        got = quiz_session.get(f"{qid}_score", 0)
        msg = quiz_session.get(f"{qid}_msg", "")
        color = "#00ff88" if got == score else "#ffaa00" if got > 0 else "#ff4444"
        st.markdown(
            f"""
            <div style='margin-top: 12px; padding: 14px 18px; border-radius: 10px;
                        background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(255,0,255,0.04));
                        border: 1px solid #30363d;'>
                <div style='color: {color}; font-weight: 700; font-size: 1rem;'>
                    🏷️ 判定结果：{msg}
                </div>
                <div style='color: #f0f0f0; margin-top: 8px; font-size: 0.95rem;'>
                    本题得分：<b style='color:{color}; font-size:1.2rem;'>{got}</b> / {score}
                </div>
                {f"<div style='color:#888; margin-top:8px; line-height:1.7;'>📖 {feedback}</div>" if feedback and got < score else ""}
            </div>
            """, unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:#21262d; margin: 24px 0;'>", unsafe_allow_html=True)


# ------------------------------------------------------------
# 进度面板
# ------------------------------------------------------------
def render_progress_panel(quiz_session: Dict, total_questions: int, full_score: int):
    """展示当前练习的得分与进度"""
    got_list = [v for k, v in quiz_session.items() if k.endswith("_score") and isinstance(v, int)]
    cur_total = sum(got_list)
    answered = len(got_list)
    percent = int((cur_total / full_score) * 100) if full_score > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📊 当前得分", f"{cur_total} / {full_score}")
    with c2:
        st.metric("✅ 已答题目", f"{answered} / {total_questions}")
    with c3:
        st.metric("🎯 得分率", f"{percent}%")
    with c4:
        status = "🏆 满分大神" if percent == 100 else "🌟 优秀" if percent >= 80 else \
                 "👍 良好" if percent >= 60 else "💪 继续努力"
        st.metric("评价", status)

    st.markdown(
        f"""
        <div style='background:#0d1117; border:1px solid #21262d; height: 18px; border-radius: 10px;
                    overflow: hidden; margin: 12px 0 0;'>
            <div style='background: linear-gradient(90deg, #00d4ff, #ff00ff);
                        width: {percent}%; height: 100%; transition: width 0.6s ease;'></div>
        </div>
        """, unsafe_allow_html=True,
    )
    st.markdown("---")
