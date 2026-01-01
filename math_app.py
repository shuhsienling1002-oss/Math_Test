import streamlit as st
import random
import math
import time

# ==========================================
# 1. 數學工具箱 (負責運算與誘答)
# ==========================================
class MathUtils:
    @staticmethod
    def get_distractors(ans, mode="int"):
        """ 生成 3 個智慧型錯誤選項 """
        distractors = set()
        count = 0
        while len(distractors) < 3 and count < 50:
            count += 1
            if mode == "int":
                val = int(ans)
                trap = random.choice([
                    val + random.randint(1, 5), 
                    val - random.randint(1, 5),
                    val * 2, 
                    int(val / 2), 
                    -val,
                    val + 10
                ])
                if trap != val: distractors.add(str(trap))
            elif mode == "float":
                trap = round(ans + random.choice([0.5, -0.5, 1.0, -1.0, 2.0]), 1)
                if trap != ans and trap > 0: distractors.add(str(trap))
            elif mode == "coord": # 座標 (x,y)
                x, y = ans
                traps = [(y, x), (x, -y), (-x, y), (x+1, y+1), (0,0)]
                t = random.choice(traps)
                if t != ans: distractors.add(f"{t}")
        
        return list(distractors)

# ==========================================
# 2. 無限題庫工廠 (核心：即時生成邏輯)
# ==========================================
class QuestionFactory:
    """
    這裡沒有固定的題目列表。
    每一個函式都是一台「製造機」，每次呼叫都會吐出一個全新的題目物件。
    """
    
    # --- 單元 3-1: 證明與推理 ---
    @staticmethod
    def gen_3_1(q_type):
        if q_type == "concept":
            prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
            return {
                "q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
                "options": ["必全等", "不一定全等", "相似", "面積相等"],
                "ans": "必全等",
                "expl": f"{prop} 是全等性質。",
                "svg": "geometry_sas", "params": {}
            }
        elif q_type == "calc":
            # 無限生成：角度
            a = random.randint(40, 85)
            b = random.randint(20, 180 - a - 10)
            ans = a + b
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
                "options": opts, "ans": str(ans),
                "expl": "外角定理：外角等於不相鄰兩內角和。",
                "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}
            }
        else: # real
            # 無限生成：吸管長度
            s1 = random.randint(3, 15)
            s2 = random.randint(3, 15)
            min_x, max_x = abs(s1 - s2), s1 + s2
            opts = [f"{min_x} < x < {max_x}", f"x > {max_x}", f"x < {min_x}", f"x = {max_x}"]
            random.shuffle(opts)
            return {
                "q": f"兩根吸管長 {s1}, {s2}，若要圍成三角形，第三邊 x 的範圍？",
                "options": opts, "ans": f"{min_x} < x < {max_x}",
                "expl": "兩邊差 < 第三邊 < 兩邊和。",
                "svg": "sticks_triangle", "params": {"s1": s1, "s2": s2}
            }

    # --- 單元 3-2: 外心 ---
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
            # 無限生成：直角三角形斜邊
            c = random.randint(5, 50) * 2 # 確保偶數好整除
            r = c // 2
            opts = MathUtils.get_distractors(r) + [str(r)]
            random.shuffle(opts)
            return {
                "q": f"直角三角形斜邊長為 {c}，求外接圓半徑 R？",
                "options": opts, "ans": str(r),
                "expl": "直角三角形外心在斜邊中點，半徑=斜邊/2。",
                "svg": "right_triangle_circumcenter", "params": {}
            }
        else:
            # 無限生成：座標
            k = random.randint(2, 10) * 2
            ans = f"({k//2},{k//2})"
            opts = [ans, f"({k},{k})", "(0,0)", f"({k//3},{k//3})"]
            random.shuffle(opts)
            return {
                "q": f"座標平面上 A(0,{k}), B({k},0), O(0,0)，求 △ABO 外心座標？",
                "options": opts, "ans": ans,
                "expl": "直角三角形外心為斜邊中點。",
                "svg": "coord_triangle", "params": {"k": k}
            }

    # --- 單元 3-3: 內心 ---
    @staticmethod
    def gen_3_3(q_type):
        if q_type == "concept":
            return {
                "q": "內心到三角形哪裡的距離相等？",
                "options": ["三邊", "三頂點", "三中點", "外部"],
                "ans": "三邊", "expl": "內切圓性質。",
                "svg": "triangle_incenter", "params": {}
            }
        elif q_type == "calc":
            # 無限生成：角度
            deg = random.randint(30, 100)
            # 確保偶數方便計算
            if deg % 2 != 0: deg += 1
            ans = 90 + deg // 2
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"I 為內心，∠A={deg}°，求 ∠BIC？",
                "options": opts, "ans": str(ans),
                "expl": "公式：90 + A/2。",
                "svg": "triangle_incenter", "params": {"a": deg}
            }
        else:
            # 無限生成：面積
            s = random.randint(10, 30)
            r = random.randint(2, 8)
            area = s * r // 2
            opts = MathUtils.get_distractors(area) + [str(area)]
            random.shuffle(opts)
            return {
                "q": f"三角形周長 {s}，內切圓半徑 {r}，求面積？",
                "options": opts, "ans": str(area),
                "expl": "面積 = rs/2。",
                "svg": "triangle_incenter", "params": {}
            }

    # --- 單元 3-4: 重心 ---
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
            # 無限生成：中線長
            m = random.randint(2, 20) * 3
            ans = m * 2 // 3
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"G 為重心，中線 AD 長為 {m}，求 AG？",
                "options": opts, "ans": str(ans),
                "expl": "重心分中線為 2:1。",
                "svg": "triangle_centroid", "params": {"m": m}
            }
        else:
            area = random.randint(5, 50) * 6
            ans = area // 3
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"△ABC 面積 {area}，G 為重心。則 △GAB 面積為？",
                "options": opts, "ans": str(ans),
                "expl": "重心與頂點連線將面積三等分。",
                "svg": "triangle_centroid", "params": {}
            }

    # --- 單元 4-1: 因式分解 ---
    @staticmethod
    def gen_4_1(q_type):
        if q_type == "concept":
            return {
                "q": "若 (x-a)(x-b) = 0，則下列推論何者正確？",
                "options": ["x=a 或 x=b", "x=a 且 x=b", "x=0", "a=b"],
                "ans": "x=a 或 x=b", "expl": "零積性質。",
                "svg": "none", "params": {}
            }
        elif q_type == "calc":
            # 無限生成：平方差
            k = random.randint(2, 15)
            ans = f"(x+{k})(x-{k})"
            opts = [ans, f"(x-{k})²", f"(x+{k})²", f"x(x-{k})"]
            random.shuffle(opts)
            return {
                "q": f"因式分解 x² - {k*k}？",
                "options": opts, "ans": ans,
                "expl": "平方差公式。",
                "svg": "diff_squares", "params": {"k": k}
            }
        else:
            # 無限生成：矩形面積
            area = random.randint(12, 100)
            return {
                "q": f"長方形面積 {area}，長寬皆為整數，請問長寬可能是？",
                "options": ["需找出面積的因數", "需找出面積的倍數", "一定是正方形", "無法判斷"],
                "ans": "需找出面積的因數", "expl": "長 × 寬 = 面積。",
                "svg": "rect_area", "params": {"area": area}
            }

    # --- 單元 4-2: 配方法 ---
    @staticmethod
    def gen_4_2(q_type):
        if q_type == "concept":
            return {
                "q": "一元二次方程式判別式 D < 0 代表？",
                "options": ["無實根(圖形與x軸無交點)", "重根", "兩相異實根", "有三個根"],
                "ans": "無實根(圖形與x軸無交點)", "expl": "D < 0 圖形與 x 軸無交點。",
                "svg": "parabola_d_neg", "params": {}
            }
        elif q_type == "calc":
            # 無限生成：配方補項
            k = random.randint(2, 20) * 2
            ans = (k // 2) ** 2
            opts = MathUtils.get_distractors(ans) + [str(ans)]
            random.shuffle(opts)
            return {
                "q": f"x² + {k}x + □ 配成完全平方式，□ = ？",
                "options": opts, "ans": str(ans),
                "expl": "補項公式：(係數/2)²。",
                "svg": "area_square_k", "params": {}
            }
        else:
            return {
                "q": "利用公式解求出時間 t = 3 ± √(-5)，這代表什麼物理意義？",
                "options": ["無解(不可能發生)", "有兩個時間點", "時間倒流", "計算錯誤"],
                "ans": "無解(不可能發生)", "expl": "根號內為負數代表無實數解。",
                "svg": "parabola_d_neg", "params": {}
            }

    # --- 單元 4-3: 應用問題 ---
    @staticmethod
    def gen_4_3(q_type):
        if q_type == "concept":
            return {
                "q": "解應用問題算出邊長為 -5，應該如何處理？",
                "options": ["不合(捨去)", "取絕對值", "當作答案", "重算"],
                "ans": "不合(捨去)", "expl": "幾何長度必須為正數。",
                "svg": "none", "params": {}
            }
        elif q_type == "calc":
            # 無限生成：數列問題
            n = random.randint(2, 20)
            val = n * (n - 1)
            ans = n
            opts = MathUtils.get_distractors(n) + [str(n)]
            random.shuffle(opts)
            return {
                "q": f"某正數平方比該數大 {val}，求該數？",
                "options": opts, "ans": str(ans),
                "expl": f"x² - x = {val}。",
                "svg": "none", "params": {}
            }
        else:
            # 無限生成：梯子問題 (畢氏定理)
            # 產生畢氏三元數
            m = random.randint(2, 10)
            n = random.randint(1, m-1)
            a = m*m - n*n
            b = 2*m*n
            c = m*m + n*n
            # 隨機交換 a, b
            if random.random() > 0.5: a, b = b, a
            
            opts = MathUtils.get_distractors(b) + [str(b)]
            random.shuffle(opts)
            return {
                "q": f"梯子長 {c} 公尺，梯腳離牆 {a} 公尺，梯頂高度？",
                "options": opts, "ans": str(b),
                "expl": "畢氏定理。",
                "svg": "ladder_wall", "params": {"a":a, "b":b, "c":c}
            }

    # 路由：根據單元名稱分派
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
        
        # 每次生成 3 題 (觀念, 計算, 情境)
        q1 = generator("concept")
        q2 = generator("calc")
        q3 = generator("real")
        
        return [q1, q2, q3]

# ==========================================
# 3. 視覺繪圖引擎 (V12.0 即時渲染版)
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
            # 正規化長度以免爆框
            scale = 150 / (s1 + s2) 
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
        # 靜態圖形
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
        elif svg_type == "rect_area":
            area = kwargs.get("area", 24)
            return base.format(f'<rect x="50" y="50" width="200" height="100" fill="#fff9c4" stroke="orange" stroke-width="2"/><text x="120" y="105" font-size="20">Area = {area}</text>')
        elif svg_type == "parabola_d_neg":
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        
        return ""

# ==========================================
# 4. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="♾️")
st.title("♾️ 國中數學無限生成引擎 (V12.0)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

# 單元列表
units = [
    "3-1 證明與推理", "3-2 三角形的外心", "3-3 三角形的內心", "3-4 三角形的重心",
    "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題"
]
unit = st.sidebar.selectbox("請選擇練習單元", units)

# 生成按鈕 (每次按都會觸發 QuestionFactory.generate)
if st.sidebar.button("🚀 生成無限試卷 (即時運算)"):
    # 呼叫工廠生成新題目
    new_quiz = QuestionFactory.generate(unit)
    
    if new_quiz:
        st.session_state.quiz = new_quiz
        st.session_state.exam_finished = False
        st.rerun()
    else:
        st.error("該單元生成器尚未實作完畢。")

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        type_names = ["觀念", "計算", "情境"]
        
        for i, q in enumerate(st.session_state.quiz):
            badge = type_names[i] if i < 3 else "綜合"
            
            st.markdown(f"### Q{i+1} <span style='background-color:#e0f7fa; padding:2px 8px; border-radius:4px; font-size:0.7em; color:#006064'>{badge}</span> {q['q']}", unsafe_allow_html=True)
            
            # 繪圖
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
        # 重新生成
        new_quiz = QuestionFactory.generate(unit)
        st.session_state.quiz = new_quiz
        st.session_state.exam_finished = False
        st.rerun()
