#!/usr/bin/env python3
"""wagara_svg.py — 和柄(日本の伝統幾何学文様)のシームレスSVGをコードで正確に生成する制作ツール。

AIの画像生成ではなく数学的に描画するため、紋様の幾何学的正確性が保証される
(= 文化的正確性が差別化になる)。標準ライブラリのみ。

使い方:
  python3 tools/wagara_svg.py <出力ディレクトリ>
全パターン × 全カラーのSVGを出力ディレクトリに書き出す。
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

SIZE = 800  # viewBox一辺(px)


def _svg(size, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">\n{body}\n</svg>\n'
    )


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
    vp = R / 2            # 縦ピッチ(半径の半分ずつ重ねる=鱗)
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
                # (cx-r,cy)→(cx+r,cy) を上側(y小)で結ぶ半円: sweep=1
                paths.append(
                    f'  <path d="M{cx-r:.2f},{cy:.2f} A{r:.2f},{r:.2f} 0 0 1 '
                    f'{cx+r:.2f},{cy:.2f}" fill="none" stroke="{color}" stroke-width="2.5"/>'
                )
    return _svg(size, "\n".join(paths))


PATTERNS = {
    "ichimatsu": ichimatsu,
    "shippo": shippo,
    "seigaiha": seigaiha,
}


def main():
    if len(sys.argv) < 2:
        sys.exit("使い方: python3 tools/wagara_svg.py <出力ディレクトリ>")
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    count = 0
    for pname, fn in PATTERNS.items():
        for cname, color in PALETTE.items():
            svg = fn(color)
            path = os.path.join(out, f"{pname}-{cname}.svg")
            with open(path, "w") as f:
                f.write(svg)
            count += 1
    print(f"生成完了: {count} ファイル → {out}")


if __name__ == "__main__":
    main()
