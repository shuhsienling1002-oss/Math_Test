import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (多樣化模板)
# ==========================================
@st.cache_data
def create_cloud_database():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心": [],
        "3-3 三角形的內心": [],
        "3-4 三角形的重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # ================= 3-1 證明與推理 =================
    for _ in range(50):
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        database["3-1 證明與推理"].append({
            "q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
            "options": ["必全等", "不一定全等", "面積相等但形狀不同", "無法判斷"],
            "ans": "必全等",
            "expl": f"{prop} 是三角形全等判別性質之一。",
            "svg": "geometry_sas"
        })

    # ================= 3-2 三角形的外心 (獨立) =================
    for _ in range(50):
        triple = random.choice([(6,8,10), (5,12,13), (8,15,17), (9,12,15), (7,24,25)])
        a, b, c = triple
        r = c / 2
        database["3-2 三角形的外心"].append({
            "q": f"直角三角形兩股長為 {a}, {b}，求其「外接圓半徑」？",
            "options": [str(r), str(c), str(a+b), str(r*2)],
            "ans": str(r),
            "expl": f"直角三角形外心在斜邊中點，外接圓半徑 = 斜邊一半 ({c}/2)。",
            "svg": "triangle_circumcenter"
        })

    # ================= 3-3 三角形的內心 (獨立) =================
    for _ in range(50):
        deg = random.choice([40, 50, 60, 70, 80])
        ans_val = 90 + deg // 2
        database["3-3 三角形的內心"].append({
            "q": f"I 為 △ABC 的內心，若 ∠A = {deg}°，求 ∠BIC 的度數？",
            "options": [str(ans_val), str(180-deg), str(90+deg), str(2*deg)],
            "ans": str(ans_val),
            "expl": f"內心角度公式：90 + ∠A/2 = 90 + {deg//2} = {ans_val}。",
            "svg": "triangle_incenter",
            "svg_params": {"a": deg}
        })

    # ================= 3-4 三角形的重心 (獨立) =================
    for _ in range(50):
        m = random.randint(6, 30) * 3
        ag = int(m * 2 / 3)
        database["3-4 三角形的重心"].append({
            "q": f"若中線 AD 長為 {m}，G 為重心，求 AG 的長度？",
            "options": [str(ag), str(m), str(int(m/2)), str(int(m/3))],
            "ans": str(ag),
            "expl": f"重心性質：頂點到重心距離 = 2/3 中線長 = {ag}。",
            "svg": "triangle_centroid",
            "svg_params": {"m": m}
        })

    # ================= 4-1 因式分解法 (數線去答案化) =================
    for _ in range(50):
        r1, r2 = random.randint(1, 5), random.randint(-5, -1)
        term1 = f"(x - {r1})"
        term2 = f"(x + {abs(r2)})" if r2 < 0 else f"(x - {r2})"
        database["4-1 因式分解法"].append({
            "q": f"解方程式 {term1}{term2} = 0？",
            "options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
            "ans": f"{r1} 或 {r2}",
            "expl": f"令括號為 0，可得 x={r1} 或 x={r2}。",
            "svg": "roots_line_hidden",
            "svg_params": {"r1_label": "a", "r2_label": "b", "r1": r1, "r2": r2}
        })

    # ================= 4-2 配方法與公式解 =================
    for _ in range(50):
        k = random.choice([6, 8, 10, 12, 14, 16])
        ans_sq = (k // 2) ** 2
        database["4-2 配方法與公式解"].append({
            "q": f"將 x² + {k}x 配成完全平方式，需加上常數項？",
            "options": [str(ans_sq), str(k), str(k*2), "1"],
            "ans": str(ans_sq),
            "expl": f"加上一次項係數一半的平方：({k}/2)² = {ans_sq}。",
            "svg": "area_square_k",
            "svg_params": {"k": k}
        })

    # ================= 4-3 應用問題 =================
    for _ in range(50):
        s = random.randint(5, 20)
        area = s * s
        database["4-3 應用問題"].append({
            "q": f"某正方形面積為 {area}，求邊長？",
            "options": [str(s), str(area), str(s*2), str(s+5)],
            "ans": str(s),
            "expl": f"邊長 = √{area} = {s}。",
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
        mx = lambda v: 150 + v*12
        
        if svg_type == "geometry_sas":
            return base.format('<path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black"/><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        elif svg_type == "triangle_centroid":
            return base.format('<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="160" y="130" fill="blue">G</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="green"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="90" fill="green">O</text>')
        elif svg_type == "triangle_incenter":
            return base.format('<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange">I</text>')
        elif svg_type == "roots_line_hidden":
            r1, r2 = kwargs.get('r1', 0), kwargs.get('r2', 0)
            l1, l2 = kwargs.get('r1_label', 'a'), kwargs.get('r2_label', 'b')
            return base.format(f'<line x1="10" y1="100" x2="290" y2="100" stroke="black"/><text x="150" y="90" text-anchor="middle">0</text><circle cx="{mx(r1)}" cy="100" r="5" fill="red"/><text x="{mx(r1)}" y="130" fill="red" text-anchor="middle">{l1}</text><circle cx="{mx(r2)}" cy="100" r="5" fill="red"/><text x="{mx(r2)}" y="130" fill="red" text-anchor="middle">{l2}</text>')
        elif svg_type == "roots_0_k":
            k = kwargs.get('k', 0)
            return base.format(f'<line x1="10" y1="100" x2="290" y2="100" stroke="black"/><circle cx="{mx(0)}" cy="100" r="5" fill="red"/><circle cx="{mx(k)}" cy="100" r="5" fill="red"/><text x="{mx(k)}" y="130" fill="red">k</text><text x="{mx(0)}" y="130" fill="black">0</text>')
        elif svg_type == "area_square":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#e3f2fd" stroke="black"/><text x="150" y="105" text-anchor="middle">面積</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        return ""

# ==========================================
# 3. APP 介面邏輯 (整合計時器)
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (V25.3)")

if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False
if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'total_time' not in st.session_state: st.session_state.total_time = 0

data = create_cloud_database()

unit_options = list(data.keys()) + ["全範圍總複習"]
unit = st.sidebar.selectbox("請選擇練習單元", unit_options)

if st.sidebar.button("🚀 生成試卷"):
    all_q = []
    for k in data: all_q.extend(data[k])
    target = all_q if unit == "全範圍總複習" else data[unit]
    st.session_state.quiz = random.sample(target, min(len(target), 10))
    st.session_state.exam_finished = False
    st.session_state.start_time = time.time() # 啟動計時
    st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    # 浮動計時提醒
    elapsed = int(time.time() - st.session_state.start_time)
    st.sidebar.metric("⏳ 當前已用時", f"{elapsed} 秒")
    
    with st.form("quiz_form"):
        u_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1}. {q['q']}")
            if q['svg'] != "none":
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('svg_params', {})), unsafe_allow_html=True)
            u_ans = st.radio("選擇答案", q['options'], key=f"q_{i}", label_visibility="collapsed")
            u_answers.append(u_ans)
            st.divider()
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            st.session_state.total_time = int(time.time() - st.session_state.start_time) # 結束計時
            st.session_state.results = u_answers
            st.session_state.exam_finished = True
            st.rerun()

if st.session_state.exam_finished:
    score = 0
    st.info(f"⏱️ 本次測驗總耗時：{st.session_state.total_time} 秒")
    
    for i, q in enumerate(st.session_state.quiz):
        is_correct = st.session_state.results[i] == q['ans']
        if is_correct: score += 1
        with st.expander(f"第 {i+1} 題: {'✅ 正確' if is_correct else '❌ 錯誤'}"):
            st.write(f"題目: {q['q']}")
            st.write(f"正確答案: {q['ans']}")
            st.info(f"解析: {q['expl']}")
            
    st.success(f"## 您的總分: {score * 10} 分")
    if st.button("🔄 重新生成測驗", use_container_width=True):
        st.session_state.quiz = []
        st.session_state.exam_finished = False
        st.rerun()
