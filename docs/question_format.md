# 题库格式说明

MathPro 第一阶段使用 JSON 文件维护题目模板。题库文件放在 `data/templates/`，代码不直接写死题目。

## 文件结构

推荐每个模板文件使用对象格式：

```json
{
  "file_version": "0.1.0",
  "description": "文件说明",
  "templates": []
}
```

`templates` 是题目模板数组。

## 模板字段

每个模板必须包含：

| 字段 | 说明 |
| --- | --- |
| `id` | 全局唯一模板 id |
| `version` | 模板版本号，例如 `1.0.0` |
| `grade` | 年级，例如 `高二` |
| `semester` | 学期，例如 `上`、`下`、`全年` |
| `module` | 章节或模块，例如 `函数` |
| `knowledge_point` | 知识点名称，必须存在于知识点地图 |
| `difficulty` | 难度，建议 1 到 5 |
| `question_type` | 题型，例如 `填空题`、`选择题`、`解答题` |
| `source_type` | 来源类型，例如 `template`、`variant`、`self_made` |
| `tags` | 标签数组 |
| `parameters` | 参数定义 |
| `question_template` | 题干模板 |
| `answer_rule` | 判题规则 |
| `solution_template` | 解析模板 |

## 参数格式

当前支持整数参数：

```json
{
  "a": {
    "type": "integer",
    "min": -5,
    "max": 5,
    "exclude": [0]
  }
}
```

题干、答案规则、解析中可使用 `{a}` 引用参数。

## 判题规则

第一阶段支持轻量规则：

| 规则 | 示例 | 说明 |
| --- | --- | --- |
| `exact:` | `exact:A` | 完全匹配 |
| `contains:` | `contains:x!=2` | 答案包含指定文本 |
| `numeric:` | `numeric:3` | 数值匹配 |
| `sympy:` | `sympy:2*x+1` | 使用 SymPy 判断表达式等价 |

后续会扩展区间、集合、选择题多选、步骤判分等规则。

## 示例

```json
{
  "id": "g10_function_domain_001",
  "version": "1.0.0",
  "grade": "高一",
  "semester": "上",
  "module": "函数",
  "knowledge_point": "函数的定义域",
  "difficulty": 1,
  "question_type": "填空题",
  "source_type": "template",
  "tags": ["函数", "定义域"],
  "parameters": {
    "a": { "type": "integer", "min": -5, "max": 5, "exclude": [0] }
  },
  "question_template": "求函数 $f(x)=1/(x-{a})$ 的定义域。",
  "answer_rule": "contains:x!={a}",
  "solution_template": "分母不能为 0，所以 $x-{a}≠0$，因此 $x≠{a}$。"
}
```

## 质量要求

- 不能让 AI 随机生成并直接入库。
- 每道题必须绑定明确年级和知识点。
- 每道题必须有答案、解析和可判题规则。
- 每个知识点应逐步沉淀多种题型，不只做换数字。
- 高考内容应优先自制仿真题、变式题、综合题和知识点拆解题。
