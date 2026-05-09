# MathPro Project Status

更新时间：2026-05-08

## 当前阶段

第一阶段：项目基础骨架。

## 已完成

- 创建推荐目录结构。
- 创建 README、MIT License、`.env.example`、`.gitignore`。
- 创建 Docker Compose 部署骨架，默认前端端口 `18080`。
- 创建 FastAPI 后端基础结构。
- 实现 `/api/health` 健康检查。
- 初步实现年级、模块、知识点、随机题、指定知识点出题、答案检查、覆盖率 API。
- 创建 Vite React TypeScript 前端基础结构。
- 接入 TailwindCSS 和 KaTeX 依赖。
- 创建知识点地图 `data/curriculum/knowledge_map.json`，覆盖初一到高三主要数学知识点。
- 创建示例模板 `data/templates/sample_templates.json`，覆盖初一、初二、初三、高一、高二各 10 个模板。
- 创建覆盖率检查脚本 `scripts/check_coverage.py`。
- 创建部署、题库格式、知识点地图、贡献说明文档。

## 当前限制

- 前端只是基础状态页，不包含完整刷题流程。
- 后端尚未接入数据库持久化。
- 判题规则仍是第一阶段轻量实现。
- 覆盖率只统计模板数量，不评价题型丰富度和难度梯度。

## 下一阶段建议

1. 实现第一版刷题 WebUI：年级、章节、知识点选择，随机出题，提交答案，显示解析，下一题。
2. 为后端补充数据库模型和 SQLite 初始化流程。
3. 扩展判题规则，支持区间、集合、选择题、多答案表达式。
4. 将模板导入数据库，并保留 JSON 作为题库源数据。
5. 增加基础自动化测试和 CI 配置。

## 2026-05-08 更新

- 新增 `AI_CONTEXT.md`，用于保存项目长期规则、技术栈、题库原则、开源隐私规则和开发协作规则。
- 新增 `NEXT_TASK.md`，用于保存下次继续工作的入口文件、当前判断和下一阶段建议任务。
- 约定以后每次完成阶段性修改后，必须同时更新 `project_status.md` 和 `NEXT_TASK.md`。

## 当前阶段

项目初始化阶段。

## 已完成内容

- 已创建推荐项目结构：`frontend/`、`backend/`、`data/`、`scripts/`、`docs/`。
- 已创建 README、MIT License、`.env.example`、`.gitignore`。
- 已创建 `docker-compose.yml`，默认通过前端容器暴露 `18080` 端口。
- 已创建 FastAPI 后端基础结构和 `backend/app/main.py`。
- 已实现 `/api/health`、年级、章节、知识点、随机题、按知识点出题、答案检查、覆盖率统计等基础 API。
- 已创建 Vite React TypeScript 前端基础结构。
- 已接入 TailwindCSS 和 KaTeX 相关依赖。
- 已创建 `data/curriculum/knowledge_map.json`，覆盖初一到高三主要数学知识点。
- 已创建 `data/templates/sample_templates.json`，初一、初二、初三、高一、高二各 10 个示例模板。
- 已创建 `scripts/check_coverage.py`，用于检查知识点模板覆盖情况。
- 已创建部署、题库格式、知识点地图、贡献说明文档。
- 已建立 AI 项目记忆机制：`AI_CONTEXT.md`、`NEXT_TASK.md`、`CHANGELOG.md`、`docs/dev_workflow.md`。

## 当前项目结构

```text
mathpro/
├─ frontend/
│  ├─ src/
│  ├─ Dockerfile
│  ├─ nginx.conf
│  ├─ package.json
│  └─ vite.config.ts
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py
│  │  └─ main.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ data/
│  ├─ curriculum/
│  │  └─ knowledge_map.json
│  ├─ templates/
│  │  └─ sample_templates.json
│  ├─ examples/
│  ├─ exams/
│  └─ imports/
├─ scripts/
│  └─ check_coverage.py
├─ docs/
│  ├─ contribute.md
│  ├─ curriculum_map.md
│  ├─ deploy.md
│  ├─ dev_workflow.md
│  └─ question_format.md
├─ AI_CONTEXT.md
├─ NEXT_TASK.md
├─ CHANGELOG.md
├─ README.md
├─ LICENSE
├─ docker-compose.yml
├─ .env.example
├─ .gitignore
└─ project_status.md
```

## 当前运行方式

Docker 方式：

```bash
docker compose up -d --build
```

访问：

- `http://localhost:18080`
- `http://localhost:18080/api/health`

开发方式：

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

覆盖率检查：

```bash
python scripts/check_coverage.py
```

## 当前问题

- 前端目前仍是基础状态页，还没有完整刷题流程。
- 后端尚未接入数据库持久化。
- 判题规则仍是第一阶段轻量实现。
- 覆盖率脚本只统计模板数量，不评价题型丰富度和难度梯度。
- 当前工作区存在 Python 运行生成的 `__pycache__/` 文件；`.gitignore` 已忽略，后续提交前应确认不纳入 Git。

## 下一步计划

1. 实现第一版刷题 WebUI：年级选择、章节选择、知识点选择、随机出题、提交答案、显示解析、下一题。
2. 保持前端实现小范围修改，优先修改 `frontend/src/App.tsx` 和 `frontend/src/styles.css`。
3. 如接口不够用，再小范围调整 `backend/app/main.py`。
4. 完成阶段任务后更新 `project_status.md`、`NEXT_TASK.md` 和 `CHANGELOG.md`。

## Next AI Handoff

下次重新打开 VSCode 后，请先读取：

1. AI_CONTEXT.md
2. project_status.md
3. NEXT_TASK.md
4. README.md
5. docs/dev_workflow.md

然后再继续开发。

## 2026-05-08 更新：第一版刷题 WebUI

- 已将 `frontend/src/App.tsx` 从基础状态页升级为第一版刷题 WebUI。
- 前端现在可以调用后端 API 获取年级、章节和知识点。
- 支持按知识点出题，也支持当前年级章节范围内随机出题。
- 支持输入答案、提交判题、显示正确或错误、显示解析、进入下一题。
- `frontend/src/styles.css` 增加了基础表单控件和 KaTeX 显示样式。
- 本阶段仍未接入数据库持久化，题目仍由 `data/templates/*.json` 模板驱动。

## 当前阶段结论

第一阶段基础骨架和第一版刷题 WebUI 已完成。项目现在可以继续进入第二阶段前的加固工作：本地启动验证、修正构建问题、补充基础测试，然后再进入数据库和错题本等功能。

## 2026-05-08 验证记录

- 已运行 `python scripts/check_coverage.py --min-count 0`，脚本通过，当前知识点 105 个，模板 50 个。
- 已运行 `python -m compileall backend scripts`，Python 文件编译检查通过。
- 已运行 `npm install`，生成 `frontend/package-lock.json`，前端依赖无安全漏洞报告。
- 已运行 `npm run build`，前端 TypeScript 和 Vite 生产构建通过。
- 已新增 `frontend/src/react-katex.d.ts`，为 `react-katex` 补充本地类型声明。
- 已调整 `frontend/tsconfig.json`、`frontend/tsconfig.node.json` 和 `frontend/package.json`，修复 Vite 6 构建所需的 TypeScript 配置和 Node 类型。
- 当前机器未检测到 `docker` 命令，因此尚未在本机验证 `docker compose up -d --build`。

## 2026-05-08 后端本地环境修正

- 发现当前 Windows 环境只有 Python 3.14，使用它创建 `.venv` 时，`pydantic-core==2.27.2` 会尝试源码编译，并因缺少可用 `maturin` 构建依赖而安装失败。
- 明确本项目当前后端本地开发目标为 Python 3.12，与 `backend/Dockerfile` 中的 `python:3.12-slim` 保持一致。
- 新增 `.python-version`，内容为 `3.12`。
- 更新 `backend/requirements.txt` 注释，说明当前依赖建议使用 Python 3.12。
- 更新 `README.md` 和 `docs/deploy.md` 的 Windows PowerShell 后端启动命令，改为 `py -3.12 -m venv .venv` 和 `python -m uvicorn ...`。
- 已验证当前机器执行 `py -3.12 --version` 会提示未找到合适的 Python 运行时；需要先安装 Python 3.12 后再重建后端 `.venv`。

## 2026-05-08 GitHub 同步记录

- 已在本地 Git 仓库配置用户名 `bevanho777-max` 和邮箱 `bevanho777@gmail.com`。
- 已创建首个提交 `Initial MathPro project scaffold`。
- 已绑定远程仓库 `https://github.com/bevanho777-max/mathpro.git`。
- 已成功推送 `main` 分支到 GitHub。
- 已更新 `.gitignore`，避免提交 TypeScript/Vite 构建产物：`*.tsbuildinfo`、`frontend/vite.config.js`、`frontend/vite.config.d.ts`。

## 2026-05-08 第一阶段收尾验收

- 已修复题库模板中的 `sqrt(...)` 普通文本，改为 LaTeX：`\\sqrt{...}`。
- 已将相关解析中的不等号改为 LaTeX：`\\ge`。
- 前端题目和解析仍通过 KaTeX 渲染 `$...$` 内的 LaTeX。
- 已增强后端 `contains:` 判题的文本归一化，支持 `x>=6`、`x ≥ 6`、`x大于等于6` 等常见写法。
- 已验证错误答案 `x>5` 不会被误判为 `x>=6`。
- 已运行模板 JSON 检查、覆盖率检查、后端编译检查和前端 `npm run build`，均通过。

## 2026-05-08 第二阶段 API 驱动加固

- 已确认前端没有内置题库模拟数据，年级、章节、知识点、出题和判题都通过后端 `/api/*` 接口完成。
- 已将前端提交答案逻辑从回传 `answer_rule` 调整为回传 `problem_id`。
- 后端生成题目时会临时登记该题目的判题规则，并在 `/api/answer/check` 中根据 `problem_id` 完成判题。
- 题库模板仍然保存在 `data/templates/*.json`，前端不直接读取题库文件。
- 当前 `problem_id` 判题记录为后端进程内存态，适合本地开发和第一版刷题流程；后续进入 SQLite 阶段后应持久化到 `generated_problems` 表。
- 已将平方根模板统一为标准 LaTeX 单层花括号形式，例如 `\\sqrt{x-{a}}`、`\\sqrt{{a}^2}` 和 `\\sqrt{ab}`。

## 2026-05-08 第三阶段 SQLite 生成题记录

- 已新增 SQLite 数据库配置，默认数据库路径为 `./local_data/mathpro.sqlite3`。
- 数据库路径可通过环境变量 `MATHPRO_DATABASE_PATH` 覆盖，也保留 `MATHPRO_DATABASE_URL` 作为后续扩展入口。
- `.env.example` 和 `docker-compose.yml` 已统一使用 `MATHPRO_DATABASE_PATH`。
- 已新增 `generated_problems` 表模型，保存 `problem_id`、模板信息、题面、判题规则、解析和创建时间。
- 后端生成题目时会把生成结果写入 SQLite。
- `/api/answer/check` 现在根据 `problem_id` 从 SQLite 查询 `answer_rule`，不再依赖内存字典判题。
- 前端 UI 和 API 路径保持不变。
- `local_data/` 和 `*.sqlite3` 已被 `.gitignore` 忽略，数据库文件不会提交到 GitHub。
- 已验证后端编译检查、前端 `npm run build`、覆盖率检查、HTTP 出题和提交答案均通过。
- 已用独立 Python 进程模拟后端重启后的旧 `problem_id` 判题，确认可从 SQLite 查询并判题成功。

## 2026-05-09 第四阶段 A 答题记录

- 已新增 `user_answers` 表模型，用于保存每次提交答案的记录。
- `user_answers.problem_id` 通过外键关联 `generated_problems.problem_id`。
- `/api/answer/check` 判题后会写入答题记录，保存题目元数据、原始答案、归一化答案和是否正确。
- `/api/answer/check` 保持原有 `correct` 字段，并额外返回 `answer_recorded: true`。
- 已新增 `GET /api/answers/recent`，默认返回最近 20 条答题记录，支持 `limit` 参数，当前限制为 1 到 100。
- 本阶段未新增错题本、用户系统或前端页面。
- 已验证自动建表、提交答案写入 `user_answers`、`GET /api/answers/recent?limit=5`、后端编译检查、覆盖率脚本和前端 `npm run build` 均通过。

## 2026-05-09 第四阶段 B 错题本

- 已新增 `wrong_book` 表模型，用于保存答错题目。
- `/api/answer/check` 判题错误时会自动写入或更新错题本。
- 同一个 `problem_id` 重复答错不会重复插入，会增加 `wrong_count`，并更新 `last_wrong_answer` 和 `last_wrong_at`。
- 如果已移除的同题再次答错，会重新标记为 `removed=false`。
- 同题后来答对不会自动移除错题。
- `/api/answer/check` 保持 `correct` 和 `answer_recorded` 字段，并额外返回 `wrong_recorded`。
- 已新增 `GET /api/wrong-book`，默认只返回 `removed=false` 的错题，支持 `limit`、`grade` 和 `knowledge_point` 参数。
- 已新增 `POST /api/wrong-book/remove`，按 `problem_id` 将错题标记为 `removed=true`，不物理删除。
- 本阶段未新增用户系统或前端页面。
- 已验证自动建表、重复答错 `wrong_count` 增加、错题查询、按 `problem_id` 软移除、默认查询排除已移除错题、后端编译检查、覆盖率脚本和前端 `npm run build` 均通过。
