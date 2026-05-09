# NEXT_TASK

更新时间：2026-05-08

## 下次继续工作前先读

1. `AI_CONTEXT.md`
2. `project_status.md`
3. `README.md`
4. `docs/deploy.md`
5. `docs/question_format.md`
6. `docker-compose.yml`
7. `backend/app/main.py`
8. `frontend/package.json`

## 当前判断

项目基础骨架已经完成：

- 目录结构已创建。
- README、License、部署配置、环境变量示例和 Git 忽略规则已创建。
- FastAPI 后端基础 API 已创建。
- Vite React TypeScript 前端基础结构已创建。
- 知识点地图已覆盖初一到高三主要知识点。
- 示例题库模板已覆盖初一、初二、初三、高一、高二各 10 个。
- 覆盖率检查脚本已创建并可运行。

## 下一阶段建议任务

实现第一版刷题 WebUI，不做复杂 UI，重点让核心刷题流程跑通：

1. 前端调用 `/api/grades` 获取年级。
2. 选择年级后调用 `/api/modules` 获取章节。
3. 选择章节后调用 `/api/knowledge-points` 获取知识点。
4. 选择知识点后调用 `/api/problem/by-knowledge` 出题。
5. 没有指定知识点时，可调用 `/api/problem/random` 随机出题。
6. 用户提交答案后调用 `/api/answer/check`。
7. 前端显示正确或错误。
8. 前端显示解析。
9. 支持下一题。
10. 保持移动端和 PC 端基础适配。

## 建议准备修改的文件

下一阶段如果开始实现刷题 WebUI，建议小范围修改：

- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `project_status.md`
- `NEXT_TASK.md`

如果发现后端接口返回值不够用，再小范围修改：

- `backend/app/main.py`

## 2026-05-08 阶段完成记录

第一版刷题 WebUI 已完成。下次继续时建议先做验证和加固，不急着进入复杂功能。

建议下一步：

1. 安装前端依赖并运行 `npm run build`，确认 Vite React TypeScript 构建通过。
2. 安装后端依赖并运行 FastAPI，本地访问 `/api/health`、`/api/grades`、`/api/problem/random`。
3. 如果本机有 Docker，运行 `docker compose up -d --build` 验证 `http://localhost:18080`。
4. 修复验证中发现的问题。
5. 之后再进入第二阶段：SQLite 持久化、答题记录、错题本、掌握统计。

建议准备修改的文件：

- `frontend/src/App.tsx`（仅在构建或交互验证发现问题时修改）
- `backend/app/main.py`（仅在 API 验证发现问题时修改）
- `project_status.md`
- `NEXT_TASK.md`
- `CHANGELOG.md`

## 2026-05-08 验证后下一步

已完成：

1. 前端依赖安装。
2. 前端生产构建验证。
3. 覆盖率脚本验证。
4. Python 编译检查。

下次建议继续：

1. 安装后端依赖并启动 FastAPI，实际访问 `/api/health`、`/api/grades`、`/api/problem/random`。
2. 如果本机安装 Docker，运行 `docker compose up -d --build` 验证容器启动和 `http://localhost:18080`。
3. 用浏览器手动检查刷题页面：选择高二、章节、知识点，出题，提交答案，显示解析，下一题。
4. 若验证通过，再规划第二阶段：SQLite 持久化、答题记录、错题本。

## 2026-05-08 后端环境问题处理后下一步

当前机器只检测到 Python 3.14。后端依赖安装失败不是业务代码问题，而是本地 Python 版本不匹配。

下次继续建议：

1. 安装 Python 3.12。
2. 确认 `py -3.12 --version` 能输出 Python 3.12.x。
3. 在 `backend/` 删除旧 `.venv` 后，重新运行：

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. 访问 `http://localhost:8000/api/health`、`http://localhost:8000/api/grades`、`http://localhost:8000/api/problem/random`。
5. 后端本地验证通过后，再继续 Docker 验证或第二阶段规划。

## 2026-05-08 Git 同步后下一步

项目已经推送到 GitHub：`https://github.com/bevanho777-max/mathpro.git`。

以后每次完成修改后，建议执行：

```powershell
git status
git add .
git commit -m "说明本次修改"
git push
```

提交前确认 `.env`、数据库、日志、备份、`node_modules/`、`dist/`、`.venv/` 和学生答题记录没有进入暂存区。

## 2026-05-08 第一阶段收尾后下一步

第一阶段本地开发模式已基本验收通过：

1. 前端页面可显示题目、提交答案、显示正确结果和解析。
2. 题库模板中的平方根公式已改为 LaTeX。
3. `x>=6`、`x ≥ 6`、`x大于等于6` 均可识别为正确答案。
4. `npm run build` 已通过。

下次建议：

1. 手动在浏览器再抽测 3 到 5 道不同年级和章节的题。
2. 如果体验稳定，将本次收尾修复提交并推送到 GitHub。
3. 之后进入第二阶段前，先规划 SQLite 数据模型、答题记录和错题本。

## 2026-05-08 第二阶段 API 驱动加固后下一步

已完成：

1. 确认前端没有题库模拟数据。
2. 前端通过后端 API 获取年级、章节、知识点和题目。
3. 提交答案时前端回传 `problem_id`，后端根据已生成题目的判题规则判题。
4. 前端不再依赖或回传 `answer_rule`。

下次建议：

1. 运行前端 `npm run build` 和后端 API 抽测。
2. 手动在浏览器测试高二题目流程：出题、提交正确答案、提交错误答案、查看解析、下一题。
3. 开始设计 SQLite 数据模型：`generated_problems`、`user_answers`、`wrong_book`。
4. 将当前内存态 `problem_id` 记录迁移为数据库记录。

## 2026-05-08 第三阶段 SQLite 生成题记录后下一步

已完成：

1. 新增 SQLite 配置和 `generated_problems` 表。
2. 生成题目时保存 `problem_id`、题面、解析和判题规则。
3. 判题时从 SQLite 查询 `answer_rule`。
4. 后端不再依赖内存字典保存已生成题目的判题规则。

下次建议：

1. 手动重启后端，使用重启前生成的 `problem_id` 再次调用 `/api/answer/check`。
2. 浏览器抽测高二刷题流程，确认前端交互无变化。
3. 进入下一阶段前先设计 `user_answers` 和 `wrong_book`，不要急着做用户系统。
4. 后续如果要支持 PostgreSQL，再补迁移工具和数据库 URL 配置说明。

## 2026-05-09 第四阶段 A 答题记录后下一步

已完成：

1. 新增 `user_answers` 表。
2. 每次 `/api/answer/check` 会保存答题记录。
3. 新增 `GET /api/answers/recent` 查询最近答题记录。
4. 暂未新增错题本、用户系统或前端页面。

下次建议：

1. 用浏览器完成几次答题，再调用 `/api/answers/recent` 检查记录。
2. 第四阶段 B 可以实现错题本：只记录错误答案，先不做用户系统。
3. 在做错题本前先确认 `user_answers` 字段是否足够支撑后续统计。

## 2026-05-09 第四阶段 B 错题本后下一步

已完成：

1. 新增 `wrong_book` 表。
2. 答错时自动写入或更新错题本。
3. 新增 `GET /api/wrong-book` 查询未移除错题。
4. 新增 `POST /api/wrong-book/remove` 软移除错题。
5. 暂未新增用户系统或前端页面。

下次建议：

1. 在浏览器里故意答错几道题，再用 `/api/wrong-book` 检查错题。
2. 第四阶段 C 可以做一个简单的错题本前端入口，先只读列表和移除。
3. 后续再考虑知识点掌握统计，不要急着引入用户体系。

## 2026-05-09 模板覆盖范围修复后下一步

已完成：

1. 后端年级接口保持完整课程年级可见。
2. 后端章节和知识点接口只返回已有模板覆盖的范围。
3. 高三等暂未覆盖模板的年级会显示为空范围提示。
4. 无模板范围出题时返回中文提示。
5. 前端会提取 JSON `detail`，不再直接显示原始错误 JSON。

下次建议：

1. 浏览器检查各年级下拉框，确认高三可见但显示暂无题目提示。
2. 继续补充缺失知识点模板，逐步减少覆盖率报告中的 0。
3. 第四阶段 C 再做轻量错题本前端入口。

## 2026-05-09 年级可见性修正后下一步

已完成：

1. `/api/grades` 恢复显示初一到高三完整年级。
2. 无模板范围出题时返回中文提示。
3. 前端在年级暂无可练习题目时显示友好提示。

下次建议：

1. 给高三先补一批基础模板，让高三不只是可见，也能开始刷题。
2. 继续保持无模板范围不静默跳题。
3. 后续再做错题本前端入口。

## 注意

- 不要引入复杂状态管理库。
- 不要接入运行时 AI。
- 不要把题库写死进前端。
- 不要把学生答题记录提交到仓库。
- 阶段性修改完成后，更新 `project_status.md` 和本文档。

## 下次继续时先做

1. 读取 AI_CONTEXT.md。
2. 读取 project_status.md。
3. 检查当前项目结构。
4. 不要直接大范围修改。
5. 先总结项目状态。
6. 再说明准备修改哪些文件。
7. 修改完成后更新 project_status.md。
8. 阶段任务完成后更新 NEXT_TASK.md。

## 当前下一步任务

继续第一阶段后半段：实现第一版刷题 WebUI。

重点完成：

1. 年级选择。
2. 章节选择。
3. 知识点选择。
4. 随机刷题。
5. 提交答案。
6. 判断正确或错误。
7. 显示解析。
8. 下一题。
9. 移动端和 PC 端基础适配。

建议先修改：

- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `project_status.md`
- `NEXT_TASK.md`

如果后端接口返回内容不够，再修改：

- `backend/app/main.py`
