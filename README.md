# WorkTag - Windows 桌面工作日志工具

一个基于 Python + PySide6 + SQLite 的 Windows 桌面工作日志工具，帮助工程师快速记录每日工作并一键生成周报。

## 功能特性

- 🏷️ **标签式窗口**：桌面常驻无边框窗口，不打断工作流
- ⚡ **快速输入**：支持 `[项目名]` 和 `#标签` 格式解析
- 📅 **自动日期**：自动记录日期和时间
- 💾 **本地存储**：使用 SQLite 数据库，数据安全可靠
- 📊 **周报生成**：一键生成 Markdown 格式周报
- 🎯 **项目统计**：自动按项目分类统计
- 🖥️ **系统托盘**：支持最小化到系统托盘
- 🎨 **暗色主题**：现代化暗色界面，保护眼睛
- 📋 **项目选择**：快速选择常用项目，无需重复输入

## 安装与运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python main.py
```

或者直接运行：

```bash
python main.py
```

## 使用说明

### 基本操作

1. **启动程序**：运行 `python main.py`，窗口会出现在桌面右上角
2. **输入工作内容**：
   - 格式：`[项目名] 工作内容 #标签`
   - 示例：`[Unity][Ads] 修复激励广告回调 #bug #hook`
3. **提交记录**：按 `Enter` 键或点击"添加记录"按钮
4. **隐藏窗口**：按 `Esc` 键或点击关闭按钮（最小化到托盘）
5. **显示窗口**：双击系统托盘图标

### 输入格式解析

- `[项目名]`：会被提取为项目字段，支持多个项目
- `#标签`：会被提取为标签字段，支持多个标签
- 剩余文本：作为工作内容

### 项目选择功能

WorkTag 新增了项目选择功能，让您无需重复输入项目名：

1. **项目按钮区域**：窗口顶部显示常用项目按钮
2. **快速插入**：点击项目按钮即可将 `[项目名]` 插入到输入框光标位置
3. **使用统计**：系统自动统计项目使用次数，常用项目排在前面
4. **项目管理**：
   - **从历史导入**：自动从已有日志记录中提取项目名
   - **添加项目**：手动添加新项目
   - **刷新**：重新加载项目列表

**使用示例**：
- 点击 `[Unity]` 按钮 → 输入框自动插入 `[Unity]`
- 继续输入工作内容：`修复广告回调 #bug`
- 完整输入：`[Unity] 修复广告回调 #bug`

### 周报生成

1. 点击"生成周报"按钮
2. 程序会自动生成本周（周一到周日）的工作报告
3. 报告保存为 Markdown 格式：`export/week_report_YYYY-MM-DD_to_YYYY-MM-DD.md`

## 项目结构

```
worktag/
├── main.py              # 程序入口
├── ui/
│   └── main_window.py   # 主窗口界面
├── db/
│   └── database.py      # 数据库操作
├── service/
│   ├── parser.py        # 输入解析
│   └── report.py        # 周报生成
├── data/
│   └── worklog.db       # SQLite 数据库（自动创建）
├── export/              # 周报导出目录
├── requirements.txt     # 依赖列表
└── README.md           # 说明文档
```

## 数据库设计

```sql
CREATE TABLE work_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,        -- 日期：2026-01-19
    content TEXT NOT NULL,     -- 工作内容
    project TEXT,              -- 项目：Unity / Ads / AOSP
    tags TEXT,                 -- 标签：#hook,#bug
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 新增 projects 表（v1.1.0）
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,          -- 项目名称
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usage_count INTEGER DEFAULT 0       -- 使用次数统计
);
```

## 快捷键

- `Enter`：提交工作记录
- `Esc`：隐藏窗口到托盘
- `Delete`：删除选中的记录（需先选中）
- `鼠标拖拽`：移动窗口位置

## 系统要求

- Windows 10/11
- Python 3.8+
- PySide6 6.5.0+

## 开发计划

- [x] **项目选择功能**：快速选择常用项目（v1.1.0）
- [ ] 支持自定义窗口位置记忆
- [ ] 支持数据备份与恢复
- [ ] 支持导出为 Word/PDF 格式
- [ ] 支持数据图表可视化
- [ ] 支持搜索和筛选功能
- [ ] 支持开机自启动

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

WorkTag 项目 - 为工程师打造的高效工作日志工具
