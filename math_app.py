import streamlit as st
import random

# ==========================================
# 1. 內嵌視覺圖庫 (SVG Assets) - 零設定核心
# ==========================================
SVG_ASSETS = {
    # --- 國一視覺 ---
    "number_line_dist": """
        <svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">
         <line x1="20" y1="50" x2="380" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
         <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs>
         <line x1="200" y1="45" x2="200" y2="55" stroke="black" stroke-width="2"/><text x="200" y="70" text-anchor="middle">0</text>
         <line x1="120" y1="45" x2="120" y2="55" stroke="black" stroke-width="2"/><text x="120" y="70" text-anchor="middle">-4</text>
         <line x1="280" y1="45" x2="280" y2="55" stroke="black" stroke-width="2"/><text x="280" y="70" text-anchor="middle">3</text>
         <path d="M120,40 Q200,10 280,40" stroke="red" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
         <text x="200" y="25" text-anchor="middle" fill="red" font-weight="bold">距離 = ?</text>
         <circle cx="120" cy="50" r="5" fill="red"/><circle cx="280" cy="50" r="5" fill="red"/>
        </svg>
    """,
    "coordinate_q2": """
        <svg width="300" height="300" viewBox="-150 -150 300 300" xmlns="http://www.w3.org/2000/svg">
         <line x1="-140" y1="0" x2="140" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
         <line x1="0" y1="140" x2="0" y2="-140" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
         <text x="130" y="20">x</text><text x="10" y="-130">y</text>
         <text x="-20" y="20">O</text>
         <circle cx="-80" cy="-60" r="6" fill="red"/>
         <text x="-110" y="-70" fill="red" font-size="16" font-weight="bold">P</text>
         <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs>
        </svg>
    """,
    # --- 國二視覺 ---
    "pythagoras_visual": """
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
         <polygon points="50,150 250,150 50,50" style="fill:lightblue;stroke:black;stroke-width:2" />
         <rect x="50" y="130" width="20" height="20" style="fill:none;stroke:black;stroke-width:1"/>
         <text x="150" y="170" text-anchor="middle" font-size="14">股 a = 12</text>
         <text x="30" y="100" text-anchor="end" font-size="14">股 b = 5</text>
         <text x="160" y="90" text-anchor="start" font-size="16" fill="red" font-weight="bold">斜邊 c = ?</text>
        </svg>
    """,
    "parallel_lines": """
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
         <line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2"/><text x="290" y="55">L1</text>
         <line x1="20" y1="150" x2="280" y2="150" stroke="black" stroke-width="2"/><text x="290" y="155">L2</text>
         <line x1="80" y1="20" x2="220" y2="180" stroke="red" stroke-width="2"/>
         <text x="120" y="65" font-size="14">∠1</text>
         <text x="170" y="140" font-size="14" fill="blue" font-weight="bold">∠2 = ?</text>
         <text x="20" y="20" fill="gray">若 L1 // L2</text>
        </svg>
    """,
    # --- 國三視覺 ---
    "parabola_visual": """
        <svg width="300" height="300" viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">
         <line x1="-9" y1="0" x2="9" y2="0" stroke="gray" stroke-width="0.5"/>
         <line x1="0" y1="9" x2="0" y2="-9" stroke="gray" stroke-width="0.5"/>
         <path d="M -3,5 Q 0,-4 3,5" stroke="blue" stroke-width="1" fill="none"/>
         <circle cx="0" cy="-4" r="0.8" fill="red"/>
         <text x="1" y="-4" fill="red" font-size="2">頂點</text>
         <text x="-8" y="8" font-size="2">y = ax² + k</text>
        </svg>
    """,
    "circle_tangent": """
        <svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
         <circle cx="150" cy="150" r="80" stroke="black" stroke-width="2" fill="none"/>
         <circle cx="150" cy="150" r="3" fill="black"/><text x="140" y="145">O</text>
         <line x1="50" y1="250" x2="250" y2="50" stroke="red" stroke-width="2"/><text x="260" y="60" fill="red">L (切線)</text>
         <line x1="150" y1="150" x2="206.5" y2="93.5" stroke="blue" stroke-width="2" stroke-dasharray="5,5"/>
         <circle cx="206.5" cy="93.5" r="5" fill="red"/><text x="215" y="100">P (切點)</text>
         <text x="170" y="130" fill="blue">半徑 r</text>
         <text x="20" y="30" fill="gray">請問 OP 與 L 的夾角？</text>
        </svg>
    """
}

# ==========================================
# 2. 視覺導向題庫 (Visual Math DB)
# ==========================================
MATH_DB = {
    "國一數學 (七年級) - 圖像理解": [
        {"q": "【視覺題】請參考上方數線圖，-4 到 3 的距離是多少？", "options": ["1", "7", "-1", "-7"], "ans": 1, "diff": "簡單", "type": "單選", "svg": "number_line_dist", "expl": "距離 = 大數減小數 = $3 - (-4) = 3 + 4 = 7$。或者直接數格子：從-4走到0是4格，從0走到3是3格，共7格。"},
        {"q": "【視覺題】請參考上方坐標圖，紅點 P 位於第幾象限？", "options": ["第一象限 (+,+)", "第二象限 (-,+)", "第三象限 (-,-)", "第四象限 (+,-)"], "ans": 2, "diff": "簡單", "type": "單選", "svg": "coordinate_q2", "expl": "點在左下方，x軸往左(負)，y軸往下(負)。負負得第三象限。"},
        {"q": "若 $|x| = 5$，在數線上表示 x 的點與原點的距離為何？", "options": ["5", "-5", "0", "10"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "絕對值的幾何意義就是「與原點的距離」。"},
        {"q": "溫度計從 -3度 上升 8度，現在是幾度？", "options": ["5度", "11度", "-11度", "-5度"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$-3 + 8 = 5$。想像在數線上從-3往右走8格。"}
    ],
    "國二數學 (八年級) - 圖像理解": [
        {"q": "【視覺題】請參考上方直角三角形，已知兩股為 5 和 12，斜邊 c 長度為何？", "options": ["13", "17", "sqrt(119)", "10"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "pythagoras_visual", "expl": "畢氏定理：$a^2 + b^2 = c^2$。$5^2 + 12^2 = 25 + 144 = 169$。$c = \sqrt{169} = 13$。"},
        {"q": "【視覺題】請參考上方圖形，已知 L1 平行 L2，若 ∠1 與 ∠2 是「內錯角」，則 ∠2 幾度？", "options": ["與 ∠1 互補 (相加180度)", "與 ∠1 相等", "比 ∠1 大", "無法判斷"], "ans": 1, "diff": "中等", "type": "單選", "svg": "parallel_lines", "expl": "平行線性質：兩平行線被一直線所截，內錯角相等。"},
        {"q": "下列哪一個圖形一定有「對稱軸」？", "options": ["等腰三角形", "直角三角形", "平行四邊形", "任意梯形"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "等腰三角形底邊的中垂線即為其對稱軸。平行四邊形是點對稱，不一定是線對稱。"},
        {"q": "乘法公式 $(a+b)^2$ 可以用下列哪個圖形面積來解釋？", "options": ["一個邊長為 a+b 的正方形", "一個長 a 寬 b 的長方形", "兩個邊長為 a 的正方形", "一個三角形"], "ans": 0, "diff": "中等", "type": "單選", "expl": "邊長為 (a+b) 的正方形面積，可切割成 $a^2$、$b^2$ 和兩個 $ab$ 的矩形。"}
    ],
    "國三數學 (九年級) - 圖像理解": [
        {"q": "【視覺題】請觀察上方二次函數圖形，其開口方向與頂點位置為何？", "options": ["開口向上，頂點是最高點", "開口向下，頂點是最低點", "開口向上，頂點是最低點", "開口向下，頂點是最高點"], "ans": 2, "diff": "簡單", "type": "單選", "svg": "parabola_visual", "expl": "圖形像杯子一樣向上開口。紅色點在最底部，所以頂點是最低點。這代表二次項係數 $a > 0$。"},
        {"q": "【視覺題】請參考上方圓形圖，直線 L 切圓 O 於 P 點。則半徑 OP 與切線 L 的夾角是幾度？", "options": ["45度", "60度", "90度 (垂直)", "180度"], "ans": 2, "diff": "簡單", "type": "單選", "svg": "circle_tangent", "expl": "圓的切線性質：圓心到切點的連線(半徑)必垂直於切線。"},
        {"q": "投擲一枚公正硬幣兩次，利用樹狀圖分析，出現「一正一反」的機率是？", "options": ["1/4", "1/2", "3/4", "1"], "ans": 1, "diff": "中等", "type": "單選", "expl": "可能結果有：(正,正), (正,反), (反,正), (反,反) 共4種。一正一反有2種。機率 = 2/4 = 1/2。"},
        {"q": "兩個相似三角形，若邊長比為 1:3，則它們的「面積比」為何？", "options": ["1:3", "1:6", "1:9", "3:1"], "ans": 2, "diff": "中等", "type": "單選", "expl": "相似形的面積比等於邊長比的平方。$1^2 : 3^2 = 1 : 9$。"}
    ]
}

# ==========================================
# 3. APP 主程式邏輯 (加入 SVG 渲染)
# ==========================================
def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：超視覺圖像理解版", page_icon="🎨", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🎨 視覺數學設定")
    grade_level = st.sidebar.selectbox("選擇單元", list(MATH_DB.keys()), on_change=reset_exam)
    st.sidebar.info("💡 此版本特別針對需要圖像輔助的學生設計，強調看圖理解觀念。")
    
    st.title("🎨 國中數學：超視覺圖像理解版")
    st.caption("不用憑空想像，看圖就懂！")
    
    if not st.session_state.exam_started:
        st.info(f"準備開始：**{grade_level}**")
        if st.button("🚀 載入圖形與題目", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            questions = MATH_DB.get(grade_level, [])
            random.shuffle(questions)
            st.session_state.current_questions = questions
            st.session_state.exam_started = True
            st.rerun()

    else:
        st.subheader(f"📝 {grade_level}")
        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                # === 核心修改：渲染 SVG ===
                if "svg" in q and q["svg"] in SVG_ASSETS:
                    # 使用 unsafe_allow_html 來顯示 SVG
                    st.markdown(SVG_ASSETS[q["svg"]], unsafe_allow_html=True)
                    st.caption("👆 請參考上方圖形作答")
                # ========================
                st.write(q['q'])
                st.radio("選項：", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            if st.form_submit_button("✅ 交卷看詳解", use_container_width=True):
                score = 0
                results = []
                for idx, q in enumerate(questions):
                    q_key = f"q_{idx}"
                    user_ans = st.session_state.get(q_key)
                    correct_ans = q['options'][q['ans']]
                    is_correct = (user_ans == correct_ans)
                    if is_correct: score += 1
                    results.append({"q": q, "is_correct": is_correct, "user": user_ans, "correct": correct_ans})
                st.session_state.exam_results = {"score": score, "total": len(questions), "details": results}
                st.session_state.exam_finished = True

        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            st.markdown("---")
            if final_score >= 90: st.success(f"💯 視覺天才！ ({final_score}分)")
            elif final_score >= 60: st.info(f"👍 有概念喔！ ({final_score}分)")
            else: st.error(f"💪 多看圖幾次就會了！ ({final_score}分)")
            
            for i, item in enumerate(res['details']):
                q_data = item['q']
                with st.expander(f"第 {i+1} 題詳解 ({'✅ 對' if item['is_correct'] else '❌ 錯'})"):
                    # 詳解也要顯示圖
                    if "svg" in q_data and q_data["svg"] in SVG_ASSETS:
                         st.markdown(SVG_ASSETS[q_data["svg"]], unsafe_allow_html=True)
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.info(f"**💡 圖像解析**：\n\n{q_data['expl']}")

            if st.button("🔄 重新練習"):
                reset_exam()
                st.rerun()

if __name__ == "__main__":
    main()
