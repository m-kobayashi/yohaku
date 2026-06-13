# 月次作業(人間、10〜15分)

- [ ] **入金確認**: Payoneer→銀行口座の着金を確認。`data/sales-ledger.csv` と金額照合(差異があればClaude に調査させる)
- [ ] **証憑保存**: Payoneer/Etsy/Gumroadの月次明細PDFをダウンロードし `data/receipts/{YYYY-MM}/` に保存、`expenses.csv` の receipt_path を更新
- [ ] **再投資承認**: 当月純収益の50%の使途(weekly-strategyの提案)を最終承認
- [ ] **20万円ライン確認**: `python3 ops/scripts/ledger-jpy.py` の出力を確認。年間雑所得が20万円に近づいたら確定申告準備(20万円以下でも住民税申告は必要)

## 確定申告メモ
- 雑所得 = 売上(円換算済net) − 経費(リスティング費・ツール代・素材代)
- 帳簿は sales-ledger.csv / expenses.csv がそのまま根拠資料になる
- 為替はTTMレート(ledger-jpy.pyがfrankfurter.appのレートで自動換算。厳密にはみずほ等のTTM公表値で締め時に再計算)
