import streamlit as st
import random

# ==========================================
# 1. 內嵌視覺圖庫 (SVG Assets)
# ==========================================
SVG_ASSETS = {
    "number_line_dist": """
        <svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">
         <line x1="20" y1="50" x2="380" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
         <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs>
         <line x1="200" y1="45" x2="200" y2="55" stroke="black" stroke-width="2"/><text x="200" y="70" text-anchor="middle">0</text>
         <line x1="120" y1="45" x2="120" y2="55" stroke="black" stroke-width="2"/><text x="120" y="70" text-anchor="middle">-4</text>
         <line x1="280" y1="45" x2="280" y2="55" stroke="black" stroke-width="2"/><text x="280" y="70" text-anchor="middle">3</text>
         <path d="M120,40 Q200,10 280,40" stroke="red" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
         <text x="200" y="25" text-anchor="middle" fill="red" font-weight="bold">距離 = ?</text>
         <circle cx="120" cy="50" r="5" fill="red"/><circle cx="280" cy="50" r="5" fill="red"/>
        </svg>
    """,
    "coordinate_q2": """
        <svg width="300" height="300" viewBox="-150 -150 300 300" xmlns="http://www.w3.org/2000/svg">
         <line x1="-140" y1="0" x2="140" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
         <line x1="0" y1="140" x2="0" y2="-140" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
         <text x="130" y="20">x</text><text x="10" y="-130">y</text>
         <text x="-20" y="20">O</text>
         <circle cx="-80" cy="-60" r="6" fill="red"/>
         <text x="-110" y="-70" fill="red" font-size="16" font-weight="bold">P</text>
         <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#000" /></marker></defs>
        </svg>
    """,
    "pythagoras_visual": """
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
         <polygon points="50,150 250,150 50,50" style="fill:lightblue;stroke:black;stroke-width:2" />
         <rect x="50" y="130" width="20" height="20" style="fill:none;stroke:black;stroke-width:1"/>
         <text x="150" y="170" text-anchor="middle" font-size="14">股 a = 12</text>
         <text x="30" y="100" text-anchor="end" font-size="14">股 b = 5</text>
         <text x="160" y="90" text-anchor="start" font-size="16" fill="red" font-weight="bold">斜邊 c = ?</text>
        </svg>
    """,
    "parallel_lines": """
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
         <line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2"/><text x="290" y="55">L1</text>
         <line x1="20" y1="150" x2="280" y2="150" stroke="black" stroke-width="2"/><text x="290" y="155">L2</text>
         <line x1="80" y1="20" x2="220" y2="180" stroke="red" stroke-width="2"/>
         <text x="120" y="65" font-size="14">∠1</text>
         <text x="170" y="140" font-size="14" fill="blue" font-weight="bold">∠2 = ?</text>
         <text x="20" y="20" fill="gray">若 L1 // L2</text>
        </svg>
    """,
    "parabola_visual": """
        <svg width="300" height="300" viewBox="-10 -10 20 20" xmlns="http://www.w3.org/2000/svg">
         <line x1="-9" y1="0" x2="9" y2="0" stroke="gray" stroke-width="0.5"/>
         <line x1="0" y1="9" x2="0" y2="-9" stroke="gray" stroke-width="0.5"/>
         <path d="M -3,5 Q 0,-4 3,5" stroke="blue" stroke-width="1" fill="none"/>
         <circle cx="0" cy="-4" r="0.8" fill="red"/>
         <text x="1" y="-4" fill="red" font-size="2">頂點</text>
         <text x="-8" y="8" font-size="2">y = ax² + k</text>
        </svg>
    """,
    "circle_tangent": """
        <svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
         <circle cx="150" cy="150" r="80" stroke="black" stroke-width="2" fill="none"/>
         <circle cx="150" cy="150" r="3" fill="black"/><text x="140" y="145">O</text>
         <line x1="50" y1="250" x2="250" y2="50" stroke="red" stroke-width="2"/><text x="260" y="60" fill="red">L (切線)</text>
         <line x1="150" y1="150" x2="206.5" y2="93.5" stroke="blue" stroke-width="2" stroke-dasharray="5,5"/>
         <circle cx="206.5" cy="93.5" r="5" fill="red"/><text x="215" y="100">P (切點)</text>
         <text x="170" y="130" fill="blue">半徑 r</text>
         <text x="20" y="30" fill="gray">請問 OP 與 L 的夾角？</text>
        </svg>
    """
}

# ==========================================
# 2. 海量題庫 (Massive Math DB)
# ==========================================
MATH_DB = {
    # ---------------- 國一 (七年級) ----------------
    "七上：整數與絕對值": [
        {"q": "計算 $(-15) + 8 - (-5)$ 的值？", "options": ["-2", "-12", "2", "-28"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "負負得正：$-15 + 8 + 5 = -15 + 13 = -2$"},
        {"q": "若 $|a| = 6$，則 $a$ 的值可能為？", "options": ["6", "-6", "6 或 -6", "0"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "絕對值代表距離，距離為 6 的點有兩個。"},
        {"q": "【圖解題】參考數線圖，-4 到 3 的距離？", "options": ["1", "7", "-1", "-7"], "ans": 1, "diff": "簡單", "type": "單選", "svg": "number_line_dist", "expl": "距離 = 大減小 = $3 - (-4) = 7$。"},
        {"q": "計算 $12 \div (-3) \times 4$？", "options": ["-16", "-1", "16", "1"], "ans": 0, "diff": "中等", "type": "單選", "expl": "由左而右運算：$-4 \times 4 = -16$ (不能先算後面乘法！)"},
        {"q": "比 -8 大 5 的數是多少？", "options": ["-13", "-3", "3", "13"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "往右移 5 格：$-8 + 5 = -3$"},
        {"q": "若甲數為負整數，且 $|甲| < 4$，則甲數共有幾個？", "options": ["3", "4", "5", "無限多"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$-1, -2, -3$，共 3 個。"}
    ],
    "七上：分數與指數律": [
        {"q": "計算 $\\frac{2}{3} + (-\\frac{1}{4})$？", "options": ["5/12", "3/7", "1/12", "11/12"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "通分母為 12：$\\frac{8}{12} - \\frac{3}{12} = \\frac{5}{12}$。"},
        {"q": "計算 $(-\\frac{3}{2})^2 \div (-\\frac{9}{4})$？", "options": ["1", "-1", "2/3", "-9/8"], "ans": 1, "diff": "中等", "type": "單選", "expl": "平方變正：$\\frac{9}{4} \times (-\\frac{4}{9}) = -1$。"},
        {"q": "下列何者錯誤？", "options": ["$2^3 \times 2^2 = 2^5$", "$(2^3)^2 = 2^6$", "$2^0 = 1$", "$2^3 + 2^3 = 2^6$"], "ans": 3, "diff": "中等", "type": "單選", "expl": "$2^3 + 2^3 = 2 \times 2^3 = 2^4 \ne 2^6$ (相加不能指數相加)。"},
        {"q": "科學記號 $3.5 \times 10^{-3}$ 乘開後，小數點後第幾位開始不為 0？", "options": ["2", "3", "4", "5"], "ans": 1, "diff": "中等", "type": "單選", "expl": "$-3$ 次方代表小數點後第 3 位。"},
        {"q": "若 $5^{20} + 5^{20} + 5^{20} + 5^{20} + 5^{20} = 5^x$，則 x = ？", "options": ["21", "25", "100", "20"], "ans": 0, "diff": "困難", "type": "單選", "expl": "5 個 $5^{20}$ 相加 = $5 \times 5^{20} = 5^{1} \times 5^{20} = 5^{21}$。"}
    ],
    "七上：一元一次方程式": [
        {"q": "化簡 $5(x-2) - 2(2x+1)$？", "options": ["$x-12$", "$x-8$", "$9x-12$", "$x+8$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$5x - 10 - 4x - 2 = x - 12$。"},
        {"q": "解方程式 $\\frac{x}{3} + 1 = x - 3$？", "options": ["6", "4", "2", "-6"], "ans": 0, "diff": "中等", "type": "單選", "expl": "同乘 3：$x + 3 = 3x - 9 \Rightarrow 12 = 2x \Rightarrow x = 6$。"},
        {"q": "父親今年 40 歲，兒子 10 歲，幾年後父親年齡是兒子的 3 倍？", "options": ["5", "8", "10", "15"], "ans": 0, "diff": "中等", "type": "單選", "expl": "設 x 年後：$40+x = 3(10+x) \Rightarrow 40+x = 30+3x \Rightarrow 10=2x \Rightarrow x=5$。"},
        {"q": "某物打七折後賣 350 元，原價多少？", "options": ["500", "490", "450", "600"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$0.7x = 350 \Rightarrow x = 500$。"},
        {"q": "連續三個偶數的和是 60，其中最大的數是多少？", "options": ["18", "20", "22", "24"], "ans": 2, "diff": "中等", "type": "單選", "expl": "設中間數 $x$，則 $(x-2)+x+(x+2)=60 \Rightarrow 3x=60 \Rightarrow x=20$。最大數 $20+2=22$。"}
    ],
    "七下：二元一次聯立方程式": [
        {"q": "化簡 $3(x+y) - 2(x-y)$？", "options": ["$x+5y$", "$x+y$", "$5x+y$", "$x-5y$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$3x+3y-2x+2y = x+5y$ (注意負負得正)。"},
        {"q": "解 $\\begin{cases} x+y=5 \\\\ x-y=1 \\end{cases}$，$(x, y)$？", "options": ["(3, 2)", "(2, 3)", "(4, 1)", "(1, 4)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "相加：$2x=6 \Rightarrow x=3$。代回 $y=2$。"},
        {"q": "兩支原子筆與三支鉛筆共 50 元，一支原子筆比一支鉛筆貴 5 元，求原子筆一支多少錢？", "options": ["13", "8", "10", "15"], "ans": 0, "diff": "中等", "type": "單選", "expl": "設筆 $x$, 鉛 $y$。$2x+3y=50, x-y=5$。解得 $x=13, y=8$。"},
        {"q": "聯立方程式若有「無限多組解」，代表兩直線關係為何？", "options": ["重合", "平行", "交於一點", "垂直"], "ans": 0, "diff": "中等", "type": "單選", "expl": "係數成比例，代表是同一條直線 (重合)。"}
    ],
    "七下：坐標與函數圖形": [
        {"q": "【圖解題】點 P 在第三象限，其坐標特性？", "options": ["(+,+)", "(-,+)", "(-,-)", "(+,-)"], "ans": 2, "diff": "簡單", "type": "單選", "svg": "coordinate_q2", "expl": "左(-)、下(-)。"},
        {"q": "方程式 $y=3$ 的圖形是？", "options": ["水平線", "鉛垂線", "斜線", "拋物線"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "y 永遠是 3，不管 x 是多少，故為水平線。"},
        {"q": "函數 $f(x) = 2x - 5$，則 $f(3) = ？$", "options": ["1", "-1", "6", "11"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "代入 $x=3$，$2(3) - 5 = 1$。"},
        {"q": "若點 (a, -2) 在 x 軸上，則 a = ？", "options": ["0", "2", "-2", "無解 (點不可能在x軸)"], "ans": 3, "diff": "困難", "type": "單選", "expl": "x 軸上的點，y 坐標必須是 0。題目給 y=-2，故不可能在 x 軸上。陷阱題！"},
        {"q": "通過 (1, 2) 與 (0, 0) 的直線方程式？", "options": ["$y=2x$", "$y=x+1$", "$y=0.5x$", "$y=x$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "正比關係，斜率為 2。"}
    ],

    # ---------------- 國二 (八年級) ----------------
    "八上：乘法公式與多項式": [
        {"q": "展開 $(a-b)^2$？", "options": ["$a^2-b^2$", "$a^2+b^2$", "$a^2-2ab+b^2$", "$a^2+2ab+b^2$"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "差平方公式。"},
        {"q": "計算 $199^2$？", "options": ["39601", "39999", "39901", "39801"], "ans": 0, "diff": "中等", "type": "單選", "expl": "題目應為 $199^2=(200-1)^2 = 40000 - 400 + 1 = 39601$。"},
        {"q": "多項式 $2x^2 - 3x + 1$ 的二次項係數是多少？", "options": ["2", "-3", "1", "x"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$x^2$ 前面的數字。"},
        {"q": "計算 $(x+2)(x-3)$？", "options": ["$x^2-x-6$", "$x^2+x-6$", "$x^2-6$", "$x^2-5x-6$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$x^2 -3x +2x -6 = x^2 -x -6$。"}
    ],
    "八上：平方根與畢氏定理": [
        {"q": "【圖解題】兩股為 5, 12，斜邊？", "options": ["13", "17", "10", "15"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "pythagoras_visual", "expl": "常見商高數：5-12-13。"},
        {"q": "計算 $\sqrt{20}$ 化簡後？", "options": ["$2\sqrt{5}$", "$5\sqrt{2}$", "$4\sqrt{5}$", "10"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "$20 = 4 \times 5$，4 開出來是 2。"},
        {"q": "正方形面積為 10，邊長是？", "options": ["5", "$\sqrt{10}$", "2.5", "100"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "邊長 = $\sqrt{\\text{面積}}$。"},
        {"q": "直角三角形斜邊 10，一股 6，面積？", "options": ["24", "48", "30", "60"], "ans": 0, "diff": "中等", "type": "單選", "expl": "另一股為 $\sqrt{10^2-6^2}=8$。面積 $(6 \times 8) \div 2 = 24$。"}
    ],
    "八上：因式分解": [
        {"q": "分解 $x^2 - 25$？", "options": ["$(x-5)^2$", "$(x+5)(x-5)$", "$(x+25)(x-1)$", "無法分解"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "平方差：$a^2-b^2 = (a+b)(a-b)$。"},
        {"q": "分解 $x^2 + 5x + 6$？", "options": ["$(x+2)(x+3)$", "$(x+1)(x+6)$", "$(x-2)(x-3)$", "$(x-1)(x-6)$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "積 6 和 5 $\Rightarrow$ 2, 3。"},
        {"q": "分解 $3x^2 - 12$？", "options": ["$3(x-2)^2$", "$3(x+2)(x-2)$", "$(3x+6)(x-2)$", "$3(x^2-4)$ (未完成)"], "ans": 1, "diff": "中等", "type": "單選", "expl": "先提 3 得 $3(x^2-4)$，再平方差。"},
        {"q": "若 $x^2 + kx + 16$ 是完全平方式，k 可能為？", "options": ["4", "8", "8 或 -8", "16"], "ans": 2, "diff": "困難", "type": "單選", "expl": "中間項為 $2ab$。$2 \times x \times 4 = 8x$，但也可能是 $-8x$。"}
    ],
    "八下：等差數列與級數": [
        {"q": "數列 2, 5, 8, ... 第 20 項？", "options": ["59", "60", "62", "57"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$a_{20} = 2 + 19 \times 3 = 59$。"},
        {"q": "級數 1+2+...+100？", "options": ["5050", "5000", "5100", "10100"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "梯形公式：$(1+100) \times 100 \div 2 = 5050$。"},
        {"q": "若三數成等差，和為 15，則中間項為？", "options": ["3", "5", "7", "無法得知"], "ans": 1, "diff": "簡單", "type": "單選", "expl": "等差中項 $\times$ 項數 = 總和。$x \times 3 = 15 \Rightarrow x=5$。"}
    ],
    "八下：幾何圖形與性質": [
        {"q": "【圖解題】L1//L2，內錯角 ∠1, ∠2 關係？", "options": ["相等", "互補", "互餘", "無關"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "parallel_lines", "expl": "平行線內錯角相等。"},
        {"q": "正五邊形的「內角和」度數？", "options": ["540", "720", "360", "180"], "ans": 0, "diff": "中等", "type": "單選", "expl": "$(5-2) \times 180 = 540$。"},
        {"q": "三角形兩邊長為 3, 7，第三邊長可能是？", "options": ["3", "4", "7", "10"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "兩邊和 > 第三邊，兩邊差 < 第三邊。$4 < x < 10$，選 7。"},
        {"q": "平行四邊形的對角線具有什麼性質？", "options": ["互相平分", "互相垂直", "等長", "平分且等長"], "ans": 0, "diff": "中等", "type": "單選", "expl": "互相平分是平行四邊形的特性。菱形才垂直，矩形才等長。"}
    ],

    # ---------------- 國三 (九年級) ----------------
    "九上：相似形": [
        {"q": "兩相似三角形對應邊比 1:3，面積比？", "options": ["1:3", "1:6", "1:9", "3:1"], "ans": 2, "diff": "簡單", "type": "單選", "expl": "面積比 = 邊長平方比。"},
        {"q": "地圖比例尺 1:100，圖上 2cm 代表實際？", "options": ["2m", "200m", "20m", "0.2m"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "200 cm = 2 m。"},
        {"q": "一直角三角形三邊 3,4,5，放大 2 倍後，新三角形面積是原來的幾倍？", "options": ["2", "4", "8", "16"], "ans": 1, "diff": "中等", "type": "單選", "expl": "邊長 2 倍，面積 $2^2=4$ 倍。"}
    ],
    "九上：圓的性質": [
        {"q": "【圖解題】半徑與切線夾角？", "options": ["90度", "60度", "45度", "180度"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "circle_tangent", "expl": "切線垂直半徑。"},
        {"q": "圓內接四邊形對角關係？", "options": ["互補", "相等", "互餘", "無關"], "ans": 0, "diff": "中等", "type": "單選", "expl": "對角和 180 度。"},
        {"q": "兩圓外切，半徑分別為 3, 5，則連心線長？", "options": ["8", "2", "15", "4"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "外切距離 = 半徑相加 $3+5=8$。"},
        {"q": "一圓的直徑為 10，則圓周長？", "options": ["$10\pi$", "$5\pi$", "$25\pi$", "$100\pi$"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "圓周長 = 直徑 $\times \pi$。"}
    ],
    "九上：三角形三心": [
        {"q": "「重心」是哪三線交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "重心分中線為 2:1。"},
        {"q": "「內心」到三角形哪裡距離相等？", "options": ["三邊", "三頂點", "三高", "重心"], "ans": 0, "diff": "中等", "type": "單選", "expl": "內心是內切圓圓心，到三邊等距 (半徑)。"},
        {"q": "「外心」到三角形哪裡距離相等？", "options": ["三頂點", "三邊", "三高", "重心"], "ans": 0, "diff": "中等", "type": "單選", "expl": "外心是外接圓圓心，到三頂點等距 (半徑)。"}
    ],
    "九下：二次函數": [
        {"q": "【圖解題】開口向上的拋物線，係數 a？", "options": ["正", "負", "0", "無法判斷"], "ans": 0, "diff": "簡單", "type": "單選", "svg": "parabola_visual", "expl": "a > 0 開口向上，有最小值。"},
        {"q": "函數 $y=(x-3)^2+5$ 的頂點？", "options": ["(3, 5)", "(-3, 5)", "(3, -5)", "(-3, -5)"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "頂點式 $(h, k)$。"},
        {"q": "拋物線 $y=x^2$ 向右平移 2 單位，新方程式？", "options": ["$y=(x-2)^2$", "$y=(x+2)^2$", "$y=x^2+2$", "$y=x^2-2$"], "ans": 0, "diff": "中等", "type": "單選", "expl": "左加右減 (x軸方向)。"},
        {"q": "二次函數與 x 軸有兩個交點，判別式 $b^2-4ac$？", "options": ["> 0", "= 0", "< 0", "無法判斷"], "ans": 0, "diff": "困難", "type": "單選", "expl": "判別式大於 0 代表有兩相異實根 (交點)。"}
    ],
    "九下：統計與機率": [
        {"q": "投擲一枚硬幣 3 次，恰好 1 正 2 反的機率？", "options": ["3/8", "1/8", "1/2", "1/4"], "ans": 0, "diff": "困難", "type": "單選", "expl": "(正反反, 反正反, 反反正) 共 3 種。全部 $2^3=8$ 種。機率 3/8。"},
        {"q": "盒中 3 紅 7 白球，抽中紅球機率？", "options": ["3/10", "7/10", "3/7", "1/2"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "紅 / 全部 = 3 / 10。"},
        {"q": "資料：10, 20, 20, 30, 40，眾數是？", "options": ["20", "30", "24", "10"], "ans": 0, "diff": "簡單", "type": "單選", "expl": "出現次數最多的數。"},
        {"q": "四分位距 (IQR) 是指？", "options": ["Q3 - Q1", "Q3 - Q2", "最大值 - 最小值", "平均數"], "ans": 0, "diff": "中等", "type": "單選", "expl": "第三四分位數減第一四分位數。"}
    ]
}

# ==========================================
# 3. APP 主程式邏輯 (隨機抽題系統)
# ==========================================
def reset_exam():
    """切換單元時重置狀態"""
    st.session_state.exam_started = False
    st.session_state.current_questions = []
    st.session_state.exam_results = {}
    st.session_state.exam_finished = False

def main():
    st.set_page_config(page_title="國中數學：海量題庫無限刷題版", page_icon="🚀", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🚀 數學無限刷題")
    st.sidebar.caption("針對 108 課綱弱點擊破")
    
    # 選單
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)
    
    st.title("🚀 國中數學：海量題庫版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    # 考試首頁
    if not st.session_state.exam_started:
        st.info("💡 本系統採用「隨機抽題」模式，每次測驗會從題庫中隨機抽出 10 題。")
        st.write("請多刷幾次，確保所有題型都練習到！")
        
        if st.button("🎲 隨機抽題開始", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            
            # 從題庫載入
            all_questions = MATH_DB.get(selected_unit, [])
            
            # 隨機抽 10 題 (如果題目少於 10 則全取)
            num_to_pick = min(len(all_questions), 10)
            if num_to_pick == 0:
                st.error("此單元暫無題目")
            else:
                selected_q = random.sample(all_questions, num_to_pick)
                st.session_state.current_questions = selected_q
                st.session_state.exam_started = True
                st.rerun()

    # 考試進行中
    else:
        # 進度條
        total_q = len(st.session_state.current_questions)
        st.progress(0, text=f"共 {total_q} 題")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                
                # 顯示 SVG
                if "svg" in q and q["svg"] in SVG_ASSETS:
                    st.markdown(SVG_ASSETS[q["svg"]], unsafe_allow_html=True)
                    st.caption("👆 請參考圖形")
                
                # 顯示題目
                st.markdown(f"### {q['q']}")
                st.radio("選項", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                st.divider()

            # 交卷
            if st.form_submit_button("✅ 交卷看成績", use_container_width=True):
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

        # 結果頁面
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
                with st.expander(f"第 {i+1} 題詳解 ({'✅' if item['is_correct'] else '❌'})"):
                    if "svg" in q_data and q_data["svg"] in SVG_ASSETS:
                         st.markdown(SVG_ASSETS[q_data["svg"]], unsafe_allow_html=True)
                    st.write(f"**題目**：{q_data['q']}")
                    st.write(f"**正解**：{item['correct']}")
                    st.markdown(f"**💡 解析**：")
                    st.latex(q_data['expl'])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 再刷一次 (題目會變)", use_container_width=True):
                    # 重新隨機抽題
                    all_questions = MATH_DB.get(selected_unit, [])
                    num_to_pick = min(len(all_questions), 10)
                    st.session_state.current_questions = random.sample(all_questions, num_to_pick)
                    st.session_state.exam_finished = False
                    st.session_state.exam_results = {}
                    st.rerun()
            with col2:
                if st.button("⬅️ 換單元", use_container_width=True):
                    reset_exam()
                    st.rerun()

if __name__ == "__main__":
    main()
