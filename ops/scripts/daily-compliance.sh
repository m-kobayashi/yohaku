#!/bin/bash
# daily-compliance.sh — claude不要の日次コンプライアンス検査。
# 実体は lint-listing.sh --all(AI開示・禁止語・必須フィールドの機械検証)。
# claudeを起動しないのでトークン消費ゼロ。FAIL時はログを目立たせ、当日の
# 日次レポートにも残す(出品前の最後の砦なので人間が気づけるように)。
#
# 使い方: daily-compliance.sh [ログファイルの絶対パス]
set -u
PROJ=/Users/kobayashi/develop/11_AI/private
cd "$PROJ" || exit 1
LOG="${1:-$PROJ/logs/cron-compliance.log}"
DATE=$(date '+%F %T')

# 緊急停止
if [ -f ops/STOP ]; then
  echo "$DATE SKIP (ops/STOP あり)" >> "$LOG"
  exit 0
fi

OUT=$(bash ops/scripts/lint-listing.sh --all 2>&1)
RC=$?
{
  echo "$DATE daily-compliance (lint --all, rc=$RC)"
  echo "$OUT"
} >> "$LOG"

if [ "$RC" -ne 0 ]; then
  REPORT="logs/$(date +%F)-compliance.md"
  {
    echo "# $DATE 日次コンプライアンス: lint FAIL検知"
    echo ""
    echo '```'
    echo "$OUT"
    echo '```'
    echo ""
    echo "→ 出品前に要修正。禁止語/AI開示漏れ/必須フィールド欠落のいずれか。"
    echo "  修正が判断を要する場合のみ \`/compliance-check\` をclaudeで実行。"
  } >> "$REPORT"
  echo "$DATE !!! lint FAIL → $REPORT に記録" >> "$LOG"
fi
exit 0
