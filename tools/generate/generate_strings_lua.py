import json
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS_ROOT not in sys.path:
    sys.path.insert(0, TOOLS_ROOT)

from package.sync_packages import sync_shared_package_files

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "json", "strings_tr.json")
TARGET_PATHS = [os.path.join(PROJECT_ROOT, "mod", "scripts", "languages", "tr_ui.lua")]
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def lua_escape(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return s


def sort_items(obj):
    return sorted(
        obj.items(),
        key=lambda item: (0, int(item[0])) if item[0].isdigit() else (1, item[0]),
    )


def lua_ref(prefix, key):
    if key.isdigit():
        return f"{prefix}[{key}]"
    if IDENTIFIER_RE.match(key):
        return f"{prefix}.{key}"
    return f'{prefix}["{lua_escape(key)}"]'


def gen_lines(obj, prefix):
    lines = []
    if not isinstance(obj, dict):
        return lines

    for key, value in sort_items(obj):
        full = lua_ref(prefix, key)
        if isinstance(value, str):
            if value:
                lines.append(f'{full} = "{lua_escape(value)}"')
        elif isinstance(value, dict):
            child_lines = gen_lines(value, full)
            if child_lines:
                lines.append(f'{full} = {full} or {{}}')
                lines.extend(child_lines)
    return lines


def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        tr = json.load(f)

    all_lines = [
        "-- Don't Starve Together Turkish Translation",
        "-- Auto-generated",
        "",
    ]

    for top_key, top_val in sort_items(tr):
        prefix = lua_ref("STRINGS", top_key)
        if isinstance(top_val, str):
            if top_val:
                all_lines.append(f'{prefix} = "{lua_escape(top_val)}"')
        elif isinstance(top_val, dict):
            child_lines = gen_lines(top_val, prefix)
            if child_lines:
                all_lines.append(f'{prefix} = {prefix} or {{}}')
                all_lines.extend(child_lines)

    for target_path in TARGET_PATHS:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_lines))
        print(f'Generated {len(all_lines)} lines in {target_path}')

    results = sync_shared_package_files(include_live=False)
    for target, stats in results.items():
        print(f"[SYNC] {target}: copied={stats['copied']} removed={stats['removed_files']}")


if __name__ == "__main__":
    main()
