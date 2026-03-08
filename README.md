# Don't Starve Together Türkçe Çeviri Projesi

English version: [README.en.md](./README.en.md)

Bu repo, `Don't Starve Together` için hazırlanan Türkçe çeviri paketlerini, üretim araçlarını ve Workshop yayın akışını içerir.

## Yapı

- [`data`](./data)
  - `data/json`: Çeviri verileri ve sözlük dosyaları
  - `data/source_scripts`: Yerel referans için tutulan kaynak Lua dosyaları
- [`tools`](./tools)
  - `extract`
  - `translate`
  - `generate`
  - `package`
  - `workshop`
- [`mod`](./mod): Ortak kaynak paket
- [`mod-client`](./mod-client): İstemci tarafı yayın paketi
- [`mod-server`](./mod-server): Sunucu tarafı yayın paketi
- [`DST_LOCALIZATION_RESEARCH.md`](./DST_LOCALIZATION_RESEARCH.md): Terim politikası ve lokalizasyon notları
- [`NOTICE.md`](./NOTICE.md): Lisans kapsamı ve türetilmiş içerik notları

## Amaç

- Ana oyun metinlerini Türkçeleştirmek
- Karakter konuşmalarını ve etkinlik diyaloglarını düzeltmek
- İstemciye özel UI, skill tree ve benzeri ekranları çevirmek
- Sunucu tarafında misafir oyunculara mümkün olduğunca fazla Türkçe metin yansıtmak

## Tek Kaynak Mantığı

Projede iki ana tek kaynak yapısı vardır:

1. Ortak oyun dosyaları
- Ana kaynak: `mod`
- Hedef paketler: `mod-client`, `mod-server`
- Araçlar: `tools/package/*`

2. Workshop metadata
- Ana kaynak: `tools/workshop/workshop_config.json`
- Yerelde üretilen dosyalar:
  - `tools/workshop/workshop_client.vdf`
  - `tools/workshop/workshop_server.vdf`
  - `%USERPROFILE%/workshop_upload_dst/client_upload.vdf`
  - `%USERPROFILE%/workshop_upload_dst/server_upload.vdf`

## Tipik Akış

### 1. Çeviri verisi değiştiyse

```bash
python tools/generate/generate_strings_lua.py
python tools/generate/generate_speech_lua.py
python tools/generate/generate_stageactor_lua.py
python tools/generate/generate_skin_lua.py
python tools/package/sync_packages.py --live
```

Not:
- Generate scriptleri önce ortak çıktıyı `mod` içine yazar.
- Ardından ortak dosyaları `mod-client` ve `mod-server` klasörlerine senkronlar.
- `--live`, yerel DST mod klasörlerine de kopyalar.

### 2. Paket metadata'sı değiştiyse

Örnek:
- `modmain.lua`
- `modinfo.lua`
- sürüm, açıklama, yazar bilgisi

```bash
python tools/package/render_package_files.py --live
```

Kaynak dosyalar:
- `tools/package/package_config.json`
- `tools/package/templates/modmain.lua.tmpl`
- `tools/package/templates/modinfo.lua.tmpl`

### 3. Workshop metadata değiştiyse

```bash
python tools/workshop/render_workshop_files.py
```

Kaynak dosyalar:
- `tools/workshop/workshop_config.json`
- `tools/workshop/templates/workshop_item.vdf.tmpl`

### 4. Workshop güncellemesi basılacaksa

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target client -SteamCmdPath "<path-to-steamcmd.exe>" -SteamUser "<steam-username>"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target server -SteamCmdPath "<path-to-steamcmd.exe>" -SteamUser "<steam-username>"
```

Not:
- `upload_workshop.ps1`, çalışmadan önce `render_workshop_files.py` komutunu otomatik çağırır.
- VDF dosyaları bu yüzden elde güncellenmez.

## Üretim Akışı

### 1. Kaynak veriyi çıkar

`tools/extract` altındaki scriptler İngilizce/Türkçe veri dosyalarını çıkarır:

- `tools/extract/extract_strings.py`
- `tools/extract/extract_speech.py`
- `tools/extract/extract_stageactor.py`
- `tools/extract/extract_skin.py`

### 2. Çeviri verisini güncelle

Temel JSON dosyaları `data/json` altında tutulur:

- `data/json/strings_tr.json`
- `data/json/speech_tr.json`
- `data/json/stageactor_tr.json`
- `data/json/skin_tr.json`

### 3. Lua çıktısını üret

Üretim scriptleri `tools/generate` altındadır:

- `tools/generate/generate_strings_lua.py`
- `tools/generate/generate_speech_lua.py`
- `tools/generate/generate_stageactor_lua.py`
- `tools/generate/generate_skin_lua.py`

### 4. Paket dosyalarını render et

```bash
python tools/package/render_package_files.py
```

### 5. Ortak dosyaları senkronla

```bash
python tools/package/sync_packages.py
```

Canlı klasörleri de güncellemek için:

```bash
python tools/package/render_package_files.py --live
python tools/package/sync_packages.py --live
```

## Runtime Düzeltmeleri

Sadece veri üretimi yetmediğinde şu katmanlar kullanılır:

- `compat_skilltree.lua`
- `compat_levels.lua`
- `compat_stageactor_cache.lua`
- `compat_shb_guard.lua`
- `tr_dialogue_fixes.lua`
- `tr_speech_fixes.lua`
- `tr_speech_polish.lua`
- `tr_pearl.lua`
- `tr_yotb.lua`

## Paket Rolleri

### Client modu

- Ana menü ve frontend çevirileri
- UI metinleri
- Skill tree açıklamaları
- Craft ve bazı client-cache düzeltmeleri
- Sahne performansları ve stageactor cache düzeltmeleri
- Konuşma balonu ve font özel düzeltmeleri

### Server modu

- Paylaşılan çeviri verilerini sunucu tarafında yükler
- Ortak event, NPC ve dünya metinlerini misafir oyunculara mümkün olduğunca Türkçe yansıtır
- Tam deneyim için client moduyla birlikte kullanılmalıdır

## Workshop Bilgileri

Ana dosyalar:

- `tools/workshop/workshop_config.json`
- `tools/workshop/render_workshop_files.py`
- `tools/workshop/upload_workshop.ps1`

Mevcut Workshop kimlikleri:

- Client: `3680639043`
- Server: `3680639406`

## Canlı Mod Klasörleri

Yerel testte kullanılan canlı mod klasörleri:

- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-client`
- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-server`

Not:
- Proje klasörleri ile canlı oyun klasörleri farklıdır.
- Oyunda test etmeden önce güncel dosyaların canlı mod klasörlerine kopyalanmış olması gerekir.

## Bakım Notları

- Geçici extract klasörleri proje kökünde tutulmamalıdır.
- Artık kullanılmayan ikon varyasyonları projede bırakılmamalıdır.
- Kullanılmayan uyumluluk dosyaları temizlenmelidir.
- Yeni lokalizasyon kararları mümkünse önce `DST_LOCALIZATION_RESEARCH.md` içine not edilmelidir.
- `data/source_scripts` yerel referans içindir; repoya dahil edilmez.
