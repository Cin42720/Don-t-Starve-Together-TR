"""
DST Speech File Extractor
Karakter konusma dosyalarindan tum stringleri cikarir.
"""
import re
import json
import os
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
JSON_DIR = os.path.join(DATA_ROOT, "json")
SCRIPTS_DIR = os.path.join(DATA_ROOT, "source_scripts")
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


def parse_speech_file(filepath):
    """Speech dosyasini parse et, tum key=value ciftlerini cikar."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    strings = {}
    path_stack = []
    in_block = False
    array_indices = {}

    for line in lines:
        # Satir sonundaki yorumu temizle (string icindeki -- haric)
        # Once string'i bul, sonra string disindaki yorumu kaldir
        raw = line.rstrip()
        stripped = raw.strip()

        # Bos satir
        if not stripped:
            continue

        # Tamamen yorum satiri
        if stripped.startswith("--"):
            continue

        # Satir icindeki yorumu temizle: string disindaki --
        clean = stripped
        in_str = False
        escape = False
        for ci, ch in enumerate(stripped):
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"':
                in_str = not in_str
            if not in_str and ch == "-" and ci + 1 < len(stripped) and stripped[ci + 1] == "-":
                clean = stripped[:ci].rstrip()
                break

        if not clean:
            continue

        # return{ veya return { -> baslangic
        if re.match(r"^return\s*\{?\s*$", clean):
            in_block = True
            path_stack = []
            continue

        if not in_block:
            # Henuz return gormedik
            if clean == "{":
                in_block = True
                path_stack = []
            continue

        # } veya }, -> kapanma
        if clean == "}" or clean == "},":
            if path_stack:
                array_indices.pop(tuple(path_stack), None)
                path_stack.pop()
            else:
                in_block = False
            continue

        # KEY = { -> tablo acilisi (cok satirli)
        m = re.match(r"^(\w+)\s*=\s*\{\s*$", clean)
        if m:
            path_stack.append(m.group(1))
            array_indices[tuple(path_stack)] = 1
            continue

        # KEY = -> sonraki satirda { bekleniyor
        m = re.match(r"^(\w+)\s*=\s*$", clean)
        if m:
            path_stack.append(m.group(1))
            continue

        # Sadece { (onceki KEY = icin)
        if clean == "{":
            continue

        # Tek satirlik tablo: KEY = { ... },
        m = re.match(r"^(\w+)\s*=\s*\{(.+)\}", clean)
        if m:
            key = m.group(1)
            inner = m.group(2)
            # Icerideki key=value ciftlerini cikar
            inner_matches = re.findall(r'(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"', inner)
            if inner_matches:
                for ik, iv in inner_matches:
                    full = ".".join(path_stack + [key, ik])
                    strings[full] = decode_lua_string(iv)
            else:
                array_path = path_stack + [key]
                array_indices[tuple(array_path)] = 1
                for match in STRING_LITERAL_RE.finditer(inner):
                    raw_value = match.group(1) if match.group(1) is not None else match.group(2)
                    add_array_value(strings, array_path, array_indices, decode_lua_string(raw_value))
                array_indices.pop(tuple(array_path), None)
            continue

        # key = "value" atamasi
        m = re.match(r'^(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"', clean)
        if m:
            key = m.group(1)
            value = decode_lua_string(m.group(2))
            full = ".".join(path_stack + [key])
            strings[full] = value
            continue

        # key = 'value' atamasi
        m = re.match(r"^(\w+)\s*=\s*'((?:[^'\\]|\\.)*)'", clean)
        if m:
            key = m.group(1)
            value = decode_lua_string(m.group(2))
            full = ".".join(path_stack + [key])
            strings[full] = value
            continue

        # Cok satirli dizilerdeki string elemanlari
        if clean.startswith('"') or clean.startswith("'"):
            for match in STRING_LITERAL_RE.finditer(clean):
                raw_value = match.group(1) if match.group(1) is not None else match.group(2)
                add_array_value(strings, path_stack, array_indices, decode_lua_string(raw_value))
            continue

    return strings


def main():
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

    speech_files = sorted(glob.glob(os.path.join(SCRIPTS_DIR, "speech_*.lua")))
    all_strings = {}
    total = 0

    for sf in speech_files:
        basename = os.path.splitext(os.path.basename(sf))[0]
        char_key = char_map.get(basename, basename.upper().replace("SPEECH_", ""))
        result = parse_speech_file(sf)
        count = len(result)
        total += count
        print(f"  {basename}: {count:,} string")

        for key, value in result.items():
            full_key = f"CHARACTERS.{char_key}.{key}"
            all_strings[full_key] = value

    print(f"\nToplam: {total:,} karakter konusma stringi")

    # JSON olarak kaydet
    os.makedirs(JSON_DIR, exist_ok=True)
    output_path = os.path.join(JSON_DIR, "speech_en.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_strings, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"Kaydedildi: {output_path}")


if __name__ == "__main__":
    main()
