# Task 5: TestKeywordMatching + TestCategoryFallback

## Summary

Added two test classes to `test_assign_icons.py` to cover keyword matching and category fallback logic introduced in Tasks 1-4.

## Changes

- **`test_assign_icons.py`**: Updated import to include `KEYWORD_ICONS`, `ICON_TO_CATEGORY`, `ALL_ICONS`, `_match_keyword`, `ICON_CATEGORIES`.
- **`TestKeywordMatching`** (7 tests): Validates `_match_keyword` behavior — short keyword word-boundary matching, long keyword substring matching, case insensitivity, and false-positive avoidance.
- **`TestCategoryFallback`** (4 tests): Validates fallback chain in `assign_directory_icons` and `assign_file_icons` — same-category fallback when matched icon is taken, global pool fallback when category is exhausted.

## Verification

- 15/15 tests pass (8 original + 7 keyword matching + 4 category fallback)
- All existing tests continue to pass with no regressions
