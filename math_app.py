import streamlit as st
import random
import math

# ==========================================
# 1. 數學核心引擎
# ==========================================
class MathUtils:
    @staticmethod
    def get_distractors(ans, mode="int"):
        distractors = set()
        count = 0
        if mode == "int": ans = int(ans)
        while len(distractors) < 3 and count < 50:
            count += 1
            if mode == "int":
                trap = random.choice([ans+random.randint(1,5), ans-random.randint(1,5), ans*2, int(ans/2), -ans, abs(ans-10), ans+10])
                if trap != ans: distractors.add(str(trap))
            elif mode == "float":
                trap = round(ans + random.choice([0.5, -0.5, 1.0, -1.0, 2.0]), 1)
                if trap != ans and trap > 0: distractors.add(str(trap))
            elif mode == "coord": 
                try:
                    parts = ans.replace('(','').replace(')','').split(',')
                    x, y = int(parts[0]), int(parts[1])
                    traps = [(y, x), (x, -y), (-x, y), (0,0), (x+5, y+5), (x-2, y+2)]
                    t = random.choice(traps)
                    t_str = f"({t[0]},{t[1]})"
                    if t_str != ans: distractors.add(t_str)
                except:
                    distractors.add("(0,0)")
        return list(distractors)

# ==========================================
# 2. 題庫工廠 (V25.1 完整版)
# ==========================================
class QuestionFactory:
    # --- 3-1 證明與推理 ---
    @staticmethod
    def gen_3_1(q_type):
        if q_type == "concept":
            subtype = random.choice(["congruence", "inequality", "logic", "bad_cond"])
            if subtype == "congruence":
                prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
                return {"q": f"若兩個三角形滿足「{prop}」對應相等，則它們？", "options": ["必全等", "相似", "面積相等", "不一定"], "ans": "必全等", "expl": f"{prop} 是全等性質。", "svg": "geometry_sas", "params": {}}
            elif subtype == "inequality":
                return {"q": "在一個三角形中，若 ∠A > ∠B，則對邊關係為何？", "options": ["BC > AC", "AC > BC", "BC = AC", "無法判斷"], "ans": "BC > AC", "expl": "大角對大邊性質。", "svg": "none", "params": {}}
            elif subtype == "logic":
                return {"q": "「若 P 則 Q」中，Q 稱為？", "options": ["結論", "題設", "逆敘述", "公理"], "ans": "結論", "expl": "邏輯定義。", "svg": "none", "params": {}}
            else:
                bad = random.choice(["SSA", "AAA"])
                return {"q": f"下列何者「無法」保證全等？", "options": [bad, "SAS", "ASA", "SSS"], "ans": bad, "expl": f"{bad} 不保證全等。", "svg": "none", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["angle_sum", "ext_angle", "side_angle", "poly"])
            if subtype == "angle_sum":
                a = random.randint(40, 80); b = random.randint(20, 180-a-10); ans = 180-a-b
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"△ABC 中，∠A={a}°，∠B={b}°，求 ∠C？", "options": opts, "ans": str(ans), "expl": "內角和180。", "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}}
            elif subtype == "ext_angle":
                a = random.randint(40, 80); b = random.randint(20, 180-a-10); ans = a + b
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角？", "options": opts, "ans": str(ans), "expl": "外角定理。", "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}}
            elif subtype == "side_angle":
                sides = [5, 6, 7]; random.shuffle(sides)
                a, b, c = sides[0], sides[1], sides[2]
                min_side = min(a, b, c)
                ans_map = {a: "∠A", b: "∠B", c: "∠C"}
                ans = ans_map[min_side]
                return {"q": f"△ABC 中，AB={c}, BC={a}, AC={b}，請問哪一個角最小？", "options": ["∠A", "∠B", "∠C", "一樣大"], "ans": ans, "expl": f"最小邊 {min_side} 對應最小角 {ans} (小邊對小角)。", "svg": "none", "params": {}}
            else:
                n = random.choice([5,6,8,10]); ans = (n-2)*180
                opts = [str(ans), str(n*180), "360", "720"]; random.shuffle(opts)
                return {"q": f"正 {n} 邊形內角和？", "options": opts, "ans": str(ans), "expl": "(n-2)*180。", "svg": "polygon_n", "params": {"n": n}}
        else: # Real
            scenarios = [
                {"q": "兩根吸管長 {s1}, {s2}，第三邊 x 的範圍？", "type": "sticks"},
                {"q": "地板鋪滿正六邊形磁磚，接點有 3 塊，利用了？", "type": "tiles"},
                {"q": "小明走捷徑穿越草地(三角形兩邊)，而不走直角轉彎，是因為？", "type": "shortcut"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "sticks":
                s1, s2 = random.randint(5, 20), random.randint(5, 20)
                min_x, max_x = abs(s1 - s2), s1 + s2
                opts = [f"{min_x} < x < {max_x}", f"x > {max_x}", f"x < {min_x}", f"x = {max_x}"]; random.shuffle(opts)
                return {"q": s["q"].format(s1=s1, s2=s2), "options": opts, "ans": f"{min_x} < x < {max_x}", "expl": "三角形兩邊和 > 第三邊。", "svg": "sticks_triangle", "params": {"s1": s1, "s2": s2}}
            elif s["type"] == "shortcut":
                return {"q": s["q"], "options": ["兩邊之和大於第三邊", "畢氏定理", "內角和180", "大角對大邊"], "ans": "兩邊之和大於第三邊", "expl": "直線距離最短。", "svg": "none", "params": {}}
            else:
                return {"q": s["q"], "options": ["內角120度x3=360", "邊長相等", "對角線等長", "面積相等"], "ans": "內角120度x3=360", "expl": "密鋪性質。", "svg": "polygon_n", "params": {"n": 6}}

    # --- 3-2 外心 ---
    @staticmethod
    def gen_3_2(q_type):
        if q_type == "concept":
            tri_type = random.choice([("鈍角", "外部"), ("直角", "斜邊中點"), ("銳角", "內部")])
            return {"q": f"「{tri_type[0]}三角形」的外心位置在哪裡？", "options": [tri_type[1], "頂點", "重心", "不一定"], "ans": tri_type[1], "expl": "外心位置性質。", "svg": "triangle_circumcenter", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["right_R", "reverse_R", "coord_O"])
            if subtype == "right_R":
                c = random.randint(5, 30) * 2; r = c // 2
                opts = MathUtils.get_distractors(r) + [str(r)]; random.shuffle(opts)
                return {"q": f"直角三角形斜邊長 {c}，外接圓半徑 R？", "options": opts, "ans": str(r), "expl": "直角外心在斜邊中點。", "svg": "right_triangle_circumcenter", "params": {}}
            elif subtype == "reverse_R":
                r = random.randint(3, 15); ans = r * 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"直角三角形的外接圓半徑為 {r}，求斜邊長？", "options": opts, "ans": str(ans), "expl": "斜邊 = 2R。", "svg": "right_triangle_circumcenter", "params": {}}
            else:
                k = random.randint(2, 8) * 2; ans = f"({k//2},{k//2})"
                opts = MathUtils.get_distractors(ans, "coord") + [ans]; random.shuffle(opts)
                return {"q": f"A(0,{k}), B({k},0), O(0,0)，求外心座標？", "options": opts, "ans": ans, "expl": "直角三角形外心為斜邊中點。", "svg": "coord_triangle", "params": {"k": k}}
        else: # Real
            scenarios = [
                {"q": "三村莊 A, B, C 想蓋共用水塔(到三點等距)，選址？", "type": "tower"},
                {"q": "考古學家挖到圓盤碎片，想復原圓盤大小，應找？", "type": "plate"},
                {"q": "要在圓形廣場周圍裝設三個監視器，監視器連線構成銳角三角形，監控中心(外心)會在？", "type": "camera"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "tower":
                return {"q": s["q"], "options": ["外心", "內心", "重心", "垂心"], "ans": "外心", "expl": "外心到三頂點等距。", "svg": "triangle_circumcenter", "params": {}}
            elif s["type"] == "plate":
                return {"q": s["q"], "options": ["中垂線交點(外心)", "角平分線(內心)", "中線(重心)", "切線"], "ans": "中垂線交點(外心)", "expl": "三點定圓(外心)。", "svg": "none", "params": {}}
            else:
                return {"q": s["q"], "options": ["廣場內部", "廣場外部", "邊緣", "不一定"], "ans": "廣場內部", "expl": "銳角三角形外心在內部。", "svg": "none", "params": {}}

    # --- 3-3 內心 ---
    @staticmethod
    def gen_3_3(q_type):
        if q_type == "concept":
            return {"q": "內心到三角形哪裡的距離相等？", "options": ["三邊", "三頂點", "三中點", "外部"], "ans": "三邊", "expl": "內切圓性質。", "svg": "triangle_incenter_concept", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["angle", "reverse_angle", "right_r", "area"])
            if subtype == "angle":
                deg = random.randint(30, 100); deg += 1 if deg%2!=0 else 0; ans = 90 + deg // 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"I 為內心，∠A={deg}°，求 ∠BIC？", "options": opts, "ans": str(ans), "expl": "90 + A/2。", "svg": "triangle_incenter_angle", "params": {"a": deg}}
            elif subtype == "right_r":
                k = random.randint(1,4); a,b,c = 3*k, 4*k, 5*k; ans = (a+b-c)//2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"直角三角形三邊 {a},{b},{c}，內切圓半徑？", "options": opts, "ans": str(ans), "expl": "(股+股-斜)/2。", "svg": "right_triangle_incenter", "params": {"a":a,"b":b,"c":c}}
            elif subtype == "area":
                s = random.randint(10, 30); r = random.randint(2, 6); area = s * r // 2
                opts = MathUtils.get_distractors(area) + [str(area)]; random.shuffle(opts)
                return {"q": f"周長 {s}，內切圓半徑 {r}，求三角形面積？", "options": opts, "ans": str(area), "expl": "面積 = rs/2。", "svg": "triangle_incenter_concept", "params": {}}
            else:
                ans_a = random.randint(40, 100); ans_a += 1 if ans_a%2!=0 else 0; bic = 90 + ans_a // 2
                opts = MathUtils.get_distractors(ans_a) + [str(ans_a)]; random.shuffle(opts)
                return {"q": f"I 為內心，若 ∠BIC={bic}°，則 ∠A 是幾度？", "options": opts, "ans": str(ans_a), "expl": "(BIC-90)*2。", "svg": "triangle_incenter_angle", "params": {"a": "?"}}
        else: # Real
            scenarios = [
                {"q": "公園內蓋最大圓形噴水池，圓心選？", "type": "fountain"},
                {"q": "物流中心要蓋在三條公路之間且等距，應選？", "type": "roads"},
                {"q": "想要做一個三角形的內切圓時鐘，圓心應如何找？", "type": "clock"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "fountain":
                return {"q": s["q"], "options": ["內心", "外心", "重心", "頂點"], "ans": "內心", "expl": "內切圓。", "svg": "triangle_incenter_concept", "params": {}}
            elif s["type"] == "roads":
                return {"q": s["q"], "options": ["內心", "外心", "重心", "中點"], "ans": "內心", "expl": "角平分線到兩邊等距。", "svg": "none", "params": {}}
            else:
                return {"q": s["q"], "options": ["角平分線交點", "中垂線交點", "中線交點", "高線交點"], "ans": "角平分線交點", "expl": "內心定義。", "svg": "none", "params": {}}

    # --- 3-4 重心 ---
    @staticmethod
    def gen_3_4(q_type):
        if q_type == "concept":
            return {"q": "重心是哪三條線的交點？", "options": ["中線", "中垂線", "角平分線", "高"], "ans": "中線", "expl": "重心定義。", "svg": "triangle_centroid", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["len_ratio", "coord_G", "area_div"])
            if subtype == "len_ratio":
                m = random.randint(3, 15) * 3; ans = m * 2 // 3
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"G 為重心，中線 AD 長 {m}，求 AG？", "options": opts, "ans": str(ans), "expl": "重心分中線 2:1。", "svg": "triangle_centroid", "params": {"m": m}}
            elif subtype == "coord_G":
                x1,y1=random.randint(0,6)*3,random.randint(0,6)*3
                x2,y2=random.randint(0,6)*3,random.randint(0,6)*3
                x3,y3=random.randint(0,6)*3,random.randint(0,6)*3
                gx,gy=(x1+x2+x3)//3, (y1+y2+y3)//3; ans = f"({gx},{gy})"
                opts = MathUtils.get_distractors(ans, "coord") + [ans]; random.shuffle(opts)
                return {"q": f"A({x1},{y1}), B({x2},{y2}), C({x3},{y3})，求重心 G？", "options": opts, "ans": ans, "expl": "三點座標相加除以 3。", "svg": "none", "params": {}}
            else:
                total = random.randint(2, 12) * 6; ans = total // 6
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"△ABC 面積 {total}，G 為重心，△GAB 內的中線分割出的最小三角形面積？", "options": opts, "ans": str(ans), "expl": "重心將面積六等分。", "svg": "triangle_centroid", "params": {}}
        else: # Real
            scenarios = [
                {"q": "手指頂住三角形木板平衡，支點是？", "type": "balance"},
                {"q": "要用一條繩子吊起一塊三角形招牌並保持水平，繩子應綁在？", "type": "hanging"},
                {"q": "把三角形披薩平分給 6 個人，切點應選？", "type": "pizza"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "balance":
                return {"q": s["q"], "options": ["重心", "內心", "外心", "垂心"], "ans": "重心", "expl": "物理重心。", "svg": "triangle_centroid", "params": {}}
            elif s["type"] == "hanging":
                return {"q": s["q"], "options": ["重心", "外心", "內心", "頂點"], "ans": "重心", "expl": "力矩平衡。", "svg": "none", "params": {}}
            else:
                return {"q": s["q"], "options": ["重心", "內心", "外心", "頂點"], "ans": "重心", "expl": "重心將面積六等分。", "svg": "none", "params": {}}

    # --- 4-1 因式分解 ---
    @staticmethod
    def gen_4_1(q_type):
        if q_type == "concept":
            return {"q": "若 ab=0，則？", "options": ["a=0 或 b=0", "a=0 且 b=0", "a=b", "無法判斷"], "ans": "a=0 或 b=0", "expl": "零積性質。", "svg": "none", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["diff_sq", "cross", "common_factor", "perfect_sq_k"])
            if subtype == "diff_sq":
                k = random.randint(2, 9); ans = f"(x+{k})(x-{k})"
                opts = [ans, f"(x-{k})²", f"(x+{k})²", f"x(x-{k})"]; random.shuffle(opts)
                return {"q": f"因式分解 x² - {k*k}？", "options": opts, "ans": ans, "expl": "平方差公式。", "svg": "diff_squares", "params": {"k": k}}
            elif subtype == "common_factor":
                a = random.randint(2, 5); b = random.randint(2, 5)
                ans = f"x({a}x+{b})"
                return {"q": f"因式分解 {a}x² + {b}x？", "options": [ans, f"x({a}x-{b})", f"x²({a}+{b})", f"({a}x+1)({b}x)"], "ans": ans, "expl": "提公因式 x。", "svg": "none", "params": {}}
            elif subtype == "perfect_sq_k":
                b = random.randint(2, 10) * 2; ans = (b // 2) ** 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"若 x² + {b}x + k 是完全平方式，求 k？", "options": opts, "ans": str(ans), "expl": "一次項係數一半的平方。", "svg": "area_square_k", "params": {}}
            else: # cross
                p = random.randint(1,5); q_val = random.randint(1,5); b = p+q_val; c = p*q_val
                ans = f"(x+{p})(x+{q_val})"
                opts = [ans, f"(x-{p})(x-{q_val})", f"(x+{p})(x-{q_val})", f"(x+{b})(x+1)"]; random.shuffle(opts)
                return {"q": f"因式分解 x² + {b}x + {c}？", "options": opts, "ans": ans, "expl": "十字交乘。", "svg": "none", "params": {}}
        else: # Real
            scenarios = [
                {"q": "長方形面積 {area}，長寬為整數，長寬關係？", "type": "rect"},
                {"q": "全班 x 人，剛好排成 x² + 5x + 6 的隊形，若 x=10，分兩隊？", "type": "group"},
                {"q": "某數平方減 9 可以被分解為 (x+3)(x-3)，這是利用？", "type": "diff"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "rect":
                area = random.randint(12, 50)
                return {"q": s["q"].format(area=area), "options": ["面積的因數", "面積的倍數", "必相等", "無關"], "ans": "面積的因數", "expl": "因數分解。", "svg": "rect_area", "params": {"area": area}}
            elif s["type"] == "group":
                return {"q": s["q"], "options": ["12和13", "10和16", "11和15", "無法計算"], "ans": "12和13", "expl": "(x+2)(x+3)。", "svg": "none", "params": {}}
            else:
                return {"q": s["q"], "options": ["平方差公式", "和的平方", "差的平方", "分配律"], "ans": "平方差公式", "expl": "a^2-b^2=(a+b)(a-b)。", "svg": "none", "params": {}}

    # --- 4-2 配方法 ---
    @staticmethod
    def gen_4_2(q_type):
        if q_type == "concept":
            case = random.choice(["pos", "zero", "neg"])
            if case == "pos":
                return {"q": "判別式 D > 0 代表？", "options": ["兩相異實根", "重根", "無實根", "無限多解"], "ans": "兩相異實根", "expl": "與 x 軸有兩個交點。", "svg": "none", "params": {}}
            elif case == "zero":
                return {"q": "判別式 D = 0 代表？", "options": ["重根(兩相等實根)", "兩相異實根", "無實根", "無解"], "ans": "重根(兩相等實根)", "expl": "與 x 軸相切。", "svg": "none", "params": {}}
            else:
                return {"q": "判別式 D < 0 代表？", "options": ["無實根", "重根", "兩相異實根", "無限多解"], "ans": "無實根", "expl": "與 x 軸無交點。", "svg": "parabola_d_neg", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["complete_sq", "sum_roots", "discriminant", "formula"])
            if subtype == "discriminant":
                d_case = random.choice(["pos", "zero", "neg"])
                if d_case == "pos":
                    eq = "x² + 5x + 4 = 0"; ans = "兩相異實根"; expl = "D = 25-16 > 0"
                elif d_case == "zero":
                    eq = "x² + 4x + 4 = 0"; ans = "重根"; expl = "D = 16-16 = 0"
                else:
                    eq = "x² + x + 5 = 0"; ans = "無實根"; expl = "D = 1-20 < 0"
                return {"q": f"方程式 {eq} 的根的性質？", "options": ["兩相異實根", "重根", "無實根", "無限多解"], "ans": ans, "expl": expl, "svg": "none", "params": {}}
            elif subtype == "complete_sq":
                k = random.randint(2, 10) * 2; ans = (k//2)**2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"x² + {k}x + □ 配成完全平方，□ = ？", "options": opts, "ans": str(ans), "expl": "一半的平方。", "svg": "area_square_k", "params": {}}
            elif subtype == "sum_roots":
                r1, r2 = random.randint(-5, 5), random.randint(-5, 5)
                b = -(r1 + r2); c = r1 * r2; ans = r1 + r2
                eq = f"x² + {b}x + {c} = 0" if b >= 0 else f"x² - {-b}x + {c} = 0"
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"方程式 {eq} 的兩根之和為何？", "options": opts, "ans": str(ans), "expl": "兩根和 = -b/a。", "svg": "none", "params": {}}
            else: # formula
                ans = "x = (-b ± √D) / 2a"
                opts = [ans, "x = -b / 2a", "x = (-b ± √D) / a", "x = b ± √D"]; random.shuffle(opts)
                return {"q": "一元二次方程式公式解為何？", "options": opts, "ans": ans, "expl": "公式解。", "svg": "none", "params": {}}
        else: # Real
            scenarios = [
                {"q": "長方形花圃長20寬10，中間開闢等寬道路，剩餘面積144，求路寬？", "type": "path"},
                {"q": "計算物體落地時間 t 得到虛數，代表？", "type": "imaginary"},
                {"q": "長方形剪掉正方形後與原形相似(黃金比例)，長寬比 x 的方程式？", "type": "golden"},
                {"q": "彈簧掛重物後長度 y = x² + 2x + 5，若 y=4 (比原長還短)，求 x？", "type": "spring"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "path":
                return {"q": s["q"], "options": ["2", "4", "5", "8"], "ans": "2", "expl": "(20-x)(10-x)=144，解得 x=2。", "svg": "rect_path", "params": {}}
            elif s["type"] == "imaginary":
                return {"q": s["q"], "options": ["物體不落地", "有兩個時間", "計算錯", "時間倒流"], "ans": "物體不落地", "expl": "無實數解。", "svg": "parabola_d_neg", "params": {}}
            elif s["type"] == "golden":
                return {"q": s["q"], "options": ["x²-x-1=0", "x²+x+1=0", "x²-1=0", "x=2"], "ans": "x²-x-1=0", "expl": "黃金比例定義。", "svg": "none", "params": {}}
            else:
                return {"q": s["q"], "options": ["無實數解", "x=1", "x=-1", "x=0"], "ans": "無實數解", "expl": "D < 0，不可能發生。", "svg": "none", "params": {}}

    # --- 4-3 應用問題 ---
    @staticmethod
    def gen_4_3(q_type):
        if q_type == "concept":
            return {"q": "解幾何邊長為負數，應？", "options": ["捨去", "取絕對值", "保留", "重算"], "ans": "捨去", "expl": "長度為正。", "svg": "none", "params": {}}
        elif q_type == "calc":
            subtype = random.choice(["num_sq", "max_val"])
            if subtype == "num_sq":
                n = random.randint(2, 10); val = n*n - n
                opts = MathUtils.get_distractors(n) + [str(n)]; random.shuffle(opts)
                return {"q": f"某正數平方減去該數等於 {val}，求該數？", "options": opts, "ans": str(n), "expl": "x^2-x-val=0。", "svg": "none", "params": {}}
            else:
                h = random.randint(1,5); k = random.randint(5,15); ans = k
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"y = -2(x-{h})² + {k} 的最大值？", "options": opts, "ans": str(ans), "expl": "頂點 y 座標。", "svg": "parabola_firework", "params": {}}
        else: # Real
            scenarios = [
                {"type": "ladder", "q": "梯子長 {c}，梯腳離牆 {a}，梯頂高度？"},
                {"type": "profit", "q": "賣 {p} 元時利潤最大，利潤函數可能是？"},
                {"type": "speed", "q": "甲乙兩地距離 {d} km，去程時速 {v1}，回程時速 {v2}，平均速率？"},
                {"type": "firework", "q": "煙火 h=30t-5t²，t={t} 時高度？"},
                {"type": "tv", "q": "電視長 {a} 吋，寬 {b} 吋，請問這是幾吋電視(對角線)？"},
                {"type": "taxi", "q": "計程車起跳 70 元，每公里加 20 元，跑 {x} 公里多少錢？"}
            ]
            s = random.choice(scenarios)
            if s["type"] == "ladder":
                m=random.randint(2,6); n=1; a=m*m-n*n; b=2*m*n; c=m*m+n*n
                opts = MathUtils.get_distractors(b) + [str(b)]; random.shuffle(opts)
                return {"q": s["q"].format(c=c, a=a), "options": opts, "ans": str(b), "expl": "畢氏定理。", "svg": "ladder_wall", "params": {"a":a,"b":b,"c":c}}
            elif s["type"] == "profit":
                p = random.randint(10, 50)
                return {"q": s["q"].format(p=p), "options": [f"y=-(x-{p})²+100", f"y=(x-{p})²+100", f"y=x-{p}", "y=x²"], "ans": f"y=-(x-{p})²+100", "expl": "開口向下拋物線頂點。", "svg": "none", "params": {}}
            elif s["type"] == "speed":
                d = 60; v1 = 20; v2 = 30; ans = 24
                return {"q": s["q"].format(d=d, v1=v1, v2=v2), "options": ["24", "25", "20", "30"], "ans": "24", "expl": "總距離/總時間 = 120/5 = 24。", "svg": "none", "params": {}}
            elif s["type"] == "firework":
                t=random.randint(2,4); h=30*t-5*t*t
                opts = [str(h), "0", "100", "50"]; random.shuffle(opts)
                return {"q": s["q"].format(t=t), "options": opts, "ans": str(h), "expl": "代入。", "svg": "parabola_firework", "params": {}}
            elif s["type"] == "tv":
                k = random.randint(5, 10); a, b, c = 4*k, 3*k, 5*k
                opts = MathUtils.get_distractors(c) + [str(c)]; random.shuffle(opts)
                return {"q": s["q"].format(a=a, b=b), "options": opts, "ans": str(c), "expl": "畢氏定理求對角線。", "svg": "rect_diag", "params": {"a":a, "b":b}}
            elif s["type"] == "taxi":
                x = random.randint(2, 10); ans = 70 + 20 * x
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": s["q"].format(x=x), "options": opts, "ans": str(ans), "expl": "y = 20x + 70。", "svg": "none", "params": {}}

    @staticmethod
    def generate(unit):
        mapping = {
            "3-1 證明與推理": QuestionFactory.gen_3_1, "3-2 三角形的外心": QuestionFactory.gen_3_2,
            "3-3 三角形的內心": QuestionFactory.gen_3_3, "3-4 三角形的重心": QuestionFactory.gen_3_4,
            "4-1 因式分解法": QuestionFactory.gen_4_1, "4-2 配方法與公式解": QuestionFactory.gen_4_2,
            "4-3 應用問題": QuestionFactory.gen_4_3
        }
        generator = mapping.get(unit)
        if not generator: return None
        return [generator("concept"), generator("calc"), generator("real")]

# ==========================================
# 3. 視覺繪圖引擎 (V25.1 緊湊版)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="220" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        if svg_type == "rect_path":
            return base.format('<rect x="50" y="50" width="200" height="120" fill="#81c784" stroke="black"/><rect x="140" y="50" width="20" height="120" fill="#e0e0e0" stroke="none"/><rect x="50" y="100" width="200" height="20" fill="#e0e0e0" stroke="none"/><text x="145" y="45">x</text><text x="30" y="115">x</text><text x="260" y="115">長20</text><text x="140" y="190">寬10</text>')
        elif svg_type == "triangle_incenter_angle":
            a_val = kwargs.get("a", "?")
            return base.format(f'<path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/><text x="150" y="25" font-size="16" text-anchor="middle" font-weight="bold">A ({a_val}°)</text><text x="25" y="200" font-size="16" font-weight="bold">B</text><text x="275" y="200" font-size="16" font-weight="bold">C</text><circle cx="150" cy="132.2" r="57.8" fill="#fff9c4" stroke="#fbc02d" stroke-width="2" opacity="0.6"/><circle cx="150" cy="132.2" r="4" fill="red"/><text x="150" y="125" fill="red" font-size="14" text-anchor="middle" font-weight="bold">I</text><line x1="40" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/><line x1="260" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/><text x="150" y="170" fill="blue" font-size="20" text-anchor="middle" font-weight="bold">?</text>')
        elif svg_type == "right_triangle_incenter":
            a = kwargs.get("a", 3); b = kwargs.get("b", 4); c = kwargs.get("c", 5)
            return base.format(f'<path d="M50,40 L50,180 L200,180 Z" fill="none" stroke="black" stroke-width="2"/><rect x="50" y="160" width="20" height="20" fill="none" stroke="black"/><circle cx="85" cy="145" r="35" fill="#e1bee7" stroke="purple" opacity="0.5"/><text x="30" y="110" font-size="14">{a}</text><text x="120" y="200" font-size="14">{b}</text><text x="130" y="100" font-size="14">{c}</text><text x="85" y="150" fill="purple" font-weight="bold">r?</text>')
        elif svg_type == "triangle_incenter_concept":
            return base.format('<path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="132.2" r="57.8" fill="none" stroke="orange" stroke-width="2"/><circle cx="150" cy="132.2" r="4" fill="orange"/><text x="150" y="125" fill="orange" font-weight="bold" text-anchor="middle">I</text><line x1="150" y1="132.2" x2="150" y2="190" stroke="orange" stroke-width="2" stroke-dasharray="4"/><text x="155" y="165" font-size="14" fill="gray" font-weight="bold">r</text>')
        elif svg_type == "general_triangle":
            a = kwargs.get("angle_a", 60); b = kwargs.get("angle_b", 60)
            return base.format(f'<path d="M80,150 L220,150 L120,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/><text x="110" y="40" font-size="14">A({a}°)</text><text x="60" y="160" font-size="14">B({b}°)</text><text x="230" y="160" font-size="14" fill="red">C(?)</text>')
        elif svg_type == "sticks_triangle":
            s1 = kwargs.get("s1", 5); s2 = kwargs.get("s2", 5); total = s1 + s2 if s1+s2 > 0 else 1; scale = 150 / total
            return base.format(f'<rect x="50" y="80" width="{s1*scale}" height="10" fill="blue"/><rect x="50" y="110" width="{s2*scale}" height="10" fill="green"/><text x="50" y="70" fill="blue">長度 {s1}</text><text x="50" y="140" fill="green">長度 {s2}</text><text x="200" y="100" fill="red">第三邊 x ?</text>')
        elif svg_type == "ladder_wall":
            a = kwargs.get("a", 3); c = kwargs.get("c", 5)
            return base.format(f'<line x1="50" y1="20" x2="50" y2="180" stroke="black" stroke-width="4"/><line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="4"/><line x1="50" y1="60" x2="130" y2="180" stroke="brown" stroke-width="5"/><text x="20" y="120" font-size="14">高?</text><text x="80" y="195" font-size="14">底{a}</text><text x="100" y="110" font-size="14" fill="brown">斜{c}</text>')
        elif svg_type == "rect_diag":
            a = kwargs.get("a", 4); b = kwargs.get("b", 3)
            return base.format(f'<rect x="50" y="40" width="160" height="120" fill="#333"/><rect x="55" y="45" width="150" height="110" fill="#fff"/><line x1="55" y1="45" x2="205" y2="155" stroke="red" stroke-width="2"/><text x="130" y="100" fill="red" font-weight="bold">?</text><text x="130" y="175">{a} 吋</text><text x="20" y="100">{b} 吋</text>')
        elif svg_type == "polygon_n":
            n = kwargs.get("n", 5); points = []
            for i in range(n):
                angle = 2 * math.pi * i / n - math.pi / 2
                points.append(f"{150 + 70 * math.cos(angle)},{100 + 70 * math.sin(angle)}")
            return base.format(f'<polygon points="{" ".join(points)}" fill="#f3e5f5" stroke="purple" stroke-width="2"/><text x="130" y="105" fill="purple">正{n}邊形</text>')
        elif svg_type == "diff_squares":
            k = kwargs.get("k", 3)
            return base.format(f'<rect x="80" y="40" width="140" height="140" fill="#e8f5e9" stroke="black"/><rect x="180" y="140" width="40" height="40" fill="white" stroke="red" stroke-dasharray="4"/><text x="130" y="110" font-size="20">x²</text><text x="190" y="165" font-size="12" fill="red">{k}²</text>')
        elif svg_type == "coord_triangle":
            k = kwargs.get("k", 4)
            return base.format(f'<line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="2"/><line x1="20" y1="20" x2="20" y2="180" stroke="black" stroke-width="2"/><path d="M20,20 L180,180 L20,180 Z" fill="none" stroke="blue"/><text x="10" y="20">A(0,{k})</text><text x="180" y="195">B({k},0)</text><text x="5" y="195">O</text>')
        elif svg_type == "geometry_sas":
            return base.format('<path d="M30,120 L90,120 L60,40 Z" fill="none" stroke="black"/><path d="M160,120 L220,120 L190,40 Z" fill="none" stroke="black"/><text x="110" y="80" fill="blue">全等?</text>')
        elif svg_type == "right_triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#e0e0e0"/><path d="M90,40 L90,160 L210,160 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="150" cy="100" r="5" fill="red"/><text x="160" y="95" fill="red">O</text>')
        elif svg_type == "triangle_circumcenter":
            return base.format('<circle cx="150" cy="100" r="80" fill="none" stroke="#b2dfdb"/><path d="M150,20 L80,140 L220,140 Z" fill="none" stroke="black"/><circle cx="150" cy="100" r="4" fill="green"/><text x="150" y="90" fill="green">O</text>')
        elif svg_type == "triangle_centroid":
            return base.format('<path d="M150,20 L50,180 L250,180 Z" fill="none" stroke="black"/><line x1="150" y1="20" x2="150" y2="180" stroke="red" stroke-dasharray="4"/><circle cx="150" cy="126" r="5" fill="blue"/><text x="160" y="130" fill="blue">G</text>')
        elif svg_type == "rect_area":
            area = kwargs.get("area", 24)
            return base.format(f'<rect x="50" y="50" width="200" height="100" fill="#fff9c4" stroke="orange" stroke-width="2"/><text x="120" y="105" font-size="20">Area = {area}</text>')
        elif svg_type == "parabola_d_neg":
            return base.format('<path d="M50,50 Q150,180 250,50" fill="none" stroke="gray" stroke-dasharray="4"/><line x1="20" y1="150" x2="280" y2="150" stroke="black"/><text x="120" y="170">無交點 (D<0)</text>')
        elif svg_type == "parabola_firework":
            return base.format('<path d="M20,180 Q150,-50 280,180" fill="none" stroke="red" stroke-width="2"/><circle cx="150" cy="40" r="5" fill="orange"/><text x="160" y="40">最高點</text>')
        elif svg_type == "area_square_k":
            return base.format('<rect x="100" y="50" width="100" height="100" fill="#fff3e0" stroke="black" stroke-dasharray="4"/><text x="150" y="105" text-anchor="middle">補項?</text>')
        return ""

# ==========================================
# 4. APP 介面
# ==========================================
st.set_page_config(page_title="國中數學雲端教室", page_icon="♾️")
st.title("♾️ 國中數學無限生成引擎 (V25.1 完整修復版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

units = ["3-1 證明與推理", "3-2 三角形的外心", "3-3 三角形的內心", "3-4 三角形的重心", "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題"]
unit = st.sidebar.selectbox("請選擇練習單元", units)

if st.sidebar.button("🚀 生成無限試卷 (全功能無刪減)"):
    new_quiz = QuestionFactory.generate(unit)
    if new_quiz:
        st.session_state.quiz = new_quiz
        st.session_state.exam_finished = False
        st.rerun()

if st.session_state.quiz and not st.session_state.exam_finished:
    with st.form("quiz_form"):
        u_answers = []
        type_names = ["觀念", "計算", "情境"]
        for i, q in enumerate(st.session_state.quiz):
            badge = type_names[i] if i < 3 else "綜合"
            st.markdown(f"### Q{i+1} <span style='background-color:#e0f7fa; padding:2px 8px; border-radius:4px; font-size:0.7em; color:#006064'>{badge}</span> {q['q']}", unsafe_allow_html=True)
            if q.get('svg') != "none":
                st.markdown(SVGDrawer.draw(q['svg'], **q.get('params', {})), unsafe_allow_html=True)
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
    final_score = int((score / 3) * 100)
    st.success(f"## 您的最終得分: {final_score} 分")
    if st.button("🔄 再生成一份 (題目會完全不同)", use_container_width=True):
        new_quiz = QuestionFactory.generate(unit)
        st.session_state.quiz = new_quiz
        st.session_state.exam_finished = False
        st.rerun()
