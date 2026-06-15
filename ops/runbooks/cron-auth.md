# cron/headless 認証セットアップ(claude -p を自動実行するため)

## 症状と原因
- cronの `claude -p` ジョブが「Not logged in · Please run /login」で失敗する
- 原因: 対話ログインの認証は **macOS Keychain** に保存され、cron(無人実行)からは読めない
- python/git ジョブは claude 不要なので影響なし(動作している)

## 解決手順(人間が一度だけ実行)

### 1. 長期トークンを発行
対話ターミナルで実行(ブラウザ認証が開く)。**Maxサブスクのまま使えます**:
```
claude setup-token
```
→ 1年有効のOAuthトークン(`sk_...`)が表示される。コピーする。
(このセッション内なら `! claude setup-token` でも実行可)

### 2. トークンを安全なファイルに保存(600パーミッション)
```
printf 'export CLAUDE_CODE_OAUTH_TOKEN=%s\n' 'sk_ここに貼る' > ~/.claude/.oauth-token-env
chmod 600 ~/.claude/.oauth-token-env
```
※ プロジェクト外(~/.claude/)に置くのでGitには絶対入らない。

### 3. crontab を反映(ラッパー方式に更新済み)
```
crontab ops/cron/crontab.txt   # 全置換
crontab -l                     # 確認
```

### 4. 動作テスト(その場で1回実行)
```
ops/cron/run-claude-job.sh "/compliance-check 日次検査のみ実行" /tmp/test-claude-job.log
cat /tmp/test-claude-job.log    # "Not logged in" が消え、正常に動けばOK
```

## コスト注意(2026-06-15〜)
- この日からMaxサブスクの `claude -p`/Agent SDK利用に**月額$200相当の専用クレジット枠**が自動適用され、対話利用枠と分離される
- daily-production(1日数件生成)程度なら枠内に収まる見込みだが、超過分は従量課金になりうる
- 対策: 生成上限(商品案3件+ピン10件/日)を厳守。枠消費が大きければ週次戦略会議で頻度・量を調整

## 確実性を上げたい場合: launchd 化(任意・推奨)
cron は Mac スリープ中に動かない。launchd ならスリープ復帰後も実行される。
`~/Library/LaunchAgents/com.yohaku.<job>.plist` を作成し、Program に run-claude-job.sh、
StartCalendarInterval に時刻、EnvironmentVariables に HOME/PATH を設定して
`launchctl load` する。plist雛形が必要ならClaudeに生成させる。

## トークン期限切れ時(約1年後)
`claude setup-token` を再実行し、手順2で `~/.claude/.oauth-token-env` を上書きする。
