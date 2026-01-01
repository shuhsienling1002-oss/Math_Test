import streamlit as st
import random

# ==========================================
# 1. 內嵌視覺圖庫 (SVG Assets) - 幾何單元專用
# ==========================================
SVG_ASSETS = {
    # 數線與距離
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
    # 坐標象限
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
    # 畢氏定理
    "pythagoras_visual": """
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
         <polygon points="50,150 250,150 50,50" style="fill:lightblue;stroke:black;stroke-width:2" />
         <rect x="50" y="130" width="20" height="20" style="fill:none;stroke:black;stroke-width:1"/>
         <text x="150" y="170" text-anchor="middle" font-size="14">股 a = 12</text>
         <text x="30" y="100" text-anchor="end" font-size="14">股 b = 5</text>
         <text x="160" y="90" text-anchor="start" font-size="16" fill="red" font-weight="bold">斜邊 c = ?</text>
        </svg>
    """,
    # 平行線
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
    # 二次函數
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
    # 圓的切線
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
# 2. 旗艦級題庫 (按 108 課綱細分)
# ==========================================
MATH_DB = {
    # ================= 國一 (七年級) =================
    "七上：整數的運算與絕對值": [
        {"q": "計算 $(-15) + 8 - (-5)$ 的值？", "options": ["-2", "-12", "2", "-28"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "負負得正：$-15 + 8 + 5 = -15 + 13 = -2$"},
        {"q": "若 $|a| = 6$，則 $a$ 的值可能為？", "options": ["6", "-6", "6 或 -6", "0"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "絕對值代表距離，距離為 6 的點有兩個：6 和 -6。"},
        {"q": "【圖解題】參考數線圖，-4 到 3 的距離？", "options": ["1", "7", "-1", "-7"], "ans": 1, "diff": "簡單", "type": "單選", "svg": "number_line_dist", "expl": "距離 = 大減小 = $3 - (-4) = 7$。"},
        {"q": "計算 $(-2)^3 \times (-3)^2$？", "options": ["72", "-72", "36", "-36"], "ans": 1, "diff": "中等", "type": "單選", "expl": "$(-8) \times 9 = -72$ (負數的奇次方為負)。"}
    ],
    "七上：分數的運算 (含指數)": [
        {"q": "計算 $\\frac{2}{3} + (-\\frac{1}{4})$？", "options": ["5/12", "3/7", "1/12", "11/12"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "通分母為 12：$\\frac{8}{12} - \\frac{3}{12} = \\frac{5}{12}$。"},
        {"q": "計算 $(-\\frac{3}{2})^2 \div (-\\frac{9}{4})$？", "options": ["1", "-1", "2/3", "-9/8"], "ans": 1, "diff": "中等", "type": "單選", "expl": "$\\frac{9}{4} \times (-\\frac{4}{9}) = -1$。"},
        {"q": "若 $2^{-2}$ 代表什麼？", "options": ["-4", "1/4", "-1/4", "0"], "ans": 1, "diff": "中等", "type": "單選", "expl": "負指數代表倒數，$2^{-2} = \\frac{1}{2^2} = \\frac{1}{4}$。"}
    ],
    "七上：一元一次方程式": [
        {"q": "化簡 $5(x-2) - 2(2x+1)$？", "options": ["$x-12$", "$x-8$", "$9x-12$", "$x+8$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$5x - 10 - 4x - 2 = x - 12$。"},
        {"q": "解方程式 $\\frac{x}{3} + 1 = x - 3$？", "options": ["6", "4", "2", "-6"], "ans": 0, "diff": "中等", "type": "單選", "expl": "同乘 3：$x + 3 = 3x - 9 \\Rightarrow 12 = 2x \\Rightarrow x = 6$。"},
        {"q": "甲比乙大 5 歲，兩人年齡和為 35，求乙幾歲？", "options": ["15", "20", "10", "12"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "設乙 $x$，甲 $x+5$。$x + (x+5) = 35 \\Rightarrow 2x = 30 \\Rightarrow x=15$。"}
    ],
    "七下：二元一次聯立方程式": [
        {"q": "化簡 $3(x+y) - 2(x-y)$？", "options": ["$x+5y$", "$x+y$", "$5x+y$", "$x-5y$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$3x + 3y - 2x + 2y = x + 5y$。"},
        {"q": "解聯立方程式 $\\begin{cases} x+y=5 \\\\ x-y=1 \\end{cases}$，則 $(x, y)=？$", "options": ["(3, 2)", "(2, 3)", "(4, 1)", "(1, 4)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "兩式相加得 $2x=6 \Rightarrow x=3$。代回得 $y=2$。"}
    ],
    "七下：直角坐標與二元一次方程式圖形": [
        {"q": "【圖解題】點 P 在左下方 (第三象限)，坐標特徵？", "options": ["(+,+)", "(-,+)", "(-,-)", "(+,-)"], "ans": 2, "diff": "簡單", "type": "單選", "svg": "coordinate_q2", "expl": "左為負，下為負，故 (-,-)。"},
        {"q": "方程式 $y=3$ 的圖形是？", "options": ["垂直 x 軸的直線", "垂直 y 軸的水平線", "通過原點的斜線", "拋物線"], "ans": 1, "diff": "中等", "type": "單選", "expl": "y 坐標永遠是 3，是一條水平線。"},
        {"q": "點 A(2, -3) 到 x 軸的距離？", "options": ["2", "3", "-3", "5"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "到 x 軸看 y 坐標絕對值，$|-3| = 3$。"}
    ],
    "七下：比例與不等式": [
        {"q": "若 $x:y = 3:4$，且 $x=9$，求 $y$？", "options": ["12", "16", "9", "3"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$9:y = 3:4 \Rightarrow 3y = 36 \Rightarrow y=12$ (內項乘積=外項乘積)。"},
        {"q": "解不等式 $-2x < 10$？", "options": ["$x < -5$", "$x > -5$", "$x < 5$", "$x > 5$"], "ans": 1, "diff": "中等", "type": "單選", "expl": "除以負數，開口要變號！$x > -5$。"}
    ],

    # ================= 國二 (八年級) =================
    "八上：乘法公式與多項式": [
        {"q": "展開 $(a-b)^2$？", "options": ["$a^2-b^2$", "$a^2+b^2$", "$a^2-2ab+b^2$", "$a^2+2ab+b^2$"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "差的平方公式。"},
        {"q": "計算 $99^2$？", "options": ["9801", "9901", "9999", "9981"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$(100-1)^2 = 10000 - 200 + 1 = 9801$。"},
        {"q": "若多項式 A 除以 B，商為 Q，餘式為 R，則？", "options": ["$A = B \\times Q + R$", "$A = B \\times Q - R$", "$A = B / Q + R$", "$A = Q \times R + B$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "除法原理：被除式 = 除式 × 商式 + 餘式。"}
    ],
    "八上：平方根與畢氏定理": [
        {"q": "【圖解題】直角三角形兩股 5, 12，斜邊？", "options": ["13", "17", "10", "15"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "pythagoras_visual", "expl": "$\sqrt{5^2+12^2} = 13$。"},
        {"q": "計算 $\sqrt{18} + \sqrt{2}$？", "options": ["$\sqrt{20}$", "$4\sqrt{2}$", "$3\sqrt{2}$", "$2\sqrt{5}$"], "ans": 1, "diff": "中等", "type": "單選", "expl": "$\sqrt{18} = 3\sqrt{2}$，故 $3\sqrt{2} + 1\sqrt{2} = 4\sqrt{2}$。"},
        {"q": "坐標平面上，(1, 1) 與 (4, 5) 的距離？", "options": ["5", "4", "3", "7"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$\sqrt{(4-1)^2 + (5-1)^2} = \sqrt{3^2+4^2} = 5$。"}
    ],
    "八上：因式分解": [
        {"q": "因式分解 $x^2 - 9$？", "options": ["$(x-3)^2$", "$(x+3)(x-3)$", "$(x-9)(x+1)$", "$(x+9)(x-1)$"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "平方差公式 $a^2-b^2 = (a+b)(a-b)$。"},
        {"q": "因式分解 $x^2 + 5x + 6$？", "options": ["$(x+2)(x+3)$", "$(x+1)(x+6)$", "$(x-2)(x-3)$", "$(x+5)(x+1)$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "十字交乘：積為 6，和為 5 $\Rightarrow$ 2, 3。"}
    ],
    "八下：等差數列與級數": [
        {"q": "數列 1, 4, 7, 10, ... 第 10 項是？", "options": ["28", "30", "29", "31"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$a_{10} = 1 + (10-1) \times 3 = 28$。"},
        {"q": "等差級數 1+2+...+20 的和？", "options": ["200", "210", "190", "220"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "梯形公式：$\\frac{(1+20) \times 20}{2} = 210$。"}
    ],
    "八下：幾何圖形與平行線": [
        {"q": "【圖解題】L1//L2，∠1 與 ∠2 是內錯角，關係是？", "options": ["相等", "互補", "互餘", "沒關係"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "parallel_lines", "expl": "平行線內錯角相等。"},
        {"q": "n 邊形內角和公式？", "options": ["$(n-2) \times 180$", "$n \times 180$", "$(n-2) \times 360$", "360"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "可以切成 n-2 個三角形。"},
        {"q": "下列何者「不一定」是全等三角形的性質？", "options": ["SSS", "SAS", "AAS", "SSA"], "ans": 3, "diff": "中等", "type": "單選", "expl": "SSA (邊邊角) 不一定全等，除非是 RHS (直角三角形)。"}
    ],

    # ================= 國三 (九年級) =================
    "九上：相似形": [
        {"q": "兩相似三角形對應邊長比 1:3，面積比？", "options": ["1:3", "1:6", "1:9", "3:1"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "面積比 = 邊長比的平方 ($1^2 : 3^2 = 1:9$)。"},
        {"q": "地圖比例尺 1:10000，地圖上 1cm 代表實際？", "options": ["100m", "1km", "10m", "1000m"], "ans": 0, "diff": "中等", "type": "單選", "expl": "10000 cm = 100 m。"}
    ],
    "九上：圓的性質": [
        {"q": "【圖解題】切線 L 與半徑 OP 的夾角？", "options": ["90度", "60度", "45度", "180度"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "circle_tangent", "expl": "切線半徑必垂直。"},
        {"q": "同一圓中，弦心距越長，對應的弦長？", "options": ["越短", "越長", "不變", "無法判斷"], "ans": 0, "diff": "中等", "type": "單選", "expl": "弦心距越長，代表弦離圓心越遠，弦就越短。"},
        {"q": "圓內接四邊形，其對角關係？", "options": ["互補 (相加180)", "相等", "互餘", "無關"], "ans": 0, "diff": "中等", "type": "單選", "expl": "圓內接四邊形對角互補。"}
    ],
    "九上：三角形的三心": [
        {"q": "三角形的「重心」是哪三條線的交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "重心：中線交點 (分中線為 2:1)。"},
        {"q": "直角三角形的外心在哪裡？", "options": ["斜邊中點", "三角形內部", "三角形外部", "直角頂點"], "ans": 0, "diff": "中等", "type": "單選", "expl": "直角三角形外接圓圓心在斜邊中點。"}
    ],
    "九下：二次函數": [
        {"q": "【圖解題】開口向上的拋物線，a 值？", "options": ["正數", "負數", "0", "無法判斷"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "parabola_visual", "expl": "a > 0 開口向上 (有最小值)。"},
        {"q": "函數 $y = (x-2)^2 + 3$ 的頂點？", "options": ["(2, 3)", "(-2, 3)", "(2, -3)", "(-2, -3)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "頂點式 $(h, k)$。"}
    ],
    "九下：統計與機率": [
        {"q": "丟一枚硬幣 2 次，兩次都正面的機率？", "options": ["1/4", "1/2", "3/4", "1"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "1/2 * 1/2 = 1/4。"},
        {"q": "資料：2, 4, 6, 8, 10，中位數是？", "options": ["6", "5", "4", "8"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "正中間的數。"},
        {"q": "盒中有 2 紅 3 白球，抽中紅球機率？", "options": ["2/5", "3/5", "1/2", "1/5"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "紅球數 / 總球數。"}
    ]
}

# ==========================================
# 3. APP 主程式邏輯 (視覺 + 單元細分)
# ==========================================
def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：全單元旗艦版", page_icon="🎓", layout="centered")
    
    # 狀態初始化
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    # 側邊欄
    st.sidebar.title("📚 國中數學單元選單")
    st.sidebar.caption("依據 108 課綱細分")
    
    # 建立選單 (分類更細)
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 每個單元都有重點練習，包含視覺化圖解題！")

    st.title("🎓 國中數學：全單元旗艦版")
    st.caption(f"目前選擇單元：{selected_unit}")

    # 考試首頁
    if not st.session_state.exam_started:
        st.info(f"準備好挑戰 **{selected_unit}** 了嗎？")
        st.markdown("這個單元包含：觀念檢測、計算練習與圖形判斷。")
        if st.button("🚀 載入題庫開始", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            
            # 載入題目
            questions = MATH_DB.get(selected_unit, [])
            random.shuffle(questions) # 隨機排序
            
            if not questions:
                st.error("此單元暫無題目")
            else:
                st.session_state.current_questions = questions
                st.session_state.exam_started = True
                st.rerun()

    # 考試進行中
    else:
        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # 顯示 SVG 圖形 (如果有)
                if "svg" in q and q["svg"] in SVG_ASSETS:
                    st.markdown(SVG_ASSETS[q["svg"]], unsafe_allow_html=True)
                    st.caption("👆 請參考上方圖形作答")
                
                # 顯示 LaTeX 題目
                st.markdown(f"### {q['q']}") 
                
                st.radio("選項：", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            # 交卷
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

        # 結果頁面
        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            
            st.markdown("---")
            if final_score == 100: st.success(f"💯 該單元完全精通！ ({final_score}分)")
            elif final_score >= 60: st.info(f"👍 通過標準，觀念不錯！ ({final_score}分)")
            else: st.error(f"💪 這個單元要再複習一下喔！ ({final_score}分)")
            
            for i, item in enumerate(res['details']):
                q_data = item['q']
                with st.expander(f"第 {i+1} 題詳解 ({'✅ 對' if item['is_correct'] else '❌ 錯'})"):
                    if "svg" in q_data and q_data["svg"] in SVG_ASSETS:
                         st.markdown(SVG_ASSETS[q_data["svg"]], unsafe_allow_html=True)
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.markdown(f"**💡 解析**：")
                    st.latex(q_data['expl']) # 支援 LaTeX 解析

            if st.button("🔄 重新練習此單元"):
                reset_exam()
                st.rerun()

            if st.button("⬅️ 回首頁選擇其他單元"):
                reset_exam()
                st.rerun()

if __name__ == "__main__":
    main()
