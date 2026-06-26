#!/usr/bin/env python3
"""
Obsidian Iconic 图标自动分配器

为Obsidian知识库中的Markdown文档自动分配Iconic插件的图标和颜色。
遵循目录级颜色继承、文件级图标唯一性原则。
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import shutil
from datetime import datetime

# Lucide图标池（按主题分类）
ICON_CATEGORIES = {
    "document": [
        "lucide-file-text", "lucide-file", "lucide-file-code",
        "lucide-file-spreadsheet", "lucide-file-output", "lucide-file-input"
    ],
    "book": [
        "lucide-book", "lucide-book-open", "lucide-book-marked",
        "lucide-library", "lucide-notebook", "lucide-notebook-text"
    ],
    "tool": [
        "lucide-wrench", "lucide-settings", "lucide-tool", "lucide-hammer",
        "lucide-cog", "lucide-sliders", "lucide-microwave"
    ],
    "tech": [
        "lucide-code", "lucide-terminal", "lucide-server", "lucide-database",
        "lucide-cpu", "lucide-hard-drive", "lucide-network", "lucide-cloud"
    ],
    "media": [
        "lucide-image", "lucide-film", "lucide-music", "lucide-video",
        "lucide-headphones", "lucide-tv", "lucide-camera"
    ],
    "chart": [
        "lucide-bar-chart", "lucide-line-chart", "lucide-pie-chart",
        "lucide-trending-up", "lucide-trending-down"
    ],
    "communication": [
        "lucide-message-square", "lucide-mail", "lucide-send",
        "lucide-chat", "lucide-phone", "lucide-video"
    ],
    "person": [
        "lucide-user", "lucide-users", "lucide-user-plus",
        "lucide-user-check", "lucide-user-cog"
    ],
    "symbol": [
        "lucide-star", "lucide-heart", "lucide-flag", "lucide-bell",
        "lucide-key", "lucide-lock", "lucide-unlock", "lucide-shield"
    ],
    "time": [
        "lucide-calendar", "lucide-clock", "lucide-timer",
        "lucide-watch", "lucide-alarm-clock"
    ],
    "location": [
        "lucide-map", "lucide-map-pin", "lucide-globe", "lucide-compass",
        "lucide-navigation", "lucide-home"
    ],
    "business": [
        "lucide-briefcase", "lucide-building", "lucide-store",
        "lucide-credit-card", "lucide-dollar-sign", "lucide-tag"
    ],
    "education": [
        "lucide-graduation-cap", "lucide-school", "lucide-book-open-text",
        "lucide-lightbulb", "lucide-brain", "lucide-target"
    ],
    "nature": [
        "lucide-leaf", "lucide-tree", "lucide-flower", "lucide-mountain",
        "lucide-sun", "lucide-moon", "lucide-cloud"
    ],
    "transport": [
        "lucide-car", "lucide-bike", "lucide-train", "lucide-plane",
        "lucide-ship", "lucide-rocket"
    ],
    "food": [
        "lucide-utensils", "lucide-coffee", "lucide-wine", "lucide-pizza",
        "lucide-cake", "lucide-apple"
    ],
    "health": [
        "lucide-heart-pulse", "lucide-stethoscope", "lucide-pill",
        "lucide-bandage", "lucide-ambulance", "lucide-hospital"
    ],
    "sport": [
        "lucide-trophy", "lucide-medal", "lucide-gamepad-2",
        "lucide-football", "lucide-basketball", "lucide-tennis"
    ],
    "folder": [
        "lucide-folder", "lucide-folder-open", "lucide-folder-plus",
        "lucide-folder-search", "lucide-folder-heart", "lucide-folder-lock",
        "lucide-folder-tree", "lucide-folder-kanban", "lucide-folder-git",
        "lucide-folder-clock", "lucide-folder-input", "lucide-folder-output"
    ]
}

# 目录关键词 → 图标映射（用于目录图标语义分配）
DIR_KEYWORD_ICONS = {
    "技术": "lucide-code",
    "文档": "lucide-file-text",
    "AI": "lucide-brain",
    "agent": "lucide-bot",
    "python": "lucide-python",
    "docker": "lucide-container",
    "kubernetes": "lucide-ship-wheel",
    "k8s": "lucide-ship-wheel",
    "linux": "lucide-terminal",
    "mysql": "lucide-database",
    "rust": "lucide-ferris",
    "elastic": "lucide-search",
    "rabbitmq": "lucide-message-circle",
    "tauri": "lucide-window",
    "wsl": "lucide-monitor",
    "工具": "lucide-tool",
    "项目": "lucide-briefcase",
    "旅游": "lucide-plane",
    "资源": "lucide-bookmark",
    "收藏": "lucide-star",
    "个人": "lucide-user",
    "成长": "lucide-trending-up",
    "学习": "lucide-graduation-cap",
    "模板": "lucide-copy",
    "笔记": "lucide-notebook",
    "cli": "lucide-terminal",
    "superpowers": "lucide-zap",
    "claude": "lucide-sparkles",
    "prompt": "lucide-message-square",
    "skill": "lucide-lightbulb",
    "gstack": "lucide-git-branch",
    "clippings": "lucide-scissors",
    "驾照": "lucide-car",
    "安全": "lucide-shield",
    "测试": "lucide-check-circle",
    "docs": "lucide-book-open",
    "plans": "lucide-kanban",
    "specs": "lucide-file-check",
    "plugin": "lucide-puzzle",
    "指南": "lucide-compass",
    "应用": "lucide-app-window",
    "服务": "lucide-server",
    "配置": "lucide-settings",
    "数据": "lucide-database",
    "网络": "lucide-network",
    "开发": "lucide-code-2",
}
# 目录图标回退池（不被DIR_KEYWORD_ICONS覆盖时使用）
FOLDER_ICONS = [
    "lucide-folder", "lucide-folder-open", "lucide-folder-plus",
    "lucide-folder-search", "lucide-folder-heart", "lucide-folder-lock",
    "lucide-folder-tree", "lucide-folder-kanban", "lucide-folder-git",
    "lucide-folder-clock", "lucide-folder-input", "lucide-folder-output"
]

# 扁平化图标列表
ALL_ICONS = []
for category in ICON_CATEGORIES.values():
    ALL_ICONS.extend(category)


class IconAssigner:
    def __init__(self, vault_path: str, config_path: Optional[str] = None):
        """
        初始化图标分配器

        Args:
            vault_path: Obsidian vault路径
            config_path: Iconic插件配置文件路径，默认为.obsidian/plugins/iconic/data.json
        """
        self.vault_path = Path(vault_path).resolve()
        if config_path:
            self.config_path = Path(config_path).resolve()
        else:
            self.config_path = self.vault_path / ".obsidian" / "plugins" / "iconic" / "data.json"

        if not self.config_path.exists():
            raise FileNotFoundError(f"Iconic配置文件不存在: {self.config_path}")

        self.config = None
        self.existing_icons = {}  # 路径 -> 图标
        self.existing_colors = {}  # 路径 -> 颜色

    def load_config(self) -> Dict:
        """加载Iconic插件配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)

            # 提取现有图标和颜色
            if 'fileIcons' in self.config:
                for path, info in self.config['fileIcons'].items():
                    if isinstance(info, dict):
                        if 'icon' in info:
                            self.existing_icons[path] = info['icon']
                        if 'color' in info:
                            self.existing_colors[path] = info['color']

            return self.config
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件JSON格式错误: {e}")

    def save_config(self) -> None:
        """保存配置回文件"""
        # 创建备份
        backup_path = self.config_path.with_suffix(f'.{datetime.now().strftime("%Y%m%d_%H%M%S")}.bak')
        shutil.copy2(self.config_path, backup_path)
        print(f"已创建备份: {backup_path}")

        # 保存更新
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def scan_markdown_files(self) -> List[str]:
        """扫描vault中的所有Markdown文件"""
        md_files = []
        for root, dirs, files in os.walk(self.vault_path):
            # 跳过隐藏目录和系统目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    # 转换为相对于vault的路径
                    rel_path = os.path.relpath(file_path, self.vault_path)
                    md_files.append(rel_path.replace('\\', '/'))  # 统一使用正斜杠

        return md_files

    def get_directories(self, files: List[str]) -> Set[str]:
        """从文件列表中提取所有目录"""
        directories = set()
        for file_path in files:
            # 获取所有父目录
            parts = file_path.split('/')
            for i in range(1, len(parts)):  # 从1开始，排除文件名本身
                dir_path = '/'.join(parts[:i])
                if dir_path:  # 排除空字符串
                    directories.add(dir_path)
        return directories

    def find_parent_color(self, directory: str, colors: Dict[str, str]) -> Optional[str]:
        """查找最近父目录的颜色"""
        parts = directory.split('/')
        for i in range(len(parts) - 1, 0, -1):
            parent = '/'.join(parts[:i])
            if parent in colors:
                return colors[parent]
            if parent in self.existing_colors:
                return self.existing_colors[parent]
        return None

    def assign_directory_colors(self, directories: Set[str]) -> Dict[str, str]:
        """为目录分配颜色"""
        colors = {}

        for directory in sorted(directories):
            if directory in self.existing_colors:
                # 保留目录自身已有颜色
                colors[directory] = self.existing_colors[directory]
                continue

            parent_color = self.find_parent_color(directory, colors)
            if parent_color:
                # 新子目录继承最近父目录颜色
                colors[directory] = parent_color
                continue

            # 没有可继承的父目录颜色时，哈希生成HSL颜色
            hash_bytes = hashlib.sha256(directory.encode()).digest()
            hue = int.from_bytes(hash_bytes[:2], 'big') % 360
            colors[directory] = f"hsl({hue}, 70%, 50%)"

        return colors

    def assign_directory_icons(self, directories: Set[str], skip_existing: bool = True) -> Dict[str, str]:
        """为目录分配图标"""
        assigned = {}
        skipped = 0
        assigned_count = 0

        for directory in sorted(directories):
            if skip_existing and directory in self.existing_icons:
                assigned[directory] = self.existing_icons[directory]
                skipped += 1
                continue

            directory_lower = directory.lower()
            matched_icon = None
            for keyword, icon in DIR_KEYWORD_ICONS.items():
                if keyword.lower() in directory_lower:
                    matched_icon = icon
                    break

            if not matched_icon:
                hash_bytes = hashlib.sha256(directory.encode()).digest()
                icon_index = int.from_bytes(hash_bytes[:2], 'big') % len(FOLDER_ICONS)
                matched_icon = FOLDER_ICONS[icon_index]

            assigned[directory] = matched_icon
            assigned_count += 1

        print(f"目录图标分配完成: 跳过 {skipped} 个, 新分配 {assigned_count} 个")
        return assigned

    def assign_file_icons(self, files: List[str], skip_existing: bool = True) -> Dict[str, str]:
        """为文件分配图标"""
        assigned = {}
        used_icons = set(self.existing_icons.values())  # 已使用的图标

        # 统计跳过和分配的文件
        skipped = 0
        assigned_count = 0
        conflicts = 0

        for file_path in sorted(files):
            if skip_existing and file_path in self.existing_icons:
                # 跳过已有图标的文件
                assigned[file_path] = self.existing_icons[file_path]
                skipped += 1
                continue

            # 计算文件指纹（确定性哈希）
            hash_obj = hashlib.sha256(file_path.encode())
            fingerprint = int.from_bytes(hash_obj.digest()[:8], 'big')

            # 尝试分配唯一图标
            max_attempts = min(50, len(ALL_ICONS) * 2)  # 最大尝试次数
            icon_assigned = False

            for attempt in range(max_attempts):
                # 选择图标（基于指纹+尝试次数）
                icon_index = (fingerprint + attempt) % len(ALL_ICONS)
                candidate = ALL_ICONS[icon_index]

                if candidate not in used_icons:
                    used_icons.add(candidate)
                    assigned[file_path] = candidate
                    icon_assigned = True
                    assigned_count += 1
                    break

            if not icon_assigned:
                # 图标池耗尽，使用冲突解决策略
                # 选择使用最少的图标变体
                base_icon = ALL_ICONS[fingerprint % len(ALL_ICONS)]

                # 尝试变体1-5
                for variant_num in range(1, 6):
                    variant = f"{base_icon}-{variant_num}"
                    if variant not in used_icons:
                        used_icons.add(variant)
                        assigned[file_path] = variant
                        icon_assigned = True
                        assigned_count += 1
                        conflicts += 1
                        break

                if not icon_assigned:
                    # 最后手段：使用带修饰符的图标
                    assigned[file_path] = f"{base_icon}"
                    used_icons.add(assigned[file_path])
                    assigned_count += 1
                    conflicts += 1

        print(f"图标分配完成: 跳过 {skipped} 个, 新分配 {assigned_count} 个, 冲突解决 {conflicts} 个")
        return assigned

    def update_configuration(self, file_icons: Dict[str, str], dir_colors: Dict[str, str], dir_icons: Dict[str, str]) -> None:
        """更新配置文件"""
        if 'fileIcons' not in self.config:
            self.config['fileIcons'] = {}

        # 更新文件图标
        for file_path, icon in file_icons.items():
            if file_path not in self.config['fileIcons']:
                self.config['fileIcons'][file_path] = {}

            if isinstance(self.config['fileIcons'][file_path], dict):
                self.config['fileIcons'][file_path]['icon'] = icon

                # 设置颜色：使用文件所在目录的颜色
                dir_path = '/'.join(file_path.split('/')[:-1])
                if dir_path and dir_path in dir_colors:
                    self.config['fileIcons'][file_path]['color'] = dir_colors[dir_path]

        # 确保目录也有图标和颜色记录（用于未来继承）
        for dir_path, color in dir_colors.items():
            if dir_path not in self.config['fileIcons']:
                self.config['fileIcons'][dir_path] = {}
            if isinstance(self.config['fileIcons'][dir_path], dict):
                if dir_path in dir_icons:
                    self.config['fileIcons'][dir_path]['icon'] = dir_icons[dir_path]
                self.config['fileIcons'][dir_path]['color'] = color

    def run(self, skip_existing: bool = True, dry_run: bool = False) -> Dict:
        """
        运行图标分配

        Args:
            skip_existing: 是否跳过已有图标的文件
            dry_run: 试运行，不实际修改配置

        Returns:
            分配统计信息
        """
        print(f"=== Obsidian 图标自动分配器 ===")
        print(f"Vault路径: {self.vault_path}")
        print(f"配置文件: {self.config_path}")

        # 1. 加载配置
        print("1. 加载现有配置...")
        self.load_config()

        # 2. 扫描文件
        print("2. 扫描Markdown文件...")
        files = self.scan_markdown_files()
        print(f"   找到 {len(files)} 个.md文件")

        # 3. 提取目录
        directories = self.get_directories(files)
        print(f"   提取 {len(directories)} 个目录")

        # 4. 分配目录颜色
        print("3. 分配目录颜色...")
        dir_colors = self.assign_directory_colors(directories)

        # 5. 分配目录图标
        print("4. 分配目录图标...")
        dir_icons = self.assign_directory_icons(directories, skip_existing)

        # 6. 分配文件图标
        print("5. 分配文件图标...")
        file_icons = self.assign_file_icons(files, skip_existing)

        # 7. 更新配置
        if not dry_run:
            print("6. 更新配置文件...")
            self.update_configuration(file_icons, dir_colors, dir_icons)
            self.save_config()
            print("   配置已保存")
        else:
            print("6. [试运行] 跳过实际写入")

        # 统计信息
        stats = {
            'total_files': len(files),
            'total_directories': len(directories),
            'existing_file_icons': len([path for path in files if path in self.existing_icons]),
            'existing_dir_icons': len([path for path in directories if path in self.existing_icons]),
            'new_file_icons': len([path for path in file_icons if path not in self.existing_icons]),
            'new_dir_icons': len([path for path in dir_icons if path not in self.existing_icons]),
            'dir_colors_assigned': len(dir_colors),
            'dry_run': dry_run
        }

        print(f"\n=== 分配完成 ===")
        print(f"文件总数: {stats['total_files']}")
        print(f"目录总数: {stats['total_directories']}")
        print(f"已有文件图标: {stats['existing_file_icons']}")
        print(f"已有目录图标: {stats['existing_dir_icons']}")
        print(f"新分配文件图标: {stats['new_file_icons']}")
        print(f"新分配目录图标: {stats['new_dir_icons']}")
        print(f"目录颜色: {stats['dir_colors_assigned']}")

        return stats


def main():
    parser = argparse.ArgumentParser(description='Obsidian Iconic 图标自动分配器')
    parser.add_argument('--vault-path', required=True, help='Obsidian vault路径')
    parser.add_argument('--config-path', help='Iconic配置文件路径，默认为.obsidian/plugins/iconic/data.json')
    parser.add_argument('--skip-existing', action='store_true', default=True,
                       help='跳过已有图标的文件（默认: True）')
    parser.add_argument('--force', action='store_false', dest='skip_existing',
                       help='强制重新分配所有文件图标')
    parser.add_argument('--dry-run', action='store_true',
                       help='试运行，不实际修改配置文件')
    parser.add_argument('--list-icons', action='store_true',
                       help='列出所有可用图标')

    args = parser.parse_args()

    if args.list_icons:
        print("=== 可用Lucid图标 ===")
        for category, icons in ICON_CATEGORIES.items():
            print(f"\n{category}:")
            for icon in icons:
                print(f"  {icon}")
        print(f"\n总计: {len(ALL_ICONS)} 个图标")
        return

    try:
        assigner = IconAssigner(args.vault_path, args.config_path)
        stats = assigner.run(
            skip_existing=args.skip_existing,
            dry_run=args.dry_run
        )

        if args.dry_run:
            print("\n[试运行模式] 如需实际应用，请移除 --dry-run 参数")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()