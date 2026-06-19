# ジャンル別バナー画像

Instagram 投稿に使う、ジャンル別のバナー画像を置くディレクトリです。

## 画像仕様
- サイズ: **1080 × 1080 px**（Instagram 推奨の正方形）
- 形式: **PNG**
- 内容: ジャンルが一目でわかるシンプルなデザイン

## 必要なファイル（初期）
ジャンルとファイル名の対応は `config.json` の `genre_images` で管理しています。

| ジャンル | ファイル名 |
|---------|-----------|
| 花火 | `hanabi.png` |
| 神輿 | `mikoshi.png` |
| 盆踊り | `bon_odori.png` |
| 農祭り | `nou_matsuri.png` |
| （該当なし・ファイル未存在） | `default.png` |

`default.png` は必ず用意してください（フォールバック用）。

## ジャンルを追加するとき
1. このディレクトリに 1080×1080 の PNG を追加する
2. `config.json` の `genre_images` に「ジャンル名: ファイル名」を追記する

コード（`scripts/post_instagram.py`）の変更は不要です。

## 公開URLについて
Instagram API は画像を**公開URL**として取得するため、これらのファイルは
`config.json` の `image_base_url` を起点に参照されます（既定はこのリポジトリの
`raw.githubusercontent.com` URL）。ファイルを追加したら git push して公開してください。
