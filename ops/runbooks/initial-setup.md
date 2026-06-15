# 初期設定チェックリスト(人間の作業、目安2〜3時間)

## 1. アカウント開設(約90分)
- [ ] **Etsyショップ開設** (etsy.com/sell) — ショップ名は以下の優先順で空いている最初のものを取る: `YohakuStudio` → `YohakuGoods` → `YohakuCo` → `StudioYohaku` → `YohakuPaper`。確定したらvoice.mdの「確定ショップ名」行に追記。プロフィール各欄は `templates/brand/shop-profile.md` の文をそのまま貼る。Etsy Paymentsの入金先としてPayoneerを接続、本人確認を完了
- [ ] **Pinterestビジネスアカウント** (business.pinterest.com) — 後でEtsyショップURLのドメイン認証を行う
- [ ] **Gumroadアカウント** — 既存決済(PayPal等)を接続
- [ ] (任意・後回し可) eRankアカウント(無料枠から。erank.com)

## 2. プロジェクト設定(約30分)
- [ ] GitHubにprivateリポジトリを作成し、`git remote add origin ...` して初回push
- [ ] **権限設定**: `ops/settings.example.json` の内容を確認し、問題なければ `cp ops/settings.example.json .claude/settings.json` を自分で実行(エージェントが自分の権限を広げることはできないため人間の作業。cron運用に必須)
- [ ] **headless認証(cron必須)**: `claude setup-token`(1行で)でトークン発行 → `secrets/oauth-token.env`(600)に保存。手順は `ops/runbooks/cron-auth.md`。これがないと claude系cronジョブは全て「Not logged in」で失敗する
- [ ] `crontab ops/cron/crontab.txt` で反映(ラッパー経由・全置換)→ `crontab -l` で確認
- [ ] cronの動作確認: 翌朝 `logs/cron-daily.log` が生成されているか
- [ ] macOSの省エネ設定: 早朝ジョブのためスリープ解除を許可(または `pmset repeat wakeorpoweron MTWRFSU 05:25:00`)

## 3. ブランド・ニッチ決定(約30分、Claudeと対話)
- [ ] `templates/brand/voice.md` — Claudeの3案から1つ選ぶ(済んでいれば確認のみ)
- [ ] `niches/active.md` — 候補から注力2〜3ニッチを承認
- [ ] Etsyショップ名・プロフィールをvoice.mdに合わせて設定(Claudeが文面生成)

## 4. 初回出品セッション(週末等、Claude同席で30〜60分)
- [ ] `/daily-production` が貯めた pending を確認・承認
- [ ] `/publish-assist` で最初の5〜10リスティングを出品(Publishクリックは自分で)
- [ ] `data/expenses.csv` にリスティング費が記帳されたか確認

## 完了基準
- 自動ジョブが3日連続エラーなしで実行されている(logs/ 確認)
- 最初の5リスティングが公開され、listings.csv に記録されている
