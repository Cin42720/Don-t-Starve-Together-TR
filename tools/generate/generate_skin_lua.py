"""
Skin cevirilerini Lua dosyasina donustur.
data/json/skin_tr.json -> tr_skin.lua
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


def main():
    tr_path = os.path.join(JSON_DIR, "skin_tr.json")
    if not os.path.isfile(tr_path):
        print("[HATA] skin_tr.json bulunamadi. Once tools/translate/translate_skin.py calistirin.")
        return

    with open(tr_path, "r", encoding="utf-8") as f:
        skin_tr = json.load(f)

    if not skin_tr:
        print("Ceviri yok!")
        return

    lua_path = os.path.join(PROJECT_ROOT, "mod", "scripts", "languages", "tr_skin.lua")

    lines = [
        "-- Don't Starve Together Turkish Translation - Skins",
        "-- Auto-generated",
        "",
    ]

    # Kategorilere gore grupla
    categories = {}
    for key, value in skin_tr.items():
        if not value:
            continue
        parts = key.split('.', 1)
        cat = parts[0]  # SKIN_QUOTES, SKIN_NAMES, SKIN_DESCRIPTIONS
        sub_key = parts[1] if len(parts) > 1 else key
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((sub_key, value))

    for cat in sorted(categories.keys()):
        items = categories[cat]
        lines.append(f"STRINGS.{cat} = STRINGS.{cat} or {{}}")

        for sub_key, value in items:
            lines.append(f'STRINGS.{cat}.{sub_key} = "{lua_escape(value)}"')

        lines.append("")

    os.makedirs(os.path.dirname(lua_path), exist_ok=True)
    with open(lua_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"{len(skin_tr):,} skin cevirisi tr_skin.lua'ya yazildi.")
    print(f"Dosya: {lua_path}")
    print(f"Satirlar: {len(lines):,}")
    results = sync_shared_package_files(include_live=False)
    for target, stats in results.items():
        print(f"[SYNC] {target}: copied={stats['copied']} removed={stats['removed_files']}")


if __name__ == "__main__":
    main()
