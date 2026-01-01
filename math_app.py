import streamlit as st
import random
import math

# ==========================================
# 1. 數學工具箱
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
                trap = random.choice([
                    ans + random.randint(1, 5), 
                    ans - random.randint(1, 5),
                    ans * 2, 
                    int(ans / 2), 
                    -ans,
                    abs(ans - 10),
                    ans + 10
                ])
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
# 2. 無限題庫工廠 (V20 - 真正的全功能融合)
# ==========================================
class QuestionFactory:
    
    # --- 3-1 證明與推理 ---
    @staticmethod
    def gen_3_1(q_type):
        if q_type == "concept":
            subtype = random.choice(["congruence", "bad_cond", "definition"])
            if subtype == "congruence":
                prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
                return {"q": f"若兩個三角形滿足「{prop}」對應相等，則它們的關係？", "options": ["必全等", "相似", "面積相等", "不一定"], "ans": "必全等", "expl": f"{prop} 是全等性質。", "svg": "geometry_sas", "params": {}}
            elif subtype == "bad_cond":
                bad = random.choice(["SSA", "AAA"])
                return {"q": f"下列何者「無法」保證全等？", "options": [bad, "SAS", "ASA", "SSS"], "ans": bad, "expl": f"{bad} 不保證全等。", "svg": "none", "params": {}}
            else:
                return {"q": "「若 P 則 Q」中，P 稱為？", "options": ["題設(前件)", "結論", "逆敘述", "公理"], "ans": "題設(前件)", "expl": "邏輯定義。", "svg": "none", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：三種計算題型
            subtype = random.choice(["tri_angle", "ext_angle", "poly_angle"])
            if subtype == "tri_angle":
                a = random.randint(40, 80); b = random.randint(20, 180-a-10); ans = 180-a-b
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"△ABC 中，∠A={a}°，∠B={b}°，求 ∠C？", "options": opts, "ans": str(ans), "expl": "內角和180。", "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}}
            elif subtype == "ext_angle":
                a = random.randint(40, 80); b = random.randint(20, 180-a-10); ans = a + b
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角？", "options": opts, "ans": str(ans), "expl": "外角定理。", "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}}
            else:
                n = random.choice([5,6,8,10,12]); ans = (n-2)*180
                opts = [str(ans), str(n*180), "360", "720"]; random.shuffle(opts)
                return {"q": f"正 {n} 邊形內角和？", "options": opts, "ans": str(ans), "expl": "(n-2)*180。", "svg": "polygon_n", "params": {"n": n}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["sticks", "tiles"])
            if subtype == "sticks":
                s1 = random.randint(5, 20); s2 = random.randint(5, 20)
                min_x, max_x = abs(s1 - s2), s1 + s2
                opts = [f"{min_x} < x < {max_x}", f"x > {max_x}", f"x < {min_x}", f"x = {max_x}"]; random.shuffle(opts)
                return {"q": f"兩根吸管長 {s1}, {s2}，第三邊 x 的範圍？", "options": opts, "ans": f"{min_x} < x < {max_x}", "expl": "三角形邊長性質。", "svg": "sticks_triangle", "params": {"s1": s1, "s2": s2}}
            else:
                return {"q": "地板要鋪滿正六邊形磁磚，每個接點有 3 塊磁磚，這是利用？", "options": ["內角120度x3=360", "邊長相等", "對角線等長", "面積相等"], "ans": "內角120度x3=360", "expl": "密鋪性質。", "svg": "polygon_n", "params": {"n": 6}}

    # --- 3-2 外心 ---
    @staticmethod
    def gen_3_2(q_type):
        if q_type == "concept":
            tri_type = random.choice([("鈍角", "外部"), ("直角", "斜邊中點"), ("銳角", "內部")])
            return {"q": f"「{tri_type[0]}三角形」的外心在哪？", "options": [tri_type[1], "頂點", "重心", "不一定"], "ans": tri_type[1], "expl": "外心位置性質。", "svg": "triangle_circumcenter", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：包含 Reverse R (逆推)
            subtype = random.choice(["right_R", "reverse_R", "coord_O"])
            if subtype == "right_R":
                c = random.randint(5, 30) * 2; r = c // 2
                opts = MathUtils.get_distractors(r) + [str(r)]; random.shuffle(opts)
                return {"q": f"直角三角形斜邊長 {c}，外接圓半徑 R？", "options": opts, "ans": str(r), "expl": "斜邊一半。", "svg": "right_triangle_circumcenter", "params": {}}
            elif subtype == "reverse_R":
                r = random.randint(3, 15); ans = r * 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"直角三角形的外接圓半徑為 {r}，求斜邊長？", "options": opts, "ans": str(ans), "expl": "斜邊 = 2R。", "svg": "right_triangle_circumcenter", "params": {}}
            else:
                k = random.randint(2, 8) * 2; ans = f"({k//2},{k//2})"
                opts = MathUtils.get_distractors(ans, "coord") + [ans]; random.shuffle(opts)
                return {"q": f"A(0,{k}), B({k},0), O(0,0)，求外心？", "options": opts, "ans": ans, "expl": "斜邊中點。", "svg": "coord_triangle", "params": {"k": k}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["water_tower", "broken_plate"])
            if subtype == "water_tower":
                return {"q": "三村莊 A, B, C 想蓋共用水塔(到三點等距)，選址？", "options": ["外心", "內心", "重心", "垂心"], "ans": "外心", "expl": "外心到頂點等距。", "svg": "triangle_circumcenter", "params": {}}
            else:
                return {"q": "考古學家挖到圓盤碎片(圓弧)，想復原圓盤，應找圓弧上的點作？", "options": ["中垂線交點(外心)", "角平分線(內心)", "中線(重心)", "切線"], "ans": "中垂線交點(外心)", "expl": "三點定圓(外心)。", "svg": "none", "params": {}}

    # --- 3-3 內心 ---
    @staticmethod
    def gen_3_3(q_type):
        if q_type == "concept":
            return {"q": "內心到哪裡的距離相等？", "options": ["三邊", "三頂點", "三中點", "外部"], "ans": "三邊", "expl": "內切圓性質。", "svg": "triangle_incenter_concept", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：包含 Reverse Angle (逆推角度) 和 Right r (直角內切圓)
            subtype = random.choice(["angle", "reverse_angle", "right_r", "area"])
            if subtype == "angle":
                deg = random.randint(30, 100); deg += 1 if deg%2!=0 else 0; ans = 90 + deg // 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"I 為內心，∠A={deg}°，求 ∠BIC？", "options": opts, "ans": str(ans), "expl": "90 + A/2。", "svg": "triangle_incenter_angle", "params": {"a": deg}}
            elif subtype == "reverse_angle":
                ans_a = random.randint(40, 100); ans_a += 1 if ans_a%2!=0 else 0; bic = 90 + ans_a // 2
                opts = MathUtils.get_distractors(ans_a) + [str(ans_a)]; random.shuffle(opts)
                return {"q": f"I 為內心，若 ∠BIC={bic}°，則 ∠A 是幾度？", "options": opts, "ans": str(ans_a), "expl": "(BIC-90)*2。", "svg": "triangle_incenter_angle", "params": {"a": "?"}}
            elif subtype == "right_r":
                k = random.randint(1,4); a,b,c = 3*k, 4*k, 5*k; ans = (a+b-c)//2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"直角三角形三邊 {a},{b},{c}，內切圓半徑？", "options": opts, "ans": str(ans), "expl": "(股+股-斜)/2。", "svg": "right_triangle_incenter", "params": {"a":a,"b":b,"c":c}}
            else:
                s = random.randint(10, 30); r = random.randint(2, 6); area = s * r // 2
                opts = MathUtils.get_distractors(area) + [str(area)]; random.shuffle(opts)
                return {"q": f"周長 {s}，內切圓半徑 {r}，面積？", "options": opts, "ans": str(area), "expl": "rs/2。", "svg": "triangle_incenter_concept", "params": {}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["fountain", "roads"])
            if subtype == "fountain":
                return {"q": "公園內蓋最大圓形噴水池，圓心選？", "options": ["內心", "外心", "重心", "頂點"], "ans": "內心", "expl": "內切圓。", "svg": "triangle_incenter_concept", "params": {}}
            else:
                return {"q": "物流中心要蓋在三條公路(圍成三角形)之間，且到三條路距離相等，應選？", "options": ["內心", "外心", "重心", "中點"], "ans": "內心", "expl": "角平分線到兩邊等距。", "svg": "none", "params": {}}

    # --- 3-4 重心 ---
    @staticmethod
    def gen_3_4(q_type):
        if q_type == "concept":
            return {"q": "重心是哪三條線的交點？", "options": ["中線", "中垂線", "角平分線", "高"], "ans": "中線", "expl": "重心定義。", "svg": "triangle_centroid", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：包含 coord_G (座標重心)
            subtype = random.choice(["len_ratio", "coord_G", "area_div"])
            if subtype == "len_ratio":
                m = random.randint(3, 15) * 3; ans = m * 2 // 3
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"G 為重心，中線 AD 長 {m}，求 AG？", "options": opts, "ans": str(ans), "expl": "2:1 性質。", "svg": "triangle_centroid", "params": {"m": m}}
            elif subtype == "coord_G":
                x1,y1=random.randint(0,6)*3,random.randint(0,6)*3
                x2,y2=random.randint(0,6)*3,random.randint(0,6)*3
                x3,y3=random.randint(0,6)*3,random.randint(0,6)*3
                gx,gy=(x1+x2+x3)//3, (y1+y2+y3)//3; ans = f"({gx},{gy})"
                opts = MathUtils.get_distractors(ans, "coord") + [ans]; random.shuffle(opts)
                return {"q": f"A({x1},{y1}), B({x2},{y2}), C({x3},{y3})，求重心 G？", "options": opts, "ans": ans, "expl": "三點座標平均。", "svg": "none", "params": {}}
            else:
                total = random.randint(2, 12) * 6; ans = total // 6
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"△ABC 面積 {total}，G 為重心，△GAB 內的中線分割出的最小三角形面積？", "options": opts, "ans": str(ans), "expl": "六等分。", "svg": "triangle_centroid", "params": {}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["balance", "hanging"])
            if subtype == "balance":
                return {"q": "手指頂住三角形木板平衡，支點是？", "options": ["重心", "內心", "外心", "垂心"], "ans": "重心", "expl": "物理重心。", "svg": "triangle_centroid", "params": {}}
            else:
                return {"q": "要用一條繩子吊起一塊三角形招牌並保持水平，繩子應綁在？", "options": ["重心", "外心", "內心", "頂點"], "ans": "重心", "expl": "力矩平衡。", "svg": "none", "params": {}}

    # --- 4-1 因式分解 ---
    @staticmethod
    def gen_4_1(q_type):
        if q_type == "concept":
            return {"q": "若 ab=0，則？", "options": ["a=0 或 b=0", "a=0 且 b=0", "a=b", "無法判斷"], "ans": "a=0 或 b=0", "expl": "零積性質。", "svg": "none", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：包含 perfect_sq_k (完全平方常數)
            subtype = random.choice(["diff_sq", "cross", "perfect_sq_k"])
            if subtype == "diff_sq":
                k = random.randint(2, 9); ans = f"(x+{k})(x-{k})"
                opts = [ans, f"(x-{k})²", f"(x+{k})²", f"x(x-{k})"]; random.shuffle(opts)
                return {"q": f"因式分解 x² - {k*k}？", "options": opts, "ans": ans, "expl": "平方差。", "svg": "diff_squares", "params": {"k": k}}
            elif subtype == "perfect_sq_k":
                b = random.randint(2, 10) * 2; ans = (b // 2) ** 2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"若 x² + {b}x + k 是完全平方式，求 k？", "options": opts, "ans": str(ans), "expl": "一次項係數一半的平方。", "svg": "area_square_k", "params": {}}
            else:
                p = random.randint(1,5); q_val = random.randint(1,5); b = p+q_val; c = p*q_val
                ans = f"(x+{p})(x+{q_val})"
                opts = [ans, f"(x-{p})(x-{q_val})", f"(x+{p})(x-{q_val})", f"(x+{b})(x+1)"]; random.shuffle(opts)
                return {"q": f"因式分解 x² + {b}x + {c}？", "options": opts, "ans": ans, "expl": "十字交乘。", "svg": "none", "params": {}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["rect_area", "grouping"])
            if subtype == "rect_area":
                area = random.randint(12, 50)
                return {"q": f"長方形面積 {area}，長寬為整數，長寬關係？", "options": ["面積的因數", "面積的倍數", "必相等", "無關"], "ans": "面積的因數", "expl": "因數分解。", "svg": "rect_area", "params": {"area": area}}
            else:
                return {"q": "全班 x 人，剛好排成 x² + 5x + 6 的隊形，若 x=10，可分成兩大隊分別多少人？", "options": ["12和13", "10和16", "11和15", "無法計算"], "ans": "12和13", "expl": "(x+2)(x+3)。", "svg": "none", "params": {}}

    # --- 4-2 配方法 ---
    @staticmethod
    def gen_4_2(q_type):
        if q_type == "concept":
            return {"q": "判別式 D < 0 代表？", "options": ["無實根", "重根", "兩相異實根", "無限多解"], "ans": "無實根", "expl": "無交點。", "svg": "parabola_d_neg", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：包含 sum_roots (根與係數)
            subtype = random.choice(["complete_sq", "sum_roots", "formula"])
            if subtype == "complete_sq":
                k = random.randint(2, 10) * 2; ans = (k//2)**2
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"x² + {k}x + □ 配成完全平方，□ = ？", "options": opts, "ans": str(ans), "expl": "一半的平方。", "svg": "area_square_k", "params": {}}
            elif subtype == "sum_roots":
                r1, r2 = random.randint(-5, 5), random.randint(-5, 5)
                b = -(r1 + r2); c = r1 * r2; ans = r1 + r2
                eq = f"x² + {b}x + {c} = 0" if b >= 0 else f"x² - {-b}x + {c} = 0"
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"方程式 {eq} 的兩根之和為何？", "options": opts, "ans": str(ans), "expl": "-b/a。", "svg": "none", "params": {}}
            else:
                ans = "x = (-b ± √D) / 2a"
                opts = [ans, "x = -b / 2a", "x = (-b ± √D) / a", "x = b ± √D"]; random.shuffle(opts)
                return {"q": "一元二次方程式公式解為何？", "options": opts, "ans": ans, "expl": "公式解。", "svg": "none", "params": {}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["imaginary_time", "golden_ratio"])
            if subtype == "imaginary_time":
                return {"q": "計算物體落地時間 t 得到虛數，代表？", "options": ["物體不落地", "有兩個時間", "計算錯", "時間倒流"], "ans": "物體不落地", "expl": "無實數解。", "svg": "parabola_d_neg", "params": {}}
            else:
                return {"q": "長方形剪掉正方形後與原形相似(黃金比例)，長寬比 x 的方程式？", "options": ["x²-x-1=0", "x²+x+1=0", "x²-1=0", "x=2"], "ans": "x²-x-1=0", "expl": "黃金比例定義。", "svg": "none", "params": {}}

    # --- 4-3 應用問題 ---
    @staticmethod
    def gen_4_3(q_type):
        if q_type == "concept":
            return {"q": "解幾何邊長為負數，應？", "options": ["捨去", "取絕對值", "保留", "重算"], "ans": "捨去", "expl": "長度為正。", "svg": "none", "params": {}}
        
        elif q_type == "calc":
            # V18 保留：包含 max_val (極值)
            subtype = random.choice(["num_sq", "max_val"])
            if subtype == "num_sq":
                n = random.randint(2, 10); val = n*n - n
                opts = MathUtils.get_distractors(n) + [str(n)]; random.shuffle(opts)
                return {"q": f"某正數平方減去該數等於 {val}，求該數？", "options": opts, "ans": str(n), "expl": "x^2-x-val=0。", "svg": "none", "params": {}}
            else:
                h = random.randint(1,5); k = random.randint(5,15); ans = k
                opts = MathUtils.get_distractors(ans) + [str(ans)]; random.shuffle(opts)
                return {"q": f"y = -2(x-{h})² + {k} 的最大值？", "options": opts, "ans": str(ans), "expl": "頂點 y 座標。", "svg": "parabola_firework", "params": {}}
        
        else: # Real (V19 融合)
            subtype = random.choice(["ladder", "firework", "profit"])
            if subtype == "ladder":
                m=random.randint(2,6); n=1; a=m*m-n*n; b=2*m*n; c=m*m+n*n
                opts = MathUtils.get_distractors(b) + [str(b)]; random.shuffle(opts)
                return {"q": f"梯子長 {c}，梯腳離牆 {a}，梯頂高度？", "options": opts, "ans": str(b), "expl": "畢氏定理。", "svg": "ladder_wall", "params": {"a":a,"b":b,"c":c}}
            elif subtype == "firework":
                t=random.randint(2,4); h=30*t-5*t*t
                opts = [str(h), "0", "100", "50"]; random.shuffle(opts)
                return {"q": f"煙火 h=30t-5t²，t={t} 時高度？", "options": opts, "ans": str(h), "expl": "代入。", "svg": "parabola_firework", "params": {}}
            else:
                p = random.randint(10, 50)
                return {"q": f"賣 {p} 元時利潤最大，利潤函數可能是？", "options": [f"y=-(x-{p})²+100", f"y=(x-{p})²+100", f"y=x-{p}", "y=x²"], "ans": f"y=-(x-{p})²+100", "expl": "開口向下拋物線頂點。", "svg": "none", "params": {}}

    @staticmethod
    def generate(unit):
        mapping = {
            "3-1 證明與推理": QuestionFactory.gen_3_1,
            "3-2 三角形的外心": QuestionFactory.gen_3_2,
            "3-3 三角形的內心": QuestionFactory.gen_3_3,
            "3-4 三角形的重心": QuestionFactory.gen_3_4,
            "4-1 因式分解法": QuestionFactory.gen_4_1,
            "4-2 配方法與公式解": QuestionFactory.gen_4_2,
            "4-3 應用問題": QuestionFactory.gen_4_3
        }
        generator = mapping.get(unit)
        if not generator: return None
        return [generator("concept"), generator("calc"), generator("real")]

# ==========================================
# 3. 視覺繪圖引擎 (V20 - 包含所有圖形)
# ==========================================
class SVGDrawer:
    @staticmethod
    def draw(svg_type, **kwargs):
        base = '<svg width="300" height="220" xmlns="http://www.w3.org/2000/svg" style="background-color:white; border:1px solid #eee; border-radius:8px;">{}</svg>'
        
        if svg_type == "triangle_incenter_angle":
            a_val = kwargs.get("a", "?")
            return base.format(f'''
                <path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/>
                <text x="150" y="25" font-size="16" text-anchor="middle" font-weight="bold">A ({a_val}°)</text>
                <text x="25" y="200" font-size="16" font-weight="bold">B</text>
                <text x="275" y="200" font-size="16" font-weight="bold">C</text>
                <circle cx="150" cy="132.2" r="57.8" fill="#fff9c4" stroke="#fbc02d" stroke-width="2" opacity="0.6"/>
                <circle cx="150" cy="132.2" r="4" fill="red"/>
                <text x="150" y="125" fill="red" font-size="14" text-anchor="middle" font-weight="bold">I</text>
                <line x1="40" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
                <line x1="260" y1="190" x2="150" y2="132.2" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
                <text x="150" y="170" fill="blue" font-size="20" text-anchor="middle" font-weight="bold">?</text>
            ''')
        elif svg_type == "right_triangle_incenter":
            a = kwargs.get("a", 3); b = kwargs.get("b", 4); c = kwargs.get("c", 5)
            return base.format(f'''
                <path d="M50,40 L50,180 L200,180 Z" fill="none" stroke="black" stroke-width="2"/>
                <rect x="50" y="160" width="20" height="20" fill="none" stroke="black"/>
                <circle cx="85" cy="145" r="35" fill="#e1bee7" stroke="purple" opacity="0.5"/>
                <text x="30" y="110" font-size="14">{a}</text>
                <text x="120" y="200" font-size="14">{b}</text>
                <text x="130" y="100" font-size="14">{c}</text>
                <text x="85" y="150" fill="purple" font-weight="bold">r?</text>
            ''')
        elif svg_type == "triangle_incenter_concept":
            return base.format('''
                <path d="M150,30 L40,190 L260,190 Z" fill="none" stroke="black" stroke-width="2"/>
                <circle cx="150" cy="132.2" r="57.8" fill="none" stroke="orange" stroke-width="2"/>
                <circle cx="150" cy="132.2" r="4" fill="orange"/>
                <text x="150" y="125" fill="orange" font-weight="bold" text-anchor="middle">I</text>
                <line x1="150" y1="132.2" x2="150" y2="190" stroke="orange" stroke-width="2" stroke-dasharray="4"/>
                <text x="155" y="165" font-size="14" fill="gray" font-weight="bold">r</text>
            ''')
        elif svg_type == "general_triangle":
            a = kwargs.get("angle_a", 60); b = kwargs.get("angle_b", 60)
            return base.format(f'''
                <path d="M80,150 L220,150 L120,50 Z" fill="#e3f2fd" stroke="black" stroke-width="2"/>
                <text x="110" y="40" font-size="14">A({a}°)</text>
                <text x="60" y="160" font-size="14">B({b}°)</text>
                <text x="230" y="160" font-size="14" fill="red">C(?)</text>
            ''')
        elif svg_type == "sticks_triangle":
            s1 = kwargs.get("s1", 5); s2 = kwargs.get("s2", 5); total = s1 + s2 if s1+s2 > 0 else 1; scale = 150 / total
            return base.format(f'''
                <rect x="50" y="80" width="{s1*scale}" height="10" fill="blue"/>
                <rect x="50" y="110" width="{s2*scale}" height="10" fill="green"/>
                <text x="50" y="70" fill="blue">長度 {s1}</text>
                <text x="50" y="140" fill="green">長度 {s2}</text>
                <text x="200" y="100" fill="red">第三邊 x ?</text>
            ''')
        elif svg_type == "ladder_wall":
            a = kwargs.get("a", 3); c = kwargs.get("c", 5)
            return base.format(f'''
                <line x1="50" y1="20" x2="50" y2="180" stroke="black" stroke-width="4"/>
                <line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="4"/>
                <line x1="50" y1="60" x2="130" y2="180" stroke="brown" stroke-width="5"/>
                <text x="20" y="120" font-size="14">高?</text>
                <text x="80" y="195" font-size="14">底{a}</text>
                <text x="100" y="110" font-size="14" fill="brown">斜{c}</text>
            ''')
        elif svg_type == "polygon_n":
            n = kwargs.get("n", 5); points = []
            for i in range(n):
                angle = 2 * math.pi * i / n - math.pi / 2
                points.append(f"{150 + 70 * math.cos(angle)},{100 + 70 * math.sin(angle)}")
            return base.format(f'<polygon points="{" ".join(points)}" fill="#f3e5f5" stroke="purple" stroke-width="2"/><text x="130" y="105" fill="purple">正{n}邊形</text>')
        elif svg_type == "diff_squares":
            k = kwargs.get("k", 3)
            return base.format(f'''
                <rect x="80" y="40" width="140" height="140" fill="#e8f5e9" stroke="black"/>
                <rect x="180" y="140" width="40" height="40" fill="white" stroke="red" stroke-dasharray="4"/>
                <text x="130" y="110" font-size="20">x²</text>
                <text x="190" y="165" font-size="12" fill="red">{k}²</text>
            ''')
        elif svg_type == "coord_triangle":
            k = kwargs.get("k", 4)
            return base.format(f'''
                <line x1="20" y1="180" x2="200" y2="180" stroke="black" stroke-width="2"/>
                <line x1="20" y1="20" x2="20" y2="180" stroke="black" stroke-width="2"/>
                <path d="M20,20 L180,180 L20,180 Z" fill="none" stroke="blue"/>
                <text x="10" y="20">A(0,{k})</text>
                <text x="180" y="195">B({k},0)</text>
                <text x="5" y="195">O</text>
            ''')
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
st.title("♾️ 國中數學無限生成引擎 (V20.0 真·全功能融合版)")

if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

units = [
    "3-1 證明與推理", "3-2 三角形的外心", "3-3 三角形的內心", "3-4 三角形的重心",
    "4-1 因式分解法", "4-2 配方法與公式解", "4-3 應用問題"
]
unit = st.sidebar.selectbox("請選擇練習單元", units)

if st.sidebar.button("🚀 生成無限試卷 (全題型+全情境)"):
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
