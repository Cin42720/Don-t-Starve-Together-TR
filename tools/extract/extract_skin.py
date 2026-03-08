"""
DST skin_strings.lua dosyasini scripts.zip icinden cikar
ve skin_en.json olarak kaydet.

3 kategori: SKIN_QUOTES, SKIN_NAMES, SKIN_DESCRIPTIONS
"""
import json
import os
import re
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
JSON_DIR = os.path.join(DATA_ROOT, "json")

DST_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together"
SCRIPTS_ZIP = os.path.join(DST_PATH, "data", "databundles", "scripts.zip")


def main():
    os.makedirs(JSON_DIR, exist_ok=True)

    if not os.path.isfile(SCRIPTS_ZIP):
        print(f"[HATA] scripts.zip bulunamadi: {SCRIPTS_ZIP}")
        return

    print(f"scripts.zip okunuyor...")
    with zipfile.ZipFile(SCRIPTS_ZIP, 'r') as zf:
        content = zf.read('scripts/skin_strings.lua').decode('utf-8')

    print(f"Dosya boyutu: {len(content):,} karakter, {len(content.splitlines()):,} satir")

    skin_data = {}

    # 3 bolumu parse et: SKIN_QUOTES, SKIN_NAMES, SKIN_DESCRIPTIONS
    # Format: key = "value",
    pattern = re.compile(r'\t(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"')

    sections = {
        'SKIN_QUOTES': ('STRINGS.SKIN_QUOTES', 'STRINGS.SKIN_NAMES'),
        'SKIN_NAMES': ('STRINGS.SKIN_NAMES', 'STRINGS.SKIN_DESCRIPTIONS'),
        'SKIN_DESCRIPTIONS': ('STRINGS.SKIN_DESCRIPTIONS', None),
    }

    for section_name, (start_marker, end_marker) in sections.items():
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print(f"[UYARI] {start_marker} bulunamadi!")
            continue

        if end_marker:
            end_idx = content.find(end_marker)
            if end_idx == -1:
                end_idx = len(content)
        else:
            end_idx = len(content)

        block = content[start_idx:end_idx]
        matches = pattern.findall(block)

        for key, value in matches:
            clean_val = value.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
            full_key = f"{section_name}.{key}"
            skin_data[full_key] = clean_val

        print(f"  {section_name}: {len(matches):,} string")

    # Kaydet
    out_path = os.path.join(JSON_DIR, "skin_en.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(skin_data, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"\nToplam: {len(skin_data):,} skin stringi cikarildi.")
    print(f"Kaydedildi: {out_path}")


if __name__ == "__main__":
    main()
