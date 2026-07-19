# -*- coding: utf-8 -*-
"""GA4 Data API からアクセスデータを取得し data/analytics_snapshot.json に保存する。

認証は環境変数 GA4_SERVICE_ACCOUNT_JSON（サービスアカウントJSONキーの中身全体）を
メモリ上でパースして行う。キーを一時ファイルにもログにも書き出さない。

終了コード:
  0 = 正常（アクセス0件でも snapshot は正常保存される）
  2 = 環境変数が未設定
  1 = API エラー等（data/error_log.json に追記される）
"""

import json
import os
import sys
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
SNAPSHOT_PATH = os.path.join(DATA_DIR, 'analytics_snapshot.json')
ERROR_LOG_PATH = os.path.join(DATA_DIR, 'error_log.json')
PERIOD_DAYS = 7


def load_env():
    """.env を読み込む（既存の環境変数は上書きしない＝CI/ルーティンのSecretsを優先）"""
    env_path = os.path.join(ROOT_DIR, '.env')
    if not os.path.exists(env_path):
        return
    with open(env_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def append_error_log(error, detail):
    """data/error_log.json（{"errors": [...]} 形式）にエラーを追記する。
    detail に秘密情報（キーの中身等）を含めないこと。"""
    try:
        with open(ERROR_LOG_PATH, encoding='utf-8') as f:
            log = json.load(f)
    except (OSError, json.JSONDecodeError):
        log = {'errors': []}
    log.setdefault('errors', []).append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'step': 'fetch_analytics',
        'error': error,
        'detail': detail,
    })
    with open(ERROR_LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
        f.write('\n')


def build_client(service_account_json):
    """サービスアカウントJSON文字列から GA4 Data API クライアントを作る。
    キーはメモリ上でのみ扱い、ファイルには書き出さない。"""
    from google.oauth2 import service_account
    from google.analytics.data_v1beta import BetaAnalyticsDataClient

    info = json.loads(service_account_json)
    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/analytics.readonly'])
    return BetaAnalyticsDataClient(credentials=credentials)


def run_report(client, property_id, dimensions, metrics):
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest)

    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=f'{PERIOD_DAYS}daysAgo', end_date='today')],
    )
    return client.run_report(request)


def fetch_snapshot(client, property_id):
    snapshot = {
        'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'period_days': PERIOD_DAYS,
        'pages': [],
        'totals': {'sessions': 0, 'channels': {}, 'devices': {}},
    }

    # ページ別: ページビュー数と平均エンゲージメント時間
    res = run_report(client, property_id, ['pagePath'],
                     ['screenPageViews', 'userEngagementDuration'])
    for row in res.rows:
        views = int(float(row.metric_values[0].value or 0))
        engagement = float(row.metric_values[1].value or 0)
        snapshot['pages'].append({
            'path': row.dimension_values[0].value,
            'views': views,
            'avg_engagement_sec': round(engagement / views, 1) if views else 0,
        })
    snapshot['pages'].sort(key=lambda p: p['views'], reverse=True)

    # サイト全体: セッション数
    res = run_report(client, property_id, [], ['sessions'])
    if res.rows:
        snapshot['totals']['sessions'] = int(float(res.rows[0].metric_values[0].value or 0))

    # 流入元別セッション数
    res = run_report(client, property_id, ['sessionDefaultChannelGroup'], ['sessions'])
    for row in res.rows:
        snapshot['totals']['channels'][row.dimension_values[0].value] = \
            int(float(row.metric_values[0].value or 0))

    # デバイス別セッション数
    res = run_report(client, property_id, ['deviceCategory'], ['sessions'])
    for row in res.rows:
        snapshot['totals']['devices'][row.dimension_values[0].value] = \
            int(float(row.metric_values[0].value or 0))

    return snapshot


def main():
    load_env()

    property_id = os.environ.get('GA4_PROPERTY_ID', '').strip()
    service_account_json = os.environ.get('GA4_SERVICE_ACCOUNT_JSON', '').strip()

    missing = [name for name, val in [('GA4_PROPERTY_ID', property_id),
                                      ('GA4_SERVICE_ACCOUNT_JSON', service_account_json)] if not val]
    if missing:
        msg = f"環境変数が未設定: {', '.join(missing)}"
        print(f'[fetch_analytics] エラー: {msg}')
        append_error_log('GA4環境変数が未設定', msg)
        return 2

    try:
        client = build_client(service_account_json)
    except ImportError:
        msg = 'google-analytics-data がインストールされていません（pip install -r requirements.txt を実行してください）'
        print(f'[fetch_analytics] エラー: {msg}')
        append_error_log('GA4ライブラリ未インストール', msg)
        return 1
    except (ValueError, KeyError) as e:
        # JSONキーのパース失敗。キーの中身はログに出さない
        msg = f'GA4_SERVICE_ACCOUNT_JSON の形式が不正です（{type(e).__name__}）。サービスアカウントJSONの中身全体が設定されているか確認してください。'
        print(f'[fetch_analytics] エラー: {msg}')
        append_error_log('GA4サービスアカウント認証情報の形式不正', msg)
        return 1

    try:
        snapshot = fetch_snapshot(client, property_id)
    except Exception as e:
        # API呼び出し失敗。例外メッセージには秘密情報は含まれない（キー自体は渡していない）
        msg = f'GA4 Data API の呼び出しに失敗: {type(e).__name__}: {e}'
        print(f'[fetch_analytics] エラー: {msg}')
        append_error_log('GA4 Data API呼び出し失敗', msg)
        return 1

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SNAPSHOT_PATH, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'[fetch_analytics] 保存完了: {SNAPSHOT_PATH}')
    print(f"  期間: 過去{PERIOD_DAYS}日 / ページ数: {len(snapshot['pages'])} / "
          f"セッション: {snapshot['totals']['sessions']}")
    if not snapshot['pages']:
        print('  ※ データ0件（サイト公開直後でアクセスが無いのは正常な状態です）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
