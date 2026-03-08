# Don't Starve Together Turkce Ceviri Projesi

Bu proje, `Don't Starve Together` icin hazirlanan Turkce ceviri paketlerini ve bunlarin uretim araclarini icerir.

Proje uc ana mod paketi etrafinda duzenlenmistir:

- `mod`: ortak kaynak paket
- `mod-client`: istemci tarafi yayin paketi
- `mod-server`: sunucu tarafi yayin paketi

## Hedef

Projenin amaci:

- ana oyun metinlerini Turkcelestirmek
- karakter konusmalarini ve etkinlik diyaloglarini duzeltmek
- istemciye ozel UI, skill tree ve benzeri ekranlari cevirmek
- sunucu tarafinda misafir oyunculara mumkun oldugunca fazla Turkce metin yansitmak

## Klasor Yapisi

- [`data`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/data)
  - `data/json`: Ingilizce/Turkce JSON verileri ve sozluk
  - `data/source_scripts`: oyundan cikarilmis kaynak Lua dosyalari

- [`tools`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools)
  - `extract`
  - `translate`
  - `generate`
  - `package`
  - `workshop`

- [`mod`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/mod)
  Ortak kaynak paket. Paylasilan `scripts` ve `fonts` iceriginin tek kaynagidir.

- [`mod-client`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/mod-client)
  Istemci tarafi yayin paketi.

- [`mod-server`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/mod-server)
  Sunucu tarafi yayin paketi.

- [`DST_LOCALIZATION_RESEARCH.md`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/DST_LOCALIZATION_RESEARCH.md)
  Terim politikasi, lore notlari ve lokalizasyon kararlari.
- [`NOTICE.md`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/NOTICE.md)
  Lisans kapsami ve oyun-turevi icerik notlari.

## Tek Kaynak Mantigi

Projede iki ana "tek kaynak" yapisi vardir:

1. Ortak oyun dosyalari
- Ana kaynak: `mod`
- Hedef paketler: `mod-client`, `mod-server`
- Senkron araclari: `tools/package/*`

2. Workshop metadata
- Ana kaynak: `tools/workshop/workshop_config.json`
- Uretilen dosyalar:
  - `tools/workshop/workshop_client.vdf`
  - `tools/workshop/workshop_server.vdf`
  - `C:/Users/husey/workshop_upload_dst/client_upload.vdf`
  - `C:/Users/husey/workshop_upload_dst/server_upload.vdf`

## Hangi Durumda Ne Yapilir

### 1. Sadece ceviri metni degistirdin

JSON veya `scripts/languages/*.lua` tarafinda bir degisiklikten sonra tipik akis:

```bash
python tools/generate/generate_strings_lua.py
python tools/generate/generate_speech_lua.py
python tools/generate/generate_stageactor_lua.py
python tools/generate/generate_skin_lua.py
python tools/package/sync_packages.py --live
```

Not:
- Generate scriptleri ortak ciktiyi once `mod` icine yazar.
- Ardindan `mod-client` ve `mod-server` paketlerini otomatik senkronlar.
- `--live`, yerel DST mod klasorlerine de kopyalar.

### 2. Paket metadata'si degisti

Ornek:
- `modmain.lua`
- `modinfo.lua`
- package header / author / version / description

Bu durumda:

```bash
python tools/package/render_package_files.py --live
```

Bu komut:
- `mod`, `mod-client`, `mod-server` altindaki `modmain.lua` ve `modinfo.lua` dosyalarini yeniden uretir
- istenirse canli DST mod klasorlerine de kopyalar

Kaynak dosyalar:
- `tools/package/package_config.json`
- `tools/package/templates/modmain.lua.tmpl`
- `tools/package/templates/modinfo.lua.tmpl`

### 3. Workshop aciklama / baslik / publishedfileid / hedef yol degisti

Bu durumda:

```bash
python tools/workshop/render_workshop_files.py
```

Kaynak dosyalar:
- `tools/workshop/workshop_config.json`
- `tools/workshop/templates/workshop_item.vdf.tmpl`

### 4. Workshop'a yeni guncelleme basacaksin

Normal akis:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target client -SteamCmdPath "C:\Users\husey\Downloads\steamcmd\steamcmd.exe" -SteamUser "husoaga45"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target server -SteamCmdPath "C:\Users\husey\Downloads\steamcmd\steamcmd.exe" -SteamUser "husoaga45"
```

Not:
- `upload_workshop.ps1`, calismadan once `render_workshop_files.py` komutunu otomatik cagirir.
- Yani VDF'leri elle guncel tutmak gerekmez.

## Temel Uretim Akisi

### 1. Kaynak veriyi cikar

`tools/extract` altindaki scriptler Ingilizce/Turkce veri dosyalarini cikarir:

- `tools/extract/extract_strings.py`
- `tools/extract/extract_speech.py`
- `tools/extract/extract_stageactor.py`
- `tools/extract/extract_skin.py`

### 2. Ceviri verisini guncelle

Kaynak JSON dosyalari `data/json` altinda tutulur:

- `data/json/strings_tr.json`
- `data/json/speech_tr.json`
- `data/json/stageactor_tr.json`
- `data/json/skin_tr.json`

### 3. Lua ciktisini uret

Uretim scriptleri `tools/generate` altinda durur:

- `tools/generate/generate_strings_lua.py`
- `tools/generate/generate_speech_lua.py`
- `tools/generate/generate_stageactor_lua.py`
- `tools/generate/generate_skin_lua.py`

### 4. Gerekirse paket ozel dosyalari render et

```bash
python tools/package/render_package_files.py
```

### 5. Gerekirse ortak dosyalari manuel senkronla

```bash
python tools/package/sync_packages.py
```

Canli klasorleri de guncellemek icin:

```bash
python tools/package/render_package_files.py --live
python tools/package/sync_packages.py --live
```

## Runtime Duzeltmeleri

Sadece veri uretimi yetmediginde su katmanlar kullanilir:

- `compat_skilltree.lua`
- `compat_levels.lua`
- `compat_stageactor_cache.lua`
- `compat_shb_guard.lua`
- `tr_dialogue_fixes.lua`
- `tr_speech_fixes.lua`
- `tr_speech_polish.lua`
- `tr_pearl.lua`
- `tr_yotb.lua`

## Client ve Server Paketlerinin Rolu

### Client modu ne yapar

- ana menu ve frontend cevirileri
- UI metinleri
- skill tree aciklamalari
- craft ve bazi client-cache duzeltmeleri
- sahne performanslari ve stageactor cache duzeltmeleri
- konusma balonu/font ozel duzeltmeleri

### Server modu ne yapar

- paylasilan ceviri verilerini sunucu tarafinda yukler
- ortak event/NPC/world metinlerini misafir oyunculara mumkun oldugunca Turkce yansitir
- tam deneyim icin client moduyla birlikte kullanilmalidir

## Workshop Bilgileri

Workshop yardimci dosyalari:

- [`tools/workshop/workshop_client.vdf`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/workshop_client.vdf)
- [`tools/workshop/workshop_server.vdf`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/workshop_server.vdf)
- [`tools/workshop/workshop_config.json`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/workshop_config.json)
- [`tools/workshop/render_workshop_files.py`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/render_workshop_files.py)
- [`tools/workshop/upload_workshop.ps1`](c:/Users/husey/OneDrive/Desktop/Test%20%C3%87eviri/tools/workshop/upload_workshop.ps1)

Mevcut Workshop kimlikleri:

- Client: `3680639043`
- Server: `3680639406`

## Canli Mod Klasorleri

Yerel testte kullanilan canli mod klasorleri:

- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-client`
- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-server`

Not:

- Proje icindeki kaynak klasorler ile canli oyun klasorleri farklidir.
- Oyunda test etmeden once guncel dosyalarin canli mod klasorlerine kopyalanmis olmasi gerekir.

## Bakim Notlari

- Gecici extract klasorleri proje kokunde tutulmamali.
- Eski `modicon_v2` gibi artik kullanilmayan ikon varyasyonlari tekrar uretilmemeli.
- Kullanilmayan uyumluluk dosyalari projede birakilmamali.
- Yeni lokalizasyon kararlari mumkunse once `DST_LOCALIZATION_RESEARCH.md` icine not edilmelidir.
- `data/source_scripts` yerel referans icindir; repoya dahil edilmez.
