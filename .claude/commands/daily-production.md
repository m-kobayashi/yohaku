# 日次量産ジョブ(制作レイヤー)

毎朝の自動実行。商品案の生成からpendingキュー投入までを行う。

## 手順
1. **停止チェック**: `ops/STOP` が存在したら「STOPファイルあり」とログに記録して即終了
2. **本日の生産計画**: `niches/active.md` の注力ニッチと検証ステータスを読み、本日の生産割当を決める
   - 上限: 商品案3件+ピン10件/日(CLAUDE.md)
   - 検証中ニッチ(5件未満)を優先し、増産指示(20件化)があるニッチに残りを割当
   - 出品済み商品でピンが5本未満のものがあればピン生産に割当
3. **商品制作**: 各商品案について `templates/01-printable-design.md` または `templates/02-svg-bundle.md` を厳密に実行(4部構成: 入力契約→ブランド核→段階的生成→セルフレビュー)
4. **リスティング生成**: `templates/03-etsy-listing.md` を実行し、`ops/scripts/lint-listing.sh {slug}` で検証
5. **ピン制作**: `templates/04-pinterest-pin.md` を実行
6. **キュー投入**: rubric 7点以上+lint合格のものだけ `review/pending/{slug}.md` を作成(商品パス・採点・差別化点・人間が確認すべき点を記載)
7. **ログ**: `logs/{YYYY-MM-DD}-daily.md` に生産数・合格数・rejected数・所要の概要を記録
8. **listings.csv 更新**: 新規 pending 分は status=pending で追記

## 禁止事項
- 人間の承認なしにいかなる外部公開も行わない(出品・ピン投稿・SNS投稿すべて)
- 上限超過の生産(質が下がるだけでなくAIスロップ判定リスク)
