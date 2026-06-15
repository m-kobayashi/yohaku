#!/bin/bash
# run-claude-job.sh — cron/launchd から Claude Code を headless 実行するラッパー
#
# 背景: 対話ログインの認証は macOS Keychain に保存され、cron からは読めない
# (Not logged in になる)。そこで `claude setup-token` で発行した長期OAuthトークンを
# 600パーミッションのenvファイルから読み込んで認証する。
#
# 使い方: run-claude-job.sh "<プロンプト>" "<ログファイルの絶対パス>"
set -u

export HOME=/Users/kobayashi
export PATH=/Users/kobayashi/.local/bin:/usr/local/bin:/usr/bin:/bin
PROJ=/Users/kobayashi/develop/11_AI/private
TOKEN_ENV="$HOME/.claude/.oauth-token-env"

PROMPT="${1:?プロンプトを指定してください}"
LOG="${2:-$PROJ/logs/cron-claude.log}"

cd "$PROJ" || exit 1

# 緊急停止スイッチ
if [ -f ops/STOP ]; then
  echo "$(date '+%F %T') SKIP (ops/STOP あり): $PROMPT" >> "$LOG"
  exit 0
fi

# 認証トークン
if [ ! -f "$TOKEN_ENV" ]; then
  echo "$(date '+%F %T') ERROR: $TOKEN_ENV がありません。" >> "$LOG"
  echo "  → 'claude setup-token' でトークンを発行し設定してください (ops/runbooks/cron-auth.md)" >> "$LOG"
  exit 1
fi
# shellcheck disable=SC1090
. "$TOKEN_ENV"            # export CLAUDE_CODE_OAUTH_TOKEN=...
unset ANTHROPIC_API_KEY  # 古い/無効なAPIキーがOAuthトークンより優先されるのを防ぐ

echo "$(date '+%F %T') START: $PROMPT" >> "$LOG"
claude -p "$PROMPT" --permission-mode acceptEdits >> "$LOG" 2>&1
echo "$(date '+%F %T') END (exit=$?): $PROMPT" >> "$LOG"
