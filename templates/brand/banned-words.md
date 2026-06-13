# 禁止語・禁止表現リスト

lint対象。生成物(リスティング・ピン・商品説明)にこれらが含まれる場合は自己破棄して再生成する。

## 1. AI隠蔽につながる表現(Etsy BAN直結・最重要)
非手描き・AI生成の商品に対して以下を使うことを禁止:
- hand-drawn / hand drawn / handdrawn
- hand-painted / hand painted
- hand-lettered / hand lettering(実際に手書きでない場合)
- handmade(デジタル商品自体に使わない。"digital download" を明示)
- original artwork by me(AI併用の場合)
- watercolor painted by hand

## 2. 誇大表現(Etsyスパム判定・返金リスク)
- life-changing / life changing
- guaranteed / guarantee(収益・効果の保証)
- best in the world / #1 / number one
- miracle / magical results
- 100% effective
- get rich / make money fast

## 3. 商標・版権(アカウント停止リスク)
商品名・タグ・説明文に以下のカテゴリを含めない:
- ディズニー/ピクサー関連(Disney, Mickey, Frozen, etc.)
- 任天堂/ポケモン関連(Pokemon, Mario, Zelda, etc.)
- アニメ・漫画作品名(Ghibli, Totoro, Naruto, One Piece, Demon Slayer, etc.)
- ブランド名(Nike, Apple, Starbucks, Louis Vuitton, etc.)
- セレブリティ・実在人物名
- スポーツチーム・リーグ名(NFL, NBA, etc.)
- "inspired by {版権物}" の形式も不可

## 4. Etsyポリシー抵触語
- COVID / vaccine 関連の医療効能
- 武器・規制品を連想させる語
- 金融・医療・法律アドバイスの断定表現(cure, treat, legal advice)

## 5. ブランドボイス違反(voice.md と整合)
- 過度なスラング(lit, fire, slay 等)
- ALL CAPS の多用(タイトル内2語まで)
- 絵文字の商品説明文での使用(ピンのテキストオーバーレイも不可。タグは対象外)
- 安売り訴求(cheap, cheapest)。価値訴求(affordable は可)

## lint実装メモ
- 大文字小文字を無視してマッチ
- 「3. 商標・版権」はニッチ選定段階(`/niche-scan`)でも除外フィルタとして使用
- 新しい違反パターンを発見したら本ファイルに追記し、週次戦略会議で報告
