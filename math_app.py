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
            return SVGGenerator._base_svg("""<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><line x1="150" y1="30" x2="150" y2="170" stroke="red" stroke-dasharray="4"/><line x1="50" y1="170" x2="200" y2="100" stroke="red" stroke-dasharray="4"/><circle cx="150" cy="123" r="4" fill="blue"/><text x="160" y="123" fill="blue" font-weight="bold">重心</text>""", 300, 200)
        elif type == "circumcenter":
            return SVGGenerator._base_svg("""<circle cx="150" cy="100" r="80" fill="none" stroke="green"/><polygon points="150,20 80,140 220,140" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="115" fill="green" font-weight="bold">外心</text>""", 300, 200)
        elif type == "incenter":
            return SVGGenerator._base_svg("""<polygon points="150,20 50,170 250,170" fill="none" stroke="black"/><circle cx="150" cy="120" r="50" fill="none" stroke="orange"/><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange" font-weight="bold">內心</text>""", 300, 200)

    @staticmethod
    def geometry_sas():
        return SVGGenerator._base_svg("""
            <path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text>
            <path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text>
            <text x="115" y="80" text-anchor="middle" font-weight="bold" fill="blue">全等?</text>
        """, 300, 150)

# ==========================================
# 2. 題目工廠 (QGen) - 補齊所有題型
# ==========================================
class QGen:
    # ---------------- 3-1 證明與推理 ----------------
    # [觀念題]
    @staticmethod
    def q31_concept_congruence():
        props = ["SSS", "SAS", "ASA", "AAS", "RHS"]
        ans = random.choice(props)
        return {"q": f"判別性質：若兩個三角形符合「{ans}」對應相等，則下列敘述何者正確？", "options": ["必全等", "必相似但不全等", "面積相等但形狀不同", "無法判斷"], "ans": 0, "expl": f"{ans} 為全等判別性質。", "svg_gen": lambda: SVGGenerator.geometry_sas()}

    @staticmethod
    def q31_concept_quad():
        q_map = {"菱形": "對角線互相垂直平分", "矩形": "對角線等長且互相平分", "平行四邊形": "對角線互相平分"}
        shape = random.choice(list(q_map.keys()))
        return {"q": f"關於「{shape}」的對角線性質，下列何者正確？", "options": [q_map[shape], "對角線只有一條平分", "對角線無特殊性質", "以上皆非"], "ans": 0, "expl": f"{shape} 性質：{q_map[shape]}。", "svg_gen": None}

    # [一般計算題]
    @staticmethod
    def q31_calc_angle():
        in1, in2 = random.randint(30, 80), random.randint(30, 80)
        return {"q": f"$\\triangle ABC$ 中，$\\angle A={in1}^\\circ, \\angle B={in2}^\\circ$，求 $\\angle C$ 的外角？", "options": [f"{in1+in2}", f"{180-(in1+in2)}", "180", "90"], "ans": 0, "expl": f"外角 = 兩內對角和：{in1}+{in2}={in1+in2}。", "svg_gen": None}

    @staticmethod
    def q31_calc_isosceles():
        deg = random.choice([40, 50, 70])
        ans = (180 - deg) // 2
        return {"q": f"等腰三角形頂角為 {deg} 度，求其底角？", "options": [f"{ans}", f"{deg}", f"{180-deg}", "60"], "ans": 0, "expl": f"(180-{deg})/2 = {ans}", "svg_gen": None}

    # [情境題]
    @staticmethod
    def q31_story_bridge():
        return {"q": "工程師設計大橋結構時，常利用三角形的哪種全等性質來確保結構穩固不變形 (三邊長固定則形狀固定)？", "options": ["SSS", "AAA", "SSA", "以上皆非"], "ans": 0, "expl": "SSS 性質確保了三角形結構的唯一性與穩定性。", "svg_gen": lambda: SVGGenerator.geometry_sas()}

    # ---------------- 3-2 三心 (完整補齊) ----------------
    # [觀念題]
    @staticmethod
    def q32_concept_def():
        q_list = [("三中線交點", "重心"), ("三中垂線交點", "外心"), ("三內角平分線交點", "內心")]
        q, a = random.choice(q_list)
        return {"q": f"三角形的「{q}」稱為？", "options": [a, "重心" if a!="重心" else "外心", "內心" if a!="內心" else "垂心", "旁心"], "ans": 0, "expl": "基本定義。", "svg_gen": None}

    @staticmethod
    def q32_concept_position():
        return {"q": "關於「鈍角三角形」的外心位置，下列何者正確？", "options": ["在三角形外部", "在三角形內部", "在邊上", "在頂點"], "ans": 0, "expl": "銳角在內，直角在邊，鈍角在外。", "svg_gen": None}

    @staticmethod
    def q32_concept_equilateral():
        return {"q": "哪一種三角形的重心、外心、內心會重合在同一點？", "options": ["正三角形", "等腰三角形", "直角三角形", "任意三角形"], "ans": 0, "expl": "正三角形性質：三心合一。", "svg_gen": None}

    # [一般計算題]
    @staticmethod
    def q32_calc_centroid_len():
        median = random.choice([12, 18, 24, 30])
        ag = int(median * 2/3)
        return {"q": f"$\\triangle ABC$ 中線 AD 長 {median}，G 為重心，求 $\\overline{{AG}}$？", "options": [f"{ag}", f"{median/3}", f"{median/2}", f"{median}"], "ans": 0, "expl": f"重心分中線 2:1，AG佔 2/3。{median}*2/3={ag}。", "svg_gen": lambda: SVGGenerator.triangle_centroid_len(median)}

    @staticmethod
    def q32_calc_incenter_angle():
        angle = random.randint(40, 80)
        ans = 90 + angle // 2
        return {"q": f"I 為內心，$\\angle A = {angle}^\\circ$，求 $\\angle BIC$？", "options": [f"{ans}", f"{180-angle}", f"{90+angle}", f"{2*angle}"], "ans": 0, "expl": f"公式：$90 + A/2 = {ans}$。", "svg_gen": lambda: SVGGenerator.triangle_center_angle("內心 I", ans)}

    @staticmethod
    def q32_calc_circum_radius():
        triples = [(6,8,10), (5,12,13), (8,15,17)]
        a, b, c = random.choice(triples)
        return {"q": f"直角三角形兩股 {a}, {b}，求外接圓半徑？", "options": [f"{c/2}", f"{c}", f"{a+b}", f"{c*2}"], "ans": 0, "expl": f"斜邊 {c}，外心在斜邊中點，半徑 {c/2}。", "svg_gen": None}

    @staticmethod
    def q32_calc_inradius_right():
        # [補回] 內切圓半徑計算
        triples = [(3,4,5), (5,12,13), (8,15,17)]
        a, b, c = random.choice(triples)
        r = int((a + b - c) / 2)
        return {"q": f"直角三角形兩股 {a}, {b}，求內切圓半徑？", "options": [f"{r}", f"{r+1}", f"{c/2}", f"{c}"], "ans": 0, "expl": f"直角三角形內半徑 = (兩股和-斜邊)/2 = ({a}+{b}-{c})/2 = {r}。", "svg_gen": None}

    # [情境題]
    @staticmethod
    def q32_story_firestation():
        return {"q": "三個村莊 A, B, C 想要蓋一座消防局，且消防局到三個村莊的直線距離要相等。請問工程師應選在哪一點？", "options": ["外心", "內心", "重心", "垂心"], "ans": 0, "expl": "到三頂點等距 => 外心。", "svg_gen": lambda: SVGGenerator.center_visual("circumcenter")}

    @staticmethod
    def q32_story_balance():
        return {"q": "美術課剪了一個三角形紙板，小明想用指尖頂住紙板讓它保持平衡不掉落，他該頂在哪裡？", "options": ["重心", "外心", "內心", "頂點"], "ans": 0, "expl": "重心是物理上的重量中心。", "svg_gen": lambda: SVGGenerator.center_visual("centroid")}

    # ---------------- 4-1 因式分解法 (完整補齊) ----------------
    # [觀念題]
    @staticmethod
    def q41_concept_root_meaning():
        k = random.randint(1, 5)
        return {"q": f"若 $x={k}$ 是方程式 $x^2+ax+b=0$ 的根，則下列何者必成立？", "options": [f"將 {k} 代入方程式會等於 0", f"將 -{k} 代入方程式會等於 0", "a 必為正數", "b 必為負數"], "ans": 0, "expl": "根的定義：代入使等號成立。", "svg_gen": None}

    @staticmethod
    def q41_concept_reverse_roots():
        return {"q": "若一元二次方程式的兩根互為相反數 (如 3, -3)，則該方程式缺哪一項？", "options": ["一次項 (x項)", "常數項", "二次項", "無法判斷"], "ans": 0, "expl": "兩根和為0，故一次項係數為0。", "svg_gen": None}

    # [一般計算題]
    @staticmethod
    def q41_calc_solve_basic():
        r1, r2 = random.randint(1,5), random.randint(-5,-1)
        return {"q": f"解方程式 $(x-{r1})(x-{r2})=0$？", "options": [f"{r1}, {r2}", f"{-r1}, {-r2}", f"{r1}, {-r2}", "無解"], "ans": 0, "expl": f"x={r1} 或 x={r2}。", "svg_gen": lambda: SVGGenerator.roots_on_line(r1, r2)}

    @staticmethod
    def q41_calc_solve_sq():
        k = random.choice([9, 16, 25, 36])
        sq = int(math.sqrt(k))
        return {"q": f"解 $x^2 - {k} = 0$？", "options": [f"±{sq}", f"{sq}", f"{k}", "無解"], "ans": 0, "expl": f"$x^2={k} \\Rightarrow x=\\pm{sq}$。", "svg_gen": lambda: SVGGenerator.roots_on_line(sq, -sq)}

    @staticmethod
    def q41_calc_find_k():
        k = random.randint(2, 5)
        r_val = -k
        return {"q": f"若 $x={r_val}$ 是方程式 $x^2 + kx = 0$ 的一根，則 k 值為何？", "options": [f"{k}", f"-{k}", "0", "1"], "ans": 0, "expl": f"代入求得 k={k}。", "svg_gen": None}

    # [情境題]
    @staticmethod
    def q41_story_number():
        r1, r2 = 3, -2
        return {"q": "小華心裡想兩個數，其中一個減 3，另一個加 2，兩者相乘剛好是 0。請問這兩個數可能是？", "options": ["3 或 -2", "-3 或 2", "3 或 2", "0"], "ans": 0, "expl": "$(x-3)(x+2)=0$。", "svg_gen": None}

    # ---------------- 4-2 配方法 (觀念+計算) ----------------
    # [觀念題]
    @staticmethod
    def q42_concept_discriminant():
        return {"q": "若一元二次方程式的判別式 $D < 0$，代表圖形與 x 軸的關係？", "options": ["沒有交點", "交於兩點", "切於一點", "重合"], "ans": 0, "expl": "D<0 無實根，圖形懸空不相交。", "svg_gen": None}

    @staticmethod
    def q42_concept_formula_def():
        return {"q": "一元二次方程式公式解中，根號內的是？", "options": ["$b^2-4ac$", "$b^2+4ac$", "$2a$", "$b-4ac$"], "ans": 0, "expl": "判別式 D = $b^2-4ac$。", "svg_gen": None}

    # [一般計算題]
    @staticmethod
    def q42_calc_discriminant_val():
        return {"q": "求 $x^2 + 4x + 1 = 0$ 的判別式 D？", "options": ["12", "16", "0", "-4"], "ans": 0, "expl": "$D = 4^2 - 4(1)(1) = 12$。", "svg_gen": None}

    @staticmethod
    def q42_calc_complete_sq():
        k = 6
        return {"q": "將 $x^2 + 6x$ 配方需加上多少？", "options": ["9", "36", "3", "6"], "ans": 0, "expl": "$(6/2)^2 = 9$。", "svg_gen": lambda: SVGGenerator.area_square(3)}

    # [情境題]
    @staticmethod
    def q42_story_path():
        return {"q": "棒球飛行的軌跡是一個二次函數，若判別式 D > 0，代表球的高度與某個水平線有幾個交點？", "options": ["2個", "1個", "0個", "無限多"], "ans": 0, "expl": "D>0 代表有兩個相異實根（交點）。", "svg_gen": None}

    # ---------------- 4-3 應用問題 ----------------
    # [觀念題]
    @staticmethod
    def q43_concept_setup():
        return {"q": "解應用問題時，若算出邊長為 -5，應該如何處理？", "options": ["不合 (邊長需為正)", "取絕對值", "直接當作答案", "重算"], "ans": 0, "expl": "幾何長度必須大於 0。", "svg_gen": None}

    # [一般計算題]
    @staticmethod
    def q43_calc_number():
        return {"q": "某數 x 的平方等於 3x，求 x？", "options": ["0 或 3", "3", "0", "9"], "ans": 0, "expl": "$x^2=3x \\Rightarrow x(x-3)=0$。", "svg_gen": lambda: SVGGenerator.roots_on_line(0, 3)}

    # [情境題]
    @staticmethod
    def q43_story_garden():
        side = random.randint(5, 12)
        area = side*side
        return {"q": f"王老先生有一塊正方形花圃，面積 {area} 平方公尺。他想在四周圍籬笆，請問邊長是幾公尺？", "options": [f"{side}", f"{area/2}", f"{side*2}", f"{area}"], "ans": 0, "expl": f"$x^2={area} \\Rightarrow x={side}$。", "svg_gen": lambda: SVGGenerator.area_square(side)}

    @staticmethod
    def q43_story_physics():
        t = 3
        h = 5 * t * t
        return {"q": f"物體落下距離 $h=5t^2$。若落下 {h} 公尺，需時幾秒？", "options": [f"{t}", "5", "9", "25"], "ans": 0, "expl": f"{h}=5t² => t²=9 => t=3。", "svg_gen": None}

# ==========================================
# 3. 智能組卷邏輯 (Router)
# ==========================================
def get_generators_for_unit(unit_name):
    """
    分類混合：
    Concept (觀念), Calculation (計算), Story (情境)
    """
    if "3-1" in unit_name:
        return [QGen.q31_concept_congruence, QGen.q31_concept_quad, 
                QGen.q31_calc_angle, QGen.q31_calc_isosceles, 
                QGen.q31_story_bridge]
    elif "3-2" in unit_name:
        return [QGen.q32_concept_def, QGen.q32_concept_position, QGen.q32_concept_equilateral,
                QGen.q32_calc_centroid_len, QGen.q32_calc_incenter_angle, QGen.q32_calc_circum_radius, QGen.q32_calc_inradius_right,
                QGen.q32_story_firestation, QGen.q32_story_balance]
    elif "4-1" in unit_name:
        return [QGen.q41_concept_root_meaning, QGen.q41_concept_reverse_roots,
                QGen.q41_calc_solve_basic, QGen.q41_calc_solve_sq, QGen.q41_calc_find_k,
                QGen.q41_story_number]
    elif "4-2" in unit_name:
        return [QGen.q42_concept_discriminant, QGen.q42_concept_formula_def,
                QGen.q42_calc_discriminant_val, QGen.q42_calc_complete_sq,
                QGen.q42_story_path]
    elif "4-3" in unit_name:
        return [QGen.q43_concept_setup,
                QGen.q43_calc_number,
                QGen.q43_story_garden, QGen.q43_story_physics]
    else: # 總複習
        all_funcs = []
        # 混合抽樣
        all_funcs.extend([QGen.q32_story_firestation, QGen.q43_story_garden, QGen.q31_calc_angle, QGen.q41_calc_solve_basic])
        return all_funcs

def generate_quiz(unit_name, count=10):
    generators = get_generators_for_unit(unit_name)
    
    # 題型循環填充
    selected_gens = generators * (count // len(generators) + 1)
    random.shuffle(selected_gens)
    selected_gens = selected_gens[:count]
    
    questions = []
    seen_q_texts = set()
    
    for gen in selected_gens:
        for _ in range(10): # 嘗試生成不重複
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
    st.set_page_config(page_title="國中數學：全題型混合版", page_icon="💯", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("💯 數學智能題庫")
    
    units = ["3-1 證明與推理", "3-2 三角形的外心、內心與重心", "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題", "全範圍總複習"]
    selected_unit = st.sidebar.selectbox("請選擇練習單元", units, on_change=reset_exam)
    st.sidebar.success("已包含：\n1. 觀念題 (定義/判別)\n2. 計算題 (基礎運算)\n3. 情境題 (生活應用)")

    st.title("💯 國中數學：全方位練習版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info("💡 系統將混合生成「觀念、計算、情境」三種題型。")
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
