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

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from assign_icons import IconAssigner


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


if __name__ == "__main__":
    unittest.main()
