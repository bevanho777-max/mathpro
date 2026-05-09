from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_MAP = REPO_ROOT / "data" / "curriculum" / "knowledge_map.json"
DEFAULT_TEMPLATE_DIR = REPO_ROOT / "data" / "templates"

REQUIRED_FIELDS = {
    "id",
    "version",
    "grade",
    "semester",
    "module",
    "knowledge_point",
    "difficulty",
    "question_type",
    "parameters",
    "question_template",
    "answer_rule",
    "solution_template",
}

RECOMMENDED_FIELDS = {"source_type", "tags"}
ALLOWED_QUESTION_TYPES = {"选择题", "填空题", "判断题", "解答题", "应用题", "计算题"}
ALLOWED_ANSWER_PREFIXES = {"exact", "contains", "numeric", "sympy"}
PLACEHOLDER_PATTERN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
MATH_SPAN_PATTERN = re.compile(r"\$([^$]*)\$")


@dataclass(frozen=True)
class Issue:
    severity: str
    file: str
    template_id: str
    message: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def relative_path(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def add_issue(issues: list[Issue], severity: str, file: str, template_id: str, message: str) -> None:
    issues.append(Issue(severity=severity, file=file, template_id=template_id, message=message))


def load_knowledge_index(path: Path, issues: list[Issue]) -> set[tuple[str, str, str]]:
    try:
        knowledge_map = load_json(path)
    except Exception as exc:
        add_issue(issues, "error", relative_path(path), "<knowledge_map>", f"cannot load JSON: {exc}")
        return set()

    valid_points: set[tuple[str, str, str]] = set()
    for grade in knowledge_map.get("grades", []):
        grade_name = grade.get("grade")
        for module in grade.get("modules", []):
            module_name = module.get("name")
            for point in module.get("knowledge_points", []):
                point_name = point.get("name")
                if grade_name and module_name and point_name:
                    valid_points.add((grade_name, module_name, point_name))

    if not valid_points:
        add_issue(issues, "error", relative_path(path), "<knowledge_map>", "no knowledge points found")
    return valid_points


def load_templates(template_dir: Path, issues: list[Issue]) -> list[dict[str, Any]]:
    templates: list[dict[str, Any]] = []
    if not template_dir.exists():
        add_issue(issues, "error", relative_path(template_dir), "<template_dir>", "template directory does not exist")
        return templates

    paths = sorted(template_dir.glob("*.json"))
    if not paths:
        add_issue(issues, "error", relative_path(template_dir), "<template_dir>", "no JSON template files found")
        return templates

    for path in paths:
        file_name = relative_path(path)
        try:
            payload = load_json(path)
        except Exception as exc:
            add_issue(issues, "error", file_name, "<file>", f"cannot load JSON: {exc}")
            continue

        items = payload.get("templates", payload) if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            add_issue(issues, "error", file_name, "<file>", "must contain a list or an object with templates")
            continue

        if not items:
            add_issue(issues, "warning", file_name, "<file>", "template file contains no templates")

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                add_issue(issues, "error", file_name, f"<item {index}>", "template item must be an object")
                continue
            item["_file"] = file_name
            item["_index"] = index
            templates.append(item)

    return templates


def sample_parameter_values(template: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    file_name = template.get("_file", "<unknown>")
    template_id = str(template.get("id", f"<item {template.get('_index', '?')}>"))
    parameters = template.get("parameters")
    values: dict[str, Any] = {}

    if not isinstance(parameters, dict):
        add_issue(issues, "error", file_name, template_id, "parameters must be an object")
        return values

    for name, spec in parameters.items():
        if not isinstance(name, str) or not name:
            add_issue(issues, "error", file_name, template_id, "parameter name must be a non-empty string")
            continue
        if not isinstance(spec, dict):
            add_issue(issues, "error", file_name, template_id, f"parameter {name} must be an object")
            continue

        parameter_type = spec.get("type")
        if parameter_type == "integer":
            if "min" not in spec or "max" not in spec:
                add_issue(issues, "error", file_name, template_id, f"integer parameter {name} needs min and max")
                continue
            try:
                minimum = int(spec["min"])
                maximum = int(spec["max"])
            except (TypeError, ValueError):
                add_issue(issues, "error", file_name, template_id, f"integer parameter {name} min/max must be numbers")
                continue
            if minimum > maximum:
                add_issue(issues, "error", file_name, template_id, f"integer parameter {name} min is greater than max")
                continue
            excluded = set(spec.get("exclude", []))
            candidates = [value for value in range(minimum, maximum + 1) if value not in excluded]
            if not candidates:
                add_issue(issues, "error", file_name, template_id, f"integer parameter {name} has no valid candidates")
                continue
            values[name] = candidates[0]
        else:
            if parameter_type not in {None, "string"}:
                add_issue(issues, "warning", file_name, template_id, f"parameter {name} uses unsupported type {parameter_type}")
            values[name] = spec.get("default", "")

    return values


def render_text(text: Any, values: dict[str, Any]) -> str:
    if not isinstance(text, str):
        raise TypeError("template text must be a string")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return str(values.get(key, match.group(0)))

    return PLACEHOLDER_PATTERN.sub(replace, text)


def check_rendered_text(
    template: dict[str, Any],
    field_name: str,
    values: dict[str, Any],
    issues: list[Issue],
) -> str:
    file_name = template.get("_file", "<unknown>")
    template_id = str(template.get("id", f"<item {template.get('_index', '?')}>"))
    try:
        rendered = render_text(template.get(field_name), values)
    except Exception as exc:
        add_issue(issues, "error", file_name, template_id, f"{field_name} cannot render: {exc}")
        return ""

    for name in values:
        if f"{{{name}}}" in rendered:
            add_issue(issues, "error", file_name, template_id, f"{field_name} still contains {{{name}}}")

    return rendered


def check_latex(template: dict[str, Any], field_name: str, text: str, issues: list[Issue]) -> None:
    file_name = template.get("_file", "<unknown>")
    template_id = str(template.get("id", f"<item {template.get('_index', '?')}>"))

    if text.count("$") % 2 != 0:
        add_issue(issues, "error", file_name, template_id, f"{field_name} has an unmatched dollar sign")

    if "sqrt(" in text:
        add_issue(issues, "error", file_name, template_id, f"{field_name} uses sqrt(...); use \\sqrt{{...}}")

    if re.search(r"\\sqrt(?!\s*\{)", text):
        add_issue(issues, "warning", file_name, template_id, f"{field_name} has \\sqrt without braces")

    for match in MATH_SPAN_PATTERN.finditer(text):
        math_text = match.group(1)
        if math_text.count("{") != math_text.count("}"):
            add_issue(issues, "error", file_name, template_id, f"{field_name} has unbalanced braces in LaTeX")
        if "≥" in math_text or "≤" in math_text or "≠" in math_text:
            add_issue(issues, "warning", file_name, template_id, f"{field_name} uses unicode inequality inside LaTeX")


def check_answer_rule(template: dict[str, Any], answer_rule: str, issues: list[Issue]) -> None:
    file_name = template.get("_file", "<unknown>")
    template_id = str(template.get("id", f"<item {template.get('_index', '?')}>"))
    if not answer_rule.strip():
        add_issue(issues, "error", file_name, template_id, "answer_rule is empty")
        return

    if ":" not in answer_rule:
        add_issue(issues, "warning", file_name, template_id, "answer_rule has no prefix")
        return

    prefix, value = answer_rule.split(":", 1)
    if prefix not in ALLOWED_ANSWER_PREFIXES:
        add_issue(issues, "warning", file_name, template_id, f"answer_rule uses unknown prefix {prefix}")
    if not value.strip():
        add_issue(issues, "error", file_name, template_id, "answer_rule value is empty")
    if prefix == "numeric":
        try:
            float(value)
        except ValueError:
            add_issue(issues, "error", file_name, template_id, "numeric answer_rule must render to a plain number")


def validate_template(
    template: dict[str, Any],
    valid_points: set[tuple[str, str, str]],
    issues: list[Issue],
) -> None:
    file_name = template.get("_file", "<unknown>")
    template_id = str(template.get("id", f"<item {template.get('_index', '?')}>"))

    missing = REQUIRED_FIELDS - set(template)
    if missing:
        add_issue(issues, "error", file_name, template_id, f"missing required fields: {sorted(missing)}")

    recommended_missing = RECOMMENDED_FIELDS - set(template)
    if recommended_missing:
        add_issue(issues, "warning", file_name, template_id, f"missing recommended fields: {sorted(recommended_missing)}")

    point_key = (template.get("grade"), template.get("module"), template.get("knowledge_point"))
    if None not in point_key and point_key not in valid_points:
        add_issue(
            issues,
            "error",
            file_name,
            template_id,
            f"unknown knowledge point: {point_key[0]} / {point_key[1]} / {point_key[2]}",
        )

    difficulty = template.get("difficulty")
    if not isinstance(difficulty, int) or isinstance(difficulty, bool) or difficulty < 1 or difficulty > 5:
        add_issue(issues, "error", file_name, template_id, "difficulty must be an integer from 1 to 5")

    question_type = template.get("question_type")
    if question_type not in ALLOWED_QUESTION_TYPES:
        add_issue(issues, "error", file_name, template_id, f"question_type is not allowed: {question_type}")

    values = sample_parameter_values(template, issues)
    rendered_question = check_rendered_text(template, "question_template", values, issues)
    rendered_solution = check_rendered_text(template, "solution_template", values, issues)
    rendered_answer_rule = check_rendered_text(template, "answer_rule", values, issues)

    check_latex(template, "question_template", rendered_question, issues)
    check_latex(template, "solution_template", rendered_solution, issues)
    check_answer_rule(template, rendered_answer_rule, issues)


def print_report(templates: list[dict[str, Any]], issues: list[Issue], strict: bool) -> None:
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    by_grade = Counter(template.get("grade", "<missing>") for template in templates)

    print("MathPro template validation")
    print("=" * 27)
    print(f"Templates scanned: {len(templates)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Strict mode: {'on' if strict else 'off'}")
    print()
    print("Templates by grade:")
    for grade, count in sorted(by_grade.items(), key=lambda item: str(item[0])):
        print(f"- {grade}: {count}")

    if errors:
        print()
        print("Errors:")
        for issue in errors:
            print(f"- {issue.file} / {issue.template_id}: {issue.message}")

    if warnings:
        print()
        print("Warnings:")
        for issue in warnings:
            print(f"- {issue.file} / {issue.template_id}: {issue.message}")

    if not errors and not warnings:
        print()
        print("No template quality issues found.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MathPro JSON problem templates.")
    parser.add_argument("--knowledge-map", type=Path, default=DEFAULT_KNOWLEDGE_MAP)
    parser.add_argument("--template-dir", type=Path, default=DEFAULT_TEMPLATE_DIR)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as a failing validation result.")
    args = parser.parse_args()

    issues: list[Issue] = []
    valid_points = load_knowledge_index(args.knowledge_map, issues)
    templates = load_templates(args.template_dir, issues)

    ids = [str(template.get("id", "")) for template in templates]
    duplicate_ids = {template_id for template_id, count in Counter(ids).items() if template_id and count > 1}
    for template in templates:
        template_id = str(template.get("id", f"<item {template.get('_index', '?')}>"))
        if not template.get("id"):
            add_issue(issues, "error", template.get("_file", "<unknown>"), template_id, "id is empty")
        if template_id in duplicate_ids:
            add_issue(issues, "error", template.get("_file", "<unknown>"), template_id, "duplicate template id")
        validate_template(template, valid_points, issues)

    print_report(templates, issues, args.strict)

    has_errors = any(issue.severity == "error" for issue in issues)
    has_warnings = any(issue.severity == "warning" for issue in issues)
    if has_errors or (args.strict and has_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
