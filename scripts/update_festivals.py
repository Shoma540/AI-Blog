"""
祭りデータ更新スクリプト（2026-06-30 実行分）
- 既存データの diff_status を UNCHANGED に更新
- 新規祭り情報を追加
"""
import json
import os
import sys

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')
LAST_POST_JSON = os.path.join(DATA_DIR, 'last_post.json')

NEW_FESTIVALS = [
    {
        "id": "festival_022",
        "name": "那智の扇祭り（那智の火祭）",
        "alternate_names": ["那智の火祭", "那智大社例大祭"],
        "similar_name_warning": False,
        "prefecture": "和歌山県",
        "city": "東牟婁郡那智勝浦町",
        "date_start": "2026-07-14",
        "date_end": "2026-07-14",
        "date_note": "午前10:00〜。飛瀧神社参道域での御火神事は14時頃。",
        "time_start": "10:00",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "熊野那智大社",
        "genre": ["神事", "火祭り"],
        "scale": "国指定重要無形民俗文化財（日本三大火祭り）",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "熊野十二所権現を象徴する十二体の扇神輿が那智大滝へ渡御する神事。日本三大火祭りの一つ。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "熊野那智大社（和歌山県東牟婁郡那智勝浦町那智山）",
        "official_url": "https://kumanonachitaisha.or.jp/event/fan/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://kumanonachitaisha.or.jp/event/fan/", "site_name": "熊野那智大社 飛瀧神社 那智御瀧", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://moyuhi.jp/ja/event/f508d497-e8ca-4dce-b76b-23b244585fb0", "site_name": "もゆひ", "is_official": False, "retrieved_date": "2026-06-30"}
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
        "name": "YOSAKOIソーラン祭り",
        "alternate_names": ["よさこいソーラン祭り"],
        "similar_name_warning": False,
        "prefecture": "北海道",
        "city": "札幌市",
        "date_start": "2026-06-10",
        "date_end": "2026-06-14",
        "date_note": "第35回。約270チーム、27,000人が参加予定。最終日にファイナルステージ開催。",
        "time_start": "不明",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "YOSAKOIソーラン祭り組織委員会",
        "genre": ["踊り"],
        "scale": "その他",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": 35,
        "history_description": "高知のよさこい祭りと北海道民謡「ソーラン節」を組み合わせた祭り。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "大通公園周辺、すすきの、道庁赤れんが会場など札幌市内各所",
        "official_url": "https://www.yosakoi-soran.jp/",
        "sns_accounts": {"instagram": "https://www.instagram.com/4351_yosakoisoran/"},
        "video_url": "不明",
        "sources": [
            {"url": "https://www.yosakoi-soran.jp/schedule", "site_name": "YOSAKOIソーラン祭り 公式ホームページ", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://www.sapporo.travel/news/yosakoi2026/", "site_name": "ようこそさっぽろ（札幌市公式観光サイト）", "is_official": True, "retrieved_date": "2026-06-30"}
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
        "name": "湘南ひらつか七夕まつり",
        "alternate_names": [],
        "similar_name_warning": False,
        "prefecture": "神奈川県",
        "city": "平塚市",
        "date_start": "2026-07-03",
        "date_end": "2026-07-05",
        "date_note": "第74回。7/3・4は20:30まで、7/5は19:00まで。七夕おどり千人パレードは7/3 10:30〜。",
        "time_start": "不明",
        "time_end": "20:30",
        "rain_policy": "不明",
        "organizer": "湘南ひらつか七夕まつり実行委員会",
        "genre": ["七夕"],
        "scale": "その他（関東三大七夕まつり）",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": 74,
        "history_description": "不明",
        "food_stalls": "約100店舗の露店（東海道本通り）",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "JR平塚駅北口すぐ（湘南スターモール・紅谷パールロードほか）",
        "official_url": "https://tanabata-hiratsuka.com/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://tanabata-hiratsuka.com/summary/", "site_name": "湘南ひらつか七夕まつり 公式サイト", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://www.city.hiratsuka.kanagawa.jp/kanko/page-c_01099.html", "site_name": "平塚市公式ウェブサイト", "is_official": True, "retrieved_date": "2026-06-30"}
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
        "name": "浜降祭（茅ヶ崎海岸）",
        "alternate_names": ["暁の祭典 茅ヶ崎海岸浜降祭"],
        "similar_name_warning": False,
        "prefecture": "神奈川県",
        "city": "茅ヶ崎市",
        "date_start": "2026-07-20",
        "date_end": "2026-07-20",
        "date_note": "海の日（祝日）開催。4時頃一番神輿入場、7時〜合同祭開式、8時〜神輿出発。",
        "time_start": "04:00",
        "time_end": "09:00",
        "rain_policy": "不明",
        "organizer": "浜降祭実行委員会",
        "genre": ["神輿"],
        "scale": "その他",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "夜明けとともに市内・寒川町の各神社から約39基の神輿が茅ヶ崎西浜海岸に集まり海でみそぎを行う。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "茅ヶ崎西浜海岸",
        "official_url": "https://www.chigasaki-kankou.org/event/hamaori/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://www.chigasaki-kankou.org/event/hamaori/", "site_name": "茅ヶ崎市観光協会 ちがさきナビ", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://www.city.chigasaki.kanagawa.jp/kankou_list/event/1006906/1006924.html", "site_name": "茅ヶ崎市公式ウェブサイト", "is_official": True, "retrieved_date": "2026-06-30"}
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
        "name": "佐原の大祭（夏祭り）",
        "alternate_names": ["佐原大祭"],
        "similar_name_warning": False,
        "prefecture": "千葉県",
        "city": "香取市",
        "date_start": "2026-07-10",
        "date_end": "2026-07-12",
        "date_note": "各日10:00〜22:00（交通規制あり）。総勢10台の山車が曳き廻される。",
        "time_start": "10:00",
        "time_end": "22:00",
        "rain_policy": "不明",
        "organizer": "佐原の大祭実行委員会",
        "genre": ["山車"],
        "scale": "国指定重要無形民俗文化財／ユネスコ無形文化遺産（関東三大山車祭り）",
        "is_free": True,
        "price": "見学無料",
        "ticket_url": "不明",
        "history_years": 300,
        "history_description": "約300年の伝統を誇る八坂神社の祇園祭。日本三大囃子の一つ「佐原囃子」が有名。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "JR成田線佐原駅から徒歩約10分（小野川周辺・八坂神社周辺）",
        "official_url": "https://maruchiba.jp/event/detail_10868.html",
        "sns_accounts": {"instagram": "https://www.instagram.com/sawaranotaisai_jikkouiinkai/"},
        "video_url": "不明",
        "sources": [
            {"url": "https://maruchiba.jp/event/detail_10868.html", "site_name": "千葉県公式観光サイト ちば観光ナビ", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://sawara-machinami.com/archives/7150", "site_name": "佐原町並み交流館", "is_official": True, "retrieved_date": "2026-06-30"}
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_027",
        "name": "尾張津島天王祭",
        "alternate_names": [],
        "similar_name_warning": False,
        "prefecture": "愛知県",
        "city": "津島市",
        "date_start": "2026-07-25",
        "date_end": "2026-07-26",
        "date_note": "宵祭：7/25 18:30〜（出船20:15）。朝祭：7/26 9:00〜。会場は天王川公園。",
        "time_start": "18:30",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "津島市",
        "genre": ["神事", "船祭り"],
        "scale": "国指定重要無形民俗文化財",
        "is_free": True,
        "price": "見学無料（有料観覧席あり）",
        "ticket_url": "不明",
        "history_years": "不明",
        "history_description": "津島神社（津島天王社）の祭礼。まきわら船と呼ばれる提灯で飾られた巻藁船が川面を彩る。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "名鉄津島駅から徒歩約15分（天王川公園）",
        "official_url": "https://tsushima-kankou.com/tenno/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://tsushima-kankou.com/tenno/", "site_name": "津島市観光協会", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://aichinow.pref.aichi.jp/events/detail/320/", "site_name": "愛知県観光サイト Aichi Now", "is_official": True, "retrieved_date": "2026-06-30"}
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_028",
        "name": "うわじま牛鬼まつり",
        "alternate_names": ["和霊大祭うわじま牛鬼まつり"],
        "similar_name_warning": False,
        "prefecture": "愛媛県",
        "city": "宇和島市",
        "date_start": "2026-07-22",
        "date_end": "2026-07-24",
        "date_note": "第60回。7/22海上花火、7/23ガイヤカーニバル、7/24牛鬼パレード。",
        "time_start": "不明",
        "time_end": "不明",
        "rain_policy": "不明",
        "organizer": "うわじま牛鬼まつり実行委員会",
        "genre": ["神輿", "パレード"],
        "scale": "その他（四国有数の夏祭り）",
        "is_free": True,
        "price": "見学無料（海上花火は一部有料観覧席あり）",
        "ticket_url": "不明",
        "history_years": 60,
        "history_description": "全長6〜7mの牛鬼（妖怪）の形をした作り物が街中を練り歩く四国有数の夏まつり。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "宇和島市街地各所",
        "official_url": "https://ushioni.gaina.ne.jp/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://ushioni.gaina.ne.jp/", "site_name": "うわじま牛鬼まつり 公式ホームページ", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://www.iyokannet.jp/event/1762", "site_name": "いよ観ネット（愛媛県観光情報）", "is_official": True, "retrieved_date": "2026-06-30"}
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_029",
        "name": "松江水郷祭湖上花火大会",
        "alternate_names": ["松江水郷祭"],
        "similar_name_warning": False,
        "prefecture": "島根県",
        "city": "松江市",
        "date_start": "2026-08-01",
        "date_end": "2026-08-02",
        "date_note": "8/1は湖上花火10,000発、8/2は11,000発。打ち上げ20:15〜21:00（20:00〜20:15ドローンショー）。",
        "time_start": "20:00",
        "time_end": "21:00",
        "rain_policy": "雨天決行",
        "organizer": "松江水郷祭実行委員会",
        "genre": ["花火"],
        "scale": "その他",
        "is_free": True,
        "price": "見学無料（有料観覧席あり・ローソンチケット等で販売）",
        "ticket_url": "https://l-tike.com/event/mevent/?mid=653006",
        "history_years": "不明",
        "history_description": "宍道湖上の台船4箇所から打ち上げる花火大会。湖面に映る花火が特徴。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "松江市宍道湖畔",
        "official_url": "https://suigosai.com/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://suigosai.com/about/", "site_name": "松江水郷祭 公式サイト", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://www.kankou-shimane.com/events/43924", "site_name": "しまね観光ナビ（島根県公式）", "is_official": True, "retrieved_date": "2026-06-30"}
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    },
    {
        "id": "festival_030",
        "name": "諏訪湖祭湖上花火大会",
        "alternate_names": [],
        "similar_name_warning": False,
        "prefecture": "長野県",
        "city": "諏訪市",
        "date_start": "2026-08-15",
        "date_end": "2026-08-15",
        "date_note": "第78回。打ち上げ19:00〜。会場は諏訪市湖畔公園前諏訪湖上。",
        "time_start": "19:00",
        "time_end": "不明",
        "rain_policy": "雨天決行",
        "organizer": "諏訪市",
        "genre": ["花火"],
        "scale": "その他",
        "is_free": True,
        "price": "見学無料（有料席あり）",
        "ticket_url": "不明",
        "history_years": 78,
        "history_description": "諏訪湖上に打ち上げられる花火大会。約4万発の花火が湖面に映える。",
        "food_stalls": "不明",
        "crowd_level": "不明",
        "visitors": "不明",
        "access": "JR上諏訪駅から徒歩約15分",
        "official_url": "https://suwako-hanabi.com/kojyou/",
        "sns_accounts": {"instagram": "不明"},
        "video_url": "不明",
        "sources": [
            {"url": "https://suwako-hanabi.com/kojyou/", "site_name": "信州 諏訪湖の花火 公式サイト", "is_official": True, "retrieved_date": "2026-06-30"},
            {"url": "https://www.suwakanko.jp/story/hanabi-suwako/", "site_name": "諏訪観光協会 公式サイト", "is_official": True, "retrieved_date": "2026-06-30"}
        ],
        "trust_level": "高",
        "conflict_note": "",
        "requires_check": False,
        "diff_status": "NEW",
        "updated_fields": [],
        "year_comparison": {"changed": False, "details": "不明（初回登録のため比較対象なし）"}
    }
]


def update():
    with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    festivals = data.get('festivals', [])

    # 既存祭りの diff_status を UNCHANGED に更新
    existing_ids = set()
    for f in festivals:
        if f.get('diff_status') in ('NEW', 'UPDATED'):
            f['diff_status'] = 'UNCHANGED'
        existing_ids.add(f['id'])

    # 新規祭りを追加（重複を避ける）
    added = 0
    for nf in NEW_FESTIVALS:
        if nf['id'] not in existing_ids:
            festivals.append(nf)
            added += 1

    data['festivals'] = festivals
    data['last_updated'] = '2026-06-30 10:00'

    with open(FESTIVALS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"festivals.json 更新完了: 既存{len(existing_ids)}件 → 新規{added}件追加 → 合計{len(festivals)}件")

    # last_post.json 更新
    last_post = {
        "last_executed": "2026-06-30 10:00",
        "has_update": added > 0,
        "posted_to_instagram": False
    }
    with open(LAST_POST_JSON, 'w', encoding='utf-8') as f:
        json.dump(last_post, f, ensure_ascii=False, indent=2)
    print(f"last_post.json 更新完了: has_update={last_post['has_update']}")


if __name__ == '__main__':
    update()
