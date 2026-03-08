# Data Düzeni

`data` klasörü iki ana bölüme ayrılmıştır:

- `json`
  Çeviri hattının kullandığı İngilizce/Türkçe JSON verileri ve `glossary.json`

- `source_scripts`
  Oyundan çıkarılmış veya referans için tutulan kaynak Lua scriptleri

## json

Burada bulunan başlıca dosyalar:

- `strings_en.json`
- `strings_tr.json`
- `speech_en.json`
- `speech_tr.json`
- `stageactor_en.json`
- `stageactor_tr.json`
- `skin_en.json`
- `skin_tr.json`
- `glossary.json`

## source_scripts

Burada bulunan dosyalar, extract işlemlerinde ya da manuel karşılaştırmalarda kullanılan kaynak scriptlerdir.

Örnekler:

- `strings.lua`
- `speech_wilson.lua`
- `speech_wendy.lua`
- `speech_waxwell.lua`

Not:

- Çeviri scriptleri JSON veriyi `data/json` altından okur.
- Extract scriptleri varsayılan olarak kaynak Lua dosyalarını `data/source_scripts` altında arar.
