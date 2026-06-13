# コンプライアンス検査(日次)+ 規約変更監視(週次・日曜)

## 日次: pending全件の機械検証
1. **停止チェック**: `ops/STOP` があれば即終了
2. `bash ops/scripts/lint-listing.sh --all` を実行
3. FAIL の商品は `review/pending/` から差し戻し:
   - 自動修正可能(開示文欠落・タグ数)→ 修正して再lint
   - 禁止語違反 → 該当箇所を voice.md 準拠で書き直し再lint。2回失敗で rejected へ
4. meta.yaml の `status` と review/ キューの整合を確認(approved なのに pending に残っている等)
5. 結果を `logs/{YYYY-MM-DD}-compliance.md` に記録

## 週次(日曜): tos-watch — 規約変更の検知
1. WebSearch で以下を確認(過去7日のニュース・公式発表):
   - Etsy: AI生成コンテンツポリシー、Creativity Standards、手数料変更
   - Pinterest: AI生成ピン・スパムポリシー
   - Gumroad: AIコンテンツ・手数料
2. 変更を検知したら:
   - `ops/STOP` ファイルを作成(理由を中に書く)→ 日次ジョブ停止
   - `strategy/weekly/{今週}.md` にアラートを追記し、影響範囲と対応案(既存リスティングの遡及修正要否)を整理
   - 人間への報告を最優先(次回セッション冒頭で必ず提示)
3. 変更なしなら `logs/` に「変更なし」を記録

## STOPファイルの運用
- `ops/STOP` の中身: 日付・理由・解除条件
- 解除は人間の指示でのみ行う(削除して再開)
