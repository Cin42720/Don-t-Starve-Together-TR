"""
DST strings_stageactor.lua dosyasini scripts.zip icinden cikar
ve stageactor_en.json olarak kaydet.
"""
import json
import os
import re
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
JSON_DIR = os.path.join(DATA_ROOT, "json")

# DST kurulum yolu
DST_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together"
SCRIPTS_ZIP = os.path.join(DST_PATH, "data", "databundles", "scripts.zip")


def parse_lua_table(text):
    """Basit Lua table parser - string array ve key-value tablolari destekler."""
    result = {}

    # String array icindeki elemanlari bul: "text",
    array_pattern = re.compile(r'"((?:[^"\\]|\\.)*)"')
    # Key = "value" atamalari bul
    kv_pattern = re.compile(r'(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"')

    # Satir satir analiz et
    lines = text.split('\n')
    current_key = None
    current_block = []
    brace_depth = 0

    for line in lines:
        stripped = line.strip()

        # Ust seviye key = { tanimini bul
        top_match = re.match(r'^(\w+)\s*=\s*\{', stripped)
        if top_match and brace_depth == 0:
            current_key = top_match.group(1)
            current_block = []
            brace_depth = 1
            # Ayni satirda kapaniyor mu?
            if stripped.endswith('},') or stripped.endswith('}'):
                inner = stripped[stripped.index('{') + 1:stripped.rindex('}')]
                values = array_pattern.findall(inner)
                if values:
                    for i, v in enumerate(values):
                        result[f"{current_key}.{i+1}"] = v.replace('\\n', '\n').replace('\\"', '"')
                brace_depth = 0
                current_key = None
            continue

        if current_key and brace_depth > 0:
            brace_depth += stripped.count('{') - stripped.count('}')
            current_block.append(line)

            if brace_depth <= 0:
                # Blok tamamlandi - parse et
                block_text = '\n'.join(current_block)
                # Key-value mi yoksa array mi?
                kv_matches = kv_pattern.findall(block_text)
                arr_matches = array_pattern.findall(block_text)

                if kv_matches:
                    for k, v in kv_matches:
                        result[f"{current_key}.{k}"] = v.replace('\\n', '\n').replace('\\"', '"')
                elif arr_matches:
                    for i, v in enumerate(arr_matches):
                        result[f"{current_key}.{i+1}"] = v.replace('\\n', '\n').replace('\\"', '"')

                brace_depth = 0
                current_key = None

    return result


def main():
    os.makedirs(JSON_DIR, exist_ok=True)

    if not os.path.isfile(SCRIPTS_ZIP):
        print(f"[HATA] scripts.zip bulunamadi: {SCRIPTS_ZIP}")
        print("DST kurulum yolunu kontrol edin.")
        return

    # scripts.zip icinden strings_stageactor.lua oku
    print(f"scripts.zip okunuyor: {SCRIPTS_ZIP}")
    with zipfile.ZipFile(SCRIPTS_ZIP, 'r') as zf:
        # Dosya adini bul
        stageactor_path = None
        for name in zf.namelist():
            if 'strings_stageactor' in name:
                stageactor_path = name
                break

        if not stageactor_path:
            print("[HATA] strings_stageactor.lua bulunamadi!")
            return

        print(f"Dosya bulundu: {stageactor_path}")
        content = zf.read(stageactor_path).decode('utf-8')

    print(f"Dosya boyutu: {len(content):,} karakter, {len(content.splitlines()):,} satir")

    # Parse et
    # Dosya "local stageactor = {" ile baslar, "return stageactor" ile biter
    # Ic yapiyi cikar
    start = content.find('{')
    end = content.rfind('}')
    if start == -1 or end == -1:
        print("[HATA] Lua table yapisi bulunamadi!")
        return

    inner = content[start + 1:end]

    # Her ust-seviye tanimlamayi bul
    stageactor = {}

    # Ust-seviye bloklari bul (WILSON1 = {...}, ACT1_SCENE1 = {...}, vs.)
    # Daha iyi parsing: satir satir git
    lines = inner.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Key = { seklinde blok baslangici
        m = re.match(r'^(\w+)\s*=\s*\{', line)
        if m:
            key = m.group(1)
            brace_depth = line.count('{') - line.count('}')
            block_lines = [line]

            if brace_depth > 0:
                i += 1
                while i < len(lines) and brace_depth > 0:
                    block_lines.append(lines[i])
                    brace_depth += lines[i].count('{') - lines[i].count('}')
                    i += 1
            else:
                i += 1

            block_text = '\n'.join(block_lines)

            # Ic icerik
            inner_start = block_text.index('{') + 1
            inner_end = block_text.rindex('}')
            inner_content = block_text[inner_start:inner_end]

            # Key-value mi array mi belirle
            kv_pattern = re.compile(r'(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"')
            arr_pattern = re.compile(r'"((?:[^"\\]|\\.)*)"')

            kv_matches = kv_pattern.findall(inner_content)
            if kv_matches:
                for k, v in kv_matches:
                    clean_v = v.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                    stageactor[f"{key}.{k}"] = clean_v
            else:
                arr_matches = arr_pattern.findall(inner_content)
                for idx, v in enumerate(arr_matches, 1):
                    clean_v = v.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                    stageactor[f"{key}.{idx}"] = clean_v
            continue

        # Tek satirlik tanimlama: KEY = "value",
        m2 = re.match(r'^(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"', line)
        if m2:
            key = m2.group(1)
            val = m2.group(2).replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
            stageactor[key] = val

        i += 1

    # Sonuclari kaydet
    out_path = os.path.join(JSON_DIR, "stageactor_en.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stageactor, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"\n{len(stageactor):,} stageactor stringi cikarildi.")
    print(f"Kaydedildi: {out_path}")

    # Istatistikler
    categories = {}
    for key in stageactor:
        cat = key.split('.')[0]
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\nKategoriler:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
