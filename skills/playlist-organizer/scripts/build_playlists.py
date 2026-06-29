#!/usr/bin/env python3
"""Build playlist text files from a song list and assignment JSON."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from datetime import datetime
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
    parser.add_argument('--max-chars-per-file', type=int, help='Split playlist txt files so each file stays within this character limit when possible.')
    parser.add_argument('--html-report', action='store_true', help='Also write an offline visual HTML report.')
    parser.add_argument('--summary-json', action='store_true', help='Also write summary.json with report data.')
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


def playlist_text(songs: list[str]) -> str:
    return '\n'.join(songs) + ('\n' if songs else '')


def write_playlist(path: Path, songs: list[str]) -> None:
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(playlist_text(songs))


def split_playlist_songs(songs: list[str], max_chars: int) -> list[list[str]]:
    if max_chars <= 0:
        raise ValueError('--max-chars-per-file 必须大于 0。')

    chunks: list[list[str]] = []
    current: list[str] = []
    for song in songs:
        candidate = current + [song]
        if current and len(playlist_text(candidate)) > max_chars:
            chunks.append(current)
            current = [song]
        else:
            current = candidate
    if current or not chunks:
        chunks.append(current)
    return chunks


def unique_filename(filename: str, used_filenames: set[str]) -> str:
    if filename not in used_filenames:
        used_filenames.add(filename)
        return filename

    path = Path(filename)
    counter = 2
    while True:
        candidate = f'{path.stem}_{counter}{path.suffix}'
        if candidate not in used_filenames:
            used_filenames.add(candidate)
            return candidate
        counter += 1


def write_playlist_files(
    output_dir: Path,
    playlist_name: str,
    songs: list[str],
    max_chars: int | None,
    used_filenames: set[str],
) -> list[tuple[str, list[str]]]:
    base_name = sanitize_filename(playlist_name)
    chunks = [songs] if max_chars is None else split_playlist_songs(songs, max_chars)
    if len(chunks) == 1:
        filename = unique_filename(base_name + '.txt', used_filenames)
        write_playlist(output_dir / filename, chunks[0])
        return [(filename, chunks[0])]

    written: list[tuple[str, list[str]]] = []
    for index, chunk in enumerate(chunks, start=1):
        filename = unique_filename(f'{base_name}_part{index:02d}.txt', used_filenames)
        write_playlist(output_dir / filename, chunk)
        written.append((filename, chunk))
    return written


def build_summary(
    *,
    input_path: Path,
    songs: list[str],
    covered_indexes: set[int],
    playlist_details: list[dict[str, Any]],
    uncovered: list[tuple[int, str]],
    uncertain_entries: list[str],
    require_coverage: bool,
    allow_repeats: bool,
    status: str,
) -> dict[str, Any]:
    return {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'source_path': str(input_path),
        'source_count': len(songs),
        'covered_count': len(covered_indexes),
        'coverage_required': require_coverage,
        'allow_repeats': allow_repeats,
        'status': status,
        'playlists': playlist_details,
        'uncovered': [{'index': index, 'song': song} for index, song in uncovered],
        'uncertain': uncertain_entries,
    }


def write_summary_json(path: Path, summary: dict[str, Any]) -> None:
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_html_report(path: Path, summary: dict[str, Any]) -> None:
    playlists = sorted(summary['playlists'], key=lambda item: item['count'], reverse=True)
    max_count = max((item['count'] for item in playlists), default=1)
    coverage_rate = 0 if summary['source_count'] == 0 else summary['covered_count'] / summary['source_count'] * 100

    rows: list[str] = []
    details: list[str] = []
    for item in playlists:
        width = 0 if max_count == 0 else item['count'] / max_count * 100
        name = html.escape(item['name'])
        filename = html.escape(item['filename'])
        rows.append(
            f'<div class="bar-row"><div class="bar-label">{name}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width: {width:.1f}%"></div></div>'
            f'<div class="bar-count">{item["count"]}</div></div>'
        )
        song_items = ''.join(f'<li>{html.escape(song)}</li>' for song in item.get('songs', item.get('preview', [])))
        if not song_items:
            song_items = '<li class="muted">无歌曲</li>'
        details.append(
            f'<details class="playlist" open><summary><span>{name}</span>'
            f'<strong>{item["count"]} 首</strong></summary>'
            f'<p class="muted">{filename} · 完整列表，可在卡片内滚动</p>'
            f'<ol class="song-list">{song_items}</ol></details>'
        )

    uncovered = ''.join(
        f'<li>{entry["index"]}. {html.escape(entry["song"])}</li>'
        for entry in summary['uncovered'][:200]
    ) or '<li class="muted">无</li>'
    uncertain = ''.join(f'<li>{html.escape(song)}</li>' for song in summary['uncertain']) or '<li class="muted">无</li>'

    document = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>歌单生成报告</title>
<style>
:root {{ color-scheme: light; --bg: #efede8; --canvas: #f8f6f1; --surface: rgba(255, 254, 250, .86); --ink: #24221f; --muted: #7a756c; --line: rgba(60, 54, 46, .13); --line-strong: rgba(60, 54, 46, .22); --accent: #9a8a68; --accent-ink: #5c513c; --ok: #49624d; --warn: #8c5b43; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 48px 24px; background: linear-gradient(180deg, #f5f3ee 0%, var(--bg) 100%); color: var(--ink); font-family: "SF Pro Text", Inter, "Segoe UI", "Microsoft YaHei", sans-serif; }}
main {{ max-width: 1120px; margin: 0 auto; padding: 38px; background: var(--canvas); border: 1px solid var(--line); border-radius: 28px; box-shadow: 0 24px 70px rgba(42, 35, 27, .08); }}
h1 {{ margin: 0 0 12px; max-width: 720px; font-size: clamp(34px, 5vw, 58px); line-height: 1.02; font-weight: 720; letter-spacing: -0.055em; }}
h2 {{ margin: 42px 0 18px; font-size: 22px; font-weight: 680; letter-spacing: -0.03em; }}
h3 {{ letter-spacing: -0.02em; }}
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(172px, 1fr)); gap: 12px; margin: 30px 0; }}
.card, .panel, .playlist, .issue-card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(42, 35, 27, .045); }}
.metric {{ margin-top: 10px; font-size: 34px; line-height: 1; font-weight: 720; letter-spacing: -0.045em; font-variant-numeric: tabular-nums; }}
.label, .muted {{ color: var(--muted); }}
.label {{ font-size: 12px; font-weight: 650; letter-spacing: .08em; text-transform: uppercase; }}
.status-ok {{ color: var(--ok); }}
.status-warn {{ color: var(--warn); }}
.panel {{ padding: 22px; }}
.bar-row {{ display: grid; grid-template-columns: minmax(170px, 270px) minmax(0, 1fr) 58px; align-items: center; gap: 14px; padding: 11px 0; border-bottom: 1px solid var(--line); }}
.bar-row:last-child {{ border-bottom: 0; }}
.bar-label, .playlist, .issue-card, li, code {{ min-width: 0; overflow-wrap: anywhere; word-break: break-word; }}
.bar-label {{ font-weight: 600; color: #35312c; }}
.bar-track {{ height: 7px; background: #e5e0d6; border-radius: 999px; overflow: hidden; }}
.bar-fill {{ height: 100%; background: var(--accent); border-radius: 999px; }}
.bar-count {{ text-align: right; color: var(--accent-ink); font-weight: 680; font-variant-numeric: tabular-nums; }}
.playlists {{ display: grid; grid-template-columns: 1fr; gap: 12px; }}
.playlist {{ padding: 0; overflow: hidden; }}
.playlist summary {{ display: flex; align-items: center; justify-content: space-between; gap: 18px; padding: 18px 20px; cursor: pointer; list-style: none; }}
.playlist summary::-webkit-details-marker {{ display: none; }}
.playlist summary span {{ font-size: 18px; font-weight: 650; letter-spacing: -0.02em; }}
.playlist summary strong {{ flex: none; color: var(--accent-ink); font-size: 14px; font-weight: 650; }}
.playlist summary::after {{ content: '展开'; flex: none; color: var(--muted); font-size: 12px; letter-spacing: .08em; }}
.playlist[open] summary::after {{ content: '收起'; }}
.playlist > p {{ margin: 0; padding: 0 20px 14px; }}
.playlist h3, .issue-card h3 {{ margin: 0; font-size: 18px; font-weight: 650; }}
.song-list {{ max-height: 420px; overflow: auto; margin: 0; padding: 4px 28px 18px 42px; scrollbar-gutter: stable; }}
.song-list li {{ line-height: 1.58; padding: 5px 0; border-bottom: 1px solid rgba(60, 54, 46, .08); }}
.song-list li:last-child {{ border-bottom: 0; }}
.song-list::-webkit-scrollbar {{ width: 8px; }}
.song-list::-webkit-scrollbar-track {{ background: transparent; }}
.song-list::-webkit-scrollbar-thumb {{ background: rgba(92, 81, 60, .26); border-radius: 999px; }}
.checks-panel {{ margin-top: 28px; }}
.issue-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 12px; margin-top: 14px; }}
.issue-card ol {{ margin-bottom: 0; }}
.note {{ margin-top: 16px; }}
ol {{ padding-left: 22px; }}
li {{ margin: 0; }}
code {{ display: inline-block; max-width: 100%; background: rgba(255,255,255,.48); color: var(--accent-ink); padding: 2px 7px; border: 1px solid var(--line); border-radius: 999px; vertical-align: bottom; font-family: "Cascadia Code", Consolas, monospace; font-size: .9em; }}
@media (max-width: 720px) {{ body {{ padding: 18px 12px; }} main {{ padding: 22px 14px; border-radius: 20px; }} .bar-row {{ grid-template-columns: 1fr; gap: 8px; }} .bar-count {{ text-align: left; }} .playlist summary {{ align-items: flex-start; flex-direction: column; }} }}
</style>
</head>
<body>
<main>
<h1>歌单生成报告</h1>
<p class="muted">生成时间：{html.escape(summary['generated_at'])} · 来源：<code>{html.escape(summary['source_path'])}</code></p>
<div class="card-grid">
  <div class="card"><div class="label">状态</div><div class="metric {'status-ok' if summary['status'] == '通过' else 'status-warn'}">{html.escape(summary['status'])}</div></div>
  <div class="card"><div class="label">源歌曲数</div><div class="metric">{summary['source_count']}</div></div>
  <div class="card"><div class="label">已覆盖</div><div class="metric">{summary['covered_count']}</div></div>
  <div class="card"><div class="label">覆盖率</div><div class="metric">{coverage_rate:.1f}%</div></div>
  <div class="card"><div class="label">歌单数</div><div class="metric">{len(playlists)}</div></div>
  <div class="card"><div class="label">待整理</div><div class="metric">{len(summary['uncertain'])}</div></div>
</div>
<section class="panel">
<h2>歌单规模</h2>
{''.join(rows)}
</section>
<h2>歌单预览</h2>
<div class="playlists">{''.join(details)}</div>
<section class="panel checks-panel">
<h2>检查项</h2>
<div class="issue-grid">
  <section class="issue-card">
    <h3>未覆盖歌曲</h3>
    <ol>{uncovered}</ol>
  </section>
  <section class="issue-card">
    <h3>待整理歌曲</h3>
    <ol>{uncertain}</ol>
  </section>
</div>
<p class="muted note">说明：HTML 报告用于快速查看规模和覆盖情况；完整歌单仍以同目录下的 txt 文件为准。</p>
</section>
</main>
</body>
</html>
'''
    path.write_text(document, encoding='utf-8')


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
    playlist_details: list[dict[str, Any]] = []
    generated_files: list[str] = []
    used_filenames: set[str] = set()

    for playlist_name, raw_items in assignments.items():
        if not isinstance(raw_items, list):
            raise ValueError(f'歌单 {playlist_name} 的值必须是数组。')

        resolved_songs: list[str] = []
        for item in raw_items:
            index, song = resolve_item(item, songs)
            resolved_songs.append(song)
            if index is not None:
                covered_indexes.add(index)

        written_files = write_playlist_files(output_dir, str(playlist_name), resolved_songs, args.max_chars_per_file, used_filenames)
        for filename, file_songs in written_files:
            playlist_counts[filename] = len(file_songs)
            playlist_details.append({
                'name': str(playlist_name),
                'filename': filename,
                'count': len(file_songs),
                'preview': file_songs[:10],
                'songs': file_songs,
            })
            generated_files.append(filename)

    uncertain_entries: list[str] = []
    if args.uncertain:
        raw_uncertain = load_json(Path(args.uncertain))
        if not isinstance(raw_uncertain, list):
            raise ValueError('uncertain JSON 必须是数组。')
        for item in raw_uncertain:
            _, song = resolve_item(item, songs)
            uncertain_entries.append(song)
        written_files = write_playlist_files(output_dir, '待整理', uncertain_entries, args.max_chars_per_file, used_filenames)
        for filename, file_songs in written_files:
            playlist_details.append({
                'name': '待整理',
                'filename': filename,
                'count': len(file_songs),
                'preview': file_songs[:10],
                'songs': file_songs,
            })
            generated_files.append(filename)

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
        f'单文件字符上限：{args.max_chars_per_file if args.max_chars_per_file else "未限制"}',
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

    summary = build_summary(
        input_path=input_path,
        songs=songs,
        covered_indexes=covered_indexes,
        playlist_details=playlist_details,
        uncovered=uncovered,
        uncertain_entries=uncertain_entries,
        require_coverage=args.require_coverage,
        allow_repeats=args.allow_repeats,
        status=status,
    )
    if args.summary_json:
        write_summary_json(output_dir / 'summary.json', summary)
    if args.html_report:
        write_html_report(output_dir / '生成报告.html', summary)

    print(report)
    return 1 if args.require_coverage and uncovered else 0


if __name__ == '__main__':
    raise SystemExit(main())
