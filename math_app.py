import streamlit as st
import json
import random
import math

# ==========================================
# 1. 視覺繪圖引擎 (SVG)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{}</svg>'
        
        if svg_type == "geometry_sas":
            return base.format('<path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black"/><text x="50" y="140">A</text><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black"/><text x="180" y="140">B</text><text x="115" y="80" fill="blue" font-weight="bold">全等?</text>')
        elif svg_type == "triangle_centroid":
            m = kwargs.get('m', '?')
            return base.format(f'<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="150" y="15">A</text><text x="40" y="180">B</text><text x="260" y="180">C</text><text x="150" y="195" fill="red">D</text><text x="165" y="126" fill="blue">G</text><text x="20" y="50">AD={m}</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="green"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><text x="150" y="15">A</text><text x="70" y="140">B</text><text x="230" y="140">C</text><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="115" fill="green">O</text>')
        elif svg_type == "triangle_incenter":
            a = kwargs.get('a', '?')
            return base.format(f'<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><text x="150" y="20">A</text><text x="40" y="170">B</text><text x="260" y="170">C</text><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange">I</text><text x="20" y="50">∠A={a}°</text>')
        elif svg_type == "center_def_dynamic":
            return base.format('<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><line x1="150" y1="30" x2="150" y2="170" stroke="red" stroke-dasharray="4"/><line x1="50" y1="170" x2="200" y2="100" stroke="red" stroke-dasharray="4"/><text x="150" y="123" fill="blue" font-weight="bold">Center</text>')
        elif svg_type == "roots_line":
            r1, r2 = kwargs.get('r1', 0), kwargs.get('r2', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(r1)}" cy="50" r="5" fill="red"/><text x="{mx(r1)}" y="80" fill="red">{r1}</text><circle cx="{mx(r2)}" cy="50" r="5" fill="red"/><text x="{mx(r2)}" y="80" fill="red">{r2}</text>')
        elif svg_type == "roots_0_k":
            k = kwargs.get('k', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(0)}" cy="50" r="5" fill="red"/><circle cx="{mx(k)}" cy="50" r="5" fill="red"/><text x="{mx(k)}" y="80" fill="red">{k}</text>')
        elif svg_type == "area_square":
            s = kwargs.get('s', 10)
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">Area={s*s}</text><text x="150" y="170" text-anchor="middle">邊長=?</text>')
        elif svg_type == "area_square_k":
            k = kwargs.get('k', 10)
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">補上?</text><text x="150" y="170" text-anchor="middle">邊長={k}/2</text>')
        return ""

# ==========================================
# 2. 考卷生成邏輯
# ==========================================
def generate_question_from_template(template):
    variables = template.get("variables", {}).copy()
    
    # 處理參數覆蓋 (SVG用)
    svg_vars = variables.copy()
    if "params_override" in template:
        svg_vars.update(template["params_override"])

    # 選項處理
    options = []
    if "fixed_options" in template:
        options = template["fixed_options"].copy()
    else:
        options = [template["answer_formula"]] + template.get("wrong_formulas", [])
    
    random.shuffle(options)
    
    svg = SVGDrawer.draw(template.get("svg", "none"), **svg_vars)
    
    return {
        "q": template["question_text"],
        "options": options,
        "correct_ans": template["answer_formula"],
        "expl": template["explanation"],
        "svg": svg
    }

# ==========================================
# 3. APP 介面
# ==========================================
st.set_page_config(page_title="數學習題載入器", page_icon="📂")
st.title("📂 國中數學習題載入器 (V24.3 最終版)")

if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False
if 'exam_results' not in st.session_state: st.session_state.exam_results = []
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0

uploaded_file = st.file_uploader("請上傳您的題庫檔 (questions.json)", type=['json'])

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        all_questions = []
        for key in data:
            all_questions.extend(data[key])
        
        unit_options = list(data.keys()) + ["全範圍總複習"]
        unit = st.selectbox("選擇單元", unit_options)
        
        if not st.session_state.exam_finished:
            if st.button("🚀 生成試卷 (10題)"):
                target_pool = all_questions if unit == "全範圍總複習" else data[unit]
                
                # 隨機抽取 10 題
                if len(target_pool) >= 10:
                    selected_templates = random.sample(target_pool, 10)
                else:
                    selected_templates = random.choices(target_pool, k=10) # 題目不夠時重複抽
                
                questions = []
                for tmpl in selected_templates:
                    questions.append(generate_question_from_template(tmpl))
                
                st.session_state.quiz = questions
                st.session_state.exam_finished = False
                st.rerun()
            
    except Exception as e:
        st.error(f"檔案讀取失敗: {e}")

if 'quiz' in st.session_state and st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("exam_form"):
        user_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**第 {i+1} 題：**")
            if q['svg']: st.markdown(q['svg'], unsafe_allow_html=True)
            st.markdown(f"### {q['q']}")
            ans = st.radio(f"q_{i}", q['options'], key=f"ans_{i}", label_visibility="collapsed")
            st.divider()
            user_answers.append(ans)
            
        if st.form_submit_button("✅ 交卷"):
            score = 0
            results = []
            for i, q in enumerate(st.session_state.quiz):
                u_ans = user_answers[i]
                is_correct = (u_ans == q['correct_ans'])
                if is_correct: score += 1
                results.append({"q": q, "user": u_ans, "correct": is_correct})
            
            st.session_state.quiz_score = score * 10
            st.session_state.exam_results = results
            st.session_state.exam_finished = True
            st.rerun()

if st.session_state.exam_finished:
    st.success(f"## 總分：{st.session_state.quiz_score} 分")
    
    for i, item in enumerate(st.session_state.exam_results):
        q = item['q']
        is_right = item['correct']
        status = "✅ 正確" if is_right else "❌ 錯誤"
        
        with st.expander(f"第 {i+1} 題詳解 ({status})"):
            if q['svg']: st.markdown(q['svg'], unsafe_allow_html=True)
            st.write(f"**題目**：{q['q']}")
            st.write(f"**您的答案**：{item['user']}")
            st.write(f"**正確答案**：{q['correct_ans']}")
            if not is_right:
                st.error(f"💡 解析：{q['expl']}")
            else:
                st.info(f"💡 解析：{q['expl']}")
    
    st.divider()
    if st.button("🔄 再來一次 (重新測驗)", use_container_width=True):
        st.session_state.exam_finished = False
        st.session_state.quiz = []
        st.session_state.exam_results = []
        st.rerun()
