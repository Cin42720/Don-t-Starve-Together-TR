"""
StageActor cevirilerini Lua dosyasina donustur.
data/json/stageactor_tr.json -> tr_stageactor.lua
data/json/stageactor_en.json + data/json/stageactor_tr.json -> tr_stageactor_map.lua
"""
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS_ROOT not in sys.path:
    sys.path.insert(0, TOOLS_ROOT)

from package.sync_packages import sync_shared_package_files

JSON_DIR = os.path.join(PROJECT_ROOT, "data", "json")


def lua_escape(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return s


def build_lua_lines(stageactor_tr):
    lines = [
        "-- Don't Starve Together Turkish Translation - StageActor",
        "-- Auto-generated",
        "",
        "STRINGS.STAGEACTOR = STRINGS.STAGEACTOR or {}",
        "",
    ]

    # Kategorilere gore grupla
    categories = {}
    for key, value in stageactor_tr.items():
        if not value:
            continue
        parts = key.split('.', 1)
        cat = parts[0]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, value))

    for cat in sorted(categories.keys()):
        items = categories[cat]
        lines.append(f"STRINGS.STAGEACTOR.{cat} = STRINGS.STAGEACTOR.{cat} or {{}}")

        for key, value in items:
            parts = key.split('.', 1)
            sub_key = parts[1] if len(parts) > 1 else key

            # Numerik key mi?
            if sub_key.isdigit():
                lines.append(f'STRINGS.STAGEACTOR.{cat}[{sub_key}] = "{lua_escape(value)}"')
            else:
                lines.append(f'STRINGS.STAGEACTOR.{cat}.{sub_key} = "{lua_escape(value)}"')

        lines.append("")

    return lines


def build_map_lua_lines(stageactor_en, stageactor_tr):
    lines = [
        "-- Don't Starve Together Turkish Translation - StageActor Map",
        "-- Auto-generated",
        "",
        "local GLOBAL = GLOBAL",
        "local rawget = GLOBAL.rawget or rawget",
        "local rawset = GLOBAL.rawset or rawset",
        "local type = GLOBAL.type or type",
        "local MAP = rawget(GLOBAL, \"TURKCE_STAGEACTOR_LINE_MAP\")",
        "if type(MAP) ~= \"table\" then",
        "    MAP = {}",
        "    rawset(GLOBAL, \"TURKCE_STAGEACTOR_LINE_MAP\", MAP)",
        "end",
        "",
    ]

    for key in sorted(stageactor_en.keys()):
        en_value = stageactor_en.get(key)
        tr_value = stageactor_tr.get(key)
        if not en_value or not tr_value or en_value == tr_value:
            continue
        lines.append(f'MAP["{lua_escape(en_value)}"] = "{lua_escape(tr_value)}"')

    lines.append("")
    return lines


def main():
    en_path = os.path.join(JSON_DIR, "stageactor_en.json")
    tr_path = os.path.join(JSON_DIR, "stageactor_tr.json")
    if not os.path.isfile(en_path) or not os.path.isfile(tr_path):
        print("[HATA] stageactor_en.json veya stageactor_tr.json bulunamadi.")
        return

    with open(en_path, "r", encoding="utf-8") as f:
        stageactor_en = json.load(f)

    with open(tr_path, "r", encoding="utf-8") as f:
        stageactor_tr = json.load(f)

    if not stageactor_tr:
        print("Ceviri yok!")
        return

    target_paths = [
        (
            os.path.join(PROJECT_ROOT, "mod", "scripts", "languages", "tr_stageactor.lua"),
            build_lua_lines(stageactor_tr),
        ),
        (
            os.path.join(PROJECT_ROOT, "mod", "scripts", "languages", "tr_stageactor_map.lua"),
            build_map_lua_lines(stageactor_en, stageactor_tr),
        ),
    ]

    for lua_path, lines in target_paths:
        os.makedirs(os.path.dirname(lua_path), exist_ok=True)
        with open(lua_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Yazildi: {lua_path}")

    results = sync_shared_package_files(include_live=False)
    for target, stats in results.items():
        print(f"[SYNC] {target}: copied={stats['copied']} removed={stats['removed_files']}")


if __name__ == "__main__":
    main()
