---
name: playlist-organizer
description: 当用户有一份音乐收藏、喜欢列表导出、歌单分享链接、本地 txt/csv 歌曲列表或从音乐 App 复制的曲目清单，想把它排序、分类、拆分成多个歌单或整理以便导入时使用。触发词包括"整理歌单""分类""拆分成歌单""做成运动/专注/夜晚歌单""排序""导入"，以及提到网易云、QQ音乐、Spotify 或本地歌曲列表时。
version: v1.0.0
---

# Playlist Organizer

核心原则：把一份歌曲列表整理成有用的歌单——先问清用户怎么听、保留源列表原样不过滤、按用户分类归类、生成导入友好的文件并核对覆盖。整理是策展，不是清洗：用户的曲目一首都不该被你擅自删掉或合并。

## When to use / When NOT to use

适用：用户有一份歌曲清单（文件/链接/复制文本），想分类、拆分、整理成多个歌单或导入用文本。
不适用：只想给单首歌曲找歌词/和弦/下载链接；只想给已分好的歌单改顺序或重命名；只想把一份歌单原样迁移到另一平台不做分类（直接用迁移工具即可）。

## 支持的输入与输出

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
5. **Repeat rule**: ask whether the same song may appear in multiple playlists. "重复" here means one song appearing across multiple playlists — it never means de-duplicating rows inside the source. Source rows are always preserved; see 去重与过滤原则.
6. **Uncertain items**: ask whether to batch-question the user, create `待整理.txt`, or assign to the closest category.
7. **Output location and format**: ask for output directory, file naming, whether to include text report, offline HTML visual report, `summary.json`, and whether import-ready text is needed.

For large collections, avoid asking per-song questions one by one. First classify the obvious items, then batch uncertain items into a short list for user review.

### "别问那么多"不等于跳过关键确认

用户说"快点弄完""别问那么多""直接帮我分好"时，压力只作用于"逐首问""来回拉扯"这类低风险偏好确认，**不**授权你单方面替用户拍板以下三项：分类方案、覆盖规则、重复规则。这三项决定结果走向，必须让用户拍板或明确接受默认——可一次性合并成一轮提问，但不能默默假设。

- ✅ 可以跳过：逐首确认、桶名微调、年代边界等低风险偏好。
- ❌ 不可跳过：用什么分类、是否要求全覆盖、是否允许跨歌单重复、是否去重源行。
- "先 ship 默认再让用户纠偏"在此不适用——分类/覆盖/重复选错会让整批歌单返工，比一轮提问更费时。

如确需用默认值，必须在产出前**显式声明**所采用的默认（"我将默认：8分类、全覆盖、允许跨歌单重复、保留重复行"），给用户一次否决机会，而非先斩后奏。声明默认时，源行的默认必须是"保留重复行、不去重"——不得把"去重"作为默认值提出，去重只在用户明确要求时做（见去重与过滤原则）。

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
- Endpoint: `http://114.132.198.202:18081/api/playlist` (cloud deployment of the QQMusic export project)
- Method: `POST`
- JSON body: `{"url": "<playlist-url>", "detailed": false, "format": "song-singer", "order": "normal"}`
- Response: `{"name": "...", "songs": ["歌名 - 歌手", ...], "songs_count": N, "total_count": N}`

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

Do not invent metadata you cannot support. If a classification depends on uncertain knowledge, say so and ask or place it in the uncertainty flow. 用户要求"全部归类、不准遗留"不构成强行猜测的授权——对不确定的歌曲，宁可放入`待整理`或批量问用户，也不要用排除法硬塞并伪装成确知。落点可以被迫给出，但置信度必须如实标注，且优先走待整理流程。

## 去重与过滤原则（不可妥协）

源歌单里的每一行都原样保留，绝不主动去重、合并或过滤。判断"是否同一首歌"的唯一依据是完整的「歌名 - 歌手」字符串是否完全一致。

1. **完全重复行保留**：同一首「歌名 - 歌手」在源里出现多次，就保留多次。每一行都是独立的源条目，独立计数、独立覆盖。生成歌单时按需出现，不删减。
2. **同名不同歌手 = 不同的歌**：歌名相同但歌手/版本不同的条目（如《单车》陈奕迅 / 庄心妍 / 一杯陈豆浆，《赤伶》HITA / 执素兮 / 谭晶）是不同的录音，绝不是重复。绝不按歌名合并、去重或互相替换；分类时各自独立判断。
3. **不基于歌名去重**：仅歌名相同不能判定为同一首歌。只有「歌名 - 歌手」整行完全相同才算重复，且即便完全相同也默认保留。
4. **辅助报告措辞**：若为帮助用户审阅而生成分组/重复类辅助文件，必须把"完全重复行"与"同名不同歌手"分成两类单独列出，并在文件顶部明确声明：后者不是重复、默认不过滤、仅作参考。绝不在辅助报告里建议或执行过滤，也不要把同名异版本描述为"需要清理"。

唯一例外：用户明确说"帮我去掉重复"时，才可对完全重复行去重；同名不同歌手即便此时也只提示、不自动合并。

### 合理化借口反驳表（基线测试实测）

| 借口 | 现实 |
|------|------|
| "用户说弄干净点/挑一个版本就行，所以删翻唱" | "弄干净"指整理结构，不是删歌。删歌需用户逐首明确授权，随口一句不算授权。 |
| "保留原唱/最权威版本，客观可复现" | 客观≠可以删。翻唱是独立录音、用户曲目，"权威"是你的主观判断，不能据此替用户删歌。 |
| "同名多版本挑一个，保留原唱" | 同名不同歌手是不同的歌，绝不能挑版本、不能删。全部保留，各自独立分类。 |
| "完全重复行留一条就行，去重更整洁" | 重复行也是用户导出的原始数据，默认全部保留。去重只在用户明确要求时做。 |
| "源歌单有 977 行但用户说 1008，差的不用管" | 缺口要如实告知用户，不能默默接受不完整数据当最终结果。 |
| "用户嫌歌单乱，合并同名更省事" | 省事不能以丢歌为代价。保真优先于整洁。 |

### 红旗清单 — 出现这些念头就停，按原则重来

- "同名的那几首挑一个版本就行" → 停。同名不同歌手是不同的歌，全留。
- "原唱最权威，删掉翻唱" → 停。无权替用户删翻唱。
- "重复行去重更干净" → 停。默认保留重复行。
- "用户说快点弄完，跳过确认直接删" → 停。速度压力不改变保留规则。
- "把同名异版本写进报告当'需清理'" → 停。它们不是重复，不是需清理项。

**违背规则的文字也是违背规则的精神。** 速度压力、整洁偏好、"客观"包装，都不是删歌/合并的授权。

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
- Keep duplicate source rows if the source contains duplicates; this preserves what the user exported. Same-name different-artist rows are different songs and must never be merged or filtered (see 去重与过滤原则 above).
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
version: v1.0.0
