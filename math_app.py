import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (V3.0 多態變異版)
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

    # ================= 3-1 證明與推理 (引入邏輯陷阱與多重題型) =================
    for _ in range(50):
        # 變異點 1: 混合全等性質與「錯誤」性質
        q_type = random.choice(["valid", "invalid", "application"])
        
        if q_type == "valid":
            prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
            database["3-1 證明與推理"].append({
                "q": f"已知兩個三角形滿足「{prop}」條件，請問它們的關係？",
                "options": ["必全等", "面積相等但不全等", "相似但不全等", "無法判斷"],
                "ans": "必全等",
                "expl": f"{prop} 是五大三角形全等性質之一。",
                "svg": "geometry_sas"
            })
        elif q_type == "invalid":
            # 專門出陷阱題：SSA, AAA
            fake_prop = random.choice(["SSA (兩邊一對角)", "AAA (三內角對應相等)"])
            database["3-1 證明與推理"].append({
                "q": f"若兩個三角形滿足「{fake_prop}」，則下列敘述何者正確？",
                "options": ["不一定全等", "必全等", "必不全等", "面積必相等"],
                "ans": "不一定全等",
                "expl": f"{fake_prop} 不是全等性質。AAA 只能證明相似；SSA 可能形成兩種不同三角形。",
                "svg": "none"
            })
        else:
            # 應用題：中垂線性質
            database["3-1 證明與推理"].append({
                "q": "若 P 點在線段 AB 的垂直平分線上，則下列何者必成立？",
                "options": ["PA = PB", "PA > PB", "PA < PB", "PA ⊥ PB"],
                "ans": "PA = PB",
                "expl": "中垂線性值：線上任一點到線段兩端點等距離。",
                "svg": "none"
            })

    for _ in range(50):
        # 變異點 2: 幾何不等式 (邊角關係逆轉)
        mode = random.choice(["angle_to_side", "side_to_angle", "triangle_inequality"])
        
        if mode == "angle_to_side":
            database["3-1 證明與推理"].append({
                "q": "△ABC 中，∠A=80°, ∠B=60°, ∠C=40°，求最長邊？",
                "options": ["BC", "AC", "AB", "無法判斷"],
                "ans": "BC",
                "expl": "大角對大邊：∠A 最大，故其對邊 BC 最長。",
                "svg": "none"
            })
        elif mode == "side_to_angle":
            database["3-1 證明與推理"].append({
                "q": "△ABC 中，AB=5, BC=8, AC=6，求最小角？",
                "options": ["∠C", "∠A", "∠B", "無法判斷"],
                "ans": "∠C",
                "expl": "小邊對小角：AB=5 最短，故對角 ∠C 最小。",
                "svg": "none"
            })
        else:
            # 三角形三邊不等式
            s1, s2 = random.randint(3,10), random.randint(3,10)
            database["3-1 證明與推理"].append({
                "q": f"三角形兩邊長為 {s1}, {s2}，則第三邊 x 的範圍？",
                "options": [f"{abs(s1-s2)} < x < {s1+s2}", f"x > {s1+s2}", f"x < {abs(s1-s2)}", f"x = {s1+s2}"],
                "ans": f"{abs(s1-s2)} < x < {s1+s2}",
                "expl": "三角形任兩邊之和大於第三邊，任兩邊之差小於第三邊。",
                "svg": "none"
            })

    # ================= 3-2 外心 (引入座標與直角坐標系) =================
    for _ in range(50):
        # 變異點 3: 混合定義、座標、半徑計算
        q_cat = random.choice(["def", "coord", "radius"])
        
        if q_cat == "def":
            database["3-2 三角形的外心"].append({
                "q": "若 O 為 △ABC 外心，則 OA, OB, OC 的長度關係？",
                "options": ["OA = OB = OC", "OA > OB > OC", "OA + OB = OC", "無特定關係"],
                "ans": "OA = OB = OC",
                "expl": "外心到三頂點等距離 (即外接圓半徑)。",
                "svg": "triangle_circumcenter"
            })
        elif q_cat == "coord":
            # 座標平面上的外心
            k = random.randint(2, 6) * 2
            database["3-2 三角形的外心"].append({
                "q": f"直角坐標平面上，A(0,{k}), B({k},0), O(0,0)，求 △ABO 的外心座標？",
                "options": [f"({k//2}, {k//2})", f"({k}, {k})", "(0, 0)", f"({k//3}, {k//3})"],
                "ans": f"({k//2}, {k//2})",
                "expl": "直角三角形外心在斜邊中點。斜邊 AB 中點為 ((0+k)/2, (k+0)/2)。",
                "svg": "none"
            })
        else:
            # 鈍角三角形外心
            database["3-2 三角形的外心"].append({
                "q": "鈍角三角形的外心位於三角形的？",
                "options": ["外部", "內部", "邊上", "頂點"],
                "ans": "外部",
                "expl": "銳角在內部，直角在斜邊中點，鈍角在外部。",
                "svg": "none"
            })

    # ================= 3-3 內心 (引入面積公式與角度) =================
    for _ in range(50):
        q_cat = random.choice(["angle", "area_formula", "dist_prop"])
        
        if q_cat == "angle":
            deg = random.choice([40, 60, 80])
            database["3-3 三角形的內心"].append({
                "q": f"I 為 △ABC 內心，∠A={deg}°，求 ∠BIC？",
                "options": [str(90 + deg//2), str(180-deg), str(90+deg), str(deg//2)],
                "ans": str(90 + deg//2),
                "expl": "∠BIC = 90° + (1/2)∠A。",
                "svg": "triangle_incenter",
                "svg_params": {"a": deg}
            })
        elif q_cat == "area_formula":
            # 內切圓半徑與面積關係: Area = r * s
            r = random.randint(2, 5)
            s_perim = random.randint(10, 20) * 2 # 周長
            area = r * (s_perim // 2)
            database["3-3 三角形的內心"].append({
                "q": f"△ABC 周長為 {s_perim}，內切圓半徑為 {r}，求 △ABC 面積？",
                "options": [str(area), str(area*2), str(area//2), str(s_perim*r)],
                "ans": str(area),
                "expl": "三角形面積 = 內切圓半徑 × 周長的一半 (A = rs)。",
                "svg": "none"
            })
        else:
            database["3-3 三角形的內心"].append({
                "q": "若 I 為內心，則 I 點到哪裡的距離等於內切圓半徑？",
                "options": ["三邊", "三頂點", "三中線", "重心"],
                "ans": "三邊",
                "expl": "內心到三邊距離相等，此距離即為內切圓半徑。",
                "svg": "none"
            })

    # ================= 3-4 重心 (引入物理性質與中線計算) =================
    for _ in range(50):
        q_cat = random.choice(["length_ratio", "area_split", "coord_avg"])
        
        if q_cat == "length_ratio":
            m = random.randint(3, 10) * 3
            database["3-4 三角形的重心"].append({
                "q": f"G 為重心，若 AG = {m}，求中線 AD 全長？",
                "options": [str(int(m * 1.5)), str(m), str(m*2), str(m*3)],
                "ans": str(int(m * 1.5)),
                "expl": f"AG 佔中線的 2/3。故中線長 = {m} × (3/2) = {int(m*1.5)}。",
                "svg": "triangle_centroid",
                "svg_params": {"m": m}
            })
        elif q_cat == "area_split":
            area = random.choice([12, 24, 36])
            database["3-4 三角形的重心"].append({
                "q": f"△ABC 面積 {area}，G 為重心，則 △GBC 面積？",
                "options": [str(area//3), str(area//2), str(area//6), str(area)],
                "ans": str(area//3),
                "expl": "重心與三頂點連線，將大三角形分割為三個等面積的小三角形。",
                "svg": "none"
            })
        else:
            # 重心座標公式
            x1, x2, x3 = 0, 3, 6
            database["3-4 三角形的重心"].append({
                "q": f"A({x1},0), B({x2},6), C({x3},0)，求 △ABC 重心 G 的 x 座標？",
                "options": [str((x1+x2+x3)//3), str(x1+x2+x3), "0", "1"],
                "ans": str((x1+x2+x3)//3),
                "expl": "重心座標 = 三頂點座標相加除以 3。",
                "svg": "none"
            })

    # ================= 4-1 因式分解 (引入十字交乘與乘法公式) =================
    for _ in range(50):
        q_cat = random.choice(["common_factor", "diff_square", "cross_mult"])
        
        if q_cat == "common_factor":
            k = random.randint(2, 9)
            database["4-1 因式分解法"].append({
                "q": f"解 x² = {k}x？",
                "options": [f"0 或 {k}", f"{k}", "0", f"±{k}"],
                "ans": f"0 或 {k}",
                "expl": f"移項得 x² - {k}x = 0，提公因式 x(x-{k})=0。",
                "svg": "roots_0_k",
                "svg_params": {"k_label": "k", "k": k}
            })
        elif q_cat == "diff_square":
            k = random.randint(2, 9)
            database["4-1 因式分解法"].append({
                "q": f"解 x² - {k*k} = 0？",
                "options": [f"±{k}", f"{k}", f"{k*k}", "無解"],
                "ans": f"±{k}",
                "expl": f"平方差公式：(x+{k})(x-{k})=0。",
                "svg": "none"
            })
        else:
            # 簡單十字交乘 x^2 + (a+b)x + ab = 0
            a, b = random.randint(1,4), random.randint(1,4)
            database["4-1 因式分解法"].append({
                "q": f"因式分解 x² + {a+b}x + {a*b} = 0 的解？",
                "options": [f"{-a}, {-b}", f"{a}, {b}", f"{a}, {-b}", "無解"],
                "ans": f"{-a}, {-b}",
                "expl": f"原式 = (x+{a})(x+{b}) = 0。",
                "svg": "none"
            })

    # ================= 4-2 配方法 (引入判別式與完全平方式) =================
    for _ in range(50):
        q_cat = random.choice(["complete_square", "discriminant", "formula_concept"])
        
        if q_cat == "complete_square":
            k = random.choice([4, 6, 8, 10])
            database["4-2 配方法與公式解"].append({
                "q": f"x² - {k}x + □ 是一個完全平方式，□ = ？",
                "options": [str((k//2)**2), str(k), str(k*2), str(k**2)],
                "ans": str((k//2)**2),
                "expl": "常數項應為 (一次項係數一半) 的平方。",
                "svg": "area_square_k"
            })
        elif q_cat == "discriminant":
            database["4-2 配方法與公式解"].append({
                "q": "若一元二次方程式有「重根」，則判別式 D 的值？",
                "options": ["D = 0", "D > 0", "D < 0", "D = 1"],
                "ans": "D = 0",
                "expl": "D > 0 兩相異實根；D = 0 重根；D < 0 無實根。",
                "svg": "none"
            })
        else:
            # 公式解形式
            database["4-2 配方法與公式解"].append({
                "q": "利用公式解求 ax²+bx+c=0，其分子部分為？",
                "options": ["-b ± √D", "b ± √D", "-b ± D", "2a"],
                "ans": "-b ± √D",
                "expl": "公式解 x = (-b ± √(b²-4ac)) / 2a。",
                "svg": "none"
            })

    # ================= 4-3 應用問題 (引入多情境) =================
    for _ in range(50):
        q_cat = random.choice(["number_problem", "geometry_problem", "physics_problem"])
        
        if q_cat == "number_problem":
            n = random.randint(1, 10)
            database["4-3 應用問題"].append({
                "q": f"一個正數比其平方少 {n*(n-1)}，求此數？",
                "options": [str(n), str(n+1), str(n-1), "0"],
                "ans": str(n),
                "expl": f"設數為 x，x² - x = {n*(n-1)}，解得 x={n} (負不合)。",
                "svg": "none"
            })
        elif q_cat == "geometry_problem":
            w = random.randint(3, 8)
            database["4-3 應用問題"].append({
                "q": f"長方形長比寬多 3，面積為 {w*(w+3)}，求周長？",
                "options": [str(2*(w + w+3)), str(w*(w+3)), str(w), str(w+3)],
                "ans": str(2*(w + w+3)),
                "expl": f"寬={w}, 長={w+3}, 周長=2*(長+寬)。",
                "svg": "area_square"
            })
        else:
            # 物理拋體
            t = random.randint(2, 5)
            database["4-3 應用問題"].append({
                "q": f"一球從大樓拋下，距離公式 h = 5t² + 10t。若 h={5*t*t + 10*t}，求時間 t？",
                "options": [str(t), str(t+1), "1", "10"],
                "ans": str(t),
                "expl": "代入公式解一元二次方程式，取正根。",
                "svg": "none"
            })

    return database

# ==========================================
# 2. 視覺繪圖引擎 (保留)
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
            l1, l2 = kwargs.get('r1_label', 'x₁'), kwargs.get('r2_label', 'x₂')
            return base.format(f'<line x1="10" y1="100" x2="290" y2="100" stroke="black"/><text x="150" y="90" text-anchor="middle">0</text><circle cx="{mx(r1)}" cy="100" r="5" fill="red"/><text x="{mx(r1)}" y="130" fill="red" text-anchor="middle">{l1}</text><circle cx="{mx(r2)}" cy="100" r="5" fill="red"/><text x="{mx(r2)}" y="130" fill="red" text-anchor="middle">{l2}</text>')
        elif svg_type == "roots_0_k":
            k = kwargs.get('k', 0)
            kl = kwargs.get('k_label', 'k')
            return base.format(f'<line x1="10" y1="100" x2="290" y2="100" stroke="black"/><circle cx="{mx(0)}" cy="100" r="5" fill="red"/><circle cx="{mx(k)}" cy="100" r="5" fill="red"/><text x="{mx(k)}" y="130" fill="red">{kl}</text><text x="{mx(0)}" y="130" fill="black">0</text>')
        elif svg_type == "area_square":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#e3f2fd" stroke="black"/><text x="150" y="105" text-anchor="middle">面積</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        return ""

# ==========================================
# 3. APP 介面 (保留去重邏輯)
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (V3.0 多態變異版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

data = create_cloud_database()
st.sidebar.success(f"✅ 題庫生成完畢！共 {sum(len(v) for v in data.values())} 題。")

unit_options = list(data.keys()) + ["全範圍總複習"]
unit = st.sidebar.selectbox("請選擇練習單元", unit_options)

if st.sidebar.button("🚀 生成試卷 (10題)"):
    all_q = []
    for k in data: all_q.extend(data[k])
    target = all_q if unit == "全範圍總複習" else data[unit]
    
    random.seed(time.time())
    random.shuffle(target)
    
    unique_quiz = []
    seen_questions = set()
    
    for q in target:
        if q['q'] not in seen_questions:
            unique_quiz.append(q)
            seen_questions.add(q['q'])
        
        if len(unique_quiz) >= 10:
            break
            
    st.session_state.quiz = unique_quiz
    st.session_state.exam_finished = False
    st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1}. {q['q']}")
            if q['svg'] != "none":
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('svg_params', {}) if 'svg_params' in q else {}), unsafe_allow_html=True)
            u_ans = st.radio("選擇答案", q['options'], key=f"q_{i}", label_visibility="collapsed")
            u_answers.append(u_ans)
            st.divider()
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            st.session_state.results = u_answers
            st.session_state.exam_finished = True
            st.rerun()

if st.session_state.exam_finished:
    score = 0
    for i, q in enumerate(st.session_state.quiz):
        is_correct = st.session_state.results[i] == q['ans']
        if is_correct: score += 1
        with st.expander(f"第 {i+1} 題: {'✅ 正確' if is_correct else '❌ 錯誤'}"):
            st.write(f"題目: {q['q']}")
            st.write(f"您的答案: {st.session_state.results[i]}")
            st.write(f"正確答案: {q['ans']}")
            st.info(f"解析: {q['expl']}")
    st.success(f"## 您的最終得分: {score * 10} 分")
    if st.button("🔄 重新挑戰", use_container_width=True):
        st.session_state.quiz = []
        st.session_state.exam_finished = False
        st.rerun()
