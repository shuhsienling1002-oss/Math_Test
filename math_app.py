import streamlit as st
import json
import random
import os

# ==========================================
# 1. 資料讀取器
# ==========================================
class DataLoader:
    @staticmethod
    @st.cache_data
    def load_questions():
        file_path = "questions.json"
        if not os.path.exists(file_path): return None
        try:
            with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
        except: return None

# ==========================================
# 2. 視覺繪圖引擎 (完全無刪減版)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="220" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
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
            r1 = params.get("r1", 0); r2 = params.get("r2", 0)
            return base.format(f'<line x1="20" y1="110" x2="280" y2="110" stroke="black"/><circle cx="100" cy="110" r="5" fill="red"/><circle cx="200" cy="110" r="5" fill="red"/><text x="100" y="140" text-anchor="middle">{r1}</text><text x="200" y="140" text-anchor="middle">{r2}</text>')
        
        elif svg_type == "area_square":
            s = params.get("s", "?")
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">Area={s*s}</text><text x="150" y="170" text-anchor="middle">邊長=?</text>')
        
        elif svg_type == "general_triangle":
             a = params.get("angle_a", 60); b = params.get("angle_b", 60)
             return base.format(f'<path d="M80,150 L220,150 L120,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/><text x="110" y="40" font-size="14">A({a}°)</text><text x="60" y="160" font-size="14">B({b}°)</text><text x="230" y="160" font-size="14" fill="red">C(?)</text>')
        
        elif svg_type == "parabola_d_neg":
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
        
        elif svg_type == "geometry_sas":
            return base.format('<path d="M30,120 L90,120 L60,40 Z" fill="none" stroke="black"/><path d="M160,120 L220,120 L190,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        
        elif svg_type == "sticks_triangle":
             s1 = params.get("s1", 5); s2 = params.get("s2", 5)
             return base.format(f'<rect x="50" y="80" width="{s1*10}" height="10" fill="blue"/><rect x="50" y="110" width="{s2*10}" height="10" fill="green"/><text x="50" y="70" fill="blue">長度 {s1}</text><text x="50" y="140" fill="green">長度 {s2}</text><text x="200" y="100" fill="red">第三邊 x ?</text>')
        
        elif svg_type == "polygon_n":
             n = params.get("n", 5)
             return base.format(f'<polygon points="150,40 220,90 190,170 110,170 80,90" fill="#f3e5f5" stroke="purple" stroke-width="2"/><text x="130" y="115" fill="purple">正{n}邊形</text>')
        
        elif svg_type == "right_triangle_incenter":
             a = params.get("a", 3); b = params.get("b", 4); c = params.get("c", 5)
             return base.format(f'<path d="M50,40 L50,180 L200,180 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="90" cy="140" r="40" fill="#e1bee7" stroke="purple" opacity="0.5"/><text x="90" y="145" fill="purple" font-size="12">r?</text>')
        
        elif svg_type == "ladder_wall":
             return base.format('<line x1="50" y1="20" x2="50" y2="180" stroke="black" stroke-width="4"/><line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="4"/><line x1="50" y1="60" x2="130" y2="180" stroke="brown" stroke-width="5"/><text x="90" y="110" fill="brown">梯子</text>')
        
        elif svg_type == "diff_squares":
             k = params.get("k", 3)
             return base.format(f'<rect x="80" y="40" width="140" height="140" fill="#e8f5e9" stroke="black"/><rect x="180" y="140" width="40" height="40" fill="white" stroke="red" stroke-dasharray="4"/><text x="130" y="110" font-size="20">x²</text><text x="190" y="165" font-size="12" fill="red">{k}²</text>')
        
        elif svg_type == "area_square_k":
             return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        
        elif svg_type == "roots_0_k":
             k = params.get("k", 3)
             return base.format(f'<line x1="20" y1="110" x2="280" y2="110" stroke="black"/><circle cx="50" cy="110" r="5" fill="red"/><text x="50" y="140">0</text><circle cx="200" cy="110" r="5" fill="red"/><text x="200" y="140">{k}</text>')

        return ""

# ==========================================
# 3. APP 介面 (V29.0 題型互斥版)
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="♾️")
st.title("♾️ 國中數學雲端教室 (V29.0 題型互斥版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

db = DataLoader.load_questions()
mode = st.sidebar.radio("模式", ["📂 題庫測驗", "📝 自訂題庫"])

if mode == "📂 題庫測驗":
    if db is None:
        st.error("⚠️ 找不到題庫")
    else:
        units = list(db.keys())
        unit = st.sidebar.selectbox("單元", units)
        st.sidebar.caption(f"庫存：{len(db[unit])} 題")
        
        # === 核心修改區：智慧選題邏輯 (強制不重複) ===
        if st.sidebar.button("🚀 生成試卷 (不重複題型)"):
            pool = db[unit][:]       # 複製題庫
            random.shuffle(pool)     # 先把題目打散
            
            selected_qs = []
            seen_types = set()       # 用來記錄已經選過的題型 ID
            
            for q in pool:
                # 取得這題的題型 ID (如果是舊題庫沒有 ID，就給它一個隨機數避免報錯)
                t_id = q.get('type_id', random.random())
                
                # 如果這個題型還沒出現過，就選它！
                if t_id not in seen_types:
                    random.shuffle(q['options'])
                    selected_qs.append(q)
                    seen_types.add(t_id) # 記錄下來，下次不選這個 ID 了
                
                # 湊滿 3 題就收工
                if len(selected_qs) >= 3:
                    break
            
            # 如果題型真的太少湊不滿 3 題，就隨便補
            if len(selected_qs) < 3:
                remaining_needed = 3 - len(selected_qs)
                extras = [x for x in pool if x not in selected_qs][:remaining_needed]
                selected_qs.extend(extras)

            st.session_state.quiz = selected_qs
            st.session_state.exam_finished = False
            st.rerun()

elif mode == "📝 自訂題庫":
    st.sidebar.info("自訂功能")

# 顯示考卷 (邏輯不變)
if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1} {q['q']}")
            if q.get('svg') and q.get('svg') != 'none':
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('params', {})), unsafe_allow_html=True)
            u_ans = st.radio("選擇", q['options'], key=f"q_{i}", label_visibility="collapsed")
            u_answers.append(u_ans)
            st.divider()
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            st.session_state.results = u_answers
            st.session_state.exam_finished = True
            st.rerun()

if st.session_state.exam_finished:
    score = 0
    for i, q in enumerate(st.session_state.quiz):
        u_ans = st.session_state.results[i]
        is_correct = (u_ans == q['ans'])
        if is_correct: score += 1
        with st.expander(f"Q{i+1}: {'✅' if is_correct else '❌'}"):
            st.write(f"題目: {q['q']}\n正解: {q['ans']}")
            if q.get('svg') and q.get('svg') != 'none':
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('params', {})), unsafe_allow_html=True)
            st.info(f"解析: {q['expl']}")
    st.markdown(f"## 得分: {int(score/len(st.session_state.quiz)*100)}")
    if st.button("🔄 再來"):
        st.session_state.exam_finished = False; st.rerun()