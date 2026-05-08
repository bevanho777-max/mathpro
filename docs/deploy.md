# 部署说明

MathPro 第一阶段提供 Docker Compose 部署方式，默认通过 `18080` 端口访问。

## 准备

需要安装：

- Docker
- Docker Compose

本地开发后端时建议安装 Python 3.12。当前后端依赖版本不建议使用 Python 3.14 创建虚拟环境，否则 `pydantic-core` 可能尝试源码编译并安装失败。

复制环境变量示例：

```bash
cp .env.example .env
```

Windows PowerShell 可使用：

```powershell
Copy-Item .env.example .env
```

`.env` 不应提交到 GitHub。

## 一键启动

```bash
docker compose up -d --build
```

访问：

- `http://localhost:18080`
- `http://服务器IP:18080`
- `http://localhost:18080/api/health`

## 停止服务

```bash
docker compose down
```

## 数据目录

题库和课程地图位于：

- `data/curriculum/knowledge_map.json`
- `data/templates/*.json`

本地运行产生的数据库、日志、备份和答题记录不应提交到仓库。SQLite 默认预留在 `local_data/` 下，该目录已加入 `.gitignore`。

## 反向代理

后续可使用 Lucky、Nginx 或 Caddy 将域名反向代理到：

```text
http://服务器IP:18080
```

如果需要 HTTPS，建议在反向代理层统一申请和续期证书。

## 常见检查

查看容器状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs -f
```

重新构建：

```bash
docker compose up -d --build
```

## 本地后端开发

Windows PowerShell：

```powershell
cd backend
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

如果 `py -3.12` 提示找不到 Python 3.12，请先安装 Python 3.12，然后删除旧的 `.venv` 并重新执行上面的命令。
