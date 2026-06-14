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
| データ保存 | JSON ファイル（DB なし） |
| HTML生成 | Python or Node.js スクリプト（予定） |
| ホスティング | GitHub Pages |
| CI/CD | GitHub Actions（main push → docs/ を自動公開） |
| 情報収集 | Web検索（47都道府県） |
| SNS連携 | X API v2（OAuth 1.0a）/ Instagram Graph API |
| シークレット管理 | .env（gitignore 済み）+ 環境変数 |
| ローカル運用 | Windows 11 / PowerShell |

---

## ディレクトリ構成
AI-Blog/
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions（自動デプロイ）
├── admin/                   # 管理画面（ローカルのみ）
├── data/
│   ├── festivals.json       # 祭りデータ
│   ├── last_post.json       # 最終投稿記録
│   └── error_log.json       # エラーログ
├── docs/                    # 公開HTML + 設計資料
│   └── README.md            # 本ファイル
├── .env                     # シークレット（gitignore済み）
├── .gitignore
├── festival-routine-prompt.md  # Claude Code Routines 実行手順書
└── README.md                # リポジトリ概要

---

## 更新スケジュール

| 時刻 | 目的 |
|------|------|
| 08:00 | 当日の祭り情報を朝イチで配信 |
| 12:00 | 昼祭りの直前情報・天気確認 |
| 16:00 | 夕方〜夜祭りの直前情報・リアルタイム更新 |
| 17:00 | 夕方〜夜祭りの直前情報・リアルタイム更新 |
| 18:00 | 夕方〜夜祭りの直前情報・リアルタイム更新 |

---

## 課題・今後の対応

- [ ] HTML・データ生成をスクリプト化（現状はLLM任せ）
- [ ] 更新スケジュールの確定
- [ ] SNSアカウント作成・API連携設定
- [ ] 初回データ収集・HTML生成の実行