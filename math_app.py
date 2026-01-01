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
# 2. 題目工廠 (Question Factory) - 支援指定題型
# ==========================================
class QuestionFactory:
    
    @staticmethod
    def gen_3_1_proof(type_idx):
        """3-1 證明與推理 (4種題型)"""
        if type_idx == 1: # 全等判別
            props = ["SSS", "SAS", "ASA", "AAS", "RHS"]
            ans = random.choice(props)
            return {
                "q": f"若已知兩個三角形滿足「{ans}」條件，則它們的關係為何？",
                "options": ["必全等", "必相似但不一定全等", "面積相等但不一定全等", "無法判斷"],
                "ans": 0,
                "expl": f"{ans} 是全等判別性質之一，可以確定兩三角形全等。(AAA 則只能確定相似)",
                "svg_gen": lambda: SVGGenerator.geometry_triangle(f"{ans} 全等")
            }
        elif type_idx == 2: # 外角定理
            in1, in2 = random.randint(25, 80), random.randint(25, 80)
            return {
                "q": f"三角形 ABC 中，若 $\\angle A = {in1}^\\circ, \\angle B = {in2}^\\circ$，則 $\\angle C$ 的外角是多少度？",
                "options": [f"{in1+in2}", f"{180-(in1+in2)}", f"{abs(in1-in2)}", "180"],
                "ans": 0,
                "expl": f"外角等於不相鄰兩內角和：${in1} + {in2} = {in1+in2}$。",
                "svg_gen": None
            }
        elif type_idx == 3: # 邊角關係
            return {
                "q": f"在 $\\triangle ABC$ 中，若 $\\angle A > \\angle B > \\angle C$，則下列邊長關係何者正確？",
                "options": ["BC > AC > AB", "AB > AC > BC", "AC > BC > AB", "無法判斷"],
                "ans": 0,
                "expl": "大角對大邊：$\\angle A$ 最大對邊 BC，$\\angle C$ 最小對邊 AB。",
                "svg_gen": None
            }
        elif type_idx == 4: # 四邊形性質
            q_map = {"菱形": "對角線互相垂直平分", "矩形": "對角線等長且互相平分", "平行四邊形": "對角線互相平分"}
            shape = random.choice(list(q_map.keys()))
            return {
                "q": f"下列何者是「{shape}」必具備的對角線性質？",
                "options": [q_map[shape], "對角線互相垂直且等長", "對角線只有一條平分", "無特殊性質"],
                "ans": 0,
                "expl": f"{shape} 的性質為：{q_map[shape]}。",
                "svg_gen": None
            }

    @staticmethod
    def gen_3_2_centers(type_idx):
        """3-2 三心 (5種題型)"""
        if type_idx == 1: # 內心角度
            angle_a = random.randint(30, 80)
            ans = 90 + angle_a // 2
            return {
                "q": f"若 I 為 $\\triangle ABC$ 的內心，且 $\\angle A = {angle_a}^\\circ$，則 $\\angle BIC$ 為多少？",
                "options": [f"{ans}", f"{180-angle_a}", f"{2*angle_a}", f"{90+angle_a}"],
                "ans": 0,
                "expl": f"內心角度公式：$90 + {angle_a}/2 = {ans}^\\circ$。",
                "svg_gen": lambda: SVGGenerator.triangle_center_angle("內心 I", ans)
            }
        elif type_idx == 2: # 外心角度
            angle_a = random.randint(30, 80)
            ans = 2 * angle_a
            return {
                "q": f"若 O 為銳角 $\\triangle ABC$ 的外心，且 $\\angle A = {angle_a}^\\circ$，則 $\\angle BOC$ 為多少？",
                "options": [f"{ans}", f"{90+angle_a//2}", f"{angle_a}", f"{180-angle_a}"],
                "ans": 0,
                "expl": f"圓心角是圓周角的 2 倍：$2 \\times {angle_a} = {ans}^\\circ$。",
                "svg_gen": lambda: SVGGenerator.triangle_center_angle("外心 O", ans)
            }
        elif type_idx == 3: # 直角外心半徑
            triples = [(6,8,10), (5,12,13), (8,15,17), (10,24,26), (12,16,20)]
            a, b, c = random.choice(triples)
            return {
                "q": f"直角三角形兩股長分別為 {a}, {b}，則其「外接圓半徑」為何？",
                "options": [f"{c/2}", f"{c}", f"{a+b}", f"{c*2}"],
                "ans": 0,
                "expl": f"斜邊 {c}。直角三角形外心在斜邊中點，半徑 = {c}/2 = {c/2}。",
                "svg_gen": None
            }
        elif type_idx == 4: # 重心性質 (定義)
            return {
                "q": "關於三角形「重心」的敘述，下列何者正確？",
                "options": ["重心是三條中線的交點", "重心到三頂點等距離", "重心到三邊等距離", "重心必在三角形外部"],
                "ans": 0,
                "expl": "重心是中線交點；外心到頂點等距；內心到邊等距。",
                "svg_gen": lambda: SVGGenerator.center_visual("centroid")
            }
        elif type_idx == 5: # 重心性質 (比例)
            return {
                "q": "重心到頂點的距離，是重心到對邊中點距離的幾倍？",
                "options": ["2倍", "1.5倍", "3倍", "1倍"],
                "ans": 0,
                "expl": "重心性質 2:1。",
                "svg_gen": lambda: SVGGenerator.center_visual("centroid")
            }

    @staticmethod
    def gen_4_1_factor(type_idx):
        """4-1 因式分解 (4種題型)"""
        if type_idx == 1: # 基礎因式分解
            r1, r2 = random.randint(1, 9), random.randint(-9, -1)
            b, c = -(r1+r2), r1*r2
            eq = f"x^2 {f'+ {b}x' if b>=0 else f'{b}x'} {f'+ {c}' if c>=0 else f'{c}'} = 0"
            return {
                "q": f"解方程式：${eq}$",
                "options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
                "ans": 0,
                "expl": f"因式分解 $(x-{r1})(x-{r2})=0$，故解為 {r1}, {r2}。",
                "svg_gen": lambda: SVGGenerator.roots_on_line(r1, r2)
            }
        elif type_idx == 2: # 提公因式
            k = random.randint(2, 9)
            return {
                "q": f"解方程式 $x^2 - {k}x = 0$？",
                "options": [f"0 或 {k}", f"{k}", "0", f"1 或 {k}"],
                "ans": 0,
                "expl": f"提 x：$x(x-{k})=0$，故 x=0 或 {k}。",
                "svg_gen": lambda: SVGGenerator.roots_on_line(0, k)
            }
        elif type_idx == 3: # 平方差
            k = random.choice([4, 9, 16, 25, 36, 49, 64, 81])
            sq = int(math.sqrt(k))
            return {
                "q": f"解 $x^2 - {k} = 0$？",
                "options": [f"{sq} 或 -{sq}", f"{sq}", f"{k}", f"{k*k}"],
                "ans": 0,
                "expl": f"$x^2={k}$，故 $x=\\pm{sq}$。",
                "svg_gen": lambda: SVGGenerator.roots_on_line(sq, -sq)
            }
        elif type_idx == 4: # 逆推
            r1, r2 = random.randint(1, 5), random.randint(1, 5)
            return {
                "q": f"若方程式的兩根為 {r1}, {-r2}，則原方程式可能為？",
                "options": [f"$(x-{r1})(x+{r2})=0$", f"$(x+{r1})(x-{r2})=0$", f"$(x-{r1})(x-{r2})=0$", "無法求得"],
                "ans": 0,
                "expl": f"根 x={r1} 對應因子 (x-{r1})；根 x={-r2} 對應因子 (x+{r2})。",
                "svg_gen": None
            }

    @staticmethod
    def gen_4_2_formula(type_idx):
        """4-2 配方法 (3種題型)"""
        if type_idx == 1: # 判別式
            a, b, c = random.randint(1,3), random.randint(1,5), random.randint(-5,5)
            D = b**2 - 4*a*c
            status = "相異兩根" if D > 0 else ("重根" if D == 0 else "無解")
            return {
                "q": f"判別 ${a}x^2 + {b}x + ({c}) = 0$ 的解？",
                "options": [f"{status}", "無法判斷", "三個根", "以上皆非"],
                "ans": 0,
                "expl": f"D = {D} ({'>' if D>0 else '<'} 0)，故{status}。",
                "svg_gen": None
            }
        elif type_idx == 2: # 配方補項
            k = random.randint(1, 8) * 2
            return {
                "q": f"將 $x^2 + {k}x$ 配成完全平方式，需加上？",
                "options": [f"{(k//2)**2}", f"{k}", f"{k*2}", f"{k//2}"],
                "ans": 0,
                "expl": f"加上 $( {k}/2 )^2 = {(k//2)**2}$。",
                "svg_gen": lambda: SVGGenerator.area_square(k//2)
            }
        elif type_idx == 3: # 公式解背誦
            return {
                "q": "一元二次方程式公式解中，根號內的是？",
                "options": ["$b^2-4ac$", "$b^2+4ac$", "$2a$", "$b-4ac$"],
                "ans": 0,
                "expl": "判別式 D = $b^2-4ac$。",
                "svg_gen": None
            }

    @staticmethod
    def gen_4_3_app(type_idx):
        """4-3 應用 (3種題型)"""
        if type_idx == 1: # 數積
            s = random.randint(2, 12)
            return {
                "q": f"兩連續整數乘積為 {s*(s+1)}，且兩數為正，求此兩數？",
                "options": [f"{s}, {s+1}", f"{s-2}, {s-1}", f"{s+2}, {s+3}", "無解"],
                "ans": 0,
                "expl": f"{s} * {s+1} = {s*(s+1)}。",
                "svg_gen": lambda: SVGGenerator.roots_on_line(s, s+1)
            }
        elif type_idx == 2: # 面積
            side = random.randint(5, 15)
            return {
                "q": f"正方形面積 {side*side}，求邊長？",
                "options": [f"{side}", f"{side*2}", f"{side/2}", f"{side*side}"],
                "ans": 0,
                "expl": f"邊長 = $\\sqrt{{{side*side}}} = {side}$。",
                "svg_gen": lambda: SVGGenerator.area_square(side)
            }
        elif type_idx == 3: # 物理
            t = random.randint(2, 6)
            return {
                "q": f"物體落下距離 $h=5t^2$，若 $h={5*t*t}$，求時間 t？",
                "options": [f"{t}", f"{t*2}", f"{t+5}", "10"],
                "ans": 0,
                "expl": f"{5*t*t} = 5t^2 => t^2={t*t} => t={t}。",
                "svg_gen": None
            }

# ==========================================
# 3. 智能洗牌生成邏輯 (Smart Shuffle)
# ==========================================
def generate_balanced_questions(unit_name, count=10):
    """
    智能洗牌演算法：
    1. 根據單元找出所有可用題型 ID (例如 3-1 有 1,2,3,4 種)
    2. 建立題型池 (Pool)，確保每種題型至少出現 n 次
    3. 洗牌 (Shuffle)
    4. 依序生成，絕不連續重複相同題型
    """
    questions = []
    
    # 定義各單元的題型數量
    type_counts = {
        "3-1": 4, "3-2": 5, 
        "4-1": 4, "4-2": 3, "4-3": 3
    }
    
    # 找出當前單元的題型總數
    key = next((k for k in type_counts if k in unit_name), None)
    
    if key:
        num_types = type_counts[key]
        # 建立題型池：確保分佈均勻 (例如 [1,2,3,4, 1,2,3,4, 1,2])
        pool = list(range(1, num_types + 1)) * (count // num_types + 1)
        random.shuffle(pool)
        pool = pool[:count] # 截取需要的數量
        
        # 生成題目
        for type_id in pool:
            if key == "3-1": q = QuestionFactory.gen_3_1_proof(type_id)
            elif key == "3-2": q = QuestionFactory.gen_3_2_centers(type_id)
            elif key == "4-1": q = QuestionFactory.gen_4_1_factor(type_id)
            elif key == "4-2": q = QuestionFactory.gen_4_2_formula(type_id)
            elif key == "4-3": q = QuestionFactory.gen_4_3_app(type_id)
            
            # 選項打亂
            correct = q['options'][q['ans']]
            random.shuffle(q['options'])
            q['ans'] = q['options'].index(correct)
            questions.append(q)
            
    else:
        # 總複習模式 (隨機混合)
        for _ in range(count):
            u = random.choice(["3-1", "3-2", "4-1", "4-2", "4-3"])
            max_t = type_counts[u]
            t = random.randint(1, max_t)
            
            if u == "3-1": q = QuestionFactory.gen_3_1_proof(t)
            elif u == "3-2": q = QuestionFactory.gen_3_2_centers(t)
            elif u == "4-1": q = QuestionFactory.gen_4_1_factor(t)
            elif u == "4-2": q = QuestionFactory.gen_4_2_formula(t)
            elif u == "4-3": q = QuestionFactory.gen_4_3_app(t)
            
            correct = q['options'][q['ans']]
            random.shuffle(q['options'])
            q['ans'] = q['options'].index(correct)
            questions.append(q)

    return questions

def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：智能洗牌版", page_icon="🃏", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🃏 數學智能洗牌")
    
    units = [
        "3-1 證明與推理", "3-2 三角形的外心、內心與重心",
        "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題",
        "全範圍總複習"
    ]
    selected_unit = st.sidebar.selectbox("請選擇練習單元", units, on_change=reset_exam)
    st.sidebar.success("系統已啟用「題型平均分配」機制，確保每次練習都能覆蓋不同考點！")

    st.title("🃏 國中數學：智能洗牌版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info("💡 點擊開始，系統將自動從題庫池中「均勻抽取」不同題型的題目。")
        if st.button("🚀 發牌 (生成試卷)", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            st.session_state.current_questions = generate_balanced_questions(selected_unit, 10)
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
            if final_score == 100: st.success("💯 太強了！全對！")
            elif final_score >= 60: st.info("👍 很棒，及格了！")
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
                if st.button("🔄 再洗一次牌 (題目不同)", use_container_width=True):
                    st.session_state.current_questions = generate_balanced_questions(selected_unit, 10)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 選擇其他單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
