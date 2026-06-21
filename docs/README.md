# AI-Blog 設計資料

## プロジェクト概要

Claude Code Routines により自動更新される全国祭り情報サイト。

**目的**
- 祭りに行く前に情報を見られるようにする（事前情報提供）
- 当日の中止・変更情報をリアルタイムで反映する

**公開URL**
https://shoma540.github.io/AI-Blog/

---

## 技術スタック

| 領域 | 採用技術 |
|------|------|
| 実行エンジン | Claude Code Routines（schedule トリガー） |
| 言語 | Python 3 |
| 依存ライブラリ | requests（`requirements.txt`） |
| データ保存 | JSON ファイル（DB なし） |
| HTML生成 | Python スクリプト（`scripts/generate_html.py`） |
| ホスティング | GitHub Pages（`docs/` を公開） |
| CI/CD | GitHub Actions（main push → `peaceiris/actions-gh-pages` で `docs/` を自動公開） |
| 情報収集 | Web検索（47都道府県） |
| SNS連携 | Instagram Graph API（v21.0） |
| シークレット管理 | `.env`（gitignore 済み）+ 環境変数（CI の Secrets を優先） |
| ローカル運用 | Windows 11 / PowerShell |

---

## ディレクトリ構成

```
AI-Blog/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions（main push → docs/ を自動デプロイ）
├── admin/                      # 管理画面（ローカルのみ・現状は空＝将来の差分管理画面用）
├── assets/
│   └── images/                 # ジャンル別画像（花火/神輿/盆踊り/農祭り 等）+ README
├── data/
│   ├── festivals.json          # 祭りデータ（本体）
│   └── last_post.json          # 最終実行・投稿記録
├── docs/                       # GitHub Pages 公開ディレクトリ
│   ├── index.html              # トップ（都道府県・月別リンク）
│   ├── prefecture/[県名].html  # 都道府県ごとの一覧ページ
│   └── README.md               # 本ファイル（設計資料）
├── scripts/
│   ├── save_data.py            # JSON 読み書きユーティリティ
│   ├── generate_html.py        # JSON → HTML 生成
│   ├── git_push.py             # 差分集計 → commit & push
│   └── post_instagram.py       # Instagram 投稿
├── config.json                 # 画像 URL・ジャンル別画像のマッピング
├── festival-routine-prompt.md  # Claude Code Routines 実行手順書（STEP 1〜9）
├── requirements.txt            # Python 依存
├── push.ps1 / git_push.bat     # ローカル手動 push 補助
├── .env                        # シークレット（gitignore 済み）
├── .gitignore
└── README.md                   # リポジトリ概要
```

---

## スクリプトの役割

| スクリプト | 役割 |
|------|------|
| `save_data.py` | `festivals.json` / `last_post.json` の読み込み・保存ユーティリティ |
| `generate_html.py` | `festivals.json` から `docs/index.html`（都道府県・月別リンク）と `docs/prefecture/[県名].html` を生成 |
| `git_push.py` | `diff_status`（NEW/UPDATED）の件数を集計し、変更があればコミットメッセージを生成して `origin main` へ push（変更なしならスキップ） |
| `post_instagram.py` | 投稿判定 → ジャンルに応じた画像を選択 → Instagram Graph API でメディア作成・公開 |

**Instagram 投稿判定ロジック（`post_instagram.py`）**
- 現在時刻が 12 時台 → 無条件で投稿
- それ以外 → `last_post.json` の `has_update` が `true` の場合のみ投稿

**画像 URL の解決優先順位（`post_instagram.py`）**
1. 環境変数 `IG_IMAGE_URL`（手動指定）
2. 環境変数 `IMAGE_BASE_URL`
3. `config.json` の `image_base_url`

---

## データモデル

**`data/festivals.json`**
```jsonc
{
  "last_updated": "YYYY-MM-DD HH:MM",
  "festivals": [
    {
      "id": "festival_001",
      "name": "祇園祭",
      "prefecture": "京都府",
      "city": "京都市",
      "date_start": "2026-07-01",
      "date_end": "2026-07-31",
      "genre": ["山車", "神事"],
      "scale": "...",
      "is_free": true,
      "diff_status": "NEW | UPDATED | (なし)",
      "...": "rain_policy / organizer / history など多数のフィールド"
    }
  ]
}
```

**`data/last_post.json`**
```json
{
  "last_executed": "YYYY-MM-DD HH:MM",
  "has_update": true,
  "posted_to_instagram": false
}
```

---

## 必要な環境変数

| 変数 | 用途 |
|------|------|
| `INSTAGRAM_ACCESS_TOKEN` | Instagram Graph API アクセストークン |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Instagram ビジネスアカウント ID |
| `IMAGE_BASE_URL`（または `IG_IMAGE_URL`） | 投稿画像の公開 URL ベース |
| `SITE_URL`（任意） | キャプションに載せるサイト URL |

ローカルでは `.env` から読み込み、CI では Secrets を優先（既存の環境変数は上書きしない）。

---

## 実行フロー（Routine：`festival-routine-prompt.md`）

1. **既存データの読み込み**（`festivals.json`）
2. **祭り情報の収集**（Web検索・47都道府県）
3. **祭りの同一性判定**
4. **信頼度の判定**
5. **差分検出**（NEW / UPDATED の付与）
6. **データの保存**（`festivals.json`）
7. **HTML 生成**（`scripts/generate_html.py`）
8. **GitHub へ Push**（`scripts/git_push.py`）
9. **Instagram 投稿**（`scripts/post_instagram.py`）

HTML 生成・Push・Instagram 投稿は既存スクリプトを呼び出す方針（Routine 実行時にスクリプト自体は書き換えない）。

---

## 更新スケジュール

毎日 08:00 / 12:00 / 16:00 / 17:00 / 18:00（日本時間）。
※実際のトリガー時刻は Claude Code Routines 側の設定で管理。

| 時刻 | 目的 |
|------|------|
| 08:00 | 当日の祭り情報を朝イチで配信 |
| 12:00 | 昼祭りの直前情報・天気確認 |
| 16:00 | 夕方〜夜祭りの直前情報・リアルタイム更新 |
| 17:00 | 夕方〜夜祭りの直前情報・リアルタイム更新 |
| 18:00 | 夕方〜夜祭りの直前情報・リアルタイム更新 |

---

## 課題・今後の対応

- [ ] HTML・データ生成のスクリプト化拡張（ジャンル別・規模別・月別個別ページ、`admin/` の差分管理画面）
- [ ] 更新スケジュールの確定
- [ ] 初回データ収集・HTML生成の運用安定化
```

