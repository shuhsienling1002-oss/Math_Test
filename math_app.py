import streamlit as st
import random
import math

# ==========================================
# 1. 核心：雲端題庫製造機 (25種模板，變數名稱嚴格對齊)
# ==========================================
@st.cache_data
def create_cloud_database():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心、內心與重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # --- 3-1 證明與推理 ---
    for _ in range(50):
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        database["3-1 證明與推理"].append({
            "q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
            "options": ["必全等", "不一定全等", "面積相等但形狀不同", "無法判斷"],
            "ans": "必全等",
            "expl": f"{prop} 是三角形全等判別性質之一。",
            "svg": "geometry_sas"
        })
    for _ in range(50):
        a, b = random.randint(30, 80), random.randint(30, 80)
        database["3-1 證明與推理"].append({
            "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
            "options": [str(a+b), str(180-(a+b)), "180", "90"],
            "ans": str(a+b),
            "expl": f"外角 = 不相鄰兩內角和：{a} + {b} = {a+b}。",
            "svg": "none"
        })
    for _ in range(50):
        shape_info = random.choice([("菱形", "互相垂直平分"), ("矩形", "等長且互相平分"), ("平行四邊形", "互相平分")])
        s_name, s_prop = shape_info
        database["3-1 證明與推理"].append({
            "q": f"下列何者是「{s_name}」對角線必具備的性質？",
            "options": [s_prop, "只有一條平分", "無特殊性質", "以上皆非"],
            "ans": s_prop,
            "expl": f"{s_name} 的對角線性質：{s_prop}。",
            "svg": "none"
        })

    # --- 3-2 三心 ---
    for _ in range(50):
        m = random.randint(6, 30) * 3
        ag = int(m * 2 / 3)
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"若中線 AD 長為 {m}，G 為重心，求 AG 的長度？",
            "options": [str(ag), str(m), str(int(m/2)), str(int(m/3))],
            "ans": str(ag),
            "expl": f"重心性質：頂點到重心 = 2/3 中線 = {ag}。",
            "svg": "triangle_centroid",
            "svg_params": {"m": m}
        })
    for _ in range(50):
        deg = random.choice([40, 50, 60, 70, 80])
        ans_val = 90 + deg // 2
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"I 為內心，若 ∠A = {deg}°，求 ∠BIC？",
            "options": [str(ans_val), str(180-deg), str(90+deg), str(2*deg)],
            "ans": str(ans_val),
            "expl": f"內心角度公式：90 + A/2 = 90 + {deg//2} = {ans_val}。",
            "svg": "triangle_incenter",
            "svg_params": {"a": deg}
        })

    # --- 4-1 因式分解 ---
    for _ in range(50):
        r1, r2 = random.randint(1, 5), random.randint(-5, -1)
        database["4-1 因式分解法"].append({
            "q": f"解方程式 (x - {r1})(x - {r2}) = 0？",
            "options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", "無解", "0"],
            "ans": f"{r1} 或 {r2}",
            "expl": f"令括號為 0，可得 x={r1} 或 x={r2}。",
            "svg": "roots_line",
            "svg_params": {"r1": r1, "r2": r2}
        })
    for _ in range(50):
        k = random.randint(2, 9)
        database["4-1 因式分解法"].append({
            "q": f"解方程式 x² - {k}x = 0？",
            "options": [f"0 或 {k}", f"{k}", "0", "1"],
            "ans": f"0 或 {k}",
            "expl": f"提 x：x(x-{k})=0，故 x=0 或 {k}。",
            "svg": "roots_0_k",
            "svg_params": {"k": k}
        })

    # --- 4-2 配方法 ---
    for _ in range(50):
        k = random.choice([6, 8, 10, 12])
        ans_sq = (k // 2) ** 2
        database["4-2 配方法與公式解"].append({
            "q": f"將 x² + {k}x 配成完全平方式，需加上？",
            "options": [str(ans_sq), str(k), str(k*2), "1"],
            "ans": str(ans_sq),
            "expl": f"加上 (一次項係數一半)² = ({k}/2)² = {ans_sq}。",
            "svg": "area_square_k",
            "svg_params": {"k": k}
        })

    # --- 4-3 應用問題 ---
    for _ in range(50):
        s = random.randint(5, 15)
        database["4-3 應用問題"].append({
            "q": f"某正方形農地面積為 {s*s} 平方公尺，求邊長？",
            "options": [str(s), str(s*s), str(s*2), "無法計算"],
            "ans": str(s),
            "expl": f"邊長 = √{s*s} = {s}。",
            "svg": "area_square",
            "svg_params": {"s": s}
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
            return base.format('<path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text><text x="115" y="80" fill="blue" font-weight="bold">全等?</text>')
        elif svg_type == "triangle_centroid":
            m = kwargs.get('m', '?')
            return base.format(f'<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="150" y="15" text-anchor="middle">A</text><text x="165" y="126" fill="blue">G</text><text x="20" y="50">AD={m}</text>')
        elif svg_type == "triangle_incenter":
            a = kwargs.get('a', '?')
            return base.format(f'<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange" text-anchor="middle">I</text><text x="20" y="50">∠A={a}°</text>')
        elif svg_type == "roots_line":
            r1, r2 = kwargs.get('r1', 0), kwargs.get('r2', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><circle cx="{mx(r1)}" cy="50" r="5" fill="red"/><circle cx="{mx(r2)}" cy="50" r="5" fill="red"/>')
        elif svg_type == "area_square":
            s = kwargs.get('s', 10)
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">Area={s*s}</text>')
        return ""

# ==========================================
# 3. 考卷生成邏輯
# ==========================================
def generate_question_from_template(template):
    # 複製變數以防污染
    svg_vars = template.get("svg_params", {}).copy()
    
    # 隨機打亂選項
    options = template["options"].copy()
    random.shuffle(options)
    
    svg_html = SVGDrawer.draw(template.get("svg", "none"), **svg_vars)
    
    return {
        "q": template["q"],
        "options": options,
        "ans": template["ans"], # 統一使用 ans 欄位
        "expl": template["expl"],
        "svg": svg_html
    }

# ==========================================
# 4. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (V25.3)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

data = create_cloud_database()

def reset_exam_state():
    st.session_state.quiz = []
    st.session_state.exam_finished = False

unit = st.sidebar.selectbox("請選擇練習單元", list(data.keys()) + ["全範圍總複習"], on_change=reset_exam_state)

if not st.session_state.exam_finished:
    if st.button("🚀 生成試卷 (10題)", use_container_width=True):
        pool = []
        if unit == "全範圍總複習":
            for k in data: pool.extend(data[k])
        else:
            pool = data[unit]
        
        # 隨機抽樣
        selected_templates = random.sample(pool, 10)
        st.session_state.quiz = [generate_question_from_template(t) for t in selected_templates]
        st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("exam_form"):
        user_ans_list = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**第 {i+1} 題：**")
            if q['svg']: st.markdown(q['svg'], unsafe_allow_html=True)
            st.markdown(f"### {q['q']}")
            user_ans_list.append(st.radio("選項", q['options'], key=f"q_{i}", label_visibility="collapsed"))
            st.divider()
        
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            score = 0
            results = []
            for i, q in enumerate(st.session_state.quiz):
                # 這裡嚴格對應 ans 欄位
                is_correct = (user_ans_list[i] == q['ans'])
                if is_correct: score += 1
                results.append({"q": q, "user": user_ans_list[i], "correct": is_correct})
            
            st.session_state.score = score * 10
            st.session_state.results = results
            st.session_state.exam_finished = True
            st.rerun()

if st.session_state.exam_finished:
    st.success(f"## 總分：{st.session_state.score} 分")
    for i, res in enumerate(st.session_state.results):
        q_obj = res['q']
        status = "✅ 正確" if res['correct'] else "❌ 錯誤"
        with st.expander(f"第 {i+1} 題解析 ({status})"):
            if q_obj['svg']: st.markdown(q_obj['svg'], unsafe_allow_html=True)
            st.write(f"**題目**：{q_obj['q']}")
            st.write(f"**正確答案**：{q_obj['ans']}")
            st.info(f"💡 解析：{q_obj['expl']}")
    
    if st.button("🔄 再來一次", use_container_width=True):
        reset_exam_state()
        st.rerun()
