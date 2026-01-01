import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (V9.0 邏輯全開 + 視覺全開版)
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

    # 參數 svg 預設為 "none"，若有圖則傳入類型字串
    def add_q(unit, cat, q, opts, ans, expl, svg="none", params={}):
        database[unit][cat].append({
            "q": q, "options": opts, "ans": ans, "expl": expl, 
            "svg": svg, "svg_params": params, "type": cat
        })

    # =================================================================
    # 單元 3-1: 證明與推理 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    # [觀念題]
    for _ in range(50):
        subtype = random.randint(1, 3)
        if subtype == 1: # 全等性質 (配圖)
            prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
            add_q("3-1 證明與推理", "concept",
                  f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
                  ["必全等", "不一定全等", "面積相等但形狀不同", "相似"],
                  "必全等", f"{prop} 是全等性質。", "geometry_sas")
        elif subtype == 2: # 陷阱題 (無圖)
            bad = random.choice(["SSA", "AAA"])
            add_q("3-1 證明與推理", "concept",
                  f"下列哪一個條件「無法」保證三角形全等？",
                  [bad, "SAS", "ASA", "SSS"],
                  bad, f"{bad} 只能確定相似(AAA)或不確定(SSA)。")
        else: # 軌跡 (無圖)
            q_text = random.choice(["中垂線上任一點到哪裡的距離相等？", "角平分線上任一點到哪裡的距離相等？"])
            ans = "線段兩端點" if "中垂線" in q_text else "角的兩邊"
            opts = ["線段兩端點", "角的兩邊", "三角形頂點", "無法判斷"]
            add_q("3-1 證明與推理", "concept", q_text, opts, ans, "幾何軌跡的基本性質。")

    # [計算題]
    for _ in range(50):
        subtype = random.randint(1, 3)
        if subtype == 1: # 角度計算 (配通用三角形圖)
            a, b = random.randint(50, 80), random.randint(20, 40)
            add_q("3-1 證明與推理", "calc",
                  f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
                  [str(a+b), str(180-a-b), "180", "90"],
                  str(a+b), "外角定理。", "general_triangle", {"angle_a": a, "angle_b": b})
        elif subtype == 2: # 多邊形內角 (配正多邊形圖)
            n = random.choice([5, 6, 8, 10])
            add_q("3-1 證明與推理", "calc",
                  f"正 {n} 邊形的內角總和是多少度？",
                  [str((n-2)*180), str(n*180), "360", "720"],
                  str((n-2)*180), "內角和公式 (n-2)×180。", "polygon_n", {"n": n})
        else: # 邊角關係 (無圖)
            s = random.randint(5, 15)
            add_q("3-1 證明與推理", "calc",
                  f"三角形兩邊長為 {s} 和 {s} (等腰)，第三邊長可能是？",
                  [str(s), str(2*s), str(2*s+1), "0"],
                  str(s), "三角形兩邊和 > 第三邊。")

    # [情境題]
    for _ in range(50):
        add_q("3-1 證明與推理", "real",
              "木工師傅想確認一塊三角形木板是否為等腰三角形，他量了兩個底角發現相等，這是利用？",
              ["等角對等邊", "大角對大邊", "內角和 180", "外角定理"],
              "等角對等邊", "兩底角相等則對邊(腰)相等。")
        
        s1, s2 = random.randint(3, 8), random.randint(3, 8)
        # 配吸管圖
        add_q("3-1 證明與推理", "real",
              f"小明有兩根長度為 {s1}, {s2} 的吸管，想剪第三根吸管圍成三角形，第三根長度 x 需滿足？",
              [f"{abs(s1-s2)} < x < {s1+s2}", f"x > {s1+s2}", f"x = {s1+s2}", "無限制"],
              f"{abs(s1-s2)} < x < {s1+s2}", "三角形兩邊和 > 第三邊。", "sticks_triangle", {"s1": s1, "s2": s2})

    # =================================================================
    # 單元 3-2: 外心 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    for _ in range(50):
        add_q("3-2 三角形的外心", "concept", "三角形的外心是哪三條線的交點？", ["中垂線", "角平分線", "中線", "高"], "中垂線", "外心定義。", "triangle_circumcenter")
        tri_type = random.choice([("鈍角", "外部"), ("直角", "斜邊中點"), ("銳角", "內部")])
        add_q("3-2 三角形的外心", "concept", f"「{tri_type[0]}三角形」的外心位置在哪裡？", [tri_type[1], "頂點", "不一定", "重心"], tri_type[1], f"{tri_type[0]}三角形外心在{tri_type[1]}。")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 直角外心 (配直角圖)
            c = random.choice([10, 13, 17, 25, 30])
            add_q("3-2 三角形的外心", "calc",
                  f"直角三角形斜邊長為 {c}，求外接圓半徑 R？",
                  [str(c/2), str(c), str(c*2), str(c/3)],
                  str(c/2), "直角三角形外心在斜邊中點。", "right_triangle_circumcenter")
        else: # 座標 (配座標圖)
            k = random.randint(2, 6) * 2
            add_q("3-2 三角形的外心", "calc",
                  f"座標平面上 A(0,{k}), B({k},0), O(0,0)，求 △ABO 外心座標？",
                  [f"({k//2},{k//2})", f"({k},{k})", "(0,0)", f"({k//3},{k//3})"],
                  f"({k//2},{k//2})", "直角三角形外心為斜邊中點。", "coord_triangle", {"k": k})

    for _ in range(50):
        add_q("3-2 三角形的外心", "real", "三村莊 A, B, C 想要蓋一座共用的水塔，要求到三村莊距離相等，應蓋在？", ["外心", "內心", "重心", "AB 線段上"], "△ABC 的外心", "外心到三頂點等距離。", "triangle_circumcenter")
        add_q("3-2 三角形的外心", "real", "圓形古蹟破裂殘缺，考古學家想找回圓心復原，應該在圓弧上取點做什麼線？", ["弦的中垂線", "切線", "角平分線", "中線"], "弦的中垂線", "圓心必在弦的中垂線上。")

    # =================================================================
    # 單元 3-3: 內心 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    for _ in range(50):
        add_q("3-3 三角形的內心", "concept", "內心到三角形哪裡的距離相等？", ["三邊", "三頂點", "三中點", "外部"], "三邊", "內心為內切圓圓心。", "triangle_incenter")
        add_q("3-3 三角形的內心", "concept", "尺規作圖找內心，需要做什麼？", ["角平分線", "中垂線", "中線", "高"], "角平分線", "內心是三內角平分線交點。")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 角度 (配內心圖)
            deg = random.choice([40, 50, 60, 70, 80])
            add_q("3-3 三角形的內心", "calc", f"I 為內心，∠A={deg}°，求 ∠BIC？", [str(90+deg//2), str(180-deg), str(90+deg), str(deg)], str(90+deg//2), "公式：90 + A/2。", "triangle_incenter", {"a": deg})
        else: # 面積 (無圖)
            s = random.randint(10, 20)
            r = random.randint(2, 5)
            area = s * r // 2
            add_q("3-3 三角形的內心", "calc", f"三角形周長 {s}，內切圓半徑 {r}，求面積？", [str(area), str(s*r), str(area*2), str(s+r)], str(area), "面積 = rs/2。")

    for _ in range(50):
        add_q("3-3 三角形的內心", "real", "想要在三角形公園內蓋一個圓形噴水池，且圓面積最大，圓心應選？", ["內心", "外心", "重心", "頂點"], "內心", "內切圓是三角形內部最大的圓。", "triangle_incenter")

    # =================================================================
    # 單元 3-4: 重心 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    for _ in range(50):
        add_q("3-4 三角形的重心", "concept", "三角形的重心是哪三條線的交點？", ["中線", "中垂線", "角平分線", "高"], "中線", "重心定義。", "triangle_centroid")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 長度 (配重心圖)
            m = random.randint(3, 9) * 3
            add_q("3-4 三角形的重心", "calc", f"G 為重心，中線 AD 長為 {m}，求 AG？", [str(m*2//3), str(m//3), str(m), str(m//2)], str(m*2//3), "重心到頂點距離為中線長的 2/3。", "triangle_centroid", {"m": m})
        else: # 面積 (無圖)
            area = random.randint(6, 12) * 6
            add_q("3-4 三角形的重心", "calc", f"△ABC 面積 {area}，G 為重心。則 △GAB 面積為？", [str(area//3), str(area//2), str(area//6), str(area)], str(area//3), "重心與頂點連線將面積三等分。")

    for _ in range(50):
        add_q("3-4 三角形的重心", "real", "童軍課製作三角形木板，想用一根手指頂住木板讓它平衡，手指要放在？", ["重心", "內心", "外心", "垂心"], "重心", "重心是物體的重量中心。", "triangle_centroid")

    # =================================================================
    # 單元 4-1: 因式分解 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    for _ in range(50):
        add_q("4-1 因式分解法", "concept", "若 (x-a)(x-b) = 0，則下列推論何者正確？", ["x=a 或 x=b", "x=a 且 x=b", "x=0", "a=b"], "x=a 或 x=b", "零積性質。")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 平方差 (配平方差圖)
            k = random.randint(2, 9)
            add_q("4-1 因式分解法", "calc", f"因式分解 x² - {k*k}？", [f"(x+{k})(x-{k})", f"(x-{k})²", f"(x+{k})²", "無法分解"], f"(x+{k})(x-{k})", "平方差公式。", "diff_squares", {"k": k})
        else: # 十字交乘 (無圖)
            a, b = random.randint(1, 5), random.randint(1, 5)
            add_q("4-1 因式分解法", "calc", f"因式分解 x² + {a+b}x + {a*b}？", [f"(x+{a})(x+{b})", f"(x-{a})(x-{b})", f"(x+{a})(x-{b})", "無解"], f"(x+{a})(x+{b})", "十字交乘法。")

    for _ in range(50):
        area = random.randint(10, 50)
        # 配面積圖
        add_q("4-1 因式分解法", "real", f"長方形面積 {area}，長寬皆為整數，請問長寬可能是？", ["需找出面積的因數", "需找出面積的倍數", "一定是正方形", "無法判斷"], "需找出面積的因數", "長 × 寬 = 面積。", "rect_area", {"area": area})

    # =================================================================
    # 單元 4-2: 配方法 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    for _ in range(50):
        # 配拋物線圖
        add_q("4-2 配方法與公式解", "concept", "一元二次方程式判別式 D < 0 代表？", ["無實根(圖形與x軸無交點)", "重根", "兩相異實根", "有三個根"], "無實根(圖形與x軸無交點)", "D < 0 圖形與 x 軸無交點。", "parabola_d_neg")

    for _ in range(50):
        k = random.choice([4, 6, 8, 10, 12])
        # 配補項圖
        add_q("4-2 配方法與公式解", "calc", f"x² + {k}x + □ 配成完全平方式，□ = ？", [str((k//2)**2), str(k), str(k*2), "1"], str((k//2)**2), "補項公式：(係數/2)²。", "area_square_k")

    for _ in range(50):
        add_q("4-2 配方法與公式解", "real", "利用公式解求出時間 t = 3 ± √(-5)，這代表什麼物理意義？", ["無解(不可能發生)", "有兩個時間點", "時間倒流", "計算錯誤"], "無解(不可能發生)", "根號內為負數代表無實數解。", "parabola_d_neg")

    # =================================================================
    # 單元 4-3: 應用問題 (邏輯 V7.4 + 視覺 V8.0)
    # =================================================================
    for _ in range(50):
        add_q("4-3 應用問題", "concept", "解應用問題算出邊長為 -5，應該如何處理？", ["不合(捨去)", "取絕對值", "當作答案", "重算"], "不合(捨去)", "幾何長度必須為正數。")

    for _ in range(50):
        n = random.randint(1, 10)
        add_q("4-3 應用問題", "calc", f"某數平方比該數大 {n*(n-1)}，求該數(正整數)？", [str(n), str(n+1), str(n-1), "0"], str(n), f"x² - x = {n*(n-1)}。")

    for _ in range(50):
        subtype = random.randint(1, 2)
        if subtype == 1: # 煙火 (配煙火圖)
            t = random.randint(2, 5)
            add_q("4-3 應用問題", "real", f"煙火發射高度 h = 20t - 5t²。在 t={t} 秒時高度為 {20*t - 5*t*t}，求 t？", [str(t), str(t+1), "0", "10"], str(t), "代入公式解方程式。", "parabola_firework")
        else: # 梯子 (配梯子圖)
            a, b, c = random.choice([(3,4,5), (5,12,13), (8,15,17)])
            add_q("4-3 應用問題", "real", f"梯子長 {c} 公尺，梯腳離牆 {a} 公尺，梯頂高度？", [str(b), str(c), str(a+b), str(c-a)], str(b), f"畢氏定理。", "ladder_wall", {"a":a, "b":b, "c":c})

    return database

# ==========================================
# 2. 視覺繪圖引擎 (V9.0 全能繪圖版)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        
        # --- V8.0 新增的通用繪圖邏輯 ---
        if svg_type == "general_triangle":
            a = kwargs.get("angle_a", 60)
            b = kwargs.get("angle_b", 60)
            return base.format(f'''
                <path d="M50,150 L250,150 L100,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/>
                <text x="90" y="40" font-size="14">A({a}°)</text>
                <text x="30" y="160" font-size="14">B({b}°)</text>
                <text x="260" y="160" font-size="14">C(?)</text>
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
                <text x="20" y="120" font-size="14">牆高?</text>
                <text x="80" y="195" font-size="14">離牆{a}</text>
                <text x="100" y="110" font-size="14" fill="brown">梯長{c}</text>
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
                <line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="2"/> <!-- X axis -->
                <line x1="20" y1="20" x2="20" y2="180" stroke="black" stroke-width="2"/> <!-- Y axis -->
                <path d="M20,20 L180,180 L20,180 Z" fill="none" stroke="blue"/>
                <text x="10" y="20">A(0,{k})</text>
                <text x="180" y="195">B({k},0)</text>
                <text x="5" y="195">O</text>
            ''')

        # --- V7.4 原有幾何圖形 (保留) ---
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
st.title("☁️ 國中數學智能題庫 (V9.0 終極融合版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

data = create_cloud_database()
st.sidebar.success(f"✅ 題庫生成完畢！(邏輯+視覺全開)")

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
