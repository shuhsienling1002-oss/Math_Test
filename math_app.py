import streamlit as st
import json
import random
import math

# ==========================================
# 1. 雲端題庫製造機 (直接在記憶體生成)
# ==========================================
@st.cache_data # 這行指令會讓 Streamlit 記住生成的題目，不用每次按鈕都重算
def create_cloud_database():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心、內心與重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # --- 3-1 幾何證明 (生成 200 題) ---
    for _ in range(200):
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        database["3-1 證明與推理"].append({
            "question_text": f"若兩個三角形符合「{prop}」條件，則它們的關係為何？",
            "variables": {},
            "answer_formula": "'必全等'",
            "fixed_options": ["必全等", "不一定全等", "面積相等但形狀不同", "無法判斷"],
            "explanation": f"{prop} 是全等判別性質之一。",
            "svg": "geometry_sas"
        })
        
        a, b = random.randint(20, 80), random.randint(20, 80)
        database["3-1 證明與推理"].append({
            "question_text": f"三角形 ABC 中，∠A={a}°，∠B={b}°，求 ∠C 的外角？",
            "variables": {},
            "answer_formula": str(a + b),
            "wrong_formulas": [str(180 - (a + b)), "180", "90"],
            "explanation": f"外角 = {a} + {b} = {a+b}。",
            "svg": "none"
        })

    # --- 3-2 三心 (生成 200 題) ---
    for _ in range(200):
        m = random.randint(6, 30) * 3
        database["3-2 三角形的外心、內心與重心"].append({
            "question_text": f"若中線 AD 長為 {m}，G 為重心，求 AG 的長度？",
            "variables": {},
            "answer_formula": str(int(m * 2 / 3)),
            "wrong_formulas": [str(int(m / 2)), str(int(m / 3)), str(m)],
            "explanation": f"重心性質：頂點到重心 = 2/3 中線 = {int(m*2/3)}。",
            "svg": "triangle_centroid",
            "params_override": {"m": m}
        })
        
        deg = random.choice([40, 50, 60, 70, 80])
        database["3-2 三角形的外心、內心與重心"].append({
            "question_text": f"I 為內心，若 ∠A = {deg}°，求 ∠BIC？",
            "variables": {},
            "answer_formula": str(90 + deg // 2),
            "wrong_formulas": [str(180 - deg), str(90 + deg), str(2 * deg)],
            "explanation": f"內心角度公式：90 + A/2 = 90 + {deg//2} = {90 + deg//2}。",
            "svg": "triangle_incenter",
            "params_override": {"a": deg}
        })

    # --- 4-1 因式分解 (生成 200 題) ---
    for _ in range(200):
        r1, r2 = random.randint(1, 9), random.randint(-9, -1)
        database["4-1 因式分解法"].append({
            "question_text": f"解方程式 (x - {r1})(x - {r2}) = 0？",
            "variables": {},
            "answer_formula": f"'{r1} 或 {r2}'",
            "fixed_options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
            "explanation": f"令括號為 0，x={r1} 或 x={r2}。",
            "svg": "roots_line",
            "params_override": {"r1": r1, "r2": r2}
        })
        
        k = random.randint(2, 9)
        database["4-1 因式分解法"].append({
            "question_text": f"解方程式 x² - {k}x = 0？",
            "variables": {},
            "answer_formula": f"'0 或 {k}'",
            "fixed_options": [f"0 或 {k}", f"{k}", "0", f"1 或 {k}"],
            "explanation": f"提 x：x(x-{k})=0。",
            "svg": "roots_0_k",
            "params_override": {"k": k}
        })

    # --- 4-2 配方法 (生成 200 題) ---
    for _ in range(200):
        b = random.choice([2, 4, 6, 8])
        c = random.randint(1, 3)
        ans_D = b*b - 4*c
        database["4-2 配方法與公式解"].append({
            "question_text": f"求 x² + {b}x + {c} = 0 的判別式 D？",
            "variables": {},
            "answer_formula": str(ans_D),
            "wrong_formulas": [str(ans_D + 4), str(ans_D - 4), "0"],
            "explanation": f"D = b² - 4ac = {b*b} - 4 = {ans_D}。",
            "svg": "none"
        })
        
        k = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
        ans_sq = (k // 2) ** 2
        database["4-2 配方法與公式解"].append({
            "question_text": f"將 x² + {k}x 配成完全平方式，需加上？",
            "variables": {},
            "answer_formula": str(ans_sq),
            "wrong_formulas": [str(k), str(k * 2), "1"],
            "explanation": f"加上 (一半)² = ({k}/2)² = {ans_sq}。",
            "svg": "area_square_k",
            "params_override": {"k": k}
        })

    # --- 4-3 應用問題 (生成 200 題) ---
    for _ in range(200):
        s = random.randint(5, 20)
        area = s * s
        database["4-3 應用問題"].append({
            "question_text": f"某正方形農地面積為 {area} 平方公尺，求邊長？",
            "variables": {},
            "answer_formula": str(s),
            "wrong_formulas": [str(s * 2), str(area), str(s + 5)],
            "explanation": f"邊長 = √{area} = {s}。",
            "svg": "area_square",
            "params_override": {"s": s}
        })
        
        t = random.randint(2, 8)
        h = 5 * t * t
        database["4-3 應用問題"].append({
            "question_text": f"物體落下距離公式 h=5t²。若落下 {h} 公尺，需時幾秒？",
            "variables": {},
            "answer_formula": str(t),
            "wrong_formulas": [str(t * 2), str(t + 2), "10"],
            "explanation": f"{h} = 5t² → t²={t * t} → t={t}。",
            "svg": "none"
        })

    return database

# ==========================================
# 2. 視覺繪圖引擎 (SVG)
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
# 3. 考卷生成邏輯
# ==========================================
def generate_question_from_template(template):
    # 複製變數以防污染
    variables = template.get("variables", {}).copy()
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
# 4. APP 介面 (全自動雲端版)
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (雲端自動生成版)")

# 初始化狀態
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False
if 'exam_results' not in st.session_state: st.session_state.exam_results = []
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'quiz' not in st.session_state: st.session_state.quiz = []

# 【核心步驟】程式啟動時，直接在雲端生成 1000+ 題
with st.spinner('正在雲端生成 1000+ 題庫中，請稍候...'):
    data = create_cloud_database()

st.sidebar.success(f"✅ 雲端連線成功！\n已加載 {sum(len(v) for v in data.values())} 道題目。")

# 選擇單元
unit_options = list(data.keys()) + ["全範圍總複習"]
unit = st.sidebar.selectbox("請選擇練習單元", unit_options)

# 生成按鈕
if not st.session_state.exam_finished:
    if st.button("🚀 生成試卷 (10題)", use_container_width=True):
        all_questions = []
        for key in data: all_questions.extend(data[key])
        
        target_pool = all_questions if unit == "全範圍總複習" else data[unit]
        
        # 隨機抽取
        selected_templates = random.choices(target_pool, k=10)
        
        questions = []
        for tmpl in selected_templates:
            questions.append(generate_question_from_template(tmpl))
        
        st.session_state.quiz = questions
        st.session_state.exam_finished = False
        st.rerun()

# 顯示考卷
if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("exam_form"):
        user_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**第 {i+1} 題：**")
            if q['svg']: st.markdown(q['svg'], unsafe_allow_html=True)
            st.markdown(f"### {q['q']}")
            ans = st.radio(f"選項", q['options'], key=f"ans_{i}", label_visibility="collapsed")
            st.divider()
            user_answers.append(ans)
            
        if st.form_submit_button("✅ 交卷", use_container_width=True):
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

# 顯示結果
if st.session_state.exam_finished:
    final_score = st.session_state.quiz_score
    if final_score == 100: st.success(f"## 💯 總分：{final_score} 分 (太神啦！)")
    elif final_score >= 60: st.info(f"## 😃 總分：{final_score} 分 (及格囉)")
    else: st.error(f"## 💪 總分：{final_score} 分 (再接再厲)")
    
    for i, item in enumerate(st.session_state.exam_results):
        q = item['q']
        is_right = item['correct']
        status = "✅ 正確" if is_right else "❌ 錯誤"
        
        with st.expander(f"第 {i+1} 題解析 ({status})"):
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
