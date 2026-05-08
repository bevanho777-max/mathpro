from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_MAP = REPO_ROOT / "data" / "curriculum" / "knowledge_map.json"
DEFAULT_TEMPLATE_DIR = REPO_ROOT / "data" / "templates"


REQUIRED_TEMPLATE_FIELDS = {
    "id",
    "version",
    "grade",
    "semester",
    "module",
    "knowledge_point",
    "difficulty",
    "question_type",
    "source_type",
    "parameters",
    "question_template",
    "answer_rule",
    "solution_template",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def iter_knowledge_points(knowledge_map: dict[str, Any]):
    for grade in knowledge_map.get("grades", []):
        for module in grade.get("modules", []):
            for point in module.get("knowledge_points", []):
                yield grade["grade"], module["name"], point["name"], point.get("id", "")


def load_templates(template_dir: Path) -> list[dict[str, Any]]:
    templates: list[dict[str, Any]] = []
    for path in sorted(template_dir.glob("*.json")):
        payload = load_json(path)
        items = payload.get("templates", payload) if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise ValueError(f"{path} must contain a list or an object with templates")
        for item in items:
            item["_file"] = str(path.relative_to(REPO_ROOT))
            templates.append(item)
    return templates


def validate_templates(templates: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    for template in templates:
        template_id = template.get("id", "<missing id>")
        missing = REQUIRED_TEMPLATE_FIELDS - set(template)
        if missing:
            errors.append(f"{template_id}: missing fields {sorted(missing)}")
        if template_id in seen_ids:
            errors.append(f"{template_id}: duplicate template id")
        seen_ids.add(template_id)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check MathPro template coverage by knowledge point.")
    parser.add_argument("--knowledge-map", type=Path, default=DEFAULT_KNOWLEDGE_MAP)
    parser.add_argument("--template-dir", type=Path, default=DEFAULT_TEMPLATE_DIR)
    parser.add_argument("--min-count", type=int, default=1)
    args = parser.parse_args()

    knowledge_map = load_json(args.knowledge_map)
    templates = load_templates(args.template_dir)
    validation_errors = validate_templates(templates)

    valid_points = {
        (grade, module, point)
        for grade, module, point, _ in iter_knowledge_points(knowledge_map)
    }
    counts = Counter((item.get("grade"), item.get("module"), item.get("knowledge_point")) for item in templates)

    unmapped = [
        item
        for item in templates
        if (item.get("grade"), item.get("module"), item.get("knowledge_point")) not in valid_points
    ]

    print("MathPro coverage report")
    print("=" * 24)
    print(f"Knowledge points: {len(valid_points)}")
    print(f"Templates: {len(templates)}")
    print()

    uncovered: list[tuple[str, str, str, int]] = []
    for grade, module, point, point_id in iter_knowledge_points(knowledge_map):
        count = counts[(grade, module, point)]
        if count < args.min_count:
            uncovered.append((grade, module, point, count))
        print(f"{grade}\t{module}\t{point}\t{count}")

    if validation_errors:
        print()
        print("Template validation errors:")
        for error in validation_errors:
            print(f"- {error}")

    if unmapped:
        print()
        print("Templates bound to unknown knowledge points:")
        for item in unmapped:
            print(f"- {item.get('id')} -> {item.get('grade')} / {item.get('module')} / {item.get('knowledge_point')}")

    if uncovered:
        print()
        print(f"Knowledge points below min-count={args.min_count}: {len(uncovered)}")
        for grade, module, point, count in uncovered:
            print(f"- {grade} / {module} / {point}: {count}")

    return 1 if validation_errors or unmapped else 0


if __name__ == "__main__":
    raise SystemExit(main())
