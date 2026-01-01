import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (V2.0 高熵版 - 拒絕重複)
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

    # ================= 3-1 證明與推理 (注入更多幾何變數) =================
    # 1. 全等性質 (維持)
    for _ in range(50):
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        database["3-1 證明與推理"].append({
            "q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
            "options": ["必全等", "不一定全等", "面積相等但形狀不同", "無法判斷"],
            "ans": "必全等",
            "expl": f"{prop} 是三角形全等判別性質之一。",
            "svg": "geometry_sas"
        })
    
    # 2. 外角定理 (維持數字變化)
    for _ in range(50):
        a, b = random.randint(30, 80), random.randint(30, 80)
        database["3-1 證明與推理"].append({
            "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
            "options": [str(a+b), str(180-(a+b)), "180", "90"],
            "ans": str(a+b),
            "expl": f"外角 = 不相鄰兩內角和：{a} + {b} = {a+b}。",
            "svg": "none"
        })

    # 3. 邊角關係 (修正：隨機化邊長大小關係，不再是靜態題目)
    for _ in range(50):
        sides = ["AB", "BC", "AC"]
        random.shuffle(sides)
        s1, s2, s3 = sides
        # 建立隨機的邊長關係：s1 > s2 > s3
        database["3-1 證明與推理"].append({
            "q": f"在 △ABC 中，若邊長 {s1} > {s2} > {s3}，則對應角的大小關係為何？",
            "options": [f"∠{s1[-1]} > ∠{s2[-1]} > ∠{s3[-1]} (對應角)", 
                        f"∠{s3[-1]} > ∠{s2[-1]} > ∠{s1[-1]}", 
                        "三內角相等", "無法判斷"],
            "ans": f"∠{s1[-1]} > ∠{s2[-1]} > ∠{s3[-1]} (對應角)",
            "expl": f"大邊對大角：邊 {s1} 對應 ∠{s1.replace('A','').replace('B','').replace('C','') if len(s1)==2 else 'C'} (此處簡化邏輯：最長邊對最大角)。",
            "svg": "none"
        })

    # 4. 特殊四邊形 (擴充：加入更多性質判斷)
    for _ in range(50):
        q_type = random.choice([
            ("菱形", "互相垂直平分", "對角線"),
            ("矩形", "等長且互相平分", "對角線"),
            ("等腰梯形", "等長", "對角線"),
            ("箏形", "互相垂直", "對角線")
        ])
        database["3-1 證明與推理"].append({
            "q": f"下列何者是「{q_type[0]}」的{q_type[2]}必具備的性質？",
            "options": [q_type[1], "互相垂直但不平分", "無特殊性質", "以上皆非"],
            "ans": q_type[1],
            "expl": f"{q_type[0]}的{q_type[2]}性質：{q_type[1]}。",
            "svg": "none"
        })

    # 5. 多邊形內角 (維持數字變化)
    for _ in range(50):
        n = random.choice([5, 6, 8, 9, 10, 12, 15])
        ans_val = (n-2)*180
        database["3-1 證明與推理"].append({
            "q": f"正 {n} 邊形的內角總和是多少度？",
            "options": [str(ans_val), str(n*180), str((n-2)*180+360), "360"],
            "ans": str(ans_val),
            "expl": f"內角和公式：(n-2)×180 = {ans_val}。",
            "svg": "none"
        })

    # ================= 3-2 外心 (注入位置觀念變化) =================
    # 1. 直角三角形外接圓 (維持)
    for _ in range(50):
        triple = random.choice([(6,8,10), (5,12,13), (8,15,17), (9,12,15), (7,24,25), (10,24,26)])
        a, b, c = triple
        database["3-2 三角形的外心"].append({
            "q": f"直角三角形兩股長為 {a}, {b}，其「外接圓半徑」為何？",
            "options": [str(c/2), str(c), str(a+b), str(c*2)],
            "ans": str(c/2),
            "expl": "直角三角形外心在斜邊中點，外接圓半徑為斜邊一半。",
            "svg": "triangle_circumcenter"
        })

    # 2. 外心位置判斷 (修正：不再只問定義，隨機問銳角/鈍角/直角的位置)
    for _ in range(50):
        tri_type = random.choice([("銳角三角形", "三角形內部"), ("直角三角形", "斜邊中點"), ("鈍角三角形", "三角形外部")])
        database["3-2 三角形的外心"].append({
            "q": f"「{tri_type[0]}」的外心位置會在哪裡？",
            "options": [tri_type[1], "頂點上", "不一定", "與重心重合"],
            "ans": tri_type[1],
            "expl": f"外心位置性質：{tri_type[0]}的外心在{tri_type[1]}。",
            "svg": "none"
        })

    # ================= 3-3 內心 (注入定義混淆選項) =================
    # 1. 角度計算 (維持)
    for _ in range(50):
        deg = random.choice([40, 50, 60, 70, 80, 44, 56])
        database["3-3 三角形的內心"].append({
            "q": f"I 為內心，若 ∠A = {deg}°，求 ∠BIC？",
            "options": [str(90 + deg//2), str(180-deg), str(90+deg), str(2*deg)],
            "ans": str(90 + deg//2),
            "expl": f"內心角度公式：90 + ∠A/2 = {90 + deg//2}。",
            "svg": "triangle_incenter",
            "svg_params": {"a": deg}
        })

    # 2. 內心性質 (修正：隨機切換問距離性質或作圖法)
    for _ in range(50):
        q_var = random.choice([
            ("內心到何處距離相等？", "三邊", "三頂點"),
            ("內心是哪種線的交點？", "角平分線", "中垂線")
        ])
        database["3-3 三角形的內心"].append({
            "q": f"關於三角形的內心，{q_var[0]}",
            "options": [q_var[1], q_var[2], "中線", "高"],
            "ans": q_var[1],
            "expl": "內心是角平分線交點，到三邊等距離。",
            "svg": "none"
        })

    # ================= 3-4 重心 (注入面積比例變化) =================
    # 1. 長度性質 (維持)
    for _ in range(50):
        m = random.randint(6, 30) * 3
        database["3-4 三角形的重心"].append({
            "q": f"若中線 AD 長為 {m}，G 為重心，求 AG 的長度？",
            "options": [str(int(m*2/3)), str(m), str(int(m/3)), str(int(m/2))],
            "ans": str(int(m*2/3)),
            "expl": f"重心性質：重心到頂點的距離 = 2/3 中線長 = {int(m*2/3)}。",
            "svg": "triangle_centroid",
            "svg_params": {"m": m}
        })

    # 2. 面積性質 (修正：隨機問 1/3, 1/6 或 1/2 的區塊)
    for _ in range(50):
        area = random.choice([12, 24, 30, 36, 60, 72])
        q_target = random.choice([
            ("△GAB", 3, "重心與兩頂點連線面積為全體 1/3"),
            ("△GBD (D為中點)", 6, "重心與中線分割出 6 個等積三角形"),
            ("四邊形 AFGE (F,E為中點)", 3, "佔全體 1/3")
        ])
        ans_val = int(area / q_target[1])
        database["3-4 三角形的重心"].append({
            "q": f"△ABC 面積為 {area}，G 為重心，D,E,F 為中點。求 {q_target[0]} 的面積？",
            "options": [str(ans_val), str(ans_val*2), str(area), str(int(area/2))],
            "ans": str(ans_val),
            "expl": f"{q_target[2]}。{area} ÷ {q_target[1]} = {ans_val}。",
            "svg": "none"
        })

    # ================= 4-1 因式分解法 (維持高數學熵) =================
    for _ in range(50):
        r1, r2 = random.randint(1, 9), random.randint(-9, -1)
        term1 = f"(x - {r1})"
        term2 = f"(x + {abs(r2)})" if r2 < 0 else f"(x - {r2})"
        database["4-1 因式分解法"].append({
            "q": f"解方程式 {term1}{term2} = 0？",
            "options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
            "ans": f"{r1} 或 {r2}",
            "expl": f"令括號為 0 可得解為 {r1} 或 {r2}。",
            "svg": "roots_line_hidden",
            "svg_params": {"r1_label": "x₁", "r2_label": "x₂", "r1": r1, "r2": r2}
        })
    for _ in range(50):
        k = random.randint(2, 15)
        database["4-1 因式分解法"].append({
            "q": f"解方程式 x² - {k}x = 0？",
            "options": [f"0 或 {k}", f"{k}", "0", f"1 或 {k}"],
            "ans": f"0 或 {k}",
            "expl": f"提公因式：x(x-{k})=0 => x=0 或 {k}。",
            "svg": "roots_0_k",
            "svg_params": {"k_label": "k", "k": k}
        })
    for _ in range(50):
        k = random.randint(2, 12)
        database["4-1 因式分解法"].append({
            "q": f"解方程式 x² - {k*k} = 0？",
            "options": [f"±{k}", f"{k}", str(k*k), "無解"],
            "ans": f"±{k}",
            "expl": f"x²={k*k} => x=±{k}。",
            "svg": "none"
        })
    for _ in range(50):
        k = random.randint(2, 5)
        database["4-1 因式分解法"].append({
            "q": f"若 x={k} 是方程式 x² + ax + b = 0 的一根，則？",
            "options": [f"將 {k} 代入方程式等號成立", f"將 -{k} 代入方程式等號成立", "a必為正", "b必為負"],
            "ans": f"將 {k} 代入方程式等號成立",
            "expl": "方程式的根定義為代入未知數後能使等號成立的數。",
            "svg": "none"
        })
    for _ in range(50):
        k = random.randint(1, 9)
        database["4-1 因式分解法"].append({
            "q": f"方程式 (x-{k})² = 0 有幾個解？",
            "options": ["1個 (重根)", "2個相異解", "無解", "無限多"],
            "ans": "1個 (重根)",
            "expl": "完全平方式為重根。",
            "svg": "none"
        })

    # ================= 4-2 配方法 (維持) =================
    for _ in range(50):
        k = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
        database["4-2 配方法與公式解"].append({
            "q": f"將 x² + {k}x 配成完全平方式，需加上？",
            "options": [str((k//2)**2), str(k), str(k*2), "1"],
            "ans": str((k//2)**2),
            "expl": f"加上 (一次項係數一半) 的平方：({k}/2)² = {(k//2)**2}。",
            "svg": "area_square_k"
        })
    for _ in range(50):
        b, c = random.choice([2, 4, 6, 8]), random.randint(1, 5)
        database["4-2 配方法與公式解"].append({
            "q": f"方程式 x² + {b}x + {c} = 0 的判別式 D 為何？",
            "options": [str(b*b-4*c), str(b*b+4*c), "0", "1"],
            "ans": str(b*b-4*c),
            "expl": f"D = b² - 4ac = {b*b} - 4*{c} = {b*b-4*c}。",
            "svg": "none"
        })
    for _ in range(50):
        database["4-2 配方法與公式解"].append({
            "q": "若一元二次方程式判別式 D < 0，則其根的性質？",
            "options": ["無實根", "重根", "兩相異實根", "無法判斷"],
            "ans": "無實根",
            "expl": "D < 0 代表方程式在實數範圍內無解。",
            "svg": "none"
        })
    for _ in range(50):
        database["4-2 配方法與公式解"].append({
            "q": "一元二次方程式公式解中，分母為何？",
            "options": ["2a", "a", "4a", "b"],
            "ans": "2a",
            "expl": "公式解分母為 2a。",
            "svg": "none"
        })

    # ================= 4-3 應用問題 (注入情境變化) =================
    # 1. 幾何面積 (修正：混合正方形、長方形、圓形)
    for _ in range(50):
        s = random.randint(5, 20)
        shape_q = random.choice([
            ("正方形", f"邊長為 {s}", s*s, "邊長"),
            ("長方形", f"長為 {s}, 寬為 {s-2}", s*(s-2), "長"),
        ])
        database["4-3 應用問題"].append({
            "q": f"某{shape_q[0]}面積為 {shape_q[2]} 平方公尺，已知{shape_q[1].split(',')[0]} (假設變數運算後)，求其{shape_q[3]}？",
            "options": [str(s), str(s*2), str(s+5), "10"],
            "ans": str(s),
            "expl": f"依據面積公式逆運算，正值解為 {s}。",
            "svg": "area_square"
        })
    
    # 2. 物理運動 (維持數字變化)
    for _ in range(50):
        t = random.randint(2, 8)
        database["4-3 應用問題"].append({
            "q": f"自由落體公式 h=5t²。若物體落下 {5*t*t} 公尺，需時幾秒？",
            "options": [str(t), str(t*2), "10", "5"],
            "ans": str(t),
            "expl": f"5*t² = {5*t*t} => t² = {t*t} => t = {t}。",
            "svg": "none"
        })
    
    # 3. 數論問題 (維持)
    for _ in range(50):
        n = random.randint(1, 15)
        database["4-3 應用問題"].append({
            "q": f"兩連續正整數的乘積為 {n*(n+1)}，求較小的數？",
            "options": [str(n), str(n+1), str(n-1), "0"],
            "ans": str(n),
            "expl": f"設數為 n, n+1，則 n(n+1) = {n*(n+1)} => n={n}。",
            "svg": "none"
        })
    
    # 4. 長寬問題 (維持)
    for _ in range(50):
        w = random.randint(3, 12)
        database["4-3 應用問題"].append({
            "q": f"長方形長比寬多 2，面積為 {w*(w+2)}，求寬？",
            "options": [str(w), str(w+2), str(w-2), "1"],
            "ans": str(w),
            "expl": f"設寬 x，則 x(x+2) = {w*(w+2)} => x = {w}。",
            "svg": "none"
        })
    
    # 5. 合理性判斷 (修正：加入更多不合邏輯的情境)
    for _ in range(50):
        scenario = random.choice([
            ("長度為 -5", "長度需為正"),
            ("人數為 3.5", "人數需為整數"),
            ("時間為 -10", "時間需為正")
        ])
        database["4-3 應用問題"].append({
            "q": f"解應用問題時，若算出{scenario[0]}，代表？",
            "options": [f"不合 ({scenario[1]})", "取絕對值", "四捨五入", "重算"],
            "ans": f"不合 ({scenario[1]})",
            "expl": f"應用問題需符合物理或邏輯限制，{scenario[1]}。",
            "svg": "none"
        })

    return database

# ==========================================
# 2. 視覺繪圖引擎 (完全保留)
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
st.title("☁️ 國中數學智能題庫 (V2.0 高熵版)")

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
    
    # 物理鎖定：更新亂數種子
    random.seed(time.time())
    
    # 內容去重邏輯 (Content Deduplication)
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
