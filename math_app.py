import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：數學智慧引擎 (V11.0 神級完全體)
# ==========================================
class MathEngine:
    """
    負責生成多樣化題幹與智慧誘答，確保題目不重複且具備教學意義。
    """
    @staticmethod
    def get_template(key, **kwargs):
        templates = {
            # 3-1 證明
            "sas_concept": [
                "若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
                "已知兩三角形有「{prop}」的條件，下列敘述何者正確？",
                "幾何老師說兩個三角形符合「{prop}」，這代表什麼？"
            ],
            "angle_calc": [
                "△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
                "已知三角形兩內角為 {a}° 與 {b}°，求第三個角的外角？",
                "計算：180° - ({a}° + {b}° ) 的補角是多少？"
            ],
            # 3-2 外心
            "circum_def": [
                "哪一個心到「三頂點」等距離？",
                "三角形的外接圓圓心稱為什麼？",
                "想要蓋一個到三個村莊距離都相等的水塔，要找什麼心？"
            ],
            # 4-2 配方法
            "discriminant": [
                "一元二次方程式判別式 D < 0，代表圖形與 x 軸的關係？",
                "若 b² - 4ac < 0，則二次函數圖形為何？",
                "計算出判別式為負數，表示方程式的根為何？"
            ]
        }
        t_list = templates.get(key, [f"題目生成模組 {key}"])
        return random.choice(t_list).format(**kwargs)

    @staticmethod
    def generate_distractors(correct_val, mode="int"):
        """ 生成 3 個「看起來很像真的」錯誤答案 (智慧誘答) """
        distractors = set()
        c = correct_val
        
        count = 0
        while len(distractors) < 3 and count < 20:
            count += 1
            if mode == "int":
                # 陷阱：加減1、兩倍、一半、正負號相反、常見計算錯誤
                trap = random.choice([c+1, c-1, c*2, int(c/2), -c, c+10, abs(c-10), 0])
                if trap != c: distractors.add(str(trap))
            elif mode == "float":
                trap = round(c + random.choice([0.5, -0.5, 1.0, -1.0, c]), 1)
                if trap != c and trap > 0: distractors.add(str(trap))
            elif mode == "coord": # 座標陷阱
                x, y = c
                traps = [(y, x), (x, -y), (-x, y), (0, 0)]
                t = random.choice(traps)
                if t != c: distractors.add(f"{t}")
                
        return list(distractors)

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
        random.shuffle(opts)
        database[unit][cat].append({
            "q": q, "options": opts, "ans": ans, "expl": expl, 
            "svg": svg, "svg_params": params, "type": cat
        })

    # =================================================================
    # 單元 3-1: 證明與推理 (完整保留)
    # =================================================================
    for _ in range(50):
        # 觀念：全等性質 (動態模板)
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        q_text = MathEngine.get_template("sas_concept", prop=prop)
        add_q("3-1 證明與推理", "concept", q_text, ["必全等", "不一定全等", "面積相等但形狀不同", "相似"], "必全等", "全等性質。", "geometry_sas")
        
        # 觀念：陷阱題 (補回 V9.0)
        bad = random.choice(["SSA", "AAA"])
        add_q("3-1 證明與推理", "concept", f"下列何者「無法」保證全等？", [bad, "SAS", "ASA", "SSS"], bad, f"{bad} 僅能確定相似或不確定。")

    for _ in range(50):
        # 計算：角度 (動態模板 + 智慧誘答)
        a, b = random.randint(50, 80), random.randint(20, 40)
        ans_val = a + b
        opts = MathEngine.generate_distractors(ans_val) + [str(ans_val)]
        q_text = MathEngine.get_template("angle_calc", a=a, b=b)
        add_q("3-1 證明與推理", "calc", q_text, opts, str(ans_val), "外角定理。", "general_triangle", {"angle_a": a, "angle_b": b})
        
        # 計算：多邊形內角 (補回 V9.0)
        n = random.choice([5, 6, 8, 10])
        ans = (n-2)*180
        opts = [str(ans), str(n*180), "360", "720"]
        add_q("3-1 證明與推理", "calc", f"正 {n} 邊形內角和？", opts, str(ans), "公式 (n-2)180。", "polygon_n", {"n": n})

    for _ in range(50):
        # 情境：吸管 (邏輯判斷)
        s1, s2 = random.randint(3, 8), random.randint(3, 8)
        min_x, max_x = abs(s1 - s2), s1 + s2
        opts = [f"{min_x} < x < {max_x}", f"x > {max_x}", f"x < {min_x}", "無限制"]
        add_q("3-1 證明與推理", "real", f"兩吸管長 {s1}, {s2}，第三邊 x 範圍？", opts, f"{min_x} < x < {max_x}", "兩邊差 < 第三邊 < 兩邊和。", "sticks_triangle", {"s1": s1, "s2": s2})

    # =================================================================
    # 單元 3-2: 外心 (完整保留 + 逆向)
    # =================================================================
    for _ in range(50):
        # 觀念：定義 (動態模板)
        q_text = MathEngine.get_template("circum_def")
        add_q("3-2 三角形的外心", "concept", q_text, ["外心", "內心", "重心", "垂心"], "外心", "外心性質。", "triangle_circumcenter")
        
        # 觀念：位置 (補回 V9.0)
        tri_type = random.choice([("鈍角", "外部"), ("直角", "斜邊中點"), ("銳角", "內部")])
        add_q("3-2 三角形的外心", "concept", f"{tri_type[0]}三角形外心在哪？", [tri_type[1], "頂點", "重心", "不一定"], tri_type[1], "外心位置性質。")

    for _ in range(50):
        # 計算：直角外接圓 (正向/逆向混合)
        c = random.choice([10, 20, 26, 30])
        if random.random() > 0.5:
            ans = str(c//2)
            opts = MathEngine.generate_distractors(c//2) + [ans]
            add_q("3-2 三角形的外心", "calc", f"直角三角形斜邊 {c}，外接圓半徑？", opts, ans, "斜邊的一半。", "right_triangle_circumcenter")
        else:
            r = c // 2
            ans = str(c)
            opts = MathEngine.generate_distractors(c) + [ans]
            add_q("3-2 三角形的外心", "calc", f"直角三角形外接圓半徑 {r}，斜邊長？", opts, ans, "半徑的兩倍。", "right_triangle_circumcenter")

        # 計算：座標 (補回 V9.0)
        k = random.randint(2, 6) * 2
        add_q("3-2 三角形的外心", "calc", f"A(0,{k}), B({k},0), O(0,0) 外心？", [f"({k//2},{k//2})", f"({k},{k})", "(0,0)", f"({k//3},{k//3})"], f"({k//2},{k//2})", "斜邊中點公式。", "coord_triangle", {"k": k})

    for _ in range(50):
        add_q("3-2 三角形的外心", "real", "三村莊蓋共用水塔(等距)，選哪裡？", ["外心", "內心", "重心", "中點"], "外心", "外心到頂點等距。", "triangle_circumcenter")

    # =================================================================
    # 單元 3-3: 內心 (完整保留)
    # =================================================================
    for _ in range(50):
        # 觀念
        add_q("3-3 三角形的內心", "concept", "內心到哪裡距離相等？", ["三邊", "三頂點", "外部", "中點"], "三邊", "內切圓性質。", "triangle_incenter")
        add_q("3-3 三角形的內心", "concept", "找內心要做什麼線？", ["角平分線", "中垂線", "中線", "高"], "角平分線", "內心定義。")

    for _ in range(50):
        # 計算：角度 (公式變化)
        deg = random.choice([40, 60, 80])
        ans = 90 + deg // 2
        opts = MathEngine.generate_distractors(ans) + [str(ans)]
        add_q("3-3 三角形的內心", "calc", f"I 為內心，∠A={deg}°，求 ∠BIC？", opts, str(ans), "90 + A/2。", "triangle_incenter", {"a": deg})
        
        # 計算：面積 (補回 V9.0)
        s, r = random.randint(10, 20), random.randint(2, 5)
        area = s * r // 2
        opts = MathEngine.generate_distractors(area) + [str(area)]
        add_q("3-3 三角形的內心", "calc", f"周長 {s}，內切圓半徑 {r}，求面積？", opts, str(area), "rs/2。")

    for _ in range(50):
        add_q("3-3 三角形的內心", "real", "三角形公園蓋最大圓形噴水池，圓心？", ["內心", "外心", "重心", "頂點"], "內心", "內切圓最大。", "triangle_incenter")

    # =================================================================
    # 單元 3-4: 重心 (完整保留)
    # =================================================================
    for _ in range(50):
        add_q("3-4 三角形的重心", "concept", "重心是哪三條線交點？", ["中線", "中垂線", "角平分線", "高"], "中線", "重心定義。", "triangle_centroid")

    for _ in range(50):
        # 計算：長度比例
        m = random.randint(3, 9) * 3
        ans = m * 2 // 3
        opts = MathEngine.generate_distractors(ans) + [str(ans)]
        add_q("3-4 三角形的重心", "calc", f"G 為重心，中線 AD 長 {m}，求 AG？", opts, str(ans), "重心分中線 2:1。", "triangle_centroid", {"m": m})
        
        # 計算：面積 (補回 V9.0)
        area = random.randint(6, 12) * 6
        add_q("3-4 三角形的重心", "calc", f"△ABC 面積 {area}，G 為重心，求 △GAB 面積？", [str(area//3), str(area//2), str(area), str(area//6)], str(area//3), "重心三等分面積。")

    for _ in range(50):
        add_q("3-4 三角形的重心", "real", "手指頂木板平衡，要頂在哪？", ["重心", "內心", "外心", "垂心"], "重心", "物理平衡點。", "triangle_centroid")

    # =================================================================
    # 單元 4-1: 因式分解 (完整保留)
    # =================================================================
    for _ in range(50):
        add_q("4-1 因式分解法", "concept", "若 (x-a)(x-b)=0，則？", ["x=a 或 x=b", "x=a 且 x=b", "x=0", "無解"], "x=a 或 x=b", "零積性質。")

    for _ in range(50):
        # 計算：平方差
        k = random.randint(2, 9)
        ans = f"(x+{k})(x-{k})"
        opts = [ans, f"(x-{k})²", f"(x+{k})²", f"x(x-{k})"]
        add_q("4-1 因式分解法", "calc", f"分解 x² - {k*k}？", opts, ans, "平方差公式。", "diff_squares", {"k": k})
        
        # 計算：十字交乘 (補回 V9.0)
        a, b = random.randint(1, 5), random.randint(1, 5)
        ans = f"(x+{a})(x+{b})"
        opts = [ans, f"(x-{a})(x-{b})", f"(x+{a})(x-{b})", "無解"]
        add_q("4-1 因式分解法", "calc", f"分解 x² + {a+b}x + {a*b}？", opts, ans, "十字交乘法。")

    for _ in range(50):
        area = random.randint(12, 40)
        add_q("4-1 因式分解法", "real", f"長方形面積 {area}，長寬關係？", ["面積的因數", "倍數", "相等", "無關"], "面積的因數", "長x寬=面積。", "rect_area", {"area": area})

    # =================================================================
    # 單元 4-2: 配方法 (補回 V9.0 被刪減部分)
    # =================================================================
    for _ in range(50):
        # 觀念：判別式 (動態模板)
        q_text = MathEngine.get_template("discriminant")
        add_q("4-2 配方法與公式解", "concept", q_text, ["與x軸無交點", "交於一點", "交於兩點", "重合"], "與x軸無交點", "D<0 無實根。", "parabola_d_neg")

    for _ in range(50):
        # 計算：配方補項
        k = random.choice([4, 6, 8, 10])
        ans = (k//2)**2
        opts = MathEngine.generate_distractors(ans) + [str(ans)]
        add_q("4-2 配方法與公式解", "calc", f"x² + {k}x + □ 配成完全平方，□ = ？", opts, str(ans), "(係數/2)²。", "area_square_k")

    for _ in range(50):
        add_q("4-2 配方法與公式解", "real", "時間 t 算出虛數，代表？", ["無解/不可能", "有兩個時間", "時間倒流", "算錯"], "無解/不可能", "物理無意義。", "parabola_d_neg")

    # =================================================================
    # 單元 4-3: 應用問題 (完整保留)
    # =================================================================
    for _ in range(50):
        add_q("4-3 應用問題", "concept", "解幾何題邊長為負，應？", ["捨去", "取絕對值", "保留", "重算"], "捨去", "長度必正。")

    for _ in range(50):
        n = random.randint(1, 10)
        ans = n
        opts = MathEngine.generate_distractors(n) + [str(n)]
        add_q("4-3 應用問題", "calc", f"某正數平方比該數大 {n*(n-1)}，求該數？", opts, str(ans), "列式求解。")

    for _ in range(50):
        # 情境：梯子 (畢氏定理)
        a, b, c = random.choice([(3,4,5), (5,12,13), (8,15,17)])
        ans = b
        opts = MathEngine.generate_distractors(b) + [str(b)]
        add_q("4-3 應用問題", "real", f"梯子長 {c}，離牆 {a}，梯頂高？", opts, str(ans), "畢氏定理。", "ladder_wall", {"a":a, "b":b, "c":c})
        
        # 情境：煙火 (拋物線)
        t = random.randint(2, 5)
        h = 20*t - 5*t*t
        add_q("4-3 應用問題", "real", f"煙火 h=20t-5t²，t={t} 高度？", [str(h), "0", "100", "50"], str(h), "代入求解。", "parabola_firework")

    return database

# ==========================================
# 2. 視覺繪圖引擎 (V11.0 全能版)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        
        if svg_type == "general_triangle":
            a = kwargs.get("angle_a", 60)
            b = kwargs.get("angle_b", 60)
            return base.format(f'''
                <path d="M50,150 L250,150 L100,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/>
                <text x="90" y="40" font-size="14">A({a}°)</text>
                <text x="30" y="160" font-size="14">B({b}°)</text>
                <text x="260" y="160" font-size="14">C(?)</text>
            ''')
        elif svg_type == "sticks_triangle":
            s1 = kwargs.get("s1", 5)
            s2 = kwargs.get("s2", 5)
            return base.format(f'''
                <rect x="50" y="80" width="{s1*15}" height="10" fill="blue"/>
                <rect x="50" y="110" width="{s2*15}" height="10" fill="green"/>
                <text x="50" y="70" fill="blue">長度 {s1}</text>
                <text x="50" y="140" fill="green">長度 {s2}</text>
                <text x="200" y="100" fill="red">第三邊 x ?</text>
            ''')
        elif svg_type == "ladder_wall":
            a = kwargs.get("a", 3)
            b = kwargs.get("b", 4)
            c = kwargs.get("c", 5)
            return base.format(f'''
                <line x1="50" y1="20" x2="50" y2="180" stroke="black" stroke-width="4"/>
                <line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="4"/>
                <line x1="50" y1="60" x2="130" y2="180" stroke="brown" stroke-width="5"/>
                <text x="20" y="120" font-size="14">高?</text>
                <text x="80" y="195" font-size="14">底{b}</text>
                <text x="100" y="110" font-size="14" fill="brown">斜{c}</text>
            ''')
        elif svg_type == "parabola_d_neg":
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
        elif svg_type == "parabola_firework":
            return base.format('<path d="M20,180 Q150,-50 280,180" fill="none" stroke="red" stroke-width="2"/><circle cx="150" cy="40" r="5" fill="orange"/><text x="160" y="40">最高點</text>')
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
        elif svg_type == "coord_triangle":
            k = kwargs.get("k", 4)
            return base.format(f'''
                <line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="2"/>
                <line x1="20" y1="20" x2="20" y2="180" stroke="black" stroke-width="2"/>
                <path d="M20,20 L180,180 L20,180 Z" fill="none" stroke="blue"/>
                <text x="10" y="20">A(0,{k})</text>
                <text x="180" y="195">B({k},0)</text>
                <text x="5" y="195">O</text>
            ''')
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
        # 原有幾何圖形
        elif svg_type == "geometry_sas":
            return base.format('<path d="M30,120 L90,120 L60,40 Z" fill="none" stroke="black"/><path d="M160,120 L220,120 L190,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        elif svg_type == "right_triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#e0e0e0"/><path d="M90,40 L90,160 L210,160 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="100" r="5" fill="red"/><text x="160" y="95" fill="red">O</text>')
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
st.title("☁️ 國中數學智能題庫 (V11.0 神級完全體)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

data = create_cloud_database()
st.sidebar.success(f"✅ 題庫生成完畢！(邏輯無損+智慧引擎+全視覺)")

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
