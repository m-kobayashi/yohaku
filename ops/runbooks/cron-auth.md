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

## コスト(2026-06-15〜のAgent SDK課金変更)
- claude -p/Agent SDK利用が対話利用枠と分離。**Max 20xにはagent専用クレジット月$200相当がサブスクに含まれる形で付く(追加料金ではない)**。Max 5xは$100
- クレジットを使い切ると自動ジョブは**停止する**(overage/API課金を明示的に有効化しない限り課金されない=コスト暴走なし)。未使用分は繰越不可
- daily-production(1日数件)程度は$200枠に十分収まる見込み。むしろheadless専用枠ができ、対話利用枠を食わなくなる
- 枠消費は週次で監視。万一止まったら頻度調整 or overage有効化を判断
- 出典: support.claude.com/en/articles/15036540

## 確実性を上げたい場合: launchd 化(任意・推奨)
cron は Mac スリープ中に動かない。launchd ならスリープ復帰後も実行される。
`~/Library/LaunchAgents/com.yohaku.<job>.plist` を作成し、Program に run-claude-job.sh、
StartCalendarInterval に時刻、EnvironmentVariables に HOME/PATH を設定して
`launchctl load` する。plist雛形が必要ならClaudeに生成させる。

## トークン期限切れ時(約1年後)
`claude setup-token` を再実行し、手順2で `~/.claude/.oauth-token-env` を上書きする。
