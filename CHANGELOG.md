# Changelog

所有重要变更都记录在这里。

## Unreleased

* 第五阶段 E：补充后端 API 边界测试，并为 `/api/problem/random` 增加可选知识点过滤。
* 第五阶段 D：新增后端 API pytest 自动化测试，并接入 GitHub Actions CI。
* 第五阶段 C：新增 GitHub Actions CI，在 push 和 pull request 时自动运行后端编译、题库校验、覆盖率检查和前端构建。
* 第五阶段 B：新增 `scripts/validate_templates.py` 题库质量校验脚本，并修复示例模板中的 LaTeX 不等号写法。
* 第五阶段 A：新增 `data/templates/high2_high3_templates.json`，补充 87 个高二/高三自制题目模板，使高三可以开始正常出题。
* 第四阶段 C：前端新增轻量“错题本”入口，可查看错题、显示解析和移除错题。
* 调整年级可见性：`/api/grades` 恢复返回完整课程年级，高三等暂无模板年级保持可见，并由前端显示暂无题目提示。
* 修复无题目模板范围出题时的错误体验：筛选接口只返回已有模板覆盖范围，前端显示中文友好提示而不是原始 JSON。
* 第四阶段 B：新增 `wrong_book` 错题本表，答错时自动记录或更新错题，新增 `GET /api/wrong-book` 和 `POST /api/wrong-book/remove`。
* 第四阶段 A：新增 `user_answers` 答题记录表，提交答案时保存记录，并新增 `GET /api/answers/recent` 查询最近答题记录。
* 第三阶段：新增 SQLite 数据库配置和 `generated_problems` 表，生成题目时持久化 `problem_id` 与判题规则，判题时从 SQLite 查询，不再依赖内存字典。
* 第二阶段加固：前端题目流程继续由后端 API 驱动，提交答案时改为回传 `problem_id`，后端根据已生成题目的判题规则检查答案，不再要求前端回传 `answer_rule`。
* 统一平方根模板为标准 LaTeX 单层花括号形式，例如 `\\sqrt{x-{a}}` 和 `\\sqrt{ab}`。
* 修复题库模板中平方根公式的 LaTeX 写法，确保 `\\sqrt{...}` 可由 KaTeX 正确渲染。
* 增强填空题文本判题归一化，支持 `x>=6`、`x ≥ 6`、`x大于等于6` 等答案写法。
* 完成本地 Git 首次提交并推送到 GitHub 仓库 `bevanho777-max/mathpro`。
* 更新 `.gitignore`，忽略 TypeScript/Vite 构建产物。
* 明确后端本地开发使用 Python 3.12，新增 `.python-version`，并更新后端启动文档，避免 Python 3.14 安装 `pydantic-core` 失败。
* 实现第一版刷题 WebUI：年级、章节、知识点选择，出题，答题，判题，解析和下一题。
* 更新前端基础样式，改善表单控件和 KaTeX 显示。
* 修复前端 TypeScript 构建配置，新增 `frontend/package-lock.json` 和 `react-katex` 本地类型声明。
* 初始化 AI 项目记忆机制。
* 新增 `AI_CONTEXT.md`，保存项目长期规则。
* 新增 `NEXT_TASK.md`，保存下次继续工作的任务。
* 新增 `docs/dev_workflow.md`，保存开发协作流程。
* 更新 `project_status.md`，补充当前状态、结构、运行方式、问题和下一步计划。
