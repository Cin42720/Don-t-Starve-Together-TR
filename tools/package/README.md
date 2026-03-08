# Package Sync

Bu klasor, ortak mod icerigini yayin paketlerine senkronlamak ve paket ozel dosyalari tek kaynaktan uretmek icin kullanilir.

## Mantik

- `mod` ortak kaynak paketidir
- `mod-client` istemciye ozel yayin paketidir
- `mod-server` sunucuya ozel yayin paketidir

Paylasilan klasorler:

- `fonts`
- `scripts`

Bu klasorler `mod` icinden alinir ve diger paketlere kopyalanir.

## Shared Sync

```bash
python tools/package/sync_packages.py
```

Canli DST mod klasorlerine de basmak icin:

```bash
python tools/package/sync_packages.py --live
```

## Paket Ozel Dosyalar

`modmain.lua` ve `modinfo.lua` dosyalari asagidaki kaynaklardan uretilir:

- `package_config.json`
- `templates/modmain.lua.tmpl`
- `templates/modinfo.lua.tmpl`
- `render_package_files.py`

`package_config.json` icinde ortak varsayilanlar `common.modmain_defaults` ve `common.modinfo_defaults` altinda tutulur. Paketler sadece farkli alanlari override eder.

Render komutu:

```bash
python tools/package/render_package_files.py
```

Canli DST mod klasorlerine de kopyalamak icin:

```bash
python tools/package/render_package_files.py --live
```
