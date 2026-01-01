import streamlit as st
import random
import math
import time

# ==========================================
# 1. 數學工具箱 (無限生成核心)
# ==========================================
class MathUtils:
    @staticmethod
    def get_distractors(ans, mode="int"):
        distractors = set()
        count = 0
        if mode == "int": ans = int(ans)
        
        while len(distractors) < 3 and count < 50:
            count += 1
            if mode == "int":
                trap = random.choice([
                    ans + random.randint(1, 5), 
                    ans - random.randint(1, 5),
                    ans * 2, 
                    int(ans / 2), 
                    -ans,
                    abs(ans - 10),
                    ans + 10
                ])
                if trap != ans: distractors.add(str(trap))
            elif mode == "float":
                trap = round(ans + random.choice([0.5, -0.5, 1.0, -1.0, 2.0]), 1)
                if trap != ans and trap > 0: distractors.add(str(trap))
            elif mode == "coord": 
                try:
                    parts = ans.replace('(','').replace(')','').split(',')
                    x, y = int(parts[0]), int(parts[1])
                    traps = [(y, x), (x, -y), (-x, y), (0,0), (x+5, y+5)]
                    t = random.choice(traps)
                    t_str = f"({t[0]},{t[1]})"
                    if t_str != ans: distractors.add(t_str)
                except:
                    distractors.add("(0,0)")
        return list(distractors)

# ==========================================
# 2. 無限題庫工廠 (全單元邏輯 - 完整回歸)
# ==========================================
class QuestionFactory:
    
    # --- 3-1 證明 ---
    @staticmethod
    def gen_3_1(q_type):
        if q_type == "concept":
            if random.random() > 0.5:
                prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
                return {
                    "q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
                    "options": ["必全等", "不一定全等", "相似", "面積相等"],
                    "ans": "必全等", "expl": f"{prop} 是全等性質。",
                    "svg": "geometry_sas", "params": {}
                }
            else:
                bad = random.choice(["SSA", "AAA"])
                return {
                    "q": f"下列哪一個條件「無法」保證三角形全等？",
                    "options": [bad, "SAS", "ASA", "SSS"],
                    "ans": bad, "expl": f"{bad} 只能確定相似或不確定。",
                    "svg": "none", "params": {}
                }
        elif q_type == "calc":
            if random.random() > 0.5: # 角度
                a = random.randint(40, 80)
                b = random.randint(20, 180 - a - 10)
                ans = a + b
                opts = MathUtils.get_distractors(ans) + [str(ans)]
                random.shuffle(opts)
                return {
                    "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角？",
                    "options": opts, "ans": str(ans), "expl": "外角定理。",
                    "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}
                }
            else: # 多邊形
                n = random.choice([5, 6, 8, 10, 12])
                ans = (n-2)*180
                opts = [str(ans), str(n*180), "360", "720"]
                random.shuffle(opts)
                return {
                    "q": f"正 {n} 邊形的內角總和是多少度？",
                    "options": opts, "ans": str(ans), "expl": "公式 (n-2)×180。",
                    "svg": "polygon_n", "params": {"n": n}
                }
        else: # real (吸管)
            s1 = random.randint(5, 20)
            s2 = random.randint(5, 20)
            min_x, max_x = abs(s1 - s2), s1 + s2
            opts = [f"{min_x} < x < {max_x}", f"x > {max_x}", f"x < {min_x}", f"x = {max_x}"]
            random.shuffle(opts)
            return {
                "q": f"兩根吸管長 {s1}, {s2}，若要圍成三角形，第三邊 x 的範圍？",
                "options": opts, "ans": f"{min_x} < x < {max_x}",
                "expl": "兩邊差 < 第三邊 < 兩邊和。",
                "svg": "sticks_triangle", "params": {"s1": s1, "s2": s2}
            }

    # --- 3-2 外心 ---
    @staticmethod
    def gen_3_2(q_type):
        if q_type == "concept":
            tri_type = random.choice([("鈍角", "外部"), ("直角", "斜邊中點"), ("銳角", "內部")])
            return {
                "q": f"「{tri_type[0]}三角形」的外心位置在哪裡？",
                "options": [tri_type[1], "頂點", "重心", "不一定"],
                "ans": tri_type[1], "expl": "外心位置性質。",
                "svg": "triangle_circumcenter", "params": {}
            }
        elif q_type == "calc":
            if random.random() > 0.5: # 直角求半徑
                c = random.randint(5, 30) * 2
                r = c // 2
                opts = MathUtils.get_distractors(r) + [str(r)]
                random.shuffle(opts)
                return {
                    "q": f"直角三角形斜邊長 {c}，外接圓半徑 R？",
                    "options": opts, "ans": str(r), "expl": "直角外心在斜邊中點。",
                    "svg": "right_triangle_circumcenter", "params": {}
                }
            else: # 座標
                k = random.randint(2, 8) * 2
                ans = f"({k//2},{k//2})"
                opts = MathUtils.get_distractors(ans, "coord") + [ans]
                random.shuffle(opts)
                return {
                    "q": f"A(0,{k}), B({k},0), O(0,0)，求 △ABO 外心？",
                    "options": opts, "ans": ans, "expl": "斜邊中點公式。",
                    "svg": "coord_triangle", "params": {"k": k}
                }
        else:
            return {
                "q": "三村莊 A, B, C 想蓋共用水塔(到三點等距)，應蓋在？",
                "options": ["外心", "內心", "重心", "AB中點"],
                "ans": "外心", "expl": "外心到三頂點等距。",
                "svg": "triangle_circumcenter", "params": {}
            }

    # --- 3-3 內心 (使用精密幾何邏輯) ---
    @staticmethod
    def gen_3_3(q_type):
        if q_type == "concept":
            return {
                "q": "內心到三角形哪裡的距離相等？",
                "options": ["三邊", "三頂點", "三中點", "外部"],
                "ans": "三邊", "expl": "內切圓性質。",
                "svg": "triangle_incenter_concept", "params": {}
            }
        elif q_type == "calc":
            if random.random() > 0.5: # 角度
                deg = random.randint(30, 100)
                if deg % 2 != 0: deg += 1
                ans = 90 + deg // 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]
                random.shuffle(opts)
                return {
                    "q": f"I 為內心，∠A={deg}°，求 ∠BIC？",
                    "options": opts, "ans": str(ans), "expl": "公式：90 + A/2。",
                    "svg": "triangle_incenter_angle", "params": {"a": deg}
                }
            else: # 面積
                s = random.randint(10, 30)
                r = random.randint(2, 8)
                area = s * r // 2
                opts = MathUtils.get_distractors(area) + [str(area)]
                random.shuffle(opts)
                return {
                    "q": f"三角形周長 {s}，內切圓半徑 {r}，求面積？",
                    "options": opts, "ans": str(area), "expl": "面積 = rs/2。",
                    "svg": "triangle_incenter_concept", "params": {}
                }
        else:
            return {
                "q": "公園內蓋最大圓形噴水池，圓心選？",
                "options": ["內心", "外心", "重心", "頂點"],
                "ans": "內心", "expl": "內切圓性質。",
                "svg": "triangle_incenter_concept", "params": {}
            }

    # --- 3-4 重心 ---
    @staticmethod
    def gen_3_4(q_type):
        if q_type == "concept":
            return {
                "q": "重心是哪三條線的交點？",
                "options": ["中線", "中垂線", "角平分線", "高"],
                "ans": "中線", "expl": "重心定義。",
                "svg": "triangle_centroid", "params": {}
            }
        elif q_type == "calc":
            m = random.randint(2, 20) * 3
            ans = m * 2 // 3
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"G 為重心，中線 AD 長 {m}，求 AG？",
                "options": opts, "ans": str(ans), "expl": "重心分中線 2:1。",
                "svg": "triangle_centroid", "params": {"m": m}
            }
        else:
            return {
                "q": "手指頂住木板平衡，要放在？",
                "options": ["重心", "內心", "外心", "垂心"],
                "ans": "重心", "expl": "物理平衡點。",
                "svg": "triangle_centroid", "params": {}
            }

    # --- 4-1 因式分解 ---
    @staticmethod
    def gen_4_1(q_type):
        if q_type == "concept":
            return {
                "q": "若 ab=0，則？",
                "options": ["a=0 或 b=0", "a=0 且 b=0", "a=b", "無法判斷"],
                "ans": "a=0 或 b=0", "expl": "零積性質。",
                "svg": "none", "params": {}
            }
        elif q_type == "calc":
            k = random.randint(2, 12)
            ans = f"(x+{k})(x-{k})"
            opts = [ans, f"(x-{k})²", f"(x+{k})²", f"x(x-{k})"]
            random.shuffle(opts)
            return {
                "q": f"因式分解 x² - {k*k}？",
                "options": opts, "ans": ans, "expl": "平方差公式。",
                "svg": "diff_squares", "params": {"k": k}
            }
        else:
            area = random.randint(12, 100)
            return {
                "q": f"長方形面積 {area}，長寬整數，長寬關係？",
                "options": ["面積的因數", "面積的倍數", "必相等", "無關"],
                "ans": "面積的因數", "expl": "因倍數概念。",
                "svg": "rect_area", "params": {"area": area}
            }

    # --- 4-2 配方法 ---
    @staticmethod
    def gen_4_2(q_type):
        if q_type == "concept":
            return {
                "q": "判別式 D < 0 代表？",
                "options": ["無實根", "重根", "兩相異實根", "無限多解"],
                "ans": "無實根", "expl": "與 x 軸無交點。",
                "svg": "parabola_d_neg", "params": {}
            }
        elif q_type == "calc":
            k = random.randint(2, 12) * 2
            ans = (k//2)**2
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"x² + {k}x + □ 配成完全平方，□ = ？",
                "options": opts, "ans": str(ans), "expl": "補項公式。",
                "svg": "area_square_k", "params": {}
            }
        else:
            return {
                "q": "時間 t 為虛數，代表？",
                "options": ["無解(不可能發生)", "有兩個時間", "計算錯", "時間倒流"],
                "ans": "無解(不可能發生)", "expl": "物理無意義。",
                "svg": "parabola_d_neg", "params": {}
            }

    # --- 4-3 應用問題 ---
    @staticmethod
    def gen_4_3(q_type):
        if q_type == "concept":
            return {
                "q": "解幾何邊長為負數，應？",
                "options": ["捨去", "取絕對值", "保留", "重算"],
                "ans": "捨去", "expl": "長度必為正。",
                "svg": "none", "params": {}
            }
        elif q_type == "calc":
            n = random.randint(2, 15)
            val = n*(n-1)
            opts = MathUtils.get_distractors(n) + [str(n)]
            random.shuffle(opts)
            return {
                "q": f"某正數平方比該數大 {val}，求該數？",
                "options": opts, "ans": str(n), "expl": "列式求解。",
                "svg": "none", "params": {}
            }
        else:
            if random.random() > 0.5: # 梯子
                m = random.randint(2, 8)
                n = random.randint(1, m-1)
                a = m*m - n*n
                b = 2*m*n
                c = m*m + n*n
                if random.random() > 0.5: a, b = b, a
                opts = MathUtils.get_distractors(b) + [str(b)]
                random.shuffle(opts)
                return {
                    "q": f"梯子長 {c}，梯腳離牆 {a}，梯頂高度？",
                    "options": opts, "ans": str(b), "expl": "畢氏定理。",
                    "svg": "ladder_wall", "params": {"a":a, "b":b, "c":c}
                }
            else: # 煙火
                t = random.randint(2, 6)
                h = 20*t - 5*t*t
                opts = [str(h), "0", "100", "50"]
                random.shuffle(opts)
                return {
                    "q": f"煙火 h=20t-5t²，t={t} 時高度？",
                    "options": opts, "ans": str(h), "expl": "代入求解。",
                    "svg": "parabola_firework", "params": {}
                }

    # --- 路由 (完整版，不刪減) ---
    @staticmethod
    def generate(unit):
        mapping = {
            "3-1 證明與推理": QuestionFactory.gen_3_1,
            "3-2 三角形的外心": QuestionFactory.gen_3_2,
            "3-3 三角形的內心": QuestionFactory.gen_3_3,
            "3-4 三角形的重心": QuestionFactory.gen_3_4,
            "4-1 因式分解法": QuestionFactory.gen_4_1,
            "4-2 配方法與公式解": QuestionFactory.gen_4_2,
            "4-3 應用問題": QuestionFactory.gen_4_3
        }
        generator = mapping.get(unit)
        if not generator: return None
        return [generator("concept"), generator("calc"), generator("real")]

# ==========================================
# 3. 視覺繪圖引擎 (全功能 + 精密幾何版)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="220" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        
        # 🔥 V16 精密幾何修復：內切圓 🔥
        if svg_type == "triangle_incenter_angle":
            a_val = kwargs.get("a", 60)
            return base.format(f'''
                <path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/>
                <text x="150" y="25" font-size="16" text-anchor="middle" font-weight="bold">A ({a_val}°)</text>
                <text x="25" y="200" font-size="16" font-weight="bold">B</text>
                <text x="275" y="200" font-size="16" font-weight="bold">C</text>
                
                <!-- 精密座標: cx=150, cy=132.2, r=57.8 -->
                <circle cx="150" cy="132.2" r="57.8" fill="#fff9c4" stroke="#fbc02d" stroke-width="2" opacity="0.6"/>
                <circle cx="150" cy="132.2" r="4" fill="red"/>
                <text x="150" y="125" fill="red" font-size="14" text-anchor="middle" font-weight="bold">I</text>
                
                <line x1="40" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
                <line x1="260" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
                <text x="150" y="170" fill="blue" font-size="20" text-anchor="middle" font-weight="bold">?</text>
            ''')
        
        elif svg_type == "triangle_incenter_concept":
            return base.format('''
                <path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/>
                <circle cx="150" cy="132.2" r="57.8" fill="none" stroke="orange" stroke-width="2"/>
                <circle cx="150" cy="132.2" r="4" fill="orange"/>
                <text x="150" y="125" fill="orange" font-weight="bold" text-anchor="middle">I</text>
                <line x1="150" y1="132.2" x2="150" y2="190" stroke="orange" stroke-width="2" stroke-dasharray="4"/>
                <text x="155" y="165" font-size="14" fill="gray" font-weight="bold">r</text>
            ''')

        # --- 其他圖形 (完整保留) ---
        elif svg_type == "general_triangle":
            a = kwargs.get("angle_a", 60)
            b = kwargs.get("angle_b", 60)
            return base.format(f'''
                <path d="M80,150 L220,150 L120,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/>
                <text x="110" y="40" font-size="14">A({a}°)</text>
                <text x="60" y="160" font-size="14">B({b}°)</text>
                <text x="230" y="160" font-size="14" fill="red">C(外角?)</text>
                <line x1="220" y1="150" x2="280" y2="150" stroke="black" stroke-dasharray="4"/>
            ''')
        elif svg_type == "sticks_triangle":
            s1 = kwargs.get("s1", 5)
            s2 = kwargs.get("s2", 5)
            total = s1 + s2 if s1+s2 > 0 else 1
            scale = 150 / total
            w1 = s1 * scale
            w2 = s2 * scale
            return base.format(f'''
                <rect x="50" y="80" width="{w1}" height="10" fill="blue"/>
                <rect x="50" y="110" width="{w2}" height="10" fill="green"/>
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
                <text x="80" y="195" font-size="14">底{a}</text>
                <text x="100" y="110" font-size="14" fill="brown">斜{c}</text>
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
        elif svg_type == "diff_squares":
            k = kwargs.get("k", 3)
            return base.format(f'''
                <rect x="80" y="40" width="140" height="140" fill="#e8f5e9" stroke="black"/>
                <rect x="180" y="140" width="40" height="40" fill="white" stroke="red" stroke-dasharray="4"/>
                <text x="130" y="110" font-size="20">x²</text>
                <text x="190" y="165" font-size="12" fill="red">{k}²</text>
            ''')
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
        elif svg_type == "geometry_sas":
            return base.format('<path d="M30,120 L90,120 L60,40 Z" fill="none" stroke="black"/><path d="M160,120 L220,120 L190,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        elif svg_type == "right_triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#e0e0e0"/><path d="M90,40 L90,160 L210,160 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="100" r="5" fill="red"/><text x="160" y="95" fill="red">O</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#b2dfdb"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="90" fill="green">O</text>')
        elif svg_type == "triangle_centroid":
            return base.format('<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red" stroke-dasharray="4"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="160" y="130" fill="blue">G</text>')
        elif svg_type == "rect_area":
            area = kwargs.get("area", 24)
            return base.format(f'<rect x="50" y="50" width="200" height="100" fill="#fff9c4" stroke="orange" stroke-width="2"/><text x="120" y="105" font-size="20">Area = {area}</text>')
        elif svg_type == "parabola_d_neg":
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
        elif svg_type == "parabola_firework":
            return base.format('<path d="M20,180 Q150,-50 280,180" fill="none" stroke="red" stroke-width="2"/><circle cx="150" cy="40" r="5" fill="orange"/><text x="160" y="40">最高點</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        
        return ""

# ==========================================
# 4. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="♾️")
st.title("♾️ 國中數學無限生成引擎 (V17.0 終極完全體)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

units = [
    "3-1 證明與推理", "3-2 三角形的外心", "3-3 三角形的內心", "3-4 三角形的重心",
    "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題"
]
unit = st.sidebar.selectbox("請選擇練習單元", units)

if st.sidebar.button("🚀 生成無限試卷 (全單元+精密幾何)"):
    new_quiz = QuestionFactory.generate(unit)
    if new_quiz:
        st.session_state.quiz = new_quiz
        st.session_state.exam_finished = False
        st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        type_names = ["觀念", "計算", "情境"]
        
        for i, q in enumerate(st.session_state.quiz):
            badge = type_names[i] if i < 3 else "綜合"
            st.markdown(f"### Q{i+1} <span style='background-color:#e0f7fa; padding:2px 8px; border-radius:4px; font-size:0.7em; color:#006064'>{badge}</span> {q['q']}", unsafe_allow_html=True)
            
            if q.get('svg') != "none":
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('params', {})), unsafe_allow_html=True)
            
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
    if st.button("🔄 再生成一份 (題目會完全不同)", use_container_width=True):
        new_quiz = QuestionFactory.generate(unit)
        st.session_state.quiz = new_quiz
        st.session_state.exam_finished = False
        st.rerun()
