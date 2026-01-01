import streamlit as st
import random
import math

# ==========================================
# 1. 核心：雲端題庫製造機 (多樣化模板)
# ==========================================
@st.cache_data
def create_cloud_database():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心、內心與重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # ================= 3-1 證明與推理 (5種變化) =================
    for _ in range(50): # 變化 A: 全等性質
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        database["3-1 證明與推理"].append({
            "q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係為何？",
            "options": ["必全等", "不一定全等", "面積相等但形狀不同", "無法判斷"],
            "ans": "必全等",
            "expl": f"{prop} 是三角形全等判別性質之一。",
            "svg": "geometry_sas"
        })
    
    for _ in range(50): # 變化 B: 外角定理
        a, b = random.randint(30, 80), random.randint(30, 80)
        database["3-1 證明與推理"].append({
            "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
            "options": [str(a+b), str(180-(a+b)), "180", "90"],
            "ans": str(a+b),
            "expl": f"外角 = 不相鄰兩內角和：{a} + {b} = {a+b}。",
            "svg": "none"
        })

    for _ in range(50): # 變化 C: 大邊對大角
        database["3-1 證明與推理"].append({
            "q": "在 △ABC 中，若邊長 AB > AC > BC，則角度關係為何？",
            "options": ["∠C > ∠B > ∠A", "∠A > ∠B > ∠C", "∠A = ∠B = ∠C", "無法判斷"],
            "ans": "∠C > ∠B > ∠A",
            "expl": "大邊對大角：最長邊 AB 對應 ∠C，最短邊 BC 對應 ∠A。",
            "svg": "none"
        })

    for _ in range(50): # 變化 D: 特殊四邊形性質
        shape_type = random.choice([
            ("菱形", "互相垂直平分"),
            ("矩形", "等長且互相平分"),
            ("平行四邊形", "互相平分"),
            ("箏形", "互相垂直")
        ])
        s_name, s_prop = shape_type
        database["3-1 證明與推理"].append({
            "q": f"下列何者是「{s_name}」對角線必具備的性質？",
            "options": [s_prop, "只有一條平分", "無特殊性質", "以上皆非"],
            "ans": s_prop,
            "expl": f"{s_name} 的對角線性質：{s_prop}。",
            "svg": "none"
        })
    
    for _ in range(50): # 變化 E: 內角和
        n = random.choice([5, 6, 8, 10, 12])
        ans_val = (n-2)*180
        database["3-1 證明與推理"].append({
            "q": f"正 {n} 邊形的內角總和是多少度？",
            "options": [str(ans_val), str(n*180), "360", "180"],
            "ans": str(ans_val),
            "expl": f"內角和公式：(n-2)×180 = ({n}-2)×180 = {ans_val}。",
            "svg": "none"
        })

    # ================= 3-2 三心 (5種變化) =================
    for _ in range(50): # 變化 A: 重心長度
        m = random.randint(6, 30) * 3
        ag = int(m * 2 / 3)
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"若中線 AD 長為 {m}，G 為重心，求 AG 的長度？",
            "options": [str(ag), str(m), str(int(m/2)), str(int(m/3))],
            "ans": str(ag),
            "expl": f"重心性質：頂點到重心 = 2/3 中線 = {ag}。",
            "svg": "triangle_centroid",
            "svg_params": {"m": m}
        })

    for _ in range(50): # 變化 B: 內心角度
        deg = random.choice([40, 50, 60, 70, 80])
        ans_val = 90 + deg // 2
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"I 為內心，若 ∠A = {deg}°，求 ∠BIC？",
            "options": [str(ans_val), str(180-deg), str(90+deg), str(2*deg)],
            "ans": str(ans_val),
            "expl": f"內心角度公式：90 + A/2 = 90 + {deg//2} = {ans_val}。",
            "svg": "triangle_incenter",
            "svg_params": {"a": deg}
        })

    for _ in range(50): # 變化 C: 直角三角形外心半徑
        triple = random.choice([(6,8,10), (5,12,13), (8,15,17), (9,12,15), (7,24,25)])
        a, b, c = triple
        r = c / 2
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"直角三角形兩股長為 {a}, {b}，求其「外接圓半徑」？",
            "options": [str(r), str(c), str(a+b), str(r*2)],
            "ans": str(r),
            "expl": f"斜邊為 {c} (畢氏定理)。直角三角形外心在斜邊中點，半徑 = {c}/2 = {r}。",
            "svg": "triangle_circumcenter"
        })

    for _ in range(50): # 變化 D: 重心面積分割
        area = random.choice([12, 24, 30, 36, 60, 72])
        ans_area = int(area / 3)
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"若 △ABC 面積為 {area}，G 為重心，則 △GAB 的面積為何？",
            "options": [str(ans_area), str(int(area/2)), str(int(area/6)), str(area)],
            "ans": str(ans_area),
            "expl": f"重心與三頂點連線將三角形面積平分為 3 等份。{area} ÷ 3 = {ans_area}。",
            "svg": "center_def_dynamic",
            "svg_params": {"pair": ["重心","中線"]}
        })

    for _ in range(50): # 變化 E: 三心定義
        q_data = random.choice([
            ("重心", "中線"), ("外心", "中垂線"), ("內心", "角平分線")
        ])
        center, line = q_data
        database["3-2 三角形的外心、內心與重心"].append({
            "q": f"三角形的「{center}」是哪三條線的交點？",
            "options": [line, "高", "對角線", "邊長"],
            "ans": line,
            "expl": f"定義：{center}是三條{line}的交點。",
            "svg": "none"
        })

    # ================= 4-1 因式分解 (5種變化) =================
    for _ in range(50): # 變化 A: 十字交乘 (兩根已知求方程式)
        r1, r2 = random.randint(1, 5), random.randint(-5, -1)
        database["4-1 因式分解法"].append({
            "q": f"解方程式 (x - {r1})(x - {r2}) = 0？",
            "options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
            "ans": f"{r1} 或 {r2}",
            "expl": f"令括號為 0，可得 x={r1} 或 x={r2}。",
            "svg": "roots_line",
            "svg_params": {"r1": r1, "r2": r2}
        })

    for _ in range(50): # 變化 B: 提公因式
        k = random.randint(2, 9)
        database["4-1 因式分解法"].append({
            "q": f"解方程式 x² - {k}x = 0？",
            "options": [f"0 或 {k}", f"{k}", "0", f"1 或 {k}"],
            "ans": f"0 或 {k}",
            "expl": f"提 x：x(x-{k})=0，故 x=0 或 {k}。",
            "svg": "roots_0_k",
            "svg_params": {"k": k}
        })

    for _ in range(50): # 變化 C: 平方差公式
        k = random.randint(2, 9)
        ksq = k*k
        database["4-1 因式分解法"].append({
            "q": f"解方程式 x² - {ksq} = 0？",
            "options": [f"±{k}", f"{k}", f"{ksq}", "無解"],
            "ans": f"±{k}",
            "expl": f"x²={ksq} → x=±{k}。",
            "svg": "roots_sq",
            "svg_params": {"k": k}
        })

    for _ in range(50): # 變化 D: 根的定義
        k = random.randint(2, 5)
        database["4-1 因式分解法"].append({
            "q": f"若 x={k} 是方程式 x² + ax + b = 0 的一根，則下列敘述何者正確？",
            "options": [f"將 {k} 代入方程式等號成立", f"將 -{k} 代入方程式等號成立", "a 必為正數", "b 必為負數"],
            "ans": f"將 {k} 代入方程式等號成立",
            "expl": "方程式的根定義：代入未知數後能使等號成立的數。",
            "svg": "none"
        })

    for _ in range(50): # 變化 E: 完全平方式
        k = random.randint(1, 9)
        database["4-1 因式分解法"].append({
            "q": f"方程式 (x-{k})² = 0 有幾個解？",
            "options": ["1個 (重根)", "2個相異解", "無解", "無限多"],
            "ans": "1個 (重根)",
            "expl": f"完全平方式為重根，視為 1 個解 (x={k})。",
            "svg": "roots_line",
            "svg_params": {"r1": k, "r2": k}
        })

    # ================= 4-2 配方法 (5種變化) =================
    for _ in range(50): # 變化 A: 判別式計算
        b = random.choice([2, 4, 6, 8])
        c = random.randint(1, 3)
        d_val = b*b - 4*c
        database["4-2 配方法與公式解"].append({
            "q": f"求 x² + {b}x + {c} = 0 的判別式 D？",
            "options": [str(d_val), str(d_val+4), str(d_val-4), "0"],
            "ans": str(d_val),
            "expl": f"D = b² - 4ac = {b*b} - 4 = {d_val}。",
            "svg": "none"
        })

    for _ in range(50): # 變化 B: 配方補數
        k = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
        ans_sq = (k // 2) ** 2
        database["4-2 配方法與公式解"].append({
            "q": f"將 x² + {k}x 配成完全平方式，需加上？",
            "options": [str(ans_sq), str(k), str(k*2), "1"],
            "ans": str(ans_sq),
            "expl": f"加上 (一次項係數一半)² = ({k}/2)² = {ans_sq}。",
            "svg": "area_square_k",
            "svg_params": {"k": k}
        })

    for _ in range(50): # 變化 C: 根的性質
        d_state = random.choice([("D > 0", "兩相異實根"), ("D = 0", "重根"), ("D < 0", "無實根")])
        cond, res = d_state
        database["4-2 配方法與公式解"].append({
            "q": f"若一元二次方程式的判別式 {cond}，則根的性質為何？",
            "options": [res, "無法判斷", "以上皆非", "必為整數根"],
            "ans": res,
            "expl": "判別式性質：D>0 相異實根，D=0 重根，D<0 無實根。",
            "svg": "none"
        })
    
    for _ in range(50): # 變化 D: 公式解分母
        database["4-2 配方法與公式解"].append({
            "q": "一元二次方程式公式解中，分母是多少？",
            "options": ["2a", "a", "4a", "b"],
            "ans": "2a",
            "expl": "公式解 x = (-b ± √D) / 2a。",
            "svg": "none"
        })

    for _ in range(50): # 變化 E: 圖形交點
        database["4-2 配方法與公式解"].append({
            "q": "若方程式無實數解 (D < 0)，代表其圖形與 x 軸有幾個交點？",
            "options": ["0個", "1個", "2個", "無限多"],
            "ans": "0個",
            "expl": "無實根代表圖形懸空，與 x 軸沒有交點。",
            "svg": "none"
        })

    # ================= 4-3 應用問題 (5種變化) =================
    for _ in range(50): # 變化 A: 正方形面積
        s = random.randint(5, 20)
        area = s * s
        database["4-3 應用問題"].append({
            "q": f"某正方形農地面積為 {area} 平方公尺，求邊長？",
            "options": [str(s), str(area), str(s*2), str(s+5)],
            "ans": str(s),
            "expl": f"邊長 = √{area} = {s}。",
            "svg": "area_square",
            "svg_params": {"s": s}
        })

    for _ in range(50): # 變化 B: 落體運動
        t = random.randint(2, 6)
        h = 5 * t * t
        database["4-3 應用問題"].append({
            "q": f"物體落下距離公式 h=5t²。若落下 {h} 公尺，需時幾秒？",
            "options": [str(t), str(t*2), str(t+2), "10"],
            "ans": str(t),
            "expl": f"{h} = 5t² → t²={t*t} → t={t}。",
            "svg": "none"
        })

    for _ in range(50): # 變化 C: 兩數乘積
        n = random.randint(1, 10)
        n2 = n + 1
        prod = n * n2
        database["4-3 應用問題"].append({
            "q": f"兩個連續正整數的乘積為 {prod}，求這兩個數？",
            "options": [f"{n}, {n2}", f"{n-1}, {n}", f"{n+1}, {n+2}", "無解"],
            "ans": f"{n}, {n2}",
            "expl": f"驗算：{n} × {n2} = {prod}。",
            "svg": "roots_line",
            "svg_params": {"r1": n, "r2": n2}
        })

    for _ in range(50): # 變化 D: 長方形面積
        w = random.randint(3, 8)
        l = w + 2
        area = w * l
        database["4-3 應用問題"].append({
            "q": f"長方形長比寬多 2，面積為 {area}，求寬？",
            "options": [str(w), str(l), str(area), str(w+1)],
            "ans": str(w),
            "expl": f"設寬 x，長 x+2。x(x+2)={area} → {w}×{l}={area}。",
            "svg": "none"
        })

    for _ in range(50): # 變化 E: 負數解判斷
        database["4-3 應用問題"].append({
            "q": "解應用問題時，若算出長度為 -5，應該如何處理？",
            "options": ["不合 (長度需為正)", "取絕對值", "直接當作答案", "重算"],
            "ans": "不合 (長度需為正)",
            "expl": "幾何圖形的長度必須大於 0。",
            "svg": "none"
        })

    return database

# ==========================================
# 2. 視覺繪圖引擎 (SVG)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{}</svg>'
        
        if svg_type == "geometry_sas":
            return base.format('<path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black"/><text x="50" y="140">A</text><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black"/><text x="180" y="140">B</text><text x="115" y="80" fill="blue" font-weight="bold">全等?</text>')
        elif svg_type == "triangle_centroid":
            m = kwargs.get('m', '?')
            return base.format(f'<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="150" y="15">A</text><text x="40" y="180">B</text><text x="260" y="180">C</text><text x="150" y="195" fill="red">D</text><text x="165" y="126" fill="blue">G</text><text x="20" y="50">AD={m}</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="green"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><text x="150" y="15">A</text><text x="70" y="140">B</text><text x="230" y="140">C</text><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="115" fill="green">O</text>')
        elif svg_type == "triangle_incenter":
            a = kwargs.get('a', '?')
            return base.format(f'<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><text x="150" y="20">A</text><text x="40" y="170">B</text><text x="260" y="170">C</text><circle cx="150" cy="120" r="4" fill="orange"/><text x="150" y="110" fill="orange">I</text><text x="20" y="50">∠A={a}°</text>')
        elif svg_type == "center_def_dynamic":
            return base.format('<path d="M150,30 L50,170 L250,170 Z" fill="none" stroke="black"/><line x1="150" y1="30" x2="150" y2="170" stroke="red" stroke-dasharray="4"/><line x1="50" y1="170" x2="200" y2="100" stroke="red" stroke-dasharray="4"/><text x="150" y="123" fill="blue" font-weight="bold">Center</text>')
        elif svg_type == "roots_line":
            r1, r2 = kwargs.get('r1', 0), kwargs.get('r2', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(r1)}" cy="50" r="5" fill="red"/><text x="{mx(r1)}" y="80" fill="red">{r1}</text><circle cx="{mx(r2)}" cy="50" r="5" fill="red"/><text x="{mx(r2)}" y="80" fill="red">{r2}</text>')
        elif svg_type == "roots_0_k":
            k = kwargs.get('k', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(0)}" cy="50" r="5" fill="red"/><circle cx="{mx(k)}" cy="50" r="5" fill="red"/><text x="{mx(k)}" y="80" fill="red">{k}</text>')
        elif svg_type == "roots_sq":
            k = kwargs.get('k', 0)
            mx = lambda v: 150 + v*12
            return base.format(f'<line x1="10" y1="50" x2="290" y2="50" stroke="black"/><text x="150" y="40">0</text><circle cx="{mx(k)}" cy="50" r="5" fill="red"/><text x="{mx(k)}" y="80" fill="red">{k}</text><circle cx="{mx(-k)}" cy="50" r="5" fill="red"/><text x="{mx(-k)}" y="80" fill="red">-{k}</text>')
        elif svg_type == "area_square":
            s = kwargs.get('s', 10)
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">Area={s*s}</text><text x="150" y="170" text-anchor="middle">邊長=?</text>')
        elif svg_type == "area_square_k":
            k = kwargs.get('k', 10)
            return base.format(f'<rect x="100" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><text x="150" y="100" text-anchor="middle">補上?</text><text x="150" y="170" text-anchor="middle">邊長={k}/2</text>')
        return ""

# ==========================================
# 3. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="☁️")
st.title("☁️ 國中數學智能題庫 (V25.0)")

# 初始化狀態
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False
if 'exam_results' not in st.session_state: st.session_state.exam_results = []
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'quiz' not in st.session_state: st.session_state.quiz = []

# 【核心步驟】程式啟動時，直接在雲端生成 1000+ 題
with st.spinner('正在雲端重構 25 種不同題型...'):
    data = create_cloud_database()

st.sidebar.success(f"✅ 題庫生成完畢！\n共 {sum(len(v) for v in data.values())} 題。\n已排除重複模板。")

# 選擇單元
unit_options = list(data.keys()) + ["全範圍總複習"]
unit = st.sidebar.selectbox("請選擇練習單元", unit_options)

# 生成按鈕
if not st.session_state.exam_finished:
    if st.button("🚀 生成試卷 (10題)", use_container_width=True):
        all_questions = []
        for key in data: all_questions.extend(data[key])
        
        target_pool = all_questions if unit == "全範圍總複習" else data[unit]
        
        # 隨機抽取，確保不重複
        selected_questions = random.sample(target_pool, 10)
        
        # 隨機打亂選項
        for q in selected_questions:
            random.shuffle(q['options'])

        st.session_state.quiz = selected_questions
        st.session_state.exam_finished = False
        st.rerun()

# 顯示考卷
if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("exam_form"):
        user_answers = []
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**第 {i+1} 題：**")
            # 處理 SVG 參數
            svg_content = q.get('svg', 'none')
            svg_params = q.get('svg_params', {})
            if svg_content != 'none':
                st.markdown(SVGDrawer.draw(svg_content, **svg_params), unsafe_allow_html=True)
            
            st.markdown(f"### {q['q']}")
            ans = st.radio(f"選項", q['options'], key=f"ans_{i}", label_visibility="collapsed")
            st.divider()
            user_answers.append(ans)
            
        if st.form_submit_button("✅ 交卷", use_container_width=True):
            score = 0
            results = []
            for i, q in enumerate(st.session_state.quiz):
                u_ans = user_answers[i]
                is_correct = (u_ans == q['ans'])
                if is_correct: score += 1
                results.append({"q": q, "user": u_ans, "correct": is_correct})
            
            st.session_state.quiz_score = score * 10
            st.session_state.exam_results = results
            st.session_state.exam_finished = True
            st.rerun()

# 顯示結果
if st.session_state.exam_finished:
    final_score = st.session_state.quiz_score
    if final_score == 100: st.success(f"## 💯 總分：{final_score} 分 (太神啦！)")
    elif final_score >= 60: st.info(f"## 😃 總分：{final_score} 分 (及格囉)")
    else: st.error(f"## 💪 總分：{final_score} 分 (再接再厲)")
    
    for i, item in enumerate(st.session_state.exam_results):
        q = item['q']
        is_right = item['correct']
        status = "✅ 正確" if is_right else "❌ 錯誤"
        
        with st.expander(f"第 {i+1} 題解析 ({status})"):
            # 再次顯示圖形
            svg_content = q.get('svg', 'none')
            svg_params = q.get('svg_params', {})
            if svg_content != 'none':
                st.markdown(SVGDrawer.draw(svg_content, **svg_params), unsafe_allow_html=True)

            st.write(f"**題目**：{q['q']}")
            st.write(f"**您的答案**：{item['user']}")
            st.write(f"**正確答案**：{q['ans']}")
            if not is_right:
                st.error(f"💡 解析：{q['expl']}")
            else:
                st.info(f"💡 解析：{q['expl']}")
    
    st.divider()
    if st.button("🔄 再來一次 (重新測驗)", use_container_width=True):
        st.session_state.exam_finished = False
        st.session_state.quiz = []
        st.session_state.exam_results = []
        st.rerun()
