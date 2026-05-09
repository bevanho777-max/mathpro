# MathPro

![CI](https://github.com/bevanho777-max/mathpro/actions/workflows/ci.yml/badge.svg)

MathPro 是一个面向中国初一到高三学生的数学刷题 WebUI。项目第一阶段服务于高二学生的日常练习，长期目标是作为可 clone、可部署、可贡献题库的开源项目持续演进。

## 核心原则

- 运行时不依赖本地大模型，也不依赖 OpenAI API。
- 出题、判题、解析主要依靠知识点地图、题目模板、数据库和程序逻辑。
- 题目必须绑定年级、章节、知识点，并具备答案、解析和可判题规则。
- 题库与代码分离，题库数据放在 `data/` 目录。
- 高考内容以自制仿真题、变式题、知识点拆解为主，避免大量收录商业题库或教辅原题。

## 技术栈

- 前端：Vite、React、TypeScript、TailwindCSS、KaTeX
- 后端：FastAPI、SQLAlchemy、Pydantic、SymPy
- 数据库：第一阶段 SQLite，后续预留 PostgreSQL
- 部署：Docker Compose，默认端口 `18080`

## 快速开始

```bash
docker compose up -d --build
```

访问：

- 本机：`http://localhost:18080`
- 局域网：`http://服务器IP:18080`
- 健康检查：`http://localhost:18080/api/health`

## 开发环境启动

后端建议使用 Python 3.12。当前依赖版本不建议使用 Python 3.14 创建虚拟环境，否则 `pydantic-core` 可能尝试源码编译并安装失败。

后端：

```powershell
cd backend
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

前端：

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## 覆盖率检查

```bash
python scripts/check_coverage.py
```

脚本会读取 `data/curriculum/knowledge_map.json` 和 `data/templates/*.json`，统计每个知识点已有模板数量。

## 题库质量校验

```bash
python scripts/validate_templates.py
python scripts/validate_templates.py --strict
```

脚本会扫描 `data/templates/*.json`，检查模板 ID、必填字段、知识点绑定、参数渲染、答案规则、难度、题型和常见 LaTeX 格式问题。普通模式下只有严重错误会返回非 0 退出码；`--strict` 会把警告也视为失败。

## 后端测试

```bash
cd backend
pytest
```

测试使用临时 SQLite 数据库，不会写入 `local_data/mathpro.sqlite3`。当前覆盖健康检查、年级接口、随机出题、判题、答题记录和错题本软移除流程。

## CI 自动检查

项目已接入 GitHub Actions。每次 push 和 pull request 会自动运行后端依赖安装、Python 编译检查、后端 pytest、题库严格校验、覆盖率检查、前端依赖安装和前端生产构建。

## 项目结构

```text
mathpro/
├─ frontend/
├─ backend/
├─ data/
│  ├─ curriculum/
│  ├─ templates/
│  ├─ examples/
│  ├─ exams/
│  └─ imports/
├─ scripts/
├─ docs/
├─ docker-compose.yml
├─ .env.example
├─ .gitignore
├─ README.md
├─ LICENSE
└─ project_status.md
```

## 文档

- [部署说明](docs/deploy.md)
- [题库格式](docs/question_format.md)
- [知识点地图](docs/curriculum_map.md)
- [贡献指南](docs/contribute.md)

## License

MIT License
