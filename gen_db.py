import json
import random

# ==========================================
# 題庫製造工廠 (V8.0 - 智慧去重終極版)
# ==========================================
# 特點：內建防重複機制，確保題庫內每一題都是唯一的。

def create_dataset():
    # 初始化題庫結構
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心": [],
        "3-3 三角形的內心": [],
        "3-4 三角形的重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # 用來記錄已生成的題目，防止重複 (格式: "單元名_題目文字")
    seen_questions = set()

    print("🚀 V8.0 工廠啟動：正在執行「去重過濾」生產程序...")

    # 定義一個內部函數來安全地加入題目
    def add_q(unit, q_obj):
        # 建立唯一識別碼 (Unit + Question Text)
        unique_id = f"{unit}_{q_obj['q']}"
        
        # 檢查是否重複
        if unique_id in seen_questions:
            return False # 重複了，跳過
        
        # 沒重複，加入資料庫與記錄
        seen_questions.add(unique_id)
        # 隨機打亂選項後再加入
        random.shuffle(q_obj['options'])
        database[unit].append(q_obj)
        return True

    # ==========================================
    # 單元 3-1: 證明與推理 (目標: 生產 100+ 題不重複)
    # ==========================================
    # 嘗試跑 300 次迴圈，利用去重機制篩選出獨特題目
    count = 0
    for _ in range(300):
        q_type = random.randint(1, 10)
        q_data = None
        
        if q_type == 1: # 外角定理 (數字變動)
            a, b = random.randint(20, 90), random.randint(20, 80)
            ans = a + b
            if ans < 180:
                q_data = {
                    "q": f"△ABC 中，∠A={a}°，∠B={b}°，則 ∠C 的外角是多少度？",
                    "options": [str(ans), str(180-ans), str(180-a), str(90+b)], "ans": str(ans),
                    "expl": f"外角 = 遠內角和 ({a}+{b})。", "svg": "general_triangle", "params": {"angle_a": a, "angle_b": b}
                }

        elif q_type == 2: # 邊角關係 (數字變動)
            # 生成一組三角形邊長
            sides = sorted(random.sample(range(5, 30), 3))
            if sides[0] + sides[1] > sides[2]: # 確保構成三角形
                a, b, c = sides[0], sides[1], sides[2]
                # 隨機分配給 AB, BC, AC
                labels = ["AB", "BC", "AC"]; random.shuffle(labels)
                s_dict = {labels[0]: a, labels[1]: b, labels[2]: c}
                # 找最大邊對最大角
                # 邏輯: 邊長最大者，其對角最大。 AB對C, BC對A, AC對B
                max_side_val = max(a, b, c)
                max_side_name = [k for k, v in s_dict.items() if v == max_side_val][0]
                ans_map = {"AB": "∠C", "BC": "∠A", "AC": "∠B"}
                ans = ans_map[max_side_name]
                
                q_data = {
                    "q": f"△ABC 中，{labels[0]}={s_dict[labels[0]]}, {labels[1]}={s_dict[labels[1]]}, {labels[2]}={s_dict[labels[2]]}，哪個角最大？",
                    "options": ["∠A", "∠B", "∠C", "無法判斷"], "ans": ans,
                    "expl": "大邊對大角。", "svg": "none", "params": {}
                }

        elif q_type == 3: # 多邊形內角和 (有限變化，只會加入一次)
            n = random.choice([5,6,7,8,9,10,12])
            ans = (n-2)*180
            q_data = {
                "q": f"正 {n} 邊形的內角總和是多少度？",
                "options": [str(ans), str(n*180), "360", "720"], "ans": str(ans),
                "expl": f"(n-2)×180。", "svg": "polygon_n", "params": {"n": n}
            }

        elif q_type == 4: # 幾何性質判斷 (有限變化)
            pair = random.choice([
                ("SAS", "必全等"), ("ASA", "必全等"), ("SSS", "必全等"), ("RHS", "必全等"),
                ("AAA", "不一定全等"), ("SSA", "不一定全等")
            ])
            q_data = {
                "q": f"若兩個三角形滿足「{pair[0]}」對應相等，則它們？",
                "options": ["必全等", "不一定全等", "一定不全等", "面積不同"], "ans": pair[1],
                "expl": f"{pair[0]} 性質判定。", "svg": "none", "params": {}
            }
            
        elif q_type == 5: # 平行線 (數字變動)
            ang = random.randint(50, 130)
            q_data = {
                "q": f"兩平行線被一直線所截，若同位角為 {ang}°，則同側內角為？",
                "options": [str(180-ang), str(ang), "90", "無法計算"], "ans": str(180-ang),
                "expl": "同側內角互補 (相加180)。", "svg": "none", "params": {}
            }

        elif q_type == 6: # 等腰三角形 (數字變動)
            top = random.choice([30, 40, 50, 60, 70, 80, 100])
            base = (180 - top) // 2
            q_data = {
                "q": f"等腰三角形頂角為 {top}°，求底角？",
                "options": [str(base), str(top), str(180-top), str(90-top)], "ans": str(base),
                "expl": "(180-頂角)/2。", "svg": "general_triangle", "params": {"angle_a": top, "angle_b": base}
            }

        # 加入檢查
        if q_data: add_q("3-1 證明與推理", q_data)


    # ==========================================
    # 單元 3-2: 外心 (目標: 100+ 題)
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 6)
        q_data = None
        
        if q_type == 1: # 直角外接圓 (數字變動)
            c = random.randint(5, 40) * 2
            r = c // 2
            q_data = {
                "q": f"直角三角形斜邊長為 {c}，求外接圓半徑？", 
                "options": [str(r), str(c), str(c*2), str(r+5)], "ans": str(r),
                "expl": "斜邊一半。", "svg": "right_triangle_circumcenter", "params": {}
            }
            
        elif q_type == 2: # 角度 BOC (數字變動)
            a = random.randint(50, 80)
            ans = 2 * a
            q_data = {
                "q": f"O 為銳角 △ABC 外心，∠A={a}°，求 ∠BOC？", 
                "options": [str(ans), str(a), str(180-a), str(90+a)], "ans": str(ans),
                "expl": "圓心角是圓周角的兩倍。", "svg": "triangle_circumcenter", "params": {}
            }

        elif q_type == 3: # 位置判斷 (有限變化)
            t_data = random.choice([("鈍角", "外部"), ("銳角", "內部"), ("直角", "斜邊中點")])
            q_data = {
                "q": f"{t_data[0]}三角形的外心位於？", 
                "options": [t_data[1], "頂點", "重心", "不一定"], "ans": t_data[1],
                "expl": "外心位置性質。", "svg": "none", "params": {}
            }

        elif q_type == 4: # 坐標 (數字變動)
            k = random.randint(2, 10) * 2
            q_data = {
                "q": f"直角座標平面上，A(0,{k}), B({k},0), O(0,0)，求 △ABO 的外心？", 
                "options": [f"({k//2},{k//2})", f"({k},{k})", "(0,0)", f"({k//2},0)"], "ans": f"({k//2},{k//2})",
                "expl": "直角三角形外心為斜邊中點。", "svg": "none", "params": {}
            }
        
        elif q_type == 5: # 距離 (數字變動)
            d = random.randint(5, 20)
            q_data = {
                "q": f"O 為 △ABC 外心，若 OA = {d}，則 OB + OC = ？", 
                "options": [str(d*2), str(d), str(d*3), "無法計算"], "ans": str(d*2),
                "expl": "外心到三頂點等距 (OA=OB=OC)。", "svg": "triangle_circumcenter", "params": {}
            }

        if q_data: add_q("3-2 三角形的外心", q_data)


    # ==========================================
    # 單元 3-3: 內心
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 5)
        q_data = None
        
        if q_type == 1: # 角度 BIC (數字變動)
            a = random.randint(30, 90)
            ans = 90 + a // 2
            q_data = {
                "q": f"I 為內心，∠A={a}°，求 ∠BIC？", 
                "options": [str(ans), str(180-a), str(90+a), str(ans+10)], "ans": str(ans),
                "expl": "90 + A/2。", "svg": "triangle_incenter_angle", "params": {"a": a}
            }
            
        elif q_type == 2: # 面積求半徑 (數字變動)
            s = random.randint(10, 30) # 周長
            r = random.randint(2, 6)   # 半徑
            area = s * r // 2
            q_data = {
                "q": f"三角形周長 {s}，面積 {area}，內切圓半徑？", 
                "options": [str(r), str(r*2), str(area//s), str(s//r)], "ans": str(r),
                "expl": "面積 = rs/2。", "svg": "triangle_incenter_concept", "params": {}
            }

        elif q_type == 3: # 直角三角形 r (數字變動)
            k = random.randint(1, 5)
            a, b, c = 3*k, 4*k, 5*k
            r = (a + b - c) // 2
            q_data = {
                "q": f"直角三角形三邊 {a}, {b}, {c}，求內切圓半徑？", 
                "options": [str(r), str(r+1), str(r*2), str(c//2)], "ans": str(r),
                "expl": "(股+股-斜)/2。", "svg": "right_triangle_incenter", "params": {"a":a,"b":b,"c":c}
            }
            
        elif q_type == 4: # 定義 (固定)
            q_data = {
                "q": "內心是哪三條線的交點？", 
                "options": ["角平分線", "中垂線", "中線", "高"], "ans": "角平分線",
                "expl": "定義。", "svg": "none", "params": {}
            }
            
        if q_data: add_q("3-3 三角形的內心", q_data)

    # ==========================================
    # 單元 3-4: 重心
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 5)
        q_data = None
        
        if q_type == 1: # 長度 (數字變動)
            m = random.randint(3, 20) * 3
            ag = m * 2 // 3
            q_data = {
                "q": f"G 為重心，中線 AD 長為 {m}，求 AG？", 
                "options": [str(ag), str(m), str(m//3), str(ag+1)], "ans": str(ag),
                "expl": "2/3 中線長。", "svg": "triangle_centroid", "params": {"m": m}
            }
            
        elif q_type == 2: # 面積分割 (數字變動)
            area = random.randint(6, 40) * 6
            sub = area // 6
            q_data = {
                "q": f"△ABC 面積 {area}，G 為重心，△GAB 面積？", 
                "options": [str(sub*2), str(sub), str(area//2), str(area)], "ans": str(sub*2),
                "expl": "重心與三頂點連線佔 1/3。", "svg": "triangle_centroid", "params": {"m": "?"}
            }
            
        elif q_type == 3: # 定義 (固定)
            q_data = {
                "q": "重心是哪三條線的交點？", 
                "options": ["中線", "中垂線", "角平分線"], "ans": "中線",
                "expl": "定義。", "svg": "none", "params": {}
            }
            
        elif q_type == 4: # 座標 (數字變動)
            x3, y3 = random.randint(0,9), random.randint(0,9)
            # A(0,0) B(3,0) C(x3,y3) -> G(1+x3/3, y3/3)
            # 簡化: 三點相加
            ans_x = (3 + x3) // 3
            ans_y = y3 // 3
            if (3+x3)%3 == 0 and y3%3 == 0:
                q_data = {
                    "q": f"A(0,0), B(3,0), C({x3},{y3})，求重心座標？", 
                    "options": [f"({ans_x},{ans_y})", f"({ans_x+1},{ans_y})", f"({x3},{y3})"], "ans": f"({ans_x},{ans_y})",
                    "expl": "座標平均。", "svg": "none", "params": {}
                }

        if q_data: add_q("3-4 三角形的重心", q_data)

    # ==========================================
    # 單元 4-1: 因式分解
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 5)
        q_data = None
        
        if q_type == 1: # 提公因式 (數字變動)
            k = random.randint(2, 9)
            q_data = {
                "q": f"解方程式 x² - {k}x = 0？", 
                "options": [f"0, {k}", f"{k}", "0", f"1, {k}"], "ans": f"0, {k}",
                "expl": "x(x-k)=0。", "svg": "none", "params": {}
            }
            
        elif q_type == 2: # 平方差 (數字變動)
            k = random.randint(2, 9)
            k2 = k*k
            q_data = {
                "q": f"解方程式 x² - {k2} = 0？", 
                "options": [f"±{k}", f"{k}", f"{k2}", "無解"], "ans": f"±{k}",
                "expl": "x = ±√k²。", "svg": "diff_squares", "params": {"k": k}
            }
            
        elif q_type == 3: # 十字交乘 (數字變動)
            r1, r2 = random.randint(1, 6), random.randint(1, 6)
            b = r1 + r2
            c = r1 * r2
            q_data = {
                "q": f"因式分解 x² - {b}x + {c}？", 
                "options": [f"(x-{r1})(x-{r2})", f"(x+{r1})(x+{r2})", f"(x+{b})(x+{c})"], "ans": f"(x-{r1})(x-{r2})",
                "expl": "十字交乘。", "svg": "none", "params": {}
            }
            
        elif q_type == 4: # 完全平方 (數字變動)
            k = random.randint(1, 9)
            b = 2*k
            c = k*k
            q_data = {
                "q": f"因式分解 x² + {b}x + {c}？", 
                "options": [f"(x+{k})²", f"(x-{k})²", f"(x+{b})²"], "ans": f"(x+{k})²",
                "expl": "和的平方公式。", "svg": "area_square_k", "params": {"k": b}
            }

        if q_data: add_q("4-1 因式分解法", q_data)
        
    # ==========================================
    # 單元 4-2: 配方法
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        
        if q_type == 1: # 判別式 (數字變動)
            b = random.choice([2,4,6,8])
            c = random.randint(1, 5)
            d = b*b - 4*c
            q_data = {
                "q": f"方程式 x² + {b}x + {c} = 0 的判別式 D = ？", 
                "options": [str(d), str(d+1), str(d-1)], "ans": str(d),
                "expl": "b² - 4ac。", "svg": "none", "params": {}
            }
            
        elif q_type == 2: # 配方補項 (數字變動)
            k = random.randint(2, 10) * 2
            ans = (k // 2) ** 2
            q_data = {
                "q": f"將 x² + {k}x 配成完全平方式，需加上？", 
                "options": [str(ans), str(k), str(k*2)], "ans": str(ans),
                "expl": "一半的平方。", "svg": "area_square_k", "params": {"k": k}
            }
            
        elif q_type == 3: # 兩根和 (數字變動)
            b = random.randint(2, 9)
            q_data = {
                "q": f"x² + {b}x + 1 = 0 的兩根和？", 
                "options": [str(-b), str(b), "1"], "ans": str(-b),
                "expl": "-b/a。", "svg": "none", "params": {}
            }
        
        elif q_type == 4: # 根的性質 (固定變化)
            pair = random.choice([("D>0", "兩相異實根"), ("D=0", "重根"), ("D<0", "無實根")])
            q_data = {
                "q": f"若判別式 {pair[0]}，則方程式有？", 
                "options": ["兩相異實根", "重根", "無實根"], "ans": pair[1],
                "expl": "判別式性質。", "svg": "none", "params": {}
            }

        if q_data: add_q("4-2 配方法與公式解", q_data)

    # ==========================================
    # 單元 4-3: 應用問題
    # ==========================================
    for _ in range(300):
        q_type = random.randint(1, 4)
        q_data = None
        
        if q_type == 1: # 正方形 (數字變動)
            s = random.randint(5, 20)
            area = s*s
            q_data = {
                "q": f"正方形面積 {area}，邊長？", 
                "options": [str(s), str(area//2), str(s*2)], "ans": str(s),
                "expl": "開根號。", "svg": "area_square", "params": {"s": s}
            }
            
        elif q_type == 2: # 兩數積 (數字變動)
            n = random.randint(2, 9)
            val = n * (n+1)
            q_data = {
                "q": f"兩連續正整數乘積為 {val}，求較小數？", 
                "options": [str(n), str(n+1), str(n-1)], "ans": str(n),
                "expl": "x(x+1) = val。", "svg": "none", "params": {}
            }
            
        elif q_type == 3: # 梯子 (數字變動)
            k = random.randint(2, 5)
            a, b, c = 3*k, 4*k, 5*k
            q_data = {
                "q": f"梯子長 {c}，腳離牆 {a}，梯頂高？", 
                "options": [str(b), str(c), str(a)], "ans": str(b),
                "expl": "畢氏定理。", "svg": "ladder_wall", "params": {"a":a,"b":b,"c":c}
            }
            
        elif q_type == 4: # 落體 (數字變動)
            t = random.randint(2, 5)
            h = 5 * t * t
            q_data = {
                "q": f"自由落體 h = 5t²，落下 {h} 公尺需幾秒？", 
                "options": [str(t), str(t*2), str(t+1)], "ans": str(t),
                "expl": "代入求解。", "svg": "none", "params": {}
            }

        if q_data: add_q("4-3 應用問題", q_data)

    # 寫入檔案
    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    # 統計
    total_q = sum(len(v) for v in database.values())
    print("\n" + "="*40)
    print(f"✅ V8.0 智慧去重版 - 更新成功！")
    print(f"💰 實際產出題數：{total_q} 題 (所有重複題目已被自動剔除)")
    print("="*40 + "\n")

if __name__ == "__main__":
    create_dataset()