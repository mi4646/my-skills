---
name: playlist-organizer
description: Use this skill whenever the user wants to turn music collections, liked-song exports, playlist links, local txt/csv song lists, or copied music-app track lists into organized playlists. This includes scene-based playlists, custom categories, import-ready txt files, coverage reports, and optional GoMusic-assisted link-to-song-list workflows. Trigger even if the user only says they have a NetEase Cloud Music, QQ Music, Spotify, or local song list and wants it “sorted,” “classified,” “split into playlists,” “made into workout/focus/night playlists,” or “organized for import.”
---

# Playlist Organizer

Use this skill to help the user convert a music collection into useful playlists. The core job is not just file splitting; it is a guided curation workflow: understand how the user actually wants to listen, normalize the song list, classify tracks, generate import-friendly files, and verify coverage.

## What this skill supports

Inputs can be:
- Local `.txt` files with lines like `1 Song - Artist` or `Song - Artist`.
- Local `.csv` files with common columns such as `title`, `track`, `name`, `artist`, `artists`, `歌曲名`, `歌名`, `歌手`.
- Copied text from music apps or migration tools.
- Playlist links from NetEase Cloud Music, QQ Music, Spotify, or similar services, using the bundled GoMusic API extractor when the user authorizes link extraction.

Outputs can be:
- One `.txt` per playlist, each line as `Song - Artist`.
- Import-ready plain text for tools such as TuneMyMusic or Spotlistr.
- A text report showing source count, covered count, playlist sizes, duplicates allowed/not allowed, and uncertain items.
- Optional offline visual HTML report and `summary.json` for easier review of large playlist splits.

## First: interview before generating

Before reading large files or writing outputs, ask only the missing questions. Reuse answers already present in the conversation.

Clarify these points:
1. **Input source**: local file, copied text, or playlist link.
2. **If the input is a link**: ask whether the user authorizes using the bundled GoMusic API extractor. Do not log in to music accounts or scrape authenticated pages unless the user explicitly authorizes a safe method.
3. **Playlist categories**: ask the user to define or approve categories. Do not force fixed categories. You may suggest examples such as focus, commute, workout, night, emotional release, Chinese style, foreign-language, KTV, nostalgia, but treat them as optional.
4. **Coverage rule**: ask whether every song must appear in at least one playlist.
5. **Repeat rule**: ask whether the same song may appear in multiple playlists.
6. **Uncertain items**: ask whether to batch-question the user, create `待整理.txt`, or assign to the closest category.
7. **Output location and format**: ask for output directory, file naming, whether to include text report, offline HTML visual report, `summary.json`, and whether import-ready text is needed.

For large collections, avoid asking per-song questions one by one. First classify the obvious items, then batch uncertain items into a short list for user review.

## Link input and GoMusic API workflow

If the user provides a playlist link rather than a local song list:

1. Identify the source if possible: NetEase Cloud Music, QQ Music, Spotify, or unknown.
2. Ask whether the user authorizes sending the playlist URL to the configured GoMusic API. Treat this as an external network call because the URL is sent to a third-party service.
3. If authorized, use `scripts/fetch_gomusic_songlist.py` to extract the link into a local `.txt` song list before classification:

```bash
python <skill-dir>/scripts/fetch_gomusic_songlist.py \
  --url <playlist-url> \
  --output <song-list.txt>
```

The script calls:
- Endpoint: `https://sss.unmeta.cn/songlist?detailed=false&format=song-singer&order=normal`
- Method: `POST`
- Form field: `url=<playlist-url>`

4. If the API call fails, returns an empty list, or the user does not authorize the network call, fall back to asking the user to run GoMusic or another extractor and provide the resulting txt/csv.
5. Continue with local-list parsing after the extracted list is available.

Keep the boundary clear: GoMusic-style tools extract links into song lists; this skill organizes the song list into playlists.

## Classification approach

Use the user's category definitions as the source of truth. Prefer quality over cleverness.

Recommended process:
1. Parse the source list into canonical `Song - Artist` entries.
2. Preserve original order unless the user asks for sorting.
3. Classify obvious songs using title, artist, language, known genre, emotional tone, and user-provided category descriptions.
4. Mark ambiguous songs instead of silently guessing when the user requested confirmation.
5. If full coverage is required, ensure every source entry appears in at least one playlist before finishing.
6. If repeats are allowed, duplicate songs across playlists when they genuinely fit multiple listening contexts.
7. If repeats are not allowed, choose the best single category and explain tie-breaks in the report.

Do not invent metadata you cannot support. If a classification depends on uncertain knowledge, say so and ask or place it in the uncertainty flow.

## Use the bundled script for deterministic file generation

After classification decisions are ready, use `scripts/build_playlists.py` to parse input, write playlist txt files, and generate the report.

Typical command:

```bash
python <skill-dir>/scripts/build_playlists.py \
  --input <song-list.txt-or-csv> \
  --output-dir <output-folder> \
  --assignments <assignments.json> \
  --allow-repeats \
  --require-coverage \
  --import-ready \
  --html-report \
  --summary-json
```

For QQ Music import, add `--max-chars-per-file 1000`. QQ Music limits the text pasted in one import operation, so split by character count rather than by a fixed number of songs. The script keeps each song line intact and writes files such as `通勤_part01.txt`, `通勤_part02.txt` when a playlist exceeds the limit.

`assignments.json` maps playlist names to songs. Values may be 1-based source indexes or exact canonical song strings:

```json
{
  "专注工作": [1, 2, "Example Song - Example Artist"],
  "夜晚放松": [3, 4]
}
```

The script writes:
- `<playlist-name>.txt` for each playlist.
- `生成报告.txt` with counts and verification notes.
- `生成报告.html` when `--html-report` is passed. This is an offline visual report with summary cards, playlist size bars, and complete per-playlist song lists inside scrollable cards.
- `summary.json` when `--summary-json` is passed. This includes playlist counts, short previews, and complete song lists for later automation or deeper analysis.
- `待整理.txt` if uncertain items are provided.

If you need to pass uncertain items, create an optional JSON file like:

```json
[1, "Example Song - Example Artist"]
```

and pass it with `--uncertain <uncertain.json>`.

## Output conventions

Default output style:
- Do not include original numbering in playlist files unless requested.
- Use one song per line: `Song - Artist`.
- For QQ Music import, keep each txt file within 1000 characters when possible by using `--max-chars-per-file 1000`. Split only between song lines; never truncate a song line.
- Keep duplicate source rows if the source contains duplicates; this preserves what the user exported.
- Sanitize playlist filenames only enough to be valid on Windows/macOS/Linux; keep Chinese names intact.

Report should include:
- Source path.
- Source entry count.
- Covered source entry count.
- Whether coverage was required.
- Whether repeats were allowed.
- Count per playlist.
- Uncovered entries, if any.
- Uncertain entries, if any.

When the collection is large or the user wants easier review, prefer passing `--html-report --summary-json` in addition to the text report. Keep `生成报告.txt` as the stable baseline; treat HTML and JSON as additive outputs, not replacements.

## Quality checks before saying done

Before final response:
1. Read or display the generated report.
2. Confirm source count and covered count.
3. Confirm output directory and filenames.
4. State any limitations, especially uncertain classifications or link extraction steps the user still needs to perform.

If tests or generation fail, report the actual error and fix it before claiming completion.
