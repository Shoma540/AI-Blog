# -*- coding: utf-8 -*-
"""push 前のサイト検証スクリプト（plan.md フェーズ3）。

チェック項目（全て通れば終了コード0、1つでも失敗なら非0）:
  1. python scripts/generate_html.py がエラーなく完走する
  2. docs/ 配下の全 HTML がパース可能（html.parser）
  3. index.html / map.html / calendar.html から張られている prefecture/*.html,
     month/*.html への相対リンクが全て実在するファイルを指す
  4. GA4 タグ（G-6NXKRMQDZ0）が docs/ 配下の全 HTML に含まれる
  5. docs/index.html に festival-card クラスの要素が1件以上ある

検証は読み取りのみ（docs/ を書き換えるのは項目1の generate_html.py 実行だけ）。
--skip-generate を付けると項目1を飛ばし、現状の docs/ をそのまま検証する
（壊れた状態の検知テストや、生成済みサイトの再確認用）。
"""

import os
import subprocess
import sys
import urllib.parse
from html.parser import HTMLParser

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(ROOT_DIR, 'docs')
GA4_TAG = 'G-6NXKRMQDZ0'
LINK_SOURCE_FILES = ['index.html', 'map.html', 'calendar.html']
LINK_TARGET_PREFIXES = ('prefecture/', 'month/')


class LinkAndCardParser(HTMLParser):
    """href と class="festival-card" を収集するパーサ"""

    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.festival_card_count = 0

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name == 'href':
                self.hrefs.append(value)
            elif name == 'class' and 'festival-card' in value.split():
                self.festival_card_count += 1


def list_html_files():
    files = []
    for dirpath, _dirnames, filenames in os.walk(DOCS_DIR):
        for fn in filenames:
            if fn.endswith('.html'):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def parse_html_file(path):
    """html.parser でパースし、(パーサ, エラー文字列 or None) を返す"""
    parser = LinkAndCardParser()
    try:
        with open(path, encoding='utf-8') as f:
            parser.feed(f.read())
        parser.close()
    except Exception as e:
        return parser, f'{type(e).__name__}: {e}'
    return parser, None


def check_generate_html():
    """項目1: generate_html.py がエラーなく完走する"""
    result = subprocess.run(
        [sys.executable, os.path.join(ROOT_DIR, 'scripts', 'generate_html.py')],
        cwd=ROOT_DIR, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        tail = (result.stderr or result.stdout or '').strip().splitlines()[-10:]
        return ['generate_html.py が終了コード {} で失敗:\n    {}'.format(
            result.returncode, '\n    '.join(tail))]
    return []


def check_all_html(html_files):
    """項目2・4・5: パース可能 / GA4タグ / festival-card をまとめて検査"""
    parse_errors = []
    ga4_errors = []
    card_errors = []
    index_path = os.path.join(DOCS_DIR, 'index.html')
    links_by_file = {}

    for path in html_files:
        rel = os.path.relpath(path, DOCS_DIR).replace(os.sep, '/')
        parser, err = parse_html_file(path)
        if err:
            parse_errors.append(f'docs/{rel} がパース不能: {err}')
            continue
        with open(path, encoding='utf-8') as f:
            content = f.read()
        if GA4_TAG not in content:
            ga4_errors.append(f'docs/{rel} に GA4 タグ（{GA4_TAG}）が無い')
        links_by_file[rel] = parser.hrefs
        if os.path.normpath(path) == os.path.normpath(index_path):
            if parser.festival_card_count < 1:
                card_errors.append('docs/index.html に festival-card クラスの要素が1件も無い')

    if not os.path.exists(index_path):
        card_errors.append('docs/index.html が存在しない')

    return parse_errors, ga4_errors, card_errors, links_by_file


def check_internal_links(links_by_file):
    """項目3: index/map/calendar から prefecture/, month/ への相対リンクが実在するか"""
    errors = []
    for src in LINK_SOURCE_FILES:
        if src not in links_by_file:
            errors.append(f'docs/{src} が存在しない（またはパース不能）')
            continue
        for href in links_by_file[src]:
            # フラグメント・クエリを除去し、URLエンコードを戻す
            target = urllib.parse.unquote(href.split('#')[0].split('?')[0])
            if target.startswith('./'):
                target = target[2:]
            if not target or not any(target.startswith(p) for p in LINK_TARGET_PREFIXES):
                continue
            target_path = os.path.normpath(os.path.join(DOCS_DIR, target))
            if not os.path.isfile(target_path):
                errors.append(f'docs/{src} のリンク切れ: {href} → docs/{target} が存在しない')
    return errors


def main():
    skip_generate = '--skip-generate' in sys.argv[1:]
    failures = []

    # 項目1
    if skip_generate:
        print('[1] generate_html.py の実行: スキップ（--skip-generate）')
    else:
        errs = check_generate_html()
        failures += errs
        print(f"[1] generate_html.py の実行: {'NG' if errs else 'OK'}")

    if not os.path.isdir(DOCS_DIR):
        failures.append('docs/ ディレクトリが存在しない')
        html_files = []
    else:
        html_files = list_html_files()

    # 項目2・4・5
    parse_errors, ga4_errors, card_errors, links_by_file = check_all_html(html_files)
    failures += parse_errors + ga4_errors + card_errors
    print(f"[2] 全HTMLのパース（{len(html_files)}ファイル）: {'NG' if parse_errors else 'OK'}")

    # 項目3
    link_errors = check_internal_links(links_by_file)
    failures += link_errors
    print(f"[3] 内部リンク（prefecture/・month/）: {'NG' if link_errors else 'OK'}")
    print(f"[4] GA4タグ（{GA4_TAG}）全ページ確認: {'NG' if ga4_errors else 'OK'}")
    print(f"[5] index.html の festival-card: {'NG' if card_errors else 'OK'}")

    if failures:
        print(f'\n検証失敗（{len(failures)}件）:')
        for msg in failures:
            print(f'  - {msg}')
        return 1

    print('\n全チェック通過: push 可能です')
    return 0


if __name__ == '__main__':
    sys.exit(main())
