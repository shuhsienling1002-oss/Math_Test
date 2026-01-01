import json
import random

# ==========================================
# 題庫製造工廠：負責生產 1000+ 種變化題
# ==========================================

def create_dataset():
    database = {
        "3-1 證明與推理": [],
        "3-2 三角形的外心、內心與重心": [],
        "4-1 因式分解法": [],
        "4-2 配方法與公式解": [],
        "4-3 應用問題": []
    }

    # ---------------------------------------------------------
    # 單元 3-1: 幾何證明 (目標 200 題)
    # ---------------------------------------------------------
    for _ in range(200):
        # 題型 1: 全等性質判斷
        prop = random.choice(["SSS", "SAS", "ASA", "AAS", "RHS"])
        q_type = random.choice([
            f"若兩個三角形符合「{prop}」條件，則它們的關係？",
            f"已知兩三角形三組對應邊/角滿足 {prop}，請問是否全等？",
            f"判別全等性質：{prop} 代表什麼？"
        ])
        database["3-1 證明與推理"].append({
            "question_text": q_type,
            "variables": {},
            "answer_formula": "'必全等'",
            "fixed_options": ["必全等", "不一定全等", "面積相等但形狀不同", "無法判斷"],
            "explanation": f"{prop} 是全等判別性質之一。",
            "svg": "geometry_sas"
        })

        # 題型 2: 角度計算
        a, b = random.randint(20, 80), random.randint(20, 80)
        database["3-1 證明與推理"].append({
            "question_text": f"三角形 ABC 中，∠A={a}°，∠B={b}°，求 ∠C 的外角？",
            "variables": {},
            "answer_formula": str(a + b),
            "wrong_formulas": [str(180 - (a + b)), "180", "90"],
            "explanation": f"外角 = {a} + {b} = {a+b}。",
            "svg": "none"
        })

        # 題型 3: 邊角關係
        database["3-1 證明與推理"].append({
            "question_text": "在 △ABC 中，若 ∠A > ∠B > ∠C，則下列邊長關係何者正確？",
            "variables": {},
            "answer_formula": "'BC > AC > AB'",
            "fixed_options": ["BC > AC > AB", "AB > AC > BC", "AC > BC > AB", "無法判斷"],
            "explanation": "大角對大邊：∠A 最大對邊 BC。",
            "svg": "none"
        })

    # ---------------------------------------------------------
    # 單元 3-2: 三心 (目標 200 題)
    # ---------------------------------------------------------
    for _ in range(200):
        # 題型 1: 重心長度
        m = random.randint(6, 30) * 3
        database["3-2 三角形的外心、內心與重心"].append({
            "question_text": f"若中線 AD 長為 {m}，G 為重心，求 AG 的長度？",
            "variables": {},
            "answer_formula": str(int(m * 2 / 3)),
            "wrong_formulas": [str(int(m / 2)), str(int(m / 3)), str(m)],
            "explanation": f"重心性質：頂點到重心 = 2/3 中線 = {int(m*2/3)}。",
            "svg": "triangle_centroid",
            "params_override": {"m": m}
        })

        # 題型 2: 內心角度
        deg = random.choice([40, 50, 60, 70, 80])
        database["3-2 三角形的外心、內心與重心"].append({
            "question_text": f"I 為內心，若 ∠A = {deg}°，求 ∠BIC？",
            "variables": {},
            "answer_formula": str(90 + deg // 2),
            "wrong_formulas": [str(180 - deg), str(90 + deg), str(2 * deg)],
            "explanation": f"內心角度公式：90 + A/2 = 90 + {deg//2} = {90 + deg//2}。",
            "svg": "triangle_incenter",
            "params_override": {"a": deg}
        })

        # 題型 3: 外心位置 (情境)
        loc_q = random.choice([
            "三個村莊想要蓋一座共用的消防局，到三村莊等距，應選在哪？",
            "要在三角形公園蓋一個噴水池，到三個頂點距離相等，圓心是？"
        ])
        database["3-2 三角形的外心、內心與重心"].append({
            "question_text": loc_q,
            "variables": {},
            "answer_formula": "'外心'",
            "fixed_options": ["外心", "內心", "重心", "垂心"],
            "explanation": "到三頂點等距是外心的性質。",
            "svg": "triangle_circumcenter"
        })

    # ---------------------------------------------------------
    # 單元 4-1: 因式分解 (目標 200 題)
    # ---------------------------------------------------------
    for _ in range(200):
        # 題型 1: 解方程式
        r1, r2 = random.randint(1, 9), random.randint(-9, -1)
        database["4-1 因式分解法"].append({
            "question_text": f"解方程式 (x - {r1})(x - {r2}) = 0？",
            "variables": {},
            "answer_formula": f"'{r1} 或 {r2}'",
            "fixed_options": [f"{r1} 或 {r2}", f"{-r1} 或 {-r2}", f"{r1} 或 {-r2}", "無解"],
            "explanation": f"令括號為 0，x={r1} 或 x={r2}。",
            "svg": "roots_line",
            "params_override": {"r1": r1, "r2": r2}
        })

        # 題型 2: 提公因式
        k = random.randint(2, 9)
        database["4-1 因式分解法"].append({
            "question_text": f"解方程式 x² - {k}x = 0？",
            "variables": {},
            "answer_formula": f"'0 或 {k}'",
            "fixed_options": [f"0 或 {k}", f"{k}", "0", f"1 或 {k}"],
            "explanation": f"提 x：x(x-{k})=0。",
            "svg": "roots_0_k",
            "params_override": {"k": k}
        })

    # ---------------------------------------------------------
    # 單元 4-2: 配方法 (目標 200 題)
    # ---------------------------------------------------------
    for _ in range(200):
        # 題型 1: 判別式計算
        b = random.choice([2, 4, 6, 8])
        c = random.randint(1, 3)
        ans_D = b*b - 4*c
        database["4-2 配方法與公式解"].append({
            "question_text": f"求 x² + {b}x + {c} = 0 的判別式 D？",
            "variables": {},
            "answer_formula": str(ans_D),
            "wrong_formulas": [str(ans_D + 4), str(ans_D - 4), "0"],
            "explanation": f"D = b² - 4ac = {b*b} - 4 = {ans_D}。",
            "svg": "none"
        })

        # 題型 2: 配方補數
        k = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
        ans_sq = (k // 2) ** 2
        database["4-2 配方法與公式解"].append({
            "question_text": f"將 x² + {k}x 配成完全平方式，需加上？",
            "variables": {},
            "answer_formula": str(ans_sq),
            "wrong_formulas": [str(k), str(k * 2), "1"],
            "explanation": f"加上 (一半)² = ({k}/2)² = {ans_sq}。",
            "svg": "area_square_k",
            "params_override": {"k": k}
        })

    # ---------------------------------------------------------
    # 單元 4-3: 應用問題 (目標 200 題)
    # ---------------------------------------------------------
    for _ in range(200):
        # 題型 1: 正方形面積
        s = random.randint(5, 20)
        area = s * s
        database["4-3 應用問題"].append({
            "question_text": f"某正方形農地面積為 {area} 平方公尺，求邊長？",
            "variables": {},
            "answer_formula": str(s),
            "wrong_formulas": [str(s * 2), str(area), str(s + 5)],
            "explanation": f"邊長 = √{area} = {s}。",
            "svg": "area_square",
            "params_override": {"s": s}
        })

        # 題型 2: 落體公式
        t = random.randint(2, 8)
        h = 5 * t * t
        database["4-3 應用問題"].append({
            "question_text": f"物體落下距離公式 h=5t²。若落下 {h} 公尺，需時幾秒？",
            "variables": {},
            "answer_formula": str(t),
            "wrong_formulas": [str(t * 2), str(t + 2), "10"],
            "explanation": f"{h} = 5t² → t²={t * t} → t={t}。",
            "svg": "none"
        })

    # 寫入檔案
    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已成功生成 questions.json，共包含 {sum(len(v) for v in database.values())} 題。")

if __name__ == "__main__":
    create_dataset()