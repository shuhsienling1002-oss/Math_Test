import streamlit as st
import random

# ==========================================
# 1. 強力視覺引擎 (SVG Generator)
# 包含：幾何圖形、數線解、函數圖形、統計圖
# ==========================================
class SVGGenerator:
    # --- 基礎工具 ---
    @staticmethod
    def _base_svg(content, width=300, height=200):
        return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{content}</svg>'

    # --- 代數具象化工具 (數線解) ---
    @staticmethod
    def roots_on_line(r1, r2=None):
        """將方程式的解(根)具象化在數線上"""
        # 映射邏輯
        def map_x(val): return 150 + (val * 25)
        
        points = f'<circle cx="{map_x(r1)}" cy="50" r="5" fill="red"/><text x="{map_x(r1)}" y="80" text-anchor="middle" fill="red" font-weight="bold">x={r1}</text>'
        if r2 is not None and r2 != r1:
            points += f'<circle cx="{map_x(r2)}" cy="50" r="5" fill="red"/><text x="{map_x(r2)}" y="80" text-anchor="middle" fill="red" font-weight="bold">x={r2}</text>'
        
        content = f"""
        <line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <line x1="150" y1="45" x2="150" y2="55" stroke="black" stroke-width="2"/><text x="150" y="70" text-anchor="middle" fill="#888">0</text>
        {points}
        <text x="150" y="20" text-anchor="middle" fill="blue" font-size="14">方程式的解(根)在數線上的位置</text>
        """
        return SVGGenerator._base_svg(content, height=100)

    # --- 幾何具象化工具 (三角形與四邊形) ---
    @staticmethod
    def triangle_shape(type="general", label=""):
        """畫出不同特性的三角形"""
        shapes = {
            "sss": '<path d="M50,150 L150,150 L100,50 Z" fill="#e3f2fd" stroke="blue" stroke-width="2"/><text x="100" y="170" text-anchor="middle">三邊對應相等 (SSS)</text>',
            "sas": '<path d="M50,150 L150,150 L50,50 Z" fill="#e3f2fd" stroke="blue" stroke-width="2"/><text x="100" y="170" text-anchor="middle">兩邊一夾角 (SAS)</text>',
            "isosceles": '<path d="M100,150 L200,150 L150,20 Z" fill="none" stroke="black" stroke-width="2"/><line x1="150" y1="20" x2="150" y2="150" stroke="red" stroke-dasharray="4"/><text x="150" y="170" text-anchor="middle">等腰三角形 (頂角平分線垂直平分底邊)</text>',
            "right": '<path d="M50,150 L200,150 L50,50 Z" fill="none" stroke="black" stroke-width="2"/><rect x="50" y="130" width="20" height="20" fill="none" stroke="black"/><text x="125" y="170" text-anchor="middle">直角三角形 (斜邊中點為外心)</text>'
        }
        return SVGGenerator._base_svg(shapes.get(type, shapes["sss"]), height=180)

    @staticmethod
    def quad_shape(type="parallelogram"):
        """畫出四邊形"""
        shapes = {
            "parallelogram": '<polygon points="50,150 200,150 230,50 80,50" fill="none" stroke="black" stroke-width="2"/><text x="140" y="170" text-anchor="middle">平行四邊形 (對邊等長)</text>',
            "rhombus": '<polygon points="150,150 200,100 150,50 100,100" fill="none" stroke="black" stroke-width="2"/><line x1="150" y1="50" x2="150" y2="150" stroke="red" stroke-dasharray="4"/><line x1="100" y1="100" x2="200" y2="100" stroke="red" stroke-dasharray="4"/><text x="150" y="170" text-anchor="middle">菱形 (對角線垂直)</text>'
        }
        return SVGGenerator._base_svg(shapes.get(type, shapes["parallelogram"]), height=180)

    # --- 三心具象化工具 ---
    @staticmethod
    def center_visual(type="centroid"):
        """畫出重心、外心、內心"""
        if type == "centroid": # 重心
            return SVGGenerator._base_svg("""
                <path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black" stroke-width="2"/>
                <line x1="150" y1="30" x2="150" y2="170" stroke="red" stroke-width="1" stroke-dasharray="4"/>
                <line x1="50" y1="170" x2="200" y2="100" stroke="red" stroke-width="1" stroke-dasharray="4"/>
                <line x1="250" y1="170" x2="100" y2="100" stroke="red" stroke-width="1" stroke-dasharray="4"/>
                <circle cx="150" cy="123" r="4" fill="blue"/><text x="160" y="123" fill="blue" font-weight="bold">G (重心)</text>
                <text x="150" y="190" text-anchor="middle" font-size="12">中線交點 / 面積平分</text>
            """, 300, 200)
        elif type == "circumcenter": # 外心
            return SVGGenerator._base_svg("""
                <circle cx="150" cy="100" r="80" fill="#f0f8ff" stroke="green"/>
                <polygon points="150,20 80,140 220,140" fill="none" stroke="black" stroke-width="2"/>
                <circle cx="150" cy="100" r="4" fill="green"/>
                <line x1="150" y1="100" x2="150" y2="20" stroke="green" stroke-dasharray="2"/>
                <line x1="150" y1="100" x2="80" y2="140" stroke="green" stroke-dasharray="2"/>
                <line x1="150" y1="100" x2="220" y2="140" stroke="green" stroke-dasharray="2"/>
                <text x="150" y="115" text-anchor="middle" fill="green" font-weight="bold">O (外心)</text>
                <text x="150" y="195" text-anchor="middle" font-size="12">到三頂點等距 (半徑)</text>
            """, 300, 200)
        elif type == "incenter": # 內心
            return SVGGenerator._base_svg("""
                <polygon points="150,20 50,170 250,170" fill="none" stroke="black" stroke-width="2"/>
                <circle cx="150" cy="120" r="50" fill="#fff3e0" stroke="orange"/>
                <circle cx="150" cy="120" r="4" fill="orange"/>
                <line x1="150" y1="120" x2="150" y2="170" stroke="orange" stroke-width="2"/>
                <text x="150" y="110" text-anchor="middle" fill="orange" font-weight="bold">I (內心)</text>
                <text x="150" y="190" text-anchor="middle" font-size="12">到三邊等距 (內切圓半徑)</text>
            """, 300, 200)

    # --- 函數具象化工具 ---
    @staticmethod
    def parabola_roots(a=1, root1=-2, root2=2):
        """畫出拋物線與 x 軸的交點 (根的幾何意義)"""
        # 簡化模擬
        return SVGGenerator._base_svg(f"""
            <line x1="20" y1="100" x2="280" y2="100" stroke="black" marker-end="url(#arrow)"/>
            <path d="M50,20 Q150,180 250,20" fill="none" stroke="red" stroke-width="2"/>
            <circle cx="100" cy="100" r="4" fill="blue"/><text x="100" y="120" text-anchor="middle">根1</text>
            <circle cx="200" cy="100" r="4" fill="blue"/><text x="200" y="120" text-anchor="middle">根2</text>
            <text x="150" y="180" text-anchor="middle" fill="red">拋物線與 x 軸交點即為解</text>
        """, 300, 200)

    @staticmethod
    def area_model():
        """畫出配方法的面積模型示意"""
        return SVGGenerator._base_svg("""
            <rect x="50" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/>
            <rect x="150" y="50" width="20" height="100" fill="#ffcdd2" stroke="black"/>
            <rect x="50" y="150" width="100" height="20" fill="#ffcdd2" stroke="black"/>
            <rect x="150" y="150" width="20" height="20" fill="#e1bee7" stroke="black"/>
            <text x="100" y="100" text-anchor="middle">x²</text>
            <text x="160" y="100" text-anchor="middle">ax</text>
            <text x="100" y="165" text-anchor="middle">ax</text>
            <text x="160" y="165" text-anchor="middle">a²</text>
            <text x="110" y="190" text-anchor="middle" font-size="12">配方法：補上缺角 (a²) 變成正方形</text>
        """, 250, 200)

# ==========================================
# 2. 題庫資料 (MATH_DB) - 全圖解版
# ==========================================
MATH_DB = {
    # ---------------- 3. 外心、內心與重心 ----------------
    "3-1 證明與推理": [
        {"q": "【圖解】若兩三角形「三邊對應相等」，則全等性質為何？", "options": ["SSS", "SAS", "ASA", "RHS"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.triangle_shape("sss"), 
         "expl": "三邊對應相等，稱為 SSS 全等。"},
        {"q": "【圖解】若兩三角形「兩邊一夾角」對應相等，則全等性質為何？", "options": ["SAS", "SSA", "AAS", "ASA"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.triangle_shape("sas"), 
         "expl": "兩邊及其夾角，稱為 SAS 全等。"},
        {"q": "【圖解】等腰三角形的「頂角平分線」會如何？", "options": ["垂直平分底邊", "只平分不垂直", "只垂直不平分", "無作用"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.triangle_shape("isosceles"), 
         "expl": "等腰三角形頂角平分線、底邊中垂線重合 (三線合一)。"},
        {"q": "【圖解】平行四邊形的判別性質不包含？", "options": ["對角線互相垂直", "兩組對邊分別相等", "兩組對角分別相等", "一組對邊平行且相等"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.quad_shape("parallelogram"), 
         "expl": "對角線互相垂直是「菱形」或「箏形」的特徵，非一般平行四邊形。"},
        {"q": "【圖解】直角三角形斜邊中點到三頂點距離？", "options": ["相等", "不相等", "只有兩點相等", "無法判斷"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.triangle_shape("right"), 
         "expl": "直角三角形斜邊中點即為外心，到三頂點等距 (外接圓半徑)。"}
    ],
    "3-2 三角形的外心、內心與重心": [
        {"q": "【圖解】三角形的「重心」定義為何？", "options": ["三中線交點", "三高交點", "角平分線交點", "中垂線交點"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.center_visual("centroid"), 
         "expl": "重心 (G) 是三條中線的交點。"},
        {"q": "【圖解】三角形的「外心」性質為何？", "options": ["到三頂點等距", "到三邊等距", "平分面積", "在三角形內部"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.center_visual("circumcenter"), 
         "expl": "外心 (O) 到三頂點距離相等 (綠色半徑)。"},
        {"q": "【圖解】三角形的「內心」性質為何？", "options": ["到三邊等距", "到三頂點等距", "平分面積", "在三角形外部"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.center_visual("incenter"), 
         "expl": "內心 (I) 到三邊垂直距離相等 (內切圓半徑)。"},
        {"q": "【圖解】重心將中線分為哪兩段比例？", "options": ["2:1 (頂點:邊)", "1:1", "3:1", "1:2"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.center_visual("centroid"), 
         "expl": "重心性質：頂點到重心 : 重心到對邊中點 = 2 : 1。"},
        {"q": "【圖解】銳角三角形的外心位置？", "options": ["內部", "外部", "邊上", "頂點"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.center_visual("circumcenter"), 
         "expl": "銳角三角形外心在內部 (如圖所示)。"}
    ],

    # ---------------- 4. 一元二次方程式 ----------------
    "4-1 因式分解法": [
        {"q": "【圖解】解方程式 $(x-2)(x+3)=0$，x 為何？", "options": ["2 或 -3", "-2 或 3", "2 或 3", "-2 或 -3"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.roots_on_line(2, -3), 
         "expl": "若兩數積為0，則 $x-2=0$ 或 $x+3=0$。解為 2 或 -3。"},
        {"q": "【圖解】解 $x^2 - 4 = 0$，x 為何？", "options": ["2 或 -2", "2", "4", "16"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.roots_on_line(2, -2), 
         "expl": "$(x+2)(x-2)=0$，故 $x = \\pm 2$。"},
        {"q": "【圖解】方程式 $x(x-5)=0$ 的解？", "options": ["0 或 5", "5", "0", "1 或 5"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.roots_on_line(0, 5), 
         "expl": "x=0 或 x-5=0。"},
        {"q": "【圖解】解完全平方式 $(x-3)^2 = 0$？", "options": ["3 (重根)", "-3", "3 或 -3", "9"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.roots_on_line(3), 
         "expl": "兩個根重疊在同一點 x=3。"}
    ],
    "4-2 配方法與公式解": [
        {"q": "【圖解】配方法的核心概念是補成什麼圖形？", "options": ["正方形", "長方形", "三角形", "圓形"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.area_model(), 
         "expl": "配方法 (Completing the Square) 就是補一塊讓它變成正方形 (完全平方式)。"},
        {"q": "【圖解】若方程式有「相異兩實根」，圖形與 x 軸有幾個交點？", "options": ["2個", "1個", "0個", "無限多"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.parabola_roots(), 
         "expl": "判別式 D > 0，拋物線與 x 軸有 2 個交點。"},
        {"q": "【圖解】解 $(x+1)^2 = 4$？", "options": ["1 或 -3", "1", "-3", "2 或 -2"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator.roots_on_line(1, -3), 
         "expl": "$x+1 = \\pm 2 \\Rightarrow x = 2-1$ 或 $-2-1$。"},
        {"q": "判別式 $D = b^2 - 4ac < 0$ 代表什麼？", "options": ["無實數解 (圖形與 x 軸無交點)", "有兩相異解", "重根", "無法判斷"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator._base_svg('<path d="M50,50 Q150,150 250,50" fill="none" stroke="red"/><line x1="0" y1="180" x2="300" y2="180" stroke="black"/><text x="150" y="170" text-anchor="middle">與 x 軸無交點</text>'), 
         "expl": "判別式小於 0，圖形懸空，與 x 軸無交點，故無實數解。"}
    ],
    "4-3 應用問題": [
        {"q": "【圖解】正方形面積 16，邊長為 x，求 x？", "options": ["4", "-4", "16", "8"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator._base_svg('<rect x="100" y="50" width="100" height="100" fill="lightblue" stroke="black"/><text x="150" y="100" text-anchor="middle">面積=16</text><text x="150" y="170" text-anchor="middle">邊長 x = ?</text>'), 
         "expl": "$x^2 = 16 \\Rightarrow x = 4$ (邊長不為負)。"},
        {"q": "【圖解】梯形上底 3，下底 x，高 4，面積 20，求 x？", "options": ["7", "5", "6", "8"], "ans": 0, "diff": "中等", 
         "svg_gen": lambda: SVGGenerator._base_svg('<polygon points="80,50 220,50 250,150 50,150" fill="none" stroke="black"/><text x="150" y="40" text-anchor="middle">3</text><text x="150" y="170" text-anchor="middle">x</text><line x1="220" y1="50" x2="220" y2="150" stroke="red" stroke-dasharray="4"/><text x="230" y="100" fill="red">4</text>'), 
         "expl": "$(3+x)\\times 4 / 2 = 20 \\Rightarrow (3+x)\\times 2 = 20 \\Rightarrow 3+x=10 \\Rightarrow x=7$。"},
        {"q": "【圖解】兩數和為 10，積為 24，求此兩數？", "options": ["4, 6", "2, 12", "3, 8", "1, 24"], "ans": 0, "diff": "簡單", 
         "svg_gen": lambda: SVGGenerator.roots_on_line(4, 6), 
         "expl": "設一數 x，另一數 10-x。$x(10-x)=24 \\Rightarrow x^2-10x+24=0$。解得 4, 6。"}
    ]
}

# ==========================================
# 3. APP 主程式
# ==========================================
def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：視覺具象化完全版", page_icon="👁️", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("👁️ 數學具象化")
    st.sidebar.success("系統特色：\n1. 代數圖形化 (看到 x 就看到點)\n2. 幾何全圖解 (每題都有圖)\n3. 針對考前衝刺設計")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)

    st.title("👁️ 國中數學：視覺具象化版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info("💡 每一道題目都配備了動態圖形，幫助你將抽象的數學概念轉化為具體的影像！")
        if st.button("🚀 開始視覺測驗", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            all_questions = MATH_DB.get(selected_unit, [])
            num_to_pick = min(len(all_questions), 10)
            st.session_state.current_questions = random.sample(all_questions, num_to_pick)
            st.session_state.exam_started = True
            st.rerun()

    else:
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"進度：0/{total_q}")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # 強制渲染圖形
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
            st.markdown(f"### 得分：{final_score} 分")
            
            if final_score == 100: st.balloons()

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
                if st.button("🔄 再刷一次 (題目不同)", use_container_width=True):
                    all_questions = MATH_DB.get(selected_unit, [])
                    num_to_pick = min(len(all_questions), 10)
                    st.session_state.current_questions = random.sample(all_questions, num_to_pick)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 選擇其他單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
