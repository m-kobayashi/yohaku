#!/usr/bin/env python3
"""wagara_svg.py — 和柄(日本の伝統幾何学文様)のシームレスSVGをコードで正確に生成する制作ツール。

AIの画像生成ではなく数学的に描画するため、紋様の幾何学的正確性が保証される
(= 文化的正確性が差別化になる)。標準ライブラリのみ。

使い方:
  python3 tools/wagara_svg.py <出力ディレクトリ> [パターン名]
パターン名省略時は全パターン × 全カラーを出力。
"""
import math
import os
import sys

# 伝統色(日本の伝統色名)
PALETTE = {
    "sumi": "#1a1a1a",   # 墨
    "ai": "#165e83",     # 藍
    "shu": "#d9333f",    # 朱
}

# ゴシック配色(halloween-yokai-svg ニッチ向け。伝統紋様パターンをこの配色で流用する)
GOTHIC_PALETTE = {
    "kokushoku": "#0d0d0d",   # 黒色(漆黒)
    "kyoshi": "#3d1350",      # 京紫寄りの深紫(妖しさ)
    "kabocha": "#d2601a",     # かぼちゃ橙(ハロウィン)
}

SIZE = 800  # viewBox一辺(px)


def _svg(size, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">\n{body}\n</svg>\n'
    )


def _line(x1, y1, x2, y2, color, sw=2.0):
    return (f'  <line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')


# ── 既存パターン ──────────────────────────────────────────────────────────────

def ichimatsu(color, size=SIZE, n=8):
    """市松文様: n×nの市松格子(fill)。偶数nでシームレス。"""
    cell = size / n
    rects = [
        f'  <rect x="{i*cell:.2f}" y="{j*cell:.2f}" width="{cell:.2f}" '
        f'height="{cell:.2f}" fill="{color}"/>'
        for i in range(n) for j in range(n) if (i + j) % 2 == 0
    ]
    return _svg(size, "\n".join(rects))


def shippo(color, size=SIZE, d=200):
    """七宝文様: 円を格子間隔dで配置、半径r=d/√2 で隣接円が交差し四つ葉を成す。線画。"""
    r = d / math.sqrt(2)
    n = int(size / d) + 2
    circles = [
        f'  <circle cx="{i*d}" cy="{j*d}" r="{r:.2f}" fill="none" '
        f'stroke="{color}" stroke-width="3"/>'
        for i in range(-1, n + 1) for j in range(-1, n + 1)
    ]
    return _svg(size, "\n".join(circles))


def seigaiha(color, size=SIZE, w=200, arcs=4):
    """青海波文様: 上向き同心半円を鱗状に重ねる。線画。"""
    R = w / 2
    vp = R / 2
    rows = int(size / vp) + 2
    cols = int(size / w) + 2
    paths = []
    for row in range(rows):
        cy = row * vp
        xoff = (w / 2) if row % 2 else 0
        for col in range(-1, cols + 1):
            cx = col * w + xoff
            for k in range(arcs):
                r = R * (1 - k / arcs)
                paths.append(
                    f'  <path d="M{cx-r:.2f},{cy:.2f} A{r:.2f},{r:.2f} 0 0 1 '
                    f'{cx+r:.2f},{cy:.2f}" fill="none" stroke="{color}" stroke-width="2.5"/>'
                )
    return _svg(size, "\n".join(paths))


# ── 新規パターン ──────────────────────────────────────────────────────────────

def asanoha(color, size=SIZE, d=90):
    """麻の葉文様: 六角格子を基本単位とした麻の葉形繰り返し。線画。
    各六角形: 中心→辺中点(6本) + 各頂点→隣接2辺中点(12本) でハノハ形を成す。
    """
    R = d
    hex_w = R * math.sqrt(3)
    hex_h_pitch = R * 1.5
    rows = int(size / hex_h_pitch) + 4
    cols = int(size / hex_w) + 4
    paths = []
    sw = 2.2

    def verts(cx, cy):
        return [(cx + R * math.sin(k * math.pi / 3),
                 cy - R * math.cos(k * math.pi / 3)) for k in range(6)]

    def mids(vs):
        return [((vs[k][0] + vs[(k + 1) % 6][0]) / 2,
                 (vs[k][1] + vs[(k + 1) % 6][1]) / 2) for k in range(6)]

    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * hex_w + (row % 2) * hex_w / 2
            cy = row * hex_h_pitch
            vs = verts(cx, cy)
            ms = mids(vs)
            for m in ms:
                paths.append(_line(cx, cy, m[0], m[1], color, sw))
            for k in range(6):
                vx, vy = vs[k]
                paths.append(_line(vx, vy, ms[(k - 1) % 6][0], ms[(k - 1) % 6][1], color, sw))
                paths.append(_line(vx, vy, ms[k][0], ms[k][1], color, sw))

    return _svg(size, "\n".join(paths))


def kagome(color, size=SIZE, a=90):
    """籠目文様: 三角格子の全辺を描く竹かごの目模様。線画。"""
    h = a * math.sqrt(3) / 2
    rows = int(size / h) + 4
    cols = int(size / a) + 4
    paths = []
    sw = 2.2

    def pt(r, c):
        return (c * a + (r % 2) * a / 2, r * h)

    for row in range(-2, rows):
        for col in range(-2, cols):
            p = pt(row, col)
            pr = pt(row, col + 1)
            paths.append(_line(p[0], p[1], pr[0], pr[1], color, sw))
            if row % 2 == 0:
                pd = pt(row + 1, col)
                pdl = pt(row + 1, col - 1)
                paths.append(_line(p[0], p[1], pd[0], pd[1], color, sw))
                paths.append(_line(p[0], p[1], pdl[0], pdl[1], color, sw))
            else:
                pd = pt(row + 1, col)
                pdr = pt(row + 1, col + 1)
                paths.append(_line(p[0], p[1], pd[0], pd[1], color, sw))
                paths.append(_line(p[0], p[1], pdr[0], pdr[1], color, sw))

    return _svg(size, "\n".join(paths))


def uroko(color, size=SIZE, w=110):
    """鱗文様: 上向き三角形を行ごとにずらして重ねた魚鱗文様。線画。"""
    h = w * math.sqrt(3) / 2
    row_pitch = h * 0.75
    rows = int(size / row_pitch) + 4
    cols = int(size / w) + 4
    paths = []
    sw = 2.2

    for row in range(-2, rows):
        for col in range(-2, cols):
            x0 = col * w + (row % 2) * w / 2
            y0 = row * row_pitch
            top = (x0 + w / 2, y0)
            bl = (x0, y0 + h)
            br = (x0 + w, y0 + h)
            paths.append(_line(top[0], top[1], bl[0], bl[1], color, sw))
            paths.append(_line(top[0], top[1], br[0], br[1], color, sw))
            paths.append(_line(bl[0], bl[1], br[0], br[1], color, sw))

    return _svg(size, "\n".join(paths))


def tatewaku(color, size=SIZE, w=90):
    """立涌文様: 対の縦波線が紡錘形を成す文様。ベジェ曲線。"""
    wave_h = w * 2.2
    amp = w * 0.22
    cols = int(size / w) + 4
    n_waves = int(size / wave_h) + 4
    paths = []
    sw = 2.2

    for col in range(-2, cols):
        x_base = col * w
        for side in (-1, 1):
            x = x_base + side * w / 4
            for wave in range(-2, n_waves):
                y0 = wave * wave_h
                y1 = y0 + wave_h
                a = amp * side
                paths.append(
                    f'  <path d="M{x:.2f},{y0:.2f} '
                    f'C{x+a:.2f},{y0+wave_h*0.25:.2f} '
                    f'{x+a:.2f},{y0+wave_h*0.75:.2f} '
                    f'{x:.2f},{y1:.2f}" '
                    f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
                )

    return _svg(size, "\n".join(paths))


def yagasuri(color, size=SIZE, w=80):
    """矢絣文様: 菱形に横中線を加えた矢羽根形繰り返しパターン。線画。"""
    h = w * 1.4
    h_half = h / 2
    row_pitch = h_half
    rows = int(size / row_pitch) + 6
    cols = int(size / w) + 6
    paths = []
    sw = 2.2

    for row in range(-3, rows):
        for col in range(-3, cols):
            cx = col * w + (row % 2) * w / 2
            cy = row * row_pitch
            top = (cx, cy)
            ml = (cx - w / 2, cy + h_half)
            mr = (cx + w / 2, cy + h_half)
            bot = (cx, cy + h)
            paths.append(_line(top[0], top[1], ml[0], ml[1], color, sw))
            paths.append(_line(top[0], top[1], mr[0], mr[1], color, sw))
            paths.append(_line(ml[0], ml[1], mr[0], mr[1], color, sw))
            paths.append(_line(ml[0], ml[1], bot[0], bot[1], color, sw))
            paths.append(_line(mr[0], mr[1], bot[0], bot[1], color, sw))

    return _svg(size, "\n".join(paths))


def hishi(color, size=SIZE, w=100):
    """菱文様: 菱形(ひし形)を整列した菱格子。線画。"""
    h = w * 0.6
    paths = []
    sw = 2.2
    cols = int(size / w) + 4
    rows = int(size / h) + 4

    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * w + (row % 2) * w / 2
            cy = row * h
            top = (cx, cy - h / 2)
            right = (cx + w / 2, cy)
            bot = (cx, cy + h / 2)
            left = (cx - w / 2, cy)
            paths.append(_line(top[0], top[1], right[0], right[1], color, sw))
            paths.append(_line(right[0], right[1], bot[0], bot[1], color, sw))
            paths.append(_line(bot[0], bot[1], left[0], left[1], color, sw))
            paths.append(_line(left[0], left[1], top[0], top[1], color, sw))

    return _svg(size, "\n".join(paths))


def nanako(color, size=SIZE, d=60):
    """魚子(ななこ)文様: 小円を格子状に整列した細かい粒文様。"""
    r = d * 0.35
    n = int(size / d) + 4
    circles = [
        f'  <circle cx="{(i-1)*d:.2f}" cy="{(j-1)*d:.2f}" r="{r:.2f}" '
        f'fill="none" stroke="{color}" stroke-width="2.0"/>'
        for i in range(n + 2) for j in range(n + 2)
    ]
    return _svg(size, "\n".join(circles))


def nami(color, size=SIZE, w=120):
    """波文様: V字の連続で成る波形パターン。線画。"""
    h = w * 0.55
    row_pitch = h
    rows = int(size / row_pitch) + 4
    cols = int(size / w) + 4
    paths = []
    sw = 2.5

    for row in range(-2, rows):
        for col in range(-2, cols):
            x0 = col * w + (row % 2) * w / 2
            y0 = row * row_pitch
            apex = (x0 + w / 2, y0)
            bl = (x0, y0 + h)
            br = (x0 + w, y0 + h)
            paths.append(_line(bl[0], bl[1], apex[0], apex[1], color, sw))
            paths.append(_line(apex[0], apex[1], br[0], br[1], color, sw))

    return _svg(size, "\n".join(paths))


def sayagata(color, size=SIZE, u=50):
    """紗綾形文様: 卍(まんじ)を基調とした連続幾何学文様。折れ線画。"""
    cell = u * 4
    cols = int(size / cell) + 4
    rows = int(size / cell) + 4
    paths = []
    sw = 2.2

    def seg(x1, y1, x2, y2):
        return _line(x1, y1, x2, y2, color, sw)

    for row in range(-2, rows):
        for col in range(-2, cols):
            x = col * cell
            y = row * cell
            # 右回り卍を縦横のL字折れ線4本で構成 (cell=4u)
            # 上腕
            paths.append(seg(x+u, y,    x+u,   y+u))
            paths.append(seg(x+u, y,    x+3*u, y))
            # 右腕
            paths.append(seg(x+4*u, y+u, x+3*u, y+u))
            paths.append(seg(x+4*u, y+u, x+4*u, y+3*u))
            # 下腕
            paths.append(seg(x+3*u, y+4*u, x+3*u, y+3*u))
            paths.append(seg(x+3*u, y+4*u, x+u,   y+4*u))
            # 左腕
            paths.append(seg(x,    y+3*u, x+u,   y+3*u))
            paths.append(seg(x,    y+3*u, x,     y+u))
            # 中心十字
            paths.append(seg(x+u,   y+u,   x+3*u, y+u))
            paths.append(seg(x+3*u, y+u,   x+3*u, y+3*u))
            paths.append(seg(x+3*u, y+3*u, x+u,   y+3*u))
            paths.append(seg(x+u,   y+3*u, x+u,   y+u))

    return _svg(size, "\n".join(paths))


# ── パターン辞書 ─────────────────────────────────────────────────────────────

PATTERNS = {
    "ichimatsu": ichimatsu,
    "shippo":    shippo,
    "seigaiha":  seigaiha,
    "asanoha":   asanoha,
    "kagome":    kagome,
    "uroko":     uroko,
    "tatewaku":  tatewaku,
    "yagasuri":  yagasuri,
    "hishi":     hishi,
    "nanako":    nanako,
    "nami":      nami,
    "sayagata":  sayagata,
}

# 商品バンドル定義
# 値はパターン名リスト(既定パレット=PALETTE使用)、または
# {"patterns": [...], "palette": {...}} で専用配色を指定
BUNDLES = {
    "wagara-svg-001": ["ichimatsu", "shippo", "seigaiha"],
    "wagara-svg-002": ["asanoha", "kagome", "uroko", "tatewaku"],
    "wagara-svg-003": ["yagasuri", "hishi", "nanako"],
    "wagara-svg-004": ["nami", "sayagata", "kagome"],
    "halloween-yokai-001": {
        "patterns": ["asanoha", "tatewaku", "sayagata"],
        "palette": GOTHIC_PALETTE,
    },
}


def main():
    if len(sys.argv) < 2:
        sys.exit("使い方: python3 tools/wagara_svg.py <出力ディレクトリ> [パターン名またはバンドルID]")
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)

    palette = PALETTE
    if len(sys.argv) >= 3:
        key = sys.argv[2]
        if key in BUNDLES:
            bundle = BUNDLES[key]
            if isinstance(bundle, dict):
                pattern_names = bundle["patterns"]
                palette = bundle.get("palette", PALETTE)
            else:
                pattern_names = bundle
        elif key in PATTERNS:
            pattern_names = [key]
        else:
            sys.exit(f"不明なパターン/バンドル: {key}")
    else:
        pattern_names = list(PATTERNS.keys())

    count = 0
    for pname in pattern_names:
        fn = PATTERNS[pname]
        for cname, color in palette.items():
            svg = fn(color)
            path = os.path.join(out, f"{pname}-{cname}.svg")
            with open(path, "w") as f:
                f.write(svg)
            count += 1
            print(f"  {pname}-{cname}.svg")

    print(f"生成完了: {count} ファイル → {out}")


if __name__ == "__main__":
    main()
