import streamlit as st
import random
import math
import time

# ==========================================
# 1. 核心：雲端題庫製造機 (V4.0 終極多態版 - 模板最大化)
# ==========================================
@st.cache_data
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
    # 單元 3-1: 證明與推理 (擴充至 12 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50): # 產生 50 題，每次隨機從下列模板抽一種
        t_type = random.randint(1, 12)
        
        if t_type == 1: # 全等性質判斷
            prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
            database["3-1 證明與推理"].append({
                "q": f"已知兩個三角形滿足「{prop}」條件，則它們？",
                "options": ["必全等", "不一定全等", "面積相等但不全等", "相似"],
                "ans": "必全等", 
                "expl": f"{prop} 為三角形全等性質。", "svg": "geometry_sas"
            })
        elif t_type == 2: # 假全等陷阱
            prop = random.choice(["SSA", "AAA"])
            database["3-1 證明與推理"].append({
                "q": f"若兩三角形滿足「{prop}」對應相等，則？",
                "options": ["不一定全等", "必全等", "必不全等", "形狀不同"],
                "ans": "不一定全等", 
                "expl": "SSA 可能形成兩種三角形；AAA 僅能證明相似。", "svg": "none"
            })
        elif t_type == 3: # 中垂線性質
            p_name = random.choice(["P", "Q", "M"])
            database["3-1 證明與推理"].append({
                "q": f"若 {p_name} 點在線段 AB 的垂直平分線上，則下列何者正確？",
                "options": [f"{p_name}A = {p_name}B", f"{p_name}A > {p_name}B", f"{p_name}A ⊥ AB", "無法判斷"],
                "ans": f"{p_name}A = {p_name}B", 
                "expl": "中垂線性值：線上任一點到兩端點等距離。", "svg": "none"
            })
        elif t_type == 4: # 角平分線性質
            database["3-1 證明與推理"].append({
                "q": "若 P 點在 ∠A 的角平分線上，則 P 點到哪裡的距離相等？",
                "options": ["∠A 的兩邊", "∠A 的頂點", "對邊中點", "無法判斷"],
                "ans": "∠A 的兩邊", 
                "expl": "角平分線性值：線上任一點到角兩邊距離相等。", "svg": "none"
            })
        elif t_type == 5: # 大角對大邊
            angles = [random.randint(60, 100), random.randint(40, 59)]
            angles.append(180 - sum(angles))
            mapping = {angles[0]:"BC", angles[1]:"AC", angles[2]:"AB"}
            max_angle = max(angles)
            database["3-1 證明與推理"].append({
                "q": f"△ABC 中，∠A={angles[0]}°, ∠B={angles[1]}°, ∠C={angles[2]}°，求最長邊？",
                "options": [mapping[max_angle], "無法判斷", "三邊等長", "AB"],
                "ans": mapping[max_angle], 
                "expl": "大角對大邊。", "svg": "none"
            })
        elif t_type == 6: # 三角形兩邊之和
            s1, s2 = random.randint(5, 10), random.randint(5, 10)
            database["3-1 證明與推理"].append({
                "q": f"三角形兩邊長為 {s1}, {s2}，第三邊長 x 的範圍？",
                "options": [f"{abs(s1-s2)} < x < {s1+s2}", f"x > {s1+s2}", f"x < {abs(s1-s2)}", f"x = {s1+s2}"],
                "ans": f"{abs(s1-s2)} < x < {s1+s2}", 
                "expl": "兩邊之和大於第三邊，兩邊之差小於第三邊。", "svg": "none"
            })
        elif t_type == 7: # 外角定理
            a, b = random.randint(30, 70), random.randint(30, 70)
            database["3-1 證明與推理"].append({
                "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角？",
                "options": [str(a+b), str(180-a-b), "180", "90"],
                "ans": str(a+b), 
                "expl": "外角等於不相鄰兩內角和。", "svg": "none"
            })
        elif t_type == 8: # 多邊形內角和
            n = random.choice([5, 6, 8, 10, 12])
            database["3-1 證明與推理"].append({
                "q": f"正 {n} 邊形的內角總和？",
                "options": [str((n-2)*180), str(n*180), "360", "720"],
                "ans": str((n-2)*180), 
                "expl": "內角和 = (n-2)×180。", "svg": "none"
            })
        elif t_type == 9: # 多邊形外角和
            n = random.randint(5, 15)
            database["3-1 證明與推理"].append({
                "q": f"{n} 邊形的一組外角和是多少度？",
                "options": ["360", "180", "720", "不一定"],
                "ans": "360", 
                "expl": "任意凸多邊形的外角和皆為 360 度。", "svg": "none"
            })
        elif t_type == 10: # 平行四邊形判別
            database["3-1 證明與推理"].append({
                "q": "下列何者「無法」判別四邊形 ABCD 為平行四邊形？",
                "options": ["一組對邊平行且另一組對邊相等", "兩組對邊分別平行", "兩組對角分別相等", "對角線互相平分"],
                "ans": "一組對邊平行且另一組對邊相等", 
                "expl": "一組平行另一組相等可能是「等腰梯形」。", "svg": "none"
            })
        elif t_type == 11: # 特殊四邊形對角線
            shape = random.choice([("菱形", "互相垂直"), ("矩形", "等長"), ("正方形", "互相垂直且等長")])
            database["3-1 證明與推理"].append({
                "q": f"「{shape[0]}」的對角線具有什麼性質？",
                "options": [shape[1], "無特殊性質", "互相平行", "長度必為整數"],
                "ans": shape[1], 
                "expl": f"{shape[0]}對角線性質：{shape[1]}。", "svg": "none"
            })
        else: # 畢氏定理逆運算 (直角判別)
            sides = random.choice([(3,4,5), (5,12,13), (8,15,17), (7,24,25)])
            database["3-1 證明與推理"].append({
                "q": f"三角形三邊長為 {sides[0]}, {sides[1]}, {sides[2]}，則此三角形為？",
                "options": ["直角三角形", "銳角三角形", "鈍角三角形", "等腰三角形"],
                "ans": "直角三角形", 
                "expl": f"{sides[0]}² + {sides[1]}² = {sides[2]}²，符合畢氏定理。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 3-2: 外心 (擴充至 8 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50):
        t_type = random.randint(1, 8)
        
        if t_type == 1: # 定義
            database["3-2 三角形的外心"].append({
                "q": "三角形的外心是哪三條線的交點？",
                "options": ["中垂線", "角平分線", "中線", "高"],
                "ans": "中垂線", "expl": "外心是三邊垂直平分線交點。", "svg": "none"
            })
        elif t_type == 2: # 距離性質
            database["3-2 三角形的外心"].append({
                "q": "外心到三角形哪裡的距離相等？",
                "options": ["三頂點", "三邊", "三中點", "重心"],
                "ans": "三頂點", "expl": "外心到三頂點距離相等 (外接圓半徑)。", "svg": "triangle_circumcenter"
            })
        elif t_type == 3: # 直角三角形半徑
            c = random.choice([10, 13, 15, 17, 20, 25, 26])
            database["3-2 三角形的外心"].append({
                "q": f"直角三角形斜邊長為 {c}，求外接圓半徑 R？",
                "options": [str(c/2), str(c), str(c*2), str(c/3)],
                "ans": str(c/2), "expl": "直角三角形外接圓半徑 = 斜邊的一半。", "svg": "none"
            })
        elif t_type == 4: # 位置判別
            tri = random.choice([("銳角", "內部"), ("直角", "斜邊中點"), ("鈍角", "外部")])
            database["3-2 三角形的外心"].append({
                "q": f"「{tri[0]}三角形」的外心位於？",
                "options": [tri[1], "頂點上", "重心上", "不一定"],
                "ans": tri[1], "expl": f"{tri[0]}三角形外心在{tri[1]}。", "svg": "none"
            })
        elif t_type == 5: # 角度計算 (圓心角)
            angle_a = random.randint(50, 80)
            database["3-2 三角形的外心"].append({
                "q": f"O 為銳角 △ABC 外心，若 ∠A={angle_a}°，求 ∠BOC？",
                "options": [str(angle_a*2), str(angle_a), str(180-angle_a), str(90+angle_a/2)],
                "ans": str(angle_a*2), "expl": "圓心角 ∠BOC = 2 × 圓周角 ∠A。", "svg": "none"
            })
        elif t_type == 6: # 座標幾何
            k = random.randint(2, 8) * 2
            database["3-2 三角形的外心"].append({
                "q": f"直角坐標上 A(0,{k}), B({k},0), O(0,0)，求 △ABO 外心？",
                "options": [f"({k//2},{k//2})", f"({k},{k})", "(0,0)", f"({k//3},{k//3})"],
                "ans": f"({k//2},{k//2})", "expl": "直角三角形外心為斜邊中點。", "svg": "none"
            })
        elif t_type == 7: # 等腰三角形外心
            database["3-2 三角形的外心"].append({
                "q": "等腰三角形的外心位於哪條線上？",
                "options": ["頂角平分線(底邊中垂線)", "底邊", "腰", "外部"],
                "ans": "頂角平分線(底邊中垂線)", "expl": "等腰三角形具有對稱軸，外心必在對稱軸上。", "svg": "none"
            })
        else: # 外接圓面積
            r = random.randint(3, 10)
            database["3-2 三角形的外心"].append({
                "q": f"若三角形外心到頂點距離為 {r}，求外接圓面積？",
                "options": [f"{r*r}π", f"{2*r}π", f"{r}π", f"{r*r}"],
                "ans": f"{r*r}π", "expl": f"半徑 R={r}，面積 = πR²。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 3-3: 內心 (擴充至 8 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50):
        t_type = random.randint(1, 8)

        if t_type == 1: # 定義
            database["3-3 三角形的內心"].append({
                "q": "三角形的內心是哪三條線的交點？",
                "options": ["角平分線", "中垂線", "中線", "高"],
                "ans": "角平分線", "expl": "內心是三內角平分線交點。", "svg": "none"
            })
        elif t_type == 2: # 距離性質
            database["3-3 三角形的內心"].append({
                "q": "內心到三角形哪裡的距離相等？",
                "options": ["三邊", "三頂點", "三中點", "外部"],
                "ans": "三邊", "expl": "內心到三邊距離相等 (內切圓半徑)。", "svg": "triangle_incenter"
            })
        elif t_type == 3: # 角度公式
            deg = random.choice([40, 50, 60, 70, 80])
            database["3-3 三角形的內心"].append({
                "q": f"I 為內心，∠A={deg}°，求 ∠BIC？",
                "options": [str(90+deg//2), str(180-deg), str(90+deg), str(deg*2)],
                "ans": str(90+deg//2), "expl": "∠BIC = 90° + ∠A/2。", "svg": "triangle_incenter", "svg_params": {"a": deg}
            })
        elif t_type == 4: # 面積公式 A = rs/2
            s = random.randint(10, 30) # 周長
            r = random.randint(2, 5)
            area = s * r // 2
            database["3-3 三角形的內心"].append({
                "q": f"三角形周長 {s}，內切圓半徑 {r}，求面積？",
                "options": [str(area), str(s*r), str(area*2), str(s+r)],
                "ans": str(area), "expl": "面積 = (周長 × 內切圓半徑) ÷ 2。", "svg": "none"
            })
        elif t_type == 5: # 直角三角形內半徑公式
            a, b, c = random.choice([(3,4,5), (5,12,13), (8,15,17)])
            r = (a + b - c) // 2
            database["3-3 三角形的內心"].append({
                "q": f"直角三角形三邊 {a}, {b}, {c}，求內切圓半徑？",
                "options": [str(r), str(r+1), str(a+b), str(c/2)],
                "ans": str(r), "expl": "直角三角形內半徑 r = (兩股和 - 斜邊) / 2。", "svg": "none"
            })
        elif t_type == 6: # 面積比
            database["3-3 三角形的內心"].append({
                "q": "若 I 為 △ABC 內心，則 △IAB, △IBC, △ICA 的面積比等於？",
                "options": ["三邊長比 (AB:BC:CA)", "1:1:1", "高的比", "無法判斷"],
                "ans": "三邊長比 (AB:BC:CA)", "expl": "因為高相等(皆為半徑)，面積比 = 底邊比。", "svg": "none"
            })
        elif t_type == 7: # 正三角形特殊性
            database["3-3 三角形的內心"].append({
                "q": "正三角形的內心、外心、重心有何關係？",
                "options": ["三心重合", "不重合", "只有內外心重合", "只有重外心重合"],
                "ans": "三心重合", "expl": "正多邊形的內心、外心、重心皆在同一點。", "svg": "none"
            })
        else: # 內心作圖
            database["3-3 三角形的內心"].append({
                "q": "尺規作圖找內心，需要做什麼？",
                "options": ["做兩內角的角平分線", "做兩邊的中垂線", "做兩邊的中線", "做兩邊的高"],
                "ans": "做兩內角的角平分線", "expl": "內心為角平分線交點。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 3-4: 重心 (擴充至 8 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50):
        t_type = random.randint(1, 8)

        if t_type == 1: # 定義
            database["3-4 三角形的重心"].append({
                "q": "三角形的重心是哪三條線的交點？",
                "options": ["中線", "中垂線", "角平分線", "高"],
                "ans": "中線", "expl": "重心是三邊中線交點。", "svg": "none"
            })
        elif t_type == 2: # 長度比 2:1
            m = random.randint(3, 12) * 3
            database["3-4 三角形的重心"].append({
                "q": f"G 為重心，中線 AD 長為 {m}，求 AG？",
                "options": [str(m*2//3), str(m//3), str(m), str(m//2)],
                "ans": str(m*2//3), "expl": "重心到頂點距離 = 2/3 中線長。", "svg": "triangle_centroid", "svg_params": {"m": m}
            })
        elif t_type == 3: # 長度比 1:2 (反向)
            gd = random.randint(2, 8)
            database["3-4 三角形的重心"].append({
                "q": f"G 為重心，D 為 BC 中點。若 GD={gd}，求 AG？",
                "options": [str(gd*2), str(gd), str(gd*3), str(gd/2)],
                "ans": str(gd*2), "expl": "AG = 2 × GD。", "svg": "none"
            })
        elif t_type == 4: # 面積 3 等分
            area = random.randint(4, 12) * 3
            database["3-4 三角形的重心"].append({
                "q": f"△ABC 面積 {area}，G 為重心，求 △GAB 面積？",
                "options": [str(area//3), str(area//2), str(area//6), str(area)],
                "ans": str(area//3), "expl": "重心與三頂點連線將面積三等分。", "svg": "none"
            })
        elif t_type == 5: # 面積 6 等分
            area = random.randint(4, 12) * 6
            database["3-4 三角形的重心"].append({
                "q": f"△ABC 面積 {area}，三中線將其分割為 6 個小三角形，每個面積為？",
                "options": [str(area//6), str(area//3), str(area//2), str(area)],
                "ans": str(area//6), "expl": "三中線將三角形分割為 6 個等積小三角形。", "svg": "none"
            })
        elif t_type == 6: # 坐標公式
            x1, x2, x3 = random.sample(range(0, 12), 3)
            gx = round((x1+x2+x3)/3, 1)
            # 簡化為整數題型
            if (x1+x2+x3)%3 == 0:
                gx = (x1+x2+x3)//3
                database["3-4 三角形的重心"].append({
                    "q": f"三頂點 x 座標分別為 {x1}, {x2}, {x3}，求重心 x 座標？",
                    "options": [str(gx), str(x1+x2+x3), str(gx*2), "0"],
                    "ans": str(gx), "expl": "重心座標為三頂點座標平均。", "svg": "none"
                })
            else:
                database["3-4 三角形的重心"].append({
                    "q": "重心的座標如何計算？",
                    "options": ["三頂點座標相加除以 3", "三頂點座標相加除以 2", "三邊中點相加", "無法計算"],
                    "ans": "三頂點座標相加除以 3", "expl": "重心是頂點的算術平均數。", "svg": "none"
                })
        elif t_type == 7: # 直角三角形重心
            database["3-4 三角形的重心"].append({
                "q": "直角三角形重心到斜邊中點的距離，是斜邊長度的幾倍？",
                "options": ["1/6", "1/3", "1/2", "2/3"],
                "ans": "1/6", 
                "expl": "斜邊中線長=1/2斜邊。重心到中點佔中線1/3。故 (1/2)*(1/3) = 1/6。", "svg": "none"
            })
        else: # 物理性質
            database["3-4 三角形的重心"].append({
                "q": "若將均勻三角形板子頂在「重心」處，板子會？",
                "options": ["保持平衡", "向一邊傾倒", "旋轉", "斷裂"],
                "ans": "保持平衡", "expl": "重心是物體重量的中心。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 4-1: 因式分解 (擴充至 8 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50):
        t_type = random.randint(1, 8)

        if t_type == 1: # 提公因式
            k = random.randint(2, 9)
            database["4-1 因式分解法"].append({
                "q": f"因式分解 x² + {k}x？",
                "options": [f"x(x+{k})", f"x(x-{k})", f"(x+{k})²", f"x²"],
                "ans": f"x(x+{k})", "expl": "提公因式 x。", "svg": "roots_0_k", "svg_params": {"k_label": "k", "k": -k}
            })
        elif t_type == 2: # 平方差
            k = random.randint(2, 9)
            database["4-1 因式分解法"].append({
                "q": f"因式分解 x² - {k*k}？",
                "options": [f"(x+{k})(x-{k})", f"(x-{k})²", f"(x+{k})²", "無法分解"],
                "ans": f"(x+{k})(x-{k})", "expl": "平方差公式 a²-b²=(a+b)(a-b)。", "svg": "none"
            })
        elif t_type == 3: # 和的平方
            k = random.randint(2, 9)
            database["4-1 因式分解法"].append({
                "q": f"因式分解 x² + {2*k}x + {k*k}？",
                "options": [f"(x+{k})²", f"(x-{k})²", f"(x+{k})(x-{k})", f"x(x+{2*k})"],
                "ans": f"(x+{k})²", "expl": "完全平方式 (a+b)² = a²+2ab+b²。", "svg": "none"
            })
        elif t_type == 4: # 差的平方
            k = random.randint(2, 9)
            database["4-1 因式分解法"].append({
                "q": f"因式分解 x² - {2*k}x + {k*k}？",
                "options": [f"(x-{k})²", f"(x+{k})²", f"(x+{k})(x-{k})", f"x(x-{2*k})"],
                "ans": f"(x-{k})²", "expl": "完全平方式 (a-b)² = a²-2ab+b²。", "svg": "none"
            })
        elif t_type == 5: # 十字交乘 (兩根為正)
            a, b = random.randint(1, 4), random.randint(1, 4)
            database["4-1 因式分解法"].append({
                "q": f"方程式 x² - {a+b}x + {a*b} = 0 的解？",
                "options": [f"{a}, {b}", f"{-a}, {-b}", f"{a}, {-b}", "無解"],
                "ans": f"{a}, {b}", "expl": f"(x-{a})(x-{b})=0，故 x={a} 或 {b}。", "svg": "none"
            })
        elif t_type == 6: # 十字交乘 (一正一負)
            a, b = random.randint(1, 5), random.randint(1, 5)
            # (x-a)(x+b) = x^2 + (b-a)x - ab
            database["4-1 因式分解法"].append({
                "q": f"方程式 x² + {b-a}x - {a*b} = 0 的解？",
                "options": [f"{a}, {-b}", f"{-a}, {b}", f"{a}, {b}", "無解"],
                "ans": f"{a}, {-b}", "expl": f"(x-{a})(x+{b})=0，故 x={a} 或 {-b}。", "svg": "none"
            })
        elif t_type == 7: # 根的定義
            k = random.randint(1, 5)
            database["4-1 因式分解法"].append({
                "q": f"若 {k} 是方程式 x² + ax + 5 = 0 的一根，則？",
                "options": [f"將 x={k} 代入等號成立", f"將 x=-{k} 代入等號成立", "a=0", "無法判斷"],
                "ans": f"將 x={k} 代入等號成立", "expl": "根的定義即為代入後方程式成立。", "svg": "none"
            })
        else: # 零積性質
            database["4-1 因式分解法"].append({
                "q": "若 (x-A)(x-B) = 0，則 x 的值？",
                "options": ["A 或 B", "A 且 B", "A+B", "A-B"],
                "ans": "A 或 B", "expl": "兩數相乘為 0，則其中一數必為 0。", "svg": "roots_line_hidden"
            })

    # ---------------------------------------------------------
    # 單元 4-2: 配方法 (擴充至 8 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50):
        t_type = random.randint(1, 8)

        if t_type == 1: # 配方補項
            k = random.choice([4, 6, 8, 10, 12])
            database["4-2 配方法與公式解"].append({
                "q": f"x² + {k}x + □ 成為完全平方式，□ = ？",
                "options": [str((k//2)**2), str(k), str(k*2), str(k**2)],
                "ans": str((k//2)**2), "expl": "補項 = (一次項係數一半)的平方。", "svg": "area_square_k"
            })
        elif t_type == 2: # 判別式 D 計算
            b, c = random.randint(2, 5), random.randint(1, 3)
            # x^2 + bx + c
            d = b*b - 4*c
            database["4-2 配方法與公式解"].append({
                "q": f"x² + {b}x + {c} = 0 的判別式 D = ？",
                "options": [str(d), str(b*b+4*c), str(b*b), "0"],
                "ans": str(d), "expl": "D = b² - 4ac。", "svg": "none"
            })
        elif t_type == 3: # 判別式性質 (兩相異實根)
            database["4-2 配方法與公式解"].append({
                "q": "若判別式 D > 0，則方程式有？",
                "options": ["兩相異實根", "重根", "無實根", "三個根"],
                "ans": "兩相異實根", "expl": "D > 0 表兩相異實根。", "svg": "none"
            })
        elif t_type == 4: # 判別式性質 (重根)
            database["4-2 配方法與公式解"].append({
                "q": "若方程式有重根，則判別式 D？",
                "options": ["D = 0", "D > 0", "D < 0", "D = 1"],
                "ans": "D = 0", "expl": "重根時，頂點在 x 軸上，D = 0。", "svg": "none"
            })
        elif t_type == 5: # 判別式性質 (無解)
            database["4-2 配方法與公式解"].append({
                "q": "若方程式無實根，則判別式 D？",
                "options": ["D < 0", "D > 0", "D = 0", "D >= 0"],
                "ans": "D < 0", "expl": "D < 0 表圖形與 x 軸無交點。", "svg": "none"
            })
        elif t_type == 6: # 公式解形式
            database["4-2 配方法與公式解"].append({
                "q": "一元二次方程式的公式解 x = ？",
                "options": ["(-b ± √D) / 2a", "(b ± √D) / 2a", "(-b ± D) / 2a", "-b / 2a"],
                "ans": "(-b ± √D) / 2a", "expl": "公式解定義。", "svg": "none"
            })
        elif t_type == 7: # 頂點形式
            h, k = random.randint(1, 5), random.randint(1, 5)
            database["4-2 配方法與公式解"].append({
                "q": f"方程式 (x-{h})² = {k} 的解？",
                "options": [f"{h} ± √{k}", f"{-h} ± √{k}", f"{h} ± {k}", "無解"],
                "ans": f"{h} ± √{k}", "expl": "開根號後移項：x - h = ±√k => x = h ± √k。", "svg": "none"
            })
        else: # 係數影響
            database["4-2 配方法與公式解"].append({
                "q": "方程式 ax² + bx + c = 0 中，若 a > 0，則拋物線開口？",
                "options": ["向上", "向下", "向左", "向右"],
                "ans": "向上", "expl": "二次項係數為正，開口向上。", "svg": "none"
            })

    # ---------------------------------------------------------
    # 單元 4-3: 應用問題 (擴充至 8 種邏輯模板)
    # ---------------------------------------------------------
    for _ in range(50):
        t_type = random.randint(1, 8)

        if t_type == 1: # 正方形面積
            s = random.randint(5, 15)
            database["4-3 應用問題"].append({
                "q": f"正方形面積為 {s*s}，求邊長？",
                "options": [str(s), str(s*2), str(s*s), str(s+4)],
                "ans": str(s), "expl": "邊長 = √面積。", "svg": "area_square"
            })
        elif t_type == 2: # 長方形周長反推
            x = random.randint(3, 10) # 寬
            # 長 = x+2, 面積 = x(x+2)
            area = x*(x+2)
            database["4-3 應用問題"].append({
                "q": f"長方形長比寬多 2，面積為 {area}，求寬？",
                "options": [str(x), str(x+2), str(area), str(2*x)],
                "ans": str(x), "expl": "設寬 x，x(x+2)=面積，解 x。", "svg": "area_square"
            })
        elif t_type == 3: # 連續整數
            n = random.randint(1, 10)
            prod = n*(n+1)
            database["4-3 應用問題"].append({
                "q": f"兩連續正整數積為 {prod}，求兩數和？",
                "options": [str(2*n+1), str(n), str(n+1), str(prod)],
                "ans": str(2*n+1), "expl": f"數為 {n}, {n+1}，和為 {2*n+1}。", "svg": "none"
            })
        elif t_type == 4: # 物理拋體
            t = random.randint(2, 6)
            h = 5*t*t
            database["4-3 應用問題"].append({
                "q": f"物體落下距離 h=5t²。若落下 {h} 公尺，需時多久？",
                "options": [str(t), str(t*2), str(t*5), "10"],
                "ans": str(t), "expl": f"5t²={h} => t²={t*t} => t={t}。", "svg": "none"
            })
        elif t_type == 5: # 梯形面積
            # (上底+下底)*高/2. 設上底 x, 下底 x+2, 高 4
            x = random.randint(3, 8)
            area = (2*x + 2) * 2 # (x + x+2)*4/2 = (2x+2)*2
            database["4-3 應用問題"].append({
                "q": f"梯形高為 4，下底比上底多 2，面積 {area}，求上底？",
                "options": [str(x), str(x+2), str(area), "4"],
                "ans": str(x), "expl": "代入梯形面積公式逆算。", "svg": "none"
            })
        elif t_type == 6: # 邏輯判斷 (負不合)
            database["4-3 應用問題"].append({
                "q": "計算長方形邊長時算出 x = 5 或 -3，應取？",
                "options": ["5", "-3", "兩者皆可", "無解"],
                "ans": "5", "expl": "邊長長度必須為正數，負數不合。", "svg": "none"
            })
        elif t_type == 7: # 數字問題 (倒數)
            # 某數 + 倒數 = 2.5 (2 + 1/2)
            database["4-3 應用問題"].append({
                "q": "某數與其倒數之和為 2.5，求此數 (整數解)？",
                "options": ["2", "0.5", "1", "3"],
                "ans": "2", "expl": "x + 1/x = 2.5 => 2x² - 5x + 2 = 0 => x=2 或 1/2。", "svg": "none"
            })
        else: # 畢氏定理應用
            # 直角三角形一股 3, 斜邊 5, 求另一股
            tri = random.choice([(3,4,5), (5,12,13), (6,8,10)])
            database["4-3 應用問題"].append({
                "q": f"梯子長 {tri[2]} 公尺，靠在牆上，梯腳離牆 {tri[0]} 公尺，求梯頂高度？",
                "options": [str(tri[1]), str(tri[2]), str(tri[0]+tri[2]), str(tri[2]-tri[0])],
                "ans": str(tri[1]), "expl": "畢氏定理：c² - a² = b²。", "svg": "none"
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
st.title("☁️ 國中數學智能題庫 (V4.0 終極多態版)")

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
