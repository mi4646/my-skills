# Obsidian Icon Assigner — 语义化 + 全局去重 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现文件名语义匹配图标分配 + 同类别优先回退 + 全局去重

**架构:** 在现有单文件 Python 脚本 `assign_icons.py` 中做轻量改造。新增 `ICON_TO_CATEGORY` 反查表、`_match_keyword` 短关键词防护函数；改造 `assign_directory_icons` 和 `assign_file_icons` 两个方法加入语义匹配→分类回退→全局去重链路。

**Tech Stack:** Python 3.7+, 零外部依赖

## Global Constraints

- 不改动 CLI 参数、data.json 格式、备份机制、颜色逻辑
- SKILL.md 只更新描述性文字
- 匹配唯一性：语义第一，不重复第二
- 所有分配到的方法共享同一份 `used_icons` 集合以实现全局去重

---

### Task 1: 重命名 `DIR_KEYWORD_ICONS` + 新增 `ICON_TO_CATEGORY` 反查表

**Files:**
- Modify: `skills/obsidian-icon-assigner/scripts/assign_icons.py:101-161`

**Interfaces:**
- Consumes: `ICON_CATEGORIES`（已存在）
- Produces: `KEYWORD_ICONS`（全局变量，Dict[str, str]），`ICON_TO_CATEGORY`（全局变量，Dict[str, str]）

- [ ] **Step 1: 原地重命名 `DIR_KEYWORD_ICONS` → `KEYWORD_ICONS`**

在 `skills/obsidian-icon-assigner/scripts/assign_icons.py` 中把第 102 行的变量定义名 `DIR_KEYWORD_ICONS` 改为 `KEYWORD_ICONS`。内容是相同的 dict，不增减键值对。

改动后，`assign_directory_icons` 中引用 `DIR_KEYWORD_ICONS` 的地方也需要同步改。搜索整个文件，把所有 `DIR_KEYWORD_ICONS` 替换为 `KEYWORD_ICONS`。

预期：文件内全部 3 处引用同步改名。

- [ ] **Step 2: 在 `KEYWORD_ICONS` 定义之后添加 `ICON_TO_CATEGORY` 反查表**

在 `KEYWORD_ICONS` 定义后面（约第 150 行后）、`FOLDER_ICONS` 定义前，插入：

```python
# 图标名 → 所属分类的反查表（自动从 ICON_CATEGORIES 生成）
ICON_TO_CATEGORY = {}
for _cat_name, _icons in ICON_CATEGORIES.items():
    for _icon in _icons:
        ICON_TO_CATEGORY[_icon] = _cat_name
```

- [ ] **Step 3: 验证无编译错误**

Run: `python -c "import ast; ast.parse(open('skills/obsidian-icon-assigner/scripts/assign_icons.py').read()); print('语法 OK')"`

Expected: `语法 OK`

- [ ] **Step 4: 提交**

```bash
git add skills/obsidian-icon-assigner/scripts/assign_icons.py
git commit -m "feat(icon): 重命名 DIR_KEYWORD_ICONS -> KEYWORD_ICONS，新增 ICON_TO_CATEGORY 反查表"
```

---

### Task 2: 添加短关键词防护函数 + import re

**Files:**
- Modify: `skills/obsidian-icon-assigner/scripts/assign_icons.py:9-17`

**Interfaces:**
- Produces: `_match_keyword(filename: str, keyword: str) -> bool`（模块级辅助函数）

- [ ] **Step 1: 在现有 import 之后添加 `import re`**

在第 12 行（`import hashlib`）和第 13 行（`import argparse`）之间插入：

```python
import re
```

- [ ] **Step 2: 在 `ICON_TO_CATEGORY` 定义之后、`FOLDER_ICONS` 定义之前（约第 156 行后），插入辅助函数**

```python
def _match_keyword(name: str, keyword: str) -> bool:
    """关键词匹配函数，短关键词（<3字符）用词边界正则避免假阳性"""
    if len(keyword) < 3:
        return bool(re.search(r'\b' + re.escape(keyword) + r'\b', name, re.IGNORECASE))
    return keyword.lower() in name.lower()
```

- [ ] **Step 3: 验证函数行为**

Run:
```python
python3 -c "
import sys; sys.path.insert(0, '.')
from skills.obsidian-icon-assigner.scripts.assign_icons import _match_keyword
# 短关键词无假阳性
assert _match_keyword('training.md', 'AI') == False, 'AI 不应匹配 training'
# 短关键词真匹配
assert _match_keyword('AI-agent.md', 'AI') == True, 'AI 应匹配 AI-agent'
# 长关键词正常匹配
assert _match_keyword('笔记-2024.md', '笔记') == True
assert _match_keyword('docker-compose.md', 'docker') == True
assert _match_keyword('zig.md', 'docker') == False
print('全部断言通过')
"
```
Expected: `全部断言通过`

- [ ] **Step 4: 提交**

```bash
git add skills/obsidian-icon-assigner/scripts/assign_icons.py
git commit -m "feat(icon): 添加 import re 和 _match_keyword 短关键词防护函数"
```

---

### Task 3: 改造 `assign_directory_icons` — 语义匹配 + 分类回退 + 日志

**Files:**
- Modify: `skills/obsidian-icon-assigner/scripts/assign_icons.py:278-313`

**Interfaces:**
- Consumes: `KEYWORD_ICONS`（已改名）, `ICON_TO_CATEGORY`（Task 1）, `_match_keyword`（Task 2）, `used_icons: Set[str]`
- Produces: `assign_directory_icons(directories, used_icons, skip_existing) -> Dict[str, str]`（签名不变，行为增强）

- [ ] **Step 1: 整体替换 `assign_directory_icons` 方法**

将当前 `assign_directory_icons` 方法体（第 278-313 行）替换为：

```python
    def assign_directory_icons(self, directories: Set[str], used_icons: Set[str], skip_existing: bool = True) -> Dict[str, str]:
        """为目录分配图标（语义匹配 → 同类优先 → 全局去重 → 文件夹池）"""
        assigned = {}
        skipped = 0
        assigned_count = 0

        for directory in sorted(directories):
            if skip_existing and directory in self.existing_icons:
                assigned[directory] = self.existing_icons[directory]
                skipped += 1
                continue

            matched_icon = None
            for keyword, icon in KEYWORD_ICONS.items():
                if _match_keyword(directory, keyword):
                    matched_icon = icon
                    break

            if matched_icon:
                if matched_icon not in used_icons:
                    used_icons.add(matched_icon)
                    assigned[directory] = matched_icon
                    print(f"  [语义] {directory}/ → {matched_icon}（匹配: {keyword}）")
                else:
                    # 图标已被占，同类优先回退
                    cat = ICON_TO_CATEGORY.get(matched_icon)
                    found = None
                    if cat:
                        cat_icons = ICON_CATEGORIES[cat]
                        start = cat_icons.index(matched_icon)
                        for offset in range(1, len(cat_icons)):
                            candidate = cat_icons[(start + offset) % len(cat_icons)]
                            if candidate not in used_icons:
                                found = candidate
                                break
                    if not found:
                        # 同类全用完或无分类 → 全局池寻未用
                        for candidate in ALL_ICONS:
                            if candidate not in used_icons:
                                found = candidate
                                break
                        if not found:
                            # 全部用完 → 最少使用
                            from collections import Counter
                            usage = Counter(assigned.values())
                            min_usage = min(usage.values())
                            candidates = [ic for ic, cnt in usage.items() if cnt == min_usage]
                            found = candidates[hash(directory) % len(candidates)]
                    if not cat:
                        print(f"  ⚠ 警告: {matched_icon} 不属于任何已定义分类，已回退到全局池分配")
                    used_icons.add(found)
                    assigned[directory] = found
                    print(f"  [语义] {directory}/ → {found}（匹配: {keyword}，{matched_icon} 已被占）")
            else:
                # 无关键词匹配 → 从文件夹池选未用
                hash_bytes = hashlib.sha256(directory.encode()).digest()
                icon_index = int.from_bytes(hash_bytes[:2], 'big') % len(FOLDER_ICONS)
                for offset in range(len(FOLDER_ICONS)):
                    candidate = FOLDER_ICONS[(icon_index + offset) % len(FOLDER_ICONS)]
                    if candidate not in used_icons:
                        assigned[directory] = candidate
                        used_icons.add(candidate)
                        break
                else:
                    # 文件夹池全用完，直接哈希分配
                    assigned[directory] = FOLDER_ICONS[icon_index]
                    used_icons.add(assigned[directory])
                print(f"  [哈希] {directory}/ → {assigned[directory]}")
            assigned_count += 1

        print(f"目录图标分配完成: 跳过 {skipped} 个, 新分配 {assigned_count} 个")
        return assigned
```

⚠ **注意**: 第 303 行 `hash(directory)` 在 Python 中不同进程间不稳定（PEP 552）。如果需要跨进程可重复性，请用 `int.from_bytes(hashlib.sha256(directory.encode()).digest()[:4], 'big')` 替代。

- [ ] **Step 2: 运行现有测试确保颜色逻辑不受影响**

Run: `cd skills/obsidian-icon-assigner/scripts && python test_assign_icons.py`

Expected: `....` (4 dots, all pass)

- [ ] **Step 3: 提交**

```bash
git add skills/obsidian-icon-assigner/scripts/assign_icons.py
git commit -m "feat(icon): assign_directory_icons 语义匹配 + 分类回退 + 日志"
```

---

### Task 4: 改造 `assign_file_icons` — 语义匹配 + 分类回退 + 日志

**Files:**
- Modify: `skills/obsidian-icon-assigner/scripts/assign_icons.py:315-359`

**Interfaces:**
- Consumes: `KEYWORD_ICONS`（Task 1）, `ICON_TO_CATEGORY`（Task 1）, `_match_keyword`（Task 2）, `used_icons: Set[str]`
- Produces: `assign_file_icons(files, used_icons, skip_existing) -> Dict[str, str]`（签名不变，行为增强）

- [ ] **Step 1: 整体替换 `assign_file_icons` 方法**

将当前 `assign_file_icons` 方法体（第 315-359 行）替换为：

```python
    def assign_file_icons(self, files: List[str], used_icons: Set[str], skip_existing: bool = True) -> Dict[str, str]:
        """为文件分配图标（语义匹配 → 同类优先 → 全局去重 → 最少使用回退）"""
        assigned = {}
        skipped = 0
        assigned_count = 0
        conflicts = 0

        for file_path in sorted(files):
            if skip_existing and file_path in self.existing_icons:
                assigned[file_path] = self.existing_icons[file_path]
                skipped += 1
                continue

            filename = file_path.rsplit('/', 1)[-1]  # 提取文件名部分

            # 优先尝试文件名语义匹配
            matched_keyword = None
            matched_icon = None
            for keyword, icon in KEYWORD_ICONS.items():
                if _match_keyword(filename, keyword):
                    matched_keyword = keyword
                    matched_icon = icon
                    break

            if matched_icon:
                if matched_icon not in used_icons:
                    used_icons.add(matched_icon)
                    assigned[file_path] = matched_icon
                    print(f"  [语义] {file_path} → {matched_icon}（匹配: {matched_keyword}）")
                    assigned_count += 1
                    continue

                # 图标已被占 → 同类优先回退
                cat = ICON_TO_CATEGORY.get(matched_icon)
                found = None
                if cat:
                    cat_icons = ICON_CATEGORIES[cat]
                    start = cat_icons.index(matched_icon)
                    for offset in range(1, len(cat_icons)):
                        candidate = cat_icons[(start + offset) % len(cat_icons)]
                        if candidate not in used_icons:
                            found = candidate
                            break
                if not found:
                    # 同类全用完或无分类 → 全局池寻未用
                    for candidate in ALL_ICONS:
                        if candidate not in used_icons:
                            found = candidate
                            break
                    if not found:
                        # 全部图标用完 → 最少使用回退
                        from collections import Counter
                        usage = Counter(list(assigned.values()) + list(self.existing_icons.values()))
                        min_usage = min(usage.values())
                        candidates = [ic for ic, cnt in usage.items() if cnt == min_usage]
                        found = candidates[hash(file_path) % len(candidates)]
                        conflicts += 1
                if not cat:
                    print(f"  ⚠ 警告: {matched_icon} 不属于任何已定义分类，已回退到全局池分配")
                used_icons.add(found)
                assigned[file_path] = found
                print(f"  [语义] {file_path} → {found}（匹配: {matched_keyword}，{matched_icon} 已被占）")
                assigned_count += 1
            else:
                # 无关键词匹配 → 哈希全量扫描去重
                hash_obj = hashlib.sha256(file_path.encode())
                fingerprint = int.from_bytes(hash_obj.digest()[:8], 'big')
                icon_assigned = False
                for attempt in range(len(ALL_ICONS)):
                    icon_index = (fingerprint + attempt) % len(ALL_ICONS)
                    candidate = ALL_ICONS[icon_index]
                    if candidate not in used_icons:
                        used_icons.add(candidate)
                        assigned[file_path] = candidate
                        icon_assigned = True
                        assigned_count += 1
                        break
                if not icon_assigned:
                    from collections import Counter
                    usage = Counter(list(assigned.values()) + list(self.existing_icons.values()))
                    min_usage = min(usage.values())
                    candidates = [ic for ic, cnt in usage.items() if cnt == min_usage]
                    chosen = candidates[fingerprint % len(candidates)]
                    assigned[file_path] = chosen
                    assigned_count += 1
                    conflicts += 1
                print(f"  [哈希] {file_path} → {assigned[file_path]}")

        print(f"图标分配完成: 跳过 {skipped} 个, 新分配 {assigned_count} 个, 冲突解决 {conflicts} 个")
        return assigned
```

- [ ] **Step 2: 快速功能验证**

Run:
```python
python3 -c "
import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, 'skills/obsidian-icon-assigner/scripts')
from assign_icons import IconAssigner, KEYWORD_ICONS, ICON_TO_CATEGORY, _match_keyword

# 验证反查表和匹配函数可用
assert len(ICON_TO_CATEGORY) > 0, 'ICON_TO_CATEGORY 不应为空'
assert _match_keyword('笔记-001.md', '笔记') == True

# 验证 ICON_TO_CATEGORY 含已知图标
assert ICON_TO_CATEGORY.get('lucide-notebook') == 'book'
print('基础验证通过')

# 构建小型 vault 验证全流程不崩溃
vault = Path(tempfile.mkdtemp())
iconic = vault / '.obsidian' / 'plugins' / 'iconic'
iconic.mkdir(parents=True)
(iconic / 'data.json').write_text(json.dumps({'fileIcons':{},'bookmarkIcons':{},'propertyIcons':{}}))
for d in ['笔记', '周报', '项目']:
    (vault / d).mkdir(parents=True, exist_ok=True)
    (vault / d / '001.md').write_text('# 1')
    (vault / d / '002.md').write_text('# 2')

a = IconAssigner(str(vault))
a.load_config()
files = a.scan_markdown_files()
dirs = a.get_directories(files)
used = set()
dir_icons = a.assign_directory_icons(dirs, used)
file_icons = a.assign_file_icons(files, used)

all_vals = list(dir_icons.values()) + list(file_icons.values())
assert len(all_vals) == len(set(all_vals)), f'存在重复图标'
print(f'全流程通过: {len(all_vals)} 个图标全部不重复')
"
```

Expected: 控制台输出分配日志 + `基础验证通过` + `全流程通过`

- [ ] **Step 3: 运行现有测试确保无回归**

Run: `cd skills/obsidian-icon-assigner/scripts && python test_assign_icons.py`

Expected: `....` (4 dots, all pass)

- [ ] **Step 4: 提交**

```bash
git add skills/obsidian-icon-assigner/scripts/assign_icons.py
git commit -m "feat(icon): assign_file_icons 语义匹配 + 分类回退 + 日志"
```

---

### Task 5: 新增图标分配测试 — 关键字匹配与分类回退

**Files:**
- Modify: `skills/obsidian-icon-assigner/scripts/test_assign_icons.py`

**Interfaces:**
- Consumes: `IconAssigner`, `KEYWORD_ICONS`, `_match_keyword`, `ALL_ICONS`, `ICON_CATEGORIES`（从 `assign_icons` 导入）
- Produces: 测试类 `TestKeywordMatching`、`TestCategoryFallback`

- [ ] **Step 1: 在文件末尾（`if __name__` 之前）添加 `TestKeywordMatching` 测试类**

```python
class TestKeywordMatching(unittest.TestCase):
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

    def test_weekly_report_gets_time_icon(self):
        """‘周报-03.md’ 应匹配 ‘周报’→ 拿到 time 类图标"""
        files = ["周报-03.md"]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        a.assign_directory_icons(dirs, used)
        icons = a.assign_file_icons(md, used)
        icon = icons["周报-03.md"]
        self.assertIn(ICON_TO_CATEGORY.get(icon, ""), ("time", ""),
                      f"周报文件应拿到 time 类图标，实际得到 {icon}")

    def test_same_keyword_diff_icon(self):
        """‘笔记-001’ 和 ‘笔记-002’ 应拿到同类别不同图标"""
        files = ["笔记-001.md", "笔记-002.md"]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        a.assign_directory_icons(dirs, used)
        icons = a.assign_file_icons(md, used)
        i1, i2 = icons["笔记-001.md"], icons["笔记-002.md"]
        self.assertNotEqual(i1, i2, "两个笔记文件图标不应相同")
        # 如果都有分类，应是同类
        c1, c2 = ICON_TO_CATEGORY.get(i1), ICON_TO_CATEGORY.get(i2)
        if c1 and c2:
            self.assertEqual(c1, c2, f"同类文件名应拿到同分类图标: {i1}({c1}) vs {i2}({c2})")

    def test_no_keyword_fallback_to_hash(self):
        """无关键词匹配的文件应走哈希分配"""
        files = ["一个完全没有关键词的文件名.md"]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        a.assign_directory_icons(dirs, used)
        icons = a.assign_file_icons(md, used)
        self.assertIn(icons["一个完全没有关键词的文件名.md"], ALL_ICONS)
```

- [ ] **Step 2: 在 `if __name__` 前面添加 `TestCategoryFallback` 测试类**

```python
class TestCategoryFallback(unittest.TestCase):
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

    def test_keyword_icon_taken_falls_back_in_category(self):
        """目标图标被占时从同类选另一个"""
        files = ["笔记-A.md", "笔记-B.md"]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        a.assign_directory_icons(dirs, used)
        icons = a.assign_file_icons(md, used)
        i1, i2 = icons["笔记-A.md"], icons["笔记-B.md"]
        self.assertNotEqual(i1, i2)
        # 两个都应在 book 类（notebook 属于 book）
        c1 = ICON_TO_CATEGORY.get(i1)
        c2 = ICON_TO_CATEGORY.get(i2)
        if c1 and c2:
            self.assertEqual(c1, "book", f"笔记图标应在 book 类: {i1} -> {c1}")
            self.assertEqual(c2, "book", f"笔记图标应在 book 类: {i2} -> {c2}")

    def test_category_exhaustion_falls_back_to_global(self):
        """某个分类所有图标用完后应回退到全局池"""
        # time 分类只有 5 个图标，放 6 个匹配 time 的文件
        files = [f"周报-{i}.md" for i in range(6)]
        temp_dir, vault = self.make_vault(files)
        self.addCleanup(temp_dir.cleanup)
        a = IconAssigner(str(vault))
        a.load_config()
        md = a.scan_markdown_files()
        dirs = a.get_directories(md)
        used = set()
        a.assign_directory_icons(dirs, used)
        icons = a.assign_file_icons(md, used)
        all_icons = list(icons.values())
        self.assertEqual(len(all_icons), len(set(all_icons)), "6个文件应拿到6个不同图标")
        # 前5个应都在 time 类，第6个在全局池（time 已满）
        time_icons_count = sum(1 for ic in all_icons if ICON_TO_CATEGORY.get(ic) == "time")
        self.assertLessEqual(time_icons_count, 5, "time 类最多 5 个图标，第 6 个应回退到全局池")

    def test_short_keyword_no_false_positive(self):
        """短关键词 'AI' 不应匹配 'training.md'"""
        from assign_icons import _match_keyword
        self.assertFalse(_match_keyword("training.md", "AI"))
        self.assertTrue(_match_keyword("AI-agent.md", "AI"))
        self.assertTrue(_match_keyword("笔记.md", "笔记"))
```

- [ ] **Step 3: 运行全部测试**

Run: `cd skills/obsidian-icon-assigner/scripts && python test_assign_icons.py -v`

Expected: 所有测试（原有 4 个 + 新增 7 个，共 11 个）均通过。

- [ ] **Step 4: 提交**

```bash
git add skills/obsidian-icon-assigner/scripts/test_assign_icons.py
git commit -m "test(icon): 新增语义匹配、同类回退、短关键词防护测试"
```

---

### Task 6: 新增全局去重与端到端测试

**Files:**
- Modify: `skills/obsidian-icon-assigner/scripts/test_assign_icons.py`

- [ ] **Step 1: 在 `if __name__` 前面添加 `TestGlobalDedup` 测试类**

```python
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
```

- [ ] **Step 2: 在文件顶部 import 段添加 `Counter`（如果还没有）**

检查 `test_assign_icons.py` 顶部是否有 `from collections import Counter`，如果没有就添加。

- [ ] **Step 3: 运行全部测试**

Run: `cd skills/obsidian-icon-assigner/scripts && python test_assign_icons.py -v`

Expected: 全部 ~14 个测试通过。

- [ ] **Step 4: 提交**

```bash
git add skills/obsidian-icon-assigner/scripts/test_assign_icons.py
git commit -m "test(icon): 全局去重和存量文件尊重测试"
```

---

### Task 7: 更新 SKILL.md 描述文字

**Files:**
- Modify: `skills/obsidian-icon-assigner/SKILL.md:3`

- [ ] **Step 1: 更新 SKILL.md frontmatter 的 description 字段**

当前第 3 行：
```
description: ...目录级颜色继承，文件级图标保持不重复，同一个库内文件和目录无图标冲突...
```

改为：
```
description: ...目录级颜色继承，文件级图标保持不重复，同一个库内文件和目录无图标冲突。文件名语义匹配优先（关键词→相关图标），同类别回退，全量哈希去重。...
```

- [ ] **Step 2: 检查是否有其他处文字需要同步（可选）**

SKILL.md 中 "核心特性" 章节的 "🎯 图标不重复" 小节当前已经是正确的描述，不需要改。

- [ ] **Step 3: 提交**

```bash
git add skills/obsidian-icon-assigner/SKILL.md
git commit -m "docs(icon): 更新 SKILL.md description 提及语义匹配"
```

---

### Task 8: 最终集成验证

**Files:**
- 验证范围：整个 `skills/obsidian-icon-assigner/` 目录

- [ ] **Step 1: 完整测试套件**

Run: `cd skills/obsidian-icon-assigner/scripts && python -m pytest test_assign_icons.py -v 2>/dev/null || python test_assign_icons.py -v`

Expected: 全部测试通过（原有颜色继承 + 新增语义匹配 + 分类回退 + 全局去重，共 14+ 个测试）。

- [ ] **Step 2: 完整集成测试**

Run:
```python
python3 -c "
import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, 'skills/obsidian-icon-assigner/scripts')
from assign_icons import IconAssigner

# 模拟中型 vault（5 目录，20 文件，含语义+非语义文件）
vault = Path(tempfile.mkdtemp())
iconic = vault / '.obsidian' / 'plugins' / 'iconic'
iconic.mkdir(parents=True)
(iconic / 'data.json').write_text(json.dumps({'fileIcons':{},'bookmarkIcons':{},'propertyIcons':{}}))

scenarios = [
    '笔记/学习笔记.md', '笔记/工作笔记.md', '笔记/读书笔记.md',
    '周报/2024-03.md', '周报/2024-04.md',
    '项目/需求评审.md', '项目/技术方案.md', '项目/上线计划.md',
    'AI/prompt-design.md', 'AI/agent-test.md',
    '工具/脚本工具.md', '工具/自动化配置.md',
    '杂项/随手记.md', '杂项/todo.md',
]
for f in scenarios:
    p = vault / f
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f'# {p.name}', encoding='utf-8')

a = IconAssigner(str(vault))
a.load_config()
files = a.scan_markdown_files()
dirs = a.get_directories(files)
used = set(a.existing_icons.values())
dir_icons = a.assign_directory_icons(dirs, used)
file_icons = a.assign_file_icons(files, used)

all_icons = list(dir_icons.values()) + list(file_icons.values())
dup = len(all_icons) - len(set(all_icons))
print(f'文件: {len(files)}, 目录: {len(dirs)}, 总图标: {len(all_icons)}, 重复: {dup}')
assert dup == 0, f'有 {dup} 个重复图标'
print('✅ 集成验证通过')
"
```

Expected: 无重复图标，控制台输出语义/哈希分配日志。

- [ ] **Step 3: 最终 git 状态确认**

Run: `git log --oneline -5`

Expected: 显示最近 7-8 个提交，每个对应一个 Task。

- [ ] **Step 4: 声明完成**

输出：

```
✅ 实现完成。共 7 个功能任务 + 1 个集成验证。
核心改动集中在 assign_icons.py（~90 行新增/修改），
新增 10+ 个测试用例，
SKILL.md description 同步更新。
```
