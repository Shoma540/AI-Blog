import json
import os
from datetime import datetime

import requests

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')
LAST_POST_JSON = os.path.join(DATA_DIR, 'last_post.json')
CONFIG_JSON = os.path.join(ROOT_DIR, 'config.json')
ASSETS_IMAGES_DIR = os.path.join(ROOT_DIR, 'assets', 'images')

GRAPH_API_VERSION = "v21.0"
MAX_CAPTION_LENGTH = 2200
DEFAULT_IMAGE = "default.png"


def load_env():
    """.env を読み込む（既存の環境変数は上書きしない＝CIのSecretsを優先）"""
    env_path = os.path.join(ROOT_DIR, '.env')
    if not os.path.exists(env_path):
        return
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def should_post():
    """12時台は無条件で投稿。それ以外は has_update が true の場合のみ。"""
    if datetime.now().hour == 12:
        return True
    if os.path.exists(LAST_POST_JSON):
        with open(LAST_POST_JSON, 'r', encoding='utf-8') as f:
            return json.load(f).get('has_update', False)
    return False


def load_festivals():
    if os.path.exists(FESTIVALS_JSON):
        with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f).get('festivals', [])
    return []


def load_config():
    if os.path.exists(CONFIG_JSON):
        with open(CONFIG_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def select_image_file(festivals, config):
    """祭りのジャンルから使用する画像ファイル名を決定する。

    - NEW/UPDATED の祭りを優先（なければ先頭）し、その祭りのジャンルを使う
    - ジャンルと画像の対応は config.json の genre_images で管理
    - 複数ジャンルを持つ場合は genre_priority 順で最も固有性の高いものを選ぶ
    - 未対応ジャンル、またはローカルにファイルが無い場合は default にフォールバック
    """
    genre_images = config.get('genre_images', {})
    default_image = config.get('default_image', DEFAULT_IMAGE)
    priority = config.get('genre_priority', [])

    target = next(
        (f for f in festivals if f.get('diff_status') in ('NEW', 'UPDATED')),
        None,
    )
    if target is None and festivals:
        target = festivals[0]

    filename = default_image
    if target:
        genres = target.get('genre') or []
        # 1. genre_priority順で最初にマッチしたジャンルの画像
        picked = None
        for p in priority:
            if p in genres and p in genre_images:
                picked = genre_images[p]
                break
        # 2. 優先リストに無いが画像があるジャンルを、genre順で
        if picked is None:
            for g in genres:
                if g in genre_images:
                    picked = genre_images[g]
                    break
        if picked is not None:
            filename = picked

    # ローカルにファイルが無ければ default にフォールバック
    if not os.path.exists(os.path.join(ASSETS_IMAGES_DIR, filename)):
        filename = default_image
    return filename


def resolve_image_url(filename, config):
    """画像ファイル名を、Instagramが取得できる公開URLに変換する。

    IG_IMAGE_URL（手動指定）があれば最優先。次に IMAGE_BASE_URL 環境変数、
    最後に config.json の image_base_url を使う。いずれも無ければ空文字。
    """
    override = os.environ.get('IG_IMAGE_URL', '')
    if override:
        return override
    base = os.environ.get('IMAGE_BASE_URL') or config.get('image_base_url', '')
    if not base:
        return ''
    return f"{base.rstrip('/')}/{filename}"


def compose_caption(festivals):
    new_count = sum(1 for f in festivals if f.get('diff_status') == 'NEW')
    updated_count = sum(1 for f in festivals if f.get('diff_status') == 'UPDATED')
    examples = [
        f.get('name', '') for f in festivals
        if f.get('diff_status') in ('NEW', 'UPDATED') and f.get('name')
    ][:5]
    site_url = os.environ.get('SITE_URL', '')

    lines = ["🎉全国祭り情報を更新しました"]
    if new_count or updated_count:
        lines.append(f"新規{new_count}件 / 更新{updated_count}件")
    if examples:
        lines.append("")
        lines.extend(f"・{name}" for name in examples)
    if site_url:
        lines.append("")
        lines.append(site_url)
    lines.append("")
    lines.append("#祭り #全国祭り情報 #日本の祭り #festival")

    caption = "\n".join(lines)
    if len(caption) > MAX_CAPTION_LENGTH:
        caption = caption[:MAX_CAPTION_LENGTH - 1] + "…"
    return caption


def mark_posted():
    """last_post.json の posted_to_instagram を true にする"""
    data = {}
    if os.path.exists(LAST_POST_JSON):
        with open(LAST_POST_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
    data['posted_to_instagram'] = True
    with open(LAST_POST_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def post_instagram(caption, image_url):
    access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    ig_user_id = os.environ.get('INSTAGRAM_BUSINESS_ACCOUNT_ID')

    missing = [name for name, value in [
        ('INSTAGRAM_ACCESS_TOKEN', access_token),
        ('INSTAGRAM_BUSINESS_ACCOUNT_ID', ig_user_id),
    ] if not value]
    if missing:
        print(f"Instagram認証情報が不足しています: {', '.join(missing)}")
        return False

    if not image_url:
        print("画像の公開URLを解決できないため Instagram投稿をスキップしました"
              "（config.json の image_base_url か IG_IMAGE_URL を設定してください）")
        return False

    base = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_user_id}"

    create = requests.post(f"{base}/media", data={
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token,
    })
    if create.status_code != 200:
        print(f"Instagramメディア作成失敗: {create.status_code} {create.text}")
        return False
    creation_id = create.json().get('id')
    if not creation_id:
        print(f"Instagram creation_id を取得できませんでした: {create.text}")
        return False

    publish = requests.post(f"{base}/media_publish", data={
        "creation_id": creation_id,
        "access_token": access_token,
    })
    if publish.status_code != 200:
        print(f"Instagram公開失敗: {publish.status_code} {publish.text}")
        return False
    print("Instagram投稿成功")
    return True


def main():
    load_env()
    if not should_post():
        print("投稿条件を満たさないため Instagram投稿をスキップしました")
        return False
    config = load_config()
    festivals = load_festivals()
    image_file = select_image_file(festivals, config)
    image_url = resolve_image_url(image_file, config)
    print(f"使用画像: {image_file} -> {image_url or '(URL未解決)'}")
    if post_instagram(compose_caption(festivals), image_url):
        mark_posted()
        return True
    return False


if __name__ == '__main__':
    main()
