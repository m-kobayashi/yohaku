#!/usr/bin/env python3
"""kamon_svg.py — 日本の家紋(伝統意匠)をコードで正確に生成する制作ツール。

回転対称・幾何学構成の定番紋のみを扱う。特定の現存家系・企業商標になっている
紋(三菱スリーダイヤ等)は対象外。すべてパブリックドメインの汎用紋。
AIの画像生成ではなく数式で描画するため、対称性と比率が正確。標準ライブラリのみ。

使い方:
  python3 tools/kamon_svg.py <出力ディレクトリ> [カラー16進(既定 #1a1a1a)]
"""
import math
import os
import sys

SIZE = 200
C = SIZE / 2  # 中心 (100,100)


def _svg(body, color):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" '
        f'viewBox="0 0 {SIZE} {SIZE}">\n<g fill="{color}" stroke="{color}">\n{body}\n</g>\n</svg>\n'
    )


def _pt(d, deg, cx=C, cy=C):
    a = math.radians(deg)
    return (cx + d * math.cos(a), cy + d * math.sin(a))


def _circle(cx, cy, r):
    return f'  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}"/>'


def umebachi():
    """梅鉢: 中心円 + 5花弁円(72度間隔) + 白い花芯。"""
    parts = []
    for k in range(5):
        x, y = _pt(48, -90 + 72 * k)
        parts.append(_circle(x, y, 30))
    parts.append(_circle(C, C, 26))
    # 花芯を白抜き(背景色)で表現
    parts.append(f'  <circle cx="{C}" cy="{C}" r="10" fill="#ffffff"/>')
    return parts


def kuyo():
    """九曜: 中心の大円 + 周囲8つの円(45度間隔)。星紋。"""
    parts = [_circle(C, C, 34)]
    for k in range(8):
        x, y = _pt(70, 45 * k)
        parts.append(_circle(x, y, 21))
    return parts


def yotsume():
    """四つ目結: 中抜きの正方形4つを上下左右に(隅立て=45度配置)。"""
    parts = []
    out, inn = 30, 16
    for deg in (-90, 0, 90, 180):
        cx, cy = _pt(48, deg)
        # 外四角(時計回り) + 内四角(反時計回り) を evenodd で枠に
        o = (
            f"M{cx-out:.2f},{cy-out:.2f} h{2*out} v{2*out} h{-2*out} Z"
        )
        i = (
            f"M{cx-inn:.2f},{cy-inn:.2f} v{2*inn} h{2*inn} v{-2*inn} Z"
        )
        parts.append(f'  <path fill-rule="evenodd" d="{o} {i}"/>')
    return parts


def kikko():
    """亀甲: 正六角形の枠(中に小さな花菱)。"""
    def hexagon(R):
        pts = [_pt(R, -90 + 60 * k) for k in range(6)]
        d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
        return d
    outer = hexagon(78)
    inner = hexagon(58)
    parts = [f'  <path fill-rule="evenodd" d="{outer} {inner}"/>']
    # 中心に花菱(小さな菱)
    h = 18
    parts.append(
        f'  <path d="M{C},{C-h} L{C+h*0.7:.2f},{C} L{C},{C+h} L{C-h*0.7:.2f},{C} Z"/>'
    )
    return parts


def yotsuwari_bishi():
    """四つ割菱: 大菱形を十字の隙間で4分割した小菱形4つ。"""
    parts = []
    w, h = 32, 32      # 小菱の半幅・半高(正菱)
    off = 46           # 中心からのオフセット(十字の隙間を確保)
    for deg in (-90, 0, 90, 180):
        cx, cy = _pt(off, deg)
        parts.append(
            f'  <path d="M{cx:.2f},{cy-h} L{cx+w:.2f},{cy:.2f} '
            f'L{cx:.2f},{cy+h} L{cx-w:.2f},{cy:.2f} Z"/>'
        )
    return parts


def mitsudomoe():
    """三つ巴: 各勾玉=大円外周(頭120度) + 中心へ巻く半円弧2本。回転対称に3つ。"""
    parts = []
    R = 82
    for k in range(3):
        phi = -90 + 120 * k
        xs, ys = _pt(R, phi - 60)   # 頭の弧の始点
        xe, ye = _pt(R, phi + 60)   # 頭の弧の終点
        # 頭: 大円(R)外周120度 → 尾1: 半径R/2弧で中心へ → 尾2: 半径R/2弧で始点へ
        parts.append(
            f'  <path d="M{xs:.2f},{ys:.2f} '
            f'A{R},{R} 0 0 1 {xe:.2f},{ye:.2f} '
            f'A{R/2:.2f},{R/2:.2f} 0 0 1 {C},{C} '
            f'A{R/2:.2f},{R/2:.2f} 0 0 1 {xs:.2f},{ys:.2f} Z"/>'
        )
    return parts


KAMON = {
    "umebachi": umebachi,
    "kuyo": kuyo,
    "yotsume": yotsume,
    "kikko": kikko,
    "yotsuwari-bishi": yotsuwari_bishi,
    # "mitsudomoe": 未完成(渦の作図に改良要)。次バッチでベジェ曲線で再実装。バンドル未収録
}


def main():
    if len(sys.argv) < 2:
        sys.exit("使い方: python3 tools/kamon_svg.py <出力ディレクトリ> [色]")
    out = sys.argv[1]
    color = sys.argv[2] if len(sys.argv) > 2 else "#1a1a1a"
    os.makedirs(out, exist_ok=True)
    n = 0
    for name, fn in KAMON.items():
        body = "\n".join(fn())
        with open(os.path.join(out, f"kamon-{name}.svg"), "w") as f:
            f.write(_svg(body, color))
        n += 1
    print(f"生成完了: {n} ファイル → {out}")


if __name__ == "__main__":
    main()
