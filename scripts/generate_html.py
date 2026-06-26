import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')
CONFIG_JSON = os.path.join(os.path.dirname(__file__), '..', 'config.json')

TRUST_COLORS = {'高': '#2e7d32', '中': '#f9a825', '低': '#c62828'}

# 画像設定はconfig.jsonから読み込む（post_instagram.pyと共通化）
def load_config():
    if os.path.exists(CONFIG_JSON):
        with open(CONFIG_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

_config = load_config()
IMAGE_BASE_URL = _config.get('image_base_url', 'https://raw.githubusercontent.com/Shoma540/AI-Blog/main/assets/images')
GENRE_IMAGES = _config.get('genre_images', {})
DEFAULT_IMAGE = _config.get('default_image', 'default_ill.png')
GENRE_PRIORITY = _config.get('genre_priority', [])

COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Noto Sans JP', 'Hiragino Sans', sans-serif;
  background: #FAF7F2;
  color: #2c2c2c;
  min-height: 100vh;
}
a { text-decoration: none; color: inherit; }

/* ナビ */
nav {
  background: #C0392B;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  height: 56px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
nav .logo {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  white-space: nowrap;
}
nav a {
  color: rgba(255,255,255,0.85);
  font-size: 0.9rem;
  padding: 0.25rem 0;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}
nav a:hover, nav a.active {
  color: #fff;
  border-bottom-color: #fff;
}

/* ヘッダー */
.page-header {
  background: linear-gradient(135deg, #C0392B 0%, #8b1a10 100%);
  color: #fff;
  padding: 3rem 1.5rem 2.5rem;
  text-align: center;
}
.page-header h1 {
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}
.page-header p {
  font-size: 0.95rem;
  opacity: 0.85;
}

/* コンテナ */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* セクション見出し */
.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #C0392B;
  border-left: 4px solid #C0392B;
  padding-left: 0.75rem;
  margin-bottom: 1.25rem;
}

/* カードグリッド */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}

/* 祭りカード */
.festival-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}
.festival-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.13);
}
.card-img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  background: #f0ebe3;
}
.card-body {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.card-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.4;
}
.card-date {
  font-size: 0.85rem;
  color: #C0392B;
  font-weight: 600;
}
.card-location {
  font-size: 0.82rem;
  color: #666;
}
.card-badges {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.25rem;
}
.badge {
  display: inline-block;
  font-size: 0.72rem;
  padding: 0.18rem 0.5rem;
  border-radius: 20px;
  font-weight: 600;
}
.badge-genre {
  background: #f3e8e8;
  color: #C0392B;
}
.badge-trust-高 { background: #e8f5e9; color: #2e7d32; }
.badge-trust-中 { background: #fffde7; color: #f57f17; }
.badge-trust-低 { background: #ffebee; color: #c62828; }
.badge-check {
  background: #fff3e0;
  color: #e65100;
}

/* バッジリンク（都道府県・月） */
.badge-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}
.badge-link {
  display: inline-block;
  background: #fff;
  border: 1.5px solid #ddd;
  border-radius: 6px;
  padding: 0.4rem 0.9rem;
  font-size: 0.9rem;
  color: #333;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}
.badge-link:hover {
  background: #C0392B;
  border-color: #C0392B;
  color: #fff;
}

/* フッター */
footer {
  text-align: center;
  padding: 2rem 1rem;
  font-size: 0.8rem;
  color: #999;
  border-top: 1px solid #e8e0d8;
  margin-top: 2rem;
}

/* 地図ページ */
.map-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 0.6rem;
  margin-bottom: 2rem;
}
.map-pref-btn {
  display: block;
  text-align: center;
  padding: 0.6rem 0.4rem;
  background: #fff;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #333;
  transition: all 0.15s;
}
.map-pref-btn:hover, .map-pref-btn.has-data {
  background: #C0392B;
  border-color: #C0392B;
  color: #fff;
}
.map-pref-btn.no-data {
  opacity: 0.4;
  pointer-events: none;
}

/* カレンダーページ */
.month-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
.month-tab {
  padding: 0.5rem 1.2rem;
  background: #fff;
  border: 1.5px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.15s;
}
.month-tab.active, .month-tab:hover {
  background: #C0392B;
  border-color: #C0392B;
  color: #fff;
}
.month-section { display: none; }
.month-section.active { display: block; }

/* レスポンシブ */
@media (max-width: 600px) {
  .card-grid { grid-template-columns: 1fr; }
  nav { gap: 1rem; }
  .page-header { padding: 2rem 1rem 1.5rem; }
}
"""

NAV_HTML = """<nav>
  <span class="logo">🎉 全国祭り情報</span>
  <a href="../index.html">ホーム</a>
  <a href="../map.html">地図</a>
  <a href="../calendar.html">カレンダー</a>
</nav>"""

NAV_ROOT_HTML = """<nav>
  <span class="logo">🎉 全国祭り情報</span>
  <a href="index.html">ホーム</a>
  <a href="map.html">地図</a>
  <a href="calendar.html">カレンダー</a>
</nav>"""

ALL_PREFS = [
    "北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
    "茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
    "新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県",
    "静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
    "奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県",
    "徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
    "熊本県","大分県","宮崎県","鹿児島県","沖縄県"
]

MONTH_NAMES = {
    1:"1月",2:"2月",3:"3月",4:"4月",5:"5月",6:"6月",
    7:"7月",8:"8月",9:"9月",10:"10月",11:"11月",12:"12月"
}


def load_data():
    if os.path.exists(FESTIVALS_JSON):
        with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_updated": "", "festivals": []}


def get_image_url(festival):
    filename = select_image_filename(festival)
    return f"{IMAGE_BASE_URL}/{filename}"


def select_image_filename(festival):
    """ジャンルから画像ファイル名を決定する。
    genre_priority 順で最初にマッチしたジャンルの画像を使う。
    優先リストに無いジャンルは祭りのgenre出現順で次点評価。
    どれもマッチしなければ default_image。
    """
    genres = festival.get('genre') or []
    # 1. genre_priority順で、この祭りが持つジャンルを探す
    for p in GENRE_PRIORITY:
        if p in genres and p in GENRE_IMAGES:
            return GENRE_IMAGES[p]
    # 2. 優先リストに無いが画像があるジャンルを、祭りのgenre順で探す
    for g in genres:
        if g in GENRE_IMAGES:
            return GENRE_IMAGES[g]
    # 3. フォールバック
    return DEFAULT_IMAGE


def format_date(date_str):
    if not date_str:
        return "日程未定"
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{d.month}月{d.day}日"
    except:
        return date_str


def festival_card_html(f, img_path_prefix=""):
    trust = f.get('trust_level', '低')
    trust_color = TRUST_COLORS.get(trust, '#999')
    check_badge = '<span class="badge badge-check">⚠️ 要確認</span>' if f.get('requires_check') else ''
    genres = f.get('genre') or []
    genre_badges = ''.join(f'<span class="badge badge-genre">{g}</span>' for g in genres[:2])
    date_start = format_date(f.get('date_start', ''))
    date_end = f.get('date_end', '')
    date_label = date_start
    if date_end and date_end != f.get('date_start', ''):
        date_label += f" 〜 {format_date(date_end)}"
    pref = f.get('prefecture', '')
    city = f.get('city', '')
    location = f"{pref} {city}".strip()
    img_url = get_image_url(f)
    return f"""<div class="festival-card">
  <img class="card-img" src="{img_url}" alt="{f.get('name','')}" loading="lazy">
  <div class="card-body">
    <div class="card-name">{f.get('name','')}</div>
    <div class="card-date">📅 {date_label}</div>
    <div class="card-location">📍 {location}</div>
    <div class="card-badges">
      {genre_badges}
      <span class="badge badge-trust-{trust}" style="background:{TRUST_COLORS.get(trust,'#eee')}1a;color:{trust_color};">[信頼度:{trust}]</span>
      {check_badge}
    </div>
  </div>
</div>"""


def html_page(title, body, nav=NAV_ROOT_HTML, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 全国祭り情報</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600;700&display=swap" rel="stylesheet">
  <style>{COMMON_CSS}</style>
  {extra_head}
</head>
<body>
{nav}
{body}
</body>
</html>"""


def generate_index(festivals, last_updated):
    """ホームページ：祭りカード一覧"""
    sorted_festivals = sorted(
        festivals,
        key=lambda f: f.get('date_start') or '9999'
    )
    cards = ''.join(festival_card_html(f) for f in sorted_festivals)
    pref_links = ''.join(
        f'<a class="badge-link" href="prefecture/{p}.html">{p}</a>'
        for p in sorted(set(f.get('prefecture','') for f in festivals if f.get('prefecture')))
    )
    body = f"""<div class="page-header">
  <h1>🎉 全国祭り情報</h1>
  <p>全国の祭りをまとめてチェック。随時更新中。</p>
</div>
<div class="container">
  <h2 class="section-title">開催が近い順</h2>
  <div class="card-grid">{cards}</div>
  <h2 class="section-title">都道府県から探す</h2>
  <div class="badge-links">{pref_links}</div>
</div>
<footer>最終更新: {last_updated} &nbsp;|&nbsp; <a href="map.html">地図から探す</a> &nbsp;|&nbsp; <a href="calendar.html">カレンダーで見る</a></footer>"""
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(os.path.join(DOCS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_page("全国祭り情報", body))
    print("docs/index.html を生成しました")


def generate_map(festivals, last_updated):
    """地図ページ：47都道府県ボタン（データありなし色分け）"""
    has_data = set(f.get('prefecture','') for f in festivals)
    pref_btns = ''
    for p in ALL_PREFS:
        if p in has_data:
            pref_btns += f'<a class="map-pref-btn has-data" href="prefecture/{p}.html">{p}</a>'
        else:
            pref_btns += f'<span class="map-pref-btn no-data">{p}</span>'
    body = f"""<div class="page-header">
  <h1>地図から探す</h1>
  <p>赤色の都道府県に祭り情報があります</p>
</div>
<div class="container">
  <h2 class="section-title">都道府県一覧</h2>
  <div class="map-grid">{pref_btns}</div>
</div>
<footer>最終更新: {last_updated}</footer>"""
    with open(os.path.join(DOCS_DIR, 'map.html'), 'w', encoding='utf-8') as f:
        f.write(html_page("地図から探す", body))
    print("docs/map.html を生成しました")


def generate_calendar(festivals, last_updated):
    """カレンダーページ：月別タブ"""
    months_data = {}
    for f in festivals:
        ds = f.get('date_start', '')
        if not ds:
            continue
        try:
            m = datetime.strptime(ds, '%Y-%m-%d').month
            months_data.setdefault(m, []).append(f)
        except:
            pass

    if not months_data:
        body = '<div class="container"><p>データがありません</p></div>'
        with open(os.path.join(DOCS_DIR, 'calendar.html'), 'w', encoding='utf-8') as f:
            f.write(html_page("カレンダー", body))
        return

    sorted_months = sorted(months_data.keys())
    tabs = ''.join(
        f'<button class="month-tab{" active" if i==0 else ""}" onclick="showMonth({m})">{m}月</button>'
        for i, m in enumerate(sorted_months)
    )
    sections = ''
    for i, m in enumerate(sorted_months):
        cards = ''.join(festival_card_html(f) for f in sorted(months_data[m], key=lambda x: x.get('date_start','')))
        active = ' active' if i == 0 else ''
        sections += f'<div class="month-section{active}" id="month-{m}"><div class="card-grid">{cards}</div></div>'

    js = """<script>
function showMonth(m) {
  document.querySelectorAll('.month-section').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.month-tab').forEach(el => el.classList.remove('active'));
  document.getElementById('month-' + m).classList.add('active');
  event.target.classList.add('active');
}
</script>"""

    body = f"""<div class="page-header">
  <h1>月別カレンダー</h1>
  <p>開催月を選んで祭りを探す</p>
</div>
<div class="container">
  <div class="month-tabs">{tabs}</div>
  {sections}
</div>
<footer>最終更新: {last_updated}</footer>"""
    with open(os.path.join(DOCS_DIR, 'calendar.html'), 'w', encoding='utf-8') as f:
        f.write(html_page("カレンダー", body, extra_head=js))
    print("docs/calendar.html を生成しました")


def generate_prefecture_pages(festivals, last_updated):
    out_dir = os.path.join(DOCS_DIR, 'prefecture')
    os.makedirs(out_dir, exist_ok=True)
    prefectures = set(f.get('prefecture','') for f in festivals if f.get('prefecture'))
    for pref in prefectures:
        pref_festivals = sorted(
            [f for f in festivals if f.get('prefecture') == pref],
            key=lambda x: x.get('date_start') or '9999'
        )
        cards = ''.join(festival_card_html(f) for f in pref_festivals)
        body = f"""<div class="page-header">
  <h1>{pref}の祭り情報</h1>
  <p>{len(pref_festivals)}件の祭りが見つかりました</p>
</div>
<div class="container">
  <div class="card-grid">{cards}</div>
  <a class="badge-link" href="../index.html">← トップへ戻る</a>
</div>
<footer>最終更新: {last_updated}</footer>"""
        nav = NAV_HTML.replace('href="../', 'href="../')
        with open(os.path.join(out_dir, f'{pref}.html'), 'w', encoding='utf-8') as f:
            f.write(html_page(f"{pref}の祭り情報", body, nav=nav))
    print(f"都道府県ページを {len(prefectures)} 件生成しました")


def generate_month_pages(festivals, last_updated):
    out_dir = os.path.join(DOCS_DIR, 'month')
    os.makedirs(out_dir, exist_ok=True)
    months_data = {}
    for f in festivals:
        ds = f.get('date_start', '')
        if not ds:
            continue
        try:
            m = datetime.strptime(ds, '%Y-%m-%d').month
            months_data.setdefault(m, []).append(f)
        except:
            pass
    for m, fests in months_data.items():
        sorted_fests = sorted(fests, key=lambda x: x.get('date_start',''))
        cards = ''.join(festival_card_html(f) for f in sorted_fests)
        body = f"""<div class="page-header">
  <h1>{m}月の祭り情報</h1>
  <p>{len(fests)}件の祭りが見つかりました</p>
</div>
<div class="container">
  <div class="card-grid">{cards}</div>
  <a class="badge-link" href="../calendar.html">← カレンダーへ戻る</a>
</div>
<footer>最終更新: {last_updated}</footer>"""
        nav = NAV_HTML
        with open(os.path.join(out_dir, f'{m}.html'), 'w', encoding='utf-8') as f:
            f.write(html_page(f"{m}月の祭り情報", body, nav=nav))
    print(f"月別ページを {len(months_data)} 件生成しました")


if __name__ == '__main__':
    data = load_data()
    festivals = data.get('festivals', [])
    last_updated = data.get('last_updated', '未更新')
    generate_index(festivals, last_updated)
    generate_map(festivals, last_updated)
    generate_calendar(festivals, last_updated)
    generate_prefecture_pages(festivals, last_updated)
    generate_month_pages(festivals, last_updated)
    print("HTML生成完了")
