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

    @staticmethod
    def geometry_sas():
        return SVGGenerator._base_svg("""
            <path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text>
            <path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text>
            <text x="115" y="80" text-anchor="middle" font-weight="bold" fill="blue">全等?</text>
        """, 300, 150)

# ==========================================
# 2. 題目工廠 (Question Generators) - 28種生成器全數到位
# ==========================================
class QGen:
    # --- 3-1 證明與推理 (5種) ---
    @staticmethod
    def gen_3_1_sss_sas():
        props = ["SSS", "SAS", "ASA", "AAS", "RHS"]
        ans = random.choice(props)
        return {"q": f"若已知兩個三角形滿足「{ans}」條件，則它們的關係為何？", "options": ["必全等", "必相似但不一定全等", "面積相等但不一定全等", "無法判斷"], "ans": 0, "expl": f"{ans} 是全等判別性質之一。", "svg_gen": lambda: SVGGenerator.geometry_sas()}

    @staticmethod
    def gen_3_1_angle_calc():
        in1, in2 = random.randint(30, 80), random.randint(30, 80)
        return {"q": f"三角形 ABC 中，$\\angle A={in1}^\\circ, \\angle B={in2}^\\circ$，求 $\\angle C$ 的外角？", "options": [f"{in1+in2}", f"{180-(in1+in2)}", "180", "90"], "ans": 0, "expl": f"外角等於不相鄰內角和：{in1}+{in2}={in1+in2}。", "svg_gen": None}

    @staticmethod
    def gen_3_1_side_angle():
        return {"q": "若 $\\angle A > \\angle B$，則對邊關係？", "options": ["BC > AC", "BC < AC", "BC = AC", "無法判斷"], "ans": 0, "expl": "大角對大邊。", "svg_gen": None}

    @staticmethod
    def gen_3_1_quad_prop():
        q_map = {"菱形": "對角線互相垂直平分", "矩形": "對角線等長且互相平分", "平行四邊形": "對角線互相平分"}
        shape = random.choice(list(q_map.keys()))
        return {"q": f"下列何者是「{shape}」的對角線性質？", "options": [q_map[shape], "對角線互相垂直且等長", "對角線只有一條平分", "無"], "ans": 0, "expl": f"{shape} 性質：{q_map[shape]}。", "svg_gen": None}

    @staticmethod
    def gen_3_1_isosceles():
        # 隨機化避免重複
        q_type = random.randint(1, 2)
        if q_type == 1:
            return {"q": "等腰三角形的頂角平分線性質？", "options": ["垂直平分底邊", "只平分", "只垂直", "無"], "ans": 0, "expl": "三線合一。", "svg_gen": None}
        else:
            deg = random.choice([40, 50, 70])
            ans = (180 - deg) // 2
            return {"q": f"等腰三角形頂角 {deg} 度，求底角？", "options": [f"{ans}", f"{deg}", f"{180-deg}", "60"], "ans": 0, "expl": f"(180-{deg})/2 = {ans}", "svg_gen": None}

    # --- 3-2 三心 (11種) ---
    @staticmethod
    def gen_3_2_centroid_def():
        return {"q": "三角形的「重心」是哪三條線的交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "expl": "重心是三條中線交點。", "svg_gen": lambda: SVGGenerator.center_visual("centroid")}
    
    @staticmethod
    def gen_3_2_circum_def():
        return {"q": "三角形的「外心」性質為何？", "options": ["到三頂點等距", "到三邊等距", "平分面積", "在三角形內部"], "ans": 0, "expl": "外心到三頂點等距。", "svg_gen": lambda: SVGGenerator.center_visual("circumcenter")}
    
    @staticmethod
    def gen_3_2_incenter_def():
        return {"q": "三角形的「內心」性質為何？", "options": ["到三邊等距", "到三頂點等距", "平分面積", "在外部"], "ans": 0, "expl": "內心到三邊等距。", "svg_gen": lambda: SVGGenerator.center_visual("incenter")}

    @staticmethod
    def gen_3_2_centroid_calc():
        median = random.choice([12, 15, 18, 24, 30])
        ag = int(median * 2/3)
        return {"q": f"若中線 AD 長為 {median}，G 為重心，則 $\\overline{{AG}}$ 長度為何？", "options": [f"{ag}", f"{median/2}", f"{median/3}", f"{ag+2}"], "ans": 0, "expl": f"重心性質：2/3 * {median} = {ag}。", "svg_gen": lambda: SVGGenerator.triangle_centroid_len(median)}

    @staticmethod
    def gen_3_2_circum_right():
        triples = [(6,8,10), (5,12,13), (8,15,17), (10,24,26)]
        a, b, c = random.choice(triples)
        return {"q": f"直角三角形兩股長為 {a}, {b}，求外接圓半徑？", "options": [f"{c/2}", f"{c}", f"{a+b}", f"{c*2}"], "ans": 0, "expl": f"斜邊={c}。半徑={c}/2={c/2}。", "svg_gen": None}

    @staticmethod
    def gen_3_2_incenter_angle():
        angle_a = random.randint(40, 80)
        ans = 90 + angle_a // 2
        return {"q": f"I 為內心，$\\angle A = {angle_a}^\\circ$，求 $\\angle BIC$？", "options": [f"{ans}", f"{180-angle_a}", f"{90+angle_a}", f"{2*angle_a}"], "ans": 0, "expl": f"公式：$90 + {angle_a}/2 = {ans}$。", "svg_gen": lambda: SVGGenerator.triangle_center_angle("內心 I", ans)}

    @staticmethod
    def gen_3_2_circum_angle():
        angle_a = random.randint(40, 70)
        ans = 2 * angle_a
        return {"q": f"O 為銳角外心，$\\angle A = {angle_a}^\\circ$，求 $\\angle BOC$？", "options": [f"{ans}", f"{90+angle_a/2}", f"{angle_a}", f"{180-angle_a}"], "ans": 0, "expl": f"圓心角是圓周角的 2 倍：$2 \\times {angle_a} = {ans}$。", "svg_gen": lambda: SVGGenerator.triangle_center_angle("外心 O", ans)}

    @staticmethod
    def gen_3_2_area_split():
        area = random.choice([12, 24, 30, 36, 60])
        return {"q": f"若 $\\triangle ABC$ 面積為 {area}，G 為重心，則 $\\triangle GAB$ 面積為何？", "options": [f"{area/3}", f"{area/6}", f"{area/2}", f"{area/4}"], "ans": 0, "expl": f"重心平分 3 等份。{area} / 3 = {area/3}。", "svg_gen": lambda: SVGGenerator.center_visual("centroid")}

    @staticmethod
    def gen_3_2_position_obtuse():
        return {"q": "鈍角三角形的外心位置在？", "options": ["三角形外部", "三角形內部", "斜邊中點", "頂點"], "ans": 0, "expl": "鈍角在外。", "svg_gen": None}

    @staticmethod
    def gen_3_2_equilateral():
        return {"q": "正三角形的重心、外心、內心有何關係？", "options": ["三心合一 (同一點)", "在同一直線上", "形成三角形", "無關"], "ans": 0, "expl": "正三角形三心重合。", "svg_gen": None}

    @staticmethod
    def gen_3_2_inradius_right():
        triples = [(3,4,5), (5,12,13), (8,15,17)]
        a, b, c = random.choice(triples)
        r = int((a + b - c) / 2)
        return {"q": f"直角三角形兩股 {a}, {b}，斜邊 {c}，求內切圓半徑 r？", "options": [f"{r}", f"{r+1}", f"{r*2}", f"{c/2}"], "ans": 0, "expl": f"公式：$r = (a+b-c)/2 = ({a}+{b}-{c})/2 = {r}$。", "svg_gen": None}

    # --- 4-1 因式分解法 (6種) ---
    @staticmethod
    def gen_4_1_solve_basic():
        r1, r2 = random.randint(1,5), random.randint(-5,-1)
        return {"q": f"解 $(x-{r1})(x-{r2})=0$？", "options": [f"{r1}, {r2}", f"{-r1}, {-r2}", f"{r1}, {-r2}", "無解"], "ans": 0, "expl": f"x={r1} 或 x={r2}。", "svg_gen": lambda: SVGGenerator.roots_on_line(r1, r2)}

    @staticmethod
    def gen_4_1_solve_no_c():
        k = random.randint(2, 9)
        return {"q": f"解 $x^2 - {k}x = 0$？", "options": [f"0, {k}", f"{k}", "0", f"1, {k}"], "ans": 0, "expl": f"提 x：$x(x-{k})=0$。", "svg_gen": lambda: SVGGenerator.roots_on_line(0, k)}

    @staticmethod
    def gen_4_1_solve_sq_diff():
        k = random.choice([4, 9, 16, 25, 36, 49])
        sq = int(math.sqrt(k))
        return {"q": f"解 $x^2 - {k} = 0$？", "options": [f"±{sq}", f"{sq}", f"{k}", "無解"], "ans": 0, "expl": f"$x^2={k}$，故 $x=\\pm{sq}$。", "svg_gen": lambda: SVGGenerator.roots_on_line(sq, -sq)}

    @staticmethod
    def gen_4_1_solve_perfect_sq():
        k = random.randint(1, 9)
        return {"q": f"解 $(x-{k})^2 = 0$？", "options": [f"{k} (重根)", f"-{k}", f"±{k}", "0"], "ans": 0, "expl": f"重根 x={k}。", "svg_gen": lambda: SVGGenerator.roots_on_line(k, k)}

    @staticmethod
    def gen_4_1_find_k_root():
        k = random.randint(2, 5)
        r_val = -k
        return {"q": f"若 $x={r_val}$ 是 $x^2 + kx = 0$ 的一根，求 k？", "options": [f"{k}", f"-{k}", "0", "1"], "ans": 0, "expl": f"代入求得 k={k}。", "svg_gen": None}

    @staticmethod
    def gen_4_1_reverse_roots():
        return {"q": "若兩根為 2, -3，原方程式為？", "options": ["$(x-2)(x+3)=0$", "$(x+2)(x-3)=0$", "$x^2-6=0$", "無法求"], "ans": 0, "expl": "逆推：(x-2)(x+3)=0。", "svg_gen": None}

    # --- 4-2 配方法 (4種) ---
    @staticmethod
    def gen_4_2_discriminant_value():
        return {"q": "方程式 $x^2 + 4x + 1 = 0$ 的判別式 D 值？", "options": ["12", "16", "0", "-4"], "ans": 0, "expl": "$D = 16 - 4 = 12$。", "svg_gen": None}

    @staticmethod
    def gen_4_2_discriminant_type():
        return {"q": "若判別式 D < 0，方程式的根？", "options": ["無解 (無實根)", "重根", "相異兩根", "無法判斷"], "ans": 0, "expl": "D<0 無實根。", "svg_gen": None}

    @staticmethod
    def gen_4_2_complete_square():
        k = random.randint(1, 5) * 2
        return {"q": f"將 $x^2 + {k}x$ 配方需加上？", "options": [f"{(k//2)**2}", f"{k}", f"{k*2}", "1"], "ans": 0, "expl": f"加上 $({k}/2)^2$。", "svg_gen": lambda: SVGGenerator.area_square(k//2)}

    @staticmethod
    def gen_4_2_formula_def():
        return {"q": "一元二次方程式公式解中，根號內的是？", "options": ["$b^2-4ac$", "$b^2+4ac$", "$2a$", "$b-4ac$"], "ans": 0, "expl": "判別式 D = $b^2-4ac$。", "svg_gen": None}

    # --- 4-3 應用問題 (3種) ---
    @staticmethod
    def gen_4_3_word_product():
        s = random.randint(3, 9)
        prod = s * (s+1)
        return {"q": f"兩連續正整數積為 {prod}，求兩數？", "options": [f"{s}, {s+1}", f"{s-1}, {s}", "無解", "1, 2"], "ans": 0, "expl": f"{s} * {s+1} = {prod}。", "svg_gen": lambda: SVGGenerator.roots_on_line(s, s+1)}

    @staticmethod
    def gen_4_3_word_area():
        side = random.randint(5, 12)
        area = side*side
        return {"q": f"正方形面積 {area}，邊長？", "options": [f"{side}", f"{area/2}", f"{side*2}", f"{area}"], "ans": 0, "expl": f"$\\sqrt{{{area}}} = {side}$。", "svg_gen": lambda: SVGGenerator.area_square(side)}

    @staticmethod
    def gen_4_3_physics():
        t = random.randint(2, 6)
        return {"q": f"物體落下距離 $h=5t^2$，若 $h={5*t*t}$，求時間 t？", "options": [f"{t}", f"{t*2}", f"{t+5}", "10"], "ans": 0, "expl": f"{5*t*t} = 5t^2 => t={t}。", "svg_gen": None}

# ==========================================
# 3. 智能組卷邏輯 (Router)
# ==========================================
def get_generators_for_unit(unit_name):
    """根據單元名稱回傳生成器列表"""
    # [檢查] 確保這裡列出的所有 function 都在 QGen 中定義了
    if "3-1" in unit_name:
        return [QGen.gen_3_1_sss_sas, QGen.gen_3_1_angle_calc, QGen.gen_3_1_side_angle, QGen.gen_3_1_quad_prop, QGen.gen_3_1_isosceles]
    elif "3-2" in unit_name:
        return [QGen.gen_3_2_centroid_def, QGen.gen_3_2_circum_def, QGen.gen_3_2_incenter_def, 
                QGen.gen_3_2_centroid_calc, QGen.gen_3_2_circum_right, QGen.gen_3_2_incenter_angle, 
                QGen.gen_3_2_circum_angle, QGen.gen_3_2_area_split, QGen.gen_3_2_position_obtuse, 
                QGen.gen_3_2_equilateral, QGen.gen_3_2_inradius_right]
    elif "4-1" in unit_name:
        return [QGen.gen_4_1_solve_basic, QGen.gen_4_1_solve_no_c, QGen.gen_4_1_solve_sq_diff, QGen.gen_4_1_solve_perfect_sq, QGen.gen_4_1_find_k_root, QGen.gen_4_1_reverse_roots]
    elif "4-2" in unit_name:
        return [QGen.gen_4_2_discriminant_value, QGen.gen_4_2_discriminant_type, QGen.gen_4_2_complete_square, QGen.gen_4_2_formula_def]
    elif "4-3" in unit_name:
        return [QGen.gen_4_3_word_product, QGen.gen_4_3_word_area, QGen.gen_4_3_physics]
    else: # 總複習
        return [QGen.gen_3_2_centroid_calc, QGen.gen_4_1_solve_basic, QGen.gen_4_3_word_area, QGen.gen_3_2_incenter_angle, QGen.gen_3_1_isosceles]

def generate_quiz(unit_name, count=10):
    generators = get_generators_for_unit(unit_name)
    # [邏輯] 確保生成器足夠循環
    selected_gens = generators * (count // len(generators) + 1)
    random.shuffle(selected_gens)
    selected_gens = selected_gens[:count]
    
    questions = []
    seen_q_texts = set() # [關鍵] 用來檢查題目文字是否重複
    
    for gen in selected_gens:
        # 嘗試生成不重複的題目 (最多嘗試 10 次)
        for _ in range(10):
            q = gen()
            if q['q'] not in seen_q_texts:
                seen_q_texts.add(q['q'])
                # 打亂選項
                correct_opt = q['options'][q['ans']]
                random.shuffle(q['options'])
                q['ans'] = q['options'].index(correct_opt)
                questions.append(q)
                break
    return questions

def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：校驗修復版", page_icon="💯", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("💯 數學智能題庫")
    
    units = ["3-1 證明與推理", "3-2 三角形的外心、內心與重心", "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題", "全範圍總複習"]
    selected_unit = st.sidebar.selectbox("請選擇練習單元", units, on_change=reset_exam)
    st.sidebar.success("已修復所有函式對應問題，並啟用不重複題型機制！")

    st.title("💯 國中數學：考前衝刺版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info("💡 系統將隨機生成 10 題不重複的考題。")
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
                    correct_ans = q['options'][q['ans']]
                    is_correct = (user_ans == correct_ans)
                    if is_correct: score += 1
                    results.append({"q": q, "is_correct": is_correct, "user": user_ans, "correct": correct_ans})
                
                st.session_state.exam_results = {"score": score, "total": total_q, "details": results}
                st.session_state.exam_finished = True

        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            
            st.markdown("---")
            if final_score == 100: st.success("💯 滿分！太強了！")
            elif final_score >= 60: st.info("👍 及格！")
            else: st.error("💪 加油，多看詳解！")
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
                if st.button("🔄 再刷一卷 (題目不同)", use_container_width=True):
                    st.session_state.current_questions = generate_quiz(selected_unit, 10)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 選擇其他單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
