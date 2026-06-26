#!/usr/bin/env python3
"""Build playlist text files from a song list and assignment JSON."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

TITLE_COLUMNS = ('title', 'track', 'name', 'song', '歌曲名', '歌名', '曲名')
ARTIST_COLUMNS = ('artist', 'artists', 'singer', '歌手', '艺人')
INVALID_FILENAME_CHARS = r'<>:"/\\|?*'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Build playlist txt files from song assignments.')
    parser.add_argument('--input', required=True, help='Input txt/csv song list.')
    parser.add_argument('--output-dir', required=True, help='Directory for generated playlist files.')
    parser.add_argument('--assignments', required=True, help='JSON mapping playlist names to 1-based indexes or song strings.')
    parser.add_argument('--uncertain', help='Optional JSON list of uncertain 1-based indexes or song strings.')
    parser.add_argument('--allow-repeats', action='store_true', help='Allow one source entry to appear in multiple playlists.')
    parser.add_argument('--require-coverage', action='store_true', help='Report failure when any source entry is uncovered.')
    parser.add_argument('--import-ready', action='store_true', help='Use plain import-ready txt output. Currently this is the default format.')
    return parser.parse_args()


def canonicalize_song(value: str) -> str:
    value = value.strip().lstrip('﻿')
    value = re.sub(r'^\s*\d+[.、\s]+', '', value)
    value = re.sub(r'\s+', ' ', value)
    return value.strip()


def read_txt(path: Path) -> list[str]:
    songs: list[str] = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        song = canonicalize_song(line)
        if song:
            songs.append(song)
    return songs


def find_column(fieldnames: list[str] | None, candidates: tuple[str, ...]) -> str | None:
    if not fieldnames:
        return None
    normalized = {name.strip().lower(): name for name in fieldnames}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    return None


def read_csv(path: Path) -> list[str]:
    songs: list[str] = []
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        title_column = find_column(reader.fieldnames, TITLE_COLUMNS)
        artist_column = find_column(reader.fieldnames, ARTIST_COLUMNS)
        if not title_column:
            raise ValueError(f'CSV 缺少歌曲名列。支持列名：{", ".join(TITLE_COLUMNS)}')
        for row in reader:
            title = (row.get(title_column) or '').strip()
            artist = (row.get(artist_column) or '').strip() if artist_column else ''
            if title:
                songs.append(canonicalize_song(f'{title} - {artist}' if artist else title))
    return songs


def read_songs(path: Path) -> list[str]:
    return read_csv(path) if path.suffix.lower() == '.csv' else read_txt(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def resolve_item(item: Any, songs: list[str]) -> tuple[int | None, str]:
    if isinstance(item, int):
        index = item - 1
        if index < 0 or index >= len(songs):
            raise ValueError(f'歌曲编号超出范围：{item}')
        return index, songs[index]
    if isinstance(item, str):
        song = canonicalize_song(item)
        try:
            return songs.index(song), song
        except ValueError:
            return None, song
    raise TypeError(f'不支持的 assignment 项：{item!r}')


def sanitize_filename(name: str) -> str:
    sanitized = ''.join('_' if char in INVALID_FILENAME_CHARS else char for char in name).strip()
    return sanitized.rstrip('.') or '未命名歌单'


def write_playlist(path: Path, songs: list[str]) -> None:
    path.write_text('\n'.join(songs) + ('\n' if songs else ''), encoding='utf-8')


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    assignments = load_json(Path(args.assignments))

    if not isinstance(assignments, dict):
        raise ValueError('assignments JSON 必须是对象：{"歌单名": [歌曲编号或歌曲字符串]}')

    songs = read_songs(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    covered_indexes: set[int] = set()
    playlist_counts: dict[str, int] = {}
    generated_files: list[str] = []

    for playlist_name, raw_items in assignments.items():
        if not isinstance(raw_items, list):
            raise ValueError(f'歌单 {playlist_name} 的值必须是数组。')

        resolved_songs: list[str] = []
        for item in raw_items:
            index, song = resolve_item(item, songs)
            resolved_songs.append(song)
            if index is not None:
                covered_indexes.add(index)

        filename = sanitize_filename(str(playlist_name)) + '.txt'
        write_playlist(output_dir / filename, resolved_songs)
        playlist_counts[filename] = len(resolved_songs)
        generated_files.append(filename)

    uncertain_entries: list[str] = []
    if args.uncertain:
        raw_uncertain = load_json(Path(args.uncertain))
        if not isinstance(raw_uncertain, list):
            raise ValueError('uncertain JSON 必须是数组。')
        for item in raw_uncertain:
            _, song = resolve_item(item, songs)
            uncertain_entries.append(song)
        write_playlist(output_dir / '待整理.txt', uncertain_entries)
        generated_files.append('待整理.txt')

    uncovered = [(index + 1, song) for index, song in enumerate(songs) if index not in covered_indexes]
    status = '未通过：存在未覆盖歌曲' if args.require_coverage and uncovered else '通过'

    report_lines = [
        '歌单生成报告',
        f'状态：{status}',
        f'来源文件：{input_path}',
        f'来源歌曲条目数：{len(songs)}',
        f'已覆盖条目数：{len(covered_indexes)}',
        f'要求全覆盖：{"是" if args.require_coverage else "否"}',
        f'允许重复归属：{"是" if args.allow_repeats else "否"}',
        '',
        '生成文件：',
    ]
    report_lines.extend(f'- {filename}' for filename in generated_files)
    report_lines.extend(['', '各歌单条目数：'])
    report_lines.extend(f'- {filename}：{count}' for filename, count in playlist_counts.items())

    if uncertain_entries:
        report_lines.extend(['', f'不确定条目数：{len(uncertain_entries)}'])
        report_lines.extend(f'- {song}' for song in uncertain_entries)

    if uncovered:
        report_lines.extend(['', f'未覆盖条目数：{len(uncovered)}'])
        report_lines.extend(f'- {index}. {song}' for index, song in uncovered[:200])
        if len(uncovered) > 200:
            report_lines.append(f'- ……还有 {len(uncovered) - 200} 条未显示')

    report_lines.extend(['', '说明：输出 txt 为导入友好的纯文本格式，每行一首歌。'])
    report = '\n'.join(report_lines) + '\n'
    (output_dir / '生成报告.txt').write_text(report, encoding='utf-8')
    print(report)
    return 1 if args.require_coverage and uncovered else 0


if __name__ == '__main__':
    raise SystemExit(main())
