# Obsidian Icon Assigner — 语义化 + 全局去重设计

日期: 2026-07-24
状态: 草稿（待评审）

---

## 1. 当前问题

Obsidian Iconic 插件的图标分配器当前只有路径哈希分配，没有任何语义理解。文件"季度总结.md"可能拿到"火箭"图标，"部署脚本.md"可能拿到"心形"。用户希望：

1. **图标符合文章语义**——根据文件名关键词分配相关图标
2. **全局去重**——同一 vault 内的目录与文件、文件与文件之间图标不重复（除非图标池耗尽）
3. **同义不同图标**——多个"笔记"文件不要全挤在同一个图标上，但在同一个视觉类别里

## 2. 已确认的设计决策

| # | 决策项 | 结论 | 理由 |
|---|--------|------|------|
| 1 | 语义来源 | 文件名匹配（非正文 OCR） | 快、零 IO、Obisidian 文件名有语义 |
| 2 | 匹配方式 | 全文件名模糊匹配，不区分大小写 | 与现有 `assign_directory_icons` 实现一致 |
| 3 | 关键词→图标表 | 单表 `KEYWORD_ICONS`（合并目录+文件） | 一份映射两处用，避免维护两套 |
| 4 | 匹配优先级 | 语义第一，不重复第二 | 用户需求原话 |
| 5 | 同义文件分派 | 同类别不同图标（B 方案） | "笔记001"→notebook，"笔记002"→book-open |
| 6 | 目录图标 | 同样走新逻辑 | 一致性，一次改完 |
| 7 | 多关键词匹配 | 按 `KEYWORD_ICONS` dict 定义顺序先匹配先得，不做额外约束 | 用户确认不做优先级规则 |
| 8 | 图标不在分类中 | 回退到全局池去重，同时打印 warning 日志 | 避免静默降级让用户困惑 |
| 9 | 分配输出 | 每条分配打印一行 `[语义/哈希] 文件名 → 图标名` | 方便用户验证语义匹配正确性 |
| 10 | 短关键词防护 | 长度 < 3 的关键词用词边界匹配（`\bkeyword\b`），≥3 的用 `in` | 避免 `"AI" in "traiNING"` 类假阳性 |
| 11 | 目录/文件分配顺序 | 目录先于文件分配（目录结构骨架优先获得语义图标） | 隐式决策，显式文档化 |
| 12 | 实现方式 | **轻量改造**（不改 CLI/配置格式） | YAGNI，最小改动 |

## 3. 数据结构的改动

### 3.1 `DIR_KEYWORD_ICONS` → `KEYWORD_ICONS`

原名暗示"仅目录用"，现合并为一份通用映射表，变量名改 `KEYWORD_ICONS`。内容和格式不变。

### 3.2 新增 `ICON_TO_CATEGORY` 反查表

自动从 `ICON_CATEGORIES` 生成，运行时只读：

```python
ICON_TO_CATEGORY = {}
for cat_name, icons in ICON_CATEGORIES.items():
    for icon in icons:
        ICON_TO_CATEGORY[icon] = cat_name
```

作用：给定一个 Lucide 图标名，O(1) 查到它所属的视觉类别（"book""tech""time"等）。

### 3.3 `used_icons` 追踪集

已在上一轮改动中实现。`run()` 中创建 `used_icons = set()`，传入 `assign_directory_icons` 和 `assign_file_icons`，两者向同一集合追加。确保目录图标和文件图标在同一命名空间内去重。

## 4. 文件图标分配流程（核心改动）

```
for 每个文件(按路径排序):
    1. 跳过已存在图标? → 是则跳过
    2. 文件名扫描 KEYWORD_ICONS (全文件名模糊匹配)
        2a. 匹配到关键词 → 拿到目标图标 target 和所属类别 cat
            2a1. target 未使用 → 分配 target
            2a2. target 已使用 → 扫描 cat 类别所有图标
                 ├─ 有未用图标 → 分配该类中第一个未用的
                 └─ 全用完了   → 扫描全局图标池
                                ├─ 有未用 → 分配全局未用
                                └─ 全用完 → 最少使用回退
        2b. 无匹配 → 全量哈希扫描 ALL_ICONS·寻找未用图标
             ├─ 找到 → 分配
             └─ 全用完 → 最少使用回退
    3. 分配结果加入 used_icons
```

### 关键细节

**2a2"同类优先"的查找方式**：从目标 icon 在类别列表中的位置开始，循环偏移寻找，确定性（同一文件永远找到同一回退图标）：

```python
cat_icons = ICON_CATEGORIES[cat]
start = cat_icons.index(target)
for offset in range(1, len(cat_icons)):
    candidate = cat_icons[(start + offset) % len(cat_icons)]
    if candidate not in used_icons:
        assign(candidate)
        break
```

如果 `ICON_TO_CATEGORY` 查不到目标图标（如 `lucide-container` 不属于任何已定义类别），静默回退到全局池去重（走 2b 路径）。

**分配顺序**：目录先于文件分配。目录作为 vault 的结构骨架优先获得语义匹配图标，文件拿到时 `used_icons` 已含目录的分配结果，会从同类或全局池找替代。

**短关键词防护**：关键词长度 < 3 时（如 `"AI"`、`"k8s"`），用正则词边界匹配 `re.search(r'\b' + re.escape(keyword) + r'\b', filename, re.I)`，避免 `"AI" in "traiNING"` 或 `"es" in "notes"` 类假阳性。长度 ≥ 3 的关键词保持 `keyword.lower() in filename.lower()` 全文件名模糊匹配。

**未分类图标 warning**：`ICON_TO_CATEGORY` 查不到目标图标时，除了回退到全局池，还打印一行 warning：
```
⚠ 警告: lucide-container 不属于任何已定义分类，已回退到全局池分配
```

```
[语义] 周报-03.md → lucide-calendar（匹配: 周报）
[哈希] 部署脚本.md → lucide-terminal
[语义] notes/docs.md → lucide-book-open（匹配: docs）
```

常规模式保持简洁输出；`--dry-run` 模式下同样打印预览。

**大小写**：文件名匹配不区分大小写（`keyword.lower() in filename.lower()`）。

**2b"全量扫描"**：从文件哈希指纹位置开始，遍历全部 119 个图标，而不是截断为 50 次。保证只要有一个未用图标就能找到。

**"最少使用回退"**：用 Counter 统计已分配图标的使用频次，选频次最低的，同频则用文件名哈希确定。

## 5. 目录图标分配流程（同步改动）

与文件流程类似，但目录无匹配时的回退池为 `FOLDER_ICONS`（而非 `ALL_ICONS`），且在文件夹池内做去重感知：

```
for 每个目录(按路径排序):
    1. 跳过已存在图标? → 是则跳过
    2. 目录名扫描 KEYWORD_ICONS
        2a. 匹配到关键词 → 同文件流程 2a (同类优先→全局去重→最少使用)
        2b. 无匹配 → 从 FOLDER_ICONS 选未用图标
            ├─ 有未用 → 分配
            └─ 全用完 → 哈希循环分配
    3. 分配结果加入 used_icons
```

这里的"同类优先"与文件池共享同一个 `used_icons` 集，所以 `lucide-brain`（"AI"→brain）被目录用了，文件就不会再拿到它。除非池耗尽。

## 6. 颜色逻辑

颜色继承逻辑（`assign_directory_colors`）**完全不动**。

文件颜色照旧从所在目录的颜色继承。本设计只改图标分配，不改颜色。

## 7. 测试策略

在现有 `test_assign_icons.py` 基础上新增 3 个测试类：

| 测试 | 验证点 |
|------|--------|
| `test_file_keyword_matching` | "周报-03.md"匹配"周报"→拿到 time 类图标 |
| `test_same_keyword_diff_icon` | "笔记-001""笔记-002"拿到同类别不同图标 |
| `test_global_dedup_with_dirs` | 目录和文件共 30 个标识，全部不重复 |
| `test_category_exhaustion_fallback` | 某个类别所有图标用完后回退到全局池 |
| `test_keyword_icon_taken` | 关键词匹配的图标被占，从同类选另一个 |

## 8. 不需改动的内容

- CLI 参数（`--vault-path`、`--force`、`--dry-run`、`--list-icons`、`--skip-existing`）
- `data.json` 的读写格式
- 备份机制
- 颜色继承逻辑
- SKILL.md 的章节结构和参数说明（只更新描述文字）

## 9. 开放问题

无。所有设计决策已在第 2 节确认。

---

## GSTACK REVIEW REPORT

### 运行

- **Skill**: plan-design-review
- **Design doc**: 2026-07-24-obsidian-icon-semantic-unique.md
- **Scope**: Python CLI 脚本设计（非 UI 界面）

### 各轮评分

| Pass | 维度 | 评分 | 说明 |
|------|------|------|------|
| 1 | 信息架构 | 8→9/10 | 多关键词匹配顺序已明确 |
| 2 | 边界状态 | 7→9/10 | 缺失分类图标的回退已明确 |
| 3 | 用户旅程 | 6→8/10 | 添加逐条分配日志让用户可见 |
| 4 | AI Slop 风险 | 10/10 | 设计描述具体，无模糊段落 |
| 5 | 代码库对齐 | 10/10 | 保持单文件+argparse+零依赖 |
| 6 | 容量与容错 | 8→9/10 | 大小写敏感性已补充 |
| 7 | 未解决决策 | 0→0 | 全部已解决 |

### 审核发现汇总

| # | 发现 | 来源 | 状态 |
|---|------|------|------|
| 1 | 多关键词匹配优先级未定义 | plan-design-review | ✅ 按 dict 顺序先匹配先得 |
| 2 | 图标不在 `ICON_CATEGORIES` 时 KeyError 风险 | plan-design-review | ✅ 回退到全局池 + warning |
| 3 | 用户看不到分配细节 | plan-design-review | ✅ 逐条打印 `[语义/哈希] 文件名 → 图标` |
| 4 | 大小写敏感性未注明 | plan-design-review | ✅ 不区分大小写，文档已补充 |
| 5 | 短关键词假阳性（"AI"→"training"） | codex | ✅ 长度 < 3 时用词边界匹配 |
| 6 | 未分类图标静默降级丢失语义 | codex | ✅ 加 warning 日志 |
| 7 | 目录/文件分配顺序隐式决策 | codex | ✅ 文档已注明"目录先于文件" |

**CODEX**: 9 条发现中采纳 3 条（#5 短关键词防护、#6 warning 日志、#7 顺序说明），1 条为误报（#3 `--skip-existing` 不追踪旧图标——代码已用 `self.existing_icons.values()` 初始化），其余列为不采纳（与设计原则不一致或超出范围）。

**VERDICT**: 审核通过。设计文档已更新，可直接用于实现。
