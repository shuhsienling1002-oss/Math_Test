import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# ==========================================
# 1. 自動繪圖引擎 (Math Plotter)
# 不用準備圖片檔，程式現場畫給你看！
# ==========================================
def draw_math_figure(fig_type):
    """根據題目類型，自動生成數學圖形"""
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # 設定通用樣式
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    if fig_type == "parabola_up": # 開口向上的拋物線
        x = np.linspace(-3, 3, 100)
        y = x**2 - 2
        ax.plot(x, y, 'b-', label='y = x² - 2')
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.set_title("y = ax² + k (a>0)")
        
    elif fig_type == "parabola_down": # 開口向下的拋物線
        x = np.linspace(-3, 3, 100)
        y = -1 * x**2 + 2
        ax.plot(x, y, 'r-', label='y = -x² + 2')
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.set_title("y = ax² + k (a<0)")

    elif fig_type == "coordinate_point": # 直角坐標點
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.plot(2, 3, 'ro') # 第一象限
        ax.text(2.2, 3, "A(2, 3)", fontsize=12)
        ax.plot(-3, -2, 'bo') # 第三象限
        ax.text(-3.2, -1.8, "B(-3, -2)", fontsize=12)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_title("Cartesian Coordinate System")

    elif fig_type == "triangle": # 直角三角形
        triangle = patches.Polygon([[0, 0], [4, 0], [0, 3]], closed=True, fill=True, alpha=0.3, edgecolor='black')
        ax.add_patch(triangle)
        ax.text(2, -0.5, "4 (a)", fontsize=12, ha='center')
        ax.text(-0.5, 1.5, "3 (b)", fontsize=12, va='center')
        ax.text(2.2, 1.7, "? (c)", fontsize=12, color='red')
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.set_title("Right Triangle")

    elif fig_type == "linear_function": # 線性函數
        x = np.linspace(-5, 5, 10)
        y = 2*x + 1
        ax.plot(x, y, 'g-', label='y = ax + b')
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.set_title("Linear Function")

    return fig

# ==========================================
# 2. 國中數學海量題庫 (含 img_tag 標記)
# ==========================================
MATH_DB = {
    "國一數學 (七年級)": [
        # --- 整數運算 ---
        {"q": "計算 $(-12) + 5 - (-8)$ 的值？", "options": ["1", "-1", "-15", "25"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$-12 + 5 + 8 = -12 + 13 = 1$"},
        {"q": "若 $|a| = 3, |b| = 7$，且 $ab < 0$，則 $a + b$ 可能為？", "options": ["4 或 -4", "10 或 -10", "4", "-4"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$ab<0$ 表異號。若 $a=3, b=-7 \Rightarrow -4$；若 $a=-3, b=7 \Rightarrow 4$。"},
        {"q": "計算 $18 \div (-3)^2 \times 2$？", "options": ["4", "-4", "1", "-12"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$18 \div 9 \times 2 = 2 \times 2 = 4$ (注意運算順序：先乘方，再乘除)"},
        # --- 指數律 ---
        {"q": "下列何者錯誤？", "options": ["$2^3 \times 2^4 = 2^7$", "$(2^3)^4 = 2^{12}$", "$2^0 = 0$", "$2^{-1} = 1/2$"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "任何非零數的 0 次方皆為 1，故 $2^0 = 1$。"},
        {"q": "若 $3^x = 81$，則 $x$ 為？", "options": ["3", "4", "5", "27"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "$81 = 9 \times 9 = 3^2 \times 3^2 = 3^4$"},
        # --- 代數與方程式 ---
        {"q": "化簡 $3(2x - 1) - 2(3x + 4)$？", "options": ["$-11$", "-5", "$12x - 11$", "$-5x - 11$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$6x - 3 - 6x - 8 = -11$"},
        {"q": "解方程式 $\frac{x}{2} - \frac{x}{3} = 1$？", "options": ["1", "5", "6", "-6"], "ans": 2, "diff": "中等", "type": "單選", "expl": "同乘 6：$3x - 2x = 6 \Rightarrow x = 6$"},
        {"q": "父親今年 40 歲，兒子 10 歲，幾年後父親年齡是兒子的 3 倍？", "options": ["3", "5", "8", "10"], "ans": 1, "diff": "困難", "type": "單選", "expl": "設 $x$ 年後。$40+x = 3(10+x) \Rightarrow 40+x=30+3x \Rightarrow 10=2x \Rightarrow x=5$"},
        # --- 直角坐標 ---
        {"q": "參考下圖，若點 A 在第二象限，則其坐標符號為何？", "options": ["$(+, +)$", "$(-, +)$", "$(-, -)$", "$(+, -)$"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "第二象限為左上，故 x 為負，y 為正。", "img": "coordinate_point"},
        {"q": "點 $P(3, -4)$ 到 x 軸的距離為何？", "options": ["3", "4", "-4", "5"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "到 x 軸距離看 y 坐標的絕對值。$|-4| = 4$。"},
        {"q": "若 $y = ax + b$ 通過 $(0,0)$ 與 $(1,2)$，則 $a+b=$？", "options": ["0", "1", "2", "3"], "ans": 2, "diff": "中等", "type": "單選", "expl": "過 $(0,0) \Rightarrow b=0$。過 $(1,2) \Rightarrow a(1)=2 \Rightarrow a=2$。$a+b=2$", "img": "linear_function"}
    ],

    "國二數學 (八年級)": [
        # --- 乘法公式與多項式 ---
        {"q": "展開 $(a+b)(a-b)$？", "options": ["$a^2+b^2$", "$a^2-b^2$", "$a^2-2ab+b^2$", "$a^2+2ab+b^2$"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "平方差公式。"},
        {"q": "計算 $1002 \times 998 = ？$", "options": ["999996", "999994", "1000004", "99996"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$(1000+2)(1000-2) = 1000^2 - 2^2 = 1000000 - 4 = 999996$"},
        {"q": "若 $x^2 + 6x + k$ 是一個完全平方式，則 $k=？$", "options": ["3", "6", "9", "36"], "ans": 2, "diff": "中等", "type": "單選", "expl": "常數項應為一次項係數一半的平方。$(6/2)^2 = 3^2 = 9$。即 $(x+3)^2$。"},
        # --- 畢氏定理 (含圖) ---
        {"q": "如下圖，直角三角形兩股為 3, 4，求斜邊長？", "options": ["5", "6", "7", "$\sqrt{7}$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$\sqrt{3^2+4^2} = \sqrt{9+16} = \sqrt{25} = 5$", "img": "triangle"},
        {"q": "直角三角形斜邊為 10，一股為 6，求另一股？", "options": ["4", "8", "12", "$\sqrt{136}$"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "$\sqrt{10^2 - 6^2} = \sqrt{100-36} = \sqrt{64} = 8$"},
        # --- 因式分解 ---
        {"q": "因式分解 $3x^2 - 3$？", "options": ["$3(x-1)^2$", "$3(x+1)(x-1)$", "$(3x+1)(x-1)$", "$3(x^2-1)$ (尚未完全分解)"], "ans": 1, "diff": "中等", "type": "單選", "expl": "提公因式 3 $\Rightarrow 3(x^2-1)$ $\Rightarrow$ 平方差 $3(x+1)(x-1)$"},
        {"q": "十字交乘：$x^2 - 7x + 12$ 因式分解為？", "options": ["$(x-3)(x-4)$", "$(x+3)(x+4)$", "$(x-2)(x-6)$", "$(x-1)(x-12)$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "積 12，和 -7 $\Rightarrow -3, -4$。"},
        # --- 數列與級數 ---
        {"q": "等差數列 $2, 5, 8, ...$ 第 10 項為何？", "options": ["29", "30", "32", "27"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$a_{10} = 2 + (10-1) \times 3 = 2 + 27 = 29$"},
        {"q": "求等差級數 $1 + 2 + 3 + ... + 10$ 之和？", "options": ["50", "55", "60", "45"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "梯形公式 $\\frac{(1+10) \times 10}{2} = 55$"}
    ],

    "國三數學 (九年級)": [
        # --- 二次函數 (含圖) ---
        {"q": "參考下圖，關於函數 $y = x^2 - 2$ 的敘述何者正確？", "options": ["開口向上，有最小值 -2", "開口向下，有最大值 -2", "開口向上，有最大值 2", "頂點在 (2, 0)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "係數 $a=1>0$ 故開口向上，頂點 $(0, -2)$ 為最低點。", "img": "parabola_up"},
        {"q": "若二次函數 $y = -2(x-1)^2 + 3$，其頂點坐標為？", "options": ["(1, 3)", "(-1, 3)", "(1, -3)", "(-1, -3)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "頂點式 $y=a(x-h)^2+k$ $\Rightarrow (h,k)=(1,3)$"},
        # --- 幾何與圓 ---
        {"q": "三角形的重心是哪三條線的交點？", "options": ["中線", "角平分線 (內心)", "中垂線 (外心)", "高 (垂心)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "重心是三條中線的交點，性質是重心到頂點距離為中線長的 2/3。"},
        {"q": "若兩圓半徑分別為 5, 3，圓心距為 10，則兩圓位置關係？", "options": ["外離", "外切", "相交", "內含"], "ans": 0, "diff": "中等", "type": "單選", "expl": "圓心距 $10 > 5+3$ (半徑和)，故兩圓分開，為外離。"},
        {"q": "一扇形半徑為 6，圓心角 $60^\circ$，求扇形面積？", "options": ["$6\pi$", "$12\pi$", "$3\pi$", "$36\pi$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "圓面積 $\times$ 比例。$36\pi \times \frac{60}{360} = 6\pi$"},
        # --- 機率與統計 ---
        {"q": "投擲一枚公正硬幣 3 次，出現「三正」的機率？", "options": ["1/2", "1/4", "1/8", "3/8"], "ans": 2, "diff": "困難", "type": "單選", "expl": "$(1/2) \times (1/2) \times (1/2) = 1/8$"},
        {"q": "盒中有 3 紅球、2 白球，隨機取一球為紅球的機率？", "options": ["3/5", "2/5", "1/2", "1/3"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "紅球數 / 總球數 = $3 / (3+2) = 3/5$"},
        {"q": "關於『中位數』的敘述，何者正確？", "options": ["資料由小到大排列，位於正中央的數", "出現次數最多的數 (眾數)", "所有數加總除以個數 (平均數)", "最大值減最小值 (全距)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "定義題。"},
        # --- 相似形 ---
        {"q": "若 $\Delta ABC \sim \Delta DEF$，且對應邊 $AB:DE = 1:2$，則面積比為何？", "options": ["1:2", "1:4", "1:8", "1:1.5"], "ans": 1, "diff": "中等", "type": "單選", "expl": "相似三角形面積比 = 邊長比的平方。$1^2 : 2^2 = 1:4$"}
    ]
}

# ==========================================
# 3. APP 主程式邏輯
# ==========================================
def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.user_answers = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學豪華版", page_icon="📐")
    
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'exam_results' not in st.session_state:
        st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state:
        st.session_state.exam_finished = False

    st.sidebar.title("🧮 數學練習設定")
    grade_level = st.sidebar.selectbox("1. 選擇年級", list(MATH_DB.keys()), on_change=reset_exam)
    difficulty = st.sidebar.radio("2. 選擇難度", ["簡單", "中等", "困難"], index=1, on_change=reset_exam)
    
    st.title("📐 國中數學總複習系統")
    st.markdown("### 觀念 $\\times$ 計算 $\\times$ 圖形解析")
    
    if not st.session_state.exam_started:
        st.info(f"準備單元：**{grade_level}** ({difficulty})")
        if st.button("🚀 生成試卷", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 

            raw_questions = MATH_DB.get(grade_level, [])
            filtered_q = []
            for q in raw_questions:
                if difficulty == "簡單" and q['diff'] != "簡單": continue
                if difficulty == "中等" and q['diff'] == "困難": continue
                filtered_q.append(q)
            
            if not filtered_q:
                st.warning("題庫擴充中，請選擇其他難度！")
            else:
                random.shuffle(filtered_q)
                st.session_state.current_questions = filtered_q
                st.session_state.user_answers = {}
                st.session_state.exam_started = True
                st.rerun()

    else:
        st.subheader(f"📝 {grade_level}")
        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # 自動繪圖偵測：如果題目有 img 標籤，就畫圖！
                if "img" in q:
                    fig = draw_math_figure(q["img"])
                    st.pyplot(fig)
                
                st.markdown(f"### {q['q']}") 
                st.radio("答案：", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            submitted = st.form_submit_button("✅ 交卷看詳解", use_container_width=True)
            
            if submitted:
                score = 0
                results = []
                for idx, q in enumerate(questions):
                    q_key = f"q_{idx}"
                    user_ans = st.session_state.get(q_key)
                    correct_ans = q['options'][q['ans']]
                    is_correct = (user_ans == correct_ans)
                    if is_correct: score += 1
                    results.append({"q": q['q'], "is_correct": is_correct, "user": user_ans, "correct": correct_ans, "expl": q['expl']})

                st.session_state.exam_results = {"score": score, "total": len(questions), "details": results}
                st.session_state.exam_finished = True

        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            
            st.markdown("---")
            if final_score >= 90: st.success(f"💯 滿分！太強了！ ({final_score}分)")
            elif final_score >= 60: st.info(f"👍 及格！ ({final_score}分)")
            else: st.error(f"💪 再加油！ ({final_score}分)")
            
            for i, item in enumerate(res['details']):
                with st.expander(f"第 {i+1} 題詳解 ({'✅ 對' if item['is_correct'] else '❌ 錯'})"):
                    st.write(f"題目：{item['q']}")
                    st.write(f"正解：{item['correct']}")
                    st.markdown(f"**💡 解析：**")
                    st.latex(item['expl'])

            if st.button("🔄 再考一次"):
                reset_exam()
                st.rerun()

if __name__ == "__main__":
    main()
