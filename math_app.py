import streamlit as st
import json
import random
import os

# ==========================================
# 1. 資料讀取器 (DataLoader)
# ==========================================
class DataLoader:
    @staticmethod
    @st.cache_data
    def load_questions():
        file_path = "questions.json"
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None

# ==========================================
# 2. 視覺繪圖引擎 (SVGDrawer)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="220" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        
        # 處理參數預設值
        params = kwargs
        
        if svg_type == "rect_path":
            return base.format('<rect x="50" y="50" width="200" height="120" fill="#81c784" stroke="black"/><rect x="140" y="50" width="20" height="120" fill="#e0e0e0" stroke="none"/><rect x="50" y="100" width="200" height="20" fill="#e0e0e0" stroke="none"/><text x="145" y="45">x</text><text x="30" y="115">x</text><text x="260" y="115">長20</text><text x="140" y="190">寬10</text>')
        
        elif svg_type == "triangle_incenter_angle":
            a_val = params.get("a", "?")
            return base.format(f'<path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/><text x="150" y="25" font-size="16" text-anchor="middle" font-weight="bold">A ({a_val}°)</text><text x="25" y="200" font-size="16" font-weight="bold">B</text><text x="275" y="200" font-size="16" font-weight="bold">C</text><circle cx="150" cy="132.2" r="57.8" fill="#fff9c4" stroke="#fbc02d" stroke-width="2" opacity="0.6"/><circle cx="150" cy="132.2" r="4" fill="red"/><text x="150" y="125" fill="red" font-size="14" text-anchor="middle" font-weight="bold">I</text><line x1="40" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/><line x1="260" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/><text x="150" y="170" fill="blue" font-size="20" text-anchor="middle" font-weight="bold">?</text>')
            
        elif svg_type == "right_triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#e0e0e0"/><path d="M90,40 L90,160 L210,160 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="100" r="5" fill="red"/><text x="160" y="95" fill="red">O</text>')
            
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#b2dfdb"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="90" fill="green">O</text>')
            
        elif svg_type == "triangle_incenter_concept":
            return base.format('<path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="132.2" r="57.8" fill="none" stroke="orange" stroke-width="2"/><circle cx="150" cy="132.2" r="4" fill="orange"/><text x="150" y="125" fill="orange" font-weight="bold" text-anchor="middle">I</text><line x1="150" y1="132.2" x2="150" y2="190" stroke="orange" stroke-width="2" stroke-dasharray="4"/><text x="155" y="165" font-size="14" fill="gray" font-weight="bold">r</text>')
            
        elif svg_type == "triangle_centroid":
            m = params.get("m", "?")
            return base.format(f'<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red" stroke-dasharray="4"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="160" y="130" fill="blue">G</text><text x="200" y="100" fill="red">中線={m}</text>')
            
        elif svg_type == "roots_line":
            r1 = params.get("r1", 0)
            r2 = params.get("r2", 0)
            return base.format(f'<line x1="20" y1="110" x2="280" y2="110" stroke="black"/><circle cx="100" cy="110" r="5" fill="red"/><circle cx="200" cy="110" r="5" fill="red"/><text x="100" y="140" text-anchor="middle">{r1}</text><text x="200" y="140" text-anchor="middle">{r2}</text>')
            
        elif svg_type == "area_square":
            s = params.get("s", "?")
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">Area={s*s}</text><text x="150" y="170" text-anchor="middle">邊長=?</text>')
        
        elif svg_type == "general_triangle":
             a = params.get("angle_a", 60)
             b = params.get("angle_b", 60)
             return base.format(f'<path d="M80,150 L220,150 L120,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/><text x="110" y="40" font-size="14">A({a}°)</text><text x="60" y="160" font-size="14">B({b}°)</text><text x="230" y="160" font-size="14" fill="red">C(?)</text>')
             
        elif svg_type == "parabola_d_neg":
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
            
        elif svg_type == "geometry_sas":
            return base.format('<path d="M30,120 L90,120 L60,40 Z" fill="none" stroke="black"/><path d="M160,120 L220,120 L190,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
            
        return ""

# ==========================================
# 3. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="♾️")
st.title("♾️ 國中數學雲端教室 (V28.0 連動版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

# 載入資料庫
db = DataLoader.load_questions()

mode = st.sidebar.radio("請選擇出題模式", ["📂 題庫測驗模式", "📝 自訂貼上題庫"])

if mode == "📂 題庫測驗模式":
    if db is None:
        st.error("⚠️ 找不到題庫檔案 (questions.json)！請先執行 gen_db.py 生成題庫。")
    else:
        units = list(db.keys())
        unit = st.sidebar.selectbox("請選擇練習單元", units)
        
        # 顯示該單元題數
        q_count = len(db[unit])
        st.sidebar.caption(f"目前題庫存量：{q_count} 題")
        
        if st.sidebar.button("🚀 生成試卷 (隨機10題)"):
            if q_count < 10:
                st.sidebar.warning("題庫數量不足 10 題，將顯示所有題目。")
                selected_qs = db[unit]
            else:
                selected_qs = random.sample(db[unit], 10)
            
            # 隨機打亂每個題目的選項 (雖然資料庫已亂，但再亂一次更保險)
            for q in selected_qs:
                random.shuffle(q['options'])
                
            st.session_state.quiz = selected_qs
            st.session_state.exam_finished = False
            st.rerun()

elif mode == "📝 自訂貼上題庫":
    st.sidebar.markdown("### 📋 格式說明")
    st.sidebar.info("題目 | 正確答案 | 錯誤1, 錯誤2, 錯誤3")
    default_text = "1+1等於多少? | 2 | 3, 4, 5"
    raw_text = st.sidebar.text_area("貼上題目", default_text)
    
    if st.sidebar.button("✨ 生成自訂試卷"):
        questions = []
        for line in raw_text.strip().split('\n'):
            if "|" in line:
                parts = line.split('|')
                q = parts[0].strip()
                ans = parts[1].strip()
                opts = [x.strip() for x in parts[2].split(',')] + [ans]
                random.shuffle(opts)
                questions.append({"q": q, "options": opts, "ans": ans, "expl": "自訂題目", "svg": "none", "params": {}})
        st.session_state.quiz = questions
        st.session_state.exam_finished = False
        st.rerun()

# 顯示考卷
if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1} {q['q']}")
            
            # 繪圖
            svg_code = q.get('svg', 'none')
            params = q.get('params', {})
            if svg_code != 'none':
                st.markdown(SVGDrawer.draw(svg_code, **params), unsafe_allow_html=True)
                
            u_ans = st.radio("選擇答案", q['options'], key=f"q_{i}", label_visibility="collapsed")
            u_answers.append(u_ans)
            st.divider()
            
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            st.session_state.results = u_answers
            st.session_state.exam_finished = True
            st.rerun()

# 顯示結果
if st.session_state.exam_finished:
    score = 0
    for i, q in enumerate(st.session_state.quiz):
        u_ans = st.session_state.results[i]
        is_correct = (u_ans == q['ans'])
        if is_correct: score += 1
        
        with st.expander(f"第 {i+1} 題: {'✅ 正確' if is_correct else '❌ 錯誤'}"):
            # 錯題再顯示一次圖
            if not is_correct and q.get('svg') != 'none':
                 st.markdown(SVGDrawer.draw(q['svg'], **q.get('params', {})), unsafe_allow_html=True)
                 
            st.write(f"**題目**: {q['q']}")
            st.write(f"**您的答案**: {u_ans}")
            st.write(f"**正確答案**: {q['ans']}")
            st.info(f"💡 解析: {q['expl']}")
    
    final_score = int((score / len(st.session_state.quiz)) * 100)
    st.markdown(f"## 🏆 最終得分: {final_score} 分")
    
    if st.button("🔄 再測驗一次"):
        st.session_state.exam_finished = False
        st.session_state.quiz = []
        st.rerun()
