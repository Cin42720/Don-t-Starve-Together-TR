# Tools Duzeni

`tools` klasoru bes ana bolume ayrilmistir:

- `extract`
  Oyundan veri cikaran scriptler
- `translate`
  JSON verilerini ceviri ve kalite kontrol hattindan geciren scriptler
- `generate`
  Turkce JSON verisinden Lua cikti ureten scriptler
- `package`
  `mod` icindeki ortak dosyalari `mod-client` ve `mod-server` paketlerine senkronlayan ve paket ozel dosyalari render eden araclar
- `workshop`
  Steam Workshop yukleme/guncelleme yardimci dosyalari

## Ornek Komutlar

### Extract

```bash
python tools/extract/extract_strings.py
python tools/extract/extract_speech.py
python tools/extract/extract_stageactor.py
python tools/extract/extract_skin.py
```

### Translate

```bash
python tools/translate/translate_strings.py
python tools/translate/translate_speech.py
python tools/translate/translate_stageactor.py
python tools/translate/translate_skin.py
```

### Generate

```bash
python tools/generate/generate_strings_lua.py
python tools/generate/generate_speech_lua.py
python tools/generate/generate_stageactor_lua.py
python tools/generate/generate_skin_lua.py
```

Not:

- Generate scriptleri ortak ciktiyi once `mod` icine yazar.
- Ardindan ortak dosyalari otomatik olarak `mod-client` ve `mod-server` klasorlerine senkronlar.

### Package

```bash
python tools/package/render_package_files.py
python tools/package/sync_packages.py
```

Canli DST mod klasorlerine de basmak icin:

```bash
python tools/package/render_package_files.py --live
python tools/package/sync_packages.py --live
```

### Workshop

```bash
python tools/workshop/render_workshop_files.py
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target client -SteamCmdPath "C:\path\to\steamcmd.exe" -SteamUser "steam_user"
```

Not:

- Scriptler proje kokunden calistirilacak sekilde dusunulmustur.
- Kaynak JSON veri `data/json`, oyundan cikarilan Lua kaynaklari `data/source_scripts` altinda tutulur.
- Uretilen cikti `mod`, `mod-client` ve `mod-server` altinda yer alir.
