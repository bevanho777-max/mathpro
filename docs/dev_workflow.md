# MathPro Development Workflow

## 每次开始开发

1. 先读取 AI_CONTEXT.md。
2. 再读取 project_status.md。
3. 再读取 NEXT_TASK.md。
4. 总结当前项目状态。
5. 说明准备修改哪些文件。
6. 再开始修改。

## 每次完成修改

1. 更新 project_status.md。
2. 如果完成阶段任务，更新 NEXT_TASK.md。
3. 如果有重要改动，更新 CHANGELOG.md。
4. 输出新增文件列表。
5. 输出修改文件列表。
6. 输出启动或测试命令。

## 代码修改原则

1. 不要大范围重构。
2. 优先小步推进。
3. 不要删除已有内容。
4. 不要只给片段。
5. 需要用户手动替换时，给完整可替换版本。
6. 保持题库和代码分离。
7. 保持项目适合 GitHub 开源。

## 记忆文件分工

- `AI_CONTEXT.md`：保存长期项目规则，通常只在原则变化时更新。
- `project_status.md`：保存当前项目状态，每次完成代码修改后必须更新。
- `NEXT_TASK.md`：保存下一次继续工作的任务，每次阶段任务完成后必须更新。
- `CHANGELOG.md`：保存重要变更记录，重要改动完成后必须更新。

## 建议交接话术

重新打开 VSCode 后，可以对 AI 说：

```text
请继续 mathpro 项目。请先读取 AI_CONTEXT.md、project_status.md、NEXT_TASK.md、README.md 和 docs/dev_workflow.md，然后总结当前状态，说明准备修改哪些文件，再继续下一步。
```
