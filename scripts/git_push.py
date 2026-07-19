import json
import os
import subprocess
from datetime import datetime

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FESTIVALS_JSON = os.path.join(DATA_DIR, 'festivals.json')
ERROR_LOG_JSON = os.path.join(DATA_DIR, 'error_log.json')

# push 前の同期でコンフリクトしても「ローカル（ルーティン生成物）優先」で
# 自動解決してよいパス。これ以外のファイルは人間の編集物とみなし、自動解決しない。
GENERATED_PREFIXES = ('data/', 'docs/')

# fetch → rebase → push のサイクルを試す最大回数（無限ループ防止）
MAX_PUSH_ATTEMPTS = 3

# 1回の rebase 中に処理するコンフリクト停止回数の上限（無限ループ防止の保険）
MAX_REBASE_STEPS = 100


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


def log_error(error, detail):
    """data/error_log.json の errors 配列に追記する（既存書式に合わせる）"""
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'step': 'git_push',
        'error': error,
        'detail': detail,
    }
    try:
        if os.path.exists(ERROR_LOG_JSON):
            with open(ERROR_LOG_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {'errors': []}
        data.setdefault('errors', []).append(entry)
        with open(ERROR_LOG_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
    except Exception as e:
        print(f"error_log.json への記録に失敗: {e}")


def is_generated(path):
    """自動解決してよい生成物パスかどうか"""
    return path.replace('\\', '/').startswith(GENERATED_PREFIXES)


def rebase_in_progress():
    res = run_git(['rev-parse', '--git-dir'])
    git_dir = res.stdout.strip()
    if not os.path.isabs(git_dir):
        git_dir = os.path.join(ROOT_DIR, git_dir)
    return (os.path.exists(os.path.join(git_dir, 'rebase-merge'))
            or os.path.exists(os.path.join(git_dir, 'rebase-apply')))


def conflicted_files():
    res = run_git(['diff', '--name-only', '--diff-filter=U'])
    return [line.strip() for line in res.stdout.splitlines() if line.strip()]


def abort_rebase(error, detail):
    """rebase を中断して error_log.json に記録する"""
    run_git(['rebase', '--abort'])
    print(f"rebase 中断: {error}")
    log_error(error, detail)


def resolve_rebase_conflicts():
    """rebase のコンフリクトを解決する。

    生成物（data/・docs/）のみのコンフリクトはローカル側を採用して続行。
    人間が編集するファイルのコンフリクトは rebase を中断して False を返す。
    ※ rebase 中は --theirs が「ローカル（今回のルーティンのコミット）」側。
    """
    for _ in range(MAX_REBASE_STEPS):
        if not rebase_in_progress():
            return True

        files = conflicted_files()
        if files:
            human_files = [f for f in files if not is_generated(f)]
            if human_files:
                abort_rebase(
                    "人間編集ファイルでコンフリクトのため rebase を中断",
                    f"コンフリクトファイル: {', '.join(files)} のうち自動解決不可: "
                    f"{', '.join(human_files)}。リモートの変更を上書きしないよう "
                    "push せずに終了した。手動でリモートの変更を取り込んでください。",
                )
                return False
            print(f"生成物のコンフリクトをローカル優先で解決: {', '.join(files)}")
            for f in files:
                # rebase 中の --theirs = ローカル（ルーティン生成）側
                co = run_git(['checkout', '--theirs', '--', f])
                if co.returncode != 0:
                    # ローカル側でファイルが削除されている場合は削除を採用
                    rm = run_git(['rm', '--force', '--', f])
                    if rm.returncode != 0:
                        abort_rebase(
                            f"コンフリクト解決に失敗: {f}",
                            f"checkout --theirs: {co.stderr.strip()} / "
                            f"rm: {rm.stderr.strip()}",
                        )
                        return False
                    continue
                add = run_git(['add', '--', f])
                if add.returncode != 0:
                    abort_rebase(f"git add に失敗: {f}", add.stderr.strip())
                    return False

        cont = run_git(['-c', 'core.editor=true', 'rebase', '--continue'])
        if cont.returncode == 0:
            continue  # 次のループで完了判定（さらに停止していれば再処理）
        if conflicted_files():
            continue  # 次のコミットで新たなコンフリクト → ループで処理
        # コンフリクトなしで continue が失敗 = 解決の結果コミットが空になった等
        skip = run_git(['rebase', '--skip'])
        if skip.returncode != 0 and rebase_in_progress() and not conflicted_files():
            abort_rebase(
                "rebase を継続できないため中断",
                f"continue: {cont.stderr.strip() or cont.stdout.strip()} / "
                f"skip: {skip.stderr.strip() or skip.stdout.strip()}",
            )
            return False

    abort_rebase(
        "rebase のコンフリクト解決が上限回数を超えたため中断",
        f"{MAX_REBASE_STEPS} 回のコンフリクト解決を試みたが完了しなかった。",
    )
    return False


def sync_and_push():
    """リモート最新を取り込んでから push する。最大 MAX_PUSH_ATTEMPTS 回試行。"""
    last_error = ''
    for attempt in range(1, MAX_PUSH_ATTEMPTS + 1):
        fetch = run_git(['fetch', 'origin', 'main'])
        if fetch.returncode != 0:
            last_error = f"git fetch 失敗: {fetch.stderr.strip()}"
            print(f"{last_error}（{attempt}/{MAX_PUSH_ATTEMPTS}回目）")
            continue

        # origin/main が HEAD の祖先でなければ、リモートが進んでいる
        ancestor = run_git(['merge-base', '--is-ancestor', 'origin/main', 'HEAD'])
        if ancestor.returncode != 0:
            print("リモート main が進んでいるため rebase で取り込みます")
            rebase = run_git(['-c', 'core.editor=true', 'rebase', 'origin/main'])
            if rebase.returncode != 0:
                if rebase_in_progress():
                    if not resolve_rebase_conflicts():
                        return False  # 中断済み・記録済み（リトライしない）
                else:
                    last_error = f"git rebase 失敗: {rebase.stderr.strip()}"
                    print(f"{last_error}（{attempt}/{MAX_PUSH_ATTEMPTS}回目）")
                    continue
            print("rebase 完了（リモートの変更を取り込みました）")

        push = run_git(['push', 'origin', 'HEAD:main'])
        if push.returncode == 0:
            print("git push 成功 (origin main)")
            return True
        last_error = f"git push 失敗: {push.stderr.strip()}"
        print(f"{last_error}（{attempt}/{MAX_PUSH_ATTEMPTS}回目）")

    log_error(
        f"push を{MAX_PUSH_ATTEMPTS}回試行したが成功しなかった",
        last_error or '原因不明',
    )
    return False


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

    return sync_and_push()


if __name__ == '__main__':
    git_push()
