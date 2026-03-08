"""
Speech cevirilerini Lua dosyasina donustur ve tr_strings.lua'ya ekle.
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


def lua_path(parts):
    expr = "STRINGS"
    for part in parts:
        if part.isdigit():
            expr += f"[{part}]"
        else:
            expr += f".{part}"
    return expr


def main():
    # Speech cevirilerini oku
    speech_tr_path = os.path.join(JSON_DIR, "speech_tr.json")
    with open(speech_tr_path, "r", encoding="utf-8") as f:
        speech_tr = json.load(f)

    if not speech_tr:
        print("Ceviri yok!")
        return

    # Speech satirlari olustur (ayri dosya olarak)
    output_path = os.path.join(PROJECT_ROOT, "mod", "scripts", "languages", "tr_speech.lua")

    lines = [
        "-- Don't Starve Together Turkish Translation - Speech",
        "-- Auto-generated",
        "",
    ]

    # Tum parent tablolari takip et
    created_tables = set()

    for key in sorted(speech_tr.keys()):
        value = speech_tr[key]
        if not value:
            continue

        parts = key.split(".")
        lua_key = lua_path(parts)

        # Parent tablolari olustur
        for i in range(1, len(parts)):
            if parts[i - 1].isdigit():
                break

            parent_parts = parts[:i]
            parent = tuple(parent_parts)
            if parent not in created_tables:
                created_tables.add(parent)
                parent_expr = lua_path(parent_parts)
                lines.append(f"{parent_expr} = {parent_expr} or {{}}")

        lines.append(f'{lua_key} = "{lua_escape(value)}"')

    # tr_speech.lua olarak yaz (ayri dosya)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"{len(speech_tr)} speech cevirisi tr_speech.lua'ya yazildi.")
    results = sync_shared_package_files(include_live=False)
    for target, stats in results.items():
        print(f"[SYNC] {target}: copied={stats['copied']} removed={stats['removed_files']}")


if __name__ == "__main__":
    main()
