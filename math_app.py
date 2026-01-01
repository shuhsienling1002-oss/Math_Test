import streamlit as st
import random

# ==========================================
# 1. 動態視覺引擎 (SVG Generator)
# ==========================================
class SVGGenerator:
    @staticmethod
    def coordinate_point(x, y, label="P"):
        cx, cy = 150 + (x * 25), 150 - (y * 25)
        return f"""<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#eee" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(#grid)" /><line x1="150" y1="0" x2="150" y2="300" stroke="black" stroke-width="2"/><line x1="0" y1="150" x2="300" y2="150" stroke="black" stroke-width="2"/><text x="285" y="145" font-weight="bold">x</text><text x="155" y="15" font-weight="bold">y</text><circle cx="{cx}" cy="{cy}" r="6" fill="red" stroke="white" stroke-width="2"/><text x="{cx+10}" y="{cy-10}" fill="red" font-weight="bold" font-size="16">{label}({x},{y})</text></svg>"""

    @staticmethod
    def number_line(p1, p2):
        x1, x2 = 200 + (p1 * 25), 200 + (p2 * 25)
        dist, mid = abs(p2 - p1), (x1 + x2) / 2
        return f"""<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="60" x2="380" y2="60" stroke="black" stroke-width="2"/><line x1="200" y1="55" x2="200" y2="65" stroke="black" stroke-width="2"/><text x="200" y="85" text-anchor="middle">0</text><circle cx="{x1}" cy="60" r="5" fill="blue"/><text x="{x1}" y="40" text-anchor="middle" fill="blue" font-weight="bold">{p1}</text><circle cx="{x2}" cy="60" r="5" fill="red"/><text x="{x2}" y="40" text-anchor="middle" fill="red" font-weight="bold">{p2}</text><path d="M{x1},60 Q{mid},{60-dist*4} {x2},60" stroke="purple" stroke-width="2" fill="none" stroke-dasharray="5,5"/><text x="{mid}" y="{50-dist*2}" text-anchor="middle" fill="purple" font-weight="bold">距離 = {dist}</text></svg>"""

    @staticmethod
    def probability_balls(red, white, green=0):
        balls = ""
        sx = 40
        for _ in range(red): balls += f'<circle cx="{sx}" cy="40" r="12" fill="#ff4444" stroke="black"/><text x="{sx}" y="44" text-anchor="middle" fill="white" font-size="10">紅</text>'; sx += 30
        for _ in range(white): balls += f'<circle cx="{sx}" cy="40" r="12" fill="white" stroke="black"/><text x="{sx}" y="44" text-anchor="middle" fill="black" font-size="10">白</text>'; sx += 30
        for _ in range(green): balls += f'<circle cx="{sx}" cy="40" r="12" fill="#44ff44" stroke="black"/><text x="{sx}" y="44" text-anchor="middle" fill="black" font-size="10">綠</text>'; sx += 30
        return f'<svg width="400" height="80" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#eee" rx="10"/>{balls}</svg>'

    @staticmethod
    def triangle_label(a, b, c="?"):
        return f"""<svg width="250" height="180" xmlns="http://www.w3.org/2000/svg"><path d="M40,140 L200,140 L40,20 Z" fill="#e3f2fd" stroke="blue" stroke-width="3"/><rect x="40" y="120" width="20" height="20" fill="none" stroke="blue"/><text x="120" y="160" text-anchor="middle" font-size="16">底={a}</text><text x="25" y="90" text-anchor="end" font-size="16">高={b}</text><text x="130" y="70" text-anchor="start" font-size="16" fill="red" font-weight="bold">斜邊={c}</text></svg>"""

    @staticmethod
    def linear_func(m, k):
        coords = 'x1="50" y1="250" x2="250" y2="50"' if m > 0 else 'x1="50" y1="50" x2="250" y2="250"' if m < 0 else 'x1="20" y1="150" x2="280" y2="150"'
        desc = "斜率 > 0 (右上)" if m > 0 else "斜率 < 0 (左上)" if m < 0 else "水平線"
        return f"""<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg"><line x1="150" y1="0" x2="150" y2="300" stroke="black"/><line x1="0" y1="150" x2="300" y2="150" stroke="black"/><line {coords} stroke="blue" stroke-width="3"/><text x="150" y="280" text-anchor="middle" font-weight="bold">{desc}</text></svg>"""

    @staticmethod
    def parabola(a, k):
        path = "M 50,50 Q 150,250 250,50" if a > 0 else "M 50,250 Q 150,50 250,250"
        desc = "開口向上 (a>0)" if a > 0 else "開口向下 (a<0)"
        return f"""<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg"><line x1="150" y1="0" x2="150" y2="300" stroke="black"/><line x1="0" y1="150" x2="300" y2="150" stroke="black"/><path d="{path}" stroke="red" stroke-width="2" fill="none"/><circle cx="150" cy="{150}" r="4" fill="blue"/><text x="150" y="280" text-anchor="middle" font-weight="bold">{desc}</text></svg>"""

    @staticmethod
    def geometry_sas():
        """畫出兩個三角形示意全等性質"""
        return f"""<svg width="300" height="150" xmlns="http://www.w3.org/2000/svg"><path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text><text x="115" y="80" text-anchor="middle" font-weight="bold" fill="blue">全等?</text></svg>"""

    @staticmethod
    def triangle_centroid():
        """畫出重心示意圖 (中線交點)"""
        return f"""<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><path d="M100,20 L20,180 L180,180 Z" fill="none" stroke="black" stroke-width="2"/><line x1="100" y1="20" x2="100" y2="180" stroke="red" stroke-width="1" stroke-dasharray="4"/><line x1="20" y1="180" x2="140" y2="100" stroke="red" stroke-width="1" stroke-dasharray="4"/><line x1="180" y1="180" x2="60" y2="100" stroke="red" stroke-width="1" stroke-dasharray="4"/><circle cx="100" cy="126" r="4" fill="blue"/><text x="110" y="126" fill="blue" font-weight="bold">G (重心)</text></svg>"""

# ==========================================
# 2. 滿血版題庫 (Full Content with Updates)
# ==========================================
MATH_DB = {
    # ======= 七年級 =======
    "7上：整數運算與絕對值": [
        {"q": "【圖解】數線上 -5 到 3 的距離？", "options": ["8", "2", "-8", "-2"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.number_line(-5, 3), "expl": "距離 = $3 - (-5) = 8$。"},
        {"q": "計算 $(-8) + 12 + (-5)$？", "options": ["-1", "1", "25", "-25"], "ans": 0, "diff": "簡單", "expl": "$4 + (-5) = -1$。"},
        {"q": "若 $|a| = 5$，且 $a$ 在原點左邊，則 $a$ 是？", "options": ["-5", "5", "0", "25"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.number_line(-5, 0), "expl": "原點左邊為負數，故為 -5。"},
        {"q": "絕對值小於 4 的「整數」有幾個？", "options": ["7", "6", "3", "無限多"], "ans": 0, "diff": "中等", "expl": "$-3, -2, -1, 0, 1, 2, 3$，共 7 個。"}
    ],
    "7上：分數與指數": [
        {"q": "計算 $\\frac{1}{2} - \\frac{2}{3}$？", "options": ["-1/6", "1/6", "-1", "1"], "ans": 0, "diff": "簡單", "expl": "通分：$\\frac{3}{6} - \\frac{4}{6} = -\\frac{1}{6}$。"},
        {"q": "科學記號 $3.5 \\times 10^{-4}$ 小數點後第幾位開始不為 0？", "options": ["4", "3", "5", "10"], "ans": 0, "diff": "中等", "expl": "$-4$ 次方代表小數點後第 4 位。"},
        {"q": "計算 $(-1)^5 \\times (-1)^4$？", "options": ["-1", "1", "2", "-2"], "ans": 0, "diff": "簡單", "expl": "$-1 \\times 1 = -1$。"}
    ],
    "7上：一元一次方程式": [
        {"q": "解 $3x - 5 = 10$？", "options": ["5", "15", "3", "5/3"], "ans": 0, "diff": "簡單", "expl": "$3x = 15 \\Rightarrow x = 5$。"},
        {"q": "甲比乙大 10 歲，和為 50，求乙？", "options": ["20", "30", "15", "25"], "ans": 0, "diff": "中等", "expl": "設乙 $x$，甲 $x+10$。$2x+10=50 \\Rightarrow 2x=40 \\Rightarrow x=20$。"},
        {"q": "化簡 $2(x-3) - (x+1)$？", "options": ["$x-7$", "$x-5$", "$x-4$", "$2x-7$"], "ans": 0, "diff": "中等", "expl": "$2x-6-x-1 = x-7$。"}
    ],
    "7下：二元一次聯立方程式": [
        {"q": "解 $\\begin{cases} x+y=4 \\\\ x-y=2 \\end{cases}$，求 x？", "options": ["3", "1", "2", "4"], "ans": 0, "diff": "簡單", "expl": "相加得 $2x=6 \\Rightarrow x=3$。"},
        {"q": "若 $2x + 3y = 12$，且 $x, y$ 為正整數，有幾組解？", "options": ["1", "2", "3", "無限多"], "ans": 0, "diff": "困難", "expl": "當 $x=3, y=2$ (僅此一組正整數解)。"}
    ],
    "7下：直角坐標與圖形": [
        {"q": "【圖解】點 (-3, 4) 在第幾象限？", "options": ["二", "一", "三", "四"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.coordinate_point(-3, 4), "expl": "左上為第二象限。"},
        {"q": "【圖解】直線 $y = -2x + 1$ 的圖形走勢？", "options": ["左上右下", "右上左下", "水平", "垂直"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.linear_func(-2, 1), "expl": "斜率 -2 小於 0，故為左上右下。"}
    ],
    "7下：比例與不等式": [
        {"q": "若 $3:x = 2:6$，求 x？", "options": ["9", "4", "1", "18"], "ans": 0, "diff": "簡單", "expl": "$2x = 18 \\Rightarrow x = 9$。"},
        {"q": "解不等式 $-2x > 6$？", "options": ["$x < -3$", "$x > -3$", "$x < 3$", "$x > 3$"], "ans": 0, "diff": "中等", "expl": "除以負數，開口方向要改變。"}
    ],

    # ======= 八年級 =======
    "8上：乘法公式與多項式": [
        {"q": "展開 $(x+3)^2$？", "options": ["$x^2+6x+9$", "$x^2+9$", "$x^2+3x+9$", "$x^2+6x+6$"], "ans": 0, "diff": "簡單", "expl": "$a^2 + 2ab + b^2$。"},
        {"q": "計算 $102 \\times 98$？", "options": ["9996", "10004", "9999", "10000"], "ans": 0, "diff": "中等", "expl": "$(100+2)(100-2) = 100^2 - 4 = 9996$。"}
    ],
    "8上：平方根與畢氏定理": [
        {"q": "【圖解】直角三角形股為 6, 8，斜邊？", "options": ["10", "14", "12", "100"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"), "expl": "$\\sqrt{36+64} = 10$。"},
        {"q": "計算 $\\sqrt{12}$？", "options": ["$2\\sqrt{3}$", "$3\\sqrt{2}$", "6", "4"], "ans": 0, "diff": "簡單", "expl": "$\\sqrt{4 \\times 3} = 2\\sqrt{3}$。"}
    ],
    "8上：因式分解": [
        {"q": "分解 $x^2 - 16$？", "options": ["$(x+4)(x-4)$", "$(x-4)^2$", "$(x+4)^2$", "$(x-8)(x+2)$"], "ans": 0, "diff": "簡單", "expl": "平方差公式。"},
        {"q": "分解 $x^2 + 3x + 2$？", "options": ["$(x+1)(x+2)$", "$(x+3)(x+1)$", "$(x-1)(x-2)$", "無法分解"], "ans": 0, "diff": "中等", "expl": "十字交乘：1x2=2, 1+2=3。"}
    ],
    # --- 考前特化：八上第四章 一元二次方程式 ---
    "8上-4-1：因式分解法解方程式": [
        {"q": "解方程式 $(x-2)(x+3) = 0$ 的根？", "options": ["2 或 -3", "-2 或 3", "2 或 3", "-2 或 -3"], "ans": 0, "diff": "簡單", "expl": "兩數相乘為0，則其中一數必為0。$x-2=0$ 或 $x+3=0$。"},
        {"q": "方程式 $x^2 - 5x = 0$ 的解？", "options": ["0 或 5", "5", "0", "1 或 5"], "ans": 0, "diff": "簡單", "expl": "提公因式：$x(x-5)=0$，故 $x=0$ 或 $x=5$。"},
        {"q": "若 $x=1$ 是方程式 $x^2 + kx + 2 = 0$ 的一根，則 k = ？", "options": ["-3", "3", "-2", "1"], "ans": 0, "diff": "中等", "expl": "將 $x=1$ 代入：$1 + k + 2 = 0 \\Rightarrow k = -3$。"},
        {"q": "解 $x^2 - 9 = 0$？", "options": ["3 或 -3", "3", "9", "81"], "ans": 0, "diff": "簡單", "expl": "因式分解 $(x+3)(x-3)=0$ 或移項 $x^2=9$。"},
        {"q": "解方程式 $x^2 + 6x + 9 = 0$？", "options": ["-3 (重根)", "3 (重根)", "3 或 -3", "9"], "ans": 0, "diff": "中等", "expl": "完全平方式：$(x+3)^2 = 0 \\Rightarrow x = -3$ (重根)。"}
    ],
    "8上-4-2：配方法與公式解": [
        {"q": "一元二次方程式 $ax^2 + bx + c = 0$ 的公式解為？", "options": ["$\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$", "$\\frac{-b \\pm \\sqrt{b^2+4ac}}{2a}$", "$\\frac{b \\pm \\sqrt{b^2-4ac}}{2a}$", "$\\frac{-b \\pm \\sqrt{b^2-4ac}}{a}$"], "ans": 0, "diff": "簡單", "expl": "這是必背公式！判別式是 $b^2-4ac$。"},
        {"q": "判別方程式 $x^2 + x + 1 = 0$ 的解的情形？", "options": ["無解 (無實數解)", "相異兩根", "重根", "無法判斷"], "ans": 0, "diff": "中等", "expl": "判別式 $D = b^2 - 4ac = 1^2 - 4(1)(1) = -3 < 0$，故無實數解。"},
        {"q": "若要將 $x^2 + 6x$ 配成完全平方式，需加上多少？", "options": ["9", "6", "3", "36"], "ans": 0, "diff": "簡單", "expl": "加上中間項係數一半的平方：$(6/2)^2 = 3^2 = 9$。"},
        {"q": "解 $(x-1)^2 = 5$？", "options": ["$1 \\pm \\sqrt{5}$", "$\\pm \\sqrt{5}$", "$1 + \\sqrt{5}$", "6"], "ans": 0, "diff": "中等", "expl": "直接開根號：$x-1 = \\pm\\sqrt{5} \\Rightarrow x = 1 \\pm \\sqrt{5}$。"},
        {"q": "方程式 $x^2 - 4x + 4 = 0$ 的判別式值為？", "options": ["0", "4", "8", "-4"], "ans": 0, "diff": "簡單", "expl": "$(-4)^2 - 4(1)(4) = 16 - 16 = 0$。"}
    ],
    "8上-4-3：應用問題": [
        {"q": "兩連續正偶數的乘積為 48，求此兩數？", "options": ["6, 8", "4, 12", "8, 10", "-6, -8"], "ans": 0, "diff": "簡單", "expl": "設小數為 $x$，則 $x(x+2)=48$。驗算 $6 \\times 8 = 48$。"},
        {"q": "正方形面積為 100 平方公分，邊長增加 x 後面積變為 144，求 x？", "options": ["2", "4", "12", "10"], "ans": 0, "diff": "中等", "expl": "原邊長 10。新邊長 $10+x$。$(10+x)^2 = 144 \\Rightarrow 10+x=12 \\Rightarrow x=2$。"},
        {"q": "長方形長比寬多 3，面積 40，求寬？", "options": ["5", "8", "4", "10"], "ans": 0, "diff": "中等", "expl": "設寬 $x$，長 $x+3$。$x(x+3)=40 \Rightarrow x^2+3x-40=0 \Rightarrow (x+8)(x-5)=0$。邊長取正，$x=5$。"},
        {"q": "某數的平方等於該數的 3 倍，求某數？", "options": ["0 或 3", "3", "0", "9"], "ans": 0, "diff": "中等", "expl": "$x^2 = 3x \Rightarrow x^2 - 3x = 0 \Rightarrow x(x-3)=0$。"}
    ],
    "8下：等差數列": [
        {"q": "數列 1, 3, 5, 7, ... 第 10 項？", "options": ["19", "20", "21", "17"], "ans": 0, "diff": "簡單", "expl": "$a_{10} = 1 + 9 \\times 2 = 19$。"}
    ],
    "8下：幾何圖形": [
        {"q": "正三角形的一個內角幾度？", "options": ["60", "90", "45", "180"], "ans": 0, "diff": "簡單", "expl": "180 除以 3。"}
    ],

    # ======= 九年級 =======
    "9上：相似形與比例": [
        {"q": "兩相似三角形邊長比 1:3，面積比？", "options": ["1:9", "1:3", "1:6", "3:1"], "ans": 0, "diff": "簡單", "expl": "面積比為邊長平方比。"},
        {"q": "地圖比例尺 1:1000，圖上 5cm 代表實際？", "options": ["50m", "500m", "5m", "5000cm"], "ans": 0, "diff": "中等", "expl": "5000 cm = 50 m。"}
    ],
    "9上：圓的性質": [
        {"q": "【圖解】一圓半徑 5，弦心距 3，弦長？", "options": ["8", "4", "10", "6"], "ans": 0, "diff": "困難", "svg_gen": lambda: SVGGenerator.triangle_label("?", 3, 5), "expl": "半弦長 = $\\sqrt{5^2-3^2}=4$。弦長 = $4 \\times 2 = 8$。"},
        {"q": "切線與過切點的半徑夾角？", "options": ["90度", "45度", "60度", "180度"], "ans": 0, "diff": "簡單", "expl": "切線垂直半徑。"}
    ],
    # --- 考前特化：九上第三章 外心、內心與重心 ---
    "9上-3-1：證明與推理": [
        {"q": "【圖解】若兩三角形三邊對應相等 (SSS)，則兩三角形？", "options": ["全等", "相似但不全等", "面積相等但不全等", "無關"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.geometry_sas(), "expl": "SSS 是全等性質之一。"},
        {"q": "下列何者「不是」全等三角形的判別性質？", "options": ["AAA", "SAS", "ASA", "SSS"], "ans": 0, "diff": "中等", "expl": "AAA (角角角) 只能保證相似 (形狀一樣)，大小不一定一樣。"},
        {"q": "在 $\Delta ABC$ 中，若 $\angle A > \angle B$，則對邊關係？", "options": ["BC > AC", "BC < AC", "BC = AC", "無法判斷"], "ans": 0, "diff": "簡單", "expl": "大角對大邊，$\angle A$ 對邊 $BC$ 大於 $\angle B$ 對邊 $AC$。"},
        {"q": "等腰三角形的兩底角？", "options": ["相等", "互補", "互餘", "無關"], "ans": 0, "diff": "簡單", "expl": "等腰三角形性質：等邊對等角。"},
        {"q": "直角三角形斜邊上的中線長等於？", "options": ["斜邊的一半", "斜邊", "一股長", "無法確定"], "ans": 0, "diff": "中等", "expl": "直角三角形外心在斜邊中點，故中線長 = 半徑 = 斜邊一半。"}
    ],
    "9上-3-2：三角形的外心、內心與重心": [
        {"q": "【圖解】三角形的「重心」是哪三條線的交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_centroid(), "expl": "重心 (G) 是三條中線的交點。"},
        {"q": "【圖解】重心到頂點的距離是到對邊中點距離的幾倍？", "options": ["2倍", "1.5倍", "3倍", "1倍"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_centroid(), "expl": "重心性質：頂點到重心 : 重心到中點 = 2 : 1。"},
        {"q": "三角形的「外心」到哪裡等距離？", "options": ["三頂點", "三邊", "重心", "垂心"], "ans": 0, "diff": "中等", "expl": "外心是外接圓圓心，半徑相等，故到三頂點等距。"},
        {"q": "三角形的「內心」到哪裡等距離？", "options": ["三邊", "三頂點", "重心", "垂心"], "ans": 0, "diff": "中等", "expl": "內心是內切圓圓心，半徑相等，故到三邊垂直距離相等。"},
        {"q": "鈍角三角形的外心位置在？", "options": ["三角形外部", "三角形內部", "斜邊上", "頂點上"], "ans": 0, "diff": "中等", "expl": "銳角在內，直角在邊(斜邊中點)，鈍角在外。"},
        {"q": "正三角形的重心、外心、內心位置？", "options": ["重合 (同一點)", "在同一直線上", "形成三角形", "無關"], "ans": 0, "diff": "簡單", "expl": "正三角形三心(含垂心)合一。"}
    ],
    "9下：二次函數": [
        {"q": "【圖解】拋物線 $y = x^2$ 開口？", "options": ["向上", "向下", "向左", "向右"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.parabola(1, 0), "expl": "係數正，開口向上。"},
        {"q": "【圖解】函數 $y = -2(x-1)^2 + 3$ 的頂點？", "options": ["(1, 3)", "(-1, 3)", "(1, -3)", "(-1, -3)"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.parabola(-2, 3), "expl": "頂點式 $(h, k)$，此處為 $(1, 3)$。"}
    ],
    "9下：統計與機率": [
        {"q": "【圖解】袋中 3 紅 2 白，抽紅球機率？", "options": ["3/5", "2/5", "1/5", "1/2"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.probability_balls(3, 2), "expl": "紅球3顆，總數5顆。"}
    ]
}

# ==========================================
# 3. APP 主程式
# ==========================================
def reset_exam():
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：考前衝刺特化版", page_icon="💯", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("💯 數學考前衝刺")
    st.sidebar.caption("針對 108 課綱段考範圍特化")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)
    st.sidebar.success(f"目前選擇：{selected_unit}")
    st.sidebar.info("💡 每個單元包含 5-10 題精選題，系統會隨機出題！")

    st.title("💯 國中數學：考前衝刺特化版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info(f"準備好挑戰 **{selected_unit}** 了嗎？")
        if st.button("🚀 開始測驗", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            all_questions = MATH_DB.get(selected_unit, [])
            num_to_pick = min(len(all_questions), 10)
            if num_to_pick == 0:
                st.error("此單元暫無題目")
            else:
                st.session_state.current_questions = random.sample(all_questions, num_to_pick)
                st.session_state.exam_started = True
                st.rerun()

    else:
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"進度：0/{total_q}")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                if q.get("svg_gen"):
                    st.markdown(q["svg_gen"](), unsafe_allow_html=True)
                    st.caption("👆 請參考上方圖形作答")
                st.markdown(f"### {q['q']}")
                st.radio("選項", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            if st.form_submit_button("✅ 交卷看解析", use_container_width=True):
                score = 0
                results = []
                for idx, q in enumerate(questions):
                    q_key = f"q_{idx}"
                    user_ans = st.session_state.get(q_key)
                    correct_ans = q['options'][q['ans']]
                    is_correct = (user_ans == correct_ans)
                    if is_correct: score += 1
                    results.append({"q": q, "is_correct": is_correct, "user": user_ans, "correct": correct_ans})
                
                st.session_state.exam_results = {"score": score, "total": total_q, "details": results}
                st.session_state.exam_finished = True

        if st.session_state.get("exam_finished") and st.session_state.exam_results:
            res = st.session_state.exam_results
            final_score = int((res['score'] / res['total']) * 100) if res['total'] > 0 else 0
            
            st.markdown("---")
            if final_score == 100: st.success(f"💯 滿分！這單元你已經無敵了！")
            elif final_score >= 60: st.info(f"👍 及格！繼續保持！")
            else: st.error(f"💪 不要氣餒，看詳解訂正！")
            st.markdown(f"### 得分：{final_score} 分")

            for i, item in enumerate(res['details']):
                q_data = item['q']
                with st.expander(f"第 {i+1} 題解析 ({'✅' if item['is_correct'] else '❌'})"):
                    if q_data.get("svg_gen"):
                        st.markdown(q_data["svg_gen"](), unsafe_allow_html=True)
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.markdown(f"**💡 解析**：")
                    st.markdown(q_data['expl'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 再刷一次 (題目不同)", use_container_width=True):
                    all_questions = MATH_DB.get(selected_unit, [])
                    num_to_pick = min(len(all_questions), 10)
                    st.session_state.current_questions = random.sample(all_questions, num_to_pick)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 選擇其他單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
