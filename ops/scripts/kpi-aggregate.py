#!/usr/bin/env python3
"""kpi-aggregate.py — 週次KPI CSVを集計し、前週比とCLAUDE.md判定基準の照合下書きを出力。

使い方: python3 ops/scripts/kpi-aggregate.py [出力先.md]
data/kpi/weekly/*.csv (metric,value 形式) を時系列に読み、直近週・前週比・推移を表にする。
標準ライブラリのみ使用。
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KPI_DIR = ROOT / "data" / "kpi" / "weekly"

METRICS = [
    "listings_live", "views", "visits", "favorites", "orders",
    "revenue_usd", "revenue_jpy", "cvr", "pins_live", "pin_impressions",
    "outbound_clicks", "new_listings", "expenses_jpy",
]


def load_week(path: Path) -> dict:
    data = {}
    with open(path) as f:
        for row in csv.reader(f):
            if len(row) >= 2 and row[0] != "metric":
                try:
                    data[row[0]] = float(row[1])
                except ValueError:
                    pass
    return data


def main():
    files = sorted(KPI_DIR.glob("*.csv"))
    if not files:
        print("KPIデータがまだありません (data/kpi/weekly/ が空)")
        return
    weeks = {f.stem: load_week(f) for f in files}
    names = list(weeks)
    cur_name, cur = names[-1], weeks[names[-1]]
    prev = weeks[names[-2]] if len(names) >= 2 else {}

    lines = [f"# KPIサマリー: {cur_name}", "", "| 指標 | 今週 | 前週 | 増減 |", "|---|---|---|---|"]
    for m in METRICS:
        c, p = cur.get(m), prev.get(m)
        if c is None:
            continue
        diff = f"{c - p:+.1f}" if p is not None else "—"
        lines.append(f"| {m} | {c:g} | {p if p is not None else '—'} | {diff} |")

    lines += ["", "## 判定下書き(CLAUDE.md基準との照合、人間が月曜に承認)"]
    views, listings = cur.get("views", 0), cur.get("listings_live", 0)
    favs, orders = cur.get("favorites", 0), cur.get("orders", 0)
    clicks = cur.get("outbound_clicks", 0)
    if listings:
        vpl = views / listings
        lines.append(f"- views/listing = {vpl:.1f}/週 (ニッチ撤退ライン: <30 かつ fav 0)")
        fav_rate = favs / views * 100 if views else 0
        lines.append(f"- fav率 = {fav_rate:.2f}% (増産ライン: ≧3%)")
    lines.append(f"- 今週売上件数 = {orders:g} (倍賭けライン: 週2件)")
    lines.append(f"- Pinterestクリック = {clicks:g}/週 (刷新ライン: 8週連続<50)")
    lines += ["", "※ニッチ別の内訳判定は listings.csv と突き合わせて /weekly-strategy 内で行う"]

    out = "\n".join(lines)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(out + "\n")
        print(f"書き出し: {sys.argv[1]}")
    else:
        print(out)


if __name__ == "__main__":
    main()
