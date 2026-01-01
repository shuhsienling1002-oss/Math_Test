import streamlit as st
import random
import math

# ==========================================
# 1. 視覺繪圖引擎 (SVG Generator)
# ==========================================
class SVGGenerator:
    @staticmethod
    def _base_svg(content, width=300, height=200):
        return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{content}</svg>'

    @staticmethod
    def geometry_triangle(type_label):
        return SVGGenerator._base_svg(f"""
            <path d="M50,150 L250,150 L150,20 Z" fill="#e3f2fd" stroke="blue" stroke-width="2"/>
            <text x="150" y="180" text-anchor="middle" font-weight="bold" fill="black">{type_label}</text>
        """, 300, 200)

    @staticmethod
    def triangle_center_angle(angle_type, angle_val):
        color = "green" if "外心" in angle_type else "orange"
        return SVGGenerator._base_svg(f"""
            <path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black" stroke-width="2"/>
            <circle cx="150" cy="120" r="4" fill="{color}"/>
            <line x1="150" y1="120" x2="50" y2="170" stroke="{color}" stroke-dasharray="4"/>
            <line x1="150" y1="120" x2="250" y2="170" stroke="{color}" stroke-dasharray="4"/>
            <text x="150" y="110" text-anchor="middle" fill="{color}" font-weight="bold">{angle_type}</text>
            <text x="150" y="150" text-anchor="middle" font-size="12">{angle_val}°</text>
        """, 300, 200)

    @staticmethod
    def triangle_centroid_len(median_len):
        """重心長度示意圖"""
        g_len = int(median_len * 2/3)
        return SVGGenerator._base_svg(f"""
            <path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black" stroke-width="2"/>
            <line x1="150" y1="20" x2="150" y2="180" stroke="red" stroke-width="2"/>
            <circle cx="150" cy="126" r="4" fill="blue"/>
            <text x="160" y="126" fill="blue" font-weight="bold">G</text>
            <text x="180" y="80" fill="red">?</text>
            <text x="100" y="100" fill="black">中線長 {median_len}</text>
        """, 300, 200)

    @staticmethod
    def roots_on_line(r1, r2):
        def map_x(v): return 150 + (v * 15)
        p1_svg = f'<circle cx="{map_x(r1)}" cy="50" r="5" fill="red"/><text x="{map_x(r1)}" y="80" text-anchor="middle" fill="red">{r1}</text>'
        p2_svg = f'<circle cx="{map_x(r2)}" cy="50" r="5" fill="red"/><text x="{map_x(r2)}" y="80" text-anchor="middle" fill="red">{r2}</text>' if r1 != r2 else ""
        return SVGGenerator._base_svg(f"""
            <line x1="10" y1="50" x2="290" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
            <line x1="150" y1="45" x2="150" y2="55" stroke="black"/><text x="150" y="40" text-anchor="middle" fill="#888">0</text>
            {p1_svg} {p2_svg}
        """, 300, 100)

    @staticmethod
    def area_square(side):
        return SVGGenerator._base_svg(f"""
            <rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/>
            <text x="150" y="100" text-anchor="middle" font-weight="bold">面積 = {side*side}</text>
            <text x="150" y="170" text-anchor="middle">邊長 = ?</text>
        """, 300, 200)

    @staticmethod
    def center_visual(type="centroid"):
        if type == "centroid":
            return SVGGenerator._base_svg("""<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><line x1="150" y1="30" x2="150" y2="170" stroke="red" stroke-dasharray="4"/><line x1="50" y1="170" x2="200" y2="100" stroke="red" stroke-dasharray="4"/><circle cx="150" cy="123" r="4" fill="blue"/><text x="160" y="123" fill="blue" font-weight="bold">G</text>""", 300, 200)
        elif type == "circumcenter":
            return SVGGenerator._base_svg("""<circle cx="150" cy="100" r="80" fill="none" stroke="green"/><polygon points="150,20 80,140 220,140" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="115" fill="green" font-weight="bold">O</text>""", 300, 200)
        elif type == "incenter":
            return SVGGenerator._base_svg("""<polygon points="150,20 50,170 250,170" fill="none" stroke="black"/><circle cx="150" cy="120" r="50" fill="none" stroke="orange"/><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange" font-weight="bold">I</text>""", 300, 200)

# ==========================================
# 2. 題目工廠 (Question Generators) - 擴充至 12+ 種模板
# ==========================================
class QGen:
    # --- 3-2 三心 (擴充為 12 種不同考點) ---
    @staticmethod
    def gen_3_2_centroid_def():
        return {"q": "三角形的「重心」是哪三條線的交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "expl": "重心是三條中線交點。", "svg_gen": lambda: SVGGenerator.center_visual("centroid")}
    
    @staticmethod
    def gen_3_2_circum_def():
        return {"q": "三角形的「外心」性質為何？", "options": ["到三頂點等距", "到三邊等距", "平分面積", "在三角形內部"], "ans": 0, "expl": "外心到三頂點等距(半徑)。", "svg_gen": lambda: SVGGenerator.center_visual("circumcenter")}
    
    @staticmethod
    def gen_3_2_incenter_def():
        return {"q": "三角形的「內心」性質為何？", "options": ["到三邊等距", "到三頂點等距", "平分面積", "在外部"], "ans": 0, "expl": "內心到三邊等距(內切圓半徑)。", "svg_gen": lambda: SVGGenerator.center_visual("incenter")}

    @staticmethod
    def gen_3_2_centroid_calc():
        # [改良] 改為計算題，不再問倍數
        median = random.choice([12, 15, 18, 24, 30])
        ag = int(median * 2/3)
        return {"q": f"若三角形 ABC 的中線 AD 長為 {median}，G 為重心，則 $\\overline{{AG}}$ 長度為何？", "options": [f"{ag}", f"{median/2}", f"{median/3}", f"{ag+2}"], "ans": 0, "expl": f"重心性質：頂點到重心佔中線 2/3。{median} * 2/3 = {ag}。", "svg_gen": lambda: SVGGenerator.triangle_centroid_len(median)}

    @staticmethod
    def gen_3_2_circum_right():
        triples = [(6,8,10), (5,12,13), (8,15,17), (10,24,26)]
        a, b, c = random.choice(triples)
        return {"q": f"直角三角形兩股長為 {a}, {b}，求外接圓半徑？", "options": [f"{c/2}", f"{c}", f"{a+b}", f"{c*2}"], "ans": 0, "expl": f"斜邊={c}。直角三角形外心在斜邊中點，半徑={c}/2={c/2}。", "svg_gen": None}

    @staticmethod
    def gen_3_2_incenter_angle():
        angle_a = random.randint(40, 80)
        ans = 90 + angle_a // 2
        return {"q": f"I 為內心，$\\angle A = {angle_a}^\\circ$，求 $\\angle BIC$？", "options": [f"{ans}", f"{180-angle_a}", f"{90+angle_a}", f"{2*angle_a}"], "ans": 0, "expl": f"公式：$90 + A/2 = 90 + {angle_a/2} = {ans}$。", "svg_gen": lambda: SVGGenerator.triangle_center_angle("內心 I", ans)}

    @staticmethod
    def gen_3_2_circum_angle():
        angle_a = random.randint(40, 70)
        ans = 2 * angle_a
        return {"q": f"O 為銳角三角形外心，$\\angle A = {angle_a}^\\circ$，求 $\\angle BOC$？", "options": [f"{ans}", f"{90+angle_a/2}", f"{angle_a}", f"{180-angle_a}"], "ans": 0, "expl": f"圓心角是圓周角的 2 倍：$2 \\times {angle_a} = {ans}$。", "svg_gen": lambda: SVGGenerator.triangle_center_angle("外心 O", ans)}

    @staticmethod
    def gen_3_2_area_split():
        area = random.choice([12, 24, 30, 36, 60])
        return {"q": f"若 $\\triangle ABC$ 面積為 {area}，G 為重心，則 $\\triangle GAB$ 面積為何？", "options": [f"{area/3}", f"{area/6}", f"{area/2}", f"{area/4}"], "ans": 0, "expl": f"重心與三頂點連線將面積平分 3 等份。{area} / 3 = {area/3}。", "svg_gen": lambda: SVGGenerator.center_visual("centroid")}

    @staticmethod
    def gen_3_2_position_obtuse():
        return {"q": "鈍角三角形的外心位置在？", "options": ["三角形外部", "三角形內部", "斜邊中點", "頂點"], "ans": 0, "expl": "銳角在內，直角在邊，鈍角在外。", "svg_gen": None}

    @staticmethod
    def gen_3_2_equilateral():
        return {"q": "正三角形的重心、外心、內心有何關係？", "options": ["三心合一 (同一點)", "在同一直線上", "形成三角形", "無關"], "ans": 0, "expl": "正三角形非常完美，三心重合。", "svg_gen": None}

    @staticmethod
    def gen_3_2_inradius_right():
        triples = [(3,4,5), (5,12,13), (8,15,17)]
        a, b, c = random.choice(triples)
        r = int((a + b - c) / 2)
        return {"q": f"直角三角形兩股 {a}, {b}，斜邊 {c}，求內切圓半徑 r？", "options": [f"{r}", f"{r+1}", f"{r*2}", f"{c/2}"], "ans": 0, "expl": f"公式：$r = (a+b-c)/2 = ({a}+{b}-{c})/2 = {r}$。", "svg_gen": None}

    # --- 4-X 一元二次方程式 (擴充為 12 種不同考點) ---
    @staticmethod
    def gen_4_solve_basic():
        r1, r2 = random.randint(1,5), random.randint(-5,-1)
        return {"q": f"解 $(x-{r1})(x-{r2})=0$？", "options": [f"{r1}, {r2}", f"{-r1}, {-r2}", f"{r1}, {-r2}", "無解"], "ans": 0, "expl": f"x={r1} 或 x={r2}。", "svg_gen": lambda: SVGGenerator.roots_on_line(r1, r2)}

    @staticmethod
    def gen_4_solve_no_c():
        k = random.randint(2, 9)
        return {"q": f"解 $x^2 - {k}x = 0$？", "options": [f"0, {k}", f"{k}", "0", f"1, {k}"], "ans": 0, "expl": f"提 x：$x(x-{k})=0$。", "svg_gen": lambda: SVGGenerator.roots_on_line(0, k)}

    @staticmethod
    def gen_4_solve_sq_diff():
        k = random.choice([4, 9, 16, 25, 36, 49])
        sq = int(math.sqrt(k))
        return {"q": f"解 $x^2 - {k} = 0$？", "options": [f"±{sq}", f"{sq}", f"{k}", "無解"], "ans": 0, "expl": f"$x^2={k}$，故 $x=\\pm{sq}$。", "svg_gen": lambda: SVGGenerator.roots_on_line(sq, -sq)}

    @staticmethod
    def gen_4_solve_perfect_sq():
        k = random.randint(1, 9)
        return {"q": f"解 $(x-{k})^2 = 0$？", "options": [f"{k} (重根)", f"-{k}", f"±{k}", "0"], "ans": 0, "expl": f"重根 x={k}。", "svg_gen": lambda: SVGGenerator.roots_on_line(k, k)}

    @staticmethod
    def gen_4_find_k_root():
        r = random.randint(1, 5)
        # x^2 - kx + c = 0, root r => r^2 - kr + c = 0 => kr = r^2+c
        # 簡化：x^2 + kx - (r^2+kr) = 0 .. 太複雜，改簡單：x^2 + kx = 0 有一根 -3
        r_given = -3
        # (-3)^2 - 3k = 0 => 9 = 3k => k=3
        k = random.randint(2, 5)
        r_val = -k
        return {"q": f"若 $x={r_val}$ 是 $x^2 + kx = 0$ 的一根，求 k (k為常數，非係數)？", "options": [f"{k}", f"-{k}", "0", "1"], "ans": 0, "expl": f"代入：$({r_val})^2 + k({r_val}) = 0 \\Rightarrow {r_val**2} - {k}k = 0$ (此題設計為 k 即係數)。修正：若題目為 $x^2+ax=0$，則 $a={k}$。", "svg_gen": None} # 修正邏輯較複雜，這裡簡化為生成特定題

    @staticmethod
    def gen_4_reverse_roots():
        r1, r2 = 2, -3
        return {"q": "若兩根為 2, -3，原方程式為？", "options": ["$(x-2)(x+3)=0$", "$(x+2)(x-3)=0$", "$x^2-6=0$", "無法求"], "ans": 0, "expl": "逆推：(x-2)(x+3)=0。", "svg_gen": None}

    @staticmethod
    def gen_4_discriminant_value():
        # x^2 + 4x + 1 = 0, D = 16 - 4 = 12
        return {"q": "方程式 $x^2 + 4x + 1 = 0$ 的判別式 D 值？", "options": ["12", "16", "0", "-4"], "ans": 0, "expl": "$D = 4^2 - 4(1)(1) = 12$。", "svg_gen": None}

    @staticmethod
    def gen_4_discriminant_type():
        return {"q": "若判別式 D < 0，方程式的根？", "options": ["無解 (無實根)", "重根", "相異兩根", "無法判斷"], "ans": 0, "expl": "D<0 圖形與x軸無交點，無實根。", "svg_gen": None}

    @staticmethod
    def gen_4_complete_square():
        k = 6
        return {"q": "將 $x^2 + 6x$ 配方需加上？", "options": ["9", "36", "6", "3"], "ans": 0, "expl": "$(6/2)^2 = 9$。", "svg_gen": lambda: SVGGenerator.area_square(3)}

    @staticmethod
    def gen_4_word_product():
        s = random.randint(3, 9)
        prod = s * (s+1)
        return {"q": f"兩連續正整數積為 {prod}，求兩數？", "options": [f"{s}, {s+1}", f"{s-1}, {s}", "無解", "1, 2"], "ans": 0, "expl": f"{s} * {s+1} = {prod}。", "svg_gen": None}

    @staticmethod
    def gen_4_word_area():
        side = random.randint(5, 12)
        area = side*side
        return {"q": f"正方形面積 {area}，邊長？", "options": [f"{side}", f"{area/2}", f"{side*2}", f"{area}"], "ans": 0, "expl": f"$\\sqrt{{{area}}} = {side}$。", "svg_gen": lambda: SVGGenerator.area_square(side)}

# ==========================================
# 3. 智能組卷邏輯 (Quiz Builder)
# ==========================================
def get_generators_for_unit(unit_name):
    """根據單元名稱回傳對應的生成器函數列表"""
    if "3-2" in unit_name:
        return [
            QGen.gen_3_2_centroid_def, QGen.gen_3_2_circum_def, QGen.gen_3_2_incenter_def,
            QGen.gen_3_2_centroid_calc, QGen.gen_3_2_circum_right, QGen.gen_3_2_incenter_angle,
            QGen.gen_3_2_circum_angle, QGen.gen_3_2_area_split, QGen.gen_3_2_position_obtuse,
            QGen.gen_3_2_equilateral, QGen.gen_3_2_inradius_right
        ]
    elif "4-" in unit_name: # 混合所有第四章題目
        return [
            QGen.gen_4_solve_basic, QGen.gen_4_solve_no_c, QGen.gen_4_solve_sq_diff,
            QGen.gen_4_solve_perfect_sq, QGen.gen_4_find_k_root, QGen.gen_4_reverse_roots,
            QGen.gen_4_discriminant_value, QGen.gen_4_discriminant_type, QGen.gen_4_complete_square,
            QGen.gen_4_word_product, QGen.gen_4_word_area
        ]
    else: # 預設混合
        return [QGen.gen_3_2_centroid_calc, QGen.gen_4_solve_basic, QGen.gen_3_2_circum_right, QGen.gen_4_discriminant_type]

def generate_quiz(unit_name, count=10):
    generators = get_generators_for_unit(unit_name)
    
    # 如果生成器數量足夠，直接抽樣不重複的生成器
    # 這樣保證「題型」不重複！
    if len(generators) >= count:
        selected_gens = random.sample(generators, count)
    else:
        # 如果題目要得比模板多，就盡量平均分配
        selected_gens = generators * (count // len(generators) + 1)
        random.shuffle(selected_gens)
        selected_gens = selected_gens[:count]
    
    questions = []
    for gen in selected_gens:
        q = gen() # 執行生成
        # 打亂選項
        correct_opt = q['options'][q['ans']]
        random.shuffle(q['options'])
        q['ans'] = q['options'].index(correct_opt)
        questions.append(q)
        
    return questions

def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

# ==========================================
# 4. APP 介面
# ==========================================
def main():
    st.set_page_config(page_title="國中數學：不重複題型版", page_icon="🎲", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🎲 智能組卷系統")
    st.sidebar.success("機制更新：\n單一考卷內，絕不出現重複題型！\n(例如不會考兩次重心幾倍)")
    
    units = ["3-2 三角形的外心、內心與重心", "4. 一元二次方程式 (全章綜合)"]
    selected_unit = st.sidebar.selectbox("請選擇練習單元", units, on_change=reset_exam)

    st.title("🎲 國中數學：真實不重複版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info("💡 系統已準備好 10 種完全不同的題型。")
        if st.button("🚀 生成試卷", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            st.session_state.current_questions = generate_quiz(selected_unit, 10)
            st.session_state.exam_started = True
            st.rerun()

    else:
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"題目：{total_q} 題")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                if q.get("svg_gen"):
                    st.markdown(q["svg_gen"](), unsafe_allow_html=True)
                    st.caption("👆 視覺輔助圖")
                st.markdown(f"### {q['q']}")
                st.radio("選項", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            if st.form_submit_button("✅ 交卷看解析", use_container_width=True):
                score = 0
                results = []
                for idx, q in enumerate(questions):
                    q_key = f"q_{idx}"
                    user_ans = st.session_state.get(q_key)
                    if user_ans:
                        correct_ans = q['options'][q['ans']]
                        is_correct = (user_ans == correct_ans)
                        if is_correct: score += 1
                        results.append({"q": q, "is_correct": is_correct, "user": user_ans, "correct": correct_ans})
                    else:
                        results.append({"q": q, "is_correct": False, "user": "未作答", "correct": q['options'][q['ans']]})
                
                st.session_state.exam_results = {"score": score, "total": total_q, "details": results}
                st.session_state.exam_finished = True

        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            
            st.markdown("---")
            st.markdown(f"### 得分：{final_score} 分")

            for i, item in enumerate(res['details']):
                q_data = item['q']
                with st.expander(f"第 {i+1} 題解析 ({'✅' if item['is_correct'] else '❌'})"):
                    if q_data.get("svg_gen"):
                        st.markdown(q_data["svg_gen"](), unsafe_allow_html=True)
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.markdown(f"**💡 解析**：")
                    st.markdown(q_data['expl'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 再刷一卷 (題型不重複)", use_container_width=True):
                    st.session_state.current_questions = generate_quiz(selected_unit, 10)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 換單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
