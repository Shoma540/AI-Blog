import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')
LAST_POST_JSON = os.path.join(DATA_DIR, 'last_post.json')


def load_festivals():
    if os.path.exists(FESTIVALS_JSON):
        with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_updated": "", "festivals": []}


def save_festivals(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(FESTIVALS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"festivals.json を保存しました: {data['last_updated']}")


def save_last_post(has_update: bool, posted_x: bool, posted_instagram: bool):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {
        "last_executed": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "has_update": has_update,
        "posted_to_x": posted_x,
        "posted_to_instagram": posted_instagram
    }
    with open(LAST_POST_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"last_post.json を保存しました")


def load_last_post():
    if os.path.exists(LAST_POST_JSON):
        with open(LAST_POST_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"has_update": False}


if __name__ == '__main__':
    data = load_festivals()
    print(f"現在の祭り件数: {len(data['festivals'])}件")
