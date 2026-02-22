#!/usr/bin/env python3
"""
Shuffle JSON data daily. Excludes the 1st and 2nd categories from shuffling.
"""
import json
import random
import sys
from pathlib import Path

JSON_FILE = Path(__file__).parent / "hello.json"
EXCLUDE_CATEGORY_COUNT = 2  # Keep 1st and 2nd categories unshuffled


def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    keys = list(data.keys())
    random.seed()  # Use current time for daily variation

    # 1. Shuffle category order (keep 1st and 2nd fixed)
    fixed_keys = keys[:EXCLUDE_CATEGORY_COUNT]
    shuffle_keys = keys[EXCLUDE_CATEGORY_COUNT:]
    random.shuffle(shuffle_keys)
    new_order = fixed_keys + shuffle_keys

    # Build new dict with shuffled category order
    shuffled_data = {k: data[k] for k in new_order}

    # 2. Shuffle images within each category (skip 1st and 2nd)
    for i, key in enumerate(new_order):
        if i < EXCLUDE_CATEGORY_COUNT:
            continue
        if isinstance(shuffled_data[key], list):
            random.shuffle(shuffled_data[key])

    _write_compact(shuffled_data)


def _write_compact(data):
    """Write JSON with 2 image objects per line to reduce file size."""
    sep = (",", ":")  # No spaces to save bytes

    lines = ["{"]
    keys = list(data.keys())
    for ki, key in enumerate(keys):
        lines.append(f'  "{key}": [')
        items = data[key]
        if not isinstance(items, list):
            lines.append(f"    {json.dumps(items, separators=sep, ensure_ascii=False)}")
        else:
            for i in range(0, len(items), 2):
                pair = items[i : i + 2]
                pair_str = ",".join(json.dumps(x, separators=sep, ensure_ascii=False) for x in pair)
                suffix = "," if i + 2 < len(items) else ""
                lines.append(f"    {pair_str}{suffix}")
        lines.append("  ]" + ("," if ki < len(keys) - 1 else ""))
    lines.append("}")

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Shuffled category order and images in {len(keys) - EXCLUDE_CATEGORY_COUNT} categories (excluded first {EXCLUDE_CATEGORY_COUNT})")


if __name__ == "__main__":
    main()
