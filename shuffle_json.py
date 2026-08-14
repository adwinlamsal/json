#!/usr/bin/env python3
"""
Shuffle JSON data daily:
- Shuffles the order of categories.
- Shuffles the items within each category.
- Formats JSON with 1 compact object per line for clean structure and low file size.
"""
import json
import random
from pathlib import Path

JSON_FILE = Path(__file__).parent / "hello.json"


def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Shuffle category order
    keys = list(data.keys())
    random.shuffle(keys)

    # 2. Shuffle items within each category
    shuffled_data = {}
    for key in keys:
        items = data[key]
        if isinstance(items, list):
            items_copy = list(items)
            random.shuffle(items_copy)
            shuffled_data[key] = items_copy
        else:
            shuffled_data[key] = items

    _write_compact(shuffled_data)


def _write_compact(data):
    """Write JSON with 1 compact object per line for low file size and clean structure."""
    lines = ["{\n"]
    categories = list(data.items())
    for cat_idx, (cat_name, items) in enumerate(categories):
        lines.append(f'    {json.dumps(cat_name, ensure_ascii=False)}: [\n')
        if isinstance(items, list):
            for item_idx, item in enumerate(items):
                comma = "," if item_idx < len(items) - 1 else ""
                lines.append(f'      {json.dumps(item, ensure_ascii=False)}{comma}\n')
        else:
            lines.append(f'      {json.dumps(items, ensure_ascii=False)}\n')
        cat_comma = "," if cat_idx < len(categories) - 1 else ""
        lines.append(f'    ]{cat_comma}\n')
    lines.append("}\n")

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Successfully shuffled {len(categories)} categories and their items!")


if __name__ == "__main__":
    main()
