# 贡献指南

欢迎为 MathPro 贡献代码、知识点地图和题目模板。

## 贡献题库

题库文件放在 `data/templates/`。

新增模板前请确认：

- 知识点已存在于 `data/curriculum/knowledge_map.json`。
- 模板有唯一 `id` 和明确 `version`。
- 模板包含年级、学期、模块、知识点、难度、题型。
- 模板包含 `parameters`、`answer_rule` 和 `solution_template`。
- 题目为自制题、变式题或明确可开源内容。

运行覆盖率检查：

```bash
python scripts/check_coverage.py
```

## 不应提交

- `.env`
- SQLite 数据库
- 学生答题记录
- 日志和备份
- `node_modules/`
- `.venv/`
- `dist/`

## 代码贡献

第一阶段保持小步稳定推进：

- 不做无关大重构。
- 优先保留现有目录结构。
- 修改后更新 `project_status.md`。
- 面向后续开源维护，避免把私人路径、隐私数据、商业题库内容写入仓库。

## 题目质量方向

- 每个知识点逐步补齐多种题型。
- 不只做换数字模板。
- 高考部分重视专题题、综合题、变式题和压轴题风格。
- 解析要说明关键步骤，不能只有答案。
