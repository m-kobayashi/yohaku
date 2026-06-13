#!/usr/bin/env python3
"""ledger-jpy.py — 売上台帳の円換算と雑所得20万円ライン監視。

- data/sales-ledger.csv の rate_jpy / net_jpy 未記入行を当日USDJPYレートで補完
- レートは open.er-api.com → frankfurter.dev の順で取得(無料・キー不要)、data/fx-rates.csv にキャッシュ
- 年初来の純収入(net_jpy)・経費・雑所得進捗(20万円ライン)を出力
標準ライブラリのみ使用。
"""
import csv
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data" / "sales-ledger.csv"
EXPENSES = ROOT / "data" / "expenses.csv"
FX_CACHE = ROOT / "data" / "fx-rates.csv"
THRESHOLD_JPY = 200_000  # 雑所得の確定申告ライン


def get_rate(today: str) -> float:
    """当日のUSDJPYレートを取得(キャッシュ優先)。"""
    if FX_CACHE.exists():
        with open(FX_CACHE) as f:
            for row in csv.reader(f):
                if row and row[0] == today:
                    return float(row[1])
    sources = [
        ("https://open.er-api.com/v6/latest/USD", lambda d: d["rates"]["JPY"]),
        ("https://api.frankfurter.dev/v1/latest?base=USD&symbols=JPY", lambda d: d["rates"]["JPY"]),
    ]
    rate = None
    for url, extract in sources:
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                rate = extract(json.load(r))
            break
        except Exception as e:
            print(f"WARN: レート取得失敗 {url} ({e})")
    if rate is None:
        print("WARN: 全ソース失敗。キャッシュの最終レートを使用")
        if FX_CACHE.exists():
            with open(FX_CACHE) as f:
                rows = [r for r in csv.reader(f) if r]
            if rows:
                return float(rows[-1][1])
        sys.exit("ERROR: レートが取得できず、キャッシュもありません")
    new = not FX_CACHE.exists()
    with open(FX_CACHE, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "usdjpy"])
        w.writerow([today, rate])
    return rate


def main():
    today = date.today().isoformat()
    if not LEDGER.exists():
        sys.exit(f"ERROR: {LEDGER} がありません")

    with open(LEDGER) as f:
        rows = list(csv.DictReader(f))
    fields = ["date", "platform", "slug", "gross_usd", "fees_usd", "net_usd", "rate_jpy", "net_jpy"]

    rate = None
    updated = 0
    for row in rows:
        if row.get("net_usd") and not row.get("net_jpy"):
            if rate is None:
                rate = get_rate(today)
            row["rate_jpy"] = f"{rate:.2f}"
            row["net_jpy"] = f"{float(row['net_usd']) * rate:.0f}"
            updated += 1
    if updated:
        with open(LEDGER, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    year = today[:4]
    revenue = sum(float(r["net_jpy"]) for r in rows if r.get("net_jpy") and r["date"].startswith(year))
    expenses = 0.0
    if EXPENSES.exists():
        with open(EXPENSES) as f:
            expenses = sum(
                float(r["amount_jpy"]) for r in csv.DictReader(f)
                if r.get("amount_jpy") and r["date"].startswith(year)
            )
    income = revenue - expenses
    print(f"=== 台帳サマリー ({today}) ===")
    print(f"円換算を補完した行: {updated}")
    print(f"年初来 純売上: ¥{revenue:,.0f}")
    print(f"年初来 経費:   ¥{expenses:,.0f}")
    print(f"年初来 雑所得: ¥{income:,.0f} / 確定申告ライン ¥{THRESHOLD_JPY:,} ({income / THRESHOLD_JPY * 100:.1f}%)")
    if income > THRESHOLD_JPY * 0.8:
        print("NOTICE: 雑所得が20万円ラインの80%を超えました。確定申告の準備を runbook 参照で開始してください")


if __name__ == "__main__":
    main()
