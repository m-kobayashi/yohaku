# テンプレ03: Etsyリスティング(タイトル・タグ・説明文・価格)生成

## [A] 入力契約(欠落時は生成せず停止)
- 商品フォルダ `products/etsy/{niche}/{slug}/` が存在し、design/ に成果物があること
- `design/spec.md` の差別化点が定義済みであること

## [B] ブランド核
1. `templates/brand/voice.md` — 説明文の文体に適用
2. `templates/brand/banned-words.md` — タイトル・タグ・説明文すべてを照合
3. **`templates/brand/ai-disclosure.md` の開示文を説明文末尾に必ず含める(改変禁止)**

## [C] 生成手順
1. **キーワード設計**: 主要キーワード1つ+ロングテール複合語(3〜4語)2つを選定。niches/research/ の調査ログを参照
2. **タイトル**(140字以内): 主要キーワードを前方配置。構成例: `{主要KW} | {用途/特徴} | {形式: Digital Download / Printable / SVG}`
   - ALL CAPSは2語まで。記号は `|` と `,` のみ
3. **タグ13個**(各20字以内): 主要KW・ロングテール・用途・スタイル・受け手(gift for…)・季節をミックス。13個すべて埋める。タイトルとの完全重複は7個まで
4. **説明文**構成(英語):
   - 冒頭2行: 何が買えるか+ベネフィット(検索プレビューに出る最重要部)
   - What's included: 収録物・サイズ・形式を箇条書き
   - How it works: 購入→DL→利用の3ステップ
   - 差別化点: spec.md の差別化点を自然な文で
   - FAQ: 印刷方法・ライセンス・返金ポリシー(デジタル商品につき返金不可、問題時はメッセージで対応)
   - 末尾: **AI開示文(ai-disclosure.md の定型文)**
5. **価格設定**: printable $4.5〜12 / SVGバンドル $8〜24 を基準に、競合上位の中央値±20%で設定。根拠を listing.md にコメントとして残す
6. **出力**: `products/etsy/{niche}/{slug}/listing.md` に title / tags / description / price_usd / keywords を構造化して保存。meta.yaml の `ai_disclosure: true` を確認

## [D] セルフレビュー
- quality-rubric.md(SEO適合軸を重点採点)
- `ops/scripts/lint-listing.sh {slug}` を実行し合格を確認(開示文・禁止語・必須フィールド)
- lint不合格はpendingに進めず修正。合格後に pending キューへ
