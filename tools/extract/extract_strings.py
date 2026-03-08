"""
DST String Extractor (Hizli Regex Yontemi)
=============================================
Don't Starve Together strings.lua dosyasindan stringleri cikarir.

Kullanim:
    python tools/extract/extract_strings.py [strings.lua yolu]
    python tools/extract/extract_strings.py   (varsayilan: data/source_scripts/strings.lua)

Cikti:
    data/json/strings_en.json
"""

import re
import json
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
JSON_DIR = os.path.join(DATA_ROOT, "json")
SOURCE_SCRIPTS_DIR = os.path.join(DATA_ROOT, "source_scripts")

INLINE_KEY_VALUE_RE = re.compile(r'(\w+)\s*=\s*("((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')')
STRING_LITERAL_RE = re.compile(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'')


def decode_lua_string(raw):
    return raw.replace('\\\\', '\\').replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n").replace("\\t", "\t")


def add_array_value(strings, path_stack, array_indices, value):
    if not path_stack:
        return

    table_path = tuple(path_stack)
    next_index = array_indices.get(table_path, 1)
    full_path = ".".join(path_stack + [str(next_index)])
    strings[full_path] = value
    array_indices[table_path] = next_index + 1


def extract_inline_table(strings, path_stack, inline_content, array_indices):
    kv_matches = list(INLINE_KEY_VALUE_RE.finditer(inline_content))
    if kv_matches:
        for match in kv_matches:
            key = match.group(1)
            raw_value = match.group(3) if match.group(3) is not None else match.group(4)
            strings[".".join(path_stack + [key])] = decode_lua_string(raw_value)
        return

    for match in STRING_LITERAL_RE.finditer(inline_content):
        raw_value = match.group(1) if match.group(1) is not None else match.group(2)
        add_array_value(strings, path_stack, array_indices, decode_lua_string(raw_value))


def merge_missing_translations(existing, source):
    changed = False

    for key, value in source.items():
        if isinstance(value, dict):
            current = existing.get(key)
            if not isinstance(current, dict):
                existing[key] = {}
                current = existing[key]
                changed = True
            if merge_missing_translations(current, value):
                changed = True
        elif key not in existing:
            existing[key] = ""
            changed = True

    return changed


def extract_strings_regex(content):
    """
    Regex ile key = "value" ciftlerini cikar.
    DST strings.lua formati oldukca duzenli:
        key = "value",
    """
    strings = {}
    path_stack = []
    lines = content.split("\n")
    in_strings = False
    expect_open_brace = False  # Onceki satirda KEY = goruldu, { bekleniyor
    array_indices = {}
    table_stack = []

    for line in lines:
        stripped = line.strip()

        # Yorum satirlarini atla
        if stripped.startswith("--"):
            continue

        # STRINGS = veya STRINGS = { baslangici
        if re.match(r'^STRINGS\s*=\s*\{', stripped):
            in_strings = True
            path_stack = []
            expect_open_brace = False
            table_stack = [None]
            continue
        if re.match(r'^STRINGS\s*=\s*$', stripped):
            in_strings = True
            path_stack = []
            expect_open_brace = True
            table_stack = []
            continue

        # STRINGS.KEY = \n veya STRINGS.KEY = {
        m = re.match(r'^STRINGS\.(\w+)\s*=\s*$', stripped)
        if m:
            in_strings = True
            path_stack = [m.group(1)]
            expect_open_brace = True
            array_indices[tuple(path_stack)] = 1
            table_stack = []
            continue
        m = re.match(r'^STRINGS\.(\w+)\s*=\s*\{', stripped)
        if m:
            in_strings = True
            path_stack = [m.group(1)]
            expect_open_brace = False
            array_indices[tuple(path_stack)] = 1
            table_stack = [m.group(1)]
            continue

        if not in_strings:
            continue

        # Beklenen { acilisi (onceki satirda KEY = gorulmustu)
        if expect_open_brace and stripped == "{":
            expect_open_brace = False
            if len(table_stack) < len(path_stack):
                table_stack.append(path_stack[-1])
            else:
                table_stack.append(None)
            continue

        # Tablo acilisi: KEY = {
        # Tek satirda kapanan tablolari/dizileri atla (orn: MONTH_ABBR = {"Jan", ...},)
        m = re.match(r'^(\w+)\s*=\s*\{', stripped)
        if m:
            # Satir ayni satirda } ile kapaniyorsa stack'e ekleme (tek satirlik dizi/tablo)
            if re.search(r'\}', stripped[stripped.index('{') + 1:]):
                inline_content = stripped[stripped.index('{') + 1:stripped.rindex('}')]
                extract_inline_table(strings, path_stack + [m.group(1)], inline_content, array_indices)
            else:
                path_stack.append(m.group(1))
                array_indices[tuple(path_stack)] = 1
                table_stack.append(m.group(1))
            expect_open_brace = False
            continue

        # KEY = (deger sonraki satirda, tablo olabilir)
        m = re.match(r'^(\w+)\s*=\s*$', stripped)
        if m:
            path_stack.append(m.group(1))
            expect_open_brace = True
            array_indices[tuple(path_stack)] = 1
            continue

        # Sadece { acilisi (iç içe tablo)
        if stripped == "{":
            expect_open_brace = False
            table_stack.append(None)
            continue

        # Tablo kapanisi: }, veya }
        if stripped.startswith("}"):
            expect_open_brace = False
            if table_stack:
                closed_key = table_stack.pop()
                if closed_key is not None and path_stack:
                    array_indices.pop(tuple(path_stack), None)
                    path_stack.pop()
                elif not table_stack:
                    in_strings = False
            else:
                in_strings = False
            continue

        # key = "value" atamasi
        m = re.match(r'^(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"', stripped)
        if m:
            key = m.group(1)
            value = decode_lua_string(m.group(2))
            full_path = ".".join(path_stack + [key])
            strings[full_path] = value
            continue

        # key = 'value' atamasi
        m = re.match(r"^(\w+)\s*=\s*'((?:[^'\\]|\\.)*)'", stripped)
        if m:
            key = m.group(1)
            value = decode_lua_string(m.group(2))
            full_path = ".".join(path_stack + [key])
            strings[full_path] = value
            continue

        # String birlestirmeli atama: key = "text" .. VAR .. "text"
        m = re.match(r'^(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"(\s*\.\.\s*.+)', stripped)
        if m:
            key = m.group(1)
            value = decode_lua_string(m.group(2))
            full_path = ".".join(path_stack + [key])
            strings[full_path] = value + " [...]"
            continue

        # Dizideki string elemani: "value", veya 'value',
        if stripped.startswith('"') or stripped.startswith("'"):
            for match in STRING_LITERAL_RE.finditer(stripped):
                raw_value = match.group(1) if match.group(1) is not None else match.group(2)
                add_array_value(strings, path_stack, array_indices, decode_lua_string(raw_value))
            continue

    return strings


def unflatten(flat_dict):
    """Duz key.path formatini ic ice sozluge cevir."""
    result = {}
    for key, value in flat_dict.items():
        parts = key.split(".")
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                current[part] = {"_value": current[part]}
            current = current[part]
        current[parts[-1]] = value
    return result


def count_by_category(nested):
    """Kategori bazinda string say."""
    def count(d):
        total = 0
        for v in d.values():
            if isinstance(v, dict):
                total += count(v)
            elif isinstance(v, str):
                total += 1
        return total

    cats = {}
    for key, value in nested.items():
        if isinstance(value, dict):
            cats[key] = count(value)
        elif isinstance(value, str):
            cats[key] = 1
    return cats


def main():
    if len(sys.argv) >= 2:
        lua_path = sys.argv[1]
    else:
        lua_path = os.path.join(SOURCE_SCRIPTS_DIR, "strings.lua")

    if not os.path.isfile(lua_path):
        print(f"[HATA] Dosya bulunamadi: {lua_path}")
        print("\nKullanim: python tools/extract/extract_strings.py <strings.lua yolu>")
        sys.exit(1)

    print(f"[...] Okunuyor: {lua_path}")
    with open(lua_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"[...] {len(content):,} karakter parse ediliyor...")
    flat_strings = extract_strings_regex(content)
    print(f"[...] {len(flat_strings):,} string bulundu (ana dosya)")

    # Speech dosyalarini da parse et (karakter konusmalari)
    scripts_dir = os.path.dirname(lua_path)
    import glob
    speech_files = sorted(glob.glob(os.path.join(scripts_dir, "speech_*.lua")))
    if speech_files:
        print(f"[...] {len(speech_files)} karakter konusma dosyasi bulundu")
        char_map = {
            "speech_wilson": "GENERIC",
            "speech_waxwell": "WAXWELL",
            "speech_wolfgang": "WOLFGANG",
            "speech_wx78": "WX78",
            "speech_willow": "WILLOW",
            "speech_wendy": "WENDY",
            "speech_woodie": "WOODIE",
            "speech_wickerbottom": "WICKERBOTTOM",
            "speech_wathgrithr": "WATHGRITHR",
            "speech_webber": "WEBBER",
            "speech_winona": "WINONA",
            "speech_wortox": "WORTOX",
            "speech_wormwood": "WORMWOOD",
            "speech_warly": "WARLY",
            "speech_wurt": "WURT",
            "speech_walter": "WALTER",
            "speech_wanda": "WANDA",
        }
        for sf in speech_files:
            basename = os.path.splitext(os.path.basename(sf))[0]
            char_key = char_map.get(basename, basename.upper().replace("SPEECH_", ""))
            with open(sf, "r", encoding="utf-8") as f:
                speech_content = f.read()
            # Speech dosyalari "return { ... }" formatinda
            # "return" satirini "DUMMY =" ile degistir ve parse et
            speech_content = re.sub(r'^return\s*$', 'STRINGS =', speech_content, count=1, flags=re.MULTILINE)
            speech_content = re.sub(r'^return\s*\{', 'STRINGS =\n{', speech_content, count=1, flags=re.MULTILINE)
            speech_content = re.sub(r'^return\{', 'STRINGS =\n{', speech_content, count=1, flags=re.MULTILINE)
            speech_strings = extract_strings_regex(speech_content)
            # Prefix olarak CHARACTERS.CHARNAME ekle
            count_added = 0
            for key, value in speech_strings.items():
                new_key = f"CHARACTERS.{char_key}.{key}"
                flat_strings[new_key] = value
                count_added += 1
            print(f"      {basename}: {count_added:,} string")

    total = len(flat_strings)
    print(f"[...] Toplam: {total:,} string")

    # Ic ice yapiya cevir
    nested = unflatten(flat_strings)

    # Kaydet
    output_path = os.path.join(JSON_DIR, "strings_en.json")
    os.makedirs(JSON_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nested, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"\n[OK] {len(flat_strings):,} string kaydedildi: {output_path}")

    # Istatistikler
    cats = count_by_category(nested)
    print("\nKategori bazinda:")
    for key in sorted(cats.keys()):
        print(f"  {key}: {cats[key]:,}")

    # strings_tr.json yoksa bos sablon olustur, varsa eksik anahtarlari ekle
    tr_path = os.path.join(JSON_DIR, "strings_tr.json")
    if not os.path.isfile(tr_path):
        def empty_copy(d):
            result = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    result[k] = empty_copy(v)
                else:
                    result[k] = ""
            return result

        tr_template = empty_copy(nested)
        with open(tr_path, "w", encoding="utf-8") as f:
            json.dump(tr_template, f, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"\n[OK] Bos ceviri sablonu olusturuldu: {tr_path}")
        print(f"     {len(flat_strings):,} string cevrilmeyi bekliyor.")
    else:
        with open(tr_path, "r", encoding="utf-8") as f:
            tr_existing = json.load(f)

        if merge_missing_translations(tr_existing, nested):
            with open(tr_path, "w", encoding="utf-8") as f:
                json.dump(tr_existing, f, ensure_ascii=False, indent=2, sort_keys=True)
            print(f"\n[OK] Eksik ceviri anahtarlari guncellendi: {tr_path}")
        else:
            print(f"\n[OK] strings_tr.json zaten guncel: {tr_path}")


if __name__ == "__main__":
    main()
