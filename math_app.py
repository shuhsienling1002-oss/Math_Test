import streamlit as st
import random
import math

# ==========================================
# 1. 動態 SVG 生成引擎 (The Artist)
# ==========================================
class SVGGenerator:
    @staticmethod
    def coordinate_point(x, y, label="P"):
        """動態生成坐標點：根據傳入的 x, y 改變紅點位置"""
        # 簡單映射：範圍 -5 到 5，映射到畫布座標
        cx = 150 + (x * 25)
        cy = 150 - (y * 25)
        
        return f"""
        <svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#f9f9f9"/>
            <defs><pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#ddd" stroke-width="1"/></pattern></defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            <line x1="150" y1="0" x2="150" y2="300" stroke="black" stroke-width="2"/>
            <line x1="0" y1="150" x2="300" y2="150" stroke="black" stroke-width="2"/>
            <text x="285" y="145" font-weight="bold">x</text><text x="155" y="15" font-weight="bold">y</text>
            <circle cx="{cx}" cy="{cy}" r="6" fill="red" stroke="white" stroke-width="2"/>
            <text x="{cx+10}" y="{cy-10}" fill="red" font-weight="bold" font-size="16">{label}({x},{y})</text>
        </svg>
        """

    @staticmethod
    def number_line(p1, p2):
        """動態數線：標示兩點與距離"""
        # 映射：每個單位 25px，原點在 200
        x1 = 200 + (p1 * 25)
        x2 = 200 + (p2 * 25)
        dist = abs(p2 - p1)
        mid = (x1 + x2) / 2
        
        return f"""
        <svg width="400" height="120" xmlns="http://www.w3.org/2000/svg">
            <line x1="20" y1="80" x2="380" y2="80" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
            <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs>
            <line x1="200" y1="75" x2="200" y2="85" stroke="black" stroke-width="2"/><text x="200" y="100" text-anchor="middle">0</text>
            <circle cx="{x1}" cy="80" r="5" fill="blue"/>
            <text x="{x1}" y="115" text-anchor="middle" fill="blue" font-weight="bold">{p1}</text>
            <circle cx="{x2}" cy="80" r="5" fill="red"/>
            <text x="{x2}" y="115" text-anchor="middle" fill="red" font-weight="bold">{p2}</text>
            <path d="M{x1},70 Q{mid},{70-dist*5} {x2},70" stroke="purple" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
            <text x="{mid}" y="{60-dist*2}" text-anchor="middle" fill="purple" font-weight="bold" font-size="14">距離 = {dist}</text>
        </svg>
        """

    @staticmethod
    def probability_balls(red, white, green=0):
        """動態機率圖：真的畫出幾顆球"""
        balls_svg = ""
        start_x = 30
        for i in range(red):
            balls_svg += f'<circle cx="{start_x}" cy="40" r="15" fill="#ff4444" stroke="black"/><text x="{start_x}" y="45" text-anchor="middle" fill="white" font-size="10">紅</text>'
            start_x += 35
        for i in range(white):
            balls_svg += f'<circle cx="{start_x}" cy="40" r="15" fill="white" stroke="black"/><text x="{start_x}" y="45" text-anchor="middle" fill="black" font-size="10">白</text>'
            start_x += 35
        for i in range(green):
            balls_svg += f'<circle cx="{start_x}" cy="40" r="15" fill="#44ff44" stroke="black"/><text x="{start_x}" y="45" text-anchor="middle" fill="black" font-size="10">綠</text>'
            start_x += 35
            
        return f"""
        <svg width="400" height="80" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#eee" rx="10"/>
            {balls_svg}
            <text x="200" y="75" text-anchor="middle" fill="#555" font-size="12">袋子裡的情況</text>
        </svg>
        """

    @staticmethod
    def triangle_label(a, b, c, h="?"):
        """動態標示三角形：圖形形狀固定(示意圖)，但數字標籤會變"""
        return f"""
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
            <path d="M50,170 L250,170 L50,50 Z" fill="#e3f2fd" stroke="blue" stroke-width="3"/>
            <rect x="50" y="150" width="20" height="20" fill="none" stroke="blue"/>
            <text x="150" y="190" text-anchor="middle" font-size="16" fill="black">底 = {a}</text>
            <text x="30" y="110" text-anchor="end" font-size="16" fill="black">高 = {b}</text>
            <text x="160" y="100" text-anchor="start" font-size="16" fill="red" font-weight="bold">斜邊 = {c}</text>
        </svg>
        """
    
    @staticmethod
    def linear_func(m, k):
        """畫出一次函數 y = mx + k (示意趨勢)"""
        # 簡單判斷斜率正負來畫線
        if m > 0:
            line = '<line x1="50" y1="250" x2="250" y2="50" stroke="blue" stroke-width="3"/>'
            text = "斜率 > 0 (右上左下)"
        elif m < 0:
            line = '<line x1="50" y1="50" x2="250" y2="250" stroke="red" stroke-width="3"/>'
            text = "斜率 < 0 (左上右下)"
        else:
            line = '<line x1="20" y1="150" x2="280" y2="150" stroke="green" stroke-width="3"/>'
            text = "斜率 = 0 (水平線)"
            
        return f"""
        <svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
            <line x1="150" y1="0" x2="150" y2="300" stroke="black" stroke-width="1"/>
            <line x1="0" y1="150" x2="300" y2="150" stroke="black" stroke-width="1"/>
            {line}
            <text x="150" y="280" text-anchor="middle" font-weight="bold">{text}</text>
            <text x="20" y="20" font-size="14">y = {m}x + {k}</text>
        </svg>
        """

# ==========================================
# 2. 題庫 (整合動態圖形生成)
# ==========================================
MATH_DB = {
    "七上：整數與數線": [
        {
            "q": "【動態圖】數線上，-3 到 4 的距離是多少？",
            "options": ["1", "7", "-1", "-7"], "ans": 1, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.number_line(-3, 4),
            "expl": "距離 = 大數 - 小數 = $4 - (-3) = 7$。請看圖中紫色虛線跨過的長度。"
        },
        {
            "q": "【動態圖】數線上，-5 到 -2 的距離是多少？",
            "options": ["3", "-3", "7", "-7"], "ans": 0, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.number_line(-5, -2),
            "expl": "距離 = $|-2 - (-5)| = |3| = 3$。"
        },
        {
            "q": "計算 $15 + (-8)$ 的值？", "options": ["7", "-7", "23", "-23"], "ans": 0, "diff": "簡單",
            "svg_gen": None, "expl": "正多負少，結果為正。$15-8=7$。"
        }
    ],
    "七下：直角坐標": [
        {
            "q": "【動態圖】請問點 A(-3, 2) 位於第幾象限？",
            "options": ["一", "二", "三", "四"], "ans": 1, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.coordinate_point(-3, 2, "A"),
            "expl": "x為負(左)，y為正(上)，故為第二象限。"
        },
        {
            "q": "【動態圖】請問點 B(4, -4) 位於第幾象限？",
            "options": ["一", "二", "三", "四"], "ans": 3, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.coordinate_point(4, -4, "B"),
            "expl": "x為正(右)，y為負(下)，故為第四象限。"
        },
        {
            "q": "【動態圖】觀察圖形，若 $y = 2x + 1$，直線走向為何？",
            "options": ["右上左下 (斜率正)", "左上右下 (斜率負)", "水平", "垂直"], "ans": 0, "diff": "中等",
            "svg_gen": lambda: SVGGenerator.linear_func(2, 1),
            "expl": "x 的係數(斜率)為 2 > 0，故直線隨著 x 變大而上升。"
        }
    ],
    "八上：畢氏定理": [
        {
            "q": "【動態圖】直角三角形兩股為 3, 4，斜邊長度？",
            "options": ["5", "6", "7", "25"], "ans": 0, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.triangle_label(3, 4, "?"),
            "expl": "$\\sqrt{3^2 + 4^2} = \\sqrt{9+16} = \\sqrt{25} = 5$。"
        },
        {
            "q": "【動態圖】直角三角形兩股為 6, 8，斜邊長度？",
            "options": ["10", "12", "14", "100"], "ans": 0, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"),
            "expl": "$\\sqrt{6^2 + 8^2} = \\sqrt{36+64} = \\sqrt{100} = 10$。"
        },
        {
            "q": "【動態圖】已知斜邊為 13，一股為 5，求另一股？",
            "options": ["12", "8", "10", "18"], "ans": 0, "diff": "中等",
            "svg_gen": lambda: SVGGenerator.triangle_label("?", 5, 13),
            "expl": "另一股 = $\\sqrt{13^2 - 5^2} = \\sqrt{169-25} = \\sqrt{144} = 12$。"
        }
    ],
    "九下：機率": [
        {
            "q": "【動態圖】袋中有 3 顆紅球，2 顆白球。抽中紅球機率？",
            "options": ["3/5", "2/5", "1/2", "1/3"], "ans": 0, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.probability_balls(3, 2),
            "expl": "總球數 = 5。紅球 = 3。機率 = 3/5。"
        },
        {
            "q": "【動態圖】袋中有 1 紅、1 白、1 綠。抽中白球機率？",
            "options": ["1/3", "1/2", "2/3", "1"], "ans": 0, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.probability_balls(1, 1, 1),
            "expl": "總球數 = 3。白球 = 1。機率 = 1/3。"
        },
        {
            "q": "【動態圖】袋中有 4 紅、1 白。抽中紅球機率？",
            "options": ["4/5", "1/5", "1/4", "3/4"], "ans": 0, "diff": "簡單",
            "svg_gen": lambda: SVGGenerator.probability_balls(4, 1),
            "expl": "紅球佔了絕大多數，看圖就知道機率很高。4/(4+1) = 4/5。"
        }
    ]
}

# 擴充其他單元的基礎題目 (混合無圖題，確保題庫量夠大)
MATH_DB["七上：整數與數線"].append({"q": "比 -10 大 3 的數是？", "options": ["-7", "-13", "7", "13"], "ans": 0, "diff": "簡單", "svg_gen": None, "expl": "$-10 + 3 = -7$"})
MATH_DB["八上：畢氏定理"].append({"q": "直角三角形斜邊最長嗎？", "options": ["是", "不是", "不一定", "看角度"], "ans": 0, "diff": "簡單", "svg_gen": None, "expl": "大角對大邊，90度最大，故斜邊最長。"})

# ==========================================
# 3. APP 主程式
# ==========================================
def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：動態視覺版", page_icon="🎨", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🎨 數學實驗室")
    st.sidebar.info("💡 此版本採用「動態繪圖技術」。\n\n每一題的圖形都是「現場畫出來」的，所以會根據題目數字不同而改變！")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("選擇單元", unit_options, on_change=reset_exam)

    st.title("🎨 國中數學：動態視覺版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info(f"準備練習：**{selected_unit}**")
        if st.button("🚀 開始動態測驗", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            all_questions = MATH_DB.get(selected_unit, [])
            # 隨機選題
            num_to_pick = min(len(all_questions), 10)
            st.session_state.current_questions = random.sample(all_questions, num_to_pick)
            st.session_state.exam_started = True
            st.rerun()

    else:
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"題目總數：{total_q}")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # === 核心：動態生成圖形 ===
                if q.get("svg_gen"):
                    svg_code = q["svg_gen"]() # 執行函數生成 SVG
                    st.markdown(svg_code, unsafe_allow_html=True)
                    st.caption("👆 這張圖是根據題目數字現場畫出來的喔！")
                # ========================
                
                st.markdown(f"### {q['q']}")
                st.radio("選項", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            if st.form_submit_button("✅ 交卷", use_container_width=True):
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
            if final_score < 60:
                st.error("別灰心，多看幾次圖就會懂了！")
            else:
                st.success("很棒！這就是圖像記憶的力量！")

            for i, item in enumerate(res['details']):
                q_data = item['q']
                with st.expander(f"第 {i+1} 題詳解 ({'✅' if item['is_correct'] else '❌'})"):
                    # 詳解也要顯示動態圖
                    if q_data.get("svg_gen"):
                        st.markdown(q_data["svg_gen"](), unsafe_allow_html=True)
                        
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.markdown(f"**💡 解析**：")
                    st.markdown(q_data['expl'])

            if st.button("🔄 再玩一次"):
                reset_exam()
                st.rerun()

if __name__ == "__main__":
    main()
