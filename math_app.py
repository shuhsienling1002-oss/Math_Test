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
        """生成幾何示意圖"""
        return SVGGenerator._base_svg(f"""
            <path d="M50,150 L250,150 L150,20 Z" fill="#e3f2fd" stroke="blue" stroke-width="2"/>
            <text x="150" y="180" text-anchor="middle" font-weight="bold" fill="black">{type_label}</text>
        """, 300, 200)

    @staticmethod
    def triangle_center_angle(angle_type, angle_val):
        """生成三心角度示意圖"""
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
        """數線顯示根"""
        # 簡單映射，避免超出範圍
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
        """正方形面積圖"""
        return SVGGenerator._base_svg(f"""
            <rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/>
            <text x="150" y="100" text-anchor="middle" font-weight="bold">面積 = {side*side}</text>
            <text x="150" y="170" text-anchor="middle">邊長 = ?</text>
        """, 300, 200)

# ==========================================
# 2. 無限題庫生成器 (Question Factory)
# 這才是 AI 該做的事：用程式碼生成無限題目
# ==========================================
class QuestionFactory:
    
    @staticmethod
    def gen_3_1_proof():
        """生成 3-1 證明與推理題目"""
        type_idx = random.randint(1, 4)
        if type_idx == 1:
            # 全等性質判別
            props = ["SSS", "SAS", "ASA", "AAS", "RHS"]
            ans = random.choice(props)
            wrong = "AAA" if ans != "AAA" else "SSA"
            return {
                "q": f"若已知兩個三角形滿足「{ans}」條件，則它們的關係為何？",
                "options": ["必全等", "必相似但不一定全等", "面積相等但不一定全等", "無法判斷"],
                "ans": 0,
                "expl": f"{ans} 是全等判別性質之一，可以確定兩三角形全等。(AAA 則只能確定相似)",
                "svg_gen": lambda: SVGGenerator.geometry_triangle(f"{ans} 全等")
            }
        elif type_idx == 2:
            # 角度計算 (外角定理)
            in1 = random.randint(30, 80)
            in2 = random.randint(30, 80)
            ext = in1 + in2
            return {
                "q": f"三角形 ABC 中，若 $\\angle A = {in1}^\\circ, \\angle B = {in2}^\\circ$，則 $\\angle C$ 的外角是多少度？",
                "options": [f"{ext}", f"{180-ext}", f"{abs(in1-in2)}", "180"],
                "ans": 0,
                "expl": f"根據外角定理，外角等於不相鄰兩內角和：${in1} + {in2} = {ext}$。",
                "svg_gen": None
            }
        elif type_idx == 3:
            # 邊角關係
            sides = ["AB", "BC", "AC"]
            random.shuffle(sides)
            return {
                "q": f"在 $\\triangle ABC$ 中，若 $\\angle A > \\angle B > \\angle C$，則下列邊長關係何者正確？",
                "options": ["BC > AC > AB", "AB > AC > BC", "AC > BC > AB", "無法判斷"],
                "ans": 0,
                "expl": "大角對大邊：$\\angle A$ 最大對邊 BC，$\\angle C$ 最小對邊 AB。",
                "svg_gen": None
            }
        else:
            # 特殊四邊形
            q_map = {
                "菱形": "對角線互相垂直平分",
                "矩形": "對角線等長且互相平分",
                "平行四邊形": "對角線互相平分",
                "箏形": "對角線互相垂直"
            }
            shape = random.choice(list(q_map.keys()))
            return {
                "q": f"下列何者是「{shape}」必具備的對角線性質？",
                "options": [q_map[shape], "對角線互相垂直且等長", "對角線只有一條平分", "無特殊性質"],
                "ans": 0,
                "expl": f"{shape} 的性質為：{q_map[shape]}。",
                "svg_gen": None
            }

    @staticmethod
    def gen_3_2_centers():
        """生成 3-2 三心題目 (動態數字)"""
        type_idx = random.randint(1, 4)
        if type_idx == 1:
            # 內心角度公式 90 + A/2
            angle_a = random.choice([40, 50, 60, 70, 80])
            ans_angle = 90 + angle_a // 2
            return {
                "q": f"若 I 為 $\\triangle ABC$ 的內心，且 $\\angle A = {angle_a}^\\circ$，則 $\\angle BIC$ 為多少度？",
                "options": [f"{ans_angle}", f"{180-angle_a}", f"{2*angle_a}", f"{90+angle_a}"],
                "ans": 0,
                "expl": f"內心角度公式：$\\angle BIC = 90^\\circ + \\frac{{1}}{{2}}\\angle A = 90 + {angle_a//2} = {ans_angle}^\\circ$。",
                "svg_gen": lambda: SVGGenerator.triangle_center_angle("內心 I", ans_angle)
            }
        elif type_idx == 2:
            # 外心角度公式 (銳角 2A, 鈍角 360-2A) - 這裡簡化考銳角
            angle_a = random.choice([40, 50, 60, 70])
            ans_angle = 2 * angle_a
            return {
                "q": f"若 O 為銳角 $\\triangle ABC$ 的外心，且 $\\angle A = {angle_a}^\\circ$，則 $\\angle BOC$ 為多少度？",
                "options": [f"{ans_angle}", f"{90+angle_a//2}", f"{angle_a}", f"{180-angle_a}"],
                "ans": 0,
                "expl": f"外心角度 (圓心角) 是圓周角的 2 倍：$2 \\times {angle_a} = {ans_angle}^\\circ$。",
                "svg_gen": lambda: SVGGenerator.triangle_center_angle("外心 O", ans_angle)
            }
        elif type_idx == 3:
            # 直角三角形外接圓半徑 (斜邊一半)
            # 生成畢氏數
            triples = [(3,4,5), (6,8,10), (5,12,13), (8,15,17), (10,24,26)]
            a, b, c = random.choice(triples)
            R = c / 2
            return {
                "q": f"直角三角形兩股長分別為 {a}, {b}，則其「外接圓半徑」為何？",
                "options": [f"{R}", f"{c}", f"{a+b}", f"{c*2}"],
                "ans": 0,
                "expl": f"斜邊 $c = \\sqrt{{{a}^2+{b}^2}} = {c}$。直角三角形外心在斜邊中點，故半徑 $R = {c}/2 = {R}$。",
                "svg_gen": None
            }
        else:
            # 重心性質
            return {
                "q": "關於三角形「重心」的敘述，下列何者正確？",
                "options": ["重心是三條中線的交點", "重心到三頂點等距離", "重心到三邊等距離", "重心必在三角形外部"],
                "ans": 0,
                "expl": "重心是中線交點；外心才到頂點等距；內心才到邊等距。",
                "svg_gen": lambda: SVGGenerator.geometry_triangle("重心 G")
            }

    @staticmethod
    def gen_4_1_factor():
        """生成 4-1 因式分解法解方程式"""
        # 生成 (x-a)(x-b)=0
        r1 = random.randint(-9, 9)
        r2 = random.randint(-9, 9)
        # 展開係數
        b = -(r1 + r2)
        c = r1 * r2
        
        # 格式化方程式字串
        eq_str = f"x^2 "
        eq_str += f"+ {b}x " if b >= 0 else f"{b}x "
        eq_str += f"+ {c} = 0" if c >= 0 else f"{c} = 0"
        
        return {
            "q": f"解一元二次方程式：${eq_str}$",
            "options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
            "ans": 0,
            "expl": f"因式分解為 $(x - ({r1}))(x - ({r2})) = 0$，故 $x = {r1}$ 或 $x = {r2}$。",
            "svg_gen": lambda: SVGGenerator.roots_on_line(r1, r2)
        }

    @staticmethod
    def gen_4_2_formula():
        """生成 4-2 配方法與判別式"""
        type_idx = random.randint(1, 3)
        if type_idx == 1:
            # 判別式計算
            a = random.randint(1, 3)
            b = random.randint(1, 8)
            c = random.randint(-5, 5)
            D = b**2 - 4*a*c
            status = "相異兩根" if D > 0 else ("重根" if D == 0 else "無解")
            
            return {
                "q": f"判別方程式 ${a}x^2 + {b}x + ({c}) = 0$ 的解的情形？",
                "options": [f"{status}", "無法判斷", "以上皆非", "三個根"],
                "ans": 0,
                "expl": f"判別式 $D = b^2 - 4ac = {b}^2 - 4({a})({c}) = {D}$。因為 $D {'>' if D>0 else ('=' if D==0 else '<')} 0$，故為{status}。",
                "svg_gen": None
            }
        else:
            # 配方法補項
            k = random.randint(2, 10) * 2 # 偶數方便除2
            term = (k // 2) ** 2
            return {
                "q": f"若要將 $x^2 + {k}x$ 配成完全平方式，需要加上多少？",
                "options": [f"{term}", f"{k}", f"{k*2}", f"{term//2}"],
                "ans": 0,
                "expl": f"配方公式：加上 $(\\frac{{一次項係數}}{{2}})^2$，即 $(\\frac{{{k}}}{{2}})^2 = {k//2}^2 = {term}$。",
                "svg_gen": lambda: SVGGenerator.area_square(k//2) # 示意
            }

    @staticmethod
    def gen_4_3_app():
        """生成 4-3 應用問題"""
        type_idx = random.randint(1, 2)
        if type_idx == 1:
            # 兩數積
            s = random.randint(2, 10)
            l = s + 2
            prod = s * l
            return {
                "q": f"兩連續偶數的乘積為 {prod}，且兩數皆為正數，求此兩數？",
                "options": [f"{s}, {l}", f"{s-2}, {l-2}", f"{s+2}, {l+2}", "無解"],
                "ans": 0,
                "expl": f"設小數為 x，則 $x(x+2)={prod}$。直接驗算：${s} \\times {l} = {prod}$。",
                "svg_gen": lambda: SVGGenerator.roots_on_line(s, l)
            }
        else:
            # 正方形面積
            side = random.randint(5, 15)
            area = side * side
            return {
                "q": f"一個正方形的面積為 {area}，求其邊長？",
                "options": [f"{side}", f"{side*2}", f"{side/2}", f"{area/2}"],
                "ans": 0,
                "expl": f"$x^2 = {area} \\Rightarrow x = \\sqrt{{{area}}} = {side}$。",
                "svg_gen": lambda: SVGGenerator.area_square(side)
            }

# ==========================================
# 3. APP 主程式邏輯
# ==========================================
def generate_quiz_questions(unit_name, count=10):
    """根據單元名稱，動態生成指定數量的題目"""
    questions = []
    
    # 根據單元路由到對應的生成器
    for _ in range(count):
        if "3-1" in unit_name:
            q = QuestionFactory.gen_3_1_proof()
        elif "3-2" in unit_name:
            q = QuestionFactory.gen_3_2_centers()
        elif "4-1" in unit_name:
            q = QuestionFactory.gen_4_1_factor()
        elif "4-2" in unit_name:
            q = QuestionFactory.gen_4_2_formula()
        elif "4-3" in unit_name:
            q = QuestionFactory.gen_4_3_app()
        else:
            # 默認混合出題 (給總複習用)
            funcs = [QuestionFactory.gen_3_1_proof, QuestionFactory.gen_3_2_centers, 
                     QuestionFactory.gen_4_1_factor, QuestionFactory.gen_4_2_formula]
            q = random.choice(funcs)()
            
        # 打亂選項順序 (除了最後一個選項如'以上皆非'通常保留，這裡簡單全亂)
        # 為了能追蹤答案，需要處理 options 和 ans 的對應
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

def main():
    st.set_page_config(page_title="國中數學：無限題庫版", page_icon="♾️", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("♾️ 無限數學題庫")
    st.sidebar.info("本系統採用「動態生成引擎」。\n\n每次點擊開始，系統會即時運算產生全新的數據與題目，題庫量理論上為無限大！")
    
    # 單元選單
    units = [
        "3-1 證明與推理",
        "3-2 三角形的外心、內心與重心",
        "4-1 因式分解法",
        "4-2 配方法與公式解",
        "4-3 應用問題",
        "全範圍總複習 (隨機出題)"
    ]
    selected_unit = st.sidebar.selectbox("請選擇練習單元", units, on_change=reset_exam)

    st.title("♾️ 國中數學：考前衝刺 (無限版)")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info(f"準備好挑戰 **{selected_unit}** 了嗎？")
        st.write("點擊下方按鈕，AI 將為您現場生成 10 道全新題目。")
        
        if st.button("🚀 生成試卷 (Generate)", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            # 呼叫工廠生成題目
            st.session_state.current_questions = generate_quiz_questions(selected_unit, 10)
            st.session_state.exam_started = True
            st.rerun()

    else:
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"題目：{total_q} 題")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # 顯示圖形
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
            if final_score == 100: st.success(f"💯 滿分！這些題目都是 AI 現場出的，代表你觀念很強！")
            elif final_score >= 60: st.info(f"👍 及格！")
            else: st.error(f"💪 再刷一次！每次數字都不一樣，練到會為止！")
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
                if st.button("🔄 再刷一卷 (全新題目)", use_container_width=True):
                    # 重新生成全新數字的題目
                    st.session_state.current_questions = generate_quiz_questions(selected_unit, 10)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 換單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
