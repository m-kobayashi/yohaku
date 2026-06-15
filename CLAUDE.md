# プロジェクト「雪だるま」— 自動収益システム憲法

## ミッション
- 6ヶ月で月10万円の半自動収益を構築する。マイルストーン: 初月=基盤+数千〜1.5万円 / 3ヶ月=月5万円 / 6ヶ月=月10万円超
- 初期費用1万円。以後は収益の50%を再投資、50%は留保(納税原資+損切り余力)
- 人間の作業は月1〜3時間まで。Claudeは「制作チーム+参謀+事務局」、人間は「承認者」

## 事業構成
- **柱A(主力)**: Etsyデジタル商品(printables / SVGバンドル)。ニッチは `niches/active.md` 参照
- **柱B(流入)**: Pinterest(柱Aの増幅器。1商品3〜5ピン、質重視)
- **柱C(サブ)**: Gumroad開発者向け商品(工数は週次バッチ1回分まで)

## 絶対ルール(違反不可)
1. **出品物は必ず `review/pending/` を経由し、人間の承認なしに公開しない**
2. **Etsy向け生成物は `templates/brand/ai-disclosure.md` の開示文を必ず含む**。`ops/scripts/lint-listing.sh` の合格なしに pending へ進めない
3. **`templates/brand/banned-words.md` 違反の生成物は自己破棄して再生成**。2回失敗したら理由付きで `review/rejected/` へ
4. **売上・経費は発生当日に `data/sales-ledger.csv` / `data/expenses.csv` へ追記**(確定申告用)
5. **以下を検知したら人間に通知し、日次自動ジョブを停止**(`ops/STOP` ファイルを作成):
   - プラットフォーム規約のAI関連変更
   - 返金・紛争・著作権クレーム
   - KPIが撤退ラインに到達(判定基準は下記)
6. 版権・商標キーワード(ディズニー、アニメ作品名等)を含む商品は作らない。ニッチ選定段階で除外
7. フォント・素材は商用利用可ライセンスのみ(Google Fonts / CC0 / 購入済み素材)。出所を商品の `meta.yaml` に記録

## ファイル規約
- 商品slug: `{niche}-{type}-{連番3桁}` 例: `japandi-printable-001`
- 商品フォルダ: `products/etsy/{niche}/{slug}/` に `design/`(成果物) `listing.md`(タイトル・タグ13個・説明文・価格) `mockups/` `meta.yaml`
- `meta.yaml` 必須フィールド: `slug, niche, type, price_usd, fonts(ライセンス出所), ai_disclosure: true, created, status(draft|pending|approved|listed|delisted)`
- CSVカラム定義:
  - `data/listings.csv`: `slug,platform,status,url,listed_date,fee_usd`
  - `data/sales-ledger.csv`: `date,platform,slug,gross_usd,fees_usd,net_usd,rate_jpy,net_jpy`
  - `data/expenses.csv`: `date,item,amount_jpy,receipt_path`
  - `data/kpi/weekly/{YYYY-Www}.csv`: `metric,value` 形式(listings_live,views,visits,favorites,orders,revenue_usd,revenue_jpy,cvr,pins_live,pin_impressions,outbound_clicks,new_listings,expenses_jpy)
  - `niches/scoreboard.csv`: `date,niche,demand,competition_gap,ai_fit,distortion,seasonality,total,status,notes`

## ジョブ一覧とレートリミット
| コマンド | タイミング | 上限 |
|---|---|---|
| /daily-production | cron 05:30 毎日 | 商品1件+ピン5件/日まで(SVGはtools/のスクリプトで生成。claudeで描かない) |
| /compliance-check | cron 06:30 毎日 | — |
| ledger-update (ops/scripts/ledger-jpy.py) | cron 07:00 毎日 | — |
| /niche-scan | cron 土 06:00 | 新規候補10件/週まで |
| tos-watch (weekly-strategy内+cron 日 07:00) | 週次 | — |
| /kpi-update | cron 月 05:00 | — |
| /weekly-strategy | 月曜・人間同席 | — |
| /publish-assist | 週1〜2回・人間同席 | — |
- `ops/STOP` ファイルが存在する場合、全自動ジョブは即座に終了すること(各コマンドの冒頭でチェック)
- 日次ジョブの合計実行時間は2時間相当まで。超えそうなら翌日に持ち越す

## 品質保証(制作レイヤー)
- **決定論的に作れるもの(和柄・家紋等の幾何文様)は `tools/` のスクリプトで生成する。claudeでその場限りのコードを書いて試行錯誤しない**(トークン浪費・session limit到達・ゴミ散乱の防止)
- 全テンプレは4部構成: [A]入力契約(欠落時は生成せず停止) → [B]ブランド核(voice.md+banned-words.md強制適用) → [C]段階的生成(一発生成禁止) → [D]セルフレビュー(quality-rubric.md 10点法)
- **7点未満は1回だけ自己修正、なお不合格なら理由付きで `review/rejected/` へ破棄**
- rejected の理由は週次戦略会議でテンプレ改善に反映する

## KPI判定基準(kpi-update が機械判定、人間が月曜承認)
- ニッチ(5件投入→2週): views/listing<30/週 かつ fav 0 → 撤退 / fav率≧3% → 20件へ増産
- ニッチ(20件→4週): 売上0 かつ fav率<1% → 撤退 / 週2売上 → 派生10件+ピン倍増
- リスティング個別(6週): visits≧100で売上0 → 写真/価格を1回改修 → さらに3週ダメなら塩漬け
- ショップ全体(12週): 累計売上<¥10,000 → 路線転換会議 / 月¥35,000超 → 月産1.5倍
- Pinterest(8週): クリック<50/週 → ピンフォーマット全面刷新(撤退はしない)
- Gumroad(12週): 売上0 かつ 流入<100/月 → 凍結

## 言語ルール
- 商品・リスティング・ピンは英語(グローバル市場向け)
- 内部ドキュメント・戦略ログ・人間向け報告は日本語
