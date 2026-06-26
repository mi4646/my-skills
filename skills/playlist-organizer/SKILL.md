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
- Playlist links from NetEase Cloud Music, QQ Music, Spotify, or similar services, when paired with an external link-to-text extractor.

Outputs can be:
- One `.txt` per playlist, each line as `Song - Artist`.
- Import-ready plain text for tools such as TuneMyMusic or Spotlistr.
- A report file showing source count, covered count, playlist sizes, duplicates allowed/not allowed, and uncertain items.

## First: interview before generating

Before reading large files or writing outputs, ask only the missing questions. Reuse answers already present in the conversation.

Clarify these points:
1. **Input source**: local file, copied text, or playlist link.
2. **If the input is a link**: ask whether the user wants to use an external extractor such as GoMusic first. Do not log in to music accounts or scrape authenticated pages unless the user explicitly authorizes a safe method.
3. **Playlist categories**: ask the user to define or approve categories. Do not force fixed categories. You may suggest examples such as focus, commute, workout, night, emotional release, Chinese style, foreign-language, KTV, nostalgia, but treat them as optional.
4. **Coverage rule**: ask whether every song must appear in at least one playlist.
5. **Repeat rule**: ask whether the same song may appear in multiple playlists.
6. **Uncertain items**: ask whether to batch-question the user, create `待整理.txt`, or assign to the closest category.
7. **Output location and format**: ask for output directory, file naming, whether to include a report, and whether import-ready text is needed.

For large collections, avoid asking per-song questions one by one. First classify the obvious items, then batch uncertain items into a short list for user review.

## Link input and GoMusic-style workflow

If the user provides a playlist link rather than a local song list:

1. Identify the source if possible: NetEase Cloud Music, QQ Music, Spotify, or unknown.
2. Explain that this skill's deterministic script works on song lists, not directly on platform accounts.
3. Offer a link-to-text step:
   - If the user already has a GoMusic-style extractor available, ask them to run it and provide the resulting txt/csv.
   - If they want help using GoMusic, explain the high-level flow: paste playlist link into GoMusic, copy/export the resulting song list, then feed that list into this skill.
4. Continue with local-list parsing after the extracted list is available.

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
  --import-ready
```

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

## Quality checks before saying done

Before final response:
1. Read or display the generated report.
2. Confirm source count and covered count.
3. Confirm output directory and filenames.
4. State any limitations, especially uncertain classifications or link extraction steps the user still needs to perform.

If tests or generation fail, report the actual error and fix it before claiming completion.
