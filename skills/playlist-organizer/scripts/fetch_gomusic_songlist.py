#!/usr/bin/env python3
"""Fetch a playlist link through the configured GoMusic API and save a song list."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_ENDPOINT = 'http://114.132.198.202:18081/api/playlist'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Fetch song list text from GoMusic API.')
    parser.add_argument('--url', required=True, help='Playlist URL to extract.')
    parser.add_argument('--output', required=True, help='Output txt path for extracted songs.')
    parser.add_argument('--endpoint', default=API_ENDPOINT, help='GoMusic API endpoint.')
    parser.add_argument('--timeout', type=int, default=30, help='HTTP timeout in seconds.')
    return parser.parse_args()


def format_song(item: object) -> str:
    if isinstance(item, str):
        return item.strip()

    if not isinstance(item, dict):
        return str(item).strip()

    title = item.get('name') or item.get('title') or item.get('song') or item.get('song_name')
    singer = item.get('singer') or item.get('artist') or item.get('artists') or item.get('author')

    if isinstance(singer, list):
        singer = '、'.join(str(value).strip() for value in singer if str(value).strip())

    if title and singer:
        return f'{title} - {singer}'.strip()
    if title:
        return str(title).strip()
    return str(item).strip()


def format_song_list(items: list[object]) -> str:
    return '\n'.join(song for song in (format_song(item) for item in items) if song)


def extract_text(response_body: str) -> str:
    text = response_body.strip('﻿\n\r\t ')
    if not text:
        return ''

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return text

    if isinstance(payload, str):
        return payload.strip()

    if isinstance(payload, list):
        return format_song_list(payload)

    if isinstance(payload, dict):
        for key in ('data', 'songs', 'songlist', 'result', 'text'):
            value = payload.get(key)
            if isinstance(value, str):
                return value.strip()
            if isinstance(value, list):
                return format_song_list(value)
            if isinstance(value, dict):
                for nested_key in ('songs', 'songlist', 'list', 'items', 'tracks'):
                    nested_value = value.get(nested_key)
                    if isinstance(nested_value, str):
                        return nested_value.strip()
                    if isinstance(nested_value, list):
                        return format_song_list(nested_value)

    raise ValueError('GoMusic API 返回了无法识别的 JSON 结构。')


def fetch_songlist(endpoint: str, playlist_url: str, timeout: int) -> str:
    data = json.dumps({
        'url': playlist_url,
        'detailed': False,
        'format': 'song-singer',
        'order': 'normal',
    }).encode('utf-8')
    request = Request(
        endpoint,
        data=data,
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'playlist-organizer/1.0',
        },
        method='POST',
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            body = response.read().decode(charset, errors='replace')
    except HTTPError as error:
        detail = error.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'歌单解析 API HTTP {error.code}: {detail[:500]}') from error
    except URLError as error:
        raise RuntimeError(f'歌单解析 API 请求失败：{error.reason}') from error

    return extract_text(body)


def main() -> int:
    args = parse_args()
    songlist = fetch_songlist(args.endpoint, args.url, args.timeout)
    lines = [line.strip() for line in songlist.splitlines() if line.strip()]
    if not lines:
        raise ValueError('GoMusic API 没有返回可用歌曲。')

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'已写入 {len(lines)} 首歌曲：{output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
