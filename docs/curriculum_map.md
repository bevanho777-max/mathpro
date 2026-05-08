# 知识点地图说明

知识点地图位于 `data/curriculum/knowledge_map.json`。

## 设计目标

- 每道题必须先绑定年级、模块和知识点。
- 不让系统或 AI 猜测题目属于哪个年级。
- 支持覆盖率检查，便于发现题库薄弱知识点。
- 为后续章节专项训练、高考专题训练、自动组卷和统计分析打基础。

## 当前结构

```json
{
  "version": "0.1.0",
  "standards": [],
  "grades": [
    {
      "grade": "高二",
      "level": "senior",
      "modules": [
        {
          "name": "数列",
          "knowledge_points": [
            {
              "id": "g11_arithmetic_sequence",
              "name": "等差数列",
              "semester": "上"
            }
          ]
        }
      ]
    }
  ]
}
```

## 命名建议

- `id` 使用稳定英文标识，例如 `g11_arithmetic_sequence`。
- `name` 使用中文展示名，例如 `等差数列`。
- 模板中的 `grade`、`module`、`knowledge_point` 必须和地图中的中文名称一致。

## 课程范围

当前第一版覆盖：

- 初一、初二、初三主要数学知识点
- 高一、高二、高三主要高中数学模块
- 高考专题、综合题和压轴题方向

后续应继续细化到教材章节、小节、题型能力点和先修关系。
