import streamlit as st
import random
import datetime

# ==========================================
# 1. 國中數學題庫 (含 LaTeX 數學公式與詳解)
# ==========================================
MATH_DB = {
    "國一數學 (七年級)": [
        # --- 正負數與絕對值 ---
        {
            "q": "計算 $(-8) + |-5| - (-3)$ 的值為何？",
            "options": ["0", "-6", "-10", "6"],
            "ans": 0,
            "diff": "簡單",
            "type": "單選",
            "expl": "原式 = $-8 + 5 + 3 = 0$"
        },
        {
            "q": "若 $|a| = 5$，且 $|b| = 3$，若 $a < 0, b > 0$，則 $a + b = ？$",
            "options": ["2", "-2", "8", "-8"],
            "ans": 1,
            "diff": "中等",
            "type": "單選",
            "expl": "因為 $a<0, |a|=5 \\Rightarrow a=-5$。因為 $b>0, |b|=3 \\Rightarrow b=3$。故 $-5+3 = -2$。"
        },
        # --- 指數律 ---
        {
            "q": "計算 $(2^3)^2 \\times 2^4 \\div 2^5 = ？$",
            "options": ["$2^2$", "$2^4$", "$2^5$", "$2^6$"],
            "ans": 2,
            "diff": "中等",
            "type": "單選",
            "expl": "指數律：$(a^m)^n = a^{mn}$。原式 = $2^6 \\times 2^4 \\div 2^5 = 2^{6+4-5} = 2^5$。"
        },
        # --- 一元一次方程式 ---
        {
            "q": "解方程式 $3(x-2) = 2x + 1$，則 $x = ？$",
            "options": ["5", "7", "-5", "-7"],
            "ans": 1,
            "diff": "簡單",
            "type": "單選",
            "expl": "$3x - 6 = 2x + 1 \\Rightarrow 3x - 2x = 1 + 6 \\Rightarrow x = 7$。"
        },
        # --- 直角坐標 ---
        {
            "q": "若點 $P(a, b)$ 在第二象限，則點 $Q(ab, a-b)$ 在第幾象限？",
            "options": ["第一象限", "第二象限", "第三象限", "第四象限"],
            "ans": 2,
            "diff": "困難",
            "type": "單選",
            "expl": "第二象限 $(-, +) \\Rightarrow a<0, b>0$。則 $ab$ 為負 $(-)$，$a-b$ (負減正) 為負 $(-)$。故 $Q(-, -)$ 在第三象限。"
        }
    ],

    "國二數學 (八年級)": [
        # --- 乘法公式 ---
        {
            "q": "展開 $(2a - 3b)^2$ 的結果為何？",
            "options": ["$4a^2 - 9b^2$", "$4a^2 - 6ab + 9b^2$", "$4a^2 - 12ab + 9b^2$", "$2a^2 - 3b^2$"],
            "ans": 2,
            "diff": "簡單",
            "type": "單選",
            "expl": "公式 $(x-y)^2 = x^2 - 2xy + y^2$。故 $(2a)^2 - 2(2a)(3b) + (3b)^2 = 4a^2 - 12ab + 9b^2$。"
        },
        {
            "q": "計算 $199^2 - 1$ 的值？",
            "options": ["39600", "39900", "39999", "39601"],
            "ans": 0,
            "diff": "中等",
            "type": "單選",
            "expl": "平方差公式 $a^2 - b^2 = (a+b)(a-b)$。$199^2 - 1^2 = (199+1)(199-1) = 200 \\times 198 = 39600$。"
        },
        # --- 畢氏定理 ---
        {
            "q": "直角三角形兩股長分別為 5, 12，求斜邊長？",
            "options": ["13", "15", "17", "$\sqrt{119}$"],
            "ans": 0,
            "diff": "簡單",
            "type": "單選",
            "expl": "畢氏定理 $c = \\sqrt{a^2 + b^2} = \\sqrt{5^2 + 12^2} = \\sqrt{25+144} = \\sqrt{169} = 13$。"
        },
        # --- 因式分解 ---
        {
            "q": "因式分解 $x^2 - 5x + 6$？",
            "options": ["$(x-1)(x-6)$", "$(x-2)(x-3)$", "$(x+2)(x+3)$", "$(x-1)(x+5)$"],
            "ans": 1,
            "diff": "中等",
            "type": "單選",
            "expl": "十字交乘法：找兩數相乘為6，相加為-5，即 -2 與 -3。故 $(x-2)(x-3)$。"
        },
        # --- 等差數列 ---
        {
            "q": "一等差數列首項 $a_1=3$，公差 $d=4$，求第10項 $a_{10}$？",
            "options": ["36", "39", "40", "43"],
            "ans": 1,
            "diff": "中等",
            "type": "單選",
            "expl": "公式 $a_n = a_1 + (n-1)d$。$a_{10} = 3 + (10-1)\\times 4 = 3 + 36 = 39$。"
        }
    ],

    "國三數學 (九年級)": [
        # --- 二次函數 ---
        {
            "q": "關於二次函數 $y = 2(x-1)^2 + 3$，下列敘述何者正確？",
            "options": ["開口向下，頂點 (1, 3)", "開口向上，頂點 (-1, 3)", "開口向上，頂點 (1, 3)", "開口向下，頂點 (-1, 3)"],
            "ans": 2,
            "diff": "簡單",
            "type": "單選",
            "expl": "係數 $a=2>0$ 故開口向上。頂點式 $y=a(x-h)^2+k$，頂點為 $(h, k)$ 即 $(1, 3)$。"
        },
        {
            "q": "若 $y = x^2 - 4x + k$ 的圖形與 x 軸只有一個交點，求 k 值？",
            "options": ["2", "4", "-4", "0"],
            "ans": 1,
            "diff": "困難",
            "type": "單選",
            "expl": "判別式 $D = b^2 - 4ac = 0$。$(-4)^2 - 4(1)(k) = 0 \\Rightarrow 16 - 4k = 0 \\Rightarrow k=4$。"
        },
        # --- 機率與統計 ---
        {
            "q": "投擲一顆公正骰子，出現點數大於 4 的機率為何？",
            "options": ["$1/2$", "$1/3$", "$1/6$", "$2/3$"],
            "ans": 1,
            "diff": "簡單",
            "type": "單選",
            "expl": "大於 4 的點數有 5, 6 兩種。總樣本空間為 6。機率 $P = 2/6 = 1/3$。"
        },
        # --- 幾何圖形 (圓) ---
        {
            "q": "圓 $O$ 半徑為 10，圓心到直線 $L$ 的距離為 8，則直線 $L$ 與圓 $O$ 的關係為何？",
            "options": ["相交於兩點 (割線)", "相切 (切線)", "不相交 (外離)", "無法判斷"],
            "ans": 0,
            "diff": "中等",
            "type": "單選",
            "expl": "圓心距 $d=8$，半徑 $r=10$。因為 $d < r$ (8 < 10)，故直線穿過圓內部，交於兩點。"
        },
        # --- 三角形的心 ---
        {
            "q": "正三角形的重心、內心、外心，三者的位置關係為何？",
            "options": ["完全重合 (同一點)", "在同一直線上但不同點", "形成一個三角形", "沒有關係"],
            "ans": 0,
            "diff": "簡單",
            "type": "單選",
            "expl": "正三角形 (等邊三角形) 的外心、內心、重心、垂心四心合一。"
        }
    ]
}

# ==========================================
# 2. APP 邏輯 (Math Edition)
# ==========================================
def reset_exam():
    """重置考試狀態"""
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.user_answers = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學全能測驗", page_icon="🧮")
    
    # Session State 初始化
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'exam_results' not in st.session_state:
        st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state:
        st.session_state.exam_finished = False

    # 側邊欄
    st.sidebar.title("🧮 數學練習設定")
    
    # 選擇年級
    grade_level = st.sidebar.selectbox(
        "1. 選擇年級", 
        list(MATH_DB.keys()),
        on_change=reset_exam
    )
    
    # 選擇難度
    difficulty = st.sidebar.radio(
        "2. 選擇難度", 
        ["簡單", "中等", "困難"], 
        index=1,
        on_change=reset_exam
    )
    
    st.title("📐 國中數學全能測驗系統")
    st.markdown("### 觀念釐清 $\\times$ 計算實戰")
    
    # === 主頁面：準備開始 ===
    if not st.session_state.exam_started:
        st.info(f"準備進行：**{grade_level}**")
        st.markdown(f"難度：**{difficulty}**")
        st.write("準備好紙筆了嗎？點擊下方按鈕開始！")
        
        if st.button("🚀 開始計算", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 

            # 篩選題目
            raw_questions = MATH_DB.get(grade_level, [])
            filtered_q = []
            for q in raw_questions:
                if difficulty == "簡單" and q['diff'] != "簡單": continue
                if difficulty == "中等" and q['diff'] == "困難": continue
                filtered_q.append(q)
            
            if not filtered_q:
                st.warning("這個難度下暫時沒有題目，請選擇其他難度！")
            else:
                random.shuffle(filtered_q)
                st.session_state.current_questions = filtered_q
                st.session_state.user_answers = {}
                st.session_state.exam_started = True
                st.rerun()

    # === 考試頁面 ===
    else:
        st.subheader(f"📝 {grade_level}")
        
        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            
            for idx, q in enumerate(questions):
                # 使用 LaTeX 渲染題目
                st.markdown(f"**第 {idx+1} 題：**")
                st.markdown(f"### {q['q']}") 
                
                q_key = f"q_{idx}"
                
                # 選項顯示
                st.radio(
                    "請選擇答案：", 
                    q['options'], 
                    key=q_key, 
                    index=None, 
                    label_visibility="collapsed"
                )
                st.divider()

            submitted = st.form_submit_button("✅ 交卷看詳解", use_container_width=True)
            
            if submitted:
                score = 0
                results = []
                
                for idx, q in enumerate(questions):
                    q_key = f"q_{idx}"
                    user_selection = st.session_state.get(q_key)
                    
                    is_correct = False
                    user_ans_display = "未作答"
                    correct_ans_display = q['options'][q['ans']]
                    
                    if user_selection:
                        user_ans_display = user_selection
                        if user_selection == correct_ans_display:
                            is_correct = True
                            score += 1

                    # 紀錄結果與詳解
                    result_item = {
                        "q_idx": idx + 1,
                        "question": q['q'],
                        "is_correct": is_correct,
                        "user_ans": user_ans_display,
                        "correct_ans": correct_ans_display,
                        "expl": q.get('expl', '暫無詳解')
                    }
                    results.append(result_item)

                st.session_state.exam_results = {
                    "score": score,
                    "total": len(questions),
                    "details": results
                }
                st.session_state.exam_finished = True

        # === 顯示成績與詳解 ===
        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            if res['total'] > 0:
                final_score = int((res['score'] / res['total']) * 100)
            else:
                final_score = 0
            
            st.markdown("---")
            st.markdown("### 📊 測驗結果")
            
            if final_score == 100:
                st.balloons()
                st.success(f"太神了！滿分！ ({final_score} 分)")
            elif final_score >= 60:
                st.info(f"不錯喔，及格了！ ({final_score} 分)")
            else:
                st.error(f"要再加油喔！ ({final_score} 分)")
            
            st.markdown("### 🧐 題目解析")
            for item in res['details']:
                with st.container():
                    # 標題區塊
                    if item['is_correct']:
                        st.markdown(f"✅ **第 {item['q_idx']} 題：答對**")
                    else:
                        st.markdown(f"❌ **第 {item['q_idx']} 題：答錯**")
                    
                    # 題目與詳解區塊
                    st.info(f"題目：{item['question']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"你的答案：{item['user_ans']}")
                    with col2:
                        st.write(f"正確答案：{item['correct_ans']}")
                    
                    # 詳解 (重點功能)
                    st.markdown(f"**💡 解析：**")
                    st.latex(item['expl']) # 使用 latex 顯示數學詳解
                    st.divider()
            
            if st.button("🔄 重新測驗"):
                reset_exam()
                st.rerun()

if __name__ == "__main__":
    main()