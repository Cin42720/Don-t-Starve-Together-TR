#!/usr/bin/env python
"""
DST Font Fixer - Eksik Türkçe karakterleri font dosyalarına ekler.
DXT1 olarak decode eder, Türkçe glyph ekler, RGBA olarak yeniden kaydeder.
"""

import zipfile
import io
import struct
import re
import os
import shutil
import texture2ddecoder
from PIL import Image, ImageFont, ImageDraw

TURKISH_CHARS = {
    286: 'Ğ', 287: 'ğ', 304: 'İ', 305: 'ı',
    350: 'Ş', 351: 'ş', 199: 'Ç', 231: 'ç',
    214: 'Ö', 246: 'ö', 220: 'Ü', 252: 'ü',
}

# Benzer base karakter (metrik referans için)
BASE_MAP = {
    286: 71, 287: 103, 304: 73, 305: 105, 350: 83, 351: 115,
    199: 67, 231: 99, 214: 79, 246: 111, 220: 85, 252: 117,
}

GAME_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/Don' + "'" + 't Starve Together'
FONTS_ZIP = os.path.join(GAME_PATH, 'data/databundles/fonts.zip')

FONTS_TO_FIX = {
    'fonts/talkingfont_hermit.zip': [286, 287, 304, 305, 350, 351],
    'fonts/talkingfont_tradein.zip': [286, 287, 304, 305, 350, 351],
    'fonts/talkingfont_wormwood.zip': [286, 287, 304, 305, 350, 351],
    'fonts/spirequal_outline_small.zip': [252],
    'fonts/fallback.zip': [286, 287, 304, 305, 350, 351],
    'fonts/fallback_outline.zip': [286, 287, 304, 305, 350, 351],
}


def read_tex(tex_data):
    """KTEX DXT1 formatını oku, RGBA image döndür."""
    assert tex_data[:4] == b'KTEX'
    flags = struct.unpack('<I', tex_data[4:8])[0]
    pixel_format = (flags >> 4) & 0x1F
    mipmap_count = (flags >> 13) & 0x1F

    offset = 8
    mipmaps = []
    for _ in range(mipmap_count):
        w, h = struct.unpack('<HH', tex_data[offset:offset+4])
        pitch = struct.unpack('<H', tex_data[offset+4:offset+6])[0]
        datasize = struct.unpack('<I', tex_data[offset+6:offset+10])[0]
        mipmaps.append((w, h, pitch, datasize))
        offset += 10

    w, h, pitch, datasize = mipmaps[0]
    pixel_data = tex_data[offset:offset+datasize]

    # DXT1 (BC1) decode
    decoded = texture2ddecoder.decode_bc1(pixel_data, w, h)
    img = Image.frombytes('RGBA', (w, h), decoded, 'raw', 'BGRA')

    return img, w, h


def write_tex_rgba(img):
    """RGBA Image'ı KTEX formatına yaz (sıkıştırmasız)."""
    w, h = img.size

    # Mipmap'ler oluştur
    mipmaps = []
    current = img.copy()
    while True:
        cw, ch = current.size
        # BGRA'ya çevir
        r, g, b, a = current.split()
        bgra = Image.merge('RGBA', (b, g, r, a))
        data = bgra.tobytes()
        pitch = cw * 4
        mipmaps.append((cw, ch, pitch, data))
        if cw <= 1 and ch <= 1:
            break
        current = current.resize((max(1, cw // 2), max(1, ch // 2)), Image.LANCZOS)

    # Header flags: platform=0, pixelformat=4(RGBA), textype=1, mipmaps=count, flags=3
    flags = 0
    flags |= (4 & 0x1F) << 4        # pixel_format = 4 (uncompressed RGBA)
    flags |= (1 & 0xF) << 9         # texture_type = 1
    flags |= (len(mipmaps) & 0x1F) << 13
    flags |= (3 & 0x3) << 18

    buf = io.BytesIO()
    buf.write(b'KTEX')
    buf.write(struct.pack('<I', flags))

    for cw, ch, pitch, data in mipmaps:
        buf.write(struct.pack('<HH', cw, ch))
        buf.write(struct.pack('<H', pitch))
        buf.write(struct.pack('<I', len(data)))

    for _, _, _, data in mipmaps:
        buf.write(data)

    return buf.getvalue()


def parse_fnt(fnt_text):
    """FNT dosyasını parse et (XML veya text format)."""
    is_xml = '<?xml' in fnt_text or '<font>' in fnt_text

    chars = {}
    if is_xml:
        for m in re.finditer(r'<char\s+([^/]+)/>', fnt_text):
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
            chars[int(attrs['id'])] = attrs
    else:
        for line in fnt_text.split('\n'):
            if line.startswith('char ') and 'id=' in line:
                attrs = dict(re.findall(r'(\w+)=(-?\d+)', line))
                chars[int(attrs['id'])] = attrs

    # Font size
    size = 50
    m = re.search(r'size="?(\d+)"?', fnt_text)
    if m:
        size = int(m.group(1))

    # Outline kontrolü
    outline = 0
    m = re.search(r'outline="?(\d+)"?', fnt_text)
    if m:
        outline = int(m.group(1))

    return chars, size, outline, is_xml


def rebuild_fnt(original_fnt, chars, is_xml):
    """FNT dosyasını yeniden oluştur."""
    if is_xml:
        new_fnt = re.sub(r'<chars count="\d+"', f'<chars count="{len(chars)}"', original_fnt)
        new_fnt = re.sub(r'<char\s+[^/]+/>\s*', '', new_fnt)
        char_lines = []
        for cid in sorted(chars.keys()):
            c = chars[cid]
            line = f'    <char id="{c["id"]}" x="{c["x"]}" y="{c["y"]}" width="{c["width"]}" height="{c["height"]}" xoffset="{c["xoffset"]}" yoffset="{c["yoffset"]}" xadvance="{c["xadvance"]}" page="{c["page"]}" chnl="{c["chnl"]}"/>'
            char_lines.append(line)
        new_fnt = new_fnt.replace('</chars>', '\n'.join(char_lines) + '\n  </chars>')
        return new_fnt
    else:
        lines = original_fnt.split('\n')
        new_lines = []
        chars_written = False
        for line in lines:
            if line.startswith('chars count='):
                new_lines.append(f'chars count={len(chars)}')
            elif line.startswith('char ') and 'id=' in line:
                if not chars_written:
                    for cid in sorted(chars.keys()):
                        c = chars[cid]
                        new_lines.append(
                            f'char id={c["id"]:>5s}   x={c["x"]:>5s}   y={c["y"]:>5s}   '
                            f'width={c["width"]:>5s}   height={c["height"]:>5s}   '
                            f'xoffset={c["xoffset"]:>5s}   yoffset={c["yoffset"]:>5s}   '
                            f'xadvance={c["xadvance"]:>5s}   page={c["page"]:>3s}   '
                            f'chnl={c["chnl"]}'
                        )
                    chars_written = True
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)


def find_empty_space(img, need_w, need_h, chars, tex_w, tex_h):
    """Texture'da boş alan bul (FNT metadata tabanlı)."""
    occupied = []
    for attrs in chars.values():
        x = int(attrs.get('x', 0))
        y = int(attrs.get('y', 0))
        w = int(attrs.get('width', 0))
        h = int(attrs.get('height', 0))
        if w > 0 and h > 0:
            occupied.append((x, y, x + w + 2, y + h + 2))

    # Mevcut glyphlerin altından başla (en çok boş alan orada)
    max_y = max((int(a.get('y', 0)) + int(a.get('height', 0)) + 2) for a in chars.values()) if chars else 0

    for sy in [max_y] + list(range(0, tex_h - need_h, 4)):
        for sx in range(0, tex_w - need_w, 4):
            if sy + need_h > tex_h or sx + need_w > tex_w:
                continue
            r = (sx, sy, sx + need_w, sy + need_h)
            ok = True
            for ox, oy, ox2, oy2 in occupied:
                if not (r[2] <= ox or r[0] >= ox2 or r[3] <= oy or r[1] >= oy2):
                    ok = False
                    break
            if ok:
                return sx, sy
    return None, None


def fix_font(font_zip_name, missing_chars, output_dir):
    """Font dosyasına eksik Türkçe karakterleri ekle."""
    print(f"\n  İşleniyor: {font_zip_name}")

    with zipfile.ZipFile(FONTS_ZIP, 'r') as fzip:
        font_data = fzip.read(font_zip_name)

    with zipfile.ZipFile(io.BytesIO(font_data), 'r') as fz:
        fnt_text = fz.read('font.fnt').decode('utf-8', errors='replace')
        tex_data = fz.read('font.tex')
        extra_files = {n: fz.read(n) for n in fz.namelist() if n not in ('font.fnt', 'font.tex')}

    chars, font_size, outline, is_xml = parse_fnt(fnt_text)
    img, tex_w, tex_h = read_tex(tex_data)

    print(f"    Font size={font_size}, outline={outline}, chars={len(chars)}, tex={tex_w}x{tex_h}")

    is_outline_font = 'outline' in font_zip_name.lower() or outline > 0
    system_font = 'C:/Windows/Fonts/arial.ttf'

    added = 0
    for char_id in missing_chars:
        if char_id in chars:
            continue

        char = TURKISH_CHARS[char_id]
        base_id = BASE_MAP.get(char_id, 65)
        base = chars.get(base_id, list(chars.values())[0])

        # Karakter render et
        pil_font = ImageFont.truetype(system_font, font_size)
        temp = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
        td = ImageDraw.Draw(temp)
        bbox = td.textbbox((0, 0), char, font=pil_font)
        pad = outline + 2
        gw = bbox[2] - bbox[0] + pad * 2
        gh = bbox[3] - bbox[1] + pad * 2

        glyph = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)

        ox, oy = pad - bbox[0], pad - bbox[1]
        if is_outline_font and outline > 0:
            for dx in range(-outline, outline + 1):
                for dy in range(-outline, outline + 1):
                    if dx*dx + dy*dy <= (outline+1)**2:
                        gd.text((ox + dx, oy + dy), char, font=pil_font, fill=(0, 0, 0, 255))
            gd.text((ox, oy), char, font=pil_font, fill=(255, 255, 255, 255))
        else:
            gd.text((ox, oy), char, font=pil_font, fill=(255, 255, 255, 255))

        # Boş yer bul
        px, py = find_empty_space(img, gw, gh, chars, tex_w, tex_h)
        if px is None:
            print(f"    UYARI: {char} için yer bulunamadı!")
            continue

        img.paste(glyph, (px, py))

        chars[char_id] = {
            'id': str(char_id), 'x': str(px), 'y': str(py),
            'width': str(gw), 'height': str(gh),
            'xoffset': base.get('xoffset', '0'),
            'yoffset': base.get('yoffset', '0'),
            'xadvance': base.get('xadvance', str(gw)),
            'page': '0', 'chnl': base.get('chnl', '15'),
        }
        added += 1
        print(f"    + {char} (U+{char_id:04X}) @ ({px},{py}) {gw}x{gh}")

    if added == 0:
        print("    Eklenecek karakter yok.")
        return

    new_fnt = rebuild_fnt(fnt_text, chars, is_xml)
    new_tex = write_tex_rgba(img)

    out_path = os.path.join(output_dir, os.path.basename(font_zip_name))
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        zout.writestr('font.fnt', new_fnt.encode('utf-8'))
        zout.writestr('font.tex', new_tex)
        for name, data in extra_files.items():
            zout.writestr(name, data)

    print(f"    Kaydedildi: {out_path} ({added} karakter)")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'mod-client', 'fonts')
    os.makedirs(output_dir, exist_ok=True)

    print("DST Font Fixer - Türkçe Karakter Ekleme\n")

    for font_name, missing in FONTS_TO_FIX.items():
        try:
            fix_font(font_name, missing, output_dir)
        except Exception as e:
            print(f"    HATA: {e}")
            import traceback
            traceback.print_exc()

    # Server mod'a kopyala
    server_fonts = os.path.join(base_dir, 'mod-server', 'fonts')
    os.makedirs(server_fonts, exist_ok=True)
    for f in os.listdir(output_dir):
        shutil.copy2(os.path.join(output_dir, f), os.path.join(server_fonts, f))

    print(f"\n{len(os.listdir(output_dir))} font dosyası oluşturuldu.")


if __name__ == '__main__':
    main()
