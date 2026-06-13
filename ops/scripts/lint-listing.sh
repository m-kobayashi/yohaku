#!/bin/bash
# lint-listing.sh — Etsy向けリスティングの機械検証(AI開示・禁止語・必須フィールド)
# 使い方:
#   ops/scripts/lint-listing.sh <slug>     # 単一商品を検証
#   ops/scripts/lint-listing.sh --all      # products/etsy 配下の全 listing.md を検証
# 終了コード: 0=全合格 / 1=不合格あり

set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BANNED="$ROOT/templates/brand/banned-words.txt"
DISCLOSURE="About this design: This item was designed with the assistance of AI"
FAIL=0

lint_one() {
  local listing="$1"
  local dir slug errors=()
  dir="$(dirname "$listing")"
  slug="$(basename "$dir")"

  # 1. AI開示文
  if ! grep -qF "$DISCLOSURE" "$listing"; then
    errors+=("AI開示文がありません (templates/brand/ai-disclosure.md の定型文を末尾に追加)")
  fi

  # 2. 禁止語(大文字小文字無視)
  if [ -f "$BANNED" ]; then
    local hits
    hits="$(grep -i -n -F -f "$BANNED" "$listing" | head -5)"
    if [ -n "$hits" ]; then
      errors+=("禁止語を検出: ${hits}")
    fi
  fi

  # 3. meta.yaml 必須フィールド
  local meta="$dir/meta.yaml"
  if [ ! -f "$meta" ]; then
    errors+=("meta.yaml がありません")
  else
    grep -q "ai_disclosure: true" "$meta" || errors+=("meta.yaml に ai_disclosure: true がありません")
    grep -q "^slug:" "$meta" || errors+=("meta.yaml に slug がありません")
    grep -q "^price_usd:" "$meta" || errors+=("meta.yaml に price_usd がありません")
    grep -q "^fonts:" "$meta" || errors+=("meta.yaml に fonts(ライセンス出所)がありません")
  fi

  # 4. タグ数(# Tags セクションのカンマ区切りが13個)
  local tags
  tags="$(awk '/^# Tags/{flag=1;next}/^# /{flag=0}flag' "$listing" | tr ',' '\n' | sed '/^[[:space:]]*$/d' | wc -l | tr -d ' ')"
  if [ "$tags" != "13" ]; then
    errors+=("タグ数が13ではありません (検出: ${tags})")
  fi

  # 5. タイトル長(140字以内)
  local title_len
  title_len="$(awk '/^# Title/{flag=1;next}/^# /{flag=0}flag' "$listing" | tr -d '\n' | wc -c | tr -d ' ')"
  if [ "$title_len" -gt 140 ]; then
    errors+=("タイトルが140字を超えています (${title_len}字)")
  fi

  if [ "${#errors[@]}" -eq 0 ]; then
    echo "PASS: $slug"
  else
    echo "FAIL: $slug"
    for e in "${errors[@]}"; do echo "  - $e"; done
    FAIL=1
  fi
}

if [ "${1:-}" = "--all" ]; then
  found=0
  while IFS= read -r f; do
    found=1
    lint_one "$f"
  done < <(find "$ROOT/products/etsy" -name listing.md 2>/dev/null)
  [ "$found" -eq 0 ] && echo "対象の listing.md がありません"
elif [ -n "${1:-}" ]; then
  match="$(find "$ROOT/products/etsy" -type d -name "$1" 2>/dev/null | head -1)"
  if [ -z "$match" ] || [ ! -f "$match/listing.md" ]; then
    echo "FAIL: slug '$1' の listing.md が見つかりません"
    exit 1
  fi
  lint_one "$match/listing.md"
else
  echo "使い方: $0 <slug> | --all"
  exit 1
fi

exit $FAIL
