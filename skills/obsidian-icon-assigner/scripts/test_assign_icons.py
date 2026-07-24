"""
Tests for obsidian-icon-assigner: directory color inheritance.

Core rule: a new subdirectory should inherit the color of its closest
parent directory that already has a color in the Iconic config.
Only when NO parent has a color should a hash-based HSL color be generated.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from assign_icons import IconAssigner, KEYWORD_ICONS, ICON_TO_CATEGORY, ALL_ICONS, _match_keyword, ICON_CATEGORIES


class TestDirectoryColorInheritance(unittest.TestCase):
    def create_vault(self):
        temp_dir = tempfile.TemporaryDirectory()
        vault = Path(temp_dir.name)

        iconic_dir = vault / ".obsidian" / "plugins" / "iconic"
        iconic_dir.mkdir(parents=True)

        config = {
            "fileIcons": {
                "AI": {
                    "icon": "lucide-bot",
                    "color": "#9333ea"
                },
                "AI/ClaudeCode": {
                    "icon": "lucide-terminal",
                    "color": "#a855f7"
                }
            },
            "bookmarkIcons": {},
            "propertyIcons": {}
        }
        (iconic_dir / "data.json").write_text(
            json.dumps(config, ensure_ascii=False),
            encoding="utf-8"
        )

        (vault / "AI" / "ClaudeCode").mkdir(parents=True)
        (vault / "AI" / "ClaudeCode" / "note.md").write_text("# Note", encoding="utf-8")

        (vault / "AI" / "agent-learning-docs").mkdir(parents=True)
        (vault / "AI" / "agent-learning-docs" / "guide.md").write_text("# Guide", encoding="utf-8")

        return temp_dir, vault

    def test_new_subdir_inherits_parent_color(self):
        temp_dir, vault = self.create_vault()
        self.addCleanup(temp_dir.cleanup)

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        files = assigner.scan_markdown_files()
        directories = assigner.get_directories(files)
        colors = assigner.assign_directory_colors(directories)

        self.assertEqual(colors["AI/agent-learning-docs"], "#9333ea")

    def test_new_subdir_inherits_closest_parent_color(self):
        temp_dir, vault = self.create_vault()
        self.addCleanup(temp_dir.cleanup)

        subdir = vault / "AI" / "ClaudeCode" / "sub"
        subdir.mkdir(parents=True)
        (subdir / "doc.md").write_text("# Doc", encoding="utf-8")

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        files = assigner.scan_markdown_files()
        directories = assigner.get_directories(files)
        colors = assigner.assign_directory_colors(directories)

        self.assertEqual(colors["AI/ClaudeCode/sub"], "#a855f7")

    def test_existing_dir_color_preserved(self):
        temp_dir, vault = self.create_vault()
        self.addCleanup(temp_dir.cleanup)

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        files = assigner.scan_markdown_files()
        directories = assigner.get_directories(files)
        colors = assigner.assign_directory_colors(directories)

        self.assertEqual(colors["AI"], "#9333ea")
        self.assertEqual(colors["AI/ClaudeCode"], "#a855f7")

    def test_no_parent_color_generates_hash(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        vault = Path(temp_dir.name)

        iconic_dir = vault / ".obsidian" / "plugins" / "iconic"
        iconic_dir.mkdir(parents=True)
        config = {"fileIcons": {}, "bookmarkIcons": {}, "propertyIcons": {}}
        (iconic_dir / "data.json").write_text(
            json.dumps(config, ensure_ascii=False),
            encoding="utf-8"
        )

        (vault / "孤立目录").mkdir(parents=True)
        (vault / "孤立目录" / "note.md").write_text("# Note", encoding="utf-8")

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        files = assigner.scan_markdown_files()
        directories = assigner.get_directories(files)
        colors = assigner.assign_directory_colors(directories)

        self.assertTrue(colors["孤立目录"].startswith("hsl("), colors["孤立目录"])


class TestKeywordMatching(unittest.TestCase):
    """Tests for _match_keyword function with short/long keyword semantics"""

    def test_short_keyword_matches_with_word_boundary(self):
        self.assertTrue(_match_keyword("AI/Notes", "AI"))

    def test_short_keyword_no_match_without_boundary(self):
        self.assertFalse(_match_keyword("MAIL", "AI"))

    def test_short_keyword_matches_with_hyphen_boundary(self):
        self.assertTrue(_match_keyword("use-k8s-cluster", "k8s"))

    def test_long_keyword_substring_match(self):
        self.assertTrue(_match_keyword("docker-compose.yml", "docker"))

    def test_long_keyword_no_match(self):
        self.assertFalse(_match_keyword("dockyard", "docker"))

    def test_case_insensitive_match(self):
        self.assertTrue(_match_keyword("Python", "python"))

    def test_short_keyword_inside_word_no_match(self):
        self.assertFalse(_match_keyword("TRAIN", "AI"))


class TestCategoryFallback(unittest.TestCase):
    """Tests for category-preferential icon fallback in assign_directory_icons and assign_file_icons"""

    def _create_minimal_vault(self):
        temp_dir = tempfile.TemporaryDirectory()
        vault = Path(temp_dir.name)
        iconic_dir = vault / ".obsidian" / "plugins" / "iconic"
        iconic_dir.mkdir(parents=True)
        config = {"fileIcons": {}, "bookmarkIcons": {}, "propertyIcons": {}}
        (iconic_dir / "data.json").write_text(json.dumps(config), encoding="utf-8")
        return temp_dir, vault

    # --- assign_directory_icons fallback ---

    def test_dir_fallback_within_same_category(self):
        """When keyword-matched icon is taken, fallback chooses from same category"""
        temp_dir, vault = self._create_minimal_vault()
        self.addCleanup(temp_dir.cleanup)

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        # "AI" -> KEYWORD_ICONS -> "lucide-brain" (education category, index 4)
        # lucide-brain taken -> first fallback = lucide-target (index 5)
        used_icons = {"lucide-brain"}
        result = assigner.assign_directory_icons({"AI"}, used_icons, skip_existing=False)

        self.assertEqual(result["AI"], "lucide-target")
        self.assertIn("lucide-target", used_icons)

    def test_dir_fallback_to_global_when_category_exhausted(self):
        """When entire matched category is used, fallback goes to global icon pool"""
        temp_dir, vault = self._create_minimal_vault()
        self.addCleanup(temp_dir.cleanup)

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        # Fill used_icons with all education icons so category is exhausted
        used_icons = set(ICON_CATEGORIES["education"])
        result = assigner.assign_directory_icons({"AI"}, used_icons, skip_existing=False)

        chosen_cat = ICON_TO_CATEGORY.get(result["AI"])
        self.assertIsNotNone(chosen_cat, f"Result icon {result['AI']} has no category mapping")
        self.assertNotEqual(chosen_cat, "education")

    # --- assign_file_icons fallback ---

    def test_file_fallback_within_same_category(self):
        """File keyword-matched icon taken -> fallback within same category"""
        temp_dir, vault = self._create_minimal_vault()
        self.addCleanup(temp_dir.cleanup)

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        used_icons = {"lucide-brain"}
        result = assigner.assign_file_icons(["AI/Claude.md"], used_icons, skip_existing=False)

        self.assertNotEqual(result["AI/Claude.md"], "lucide-brain")

    def test_file_fallback_to_global_when_category_exhausted(self):
        """File keyword-matched category exhausted -> fallback to global pool"""
        temp_dir, vault = self._create_minimal_vault()
        self.addCleanup(temp_dir.cleanup)

        assigner = IconAssigner(str(vault))
        assigner.load_config()

        # "claude" -> KEYWORD_ICONS -> "lucide-sparkles" (no category mapping)
        # We need "AI" keyword match for category testing: file must contain "AI"
        used_icons = set(ICON_CATEGORIES["education"])
        result = assigner.assign_file_icons(["AI.md"], used_icons, skip_existing=False)

        chosen_cat = ICON_TO_CATEGORY.get(result["AI.md"])
        # Icon should not be in education category (or might be if global pool has no choice)
        self.assertNotEqual(chosen_cat, "education",
                            f"Expected non-education icon, got {result['AI.md']}")


class TestGlobalDedup(unittest.TestCase):
    def make_vault(self, files: list):
        temp_dir = tempfile.TemporaryDirectory()
        vault = Path(temp_dir.name)
        iconic = vault / ".obsidian" / "plugins" / "iconic"
        iconic.mkdir(parents=True)
        (iconic / "data.json").write_text(
            json.dumps({"fileIcons": {}, "bookmarkIcons": {}, "propertyIcons": {}}),
            encoding="utf-8",
        )
        for f in files:
            p = vault / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"# {p.name}", encoding="utf-8")
        return temp_dir, vault

    def test_dir_and_file_no_conflict(self):
        """目录图标和文件图标不应冲突"""
        files = ["docs/readme.md", "tools/setup.md", "AI/agent.md", "笔记/note.md"]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        dir_icons = a.assign_directory_icons(dirs, used)
        file_icons = a.assign_file_icons(md, used)
        all_vals = list(dir_icons.values()) + list(file_icons.values())
        self.assertEqual(len(all_vals), len(set(all_vals)),
                         f"目录+文件图标应全部不重复，重复: {Counter(all_vals).most_common(3)}")

    def test_force_reassign_still_unique(self):
        """--force 模式重新分配仍不重复"""
        files = ["a/x.md", "b/y.md", "c/z.md", "d/w.md"]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        dir_icons = a.assign_directory_icons(dirs, used, skip_existing=False)
        file_icons = a.assign_file_icons(md, used, skip_existing=False)
        all_vals = list(dir_icons.values()) + list(file_icons.values())
        self.assertEqual(len(all_vals), len(set(all_vals)))

    def test_existing_icons_respected(self):
        """已有图标的文件在 --skip-existing 下不被替换"""
        temp_dir = tempfile.TemporaryDirectory()
        vault = Path(temp_dir.name)
        iconic = vault / ".obsidian" / "plugins" / "iconic"
        iconic.mkdir(parents=True)
        config = {
            "fileIcons": {
                "旧文件.md": {"icon": "lucide-star"},
            },
            "bookmarkIcons": {},
            "propertyIcons": {},
        }
        (iconic / "data.json").write_text(json.dumps(config), encoding="utf-8")
        (vault / "旧文件.md").write_text("# 旧文件", encoding="utf-8")
        (vault / "新文件.md").write_text("# 新文件", encoding="utf-8")
        self.addCleanup(temp_dir.cleanup)

        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set(a.existing_icons.values())
        a.assign_directory_icons(dirs, used)
        file_icons = a.assign_file_icons(md, used)

        self.assertEqual(file_icons.get("旧文件.md"), "lucide-star",
                         "旧文件图标应保持不变")
        self.assertIsNotNone(file_icons.get("新文件.md"),
                             "新文件应被分配图标")


if __name__ == "__main__":
    unittest.main()
