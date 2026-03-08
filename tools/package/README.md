# Package Sync

Bu klasör, ortak mod içeriğini yayın paketlerine senkronlamak ve paket özel dosyaları tek kaynaktan üretmek için kullanılır.

## Mantık

- `mod` ortak kaynak paketidir
- `mod-client` istemciye özel yayın paketidir
- `mod-server` sunucuya özel yayın paketidir

Paylaşılan klasörler:

- `fonts`
- `scripts`

Bu klasörler `mod` içinden alınır ve diğer paketlere kopyalanır.

## Shared Sync

```bash
python tools/package/sync_packages.py
```

Canlı DST mod klasörlerine de basmak için:

```bash
python tools/package/sync_packages.py --live
```

## Paket Özel Dosyalar

`modmain.lua` ve `modinfo.lua` dosyaları aşağıdaki kaynaklardan üretilir:

- `package_config.json`
- `templates/modmain.lua.tmpl`
- `templates/modinfo.lua.tmpl`
- `render_package_files.py`

`package_config.json` içinde ortak varsayılanlar `common.modmain_defaults` ve `common.modinfo_defaults` altında tutulur. Paketler sadece farklı alanları override eder.

Render komutu:

```bash
python tools/package/render_package_files.py
```

Canlı DST mod klasörlerine de kopyalamak için:

```bash
python tools/package/render_package_files.py --live
```
