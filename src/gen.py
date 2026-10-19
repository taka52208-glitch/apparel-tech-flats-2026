"""架空ブランド STRAYLIFT のアパレル仕様書(デザイン画)を SVG で書き出す。
座標は cm 単位で、HPS(肩の一番高い点)の中心を原点にする。"""
import math, random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'sheets')
FONTS = ("@import url('https://fonts.googleapis.com/css2?family=Anton&amp;family=Graduate&amp;family=Oswald:wght@400;600"
         "&amp;family=Noto+Sans+JP:wght@400;500;700&amp;display=swap');")

BLACK, CHAR, GREY = '#202022', '#3d3e42', '#8e8f93'
OFFW, LGREY, DGREY = '#ebe8e1', '#a9aaae', '#55565a'
LINE = '#0d0d0e'


def v(x, y): return (x, y)
def add(a, b, k=1): return (a[0] + b[0] * k, a[1] + b[1] * k)
def P(pts): return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
def mirror(pts): return [(-x, y) for x, y in reversed(pts)]


def sleeve(shoulder, length, deg, cuff):
    d = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
    n = (-d[1], d[0])
    top = add(shoulder, d, length)
    bot = add(top, n, cuff)
    return d, n, top, bot


# ---------- 型ごとの身頃 ----------

def tee_shape(front):
    d, n, top, bot = sleeve((29, 4), 23, 32, 20)
    right = [(10, 0), (29, 4), top, bot, (31, 28), (31, 74)]
    body = f'M -10,0 Q 0 {18 if front else 5} 10,0 L {P(right[1:])} L {P(mirror(right[1:]))} Z'
    rib = (f'<path d="M -12,0.7 Q 0 {22 if front else 9} 12,0.7" class="st"/>'
           f'<path d="M -10,0 Q 0 {18 if front else 5} 10,0" class="ol"/>')
    st = (f'<path d="M 29,4 Q 32.5 16 31,28 M -29,4 Q -32.5 16 -31,28" class="sm"/>'
          f'<path d="M {P([add(top, d, -2.5), add(bot, d, -2.5)])} M {P(mirror([add(top, d, -2.5), add(bot, d, -2.5)]))}" class="st"/>'
          f'<path d="M -31,71.5 L 31,71.5" class="st"/>')
    return body, rib + st, dict(d=d, n=n, top=top, bot=bot)


def hoodie_shape(front):
    d, n, top, bot = sleeve((28, 5), 55, 58, 13)
    r1, r2 = add(top, n, 1.5), add(bot, n, -1.5)
    r3, r4 = add(r2, d, 7), add(r1, d, 7)
    right = [(10, 0), (28, 5), top, bot, (31, 28), (31, 64), (29.5, 71)]
    body = f'M -10,0 Q 0 {16 if front else 5} 10,0 L {P(right[1:])} L {P(mirror(right[1:]))} Z'
    cuffs = f'<polygon points="{P([r1, r4, r3, r2])}" class="g"/><polygon points="{P(mirror([r1, r4, r3, r2]))}" class="g"/>'
    hemrib = '<path d="M -31,64 L 31,64" class="sm"/>' + ''.join(
        f'<path d="M {x:.1f},64.4 L {x * 29.6 / 31:.1f},70.6" class="rib"/>' for x in [i * 1.6 - 30.4 for i in range(39)])
    cuffrib = ''.join(f'<path d="M {P([add(r1, n, t * 10 / 9), add(add(r1, n, t * 10 / 9), d, 7)])}" class="rib"/>'
                      f'<path d="M {P(mirror([add(r1, n, t * 10 / 9), add(add(r1, n, t * 10 / 9), d, 7)]))}" class="rib"/>'
                      for t in range(1, 9))
    seams = '<path d="M 28,5 Q 33 16 31,28 M -28,5 Q -33 16 -31,28" class="sm"/>'
    if front:
        hood_back = '<path d="M -10,0 C -19,-6 -17,-31 0,-33 C 17,-31 19,-6 10,0 Z" class="g"/>'
        hood_open = '<path d="M -9,1 C -11,-14 -6,-25 0,-26 C 6,-25 11,-14 9,1 Q 0 10 -9,1 Z" class="lining"/>'
        strings = ''.join(f'<path d="M {s*3.2},6 C {s*3.6},12 {s*3},16 {s*3.8},22" class="cord"/>'
                          f'<rect x="{s*3.8-0.45}" y="22" width="0.9" height="2.6" rx="0.3" class="aglet"/>' for s in (-1, 1))
        pocket = ('<path d="M -19,63.6 L -19,55 L -13,43 L 13,43 L 19,55 L 19,63.6" class="ol"/>'
                  '<path d="M -12.2,44 L 12.2,44 M -13.6,43.6 L -19.6,55.4 M 13.6,43.6 L 19.6,55.4" class="st"/>')
        return body, hood_back, cuffs + cuffrib + hemrib + seams + hood_open + strings + pocket, dict(d=d, n=n, top=top, bot=bot)
    hood = ('<path d="M -12,2 C -19,-6 -17,-31 0,-33 C 17,-31 19,-6 12,2 Q 0 17 -12,2 Z" class="g"/>'
            '<path d="M 0,-33 C 0.6,-20 0.4,-4 0,9.5" class="sm"/>')
    return body, '', cuffs + cuffrib + hemrib + seams + hood, dict(d=d, n=n, top=top, bot=bot)


def jersey_shape(front):
    d, n, top, bot = sleeve((28, 4), 22, 26, 23)
    right = [(10, 0), (28, 4), top, bot, (31, 29), (31, 76)]
    neck = 'L 0,15 L 10,0' if front else 'Q 0 5 10,0'
    body = f'M -10,0 {neck} L {P(right[1:])} L {P(mirror(right[1:]))} Z'
    if front:
        rib = '<path d="M -12.5,0.8 L 0,18.6 L 12.5,0.8" class="sm"/><path d="M -10,0 L 0,15 L 10,0" class="ol"/>'
    else:
        rib = '<path d="M -12,0.7 Q 0 9 12,0.7" class="st"/><path d="M -10,0 Q 0 5 10,0" class="ol"/>'
    stripes = ''
    for k in (4, 7.5):
        a, b = add(top, d, -k), add(bot, d, -k)
        a2, b2 = add(a, d, -2), add(b, d, -2)
        for pts in ([a, b, b2, a2], mirror([a, b, b2, a2])):
            stripes += f'<polygon points="{P(pts)}" class="stripe"/>'
    mesh = ('<path d="M 24,30 L 31,29 L 31,76 L 24,76 Z M -24,30 L -31,29 L -31,76 L -24,76 Z" class="mesh"/>'
            '<path d="M 24,30 L 24,76 M -24,30 L -24,76" class="sm"/>')
    st = (f'<path d="M 28,4 Q 32 16 31,29 M -28,4 Q -32 16 -31,29" class="sm"/>'
          f'<path d="M {P([add(top, d, -1.6), add(bot, d, -1.6)])} M {P(mirror([add(top, d, -1.6), add(bot, d, -1.6)]))}" class="st"/>'
          '<path d="M -31,73.5 L 31,73.5" class="st"/>')
    return body, rib + stripes + mesh + st, dict(d=d, n=n, top=top, bot=bot)


# ---------- グラフィック ----------

def cracks(seed, x0, y0, x1, y1, cell=1.5, keep=.62):
    rnd = random.Random(seed)
    nx, ny = int((x1 - x0) / cell) + 2, int((y1 - y0) / cell) + 2
    g = [[(x0 + i * cell + rnd.uniform(-.55, .55) * cell, y0 + j * cell + rnd.uniform(-.55, .55) * cell)
          for j in range(ny)] for i in range(nx)]
    seg = []
    for i in range(nx):
        for j in range(ny):
            if i + 1 < nx and rnd.random() < keep: seg.append((g[i][j], g[i + 1][j]))
            if j + 1 < ny and rnd.random() < keep: seg.append((g[i][j], g[i][j + 1]))
    return ''.join(f'M {a[0]:.2f},{a[1]:.2f} L {b[0]:.2f},{b[1]:.2f} ' for a, b in seg)


def plate_mark(cx, cy, r, ink, ground):
    """バーベルのプレートを図案化したマーク(S)。"""
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{ink}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.74:.2f}" fill="{ground}"/>'
            f'<rect x="{cx-r*1.02:.2f}" y="{cy-r*.13:.2f}" width="{r*.34:.2f}" height="{r*.26:.2f}" fill="{ground}"/>'
            f'<rect x="{cx+r*.68:.2f}" y="{cy-r*.13:.2f}" width="{r*.34:.2f}" height="{r*.26:.2f}" fill="{ground}"/>'
            f'<text x="{cx}" y="{cy+r*.42:.2f}" font-family="Anton" font-size="{r*1.2:.2f}" fill="{ink}" text-anchor="middle">S</text></g>')


def marker(n, x, y):
    return (f'<g class="mk"><circle cx="{x}" cy="{y}" r="2.1"/>'
            f'<text x="{x}" y="{y+0.95}" text-anchor="middle">{n}</text></g>')


def dim_h(x1, x2, y, label):
    return (f'<g class="dim"><path d="M {x1},{y} L {x2},{y} M {x1},{y-1} L {x1},{y+1} M {x2},{y-1} L {x2},{y+1}"/>'
            f'<text x="{(x1+x2)/2}" y="{y-0.8}" text-anchor="middle">{label}</text></g>')


def dim_v(x, y1, y2, label, side=1):
    tx = x + 0.9 * side
    return (f'<g class="dim"><path d="M {x},{y1} L {x},{y2} M {x-1},{y1} L {x+1},{y1} M {x-1},{y2} L {x+1},{y2}"/>'
            f'<text x="{tx}" y="{(y1+y2)/2+0.8}" text-anchor="{"start" if side>0 else "end"}">{label}</text></g>')


def art_tee(front, c, info, uid):
    ink, ground = c['ink'], c['body']
    if front:
        d = info['d']
        cx, cy = (info['top'][0] + info['bot'][0]) / 2 - d[0] * 9, (info['top'][1] + info['bot'][1]) / 2 - d[1] * 9
        ang = math.degrees(math.atan2(d[1], d[0])) - 90
        return (plate_mark(12.5, 19, 3.6, ink, ground) +
                f'<text transform="translate({cx:.2f},{cy:.2f}) rotate({ang:.1f})" font-family="Oswald" font-weight="600" '
                f'font-size="1.5" fill="{c["ink2"]}" text-anchor="middle" textLength="9" lengthAdjust="spacingAndGlyphs">SET · REP · REST</text>')
    words = (f'<path id="arc{uid}" d="M -15,19 Q 0 9 15,19" fill="none"/>'
             f'<text font-family="Graduate" font-size="4.2" fill="{c["ink2"]}" letter-spacing="0.5">'
             f'<textPath href="#arc{uid}" startOffset="50%" text-anchor="middle">STRAYLIFT</textPath></text>')
    big = (f'<text x="0" y="36" font-family="Anton" font-size="15" text-anchor="middle" textLength="32" lengthAdjust="spacingAndGlyphs">HEAVY</text>'
           f'<text x="0" y="52" font-family="Anton" font-size="15" text-anchor="middle" textLength="32" lengthAdjust="spacingAndGlyphs">DAYS</text>')
    clip = f'<clipPath id="cl{uid}">{big}</clipPath>'
    return (words + clip + f'<g fill="{ink}">{big}</g>'
            f'<path d="{cracks(7, -17, 21, 17, 53, cell=2.4, keep=.55)}" stroke="{ground}" stroke-width="0.11" fill="none" clip-path="url(#cl{uid})"/>'
            f'<text x="0" y="56.4" font-family="Oswald" font-size="1.7" fill="{c["ink2"]}" text-anchor="middle" '
            f'letter-spacing="0.35">TRAINING DIVISION — EST. 2026</text>')


def art_hoodie(front, c, info, uid):
    ink = c['ink']
    if front:
        d = info['d']
        mid = add(((info['top'][0] + info['bot'][0]) / 2, (info['top'][1] + info['bot'][1]) / 2), d, -27)
        ang = math.degrees(math.atan2(d[1], d[0]))
        return (f'<text x="0" y="0" transform="translate(0,28) skewX(-12)" font-family="Anton" font-size="5" fill="{ink}" text-anchor="middle" '
                f'textLength="22" lengthAdjust="spacingAndGlyphs" letter-spacing="0.4">STRAYLIFT</text>'
                f'<path d="M -11,29.6 L 11,29.6" stroke="{c["ink2"]}" stroke-width="0.5"/>'
                f'<text transform="translate({mid[0]:.2f},{mid[1]:.2f}) rotate({ang:.1f})" font-family="Oswald" font-weight="600" '
                f'font-size="2.2" fill="{c["ink2"]}" text-anchor="middle" textLength="38" lengthAdjust="spacingAndGlyphs">'
                f'STRAYLIFT TRAINING GEAR — RACING DEPT.</text>')
    # 背面: 発泡プリントのアーチ文字 + ナンバープレート型ワッペン
    chk = ''.join(f'<rect x="{-13 + i*1.3:.1f}" y="{22.4 + (i%2)*1.3:.1f}" width="1.3" height="1.3" fill="{c["patchink"]}"/>' for i in range(20))
    return (f'<path id="arc{uid}" d="M -22,22 Q 0 4 22,22" fill="none"/>'
            f'<text font-family="Graduate" font-size="6" fill="{ink}" letter-spacing="0.4">'
            f'<textPath href="#arc{uid}" startOffset="50%" text-anchor="middle">STRAYLIFT</textPath></text>'
            f'<rect x="-13" y="22.4" width="26" height="18" rx="3.2" fill="{c["patch"]}" stroke="{c["ink"]}" stroke-width="0.8"/>'
            + chk +
            f'<text x="0" y="36.6" font-family="Anton" font-size="10" fill="{c["patchink"]}" text-anchor="middle">27</text>'
            f'<text x="0" y="39.1" font-family="Oswald" font-weight="600" font-size="1.5" fill="{c["patchink"]}" text-anchor="middle" letter-spacing="0.3">RACING DEPT.</text>'
            f'<text x="0" y="45.5" font-family="Oswald" font-size="1.8" fill="{c["ink2"]}" text-anchor="middle" letter-spacing="0.5">LIFT HEAVY · RIDE HARD</text>')


def art_jersey(front, c, info, uid):
    ink = c['ink']
    num = lambda y, size, w: (f'<text x="0" y="{y}" font-family="Graduate" font-size="{size}" text-anchor="middle" textLength="{w}" '
                              f'lengthAdjust="spacingAndGlyphs" fill="{ink}" stroke="{c["ink2"]}" stroke-width="0.9" '
                              f'paint-order="stroke" stroke-linejoin="round">92</text>')
    if front:
        return plate_mark(12.5, 9.5, 2.6, c['ink2'], c['body']) + num(47, 26, 26)
    return (f'<text x="0" y="13.5" font-family="Oswald" font-weight="600" font-size="3.6" fill="{ink}" text-anchor="middle" '
            f'textLength="25" lengthAdjust="spacingAndGlyphs">STRAYLIFT</text>' + num(51, 32, 32))


STYLES = {
    'tee': dict(shape=tee_shape, art=art_tee, scale=5.6, no='SL-26AW-01', en='Oversized Boxy Tee',
                ja='オーバーサイズ ボクシーTシャツ',
                fabric='コットン100% 天竺 10.2oz(約345g/m²)・ウォッシュ加工',
                fit='ボクシー／ドロップショルダー・身幅62cm・着丈74cm(Lサイズ基準)'),
    'hoodie': dict(shape=hoodie_shape, art=art_hoodie, scale=4.9, no='SL-26AW-02', en='Heavyweight Moto Hoodie',
                   ja='ヘビーウェイト モトクロス フーディ',
                   fabric='コットン100% 裏毛 14oz・ピグメント染め',
                   fit='オーバーサイズ・身幅62cm・着丈71cm(リブ込み)・袖リブ7cm(Lサイズ基準)'),
    'jersey': dict(shape=jersey_shape, art=art_jersey, scale=5.4, no='SL-26AW-03', en='Mesh Football Jersey Top',
                   ja='メッシュ フットボールジャージ型トップス',
                   fabric='ポリエステル100% ダブルメッシュ(脇切り替え:エアメッシュ)',
                   fit='オーバーサイズ・身幅62cm・着丈76cm・Vネック(Lサイズ基準)'),
}

COLORS = {
    'tee': [dict(name='BLACK × OFF WHITE', body=BLACK, ink=OFFW, ink2=LGREY),
            dict(name='CHARCOAL × GREY', body=CHAR, ink=LGREY, ink2=OFFW),
            dict(name='GREY × BLACK', body=GREY, ink='#18181a', ink2=DGREY)],
    'hoodie': [dict(name='BLACK × OFF WHITE', body=BLACK, ink=OFFW, ink2=LGREY, patch=GREY, patchink='#18181a'),
               dict(name='CHARCOAL × OFF WHITE', body=CHAR, ink=OFFW, ink2=LGREY, patch='#18181a', patchink=OFFW),
               dict(name='GREY × BLACK', body=GREY, ink='#18181a', ink2=DGREY, patch=OFFW, patchink='#18181a')],
    'jersey': [dict(name='BLACK × OFF WHITE', body=BLACK, ink=OFFW, ink2=GREY, stripe=GREY, mesh=CHAR),
               dict(name='CHARCOAL × BLACK', body=CHAR, ink='#18181a', ink2=LGREY, stripe='#18181a', mesh=BLACK),
               dict(name='GREY × BLACK', body=GREY, ink='#18181a', ink2=OFFW, stripe='#18181a', mesh=DGREY)],
}

SPECS = {
    'tee': [
        ('左胸 プレートマーク', 'HPSから下19cm・中心から左へ12.5cm', '直径7.2cm', 'オフホワイト(参考 PANTONE 11-0602 TCX)', 'シルクスクリーン 1色'),
        ('左袖 SET · REP · REST', '袖口から上9cm・袖中央', '幅9cm', 'ライトグレー(参考 PANTONE Cool Gray 5 C)', 'シルクスクリーン 1色'),
        ('背面 アーチロゴ', 'HPSから下13cm・中心', '幅30cm × 高さ6cm', 'ライトグレー', 'シルクスクリーン 1色'),
        ('背面 HEAVY DAYS', 'HPSから下25cm・中心', '幅32cm × 高さ28cm', 'オフホワイト', 'シルクスクリーン クラック加工(ひび割れ)'),
        ('背面 小文字', 'HPSから下55cm・中心', '幅24cm', 'ライトグレー', 'シルクスクリーン 1色(細線0.3mm以上)'),
    ],
    'hoodie': [
        ('胸 STRAYLIFT', 'HPSから下23cm・中心', '幅22cm × 高さ4cm(12°斜体)', 'オフホワイト／下線ライトグレー', '刺繍 サテン縫い'),
        ('左袖 縦長ロゴ', '肩線から下18cm・袖の中心線に沿う', '幅38cm × 高さ2cm', 'ライトグレー', 'シルクスクリーン 1色'),
        ('背面 アーチロゴ', 'HPSから下9cm・中心', '幅40cm × 高さ8cm', 'オフホワイト', '発泡プリント(盛り上がり約1mm)'),
        ('背面 ナンバーワッペン', 'HPSから下22cm・中心', '26cm × 18cm・角R3.2cm', '台:グレー／縁・文字:オフホワイト／27:ブラック', 'フェルト台＋刺繍・縁はメロー巻き'),
        ('背面 小文字', 'HPSから下44cm・中心', '幅22cm', 'ライトグレー', 'シルクスクリーン 1色'),
    ],
    'jersey': [
        ('前 ナンバー 92', 'HPSから下21cm・中心', '幅26cm × 高さ26cm', '本体:オフホワイト／縁0.9cm:グレー', 'タックルツイル(2層アップリケ)'),
        ('左胸 プレートマーク', 'HPSから下9.5cm・中心から左へ12.5cm', '直径5.2cm', 'グレー', '刺繍 タタミ縫い'),
        ('袖 2本ライン', '袖口から4cm・7.5cmの位置', '幅2cm × 2本', 'グレー', '切り替え(本体と同じメッシュ)'),
        ('背面 ネーム STRAYLIFT', 'HPSから下10cm・中心', '幅25cm × 高さ3.6cm', 'オフホワイト', 'タックルツイル 1層'),
        ('背面 ナンバー 92', 'HPSから下18cm・中心', '幅32cm × 高さ32cm', '本体:オフホワイト／縁0.9cm:グレー', 'タックルツイル(2層アップリケ)'),
    ],
}

MARKERS = {  # (面, 番号, x, y) cm
    'tee': [('f', 1, 18.5, 14.5), ('f', 2, 44, 31), ('b', 3, 19, 13), ('b', 4, 20, 30), ('b', 5, 15.5, 60)],
    'hoodie': [('f', 1, -15, 22), ('f', 2, 55, 40), ('b', 3, 24, 13), ('b', 4, 16, 26), ('b', 5, 14, 48.5)],
    'jersey': [('f', 1, 16, 26), ('f', 2, 18, 6), ('f', 3, 46, 26), ('b', 4, 16, 9), ('b', 5, 19.5, 30)],
}

DIMS = {
    'tee': lambda: dim_v(-25, 0, 25, '25cm', -1) + dim_h(-16, 16, 61, '32cm'),
    'hoodie': lambda: dim_v(-27, 0, 22.4, '22cm', -1) + dim_h(-13, 13, 50, '26cm'),
    'jersey': lambda: dim_v(-25, 0, 18, '18cm', -1) + dim_h(-16, 16, 56, '32cm'),
}

CSS = f"""{FONTS}
.ol{{fill:none;stroke:{LINE};stroke-width:.22}}
.sm{{fill:none;stroke:{LINE};stroke-width:.14;opacity:.75}}
.st{{fill:none;stroke:#77787c;stroke-width:.12;stroke-dasharray:.5 .35}}
.rib{{fill:none;stroke:{LINE};stroke-width:.08;opacity:.45}}
.cord{{fill:none;stroke:#d9d6cf;stroke-width:.45;stroke-linecap:round}}
.aglet{{fill:#77787c}}
.mk circle{{fill:#c2410c}} .mk text{{font:700 2.4px 'Noto Sans JP';fill:#fff}}
.dim path{{stroke:#c2410c;stroke-width:.13;fill:none}} .dim text{{font:500 2.1px 'Noto Sans JP';fill:#c2410c}}
.t1{{font:700 30px 'Noto Sans JP';fill:#18181a}} .t2{{font:400 15px 'Noto Sans JP';fill:#55565a}}
.en{{font:600 15px Oswald;letter-spacing:.24em;fill:#55565a}} .lab{{font:600 14px Oswald;letter-spacing:.3em;fill:#55565a}}
.sh{{font:700 16px 'Noto Sans JP';fill:#18181a}} .sv{{font:400 13.5px 'Noto Sans JP';fill:#3b3c40}}
.sk{{font:500 12px 'Noto Sans JP';fill:#8a8b8f}}
"""


def garment(style, front, c, uid):
    s = STYLES[style]
    res = s['shape'](front)
    if len(res) == 4:
        body, under, over, info = res
    else:
        body, over, info = res
        under = ''
    cls = f'''<style>#{uid} .g{{fill:{c["body"]};stroke:{LINE};stroke-width:.22}}
#{uid} .lining{{fill:{c.get("lining", "#111")};stroke:{LINE};stroke-width:.18}}
#{uid} .stripe{{fill:{c.get("stripe", GREY)}}} #{uid} .mesh{{fill:url(#mesh{uid});}}</style>'''
    mesh = (f'<pattern id="mesh{uid}" width="0.9" height="0.9" patternUnits="userSpaceOnUse">'
            f'<rect width="0.9" height="0.9" fill="{c.get("mesh", c["body"])}"/><circle cx="0.45" cy="0.45" r="0.18" fill="#000" opacity=".55"/></pattern>')
    return (cls + f'<defs>{mesh}</defs><g id="{uid}">{under}'
            f'<path d="{body}" class="g"/>{over}'
            f'{s["art"](front, c, info, uid)}</g>')


def sheet(style):
    s, cs = STYLES[style], COLORS[style]
    sc, W, H = s['scale'], 1900, 1320
    top = 330 if style == 'hoodie' else 200
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{CSS}</style>',
         f'<rect width="{W}" height="{H}" fill="#f5f4f1"/>',
         f'<text x="60" y="70" class="en">STRAYLIFT  /  {s["no"]}  /  {s["en"].upper()}</text>',
         f'<text x="60" y="114" class="t1">{s["ja"]}</text>',
         f'<text x="60" y="146" class="t2">{s["fabric"]}　｜　{s["fit"]}</text>',
         f'<path d="M 60,168 L {W-60},168" stroke="#18181a" stroke-width="1.5"/>']
    for i, (front, cx) in enumerate([(True, 360), (False, 1000)]):
        uid = f'{style}{"F" if front else "B"}'
        o.append(f'<g transform="translate({cx},{top}) scale({sc})">{garment(style, front, cs[0], uid)}')
        if not front:
            o.append(DIMS[style]())
        for face, n, x, y in MARKERS[style]:
            if (face == 'f') == front:
                o.append(marker(n, x, y))
        o.append('</g>')
        o.append(f'<text x="{cx}" y="{top + (78 if style!="hoodie" else 76) * sc + 30}" class="lab" text-anchor="middle">{"FRONT" if front else "BACK"}</text>')
    # 仕様欄
    x0, y = 1370, 220
    o.append(f'<text x="{x0}" y="{y-14}" class="lab">GRAPHIC SPEC</text>')
    for n, (title, pos, size, col, proc) in enumerate(SPECS[style], 1):
        y += 30
        o.append(f'<g transform="translate({x0+12},{y-6}) scale(5)">{marker(n, 0, 0)}</g>')
        o.append(f'<text x="{x0+34}" y="{y}" class="sh">{title}</text>')
        for k, val in (('位置', pos), ('大きさ', size), ('色', col), ('加工', proc)):
            y += 22
            o.append(f'<text x="{x0+34}" y="{y}" class="sk">{k}</text><text x="{x0+92}" y="{y}" class="sv">{val}</text>')
        y += 16
    # カラーバリエーション
    yb = 1000 if style != 'hoodie' else 1035
    o.append(f'<path d="M 60,{yb-40} L {W-60},{yb-40}" stroke="#d6d4ce"/>')
    o.append(f'<text x="60" y="{yb-8}" class="lab">COLORWAY</text>')
    tsc = 2.3 if style != 'hoodie' else 2.0
    for i, c in enumerate(cs):
        cx = 200 + i * 300
        ty = yb + (75 if style == 'hoodie' else 20)
        o.append(f'<g transform="translate({cx},{ty}) scale({tsc})">{garment(style, False, c, f"{style}C{i}")}</g>')
        o.append(f'<text x="{cx}" y="{H-36}" class="sk" text-anchor="middle">{c["name"]}</text>')
    notes = {
        'tee': ['クラック加工は洗い込みでひびが広がる前提で、細い文字には使わない', '背面は首下13cmから始め、ボクシーの身幅でも中央に寄りすぎない大きさ', '袖の小文字は袖口と平行に置き、腕を下ろしたとき横から読める向き'],
        'hoodie': ['胸は刺繍、背面は発泡とワッペンで、触ったときの質感を3種類に分ける', 'ワッペンはアーチ文字に重ならないよう、フードの影を避けた首下22cm', '袖の縦長ロゴは袖の中心線に沿わせ、モトクロスのジャージの袖の見え方に寄せる'],
        'jersey': ['番号はタックルツイルの2層で、メッシュの透けに負けない面積を取る', '脇はエアメッシュに切り替え、トレーニング中の熱を逃がす', '袖ラインは本体と同じメッシュの切り替えにして、プリントのひび割れを避ける'],
    }[style]
    o.append(f'<text x="1000" y="{yb-8}" class="lab">DESIGN NOTE</text>')
    for k, t in enumerate(notes):
        o.append(f'<text x="1000" y="{yb+30+k*30}" class="sv">・{t}</text>')
    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for st in STYLES:
        open(os.path.join(OUT, f'{st}.svg'), 'w').write(sheet(st))
        print(st)
