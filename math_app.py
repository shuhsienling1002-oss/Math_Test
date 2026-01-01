import streamlit as st
import random

# ==========================================
# 1. 視覺繪圖引擎 (SVG Generator)
# ==========================================
class SVGGenerator:
    @staticmethod
    def _base_svg(content, width=300, height=200):
        return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{content}</svg>'

    @staticmethod
    def coordinate_point(x, y, label="P"):
        cx, cy = 150 + (x * 25), 150 - (y * 25)
        return SVGGenerator._base_svg(f"""
            <defs><pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#eee" stroke-width="1"/></pattern></defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            <line x1="150" y1="0" x2="150" y2="300" stroke="black" stroke-width="2"/>
            <line x1="0" y1="150" x2="300" y2="150" stroke="black" stroke-width="2"/>
            <circle cx="{cx}" cy="{cy}" r="6" fill="red" stroke="white" stroke-width="2"/>
            <text x="{cx+10}" y="{cy-10}" fill="red" font-weight="bold">{label}({x},{y})</text>
        """, 300, 300)

    @staticmethod
    def number_line(p1, p2):
        x1, x2 = 150 + (p1 * 25), 150 + (p2 * 25)
        dist, mid = abs(p2 - p1), (x1 + x2) / 2
        return SVGGenerator._base_svg(f"""
            <line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2"/>
            <line x1="150" y1="45" x2="150" y2="55" stroke="black" stroke-width="2"/><text x="150" y="75" text-anchor="middle">0</text>
            <circle cx="{x1}" cy="50" r="5" fill="blue"/><text x="{x1}" y="35" text-anchor="middle" fill="blue">{p1}</text>
            <circle cx="{x2}" cy="50" r="5" fill="red"/><text x="{x2}" y="35" text-anchor="middle" fill="red">{p2}</text>
            <path d="M{x1},50 Q{mid},{50-dist*4} {x2},50" stroke="purple" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
            <text x="{mid}" y="{40-dist*2}" text-anchor="middle" fill="purple" font-weight="bold">距離={dist}</text>
        """, 300, 100)

    @staticmethod
    def triangle_label(a, b, c="?"):
        return SVGGenerator._base_svg(f"""
            <path d="M40,140 L200,140 L40,20 Z" fill="#e3f2fd" stroke="blue" stroke-width="3"/>
            <rect x="40" y="120" width="20" height="20" fill="none" stroke="blue"/>
            <text x="120" y="160" text-anchor="middle">底={a}</text>
            <text x="25" y="90" text-anchor="end">高={b}</text>
            <text x="130" y="70" text-anchor="start" fill="red" font-weight="bold">斜邊={c}</text>
        """, 250, 180)

    @staticmethod
    def linear_func(m, k):
        coords = 'x1="50" y1="250" x2="250" y2="50"' if m > 0 else 'x1="50" y1="50" x2="250" y2="250"'
        desc = "斜率 > 0" if m > 0 else "斜率 < 0"
        return SVGGenerator._base_svg(f"""
            <line x1="150" y1="0" x2="150" y2="300" stroke="black"/><line x1="0" y1="150" x2="300" y2="150" stroke="black"/>
            <line {coords} stroke="blue" stroke-width="3"/><text x="150" y="280" text-anchor="middle" font-weight="bold">{desc}</text>
        """, 300, 300)

    @staticmethod
    def parabola(a, k):
        path = "M 50,50 Q 150,250 250,50" if a > 0 else "M 50,250 Q 150,50 250,250"
        desc = "開口向上" if a > 0 else "開口向下"
        return SVGGenerator._base_svg(f"""
            <line x1="150" y1="0" x2="150" y2="300" stroke="black"/><line x1="0" y1="150" x2="300" y2="150" stroke="black"/>
            <path d="{path}" stroke="red" stroke-width="2" fill="none"/>
            <text x="150" y="280" text-anchor="middle" font-weight="bold">{desc}</text>
        """, 300, 300)

    @staticmethod
    def geometry_sas():
        return SVGGenerator._base_svg("""
            <path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text>
            <path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text>
            <text x="115" y="80" text-anchor="middle" font-weight="bold" fill="blue">全等?</text>
        """, 300, 150)

    @staticmethod
    def triangle_center(type="centroid"):
        if type == "centroid": # 重心
            content = """<path d="M100,20 L20,180 L180,180 Z" fill="none" stroke="black" stroke-width="2"/><line x1="100" y1="20" x2="100" y2="180" stroke="red" stroke-dasharray="4"/><line x1="20" y1="180" x2="140" y2="100" stroke="red" stroke-dasharray="4"/><line x1="180" y1="180" x2="60" y2="100" stroke="red" stroke-dasharray="4"/><circle cx="100" cy="126" r="4" fill="blue"/><text x="110" y="126" fill="blue" font-weight="bold">G</text>"""
        elif type == "circumcenter": # 外心
            content = """<circle cx="100" cy="100" r="80" fill="none" stroke="green"/><path d="M100,20 L30,140 L170,140 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="100" cy="100" r="4" fill="green"/><text x="110" y="100" fill="green" font-weight="bold">O</text>"""
        elif type == "incenter": # 內心
            content = """<path d="M100,20 L20,180 L180,180 Z" fill="none" stroke="black" stroke-width="2"/><circle cx="100" cy="120" r="40" fill="none" stroke="orange"/><circle cx="100" cy="120" r="4" fill="orange"/><text x="110" y="120" fill="orange" font-weight="bold">I</text>"""
        return SVGGenerator._base_svg(content, 200, 200)

    @staticmethod
    def roots_on_line(r1, r2=None):
        map_x = lambda val: 150 + (val * 25)
        pts = f'<circle cx="{map_x(r1)}" cy="50" r="5" fill="red"/><text x="{map_x(r1)}" y="80" text-anchor="middle" fill="red">x={r1}</text>'
        if r2 is not None and r2 != r1:
            pts += f'<circle cx="{map_x(r2)}" cy="50" r="5" fill="red"/><text x="{map_x(r2)}" y="80" text-anchor="middle" fill="red">x={r2}</text>'
        return SVGGenerator._base_svg(f"""<line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2"/><line x1="150" y1="45" x2="150" y2="55" stroke="black"/><text x="150" y="40" text-anchor="middle">0</text>{pts}""", 300, 100)

    @staticmethod
    def area_model():
        return SVGGenerator._base_svg("""<rect x="50" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/><rect x="150" y="50" width="20" height="100" fill="#ffcdd2" stroke="black"/><rect x="50" y="150" width="100" height="20" fill="#ffcdd2" stroke="black"/><rect x="150" y="150" width="20" height="20" fill="#e1bee7" stroke="black"/><text x="100" y="100" text-anchor="middle">x²</text><text x="160" y="100" text-anchor="middle">ax</text><text x="100" y="165" text-anchor="middle">ax</text><text x="160" y="165" text-anchor="middle">a²</text>""", 250, 200)

# ==========================================
# 2. 暴力擴充題庫 (Massive Expanded DB)
# ==========================================
MATH_DB = {
    # ---------------- 3. 外心、內心與重心 ----------------
    "3-1 證明與推理": [
        {"q": "【圖解】若兩三角形三邊對應相等 (SSS)，則兩三角形關係為何？", "options": ["全等", "相似但不全等", "面積相等但不全等", "無關"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.geometry_sas(), "expl": "SSS (Side-Side-Side) 是全等性質。"},
        {"q": "下列哪一個條件「無法」確定兩個三角形全等？", "options": ["AAA", "SAS", "SSS", "AAS"], "ans": 0, "diff": "簡單", "expl": "AAA 只能保證相似（形狀一樣）。"},
        {"q": "在 $\\triangle ABC$ 中，若 $\\angle A > \\angle B$，則對邊關係？", "options": ["$\\overline{BC} > \\overline{AC}$", "$\\overline{BC} < \\overline{AC}$", "$\\overline{BC} = \\overline{AC}$", "無法判斷"], "ans": 0, "diff": "簡單", "expl": "大角對大邊性質。"},
        {"q": "四邊形中，兩雙對邊分別等長，則此四邊形必為？", "options": ["平行四邊形", "菱形", "梯形", "箏形"], "ans": 0, "diff": "中等", "expl": "兩雙對邊等長是平行四邊形的判別性質。"},
        {"q": "等腰三角形的「頂角平分線」，具有下列哪些性質？", "options": ["平分底邊且垂直底邊", "平分底邊但不垂直", "垂直底邊但不平分", "以上皆非"], "ans": 0, "diff": "中等", "expl": "等腰三角形三線合一。"},
        {"q": "兩三角形全等，下列何者「錯誤」？", "options": ["面積相等", "周長相等", "對應角相等", "角度一定要是60度"], "ans": 3, "diff": "簡單", "expl": "全等三角形角度對應相等，但不一定是60度。"},
        {"q": "直角三角形中，斜邊上的中線長度等於？", "options": ["斜邊長的一半", "斜邊長", "一股長", "兩股和"], "ans": 0, "diff": "中等", "expl": "直角三角形斜邊中點為外心，到三頂點等距。"},
        {"q": "若四邊形對角線互相平分，則此四邊形必為？", "options": ["平行四邊形", "梯形", "箏形", "任意四邊形"], "ans": 0, "diff": "中等", "expl": "對角線互相平分是平行四邊形的判別性質。"},
        {"q": "若四邊形對角線「互相垂直平分」，則它必為？", "options": ["菱形", "矩形", "等腰梯形", "箏形"], "ans": 0, "diff": "困難", "expl": "互相平分是平行四邊形，加上垂直則為菱形。"},
        {"q": "根據「外角定理」，三角形任一外角等於？", "options": ["不相鄰的兩內角和", "相鄰內角", "180度", "360度"], "ans": 0, "diff": "簡單", "expl": "外角等於不相鄰的兩內角和。"},
        {"q": "任意凸四邊形的內角和為幾度？", "options": ["360", "180", "540", "720"], "ans": 0, "diff": "簡單", "expl": "(4-2)*180 = 360。"},
        {"q": "下列何者是「RHS」全等性質的條件？", "options": ["直角、斜邊、一股", "三邊", "兩角一夾邊", "兩邊一夾角"], "ans": 0, "diff": "中等", "expl": "R(Right angle), H(Hypotenuse), S(Side)。"}
    ],
    "3-2 三角形的外心、內心與重心": [
        {"q": "【圖解】三角形的「重心」是哪三條線的交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_center("centroid"), "expl": "重心 (G) 是三條中線的交點。"},
        {"q": "【圖解】三角形的「外心」特徵為何？", "options": ["到三頂點等距", "到三邊等距", "平分面積", "三高交點"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_center("circumcenter"), "expl": "外心 (O) 到三頂點距離相等。"},
        {"q": "【圖解】三角形的「內心」特徵為何？", "options": ["到三邊等距", "到三頂點等距", "平分面積", "在外部"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_center("incenter"), "expl": "內心 (I) 到三邊垂直距離相等。"},
        {"q": "鈍角三角形的外心位置在？", "options": ["三角形外部", "三角形內部", "斜邊上", "頂點上"], "ans": 0, "diff": "中等", "expl": "銳角在內，直角在邊，鈍角在外。"},
        {"q": "【圖解】重心到頂點的距離，是重心到對邊中點距離的幾倍？", "options": ["2倍", "1.5倍", "3倍", "1倍"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_center("centroid"), "expl": "重心性質 2:1。"},
        {"q": "直角三角形兩股為 6, 8，則外接圓半徑 R 為？", "options": ["5", "10", "4", "3"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"), "expl": "斜邊 10，半徑 = 10/2 = 5。"},
        {"q": "正三角形的重心、外心、內心位置關係？", "options": ["重合 (同一點)", "在同一直線上", "形成三角形", "無關"], "ans": 0, "diff": "簡單", "expl": "正三角形三心合一。"},
        {"q": "若 I 為內心，且 $\\angle A = 70^\\circ$，則 $\\angle BIC = ？$", "options": ["$125^\\circ$", "$110^\\circ$", "$140^\\circ$", "$90^\\circ$"], "ans": 0, "diff": "困難", "expl": "$\\angle BIC = 90 + \\angle A/2 = 90 + 35 = 125$。"},
        {"q": "若 O 為外心，$\\angle BOC = 100^\\circ$，則 $\\angle A$ 可能為？", "options": ["50度或130度", "50度", "100度", "80度"], "ans": 0, "diff": "困難", "expl": "若 A 為銳角 50度，若為鈍角 130度。"},
        {"q": "重心將三角形面積切分成幾等份？", "options": ["6", "3", "4", "2"], "ans": 0, "diff": "簡單", "expl": "三中線將面積切成 6 塊相等。"},
        {"q": "等腰三角形的重心、外心、內心位置關係？", "options": ["在同一條直線上 (頂角平分線)", "重合", "形成三角形", "無關"], "ans": 0, "diff": "中等", "expl": "等腰三角形三心共線 (歐拉線)。"},
        {"q": "內切圓半徑 $r$、三角形面積 $A$、周長 $S$ 的關係式？", "options": ["$A = r \\times S / 2$", "$A = r \\times S$", "$A = r^2 \\times S$", "無關"], "ans": 0, "diff": "困難", "expl": "面積 = $\\frac{1}{2}r(a+b+c)$。"},
        {"q": "直角三角形兩股 5, 12，內切圓半徑 r 為？", "options": ["2", "1", "3", "2.5"], "ans": 0, "diff": "困難", "expl": "$r = (a+b-c)/2 = (5+12-13)/2 = 2$。"}
    ],

    # ---------------- 4. 一元二次方程式 ----------------
    "4-1 因式分解法": [
        {"q": "【圖解】解方程式 $(x-3)(x+4) = 0$ 的根？", "options": ["3 或 -4", "-3 或 4", "3 或 4", "-3 或 -4"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(3, -4), "expl": "$x-3=0$ 或 $x+4=0$。"},
        {"q": "方程式 $x^2 - 7x = 0$ 的解？", "options": ["0 或 7", "7", "0", "1 或 7"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(0, 7), "expl": "提公因式 $x(x-7)=0$。"},
        {"q": "若 $x=2$ 是 $x^2 - kx + 6 = 0$ 的根，k=？", "options": ["5", "-5", "3", "-3"], "ans": 0, "diff": "中等", "expl": "$4 - 2k + 6 = 0 \\Rightarrow 2k=10 \\Rightarrow k=5$。"},
        {"q": "解 $x^2 - 36 = 0$？", "options": ["6 或 -6", "6", "36", "1296"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(6, -6), "expl": "$x = \\pm 6$。"},
        {"q": "方程式 $(x-1)(x+2) = 4$ 的解？", "options": ["2 或 -3", "1 或 -2", "3 或 -2", "無解"], "ans": 0, "diff": "困難", "svg_gen": lambda: SVGGenerator.roots_on_line(2, -3), "expl": "$x^2+x-2=4 \\Rightarrow x^2+x-6=0 \\Rightarrow (x+3)(x-2)=0$。"},
        {"q": "解方程式 $2x^2 - 5x + 2 = 0$？", "options": ["2 或 1/2", "-2 或 -1/2", "2 或 -1/2", "無解"], "ans": 0, "diff": "中等", "expl": "十字交乘：$(2x-1)(x-2)=0$。"},
        {"q": "若兩根為 5, -3，則原方程式可能為？", "options": ["$(x-5)(x+3)=0$", "$(x+5)(x-3)=0$", "$x^2+2x-15=0$", "$x^2-15=0$"], "ans": 0, "diff": "中等", "expl": "逆推回去。"},
        {"q": "解 $x(x-5) = x$？", "options": ["0 或 6", "6", "0", "5"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.roots_on_line(0, 6), "expl": "移項：$x^2-5x-x=0 \\Rightarrow x^2-6x=0 \\Rightarrow x(x-6)=0$。"}
    ],
    "4-2 配方法與公式解": [
        {"q": "公式解中，判別式 D 等於？", "options": ["$b^2-4ac$", "$b^2+4ac$", "$2a$", "$b-4ac$"], "ans": 0, "diff": "簡單", "expl": "D = $b^2 - 4ac$。"},
        {"q": "判別方程式 $x^2 + x + 5 = 0$ 的解的情形？", "options": ["無解 (無實數解)", "相異兩根", "重根", "無法判斷"], "ans": 0, "diff": "中等", "expl": "$D = 1-20 < 0$。"},
        {"q": "【圖解】將 $x^2 + 8x$ 配方需加上？", "options": ["16", "8", "4", "64"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.area_model(), "expl": "加上 $(8/2)^2 = 16$。"},
        {"q": "解 $(x+2)^2 = 7$？", "options": ["$-2 \\pm \\sqrt{7}$", "$2 \\pm \\sqrt{7}$", "$\\pm \\sqrt{7}$", "5"], "ans": 0, "diff": "中等", "expl": "$x+2 = \\pm\\sqrt{7}$。"},
        {"q": "方程式 $x^2 - 4x + 4 = 0$ 判別式值？", "options": ["0", "4", "8", "-4"], "ans": 0, "diff": "簡單", "expl": "$16 - 16 = 0$ (重根)。"},
        {"q": "若方程式有重根，則判別式 D 的值？", "options": ["D = 0", "D > 0", "D < 0", "D = 1"], "ans": 0, "diff": "簡單", "expl": "D=0 時重根。"},
        {"q": "用公式解解 $x^2 - 3x - 1 = 0$？", "options": ["$\\frac{3 \\pm \\sqrt{13}}{2}$", "$\\frac{-3 \\pm \\sqrt{13}}{2}$", "$\\frac{3 \\pm \\sqrt{5}}{2}$", "無解"], "ans": 0, "diff": "困難", "expl": "$D = 9 - 4(1)(-1) = 13$。"},
        {"q": "若 $x^2 + 6x + k = 0$ 有重根，k=？", "options": ["9", "36", "6", "3"], "ans": 0, "diff": "中等", "expl": "$k = (6/2)^2 = 9$。"}
    ],
    "4-3 應用問題": [
        {"q": "兩連續正偶數的乘積為 48，求此兩數？", "options": ["6, 8", "4, 12", "8, 10", "-6, -8"], "ans": 0, "diff": "簡單", "expl": "$6 \\times 8 = 48$。"},
        {"q": "正方形面積 100，邊長增加 x 後變 144，求 x？", "options": ["2", "4", "12", "10"], "ans": 0, "diff": "中等", "expl": "原邊長 10，新邊長 12，故 x=2。"},
        {"q": "長方形長比寬多 3，面積 40，求寬？", "options": ["5", "8", "4", "10"], "ans": 0, "diff": "中等", "expl": "$5 \\times 8 = 40$。"},
        {"q": "某數的平方等於該數的 3 倍，求某數？", "options": ["0 或 3", "3", "0", "9"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.roots_on_line(0, 3), "expl": "$x^2 = 3x \\Rightarrow x(x-3)=0$。"},
        {"q": "物體落下距離 $h = 5t^2$，若 $h=125$，求時間 t？", "options": ["5", "25", "10", "15"], "ans": 0, "diff": "簡單", "expl": "$125 = 5t^2 \\Rightarrow t^2=25 \\Rightarrow t=5$。"},
        {"q": "一個數與其倒數之和為 2.5，求此數？", "options": ["2 或 0.5", "2", "0.5", "4"], "ans": 0, "diff": "困難", "expl": "$x + 1/x = 2.5 \\Rightarrow 2x^2 - 5x + 2 = 0$。"},
        {"q": "直角三角形兩股差 1，斜邊 5，求兩股和？", "options": ["7", "6", "5", "8"], "ans": 0, "diff": "中等", "expl": "3, 4, 5 三角形，3+4=7。"},
        {"q": "參加聚會每兩人握手一次，共握 66 次，求人數？", "options": ["12", "11", "13", "10"], "ans": 0, "diff": "困難", "expl": "$n(n-1)/2 = 66 \\Rightarrow n(n-1)=132 \\Rightarrow 12 \\times 11 = 132$。"}
    ],

    # ======= 其他年級 (總複習) =======
    "7上：整數與代數": [
        {"q": "【圖解】數線上 -5 到 3 的距離？", "options": ["8", "2", "-8", "-2"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.number_line(-5, 3), "expl": "距離 = 8。"},
        {"q": "計算 $(-15) + 8 - (-5)$？", "options": ["-2", "-12", "2", "-28"], "ans": 0, "diff": "簡單", "expl": "$-15 + 8 + 5 = -2$。"},
        {"q": "解 $3x - 5 = 10$？", "options": ["5", "15", "3", "1"], "ans": 0, "diff": "簡單", "expl": "$3x=15 \\Rightarrow x=5$。"}
    ],
    "7下：二元一次與坐標": [
        {"q": "【圖解】點 (-3, 4) 在第幾象限？", "options": ["二", "一", "三", "四"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.coordinate_point(-3, 4), "expl": "左上為第二象限。"},
        {"q": "解 $\\begin{cases} x+y=4 \\\\ x-y=2 \\end{cases}$，求 x？", "options": ["3", "1", "2", "4"], "ans": 0, "diff": "簡單", "expl": "$2x=6 \\Rightarrow x=3$。"}
    ],
    "8上：乘法公式與勾股": [
        {"q": "展開 $(x+3)^2$？", "options": ["$x^2+6x+9$", "$x^2+9$", "$x^2+3x+9$", "x^2+6x+6"], "ans": 0, "diff": "簡單", "expl": "和平方公式。"},
        {"q": "【圖解】直角三角形股為 6, 8，斜邊？", "options": ["10", "14", "12", "100"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"), "expl": "$\\sqrt{36+64} = 10$。"}
    ],
    "8下：數列與幾何": [
        {"q": "正三角形內角？", "options": ["60", "90", "45", "180"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_label("60", "60", "60"), "expl": "均為 60 度。"},
        {"q": "數列 1, 3, 5, 7 ... 第 10 項？", "options": ["19", "20", "21", "17"], "ans": 0, "diff": "簡單", "expl": "$1 + 9 \\times 2 = 19$。"}
    ],
    "9上：相似形與圓": [
        {"q": "邊長比 1:3，面積比？", "options": ["1:9", "1:3", "1:6", "3:1"], "ans": 0, "diff": "簡單", "expl": "平方比 1:9。"},
        {"q": "【圖解】半徑 5，弦心距 3，弦長？", "options": ["8", "4", "10", "6"], "ans": 0, "diff": "困難", "svg_gen": lambda: SVGGenerator.triangle_label("?", 3, 5), "expl": "半弦 4，全弦 8。"}
    ],
    "9下：二次函數與機率": [
        {"q": "【圖解】$y=x^2$ 開口？", "options": ["向上", "向下", "左", "右"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.parabola(1, 0), "expl": "係數正，開口向上。"},
        {"q": "【圖解】3 紅 2 白，抽紅機率？", "options": ["3/5", "2/5", "1/5", "1/2"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.probability_balls(3, 2), "expl": "3/5。"}
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
    st.set_page_config(page_title="國中數學：考前衝刺完全版", page_icon="🏆", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🏆 國中數學全攻略")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)
    st.sidebar.info("已大幅擴充「三心」與「一元二次方程式」題庫量！")

    st.title("🏆 國中數學：考前衝刺完全版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info(f"準備好挑戰 **{selected_unit}** 了嗎？")
        st.write(f"此單元包含 {len(MATH_DB[selected_unit])} 題精選題，系統將隨機抽出 10 題。")
        if st.button("🚀 開始測驗", use_container_width=True):
            st.session_state.exam_finished = False 
            st.session_state.exam_results = {} 
            all_questions = MATH_DB.get(selected_unit, [])
            num_to_pick = min(len(all_questions), 10)
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
                    st.caption("👆 視覺輔助圖")
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
            if final_score == 100: st.success(f"💯 滿分！太強了！")
            elif final_score >= 60: st.info(f"👍 及格！觀念正確！")
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
