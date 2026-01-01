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
            pair = kwargs.get('pair', ['重心','中線'])
            name, line = pair[0], pair[1]
            return base.format(f'<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><line x1="150" y1="30" x2="150" y2="170" stroke="red" stroke-dasharray="4"/><line x1="50" y1="170" x2="200" y2="100" stroke="red" stroke-dasharray="4"/><text x="150" y="123" fill="blue" font-weight="bold">{name}</text><text x="150" y="190" font-size="12">由{line}交點構成</text>')
        elif svg_type == "roots_line":
            r1, r2 = kwargs.get('r1', 0), kwargs.get('r2', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(r1)}" cy="50" r="5" fill="red"/><text x="{mx(r1)}" y="80" fill="red">{r1}</text><circle cx="{mx(r2)}" cy="50" r="5" fill="red"/><text x="{mx(r2)}" y="80" fill="red">{r2}</text>')
        elif svg_type == "roots_0_k":
            k = kwargs.get('k', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(0)}" cy="50" r="5" fill="red"/><circle cx="{mx(k)}" cy="50" r="5" fill="red"/><text x="{mx(k)}" y="80" fill="red">{k}</text>')
        elif svg_type == "roots_sq":
            k = kwargs.get('k', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(k)}" cy="50" r="5" fill="red"/><text x="{mx(k)}" y="80" fill="red">{k}</text><circle cx="{mx(-k)}" cy="50" r="5" fill="red"/><text x="{mx(-k)}" y="80" fill="red">-{k}</text>')
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
    variables = {}
    
    # 1. 變數隨機化
    if "variables" in template:
        for var_name, range_list in template["variables"].items():
            if not range_list: continue
            if isinstance(range_list[0], list): # 選項列表
                variables[var_name] = random.choice(range_list)
            elif isinstance(range_list[0], int): # 數字範圍
                variables[var_name] = random.randint(range_list[0], range_list[1])

    # 2. 處理 list 變數展開
    flat_vars = variables.copy()
    for k, v in variables.items():
        if isinstance(v, list):
            flat_vars[k] = v
            for i, val in enumerate(v):
                flat_vars[f"{k}_{i}"] = val
    
    # 額外計算
    safe_env = {"math": math, "int": int, "abs": abs, **flat_vars}
    if "calc_extra" in template:
        for k, expr in template["calc_extra"].items():
            try:
                flat_vars[k] = eval(str(expr), {"__builtins__": {}}, safe_env)
                safe_env[k] = flat_vars[k]
            except: pass

    # 3. 計算答案
    try:
        ans_val = eval(str(template["answer_formula"]), {"__builtins__": {}}, safe_env)
        
        options = [str(ans_val)]
        if "wrong_formulas" in template:
            for form in template["wrong_formulas"]:
                try:
                    w_val = eval(str(form), {"__builtins__": {}}, safe_env)
                    if str(w_val) != str(ans_val) and str(w_val) not in options:
                        options.append(str(w_val))
                except: pass
        
        if "fixed_options" in template:
            options = template["fixed_options"]
        else:
            while len(options) < 4:
                fake = random.randint(1, 100)
                if str(fake) not in options: options.append(str(fake))
            random.shuffle(options)
        
        q_text = template["question_text"].format(**flat_vars)
        expl_text = template["explanation"].format(**flat_vars, ans=ans_val)
        
        # 處理 SVG 參數覆蓋
        svg_vars = flat_vars.copy()
        if "params_override" in template:
            for k, v in template["params_override"].items():
                # 如果值是字串且在變數裡，就替換
                if isinstance(v, str) and v in flat_vars:
                    svg_vars[k] = flat_vars[v]
                else:
                    svg_vars[k] = v

        svg = SVGDrawer.draw(template.get("svg", "none"), **svg_vars)
        
        return {
            "q": q_text,
            "options": options,
            "correct_ans": str(ans_val),
            "expl": expl_text,
            "svg": svg
        }
    except Exception as e:
        return {"q": f"生成錯誤: {e}", "options": ["Error"], "correct_ans": "Error", "expl": "", "svg": ""}

# ==========================================
# 3. APP 介面
# ==========================================
st.set_page_config(page_title="數學習題載入器", page_icon="📂")
st.title("📂 國中數學習題載入器 (V24)")
st.info("請上傳 `questions.json` 題庫檔，系統會讀取其中定義的所有題目。")

uploaded_file = st.file_uploader("上傳題庫檔 (.json)", type=['json'])

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        all_questions = []
        for key in data:
            all_questions.extend(data[key])
        
        unit_options = list(data.keys()) + ["全範圍總複習"]
        unit = st.selectbox("選擇單元", unit_options)
        
        if st.button("🚀 生成試卷 (10題不重複)"):
            questions = []
            target_pool = all_questions if unit == "全範圍總複習" else data[unit]
            seen_texts = set()
            attempts = 0
            
            needed = 10
            pool_cycle = target_pool * (needed // len(target_pool) + 2)
            random.shuffle(pool_cycle)
            
            for tmpl in pool_cycle:
                if len(questions) >= needed or attempts > 50: break
                for _ in range(5): 
                    q = generate_question_from_template(tmpl)
                    if q['q'] not in seen_texts and "Error" not in q['q']:
                        seen_texts.add(q['q'])
                        questions.append(q)
                        break
                attempts += 1
            
            st.session_state.quiz = questions
            st.session_state.exam_finished = False
            st.rerun()
            
    except Exception as e:
        st.error(f"檔案讀取失敗: {e}")

if 'quiz' in st.session_state and st.session_state.quiz:
    with st.form("exam"):
        score = 0
        results = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**第 {i+1} 題：**")
            if q['svg']: st.markdown(q['svg'], unsafe_allow_html=True)
            st.markdown(f"### {q['q']}")
            user_ans = st.radio(f"q_{i}", q['options'], label_visibility="collapsed")
            st.divider()
            results.append((q, user_ans))
            if user_ans == q['correct_ans']: score += 1
            
        if st.form_submit_button("✅ 交卷"):
            st.markdown(f"## 得分：{score * 10}")
            for i, (q, u) in enumerate(results):
                with st.expander(f"第 {i+1} 題詳解"):
                    st.write(f"題目：{q['q']}")
                    st.write(f"正解：{q['correct_ans']}")
                    st.info(q['expl'])
