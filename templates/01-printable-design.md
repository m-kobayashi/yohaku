# テンプレ01: Printable(印刷用デジタル商品)制作

## [A] 入力契約(欠落時は生成せず停止し、不足項目をログに記録)
- `niche`: niches/active.md に存在する有効ニッチであること
- `product_concept`: 1文の商品コンセプト(daily-production が niche-scan 結果から供給)
- `slug`: 命名規則 `{niche}-printable-{連番3桁}`(listings.csv と products/ を確認し重複回避)

## [B] ブランド核(必ず先に読み込む)
1. `templates/brand/voice.md` — 文体・ペルソナを適用
2. `templates/brand/banned-words.md` — 全出力を照合
3. フォントは Google Fonts(商用可)のみ。使用フォントと出所を meta.yaml に記録

## [C] 生成手順(一発生成禁止。各ステップの成果を確認してから次へ)
1. **競合確認**: 同コンセプトのEtsy上位商品を1〜3件想起し、差別化点を1文で定義(WebSearch可なら実検索、不可ならニッチresearchログを参照)
2. **デザイン仕様書**: レイアウト・配色(ニッチのトーンに合わせる)・タイポグラフィ・収録ページ構成を `design/spec.md` に書く
3. **制作**: SVG または HTML+CSS で原稿を作成 → PDF化(A4 / US Letter の2サイズ必須、需要があれば A5/Half Letter追加)
   - 印刷余白: 全辺 0.25inch 以上 / 解像度: ラスタ要素は300dpi / カラー: RGB(家庭印刷前提)
4. **検証**: PDFを開いてレイアウト崩れ・フォント埋め込み・余白を確認(スクリプトまたは目視レビュー)
5. **同梱物**: `README.txt`(使い方・印刷推奨設定・ライセンス: 個人利用のみ、再販禁止)
6. **リスティング**: テンプレ03を呼び出して listing.md を生成
7. **配置**: `products/etsy/{niche}/{slug}/` に design/ mockups/ listing.md meta.yaml を揃える

## [D] セルフレビュー
- `templates/brand/quality-rubric.md` で採点(フォーマット厳守)
- 7点以上 → `review/pending/{slug}.md` にキューファイル作成(商品パス・採点・差別化点を記載)
- 7点未満 → 1回だけ自己修正 → なお不合格なら `review/rejected/{slug}.md` に理由・改善案を記録して破棄
