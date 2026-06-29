# si4lockmac

[English](README.md) · [中文](README.zh-CN.md) · **日本語**

> ブランド名:**si4lockmac**。CLI コマンドは `lockmac` のままです（例:`lockmac veil`）。

**macOS のプライバシー目隠し**:最前面のオーバーレイで全ディスプレイを黒く覆い、
周囲から画面を見えなくします——**ただしMacはロックしません**。目隠しの裏で、
遠隔操作・スクリーンショット・自動化はそのまま動きます。

自己完結:純粋なPython標準ライブラリ + 小さなSwift製オーバーレイのみ。Telegramも
ホストプロジェクトも不要。（mob-remote が遠隔オン/オフに統合できますが、si4lockmac
単体で完全に動作します。）

![si4lockmac CLI デモ](media/cli-demo.gif)

> 読み取り専用コマンドのクイックツアー（`status`・`deadman`・`offline-lock`・`delete list`）。

> 使い方:**[GUI版 → docs/usage/USAGE-gui.md](docs/usage/USAGE-gui.md)**(ターミナル不要)· **[CLI版 → docs/usage/USAGE.md](docs/usage/USAGE.md)**。

## si4lockmac でできること

- 🕶️ **即時のプライバシー目隠し** —— コマンド1つ（またはタップ1つ）で全ディスプレイを
  黒く覆い、周囲から画面を見えなくします。あなたは作業継続:遠隔操作・スクショ・
  自動化はすべて裏で動き続けます。
- 🔒 **必要なときは本物のロック** —— 本当に守りたいときは `lock` で macOS 本物のログイン
  ウィンドウを起動。ローカルでもスマホからでも。
- 📱 **Telegram から遠隔操作** —— どこからでもチャットで目隠し・解除・ロック・状態確認。
  追加アプリもサーバーも不要。
- ⏱️ **デッドマンスイッチ** —— 無応答やオフライン時に、自動で目隠し・ロック・指定
  フォルダ削除。切断中でも機能します。
- 🌐 **オフラインロック** —— ネットワークが届かない間ずっとロックし続け、パスワード
  入力まで繰り返し再ロック。
- 🔐 **二段階認証（TOTP）** —— すべての解除に6桁の第二要素を追加。鍵はプライベート
  チャンネルにバックアップ。
- 🧹 **緊急削除** —— トリガー時にホワイトリストの機密フォルダを消去。`/`・`$HOME`・
  システム木への削除は強固に保護。

## 活用シーン

- **カフェ・コワーキング・空港** —— 席を離れた瞬間に周囲へ黒画面、ダウンロードや
  レンダリングは継続。
- **オープンオフィス・覗き見対策** —— ロックして再入力する手間なく、通りすがりの人から
  機密作業を隠す。
- **プレゼン・画面共有** —— デモの合間にデスクトップを目隠し、セッションも背景タスクも
  止めない。
- **出張・国境通過** —— デッドマンスイッチ + 緊急削除で、端末が手を離れたり応答できない
  ときに自己防衛。
- **遠隔 / ヘッドレス Mac** —— ロック/解除をすべて Telegram から操作、オフラインロックで
  そばにいられないマシンを守る。

## なぜ「ロック」でなく「目隠し」か

- オーバーレイは `CGShieldingWindowLevel` を使用（通常ウィンドウの上、メニューバー /
  Dock / 全 Spaces を覆う）。
- `screencapture` やウィンドウ単位のキャプチャは**これを回り込む**——よってスクショ／
  遠隔ツールは実際の内容を見られ、周囲には黒画面が見えます。
- これは**プライバシー画面であり、安全なロックではありません**:Force-Quit、`ssh kill`、
  再起動で解除できます。覗き見対策には有効ですが、キーボードの前にいる本気の相手には
  不十分。本当に守るならシステムロック（`lock`）を。

## インストール

**Homebrew（推奨）:**

```bash
brew install --cask Well365/lockmac/lockmac
```

署名済みの `.pkg` を自動でダウンロードしてインストールします。更新は `brew upgrade --cask lockmac`、削除は `brew uninstall --cask lockmac`。

手動で入れたい場合は `lockmac-0.5.0.pkg` をダブルクリック。その他の方法（ワンライナー、ソースからのビルド）は **[docs/usage/USAGE.md](docs/usage/USAGE.md)** を参照。

ヘルプ:`lockmac --help`（端末の簡易版） · `lockmac help`（自己完結のHTMLページを開く。
中 / English / 日本語 のコマンド説明付き）。
他のインストール方法（Homebrew / .pkg / ワンライナー）、未署名 .pkg の導入/署名方法、
旧バージョンの更新方法は **[docs/usage/USAGE.md](docs/usage/USAGE.md)** を参照。

## クイックスタート（3ステップ）

```bash
# 1. インストール(いずれか、下記参照): pip / Homebrew / .pkg / ワンライナー
# 2. 設定(2 コマンド)
lockmac setup            # パスワード設定(必須)
lockmac tg-setup         # Telegram bot を連携 —— 新規 bot は 3-5 分かかることも(自動ポーリング)
# 3. 全サービスを一括起動(起動中なら再起動)
lockmac start            # 目隠し自動起動 + Telegram 監視 + 毎時 watchdog
lockmac status           # 各サービスを確認
```

Telegram bot の作り方が分からない場合は図解ガイド（中/EN/日）:**[docs/usage/telegram-bot-setup.html](docs/usage/telegram-bot-setup.html)**。全停止は `lockmac stop`。

## 使い方

2 段階の「ロック」:

| コマンド | レベル | 遠隔解除? |
|---|---|---|
| `veil` / `unveil`（= `on` / `off`） | アプリのオーバーレイ——画面を黒く覆い、裏で作業継続 | ✅ 可（パスワード / Telegram） |
| `lock` | **本物の macOS システムロック**（loginwindow） | ❌ 不可——片方向;本体でシステムパスワードが必要 |

```bash
lockmac setup            # パスワード設定（必須）+ ログイン自動起動
lockmac veil             # 目隠しを表示
lockmac unveil           # 解除（パスワード入力）
lockmac status           # 状態を表示
```

> **パスワードは必須**:lockmac はパスワード無しの目隠しを拒否します(`lockmac on` は拒否)。

### 二段階認証（TOTP、任意）

```bash
lockmac setup-2fa        # 鍵/QRを表示し Authenticator に追加
```
有効化後:ローカル解除 = パスワード + 6 桁コード;Telegram 解除 = `/unveil`（6 桁の返信を促します）。

### Telegram 遠隔操作（任意、自己完結）

連携の CRUD:`tg-setup`(作成/トークン変更)· `tg-info`(確認、トークン伏字)· `tg-unbind`(削除 + 監視停止)。

```bash
lockmac tg-setup     # bot token を貼付、bot にメッセージ → chat id を自動保存
lockmac tg-info      # 確認:現在の連携(トークン伏字 + chat id)
lockmac tg-unbind    # 削除:連携解除し監視+watchdog を停止
lockmac tg-test      # テスト送信
lockmac tg-listen    # フォアグラウンドで監視
lockmac tg-install   # または LaunchAgent 常駐サービス化（KeepAlive + 毎時 watchdog）
```

チャットで `/veil` `/unveil` `/lock` `/status`（連携した chat のみ応答、fail-closed）:
- `/backend` — ロックのバックエンド切替（`self` / `si4locker`）、ボタンでワンタップ
- `/deadman <間隔秒> <猶予秒> <lock|veil|delete> [オフライン秒]` — デッドマン設定（即時反映）
- `/delete add <パス>` / `/delete list` / `/delete clear` — 削除リスト管理

### デッドマン（無応答 / オフラインで自動実行）

```bash
lockmac deadman 1800 600 lock   # 30分ごとに点呼、10分押さない → システムロック
lockmac deadman 0 0 delete 3600  # 点呼なし;TGに1時間繋がらない → ディレクトリ削除
lockmac deadman                 # 現在の設定を表示
lockmac deadman off             # 両トリガーを無効化(動作は保持)
```
- **ハートビート発火**:間隔ごとに「✅ います」ボタンを送信;猶予内に押さなければ発火。
- **オフライン発火**:Telegram にN秒繋がらない → 発火。**ローカル動作**で、切断中でも機能。

### オフラインロック（切断中はロックし続け、パスワード入力まで）

```bash
lockmac offline-lock            # 表示（既定ON:grace 60s / relock 300s）
lockmac offline-lock 60 300     # 60s 超でロック;切断中は 300s ごとに再ロック
lockmac offline-lock off        # 無効化
```
- `grace` を超えて切断 → **まず目隠し、次に本物のシステムロック**。
- 切断が続く限り **`relock` 秒ごとに再ロック**——解除してもしばらくすると（切断中なら）また
  ロック;再接続で解除されます。
- `tg-listen` の稼働が必要（Telegram 到達可否で在/不在を判定）。`lock-backend` に従います。

### 削除リスト（`action=delete` 用）

```bash
lockmac delete add ~/Secret           # ディレクトリ追加（/、$HOME、システム木は拒否）
lockmac delete remove ~/Secret        # 削除:1 件除去(別名 purge-rm/purge-del)
lockmac delete list
lockmac delete clear
lockmac delete now --yes             # 即時削除（手動;--yes 必須）
lockmac delete now --dry-run         # 🧪 削除対象をプレビュー(実削除しない)
```

⚠️ 不可逆(`rm -rf`)。まず `--dry-run` + 使い捨てディレクトリで安全にテスト;詳細と設定の目安は **[docs/usage/USAGE.md](docs/usage/USAGE.md)**（§6）を参照。

⚠️ **破壊的。** 保護:絶対パス必須;`/`、`$HOME` 自体、システム木（`/System` `/Library`
`/usr` …）は拒否。明示的に追加したディレクトリのみ削除。完全なディスク暗号消去には
MDM（`EraseDevice`）が必要——これは後のサーバー連携フェーズ。

> 1 bot に 1 poller:getUpdates は token ごとに消費者 1 つのみ。別のものが既にその bot を
> ポーリングしているなら、lockmac 用に別の bot を——でないと競合します（Telegram 409）。

MIT

---

## ❤️ 作者を支援 / Support

本プロジェクト（si4lockmac）は1週間を費やし、**500ドル超のトークン**を消費しました。役に立ったら開発の支援をお願いします。

<img src="lockmac/assets/doge-qr.png" width="200" alt="DOGE 投げ銭 QR">

- **DOGE**：`DJARW5ixK6sfMVGZvHiPNMMzo2Aoki13Cr`（Dogecoinネットワークのみ。他の資産は永久に失われます）
- **メール**：si4keyboard@gmail.com —— 優先フィードバック・カスタム機能
- Telegram で `/donate` を送るとQRと詳細が届きます。
