# Task 4: `assign_file_icons` — 语义匹配 + 分类回退 + 日志

## Summary

Replaced the `assign_file_icons` method with a semantic-matching first approach, sharing `used_icons` with `assign_directory_icons` to guarantee cross-group icon uniqueness.

## Changes

- **`assign_file_icons`**: signature changed from `(files, skip_existing)` to `(files, used_icons, skip_existing)`. New behavior:
  1. Filename keyword matching via `_match_keyword` + `KEYWORD_ICONS`
  2. If matched icon is taken, fall back within the same category (`ICON_TO_CATEGORY`)
  3. If same category exhausted, fall back to any unused icon from `ALL_ICONS`
  4. If all icons exhausted, least-used fallback (SHA256-based deterministic, not `hash()`)
  5. No keyword match -> SHA256-based scanning with least-used fallback
- **`run()`**: now creates a shared `used_icons` set passed to both `assign_directory_icons` and `assign_file_icons`

## Fixes

- Replaced `hash(file_path)` with `int.from_bytes(hashlib.sha256(...).digest()[:4], 'big')` for cross-process determinism (known issue from brief)

## Verification

- Quick validation: `_match_keyword`, `ICON_TO_CATEGORY`, full pipeline all pass
- Existing tests: 4/4 pass (no regressions)
