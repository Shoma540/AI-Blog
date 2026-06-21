import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')


def load_festivals():
    if os.path.exists(FESTIVALS_JSON):
        with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_updated": "", "festivals": []}


def generate_index(festivals: list, last_updated: str):
    prefectures = sorted(set(f['prefecture'] for f in festivals if 'prefecture' in f))
    months = sorted(set(
        datetime.strptime(f['date_start'], '%Y-%m-%d').month
        for f in festivals if 'date_start' in f and f['date_start']
    ))

    pref_links = ''.join(
        f'<a href="prefecture/{p}.html" class="badge">{p}</a>'
        for p in prefectures
    )
    month_links = ''.join(
        f'<a href="month/{m}.html" class="badge">{m}月</a>'
        for m in months
    )

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>全国祭り情報</title>
  <style>
    body {{ font-family: sans-serif; max-width: 900px; margin: 0 auto; padding: 1rem; }}
    h1 {{ color: #333; }}
    .badge {{ display: inline-block; margin: 4px; padding: 4px 10px; background: #f0f0f0; border-radius: 4px; text-decoration: none; color: #333; }}
    .badge:hover {{ background: #ddd; }}
    .section {{ margin: 2rem 0; }}
    footer {{ margin-top: 2rem; color: #999; font-size: 0.85rem; }}
  </style>
</head>
<body>
  <h1>🎉 全国祭り情報</h1>
  <div class="section">
    <h2>都道府県から探す</h2>
    {pref_links if pref_links else '<p>データなし</p>'}
  </div>
  <div class="section">
    <h2>月から探す</h2>
    {month_links if month_links else '<p>データなし</p>'}
  </div>
  <footer>最終更新: {last_updated}</footer>
</body>
</html>"""

    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(os.path.join(DOCS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("docs/index.html を生成しました")


def generate_prefecture_pages(festivals: list):
    out_dir = os.path.join(DOCS_DIR, 'prefecture')
    os.makedirs(out_dir, exist_ok=True)

    prefectures = set(f['prefecture'] for f in festivals if 'prefecture' in f)
    for pref in prefectures:
        pref_festivals = [f for f in festivals if f.get('prefecture') == pref]
        items = ''.join(
            f'<li><strong>{f.get("name", "")}</strong> {f.get("date_start", "")} {f.get("city", "")}</li>'
            for f in pref_festivals
        )
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{pref}の祭り情報</title>
  <style>body {{ font-family: sans-serif; max-width: 900px; margin: 0 auto; padding: 1rem; }}</style>
</head>
<body>
  <h1>{pref}の祭り情報</h1>
  <ul>{items}</ul>
  <a href="../index.html">← トップへ戻る</a>
</body>
</html>"""
        with open(os.path.join(out_dir, f'{pref}.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"都道府県ページを {len(prefectures)} 件生成しました")


if __name__ == '__main__':
    data = load_festivals()
    festivals = data.get('festivals', [])
    last_updated = data.get('last_updated', '未更新')
    generate_index(festivals, last_updated)
    generate_prefecture_pages(festivals)
    print("HTML生成完了")