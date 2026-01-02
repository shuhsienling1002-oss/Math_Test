import json
import random

# ==========================================
# 題庫製造工廠 (V9.0 - 題型標籤完整版)
# ==========================================
# 特點：生產時會加入 "type_id"，讓 APP 知道這是哪一種題目。

def create_dataset():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心": [],
        "3-3 三角形的內心": [],
        "3-4 三角形的重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    seen_questions = set()
    print("🚀 V9.0 工廠啟動：正在生產並標記題型 ID...")

    def add_q(unit, q_obj):
        unique_id = f"{unit}_{q_obj['q']}"
        if unique_id in seen_questions: return False
        seen_questions.add(unique_id)
        random.shuffle(q_obj['options'])
        database[unit].append(q_obj)
        return True

    # ==========================================
    # 單元 3-1: 證明與推理
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 6)
        q_data = None
        
        if q_type == 1: # 外角定理
            a, b = random.randint(20, 90), random.randint(20, 80)
            ans = a + b
            if ans < 180:
                q_data = {
                    "type_id": 1,
                    "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
                    "options": [str(ans), str(180-ans), str(180-a), str(90+b)], "ans": str(ans),
                    "expl": f"外角 = 遠內角和 ({a}+{b})。", "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}
                }
        elif q_type == 2: # 邊角關係
            sides = sorted(random.sample(range(5, 30), 3))
            if sides[0] + sides[1] > sides[2]:
                a, b, c = sides[0], sides[1], sides[2]
                labels = ["AB", "BC", "AC"]; random.shuffle(labels)
                s_dict = {labels[0]: a, labels[1]: b, labels[2]: c}
                max_val = max(a, b, c)
                max_name = [k for k, v in s_dict.items() if v == max_val][0]
                ans_map = {"AB": "∠C", "BC": "∠A", "AC": "∠B"}
                q_data = {
                    "type_id": 2,
                    "q": f"△ABC 中，{labels[0]}={s_dict[labels[0]]}, {labels[1]}={s_dict[labels[1]]}, {labels[2]}={s_dict[labels[2]]}，哪個角最大？",
                    "options": ["∠A", "∠B", "∠C", "無法判斷"], "ans": ans_map[max_name],
                    "expl": "大邊對大角。", "svg": "none", "params": {}
                }
        elif q_type == 3: # 多邊形內角和
            n = random.choice([5,6,7,8,9,10,12])
            ans = (n-2)*180
            q_data = {
                "type_id": 3,
                "q": f"正 {n} 邊形的內角總和是多少度？",
                "options": [str(ans), str(n*180), "360", "720"], "ans": str(ans),
                "expl": f"(n-2)×180。", "svg": "polygon_n", "params": {"n": n}
            }
        elif q_type == 4: # 幾何性質判斷
            pair = random.choice([("SAS", "必全等"), ("ASA", "必全等"), ("SSS", "必全等"), ("RHS", "必全等"), ("AAA", "不一定全等")])
            q_data = {
                "type_id": 4,
                "q": f"若兩個三角形滿足「{pair[0]}」對應相等，則它們？",
                "options": ["必全等", "不一定全等", "一定不全等", "面積不同"], "ans": pair[1],
                "expl": f"{pair[0]} 性質判定。", "svg": "geometry_sas", "params": {}
            }
        elif q_type == 5: # 平行線
            ang = random.randint(50, 130)
            q_data = {
                "type_id": 5,
                "q": f"兩平行線被一直線所截，若同位角為 {ang}°，則同側內角為？",
                "options": [str(180-ang), str(ang), "90", "無法計算"], "ans": str(180-ang),
                "expl": "同側內角互補 (相加180)。", "svg": "none", "params": {}
            }
        elif q_type == 6: # 等腰三角形
            top = random.choice([30, 40, 50, 60, 70, 80, 100])
            base = (180 - top) // 2
            q_data = {
                "type_id": 6,
                "q": f"等腰三角形頂角為 {top}°，求底角？",
                "options": [str(base), str(top), str(180-top), str(90-top)], "ans": str(base),
                "expl": "(180-頂角)/2。", "svg": "general_triangle", "params": {"angle_a": top, "angle_b": base}
            }

        if q_data: add_q("3-1 證明與推理", q_data)

    # ==========================================
    # 單元 3-2: 外心
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 5)
        q_data = None
        if q_type == 1: # 直角外接圓
            c = random.randint(5, 40) * 2; r = c // 2
            q_data = {"type_id": 1, "q": f"直角三角形斜邊長為 {c}，求外接圓半徑？", "options": [str(r), str(c), str(c*2)], "ans": str(r), "expl": "斜邊一半", "svg": "right_triangle_circumcenter", "params": {}}
        elif q_type == 2: # 角度 BOC
            a = random.randint(50, 80); ans = 2*a
            q_data = {"type_id": 2, "q": f"O 為銳角 △ABC 外心，若 ∠A={a}°，求 ∠BOC？", "options": [str(ans), str(a), str(180-a)], "ans": str(ans), "expl": "2倍圓周角", "svg": "triangle_circumcenter", "params": {}}
        elif q_type == 3: # 位置
            q_data = {"type_id": 3, "q": "鈍角三角形外心位置在哪裡？", "options": ["三角形外部", "三角形內部", "斜邊上"], "ans": "三角形外部", "expl": "性質", "svg": "none", "params": {}}
        elif q_type == 4: # 坐標
            k = random.randint(2,10)*2
            q_data = {"type_id": 4, "q": f"直角座標上 A(0,{k}), B({k},0), O(0,0)，求 △ABO 外心？", "options": [f"({k//2},{k//2})", "(0,0)", f"({k},{k})"], "ans": f"({k//2},{k//2})", "expl": "斜邊中點", "svg": "none", "params": {}}
        elif q_type == 5: # 距離
            d = random.randint(5,20)
            q_data = {"type_id": 5, "q": f"O 為外心，若 OA={d}，則 OB+OC=？", "options": [str(d*2), str(d)], "ans": str(d*2), "expl": "外心到頂點等距", "svg": "triangle_circumcenter", "params": {}}
        if q_data: add_q("3-2 三角形的外心", q_data)

    # ==========================================
    # 單元 3-3: 內心
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        if q_type == 1: # 角度 BIC
            a = random.randint(30,90); ans = 90 + a//2
            q_data = {"type_id": 1, "q": f"I 為內心，若 ∠A={a}°，求 ∠BIC？", "options": [str(ans), str(90+a), str(180-a)], "ans": str(ans), "expl": "90+A/2", "svg": "triangle_incenter_angle", "params": {"a":a}}
        elif q_type == 2: # 面積求r
            s=random.randint(10,30); r=random.randint(2,5); area=s*r//2
            q_data = {"type_id": 2, "q": f"三角形周長 {s}，面積 {area}，求內切圓半徑？", "options": [str(r), str(s), str(area//s)], "ans": str(r), "expl": "rs/2", "svg": "triangle_incenter_concept", "params": {}}
        elif q_type == 3: # 直角 r
            k=random.randint(1,5); a,b,c=3*k,4*k,5*k; r=(a+b-c)//2
            q_data = {"type_id": 3, "q": f"直角三角形三邊 {a}, {b}, {c}，求內切圓半徑？", "options": [str(r), str(c)], "ans": str(r), "expl": "(兩股和-斜邊)/2", "svg": "right_triangle_incenter", "params": {"a":a,"b":b,"c":c}}
        elif q_type == 4: # 定義
            q_data = {"type_id": 4, "q": "內心是哪三條線的交點？", "options": ["角平分線", "中線", "中垂線"], "ans": "角平分線", "expl": "定義", "svg": "none", "params": {}}
        if q_data: add_q("3-3 三角形的內心", q_data)

    # ==========================================
    # 單元 3-4: 重心
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        if q_type == 1: # 長度
            m=random.randint(3,20)*3; ag=m*2//3
            q_data = {"type_id": 1, "q": f"G 為重心，中線 AD={m}，求 AG？", "options": [str(ag), str(m), str(m//3)], "ans": str(ag), "expl": "2/3 中線", "svg": "triangle_centroid", "params": {"m":m}}
        elif q_type == 2: # 面積
            area=random.randint(6,40)*6; sub=area//6
            q_data = {"type_id": 2, "q": f"△ABC 總面積 {area}，G 為重心，求 △GAB 面積？", "options": [str(sub*2), str(area), str(sub)], "ans": str(sub*2), "expl": "佔 1/3", "svg": "triangle_centroid", "params": {"m":"?"}}
        elif q_type == 3: # 定義
            q_data = {"type_id": 3, "q": "重心是哪三條線的交點？", "options": ["中線", "高", "中垂線"], "ans": "中線", "expl": "定義", "svg": "none", "params": {}}
        elif q_type == 4: # 座標
            x=random.randint(1,5)*3
            q_data = {"type_id": 4, "q": f"A(0,0), B({x},0), C(0,{x})，求重心座標？", "options": [f"({x//3},{x//3})", "(0,0)"], "ans": f"({x//3},{x//3})", "expl": "三點平均", "svg": "none", "params": {}}
        if q_data: add_q("3-4 三角形的重心", q_data)

    # ==========================================
    # 單元 4-1: 因式分解
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        if q_type == 1: # 提公因式
            k=random.randint(2,9)
            q_data = {"type_id": 1, "q": f"解方程式 x² - {k}x = 0？", "options": [f"0, {k}", f"{k}"], "ans": f"0, {k}", "expl": "x(x-k)=0", "svg": "none", "params": {}}
        elif q_type == 2: # 平方差
            k=random.randint(2,9); k2=k*k
            q_data = {"type_id": 2, "q": f"解方程式 x² - {k2} = 0？", "options": [f"±{k}", f"{k2}"], "ans": f"±{k}", "expl": "x=±k", "svg": "diff_squares", "params": {"k":k}}
        elif q_type == 3: # 十字交乘
            r1,r2 = random.randint(1,6), random.randint(1,6); b=r1+r2; c=r1*r2
            q_data = {"type_id": 3, "q": f"因式分解 x² - {b}x + {c}？", "options": [f"(x-{r1})(x-{r2})", f"(x+{r1})(x+{r2})"], "ans": f"(x-{r1})(x-{r2})", "expl": "十字交乘", "svg": "none", "params": {}}
        elif q_type == 4: # 完全平方
            k=random.randint(1,9); b=2*k; c=k*k
            q_data = {"type_id": 4, "q": f"因式分解 x² + {b}x + {c}？", "options": [f"(x+{k})²", f"(x-{k})²"], "ans": f"(x+{k})²", "expl": "和的平方", "svg": "area_square_k", "params": {"k":b}}
        if q_data: add_q("4-1 因式分解法", q_data)

    # ==========================================
    # 單元 4-2: 配方法
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        if q_type == 1: # 判別式
            b=random.choice([2,4,6]); c=random.randint(1,5); d=b*b-4*c
            q_data = {"type_id": 1, "q": f"x² + {b}x + {c} = 0 的判別式 D？", "options": [str(d), str(d+1)], "ans": str(d), "expl": "b²-4ac", "svg": "none", "params": {}}
        elif q_type == 2: # 補項
            k=random.randint(2,10)*2; ans=(k//2)**2
            q_data = {"type_id": 2, "q": f"x² + {k}x 配方需加上？", "options": [str(ans), str(k)], "ans": str(ans), "expl": "一半平方", "svg": "area_square_k", "params": {"k":k}}
        elif q_type == 3: # 兩根和
            b=random.randint(2,9)
            q_data = {"type_id": 3, "q": f"x² + {b}x + 1 = 0 兩根和？", "options": [str(-b), str(b)], "ans": str(-b), "expl": "-b/a", "svg": "none", "params": {}}
        elif q_type == 4: # 性質
            pair = random.choice([("D>0", "兩相異實根"), ("D=0", "重根")])
            q_data = {"type_id": 4, "q": f"若 {pair[0]}，根的性質？", "options": [pair[1], "無實根"], "ans": pair[1], "expl": "性質", "svg": "none", "params": {}}
        if q_data: add_q("4-2 配方法與公式解", q_data)

    # ==========================================
    # 單元 4-3: 應用問題
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        if q_type == 1: # 正方形
            s=random.randint(5,20); area=s*s
            q_data = {"type_id": 1, "q": f"正方形面積 {area}，求邊長？", "options": [str(s), str(area)], "ans": str(s), "expl": "開根號", "svg": "area_square", "params": {"s":s}}
        elif q_type == 2: # 兩數積
            n=random.randint(2,9); val=n*(n+1)
            q_data = {"type_id": 2, "q": f"兩連續正整數積 {val}，求較小數？", "options": [str(n), str(n+1)], "ans": str(n), "expl": "x(x+1)", "svg": "none", "params": {}}
        elif q_type == 3: # 梯子
            k=random.randint(2,5); a,b,c=3*k,4*k,5*k
            q_data = {"type_id": 3, "q": f"梯長 {c}，腳離牆 {a}，梯頂高？", "options": [str(b), str(c)], "ans": str(b), "expl": "畢氏定理", "svg": "ladder_wall", "params": {"a":a,"b":b,"c":c}}
        elif q_type == 4: # 落體
            t=random.randint(2,5); h=5*t*t
            q_data = {"type_id": 4, "q": f"h=5t²，落下 {h} 公尺需幾秒？", "options": [str(t), str(t*2)], "ans": str(t), "expl": "代入", "svg": "none", "params": {}}
        if q_data: add_q("4-3 應用問題", q_data)

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*40)
    print(f"✅ V9.0 題型標籤版 - 更新成功！")
    print(f"💰 實際產出題數：{sum(len(v) for v in database.values())}")
    print("="*40 + "\n")

if __name__ == "__main__":
    create_dataset()