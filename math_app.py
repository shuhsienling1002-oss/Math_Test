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
        """畫出全等性質示意圖"""
        return f"""<svg width="300" height="150" xmlns="http://www.w3.org/2000/svg"><path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text><path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text><text x="115" y="80" text-anchor="middle" font-weight="bold" fill="blue">全等?</text></svg>"""

    @staticmethod
    def triangle_centroid():
        """畫出重心示意圖 (中線交點)"""
        return f"""<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><path d="M100,20 L20,180 L180,180 Z" fill="none" stroke="black" stroke-width="2"/><line x1="100" y1="20" x2="100" y2="180" stroke="red" stroke-width="1" stroke-dasharray="4"/><line x1="20" y1="180" x2="140" y2="100" stroke="red" stroke-width="1" stroke-dasharray="4"/><line x1="180" y1="180" x2="60" y2="100" stroke="red" stroke-width="1" stroke-dasharray="4"/><circle cx="100" cy="126" r="4" fill="blue"/><text x="110" y="126" fill="blue" font-weight="bold">G (重心)</text></svg>"""

# ==========================================
# 2. 特化版題庫 (Expanded DB)
# ==========================================
MATH_DB = {
    # ================= 考前衝刺：第三章 三心 (九上) =================
    "【衝刺】3-1：證明與推理": [
        {"q": "下列哪一個條件「無法」確定兩個三角形全等？", "options": ["AAA", "SAS", "SSS", "AAS"], "ans": 0, "diff": "簡單", "expl": "AAA (三個角對應相等) 只能保證相似（形狀一樣），不能保證大小一樣（全等）。例如正三角形有大有小，但角度都是60度。"},
        {"q": "【圖解】參考圖形，若兩三角形三邊長對應相等，是根據何種性質全等？", "options": ["SSS", "SAS", "ASA", "RHS"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.geometry_sas(), "expl": "三邊對應相等，即 Side-Side-Side (SSS) 全等性質。"},
        {"q": "等腰三角形的「頂角平分線」，具有下列哪些性質？(多選概念)", "options": ["平分底邊且垂直底邊", "平分底邊但不垂直", "垂直底邊但不平分", "以上皆非"], "ans": 0, "diff": "中等", "expl": "等腰三角形性質：頂角平分線、底邊中線、底邊中垂線，三線合一。"},
        {"q": "若 $\\triangle ABC \\cong \\triangle DEF$，且 $\\angle A=60^\\circ, \\angle B=50^\\circ$，則 $\\angle F=$？", "options": ["70度", "60度", "50度", "180度"], "ans": 0, "diff": "簡單", "expl": "$\\angle C = 180 - 60 - 50 = 70$。因為對應角相等，$\\angle F = \\angle C = 70^\\circ$。"},
        {"q": "直角三角形中，斜邊上的中線長度等於？", "options": ["斜邊長的一半", "斜邊長", "一股長", "兩股和"], "ans": 0, "diff": "中等", "expl": "直角三角形外心在斜邊中點，故外接圓半徑 = 斜邊中線 = 斜邊/2。"},
        {"q": "在 $\\triangle ABC$ 中，若 $\\angle A > \\angle B$，則對邊長度關係為何？", "options": ["$\\overline{BC} > \\overline{AC}$", "$\\overline{BC} < \\overline{AC}$", "$\\overline{BC} = \\overline{AC}$", "無法判斷"], "ans": 0, "diff": "簡單", "expl": "大角對大邊性質。$\\angle A$ 的對邊是 $\\overline{BC}$，$\\angle B$ 的對邊是 $\\overline{AC}$。"},
        {"q": "四邊形中，兩雙對邊分別等長，則此四邊形必為？", "options": ["平行四邊形", "菱形", "梯形", "箏形"], "ans": 0, "diff": "中等", "expl": "兩雙對邊等長是平行四邊形的判別性質之一。"},
        {"q": "關於「外角定理」：三角形任一外角，等於？", "options": ["兩內對角之和", "兩內對角之差", "相鄰內角", "180度"], "ans": 0, "diff": "簡單", "expl": "外角等於不相鄰的兩個內角和。"}
    ],
    "【衝刺】3-2：三角形的外心、內心與重心": [
        {"q": "【圖解】三角形的「重心」是哪三條線的交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_centroid(), "expl": "重心 (G) 是三條中線的交點。"},
        {"q": "三角形的「外心」到哪裡等距離？", "options": ["三頂點", "三邊", "重心", "垂心"], "ans": 0, "diff": "中等", "expl": "外心是外接圓圓心，半徑相等，故到三個頂點距離相等 (OA=OB=OC)。"},
        {"q": "三角形的「內心」到哪裡等距離？", "options": ["三邊", "三頂點", "重心", "垂心"], "ans": 0, "diff": "中等", "expl": "內心是內切圓圓心，半徑相等，故到三邊的垂直距離相等。"},
        {"q": "鈍角三角形的外心位置在？", "options": ["三角形外部", "三角形內部", "斜邊上", "頂點上"], "ans": 0, "diff": "中等", "expl": "口訣：銳角在內，直角在邊(斜邊中點)，鈍角在外。"},
        {"q": "【圖解】重心到頂點的距離，是重心到對邊中點距離的幾倍？", "options": ["2倍", "1.5倍", "3倍", "1倍"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_centroid(), "expl": "重心性質：頂點到重心 : 重心到中點 = 2 : 1。"},
        {"q": "直角三角形兩股為 6, 8，則外接圓半徑 R 為？", "options": ["5", "10", "4", "3"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"), "expl": "斜邊 = $\\sqrt{6^2+8^2}=10$。外心在斜邊中點，故半徑 $R = 10/2 = 5$。"},
        {"q": "正三角形的重心、外心、內心位置關係？", "options": ["重合 (同一點)", "在同一直線上", "形成三角形", "無關"], "ans": 0, "diff": "簡單", "expl": "正三角形非常完美，四心(含垂心)合一。"},
        {"q": "若 I 為 $\\triangle ABC$ 的內心，且 $\\angle A = 70^\\circ$，則 $\\angle BIC = ？$", "options": ["$125^\\circ$", "$110^\\circ$", "$140^\\circ$", "$90^\\circ$"], "ans": 0, "diff": "困難", "expl": "內心角度公式：$\\angle BIC = 90^\\circ + \\frac{1}{2}\\angle A = 90 + 35 = 125^\\circ$。"},
        {"q": "重心將三角形面積切分成幾等份？", "options": ["6", "3", "4", "2"], "ans": 0, "diff": "簡單", "expl": "三中線將面積切成 6 塊面積相等的小三角形。"},
        {"q": "若 O 為 $\\triangle ABC$ 外心，$\\angle BOC = 100^\\circ$，則 $\\angle A$ 可能為？", "options": ["50度或130度", "50度", "100度", "80度"], "ans": 0, "diff": "困難", "expl": "若 A 在優弧上，$\\angle A = \\frac{1}{2} \\angle BOC = 50^\\circ$。若 A 在劣弧上(鈍角)，$\\angle A = 180 - 50 = 130^\\circ$。"}
    ],

    # ================= 考前衝刺：第四章 一元二次方程式 (八上) =================
    "【衝刺】4-1：因式分解法解方程式": [
        {"q": "解方程式 $(x-3)(x+4) = 0$ 的根？", "options": ["3 或 -4", "-3 或 4", "3 或 4", "-3 或 -4"], "ans": 0, "diff": "簡單", "expl": "兩數相乘為0，必有一數為0。$x-3=0 \\Rightarrow x=3$；$x+4=0 \\Rightarrow x=-4$。"},
        {"q": "方程式 $x^2 - 7x = 0$ 的解？", "options": ["0 或 7", "7", "0", "1 或 7"], "ans": 0, "diff": "簡單", "expl": "提公因式 x：$x(x-7)=0$，故 $x=0$ 或 $x=7$。"},
        {"q": "若 $x=2$ 是方程式 $x^2 - kx + 6 = 0$ 的一根，則 k = ？", "options": ["5", "-5", "3", "-3"], "ans": 0, "diff": "中等", "expl": "將 $x=2$ 代入：$4 - 2k + 6 = 0 \\Rightarrow 10 = 2k \\Rightarrow k = 5$。"},
        {"q": "解 $x^2 - 25 = 0$？", "options": ["5 或 -5", "5", "25", "625"], "ans": 0, "diff": "簡單", "expl": "平方差分解 $(x+5)(x-5)=0$，或直接移項開根號。"},
        {"q": "解方程式 $x^2 - 10x + 25 = 0$？", "options": ["5 (重根)", "-5 (重根)", "5 或 -5", "25"], "ans": 0, "diff": "中等", "expl": "完全平方式：$(x-5)^2 = 0 \\Rightarrow x = 5$ (重根)。"},
        {"q": "方程式 $(x-1)(x+2) = 4$ 的解？", "options": ["2 或 -3", "1 或 -2", "3 或 -2", "無解"], "ans": 0, "diff": "困難", "expl": "陷阱題！不能直接看括號。需展開整理：$x^2+x-2=4 \\Rightarrow x^2+x-6=0 \\Rightarrow (x+3)(x-2)=0$，解為 -3, 2。"},
        {"q": "若兩根為 3, -2，則原方程式可能為？", "options": ["$(x-3)(x+2)=0$", "$(x+3)(x-2)=0$", "$x^2+x-6=0$", "$x^2-6=0$"], "ans": 0, "diff": "中等", "expl": "逆推回去：$(x-3)(x+2)=0$。"}
    ],
    "【衝刺】4-2：配方法與公式解": [
        {"q": "一元二次方程式 $ax^2 + bx + c = 0$ 的公式解為？", "options": ["$\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$", "$\\frac{-b \\pm \\sqrt{b^2+4ac}}{2a}$", "$\\frac{b \\pm \\sqrt{b^2-4ac}}{2a}$", "$\\frac{-b \\pm \\sqrt{b^2-4ac}}{a}$"], "ans": 0, "diff": "簡單", "expl": "這是必背公式！根號內為判別式 $D = b^2-4ac$。"},
        {"q": "判別方程式 $x^2 + x + 5 = 0$ 的解的情形？", "options": ["無解 (無實數解)", "相異兩根", "重根", "無法判斷"], "ans": 0, "diff": "中等", "expl": "判別式 $D = b^2 - 4ac = 1^2 - 4(1)(5) = 1 - 20 = -19 < 0$，故無實數解。"},
        {"q": "若要將 $x^2 + 8x$ 配成完全平方式，需加上多少？", "options": ["16", "8", "4", "64"], "ans": 0, "diff": "簡單", "expl": "加上中間項係數一半的平方：$(8/2)^2 = 4^2 = 16$。"},
        {"q": "解 $(x+2)^2 = 7$？", "options": ["$-2 \\pm \\sqrt{7}$", "$2 \\pm \\sqrt{7}$", "$\\pm \\sqrt{7}$", "5"], "ans": 0, "diff": "中等", "expl": "直接開根號：$x+2 = \\pm\\sqrt{7} \\Rightarrow x = -2 \\pm \\sqrt{7}$。"},
        {"q": "方程式 $x^2 - 4x + 4 = 0$ 的判別式值為？", "options": ["0", "4", "8", "-4"], "ans": 0, "diff": "簡單", "expl": "$D = (-4)^2 - 4(1)(4) = 16 - 16 = 0$ (重根)。"},
        {"q": "若方程式有重根，則判別式 D 的值？", "options": ["D = 0", "D > 0", "D < 0", "D = 1"], "ans": 0, "diff": "簡單", "expl": "D=0 重根；D>0 相異兩根；D<0 無解。"},
        {"q": "利用公式解解 $2x^2 - 3x - 1 = 0$？", "options": ["$\\frac{3 \\pm \\sqrt{17}}{4}$", "$\\frac{-3 \\pm \\sqrt{17}}{4}$", "$\\frac{3 \\pm \\sqrt{13}}{4}$", "無解"], "ans": 0, "diff": "困難", "expl": "$a=2, b=-3, c=-1$。$x = \\frac{-(-3) \\pm \\sqrt{(-3)^2 - 4(2)(-1)}}{2(2)} = \\frac{3 \\pm \\sqrt{9+8}}{4} = \\frac{3 \\pm \\sqrt{17}}{4}$。"}
    ],
    "【衝刺】4-3：應用問題": [
        {"q": "兩連續正偶數的乘積為 48，求此兩數？", "options": ["6, 8", "4, 12", "8, 10", "-6, -8"], "ans": 0, "diff": "簡單", "expl": "設小數為 $x$，大數 $x+2$。$x(x+2)=48$。驗算 $6 \\times 8 = 48$。"},
        {"q": "正方形面積為 100 平方公分，邊長增加 x 後面積變為 144，求 x？", "options": ["2", "4", "12", "10"], "ans": 0, "diff": "中等", "expl": "原邊長 $\\sqrt{100}=10$。新面積 144 邊長為 12。$10+x=12 \\Rightarrow x=2$。"},
        {"q": "長方形長比寬多 3，面積 40，求寬？", "options": ["5", "8", "4", "10"], "ans": 0, "diff": "中等", "expl": "設寬 $x$，長 $x+3$。$x(x+3)=40 \\Rightarrow x^2+3x-40=0 \\Rightarrow (x+8)(x-5)=0$。邊長取正，$x=5$。"},
        {"q": "某數的平方等於該數的 3 倍，求某數？", "options": ["0 或 3", "3", "0", "9"], "ans": 0, "diff": "中等", "expl": "$x^2 = 3x \\Rightarrow x^2 - 3x = 0 \\Rightarrow x(x-3)=0$，故 0 或 3。"},
        {"q": "一個梯形上底 x，下底 x+2，高 4，面積 20，求 x？", "options": ["4", "3", "5", "6"], "ans": 0, "diff": "中等", "expl": "面積公式：$\\frac{(x + x+2) \\times 4}{2} = 20 \\Rightarrow (2x+2) \\times 2 = 20 \\Rightarrow 4x+4=20 \\Rightarrow 4x=16 \\Rightarrow x=4$。"},
        {"q": "一物體從高空落下，距離 $h = 5t^2$，若落下距離為 125 公尺，需幾秒？", "options": ["5", "25", "10", "15"], "ans": 0, "diff": "簡單", "expl": "$125 = 5t^2 \\Rightarrow t^2 = 25 \\Rightarrow t=5$ (時間取正)。"}
    ],

    # ======= 其他單元 (保留供總複習) =======
    "國一：整數與代數": [
        {"q": "【圖解】數線上 -5 到 3 的距離？", "options": ["8", "2", "-8", "-2"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.number_line(-5, 3), "expl": "距離 = 大數 - 小數 = $3 - (-5) = 8$。"},
        {"q": "計算 $(-15) + 8 - (-5)$ 的值？", "options": ["-2", "-12", "2", "-28"], "ans": 0, "diff": "簡單", "expl": "$-15 + 8 + 5 = -2$。"},
        {"q": "解 $3x - 5 = 10$？", "options": ["5", "15", "3", "1"], "ans": 0, "diff": "簡單", "expl": "$3x=15 \\Rightarrow x=5$。"}
    ],
    "國二：乘法公式與數列": [
        {"q": "展開 $(x+3)^2$？", "options": ["$x^2+6x+9$", "$x^2+9$", "$x^2+3x+9$", "$x^2+6x+6$"], "ans": 0, "diff": "簡單", "expl": "$a^2+2ab+b^2$。"},
        {"q": "數列 1, 3, 5, 7 ... 第 10 項？", "options": ["19", "20", "21", "17"], "ans": 0, "diff": "簡單", "expl": "$1 + 9 \\times 2 = 19$。"}
    ],
    "國三：幾何證明與統計": [
        {"q": "【圖解】參考圖形，若邊長放大 2 倍，面積放大幾倍？", "options": ["4倍", "2倍", "8倍", "不變"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.geometry_sas(), "expl": "面積比是邊長比的平方 ($2^2=4$)。"},
        {"q": "投擲硬幣 3 次，出現「三正」的機率？", "options": ["1/8", "1/2", "3/8", "1/4"], "ans": 0, "diff": "中等", "expl": "$(1/2)^3 = 1/8$。"}
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
    st.sidebar.info("針對「一元二次方程式」與「三角形三心」進行細分與題庫擴充。")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)
    
    st.title("💯 國中數學：考前衝刺特化版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info(f"準備練習：**{selected_unit}**")
        st.write("系統將隨機抽出題目進行測驗，請多刷幾次！")
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
        st.progress(0, text=f"題目：{total_q} 題")

        with st.form("math_exam_form"):
            questions = st.session_state.current_questions
            for idx, q in enumerate(questions):
                st.markdown(f"**第 {idx+1} 題：**")
                if q.get("svg_gen"):
                    st.markdown(q["svg_gen"](), unsafe_allow_html=True)
                    st.caption("👆 請參考圖形作答")
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
