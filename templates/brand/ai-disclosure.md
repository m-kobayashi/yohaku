# AI開示定型文(Etsy用)

Etsyの規約(2026年版)では、AI生成・AI支援コンテンツは「Designed by」カテゴリでの出品と開示が必須。
非開示は削除・アカウント停止の対象(2026Q1に12,000件以上削除の実績)。

## リスティング説明文に必ず含める文(英語・改変禁止)

```
✦ About this design: This item was designed with the assistance of AI tools,
with human curation, refinement, and quality review at every step.
```

## 出品時の設定(publish-assist で人間が目視確認する項目)
- [ ] 「How did you make it?」→ **Designed by (seller name)** を選択("I made it" は選ばない)
- [ ] 「Did you use AI?」に該当する設問があれば **Yes** を選択
- [ ] 説明文に上記開示文が含まれている(lint済みでも目視で再確認)

## lint仕様
- `listing.md` に上記英文の1行目(`About this design: This item was designed with the assistance of AI`)が含まれない場合、lint不合格
- pending へ進む全Etsy向け商品が対象

## 注意
- 開示文は説明文の末尾セクションに配置(冒頭はSEOと訴求を優先)
- Gumroad・Pinterestには現時点で同等の義務はないが、Gumroad商品ページにも同文を入れる(信頼性+規約変更への先回り)
- 規約変更を tos-watch が検知したら本ファイルを更新し、既存リスティングへの遡及対応を週次戦略会議で決定
