import json
import os
import subprocess
from datetime import datetime

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')


def count_diffs():
    """festivals.json から NEW / UPDATED の件数を数える"""
    if not os.path.exists(FESTIVALS_JSON):
        return 0, 0
    with open(FESTIVALS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    festivals = data.get('festivals', [])
    new_count = sum(1 for f in festivals if f.get('diff_status') == 'NEW')
    updated_count = sum(1 for f in festivals if f.get('diff_status') == 'UPDATED')
    return new_count, updated_count


def run_git(args):
    return subprocess.run(
        ['git'] + args,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )


def git_push():
    new_count, updated_count = count_diffs()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    message = f"祭り情報更新 {timestamp} - 新規:{new_count}件 更新:{updated_count}件"

    add = run_git(['add', '.'])
    if add.returncode != 0:
        print(f"git add 失敗: {add.stderr.strip()}")
        return False

    # ステージ後に変更がなければ commit/push はスキップ
    status = run_git(['status', '--porcelain'])
    if not status.stdout.strip():
        print("変更がないため commit/push をスキップしました")
        return False

    commit = run_git(['commit', '-m', message])
    if commit.returncode != 0:
        print(f"git commit 失敗: {commit.stderr.strip() or commit.stdout.strip()}")
        return False
    print(f"コミットしました: {message}")

    push = run_git(['push', 'origin', 'HEAD:main'])
    if push.returncode != 0:
        print(f"git push 失敗: {push.stderr.strip()}")
        return False
    print("git push 成功 (origin main)")
    return True


if __name__ == '__main__':
    git_push()
