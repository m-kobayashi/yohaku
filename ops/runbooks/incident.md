# 障害・緊急時対応

## ops/STOP による全ジョブ停止
- 作成: `echo "理由と日付" > ops/STOP` — 全自動ジョブが次回実行時から停止
- 解除: 原因対処後に `rm ops/STOP`(人間の判断でのみ)

## ケース別対応
### Etsyから警告・リスティング削除が来た
1. `ops/STOP` を作成(出品系ジョブ停止)
2. 警告内容をClaudeに見せ、原因分析(開示漏れ/禁止語/商標)と影響範囲(他リスティングへの波及)を出させる
3. 該当リスティングを修正または自主的に取り下げ
4. `templates/brand/banned-words.md` / lint に再発防止を追記してから再開

### アカウントBAN
- products/ がマスターデータなので在庫は無傷。週次戦略会議で代替プラットフォーム(Gumroad拡充/Lemon Squeezy)への展開を判断
- 異議申し立てはEtsyヘルプから(テンプレ文面はClaudeが作成)

### cronが動いていない
- `crontab -l` で登録確認 / `logs/cron-*.log` の最終更新を確認
- Macがスリープしていた場合: `pmset repeat wakeorpoweron MTWRFSU 05:25:00` を設定、または手動で `/daily-production` を実行(取りこぼし分は翌日にまとめて生産しない。上限厳守)
- 恒常的にスリープ問題が出る場合は launchd 化: `~/Library/LaunchAgents/` に plist を作成(ClaudeにStartCalendarInterval版を生成させる)

### レート取得失敗(ledger-jpy.py)
- frankfurter.app 障害時はキャッシュの最終レートで暫定計算される。月次締めで再計算すれば問題なし
