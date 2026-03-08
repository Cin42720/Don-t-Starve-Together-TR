# Tools Düzeni

`tools` klasörü beş ana bölüme ayrılmıştır:

- `extract`
  Oyundan veri çıkaran scriptler
- `translate`
  JSON verilerini çeviri ve kalite kontrol hattından geçiren scriptler
- `generate`
  Türkçe JSON verisinden Lua çıktı üreten scriptler
- `package`
  `mod` içindeki ortak dosyaları `mod-client` ve `mod-server` paketlerine senkronlayan ve paket özel dosyaları render eden araçlar
- `workshop`
  Steam Workshop yükleme/güncelleme yardımcı dosyaları

## Örnek Komutlar

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

- Generate scriptleri ortak çıktıyı önce `mod` içine yazar.
- Ardından ortak dosyaları otomatik olarak `mod-client` ve `mod-server` klasörlerine senkronlar.

### Package

```bash
python tools/package/render_package_files.py
python tools/package/sync_packages.py
```

Canlı DST mod klasörlerine de basmak için:

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

- Scriptler proje kökünden çalıştırılacak şekilde düşünülmüştür.
- Kaynak JSON veri `data/json`, oyundan çıkarılan Lua kaynakları `data/source_scripts` altında tutulur.
- Üretilen çıktı `mod`, `mod-client` ve `mod-server` altında yer alır.
