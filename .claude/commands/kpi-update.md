# KPI集計・判定下書き(週次・月曜早朝の自動実行)

週次戦略会議(weekly-strategy)の入力を準備する。

## 手順
1. **停止チェック**: `ops/STOP` があれば即終了
2. `python3 ops/scripts/ledger-jpy.py` を実行(円換算補完+20万円ライン確認)
3. `data/kpi/weekly/{今週YYYY-Www}.csv` が未作成なら、取得済みデータ(kpi-captureでの取り込み分、listings.csv、sales-ledger.csv)から埋められる指標を埋めて作成
   - Etsy統計画面由来の指標(views/visits/favorites)が未取得の場合は「要キャプチャ」とマークし、publish-assist セッションで取得するよう `strategy/weekly/{今週}.md` の冒頭に明記
4. `python3 ops/scripts/kpi-aggregate.py strategy/weekly/{今週YYYY-Www}.md` で判定下書きを生成
5. 下書きに以下を追記:
   - ニッチ別内訳(listings.csv と売上を突き合わせ、ニッチごとの views/fav/売上)
   - CLAUDE.md判定基準に該当した項目の一覧(撤退候補・増産候補)
   - 経費・再投資可能額(今期収益の50%)
6. 撤退ライン到達のニッチがあれば、その旨をログと下書きに**目立つ形で**記載(自動では撤退しない。人間が月曜に承認)

## 出力
`strategy/weekly/{YYYY-Www}.md`(weekly-strategy がこのファイルを開いて会議を始める)
