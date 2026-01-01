import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (V8.0 全面視覺化版)
# ==========================================
def create_cloud_database():
    database = {
        "3-1 證明與推理": {"concept": [], "calc": [], "real": []},
        "3-2 三角形的外心": {"concept": [], "calc": [], "real": []},
        "3-3 三角形的內心": {"concept": [], "calc": [], "real": []},
        "3-4 三角形的重心": {"concept": [], "calc": [], "real": []},
        "4-1 因式分解法": {"concept": [], "calc": [], "real": []},
        "4-2 配方法與公式解": {"concept": [], "calc": [], "real": []},
        "4-3 應用問題": {"concept": [], "calc": [], "real": []}
    }

    def add_q(unit, cat, q, opts, ans, expl, svg="none", params={}):
        database[unit][cat].append({
            "q": q, "options": opts, "ans": ans, "expl": expl, 
            "svg": svg, "svg_params": params, "type": cat
        })

    # =================================================================
    # 單元 3-1: 證明與推理
    # =================================================================
    for _ in range(50):
        # 觀念：全等圖形
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        add_q("3-1 證明與推理", "concept", f"若兩三角形滿足「{prop}」，則關係為何？", ["必全等", "不一定全等", "相似", "無關"], "必全等", "全等性質。", "geometry_sas")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 三角形角度
            a, b = random.randint(50, 80), random.randint(20, 40)
            # 🔥 新增：通用三角形圖
            add_q("3-1 證明與推理", "calc", 
                  f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角？", 
                  [str(a+b), str(180-a-b), "180", "90"], str(a+b), "外角定理。", 
                  "general_triangle", {"angle_a": a, "angle_b": b})
        else: # 多邊形內角
            n = random.choice([5, 6, 8])
            # 🔥 新增：正多邊形繪圖
            add_q("3-1 證明與推理", "calc", 
                  f"正 {n} 邊形的內角總和是多少度？", 
                  [str((n-2)*180), str(n*180), "360", "720"], str((n-2)*180), "公式 (n-2)×180。", 
                  "polygon_n", {"n": n})

    for _ in range(50):
        s1, s2 = random.randint(3, 8), random.randint(3, 8)
        # 🔥 新增：線段示意圖
        add_q("3-1 證明與推理", "real", 
              f"兩根吸管長 {s1}, {s2}，第三根 x 需滿足？", 
              [f"{abs(s1-s2)} < x < {s1+s2}", f"x > {s1+s2}", "無限制", "x > 0"], 
              f"{abs(s1-s2)} < x < {s1+s2}", "三角形兩邊和大於第三邊。",
              "sticks_triangle", {"s1": s1, "s2": s2})

    # =================================================================
    # 單元 3-2: 外心
    # =================================================================
    for _ in range(50):
        add_q("3-2 三角形的外心", "concept", "外心是哪三條線的交點？", ["中垂線", "角平分線", "中線", "高"], "中垂線", "外心定義。", "triangle_circumcenter")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 直角外心
            c = random.choice([10, 13, 17, 25, 30])
            add_q("3-2 三角形的外心", "calc", f"直角三角形斜邊 {c}，外接圓半徑 R？", [str(c/2), str(c), str(c*2), str(c/3)], str(c/2), "直角三角形外心在斜邊中點。", "right_triangle_circumcenter")
        else: # 座標
            k = random.randint(2, 6) * 2
            add_q("3-2 三角形的外心", "calc", f"A(0,{k}), B({k},0), O(0,0)，求 △ABO 外心？", [f"({k//2},{k//2})", f"({k},{k})", "(0,0)", f"({k//3},{k//3})"], f"({k//2},{k//2})", "直角三角形外心為斜邊中點。", "coord_triangle", {"k": k})

    for _ in range(50):
        add_q("3-2 三角形的外心", "real", "三村莊 A, B, C 想蓋共用水塔，應蓋在？", ["外心", "內心", "重心", "AB中點"], "外心", "外心到三頂點等距。", "triangle_circumcenter")

    # =================================================================
    # 單元 3-3: 內心
    # =================================================================
    for _ in range(50):
        add_q("3-3 三角形的內心", "concept", "內心到哪裡的距離相等？", ["三邊", "三頂點", "三中點", "外部"], "三邊", "內切圓性質。", "triangle_incenter")

    for _ in range(50):
        deg = random.choice([40, 60, 80])
        add_q("3-3 三角形的內心", "calc", f"I 為內心，∠A={deg}°，求 ∠BIC？", [str(90+deg//2), str(180-deg), str(90+deg), str(deg)], str(90+deg//2), "公式：90 + A/2。", "triangle_incenter", {"a": deg})

    for _ in range(50):
        add_q("3-3 三角形的內心", "real", "公園內蓋最大圓形噴水池，圓心選？", ["內心", "外心", "重心", "頂點"], "內心", "內切圓最大。", "triangle_incenter")

    # =================================================================
    # 單元 3-4: 重心
    # =================================================================
    for _ in range(50):
        add_q("3-4 三角形的重心", "concept", "重心是哪三條線的交點？", ["中線", "中垂線", "角平分線", "高"], "中線", "重心定義。", "triangle_centroid")

    for _ in range(50):
        m = random.randint(3, 9) * 3
        add_q("3-4 三角形的重心", "calc", f"G 為重心，中線 AD 長 {m}，求 AG？", [str(m*2//3), str(m//3), str(m), str(m//2)], str(m*2//3), "重心分中線為 2:1。", "triangle_centroid", {"m": m})

    for _ in range(50):
        add_q("3-4 三角形的重心", "real", "手指頂住木板平衡，要放在？", ["重心", "內心", "外心", "垂心"], "重心", "物理平衡點。", "triangle_centroid")

    # =================================================================
    # 單元 4-1: 因式分解
    # =================================================================
    for _ in range(50):
        add_q("4-1 因式分解法", "concept", "若 ab=0，則？", ["a=0 或 b=0", "a=0 且 b=0", "a=b", "無法判斷"], "a=0 或 b=0", "零積性質。")

    for _ in range(50):
        k = random.randint(2, 9)
        # 🔥 新增：平方差面積示意圖
        add_q("4-1 因式分解法", "calc", f"因式分解 x² - {k*k}？", [f"(x+{k})(x-{k})", f"(x-{k})²", f"(x+{k})²", "無法分解"], f"(x+{k})(x-{k})", "平方差公式。", "diff_squares", {"k": k})

    for _ in range(50):
        area = random.randint(12, 40)
        # 🔥 新增：長方形面積分解圖
        add_q("4-1 因式分解法", "real", f"長方形面積 {area}，長寬為整數，長寬關係？", ["面積的因數", "面積的倍數", "必相等", "無關"], "面積的因數", "長×寬=面積。", "rect_area", {"area": area})

    # =================================================================
    # 單元 4-2: 配方法
    # =================================================================
    for _ in range(50):
        # 🔥 新增：拋物線與X軸關係圖
        add_q("4-2 配方法與公式解", "concept", "判別式 D < 0 代表圖形？", ["與x軸無交點", "與x軸切於一點", "交於兩點", "無法判斷"], "與x軸無交點", "無實根。", "parabola_d_neg")

    for _ in range(50):
        k = random.choice([4, 6, 8, 10])
        add_q("4-2 配方法與公式解", "calc", f"x² + {k}x + □ 配成完全平方，□ = ？", [str((k//2)**2), str(k), str(k*2), "1"], str((k//2)**2), "補項公式。", "area_square_k")

    for _ in range(50):
        add_q("4-2 配方法與公式解", "real", "時間 t 為虛數，代表？", ["無解(不可能發生)", "有兩個時間", "計算錯", "時間倒流"], "無解(不可能發生)", "物理無意義。", "parabola_d_neg")

    # =================================================================
    # 單元 4-3: 應用問題
    # =================================================================
    for _ in range(50):
        add_q("4-3 應用問題", "concept", "解幾何邊長為負數，應？", ["捨去", "取絕對值", "保留", "重算"], "捨去", "長度必為正。")

    for _ in range(50):
        n = random.randint(1, 10)
        add_q("4-3 應用問題", "calc", f"某正數平方比該數大 {n*(n-1)}，求該數？", [str(n), str(n+1), str(n-1), "0"], str(n), "列式求解。")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 煙火拋物線
            t = random.randint(2, 5)
            add_q("4-3 應用問題", "real", f"煙火 h=20t-5t²，t={t} 時高度？", [str(20*t-5*t*t), "0", "100", "50"], str(20*t-5*t*t), "代入求解。", "parabola_firework")
        else: # 梯子靠牆
            a, b, c = random.choice([(3,4,5), (5,12,13), (8,15,17)])
            # 🔥 新增：梯子靠牆圖
            add_q("4-3 應用問題", "real", f"梯子長 {c}，梯腳離牆 {a}，梯頂高度？", [str(b), str(c), str(a+b), str(c-a)], str(b), "畢氏定理。", "ladder_wall", {"a":a, "b":b, "c":c})

    return database

# ==========================================
# 2. 視覺繪圖引擎 (V8.0 全能繪圖版)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        
        # 1. 通用三角形 (顯示角度)
        if svg_type == "general_triangle":
            a = kwargs.get("angle_a", 60)
            b = kwargs.get("angle_b", 60)
            return base.format(f'''
                <path d="M50,150 L250,150 L100,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/>
                <text x="90" y="40" font-size="14">A({a}°)</text>
                <text x="30" y="160" font-size="14">B({b}°)</text>
                <text x="260" y="160" font-size="14">C(?)</text>
            ''')

        # 2. 正多邊形 (Polygon)
        elif svg_type == "polygon_n":
            n = kwargs.get("n", 5)
            points = []
            cx, cy, r = 150, 100, 70
            for i in range(n):
                angle = 2 * math.pi * i / n - math.pi / 2
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                points.append(f"{x},{y}")
            pts_str = " ".join(points)
            return base.format(f'<polygon points="{pts_str}" fill="#f3e5f5" stroke="purple" stroke-width="2"/><text x="130" y="105" fill="purple">正{n}邊形</text>')

        # 3. 梯子靠牆 (Ladder)
        elif svg_type == "ladder_wall":
            a = kwargs.get("a", 3)
            b = kwargs.get("b", 4)
            c = kwargs.get("c", 5)
            return base.format(f'''
                <line x1="50" y1="20" x2="50" y2="180" stroke="black" stroke-width="4"/> <!-- Wall -->
                <line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="4"/> <!-- Ground -->
                <line x1="50" y1="60" x2="130" y2="180" stroke="brown" stroke-width="5"/> <!-- Ladder -->
                <text x="20" y="120" font-size="14">牆高?</text>
                <text x="80" y="195" font-size="14">離牆{a}</text>
                <text x="100" y="110" font-size="14" fill="brown">梯長{c}</text>
            ''')

        # 4. 拋物線 (Parabola)
        elif svg_type == "parabola_d_neg": # D < 0 (懸空)
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
        
        elif svg_type == "parabola_firework": # 煙火軌跡
            return base.format('<path d="M20,180 Q150,-50 280,180" fill="none" stroke="red" stroke-width="2"/><circle cx="150" cy="40" r="5" fill="orange"/><text x="160" y="40">最高點</text>')

        # 5. 平方差/矩形
        elif svg_type == "diff_squares":
            k = kwargs.get("k", 3)
            return base.format(f'''
                <rect x="80" y="40" width="140" height="140" fill="#e8f5e9" stroke="black"/>
                <rect x="180" y="140" width="40" height="40" fill="white" stroke="red" stroke-dasharray="4"/>
                <text x="130" y="110" font-size="20">x²</text>
                <text x="190" y="165" font-size="12" fill="red">{k}²</text>
            ''')
        
        elif svg_type == "rect_area":
            area = kwargs.get("area", 24)
            return base.format(f'<rect x="50" y="50" width="200" height="100" fill="#fff9c4" stroke="orange" stroke-width="2"/><text x="120" y="105" font-size="20">面積 = {area}</text>')

        # 6. 原有幾何圖形 (保留並優化)
        elif svg_type == "geometry_sas":
            return base.format('<path d="M30,120 L90,120 L60,40 Z" fill="none" stroke="black"/><path d="M160,120 L220,120 L190,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        elif svg_type == "right_triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#e0e0e0"/><path d="M90,40 L90,160 L210,160 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="100" r="5" fill="red"/><text x="160" y="95" fill="red">O (斜邊中點)</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#b2dfdb"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="90" fill="green">O</text>')
        elif svg_type == "triangle_incenter":
            return base.format('<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><circle cx="150" cy="120" r="40" fill="none" stroke="orange"/><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange">I</text>')
        elif svg_type == "triangle_centroid":
            return base.format('<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red" stroke-dasharray="4"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="160" y="130" fill="blue">G</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        
        return ""

# ==========================================
# 3. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (V8.0 全面視覺化版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

data = create_cloud_database()
st.sidebar.success(f"✅ 題庫生成完畢！(視覺化引擎啟動)")

unit_options = list(data.keys()) + ["全範圍總複習"]
unit = st.sidebar.selectbox("請選擇練習單元", unit_options)

if st.sidebar.button("🚀 生成試卷 (1觀念+1計算+1情境)"):
    quiz_set = []
    
    if unit == "全範圍總複習":
        pool_concept = [q for k in data for q in data[k]["concept"]]
        pool_calc = [q for k in data for q in data[k]["calc"]]
        pool_real = [q for k in data for q in data[k]["real"]]
    else:
        pool_concept = data[unit]["concept"]
        pool_calc = data[unit]["calc"]
        pool_real = data[unit]["real"]
    
    random.seed(time.time())
    q1 = random.sample(pool_concept, 1) if pool_concept else []
    q2 = random.sample(pool_calc, 1) if pool_calc else []
    q3 = random.sample(pool_real, 1) if pool_real else []
    
    quiz_set = q1 + q2 + q3
    random.shuffle(quiz_set)
    
    st.session_state.quiz = quiz_set
    st.session_state.exam_finished = False
    st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        for i, q in enumerate(st.session_state.quiz):
            type_map = {"concept": "觀念", "calc": "計算", "real": "情境"}
            badge = type_map.get(q['type'], "綜合")
            
            st.markdown(f"### Q{i+1} <span style='background-color:#e0f7fa; padding:2px 8px; border-radius:4px; font-size:0.7em; color:#006064'>{badge}</span> {q['q']}", unsafe_allow_html=True)
            
            # 這裡一定會嘗試畫圖
            if q['svg'] != "none":
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('svg_params', {})), unsafe_allow_html=True)
            
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
    
    final_score = int((score / 3) * 100)
    st.success(f"## 您的最終得分: {final_score} 分")
    if st.button("🔄 重新挑戰", use_container_width=True):
        st.session_state.quiz = []
        st.session_state.exam_finished = False
        st.rerun()
