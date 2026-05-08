# MathPro AI Context

本文档保存 MathPro 项目的长期规则，供每次重新打开 VSCode 或继续开发时快速恢复上下文。

## 项目目标

MathPro 是一个面向中国初一到高三学生的数学刷题 WebUI。

初始用途是给高二学生使用。
长期目标是开源到 GitHub，方便其他人部署和使用。

## 开发方式

项目开发使用 VSCode + ChatGPT Plus。
项目运行时不依赖本地大模型。
项目运行时不依赖 OpenAI API。

## 技术栈

前端：

* Vite
* React
* TypeScript
* TailwindCSS
* KaTeX 或 MathJax

后端：

* FastAPI
* SQLAlchemy
* Pydantic
* SymPy

数据库：

* 第一阶段使用 SQLite
* 后续预留 PostgreSQL

部署：

* Docker Compose
* 支持 IP 访问
* 支持后续域名反向代理访问

## 核心原则

1. 题库和代码必须分离。
2. 题库放在 data 目录。
3. 不允许只靠 AI 随机生成题。
4. 题目必须绑定年级、章节、知识点。
5. 题目必须有答案。
6. 题目必须有解析。
7. 题目必须可判题。
8. 不允许 AI 自己猜题目属于哪个年级。
9. 高考内容以自制仿真题、变式题和知识点拆解为主。
10. 不大量收录商业题库、教辅原题或不明确版权的题目。
11. 不提交 .env。
12. 不提交数据库文件。
13. 不提交孩子答题记录。
14. 不提交日志和备份。
15. 每次修改后必须更新 project_status.md。
16. 每次阶段完成后必须更新 NEXT_TASK.md。
17. 需要给用户复制文件时，尽量给完整可替换版本，不只给片段。

## GitHub 开源要求

1. 项目要适合公开发布。
2. 使用 MIT License。
3. README.md 要写清楚快速开始。
4. docs/deploy.md 要写清楚部署方式。
5. docs/question_format.md 要写清楚题库格式。
6. docs/contribute.md 要写清楚贡献方式。
7. .gitignore 必须完整。
8. 隐私数据不得提交到 GitHub。

## 项目定位

MathPro 是一个面向中国初一到高三学生的数学刷题 WebUI。

初始用途是先给一名正在读高二的学生使用；长期目标是发布到 GitHub 开源，让有需要的人可以 clone、部署、使用和贡献题库。

## 长期原则

1. 项目运行时不依赖本地大模型。
2. 项目运行时不依赖 OpenAI API。
3. AI 只作为开发辅助和题库模板扩展辅助。
4. 出题、判题、解析主要依靠知识点地图、题目模板、数据库和程序逻辑。
5. 不允许只靠 AI 随机生成数学题。
6. 题目必须先绑定年级、章节、知识点，再生成。
7. 每一道题都必须有明确年级、明确知识点、答案、解析和可判题规则。
8. 不能让 AI 自己猜题目属于哪个年级。
9. 不能只做换数字题库。
10. 每个知识点必须逐步沉淀多种题型。
11. 高考部分要重视专题题、综合题、变式题和压轴题风格。
12. 高考题库不要直接大量收录商业题库或教辅原题，应以自制仿真题、变式题和知识点拆解为主。

## 技术栈

前端：

- Vite
- React
- TypeScript
- TailwindCSS
- KaTeX 或 MathJax

后端：

- FastAPI
- SQLAlchemy
- Pydantic
- SymPy

数据库：

- 第一阶段 SQLite
- 后续预留 PostgreSQL 迁移能力

部署：

- Docker Compose
- 默认端口建议使用 `18080`
- 支持本地 IP 访问
- 支持后续通过域名反向代理访问

## 数据和题库规则

1. 题库和代码必须分离。
2. 题库放在 `data/` 目录。
3. 题库支持 JSON 导入。
4. 题库模板必须有版本号和唯一 id。
5. 每个模板必须绑定 `grade`、`semester`、`module`、`knowledge_point`、`difficulty`、`question_type`。
6. 每个模板必须有 `parameters`、`answer_rule`、`solution_template`。
7. 每个模板必须标记 `source_type`。
8. 每次扩展题库后，应运行 `python scripts/check_coverage.py` 检查覆盖率。

## 开源和隐私规则

1. 项目要适合公开发布。
2. 使用 MIT License。
3. 不提交 `.env`。
4. 不提交 SQLite 数据库。
5. 不提交孩子答题记录。
6. 不提交日志、备份、隐私数据。
7. 不提交 `node_modules/`、`.venv/`、`dist/`。

## 开发协作规则

1. 先检查当前项目结构和状态。
2. 不要大范围重构。
3. 优先小步稳定推进。
4. 每次只完成一个阶段。
5. 修改代码前先说明准备修改哪些文件。
6. 修改完成后说明新增和修改了哪些文件。
7. 每次完成阶段性修改后，必须更新 `project_status.md` 和 `NEXT_TASK.md`。
8. 不要只给片段。
9. 需要手动替换文件时，必须给完整可替换版本。

## 当前优先级

根据 `project_status.md`，下一步优先实现第一版刷题 WebUI：

1. 年级选择
2. 章节选择
3. 知识点选择
4. 随机出题
5. 提交答案
6. 判断正确或错误
7. 显示解析
8. 下一题
9. 移动端和 PC 端适配
