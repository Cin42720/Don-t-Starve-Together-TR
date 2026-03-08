# Don't Starve Together Türkçe Çeviri Projesi

Bu proje, `Don't Starve Together` için hazırlanan Türkçe çeviri paketlerini ve bunların üretim araçlarını içerir.

Proje üç ana mod paketi etrafında düzenlenmiştir:

- `mod`: ortak kaynak paket
- `mod-client`: istemci tarafı yayın paketi
- `mod-server`: sunucu tarafı yayın paketi

## Hedef

Projenin amacı:

- ana oyun metinlerini Türkçeleştirmek
- karakter konuşmalarını ve etkinlik diyaloglarını düzeltmek
- istemciye özel UI, skill tree ve benzeri ekranları çevirmek
- sunucu tarafında misafir oyunculara mümkün olduğunca fazla Türkçe metin yansıtmak

## Klasör Yapısı

- [`data`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/data)
  - `data/json`: İngilizce/Türkçe JSON verileri ve sözlük
  - `data/source_scripts`: oyundan çıkarılmış kaynak Lua dosyaları

- [`tools`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools)
  - `extract`
  - `translate`
  - `generate`
  - `package`
  - `workshop`

- [`mod`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/mod)
  Ortak kaynak paket. Paylaşılan `scripts` ve `fonts` içeriğinin tek kaynağıdır.

- [`mod-client`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/mod-client)
  İstemci tarafı yayın paketi.

- [`mod-server`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/mod-server)
  Sunucu tarafı yayın paketi.

- [`DST_LOCALIZATION_RESEARCH.md`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/DST_LOCALIZATION_RESEARCH.md)
  Terim politikası, lore notları ve lokalizasyon kararları.
- [`NOTICE.md`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/NOTICE.md)
  Lisans kapsamı ve oyun-türevi içerik notları.

## Tek Kaynak Mantığı

Projede iki ana "tek kaynak" yapısı vardır:

1. Ortak oyun dosyaları
- Ana kaynak: `mod`
- Hedef paketler: `mod-client`, `mod-server`
- Senkron araçları: `tools/package/*`

2. Workshop metadata
- Ana kaynak: `tools/workshop/workshop_config.json`
- Üretilen dosyalar:
  - `tools/workshop/workshop_client.vdf`
  - `tools/workshop/workshop_server.vdf`
  - `C:/Users/husey/workshop_upload_dst/client_upload.vdf`
  - `C:/Users/husey/workshop_upload_dst/server_upload.vdf`

## Hangi Durumda Ne Yapılır

### 1. Sadece çeviri metni değiştirdin

JSON veya `scripts/languages/*.lua` tarafında bir değişiklikten sonra tipik akış:

```bash
python tools/generate/generate_strings_lua.py
python tools/generate/generate_speech_lua.py
python tools/generate/generate_stageactor_lua.py
python tools/generate/generate_skin_lua.py
python tools/package/sync_packages.py --live
```

Not:
- Generate scriptleri ortak çıktıyı önce `mod` içine yazar.
- Ardından `mod-client` ve `mod-server` paketlerini otomatik senkronlar.
- `--live`, yerel DST mod klasörlerine de kopyalar.

### 2. Paket metadata'sı değişti

Örnek:
- `modmain.lua`
- `modinfo.lua`
- package header / author / version / description

Bu durumda:

```bash
python tools/package/render_package_files.py --live
```

Bu komut:
- `mod`, `mod-client`, `mod-server` altındaki `modmain.lua` ve `modinfo.lua` dosyalarını yeniden üretir
- istenirse canlı DST mod klasörlerine de kopyalar

Kaynak dosyalar:
- `tools/package/package_config.json`
- `tools/package/templates/modmain.lua.tmpl`
- `tools/package/templates/modinfo.lua.tmpl`

### 3. Workshop açıklama / başlık / publishedfileid / hedef yol değişti

Bu durumda:

```bash
python tools/workshop/render_workshop_files.py
```

Kaynak dosyalar:
- `tools/workshop/workshop_config.json`
- `tools/workshop/templates/workshop_item.vdf.tmpl`

### 4. Workshop'a yeni güncelleme basacaksın

Normal akış:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target client -SteamCmdPath "C:\Users\husey\Downloads\steamcmd\steamcmd.exe" -SteamUser "husoaga45"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target server -SteamCmdPath "C:\Users\husey\Downloads\steamcmd\steamcmd.exe" -SteamUser "husoaga45"
```

Not:
- `upload_workshop.ps1`, çalışmadan önce `render_workshop_files.py` komutunu otomatik çağırır.
- Yani VDF'leri elle güncel tutmak gerekmez.

## Temel Üretim Akışı

### 1. Kaynak veriyi çıkar

`tools/extract` altındaki scriptler İngilizce/Türkçe veri dosyalarını çıkarır:

- `tools/extract/extract_strings.py`
- `tools/extract/extract_speech.py`
- `tools/extract/extract_stageactor.py`
- `tools/extract/extract_skin.py`

### 2. Çeviri verisini güncelle

Kaynak JSON dosyaları `data/json` altında tutulur:

- `data/json/strings_tr.json`
- `data/json/speech_tr.json`
- `data/json/stageactor_tr.json`
- `data/json/skin_tr.json`

### 3. Lua çıktısını üret

Üretim scriptleri `tools/generate` altında durur:

- `tools/generate/generate_strings_lua.py`
- `tools/generate/generate_speech_lua.py`
- `tools/generate/generate_stageactor_lua.py`
- `tools/generate/generate_skin_lua.py`

### 4. Gerekirse paket özel dosyaları render et

```bash
python tools/package/render_package_files.py
```

### 5. Gerekirse ortak dosyaları manuel senkronla

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

## Client ve Server Paketlerinin Rolü

### Client modu ne yapar

- ana menü ve frontend çevirileri
- UI metinleri
- skill tree açıklamaları
- craft ve bazı client-cache düzeltmeleri
- sahne performansları ve stageactor cache düzeltmeleri
- konuşma balonu/font özel düzeltmeleri

### Server modu ne yapar

- paylaşılan çeviri verilerini sunucu tarafında yükler
- ortak event/NPC/world metinlerini misafir oyunculara mümkün olduğunca Türkçe yansıtır
- tam deneyim için client moduyla birlikte kullanılmalıdır

## Workshop Bilgileri

Workshop yardımcı dosyaları:

- [`tools/workshop/workshop_client.vdf`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/workshop_client.vdf)
- [`tools/workshop/workshop_server.vdf`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/workshop_server.vdf)
- [`tools/workshop/workshop_config.json`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/workshop_config.json)
- [`tools/workshop/render_workshop_files.py`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/render_workshop_files.py)
- [`tools/workshop/upload_workshop.ps1`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/upload_workshop.ps1)

Mevcut Workshop kimlikleri:

- Client: `3680639043`
- Server: `3680639406`

## Canlı Mod Klasörleri

Yerel testte kullanılan canlı mod klasörleri:

- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-client`
- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-server`

Not:

- Proje içindeki kaynak klasörler ile canlı oyun klasörleri farklıdır.
- Oyunda test etmeden önce güncel dosyaların canlı mod klasörlerine kopyalanmış olması gerekir.

## Bakım Notları

- Geçici extract klasörleri proje kökünde tutulmamalı.
- Eski `modicon_v2` gibi artık kullanılmayan ikon varyasyonları tekrar üretilmemeli.
- Kullanılmayan uyumluluk dosyaları projede bırakılmamalı.
- Yeni lokalizasyon kararları mümkünse önce `DST_LOCALIZATION_RESEARCH.md` içine not edilmelidir.
- `data/source_scripts` yerel referans içindir; repoya dahil edilmez.
