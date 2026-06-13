# テンプレ02: SVGバンドル制作

## [A] 入力契約(欠落時は生成せず停止)
- `niche` / `bundle_theme`(例: "Japandi minimal wall art set")/ `slug`: `{niche}-svg-{連番3桁}`
- バンドルサイズ: 10〜20点(10点未満は商品力不足、20点超は制作コスト過大)

## [B] ブランド核
1. `templates/brand/voice.md` / `templates/brand/banned-words.md` を適用
2. モチーフに版権・商標要素が混入していないか、banned-words.md §3 で確認

## [C] 生成手順
1. **テーマ統一感の設計**: バンドル全体のスタイルガイド(線幅・モチーフ語彙・構図ルール)を `design/spec.md` に定義。バラバラな寄せ集めは0点要因
2. **SVG制作**: 各点を個別ファイルで作成。要件:
   - すべてのパスが閉じている(fill対応)
   - テキストはアウトライン化(フォント依存なし)
   - viewBox 設定済み、単一色レイヤー構成(カットマシン互換)
   - 不要なグループ・空要素なし
3. **互換検証**: Cricut / Silhouette での利用を想定し、`ops/scripts/` の検証(なければ目視+構造チェック)でパス閉じ・サイズを確認
4. **形式展開**: SVG + PNG(透過、300dpi相当)+ 可能なら DXF/EPS
5. **同梱物**: `README.txt`(対応ソフト・ライセンス: 個人利用+小規模物販可/デジタル再販禁止 を明記)
6. **リスティング**: テンプレ03で listing.md 生成(「{N} designs included」を明記)
7. **配置**: `products/etsy/{niche}/{slug}/`

## [D] セルフレビュー
- quality-rubric.md で採点。技術品質の採点はパス閉じ・アウトライン化・viewBox の3点検証結果を理由に含めること
- 統一感(独自性軸で評価)が弱い場合は、外れている数点を作り直してから再採点
- 合格 → `review/pending/{slug}.md` / 不合格 → `review/rejected/{slug}.md`
