import streamlit as st
import random

# ==========================================
# 1. 視覺繪圖引擎 (SVG Generator) - V8.0 最強版
# ==========================================
class SVGGenerator:
    @staticmethod
    def _base_svg(content, width=300, height=200):
        return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="white"/>{content}</svg>'

    @staticmethod
    def coordinate_point(x, y, label="P"):
        """直角坐標點"""
        cx, cy = 150 + (x * 25), 150 - (y * 25)
        return SVGGenerator._base_svg(f"""
            <defs><pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#eee" stroke-width="1"/></pattern></defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            <line x1="150" y1="0" x2="150" y2="300" stroke="black" stroke-width="2"/>
            <line x1="0" y1="150" x2="300" y2="150" stroke="black" stroke-width="2"/>
            <text x="285" y="145" font-weight="bold">x</text><text x="155" y="15" font-weight="bold">y</text>
            <circle cx="{cx}" cy="{cy}" r="6" fill="red" stroke="white" stroke-width="2"/>
            <text x="{cx+10}" y="{cy-10}" fill="red" font-weight="bold">{label}({x},{y})</text>
        """, 300, 300)

    @staticmethod
    def number_line(p1, p2):
        """數線距離"""
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
    def probability_balls(red, white, green=0):
        """機率球"""
        balls = ""
        sx = 40
        for _ in range(red): balls += f'<circle cx="{sx}" cy="40" r="12" fill="#ff4444" stroke="black"/><text x="{sx}" y="44" text-anchor="middle" fill="white" font-size="10">紅</text>'; sx += 30
        for _ in range(white): balls += f'<circle cx="{sx}" cy="40" r="12" fill="white" stroke="black"/><text x="{sx}" y="44" text-anchor="middle" fill="black" font-size="10">白</text>'; sx += 30
        for _ in range(green): balls += f'<circle cx="{sx}" cy="40" r="12" fill="#44ff44" stroke="black"/><text x="{sx}" y="44" text-anchor="middle" fill="black" font-size="10">綠</text>'; sx += 30
        return SVGGenerator._base_svg(f'<rect width="100%" height="100%" fill="#eee" rx="10"/>{balls}', 400, 80)

    @staticmethod
    def triangle_label(a, b, c="?"):
        """直角三角形"""
        return SVGGenerator._base_svg(f"""
            <path d="M40,140 L200,140 L40,20 Z" fill="#e3f2fd" stroke="blue" stroke-width="3"/>
            <rect x="40" y="120" width="20" height="20" fill="none" stroke="blue"/>
            <text x="120" y="160" text-anchor="middle">底={a}</text>
            <text x="25" y="90" text-anchor="end">高={b}</text>
            <text x="130" y="70" text-anchor="start" fill="red" font-weight="bold">斜邊={c}</text>
        """, 250, 180)

    @staticmethod
    def linear_func(m, k):
        """一次函數"""
        coords = 'x1="50" y1="250" x2="250" y2="50"' if m > 0 else 'x1="50" y1="50" x2="250" y2="250"' if m < 0 else 'x1="20" y1="150" x2="280" y2="150"'
        desc = "斜率 > 0 (右上)" if m > 0 else "斜率 < 0 (左上)" if m < 0 else "水平線"
        return SVGGenerator._base_svg(f"""
            <line x1="150" y1="0" x2="150" y2="300" stroke="black"/><line x1="0" y1="150" x2="300" y2="150" stroke="black"/>
            <line {coords} stroke="blue" stroke-width="3"/><text x="150" y="280" text-anchor="middle" font-weight="bold">{desc}</text>
        """, 300, 300)

    @staticmethod
    def parabola(a, k):
        """二次函數"""
        path = "M 50,50 Q 150,250 250,50" if a > 0 else "M 50,250 Q 150,50 250,250"
        desc = "開口向上" if a > 0 else "開口向下"
        return SVGGenerator._base_svg(f"""
            <line x1="150" y1="0" x2="150" y2="300" stroke="black"/><line x1="0" y1="150" x2="300" y2="150" stroke="black"/>
            <path d="{path}" stroke="red" stroke-width="2" fill="none"/>
            <circle cx="150" cy="150" r="4" fill="blue"/><text x="160" y="150" fill="blue" font-size="10">頂點</text>
            <text x="150" y="280" text-anchor="middle" font-weight="bold">{desc}</text>
        """, 300, 300)

    @staticmethod
    def geometry_sas():
        """SSS/SAS 全等示意"""
        return SVGGenerator._base_svg("""
            <path d="M20,120 L80,120 L50,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="50" y="140" text-anchor="middle">A</text>
            <path d="M150,120 L210,120 L180,40 Z" fill="none" stroke="black" stroke-width="2"/><text x="180" y="140" text-anchor="middle">B</text>
            <text x="115" y="80" text-anchor="middle" font-weight="bold" fill="blue">全等?</text>
        """, 300, 150)

    @staticmethod
    def triangle_center(type="centroid"):
        """三心繪圖整合"""
        if type == "centroid": # 重心
            content = """
                <path d="M100,20 L20,180 L180,180 Z" fill="none" stroke="black" stroke-width="2"/>
                <line x1="100" y1="20" x2="100" y2="180" stroke="red" stroke-dasharray="4"/>
                <line x1="20" y1="180" x2="140" y2="100" stroke="red" stroke-dasharray="4"/>
                <line x1="180" y1="180" x2="60" y2="100" stroke="red" stroke-dasharray="4"/>
                <circle cx="100" cy="126" r="4" fill="blue"/><text x="110" y="126" fill="blue" font-weight="bold">G</text>
            """
        elif type == "circumcenter": # 外心
            content = """
                <circle cx="100" cy="100" r="80" fill="none" stroke="green"/>
                <path d="M100,20 L30,140 L170,140 Z" fill="none" stroke="black" stroke-width="2"/>
                <circle cx="100" cy="100" r="4" fill="green"/><text x="110" y="100" fill="green" font-weight="bold">O</text>
            """
        elif type == "incenter": # 內心
            content = """
                <path d="M100,20 L20,180 L180,180 Z" fill="none" stroke="black" stroke-width="2"/>
                <circle cx="100" cy="120" r="40" fill="none" stroke="orange"/>
                <circle cx="100" cy="120" r="4" fill="orange"/><text x="110" y="120" fill="orange" font-weight="bold">I</text>
            """
        return SVGGenerator._base_svg(content, 200, 200)

    @staticmethod
    def roots_on_line(r1, r2=None):
        """數線解"""
        map_x = lambda val: 150 + (val * 25)
        pts = f'<circle cx="{map_x(r1)}" cy="50" r="5" fill="red"/><text x="{map_x(r1)}" y="80" text-anchor="middle" fill="red">x={r1}</text>'
        if r2 is not None and r2 != r1:
            pts += f'<circle cx="{map_x(r2)}" cy="50" r="5" fill="red"/><text x="{map_x(r2)}" y="80" text-anchor="middle" fill="red">x={r2}</text>'
        return SVGGenerator._base_svg(f"""
            <line x1="20" y1="50" x2="280" y2="50" stroke="black" stroke-width="2"/>
            <line x1="150" y1="45" x2="150" y2="55" stroke="black"/><text x="150" y="40" text-anchor="middle">0</text>
            {pts}
        """, 300, 100)

    @staticmethod
    def area_model():
        """配方法面積"""
        return SVGGenerator._base_svg("""
            <rect x="50" y="50" width="100" height="100" fill="#bbdefb" stroke="black"/>
            <rect x="150" y="50" width="20" height="100" fill="#ffcdd2" stroke="black"/>
            <rect x="50" y="150" width="100" height="20" fill="#ffcdd2" stroke="black"/>
            <rect x="150" y="150" width="20" height="20" fill="#e1bee7" stroke="black"/>
            <text x="100" y="100" text-anchor="middle">x²</text>
            <text x="160" y="100" text-anchor="middle">ax</text>
            <text x="100" y="165" text-anchor="middle">ax</text>
            <text x="160" y="165" text-anchor="middle">a²</text>
        """, 250, 200)

# ==========================================
# 2. 終極完整題庫 (包含所有章節)
# ==========================================
MATH_DB = {
    # ======= 七年級 =======
    "7上：整數運算": [
        {"q": "【圖解】數線上 -5 到 3 的距離？", "options": ["8", "2", "-8", "-2"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.number_line(-5, 3), "expl": "距離 = 8。"},
        {"q": "計算 $(-8) + 12 + (-5)$？", "options": ["-1", "1", "25", "-25"], "ans": 0, "diff": "簡單", "expl": "4 + (-5) = -1。"},
        {"q": "【圖解】若 $|a|=5$，a 位於原點左方，則 a=？", "options": ["-5", "5", "0", "25"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.number_line(-5, 0), "expl": "左方為負，故 -5。"}
    ],
    "7上：分數與指數": [
        {"q": "計算 $1/2 - 2/3$？", "options": ["-1/6", "1/6", "-1", "1"], "ans": 0, "diff": "簡單", "expl": "3/6 - 4/6 = -1/6。"},
        {"q": "科學記號 $3.5 \\times 10^{-4}$ 小數點後第幾位不為 0？", "options": ["4", "3", "5", "10"], "ans": 0, "diff": "中等", "expl": "指數為 -4，故第 4 位。"}
    ],
    "7上：一元一次方程式": [
        {"q": "解 $3x - 5 = 10$？", "options": ["5", "15", "3", "5/3"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(5), "expl": "3x = 15 => x = 5。"},
        {"q": "甲比乙大 10 歲，和為 50，求乙？", "options": ["20", "30", "15", "25"], "ans": 0, "diff": "中等", "expl": "2x+10=50 => 2x=40 => x=20。"}
    ],
    "7下：二元一次聯立方程式": [
        {"q": "解 $\\begin{cases} x+y=4 \\\\ x-y=2 \\end{cases}$，求 x？", "options": ["3", "1", "2", "4"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(3), "expl": "2x=6 => x=3。"}
    ],
    "7下：直角坐標": [
        {"q": "【圖解】點 (-3, 4) 在第幾象限？", "options": ["二", "一", "三", "四"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.coordinate_point(-3, 4), "expl": "左上為第二象限。"},
        {"q": "【圖解】直線 $y = -2x + 1$ 的圖形走勢？", "options": ["左上右下", "右上左下", "水平", "垂直"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.linear_func(-2, 1), "expl": "斜率負，左上右下。"}
    ],

    # ======= 八年級 =======
    "8上：乘法公式": [
        {"q": "展開 $(x+3)^2$？", "options": ["$x^2+6x+9$", "$x^2+9$", "$x^2+3x+9$", "x^2+6x+6"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.area_model(), "expl": "和平方公式。"},
        {"q": "計算 $102 \\times 98$？", "options": ["9996", "10004", "9999", "10000"], "ans": 0, "diff": "中等", "expl": "$(100+2)(100-2) = 10000-4$。"}
    ],
    "8上：平方根與畢氏定理": [
        {"q": "【圖解】直角三角形股為 6, 8，斜邊？", "options": ["10", "14", "12", "100"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"), "expl": "$\\sqrt{36+64} = 10$。"},
        {"q": "計算 $\\sqrt{12}$？", "options": ["$2\\sqrt{3}$", "$3\\sqrt{2}$", "6", "4"], "ans": 0, "diff": "簡單", "expl": "$\\sqrt{4 \\times 3} = 2\\sqrt{3}$。"}
    ],
    "8上：因式分解": [
        {"q": "分解 $x^2 - 16$？", "options": ["$(x+4)(x-4)$", "$(x-4)^2$", "$(x+4)^2$", "無法分解"], "ans": 0, "diff": "簡單", "expl": "平方差公式。"}
    ],
    # --- [考前特化] 4. 一元二次方程式 ---
    "4-1 因式分解法": [
        {"q": "【圖解】解 $(x-3)(x+4)=0$？", "options": ["3 或 -4", "-3 或 4", "3 或 4", "-3 或 -4"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(3, -4), "expl": "x=3 或 x=-4。"},
        {"q": "解 $x^2 - 7x = 0$？", "options": ["0 或 7", "7", "0", "1 或 7"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(0, 7), "expl": "x(x-7)=0。"},
        {"q": "若 x=2 是 $x^2 - kx + 6 = 0$ 的根，k=？", "options": ["5", "-5", "3", "-3"], "ans": 0, "diff": "中等", "expl": "4 - 2k + 6 = 0 => k=5。"},
        {"q": "解 $x^2 - 25 = 0$？", "options": ["5 或 -5", "5", "25", "625"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(5, -5), "expl": "x = ±5。"},
        {"q": "解 $(x-1)(x+2)=4$？", "options": ["2 或 -3", "1 或 -2", "3 或 -2", "無解"], "ans": 0, "diff": "困難", "svg_gen": lambda: SVGGenerator.roots_on_line(2, -3), "expl": "$x^2+x-6=0$ => (x+3)(x-2)=0。"}
    ],
    "4-2 配方法與公式解": [
        {"q": "公式解判別式 D = ？", "options": ["$b^2-4ac$", "$b^2+4ac$", "$2a$", "$b-4ac$"], "ans": 0, "diff": "簡單", "expl": "D = b^2 - 4ac。"},
        {"q": "若 $x^2 + x + 5 = 0$，解的情形？", "options": ["無解", "相異兩根", "重根", "無法判斷"], "ans": 0, "diff": "中等", "expl": "D = 1 - 20 = -19 < 0，無實根。"},
        {"q": "【圖解】將 $x^2 + 8x$ 配方需加上？", "options": ["16", "8", "4", "64"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.area_model(), "expl": "加上 $(8/2)^2 = 16$。"},
        {"q": "解 $(x+2)^2 = 7$？", "options": ["$-2 \\pm \\sqrt{7}$", "$2 \\pm \\sqrt{7}$", "$\\pm \\sqrt{7}$", "5"], "ans": 0, "diff": "中等", "expl": "$x = -2 \\pm \\sqrt{7}$。"},
        {"q": "方程式 $x^2 - 4x + 4 = 0$ 判別式值？", "options": ["0", "4", "8", "-4"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.roots_on_line(2), "expl": "D=0，重根。"}
    ],
    "4-3 應用問題": [
        {"q": "兩連續正偶數積 48，求兩數？", "options": ["6, 8", "4, 12", "8, 10", "-6, -8"], "ans": 0, "diff": "簡單", "expl": "6 * 8 = 48。"},
        {"q": "正方形面積 100，邊長加 x 後變 144，求 x？", "options": ["2", "4", "12", "10"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator._base_svg('<rect x="50" y="50" width="120" height="120" fill="none" stroke="black"/><text x="110" y="110" text-anchor="middle">144</text>'), "expl": "原邊長10，新邊長12，故 x=2。"},
        {"q": "長比寬多 3，面積 40，求寬？", "options": ["5", "8", "4", "10"], "ans": 0, "diff": "中等", "expl": "5 * 8 = 40，寬為 5。"},
        {"q": "物體落下 $h=5t^2$，若 $h=125$，求 t？", "options": ["5", "25", "10", "15"], "ans": 0, "diff": "簡單", "expl": "t^2 = 25 => t=5。"},
        {"q": "某數平方等於該數 3 倍，求某數？", "options": ["0 或 3", "3", "0", "9"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.roots_on_line(0, 3), "expl": "x^2 = 3x => x(x-3)=0。"}
    ],
    "8下：等差數列": [
        {"q": "數列 1, 3, 5, 7 ... 第 10 項？", "options": ["19", "20", "21", "17"], "ans": 0, "diff": "簡單", "expl": "1 + 9*2 = 19。"}
    ],
    "8下：幾何圖形": [
        {"q": "正三角形內角？", "options": ["60", "90", "45", "180"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_label("60", "60", "60"), "expl": "均為 60 度。"}
    ],

    # ======= 九年級 =======
    "9上：相似形": [
        {"q": "邊長比 1:3，面積比？", "options": ["1:9", "1:3", "1:6", "3:1"], "ans": 0, "diff": "簡單", "expl": "平方比 1:9。"},
        {"q": "地圖比例尺 1:1000，圖上 5cm 代表實際？", "options": ["50m", "500m", "5m", "5000cm"], "ans": 0, "diff": "中等", "expl": "5000 cm = 50 m。"}
    ],
    "9上：圓的性質": [
        {"q": "【圖解】半徑 5，弦心距 3，弦長？", "options": ["8", "4", "10", "6"], "ans": 0, "diff": "困難", "svg_gen": lambda: SVGGenerator.triangle_label("?", 3, 5), "expl": "半弦 4，全弦 8。"},
        {"q": "切線與半徑夾角？", "options": ["90度", "45度", "60度", "180度"], "ans": 0, "diff": "簡單", "expl": "垂直 90 度。"}
    ],
    # --- [考前特化] 3. 三心 ---
    "3-1 證明與推理": [
        {"q": "【圖解】三邊對應相等是哪種全等？", "options": ["SSS", "SAS", "ASA", "RHS"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.geometry_sas(), "expl": "SSS 全等。"},
        {"q": "下列何者「無法」判別全等？", "options": ["AAA", "SAS", "SSS", "AAS"], "ans": 0, "diff": "簡單", "expl": "AAA 只能判別相似。"},
        {"q": "在 $\\triangle ABC$ 中，$\\angle A > \\angle B$，對邊關係？", "options": ["BC > AC", "BC < AC", "BC = AC", "無法判斷"], "ans": 0, "diff": "簡單", "expl": "大角對大邊。"},
        {"q": "四邊形兩雙對邊分別等長，必為？", "options": ["平行四邊形", "菱形", "梯形", "箏形"], "ans": 0, "diff": "中等", "expl": "平行四邊形性質。"},
        {"q": "【圖解】等腰三角形頂角平分線性質？", "options": ["垂直平分底邊", "只平分", "只垂直", "無"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_label("a", "h", "c"), "expl": "三線合一。"}
    ],
    "3-2 外心、內心與重心": [
        {"q": "【圖解】重心是哪三線交點？", "options": ["中線", "角平分線", "中垂線", "高"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_center("centroid"), "expl": "重心 (G) 為中線交點。"},
        {"q": "【圖解】外心性質？", "options": ["到三頂點等距", "到三邊等距", "平分面積", "三高交點"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_center("circumcenter"), "expl": "外心 (O) 到頂點等距。"},
        {"q": "【圖解】內心性質？", "options": ["到三邊等距", "到三頂點等距", "平分面積", "在外部"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_center("incenter"), "expl": "內心 (I) 到三邊等距。"},
        {"q": "鈍角三角形外心在？", "options": ["外部", "內部", "邊上", "頂點"], "ans": 0, "diff": "中等", "expl": "鈍角外心在外部。"},
        {"q": "重心到頂點是到對邊中點的幾倍？", "options": ["2倍", "1.5倍", "3倍", "1倍"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.triangle_center("centroid"), "expl": "重心性質 2:1。"},
        {"q": "直角三角形兩股 6, 8，外接圓半徑？", "options": ["5", "10", "4", "3"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.triangle_label(6, 8, "?"), "expl": "斜邊 10，半徑 5。"},
        {"q": "正三角形三心關係？", "options": ["重合", "直線", "三角形", "無關"], "ans": 0, "diff": "簡單", "expl": "三心合一。"},
        {"q": "內心 $\\angle A=70^\\circ$，$\\angle BIC=$？", "options": ["$125^\\circ$", "$110^\\circ$", "$140^\\circ$", "$90^\\circ$"], "ans": 0, "diff": "困難", "expl": "$90 + 70/2 = 125$。"},
        {"q": "重心將面積分幾份？", "options": ["6", "3", "4", "2"], "ans": 0, "diff": "簡單", "expl": "6 等份。"}
    ],
    "9下：二次函數": [
        {"q": "【圖解】$y=x^2$ 開口？", "options": ["向上", "向下", "左", "右"], "ans": 0, "diff": "簡單", "svg_gen": lambda: SVGGenerator.parabola(1, 0), "expl": "係數正，向上。"},
        {"q": "【圖解】$y=-2(x-1)^2+3$ 頂點？", "options": ["(1, 3)", "(-1, 3)", "(1, -3)", "(-1, -3)"], "ans": 0, "diff": "中等", "svg_gen": lambda: SVGGenerator.parabola(-2, 3), "expl": "頂點 (1, 3)。"}
    ],
    "9下：統計與機率": [
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
    st.set_page_config(page_title="國中數學：終極完整版", page_icon="🏆", layout="centered")
    
    if 'exam_started' not in st.session_state: st.session_state.exam_started = False
    if 'current_questions' not in st.session_state: st.session_state.current_questions = []
    if 'exam_results' not in st.session_state: st.session_state.exam_results = {}
    if 'exam_finished' not in st.session_state: st.session_state.exam_finished = False

    st.sidebar.title("🏆 國中數學全攻略")
    
    unit_options = list(MATH_DB.keys())
    selected_unit = st.sidebar.selectbox("請選擇練習單元", unit_options, on_change=reset_exam)
    st.sidebar.info("已載入所有單元，包含考前衝刺特化區！")

    st.title("🏆 國中數學：終極完整版")
    st.markdown(f"#### 目前單元：{selected_unit}")

    if not st.session_state.exam_started:
        st.info(f"準備好挑戰 **{selected_unit}** 了嗎？")
        if st.button("🚀 開始測驗 (隨機 10 題)", use_container_width=True):
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
