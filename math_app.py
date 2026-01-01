import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (V5.0 微觀變異版)
# ==========================================
# ❌ 已移除 @st.cache_data，確保每次刷新頁面題目絕對不同
def create_cloud_database():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心": [],
        "3-3 三角形的內心": [],
        "3-4 三角形的重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # ---------------------------------------------------------
    # 單元 3-1: 證明 (引入敘述變異)
    # ---------------------------------------------------------
    for _ in range(50):
        # 變異 1: 全等性質 (正向/反向/陷阱)
        subtype = random.randint(1, 3)
        if subtype == 1:
            prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
            q_text = random.choice([
                f"若兩三角形滿足「{prop}」，則其關係為何？",
                f"判別性質「{prop}」可以用來證明什麼？",
                f"已知 △ABC 與 △DEF 符合 {prop} 條件，則？"
            ])
            database["3-1 證明與推理"].append({
                "q": q_text,
                "options": ["必全等", "不一定全等", "僅面積相等", "相似但不全等"],
                "ans": "必全等", "expl": "五大全等性質之一。", "svg": "geometry_sas"
            })
        elif subtype == 2: # 陷阱題
            bad_prop = random.choice(["SSA", "AAA"])
            q_text = random.choice([
                f"下列哪一個性質「不能」保證三角形全等？",
                f"若已知兩三角形符合 {bad_prop}，則下列敘述何者正確？"
            ])
            database["3-1 證明與推理"].append({
                "q": q_text,
                "options": [bad_prop, "SAS", "ASA", "RHS"] if "不能" in q_text else ["不一定全等", "必全等", "必不全等", "面積必相等"],
                "ans": bad_prop if "不能" in q_text else "不一定全等",
                "expl": "SSA 與 AAA 無法證明全等。", "svg": "none"
            })
        else: # 應用
            database["3-1 證明與推理"].append({
                "q": "想要證明角平分線上任一點到兩邊等距離，會用到哪個全等性質？",
                "options": ["AAS", "SSS", "SAS", "RHS"],
                "ans": "AAS", "expl": "利用兩個角(直角、平分角)及共用邊(斜邊)證明 AAS 全等。", "svg": "none"
            })

    for _ in range(50):
        # 變異 2: 邊角關係 (數字/代數/邏輯)
        subtype = random.randint(1, 3)
        if subtype == 1: # 純數字
            a = random.randint(50, 80)
            b = random.randint(20, 49)
            c = 180 - a - b
            # 隨機挖空
            target = random.choice(["最大邊", "最小邊"])
            ans_map = {"最大邊": "BC" if a==max(a,b,c) else ("AC" if b==max(a,b,c) else "AB"),
                       "最小邊": "BC" if a==min(a,b,c) else ("AC" if b==min(a,b,c) else "AB")}
            database["3-1 證明與推理"].append({
                "q": f"△ABC 中，∠A={a}°, ∠B={b}°, ∠C={c}°。請問{target}是？",
                "options": ["AB", "BC", "AC", "無法判斷"],
                "ans": ans_map[target], "expl": "大角對大邊，小角對小邊。", "svg": "none"
            })
        elif subtype == 2: # 邏輯推論
            database["3-1 證明與推理"].append({
                "q": "在一個鈍角三角形中，哪一邊一定最長？",
                "options": ["鈍角的對邊", "鈍角的鄰邊", "最短邊", "不一定"],
                "ans": "鈍角的對邊", "expl": "三角形中最多只有一個鈍角，故其角度最大，對邊最長。", "svg": "none"
            })
        else: # 兩邊之和
            s = random.randint(5, 15)
            database["3-1 證明與推理"].append({
                "q": f"三角形兩邊長為 {s} 和 {s} (等腰)，第三邊長可能是？",
                "options": [str(s), str(2*s), str(2*s+1), "0"],
                "ans": str(s), "expl": "第三邊 x 需滿足 0 < x < 2s。選項中只有 s 符合。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 3-2: 外心 (引入座標變異)
    # ---------------------------------------------------------
    for _ in range(50):
        subtype = random.randint(1, 3)
        if subtype == 1: # 直角三角形半徑 (正問/反問)
            c = random.choice([10, 20, 26, 30, 34])
            if random.random() > 0.5:
                database["3-2 三角形的外心"].append({
                    "q": f"直角三角形斜邊長為 {c}，外接圓半徑 R = ？",
                    "options": [str(c/2), str(c), str(c*2), str(c/4)],
                    "ans": str(c/2), "expl": "直角三角形外心在斜邊中點，R = 斜邊/2。", "svg": "none"
                })
            else:
                database["3-2 三角形的外心"].append({
                    "q": f"直角三角形外接圓半徑為 {c/2}，則斜邊長度為？",
                    "options": [str(c), str(c/2), str(c/4), str(c*2)],
                    "ans": str(c), "expl": "斜邊 = 2R。", "svg": "none"
                })
        elif subtype == 2: # 座標題 (原點/非原點)
            k = random.randint(2, 6) * 2
            database["3-2 三角形的外心"].append({
                "q": f"座標平面上三點 O(0,0), A({k},0), B(0,{k})，求 △OAB 外心座標？",
                "options": [f"({k//2},{k//2})", f"({k},{k})", "(0,0)", f"({k//3},{k//3})"],
                "ans": f"({k//2},{k//2})", "expl": "直角三角形外心為斜邊中點 ((0+k)/2, (0+k)/2)。", "svg": "none"
            })
        else: # 性質判斷
            database["3-2 三角形的外心"].append({
                "q": "銳角三角形的外心位於？",
                "options": ["三角形內部", "三角形外部", "邊上", "頂點"],
                "ans": "三角形內部", "expl": "銳角-內；直角-中；鈍角-外。", "svg": "triangle_circumcenter"
            })

    # ---------------------------------------------------------
    # 單元 3-3: 內心 (引入面積逆算)
    # ---------------------------------------------------------
    for _ in range(50):
        subtype = random.randint(1, 3)
        if subtype == 1: # 角度計算
            deg = random.choice([40, 50, 60, 80])
            q_style = random.choice([
                f"I 為內心，∠A={deg}°，求 ∠BIC？",
                f"若 ∠A={deg}°，I 為內心，則 ∠BIC 度數為何？"
            ])
            database["3-3 三角形的內心"].append({
                "q": q_style,
                "options": [str(90+deg//2), str(180-deg), str(90+deg), str(deg)],
                "ans": str(90+deg//2), "expl": "公式：90 + A/2。", "svg": "triangle_incenter", "svg_params": {"a": deg}
            })
        elif subtype == 2: # 面積公式 (正問/反問)
            s = random.randint(10, 20) # 周長
            r = random.randint(2, 4)
            area = s * r // 2
            if random.random() > 0.5:
                database["3-3 三角形的內心"].append({
                    "q": f"三角形周長 {s}，內切圓半徑 {r}，面積 = ？",
                    "options": [str(area), str(s*r), str(area*2), str(s+r)],
                    "ans": str(area), "expl": "A = rs/2。", "svg": "none"
                })
            else:
                database["3-3 三角形的內心"].append({
                    "q": f"三角形面積 {area}，周長 {s}，求內切圓半徑？",
                    "options": [str(r), str(r*2), str(area/s), str(s/area)],
                    "ans": str(r), "expl": "r = 2A / s。", "svg": "none"
                })
        else: # 距離性質
            database["3-3 三角形的內心"].append({
                "q": "內心到下列何者的距離相等？",
                "options": ["三邊", "三頂點", "三中線", "重心"],
                "ans": "三邊", "expl": "內心為內切圓圓心，到三邊等距。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 3-4: 重心 (引入物理與面積分割)
    # ---------------------------------------------------------
    for _ in range(50):
        subtype = random.randint(1, 3)
        if subtype == 1: # 長度比 (多種問法)
            m = random.randint(3, 9) * 3
            q_var = random.choice([
                (f"中線 AD={m}，求 AG？", str(m*2//3), "2/3"),
                (f"中線 AD={m}，求 GD？", str(m//3), "1/3"),
                (f"重心到頂點距離 AG={m*2//3}，求中線 AD？", str(m), "3/2")
            ])
            database["3-4 三角形的重心"].append({
                "q": q_var[0],
                "options": [str(m), str(m//2), str(m*2//3), str(m//3)],
                "ans": q_var[1], "expl": f"重心性質：佔中線的 {q_var[2]}。", "svg": "triangle_centroid", "svg_params": {"m": m}
            })
        elif subtype == 2: # 面積分割
            area = random.randint(6, 12) * 6
            database["3-4 三角形的重心"].append({
                "q": f"△ABC 面積 {area}，G 為重心。則 △GAB + △GBC 面積為？",
                "options": [str(area*2//3), str(area//3), str(area//2), str(area)],
                "ans": str(area*2//3), "expl": "重心分出三個等積三角形，兩塊相加為 2/3。", "svg": "none"
            })
        else: # 物理
            database["3-4 三角形的重心"].append({
                "q": "將一均勻三角形懸掛在哪一點，可以保持水平平衡？",
                "options": ["重心", "內心", "外心", "頂點"],
                "ans": "重心", "expl": "重心是重量中心。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 4-1: 因式分解 (引入符號變異)
    # ---------------------------------------------------------
    for _ in range(50):
        subtype = random.randint(1, 4)
        if subtype == 1: # 提公因式 (變數變換)
            var = random.choice(["x", "a", "y"])
            k = random.randint(2, 8)
            database["4-1 因式分解法"].append({
                "q": f"因式分解 {var}² - {k}{var}？",
                "options": [f"{var}({var}-{k})", f"{var}({var}+{k})", f"({var}-{k})²", f"{var}({var}-1)"],
                "ans": f"{var}({var}-{k})", "expl": f"提公因式 {var}。", "svg": "none"
            })
        elif subtype == 2: # 平方差
            k = random.randint(3, 9)
            database["4-1 因式分解法"].append({
                "q": f"下列何者是 {k*k} - x² 的因式？",
                "options": [f"{k}-x", f"{k}-2x", f"x-{k*k}", f"x"],
                "ans": f"{k}-x", "expl": f"原式=({k}+x)({k}-x)。", "svg": "none"
            })
        elif subtype == 3: # 十字交乘
            a, b = random.randint(1, 5), random.randint(1, 5)
            database["4-1 因式分解法"].append({
                "q": f"x² + {a+b}x + {a*b} 可以分解為？",
                "options": [f"(x+{a})(x+{b})", f"(x-{a})(x-{b})", f"(x+{a})(x-{b})", "無法分解"],
                "ans": f"(x+{a})(x+{b})", "expl": "十字交乘法。", "svg": "none"
            })
        else: # 根的意義
            k = random.randint(1, 3)
            database["4-1 因式分解法"].append({
                "q": f"若 x=1 是 x² + ax + {k} = 0 的解，求 a？",
                "options": [str(-1-k), str(1+k), str(k), str(-k)],
                "ans": str(-1-k), "expl": f"代入 x=1: 1 + a + {k} = 0 => a = {-1-k}。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 4-2: 配方法 (引入填空與判別式)
    # ---------------------------------------------------------
    for _ in range(50):
        subtype = random.randint(1, 3)
        if subtype == 1: # 配方填空
            k = random.choice([4, 6, 8, 10])
            q_text = random.choice([
                f"x² + {k}x + ? 是一個完全平方式",
                f"為了將 x² + {k}x 配方，應加上多少？"
            ])
            database["4-2 配方法與公式解"].append({
                "q": q_text,
                "options": [str((k//2)**2), str(k), str(k*2), str(k**2)],
                "ans": str((k//2)**2), "expl": "加上係數一半的平方。", "svg": "area_square_k"
            })
        elif subtype == 2: # 判別式判斷
            b = random.randint(3, 7)
            c = random.randint(1, 3)
            # D = b^2 - 4c (恆正)
            database["4-2 配方法與公式解"].append({
                "q": f"方程式 x² + {b}x + {c} = 0 的根的性質？",
                "options": ["兩相異實根", "重根", "無實根", "無法判斷"],
                "ans": "兩相異實根", "expl": f"D = {b*b} - 4({c}) = {b*b-4*c} > 0。", "svg": "none"
            })
        else: # 公式解
            database["4-2 配方法與公式解"].append({
                "q": "公式解中的根號內部分 (b²-4ac) 稱為？",
                "options": ["判別式", "完全平方式", "係數", "常數項"],
                "ans": "判別式", "expl": "用來判別根的性質。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 4-3: 應用問題 (引入情境包裝)
    # ---------------------------------------------------------
    for _ in range(50):
        subtype = random.randint(1, 4)
        if subtype == 1: # 幾何情境
            s = random.randint(5, 12)
            q_text = random.choice([
                f"一個正方形花園面積為 {s*s}，其邊長為？",
                f"某正方形磁磚邊長為 x，面積為 {s*s}，求 x？"
            ])
            database["4-3 應用問題"].append({
                "q": q_text,
                "options": [str(s), str(s*2), str(s*s), str(s+2)],
                "ans": str(s), "expl": "開根號取正值。", "svg": "area_square"
            })
        elif subtype == 2: # 數字情境
            n = random.randint(1, 9)
            database["4-3 應用問題"].append({
                "q": f"一個數比其平方小 {n*(n-1)}，此數可能為？",
                "options": [str(n), str(n+1), str(n-1), "0"],
                "ans": str(n), "expl": f"x² - x = {n*(n-1)}，解得 x={n}。", "svg": "none"
            })
        elif subtype == 3: # 物理情境
            t = random.randint(2, 5)
            database["4-3 應用問題"].append({
                "q": f"自由落體 h=5t²。若 h={5*t*t}，則 t=？",
                "options": [str(t), str(t*2), "10", "1"],
                "ans": str(t), "expl": "代入公式求解。", "svg": "none"
            })
        else: # 畢氏定理應用
            a, b, c = random.choice([(3,4,5), (5,12,13), (8,15,17)])
            database["4-3 應用問題"].append({
                "q": f"梯子長 {c} 公尺，梯腳離牆 {a} 公尺，梯頂高度？",
                "options": [str(b), str(c), str(a+b), str(c-a)],
                "ans": str(b), "expl": f"√({c}² - {a}²) = {b}。", "svg": "none"
            })

    return database

# ==========================================
# 2. 視覺繪圖引擎 (保留)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{}</svg>'
        mx = lambda v: 150 + v*12
        if svg_type == "geometry_sas":
            return base.format('<path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black"/><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        elif svg_type == "triangle_centroid":
            return base.format('<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="160" y="130" fill="blue">G</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="green"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="90" fill="green">O</text>')
        elif svg_type == "triangle_incenter":
            return base.format('<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange">I</text>')
        elif svg_type == "roots_line_hidden":
            r1, r2 = kwargs.get('r1', 0), kwargs.get('r2', 0)
            l1, l2 = kwargs.get('r1_label', 'x₁'), kwargs.get('r2_label', 'x₂')
            return base.format(f'<line x1="10" y1="100" x2="290" y2="100" stroke="black"/><text x="150" y="90" text-anchor="middle">0</text><circle cx="{mx(r1)}" cy="100" r="5" fill="red"/><text x="{mx(r1)}" y="130" fill="red" text-anchor="middle">{l1}</text><circle cx="{mx(r2)}" cy="100" r="5" fill="red"/><text x="{mx(r2)}" y="130" fill="red" text-anchor="middle">{l2}</text>')
        elif svg_type == "roots_0_k":
            k = kwargs.get('k', 0)
            kl = kwargs.get('k_label', 'k')
            return base.format(f'<line x1="10" y1="100" x2="290" y2="100" stroke="black"/><circle cx="{mx(0)}" cy="100" r="5" fill="red"/><circle cx="{mx(k)}" cy="100" r="5" fill="red"/><text x="{mx(k)}" y="130" fill="red">{kl}</text><text x="{mx(0)}" y="130" fill="black">0</text>')
        elif svg_type == "area_square":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#e3f2fd" stroke="black"/><text x="150" y="105" text-anchor="middle">面積</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        return ""

# ==========================================
# 3. APP 介面 (保留去重邏輯)
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (V5.0 微觀變異版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

data = create_cloud_database()
st.sidebar.success(f"✅ 題庫生成完畢！共 {sum(len(v) for v in data.values())} 題。")

unit_options = list(data.keys()) + ["全範圍總複習"]
unit = st.sidebar.selectbox("請選擇練習單元", unit_options)

if st.sidebar.button("🚀 生成試卷 (10題)"):
    all_q = []
    for k in data: all_q.extend(data[k])
    target = all_q if unit == "全範圍總複習" else data[unit]
    
    random.seed(time.time())
    random.shuffle(target)
    
    unique_quiz = []
    seen_questions = set()
    
    for q in target:
        if q['q'] not in seen_questions:
            unique_quiz.append(q)
            seen_questions.add(q['q'])
        
        if len(unique_quiz) >= 10:
            break
            
    st.session_state.quiz = unique_quiz
    st.session_state.exam_finished = False
    st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1}. {q['q']}")
            if q['svg'] != "none":
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('svg_params', {}) if 'svg_params' in q else {}), unsafe_allow_html=True)
            u_ans = st.radio("選擇答案", q['options'], key=f"q_{i}", label_visibility="collapsed")
            u_answers.append(u_ans)
            st.divider()
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            st.session_state.results = u_answers
            st.session_state.exam_finished = True
            st.rerun()

if st.session_state.exam_finished:
    score = 0
    for i, q in enumerate(st.session_state.quiz):
        is_correct = st.session_state.results[i] == q['ans']
        if is_correct: score += 1
        with st.expander(f"第 {i+1} 題: {'✅ 正確' if is_correct else '❌ 錯誤'}"):
            st.write(f"題目: {q['q']}")
            st.write(f"您的答案: {st.session_state.results[i]}")
            st.write(f"正確答案: {q['ans']}")
            st.info(f"解析: {q['expl']}")
    st.success(f"## 您的最終得分: {score * 10} 分")
    if st.button("🔄 重新挑戰", use_container_width=True):
        st.session_state.quiz = []
        st.session_state.exam_finished = False
        st.rerun()
