# 出品アシスト(週1〜2回・人間同席15分)— Claude in Chrome使用

approved の商品をEtsy/Pinterestに出品する。**最終のPublishクリックは必ず人間が行う。**

## 事前条件
- 人間が画面の前にいること(headlessでは実行しない)
- `review/approved/` に出品待ちがあること(なければ pending の承認から始める)

## 手順
1. **承認セッション**: `review/pending/` の各キューを人間に要約提示(商品名・採点・差別化点・価格)。人間がOK/NGを判断 → OKは `review/approved/` へ、NGは理由を聞いて `review/rejected/` へ(理由は必ず記録)
2. **Etsy出品**(Claude in Chromeでフォーム入力、人間が確認):
   - listing.md の title/tags/description/price を入力
   - 画像(mockups/)をアップロード
   - **人間の目視確認項目**(`templates/brand/ai-disclosure.md` 参照):
     - [ ] 「How did you make it?」= Designed by
     - [ ] AI使用設問 = Yes
     - [ ] 説明文末尾に開示文
   - **Publishボタンは人間がクリック**
3. **Pinterest投稿**: 出品済み商品のピン(products/pinterest/)を投稿。リンク先URLを実リスティングURLに更新してから投稿。人間が最終確認
4. **記録**: `data/listings.csv` を status=listed, url, listed_date, fee_usd=0.20 で更新。`data/expenses.csv` にリスティング費を追記
5. **KPIキャプチャ(同セッション5分)**: Etsy Shop Manager の統計画面から views/visits/favorites/orders を読み取り、`data/kpi/weekly/{今週}.csv` に記録

## 原則
- 1セッション15分以内を目安に。間に合わない分は次回(質を犠牲にしない)
- フォーム入力中にEtsyのUI・設問が変わっていたら、その差分を `ops/runbooks/` に追記して人間に報告
