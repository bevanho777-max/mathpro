# Changelog

所有重要变更都记录在这里。

## Unreleased

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
