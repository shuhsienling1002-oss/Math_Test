import streamlit as st
import random

# ==========================================
# 1. 內嵌視覺圖庫 (SVG Assets) - 擴充版
# ==========================================
SVG_ASSETS = {
    # --- 原有圖庫 ---
    "number_line_dist": """<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="50" x2="380" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs><line x1="200" y1="45" x2="200" y2="55" stroke="black" stroke-width="2"/><text x="200" y="70" text-anchor="middle">0</text><line x1="120" y1="45" x2="120" y2="55" stroke="black" stroke-width="2"/><text x="120" y="70" text-anchor="middle">-4</text><line x1="280" y1="45" x2="280" y2="55" stroke="black" stroke-width="2"/><text x="280" y="70" text-anchor="middle">3</text><path d="M120,40 Q200,10 280,40" stroke="red" stroke-width="2" fill="none" stroke-dasharray="5,5"/><text x="200" y="25" text-anchor="middle" fill="red" font-weight="bold">距離 = ?</text><circle cx="120" cy="50" r="5" fill="red"/><circle cx="280" cy="50" r="5" fill="red"/></svg>""",
    "coordinate_q2": """<svg width="300" height="300" viewBox="-150 -150 300 300" xmlns="http://www.w3.org/2000/svg"><line x1="-140" y1="0" x2="140" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/><line x1="0" y1="140" x2="0" y2="-140" stroke="black" stroke-width="2" marker-end="url(#arrow)"/><text x="130" y="20">x</text><text x="10" y="-130">y</text><text x="-20" y="20">O</text><circle cx="-80" cy="-60" r="6" fill="red"/><text x="-110" y="-70" fill="red" font-size="16" font-weight="bold">P</text><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs></svg>""",
    "pythagoras_visual": """<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><polygon points="50,150 250,150 50,50" style="fill:lightblue;stroke:black;stroke-width:2" /><rect x="50" y="130" width="20" height="20" style="fill:none;stroke:black;stroke-width:1"/><text x="150" y="170" text-anchor="middle" font-size="14">股 a = 12</text><text x="30" y="100" text-anchor="end" font-size="14">股 b = 5</text><text x="160" y="90" text-anchor="start" font-size="16" fill="red" font-weight="bold">斜邊 c = ?</text></svg>""",
    "parallel_lines": """<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2"/><text x="290" y="55">L1</text><line x1="20" y1="150" x2="280" y2="150" stroke="black" stroke-width="2"/><text x="290" y="155">L2</text><line x1="80" y1="20" x2="220" y2="180" stroke="red" stroke-width="2"/><text x="120" y="65" font-size="14">∠1</text><text x="170" y="140" font-size="14" fill="blue" font-weight="bold">∠2 = ?</text><text x="20" y="20" fill="gray">若 L1 // L2</text></svg>""",
    "parabola_visual": """<svg width="300" height="300" viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg"><line x1="-9" y1="0" x2="9" y2="0" stroke="gray" stroke-width="0.5"/><line x1="0" y1="9" x2="0" y2="-9" stroke="gray" stroke-width="0.5"/><path d="M -3,5 Q 0,-4 3,5" stroke="blue" stroke-width="1" fill="none"/><circle cx="0" cy="-4" r="0.8" fill="red"/><text x="1" y="-4" fill="red" font-size="2">頂點</text><text x="-8" y="8" font-size="2">y = ax² + k</text></svg>""",
    "circle_tangent": """<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg"><circle cx="150" cy="150" r="80" stroke="black" stroke-width="2" fill="none"/><circle cx="150" cy="150" r="3" fill="black"/><text x="140" y="145">O</text><line x1="50" y1="250" x2="250" y2="50" stroke="red" stroke-width="2"/><text x="260" y="60" fill="red">L (切線)</text><line x1="150" y1="150" x2="206.5" y2="93.5" stroke="blue" stroke-width="2" stroke-dasharray="5,5"/><circle cx="206.5" cy="93.5" r="5" fill="red"/><text x="215" y="100">P (切點)</text><text x="170" y="130" fill="blue">半徑 r</text><text x="20" y="30" fill="gray">請問 OP 與 L 的夾角？</text></svg>""",
    
    # --- 新增圖庫 ---
    "linear_graph": """<svg width="300" height="300" viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg"><line x1="-10" y1="0" x2="10" y2="0" stroke="black" stroke-width="0.5"/><line x1="0" y1="10" x2="0" y2="-10" stroke="black" stroke-width="0.5"/><text x="9" y="-1">x</text><text x="1" y="9">y</text><line x1="-5" y1="-8" x2="8" y2="5" stroke="blue" stroke-width="1.5"/><circle cx="0" cy="-3" r="0.5" fill="red"/><text x="1" y="-3" font-size="2">y截距(0, b)</text><circle cx="3" cy="0" r="0.5" fill="red"/><text x="3" y="-1" font-size="2">x截距</text></svg>""",
    "similar_triangles": """<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><polygon points="20,180 100,180 60,100" fill="none" stroke="blue" stroke-width="2"/><text x="60" y="195" text-anchor="middle">小三角形</text><text x="35" y="140">1</text><polygon points="120,180 280,180 200,20" fill="none" stroke="red" stroke-width="2"/><text x="200" y="195" text-anchor="middle">大三角形 (放大2倍)</text><text x="150" y="100">2</text></svg>""",
    "circle_angles": """<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg"><circle cx="150" cy="150" r="100" stroke="black" fill="none"/><circle cx="150" cy="150" r="3" fill="black"/><text x="140" y="160">O(圓心)</text><path d="M 50,150 L 150,150 L 100,63.4" stroke="red" stroke-width="2" fill="none"/><text x="120" y="130" fill="red">圓心角</text><path d="M 50,150 L 250,150 L 100,63.4" stroke="blue" stroke-width="2" fill="none" stroke-dasharray="5,5"/><text x="200" y="130" fill="blue">圓周角</text><text x="100" y="40">對同一弧</text></svg>"""
}

# ==========================================
# 2. 海量題庫 (已擴充圖形標記)
# ==========================================
MATH_DB = {
    # ---------------- 國一 (七年級) ----------------
    "七上：整數與絕對值": [
        {"q": "計算 $(-15) + 8 - (-5)$ 的值？", "options": ["-2", "-12", "2", "-28"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "負負得正：$-15 + 8 + 5 = -15 + 13 = -2$"},
        {"q": "【圖解題】參考數線圖，-4 到 3 的距離？", "options": ["1", "7", "-1", "-7"], "ans": 1, "diff": "簡單", "type": "單選", "svg": "number_line_dist", "expl": "距離 = 大減小 = $3 - (-4) = 7$。"},
        {"q": "若 $|a| = 5$，在數線上表示 a 的點與原點距離為何？", "options": ["5", "-5", "0", "25"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "number_line_dist", "expl": "絕對值的幾何意義就是與原點的距離。"},
        {"q": "計算 $12 \div (-3) \times 4$？", "options": ["-16", "-1", "16", "1"], "ans": 0, "diff": "中等", "type": "單選", "expl": "由左而右運算：$-4 \times 4 = -16$ (不能先算後面乘法！)"}
    ],
    "七上：分數與指數律": [
        {"q": "計算 $\\frac{2}{3} + (-\\frac{1}{4})$？", "options": ["5/12", "3/7", "1/12", "11/12"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "通分母為 12：$\\frac{8}{12} - \\frac{3}{12} = \\frac{5}{12}$。"},
        {"q": "下列何者錯誤？", "options": ["$2^3 \times 2^2 = 2^5$", "$(2^3)^2 = 2^6$", "$2^0 = 1$", "$2^3 + 2^3 = 2^6$"], "ans": 3, "diff": "中等", "type": "單選", "expl": "$2^3 + 2^3 = 2 \times 2^3 = 2^4 \ne 2^6$ (相加不能指數相加)。"}
    ],
    "七上：一元一次方程式": [
        {"q": "化簡 $5(x-2) - 2(2x+1)$？", "options": ["$x-12$", "$x-8$", "$9x-12$", "$x+8$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$5x - 10 - 4x - 2 = x - 12$。"},
        {"q": "解方程式 $\\frac{x}{3} + 1 = x - 3$？", "options": ["6", "4", "2", "-6"], "ans": 0, "diff": "中等", "type": "單選", "expl": "同乘 3：$x + 3 = 3x - 9 \Rightarrow 12 = 2x \Rightarrow x = 6$。"},
        {"q": "父親今年 40 歲，兒子 10 歲，幾年後父親年齡是兒子的 3 倍？", "options": ["5", "8", "10", "15"], "ans": 0, "diff": "中等", "type": "單選", "expl": "設 x 年後：$40+x = 3(10+x) \Rightarrow 40+x = 30+3x \Rightarrow 10=2x \Rightarrow x=5$。"}
    ],
    "七下：二元一次聯立方程式": [
        {"q": "解 $\\begin{cases} x+y=5 \\\\ x-y=1 \\end{cases}$，$(x, y)$？", "options": ["(3, 2)", "(2, 3)", "(4, 1)", "(1, 4)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "相加：$2x=6 \Rightarrow x=3$。代回 $y=2$。"}
    ],
    "七下：坐標與函數圖形": [
        {"q": "【圖解題】點 P 在第三象限，其坐標特性？", "options": ["(+,+)", "(-,+)", "(-,-)", "(+,-)"], "ans": 2, "diff": "簡單", "type": "單選", "svg": "coordinate_q2", "expl": "左(-)、下(-)。"},
        {"q": "【圖解題】參考一次函數圖形，直線與 y 軸交點稱為？", "options": ["y截距", "x截距", "斜率", "原點"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "linear_graph", "expl": "與 y 軸的交點即為 y 截距 (當 x=0 時)。"},
        {"q": "方程式 $y=3$ 的圖形是？", "options": ["水平線", "鉛垂線", "斜線", "拋物線"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "y 永遠是 3，為水平線。"}
    ],

    # ---------------- 國二 (八年級) ----------------
    "八上：乘法公式與多項式": [
        {"q": "展開 $(a-b)^2$？", "options": ["$a^2-b^2$", "$a^2+b^2$", "$a^2-2ab+b^2$", "$a^2+2ab+b^2$"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "差平方公式。"},
        {"q": "計算 $199^2$？", "options": ["39601", "39999", "39901", "39801"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$(200-1)^2 = 40000 - 400 + 1 = 39601$。"}
    ],
    "八上：平方根與畢氏定理": [
        {"q": "【圖解題】直角三角形兩股為 5, 12，斜邊？", "options": ["13", "17", "10", "15"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "pythagoras_visual", "expl": "$\sqrt{5^2+12^2} = 13$。"},
        {"q": "【圖解題】若直角三角形斜邊為 10，一股為 6，參考圖形概念，另一股為？", "options": ["8", "4", "2", "12"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "pythagoras_visual", "expl": "$\sqrt{10^2-6^2} = \sqrt{64} = 8$。"},
        {"q": "計算 $\sqrt{20}$ 化簡後？", "options": ["$2\sqrt{5}$", "$5\sqrt{2}$", "$4\sqrt{5}$", "10"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$20 = 4 \times 5$，4 開出來是 2。"}
    ],
    "八上：因式分解": [
        {"q": "分解 $x^2 - 25$？", "options": ["$(x-5)^2$", "$(x+5)(x-5)$", "$(x+25)(x-1)$", "無法分解"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "平方差：$a^2-b^2 = (a+b)(a-b)$。"},
        {"q": "分解 $x^2 + 5x + 6$？", "options": ["$(x+2)(x+3)$", "$(x+1)(x+6)$", "$(x-2)(x-3)$", "$(x-1)(x-6)$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "積 6 和 5 $\Rightarrow$ 2, 3。"}
    ],
    "八下：等差數列與級數": [
        {"q": "數列 2, 5, 8, ... 第 20 項？", "options": ["59", "60", "62", "57"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$a_{20} = 2 + 19 \times 3 = 59$。"},
        {"q": "級數 1+2+...+100？", "options": ["5050", "5000", "5100", "10100"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "梯形公式：$(1+100) \times 100 \div 2 = 5050$。"}
    ],
    "八下：幾何圖形與性質": [
        {"q": "【圖解題】L1//L2，內錯角 ∠1, ∠2 關係？", "options": ["相等", "互補", "互餘", "無關"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "parallel_lines", "expl": "平行線內錯角相等。"},
        {"q": "正五邊形的「內角和」度數？", "options": ["540", "720", "360", "180"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$(5-2) \times 180 = 540$。"}
    ],

    # ---------------- 國三 (九年級) ----------------
    "九上：相似形": [
        {"q": "【圖解題】參考相似三角形圖形，若邊長放大 2 倍，面積會放大幾倍？", "options": ["2倍", "4倍", "8倍", "不變"], "ans": 1, "diff": "簡單", "type": "單選", "svg": "similar_triangles", "expl": "面積比 = 邊長比的平方 ($2^2 = 4$)。"},
        {"q": "地圖比例尺 1:100，圖上 2cm 代表實際？", "options": ["2m", "200m", "20m", "0.2m"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "200 cm = 2 m。"}
    ],
    "九上：圓的性質": [
        {"q": "【圖解題】切線 L 與半徑 OP 的夾角？", "options": ["90度", "60度", "45度", "180度"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "circle_tangent", "expl": "切線垂直半徑。"},
        {"q": "【圖解題】參考圖形，對同一個弧，圓心角是圓周角的幾倍？", "options": ["2倍", "1/2倍", "相等", "3倍"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "circle_angles", "expl": "圓心角度數 = 所對弧度數 = 2 * 圓周角度數。"},
        {"q": "圓內接四邊形對角關係？", "options": ["互補", "相等", "互餘", "無關"], "ans": 0, "diff": "中等", "type": "單選", "expl": "對角和 180 度。"}
    ],
    "九上：三角形三心": [
        {"q": "「重心」是哪三線交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "重心分中線為 2:1。"},
        {"q": "「內心」到三角形哪裡距離相等？", "options": ["三邊", "三頂點", "三高", "重心"], "ans": 0, "diff": "中等", "type": "單選", "expl": "內心是內切圓圓心，到三邊等距 (半徑)。"}
    ],
    "九下：二次函數": [
        {"q": "【圖解題】開口向上的拋物線，係數 a？", "options": ["正", "負", "0", "無法判斷"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "parabola_visual", "expl": "a > 0 開口向上，有最小值。"},
        {"q": "函數 $y=(x-3)^2+5$ 的頂點？", "options": ["(3, 5)", "(-3, 5)", "(3, -5)", "(-3, -5)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "頂點式 $(h, k)$。"}
    ],
    "九下：統計與機率": [
        {"q": "投擲一枚硬幣 3 次，恰好 1 正 2 反的機率？", "options": ["3/8", "1/8", "1/2", "1/4"], "ans": 0, "diff": "困難", "type": "單選", "expl": "(正反反, 反正反, 反反正) 共 3 種。全部 $2^3=8$ 種。機率 3/8。"},
        {"q": "資料：10, 20, 20, 30, 40，眾數是？", "options": ["20", "30", "24", "10"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "出現次數最多的數。"}
    ]
}

# ==========================================
# 3. APP 主程式邏輯
# ==========================================
def reset_exam():
    """切換單元時重置狀態"""
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：視覺增強版", page_icon="📐", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("📐 數學單元 (視覺加強)")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("選擇單元", unit_options, on_change=reset_exam)
    st.sidebar.info("💡 此版本增加了更多幾何觀念的視覺輔助圖形。")

    st.title("📐 國中數學：視覺增強版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    # 考試首頁
    if not st.session_state.exam_started:
        st.info(f"準備練習：**{selected_unit}**")
        st.write("系統將隨機抽出 10 題進行測驗。")
        
        if st.button("🎲 隨機抽題開始", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            
            all_questions = MATH_DB.get(selected_unit, [])
            num_to_pick = min(len(all_questions), 10)
            if num_to_pick == 0:
                st.error("此單元暫無題目")
            else:
                selected_q = random.sample(all_questions, num_to_pick)
                st.session_state.current_questions = selected_q
                st.session_state.exam_started = True
                st.rerun()

    # 考試進行中
    else:
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"進度：0/{total_q}")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # 顯示 SVG
                if "svg" in q and q["svg"] in SVG_ASSETS:
                    st.markdown(SVG_ASSETS[q["svg"]], unsafe_allow_html=True)
                    st.caption("👆 請參考圖形作答")
                
                st.markdown(f"### {q['q']}")
                st.radio("選項", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            # 交卷
            if st.form_submit_button("✅ 交卷看成績", use_container_width=True):
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

        # 結果頁面
        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            
            st.markdown("---")
            if final_score == 100: st.success(f"💯 滿分！觀念很清楚喔！")
            elif final_score >= 60: st.info(f"👍 及格了！")
            else: st.error(f"💪 請務必看下方圖解訂正！")
            
            st.markdown(f"### 得分：{final_score} 分")

            for i, item in enumerate(res['details']):
                q_data = item['q']
                with st.expander(f"第 {i+1} 題詳解 ({'✅' if item['is_correct'] else '❌'})"):
                    # 詳解也要顯示圖
                    if "svg" in q_data and q_data["svg"] in SVG_ASSETS:
                         st.markdown(SVG_ASSETS[q_data["svg"]], unsafe_allow_html=True)
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.markdown(f"**💡 解析**：")
                    st.latex(q_data['expl'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 再刷一次 (題目變換)", use_container_width=True):
                    all_questions = MATH_DB.get(selected_unit, [])
                    num_to_pick = min(len(all_questions), 10)
                    st.session_state.current_questions = random.sample(all_questions, num_to_pick)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 換單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
