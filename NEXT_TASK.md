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
