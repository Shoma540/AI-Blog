"""
2026-06-24 実行分 - 収集結果に基づいてfestivals.jsonを更新する
差分：
  festival_003 (青森ねぶた祭): ticket_url・price更新
  festival_004 (阿波おどり): date_note更新
  festival_022〜026: 新規5件追加
"""
import json
import os
from datetime import datetime

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')
LAST_POST_JSON = os.path.join(DATA_DIR, 'last_post.json')

NEW_FESTIVALS = [
    {
        "id": "festival_022",
        "name": "青柏祭（でか山）",
        "alternate_names": ["青柏祭"],
        "similar_name_warning": False,
        "prefecture": "石川県",
        "city": "七尾市",
        "date_start": "2026-05-02",
        "date_end": "2026-05-05",
        "date_note": "2026年は開催終了済み（記録用）。5/4は大地主神社、5/5は能登食祭市場・仙対橋付近に曳山勢揃い。",
        "time_start": "不明",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "大地主神社（山王神社）",
        "genre": ["曳山"],
        "scale": "国指定重要無形民俗文化財（でか山）／ユネスコ無形文化遺産",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "能登最大の春祭りで、高さ12m・重さ20tの曳山「でか山」が日本一の大きさを誇る。",
        "food_stalls": "駅前エリアにグルメ・ステージ・体験イベントあり",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "大地主神社（七尾市街地中心部）。JR七尾駅から徒歩圏内。",
        "official_url": "https://www.city.nanao.lg.jp/koryu-s/event/event_syokai/seihakusai.html",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {
                "url": "https://www.city.nanao.lg.jp/koryu-s/event/event_syokai/seihakusai.html",
                "site_name": "七尾市公式ウェブサイト",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            },
            {
                "url": "https://www.hot-ishikawa.jp/event/detail_5674.html",
                "site_name": "石川県観光公式サイト ほっと石川旅ねっと",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            },
            {
                "url": "https://ishikawa-style.com/seihakusai-2026/",
                "site_name": "いしかわスタイル",
                "is_official": False,
                "retrieved_date": "2026-06-24"
            }
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_023",
        "name": "那智の扇祭り",
        "alternate_names": ["那智の火祭り", "熊野那智大社例大祭"],
        "similar_name_warning": False,
        "prefecture": "和歌山県",
        "city": "那智勝浦町",
        "date_start": "2026-07-14",
        "date_end": "2026-07-14",
        "date_note": "午後14:00頃に飛瀧神社参道域で御火神事（大松明12本）。12体の扇神輿が渡御。",
        "time_start": "14:00",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "熊野那智大社",
        "genre": ["神事", "火祭"],
        "scale": "国指定重要無形民俗文化財（日本三大火祭り）",
        "is_free": True,
        "price": "見学無料（特別拝観席プランあり）",
        "ticket_url": "https://kumanonachitaisha.or.jp/event/fan/",
        "history_years": "不明",
        "history_description": "熊野那智大社の例大祭。御瀧信仰の根本たる水の神意を発揚する神事で、大松明の炎で御瀧の参道を浄める様から「那智の火祭り」とも称される。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "熊野那智大社（那智勝浦町那智山）。JRきのくに線紀伊勝浦駅よりバス約30分。",
        "official_url": "https://kumanonachitaisha.or.jp/event/fan/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {
                "url": "https://kumanonachitaisha.or.jp/event/fan/",
                "site_name": "熊野那智大社 公式サイト",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            },
            {
                "url": "https://www.kumano-sanzan.jp/nachi/himatsuri.html",
                "site_name": "熊野三山協議会",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            },
            {
                "url": "https://www.wakayama-kanko.or.jp/events/detail_79.html",
                "site_name": "和歌山県観光公式サイト",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            }
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_024",
        "name": "川越まつり",
        "alternate_names": ["川越氷川祭", "川越氷川祭の山車行事"],
        "similar_name_warning": False,
        "prefecture": "埼玉県",
        "city": "川越市",
        "date_start": "2026-10-17",
        "date_end": "2026-10-18",
        "date_note": "川越氷川神社例大祭（10月14日）に続く神幸祭に合わせて行われる。2026年は川越氷川祭発祥380周年の節目。",
        "time_start": "不明",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "川越市",
        "genre": ["山車", "お囃子"],
        "scale": "国指定重要無形民俗文化財／ユネスコ無形文化遺産（山・鉾・屋台行事）",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "370年以上の歴史を誇る川越の秋の風物詩。川越氷川祭の山車行事としてユネスコ無形文化遺産・国指定重要無形民俗文化財に登録。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "川越市街地（川越氷川神社周辺）。西武新宿線本川越駅・JR川越駅から徒歩圏内。",
        "official_url": "https://kawagoematsuri.jp/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {
                "url": "https://kawagoematsuri.jp/",
                "site_name": "川越まつり公式サイト",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            },
            {
                "url": "https://kawagoe.fun/magazine/event/kawagoe-matsuri/",
                "site_name": "川越マガジン",
                "is_official": False,
                "retrieved_date": "2026-06-24"
            }
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_025",
        "name": "みなとみらい大盆踊り",
        "alternate_names": ["第17回みなとみらい大盆踊り"],
        "similar_name_warning": False,
        "prefecture": "神奈川県",
        "city": "横浜市",
        "date_start": "2026-08-28",
        "date_end": "2026-08-29",
        "date_note": "16:30〜20:30。臨港パーク・プラザ広場開催。小雨決行・順延なし。",
        "time_start": "16:30",
        "time_end": "20:30",
        "rain_policy": "小雨決行、荒天時は時間変更または中止",
        "organizer": "パシフィコ横浜",
        "genre": ["盆踊り"],
        "scale": "その他",
        "is_free": True,
        "price": "入場無料（キッチンカー等飲食あり）",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "不明",
        "food_stalls": "キッチンカーエリア・フードコートあり（クラフトビール、焼きそば、かき氷等）",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "みなとみらい線みなとみらい駅から徒歩7分、JR桜木町駅から徒歩14分。駐車場：みなとみらい公共駐車場ほか（有料）。",
        "official_url": "https://www.pacifico.co.jp/event/MM_BonOdori",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {
                "url": "https://www.pacifico.co.jp/event/MM_BonOdori",
                "site_name": "パシフィコ横浜 公式",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            }
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_026",
        "name": "高山祭（八幡祭）",
        "alternate_names": ["秋の高山祭", "飛騨高山秋まつり"],
        "similar_name_warning": False,
        "prefecture": "岐阜県",
        "city": "高山市",
        "date_start": "2026-10-09",
        "date_end": "2026-10-10",
        "date_note": "旧高山城下町北半分の氏神・櫻山八幡宮の例祭。11台の屋台が登場し、曳き廻し・からくり奉納・ご神幸行列を実施。",
        "time_start": "不明",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "高山市 / 櫻山八幡宮",
        "genre": ["山車", "屋台行事"],
        "scale": "国指定重要有形民俗文化財／ユネスコ無形文化遺産（日本三大美祭）",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "春の山王祭と秋の八幡祭を合わせて「高山祭」と呼ぶ。秋祭（八幡祭）は安川通り北側に11台の豪華屋台が勢揃いする。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "不明",
        "official_url": "https://www.kankou-gifu.jp/event/detail_1074.html",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {
                "url": "https://www.kankou-gifu.jp/event/detail_1074.html",
                "site_name": "岐阜県観光公式サイト（秋の高山祭）",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            },
            {
                "url": "https://www.hidatakayama.or.jp/hidatakayama/maturi_autumn/",
                "site_name": "飛騨高山観光公式サイト",
                "is_official": True,
                "retrieved_date": "2026-06-24"
            }
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    }
]


def update_festivals():
    with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    festivals = data['festivals']

    for f in festivals:
        fid = f['id']

        # festival_003: 青森ねぶた祭 - ticket_url・price更新
        if fid == 'festival_003':
            old_ticket = f.get('ticket_url')
            old_price = f.get('price')
            f['ticket_url'] = 'https://www.nebuta.jp/info/purchase/group.html'
            f['price'] = '見学無料（有料観覧席あり、観覧席1席3,500円〜）'
            f['diff_status'] = 'UPDATED'
            f['updated_fields'] = ['ticket_url', 'price']
            f['year_comparison'] = {
                'changed': True,
                'details': f'ticket_url: {old_ticket} → https://www.nebuta.jp/info/purchase/group.html / price: {old_price} → 見学無料（有料観覧席あり、観覧席1席3,500円〜）'
            }
            continue

        # festival_004: 阿波おどり - date_note更新
        if fid == 'festival_004':
            old_note = f.get('date_note')
            f['date_note'] = (
                '8月11日は屋内会場（アスティとくしま・あわぎんホール）「優りび」開催、'
                '8月12日〜15日は有料演舞場（藍場浜・南内町・紺屋町）・無料演舞場ほか開催。'
            )
            f['diff_status'] = 'UPDATED'
            f['updated_fields'] = ['date_note']
            f['year_comparison'] = {
                'changed': True,
                'details': f'date_note更新: 屋内会場がアスティとくしまのみ→アスティとくしま・あわぎんホールの2カ所に確認。屋外演舞場（藍場浜・南内町・紺屋町）の3カ所が明確化。'
            }
            continue

        # その他は UNCHANGED に変更（前回NEWだったものは今回比較対象として確認済み）
        if f['diff_status'] == 'NEW':
            f['diff_status'] = 'UNCHANGED'
            f['updated_fields'] = []

    # 新規5件を追加
    festivals.extend(NEW_FESTIVALS)

    data['festivals'] = festivals
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')

    with open(FESTIVALS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"festivals.json を更新しました（計 {len(festivals)} 件）")

    # last_post.json の更新
    last_post = {
        'last_executed': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'has_update': True,
        'posted_to_instagram': False
    }
    with open(LAST_POST_JSON, 'w', encoding='utf-8') as f:
        json.dump(last_post, f, ensure_ascii=False, indent=2)
    print("last_post.json を更新しました")


if __name__ == '__main__':
    update_festivals()
