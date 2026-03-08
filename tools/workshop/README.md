# Workshop

Bu klasor Steam Workshop metadata ve upload yardimcilari icin kullanilir.

## Dosyalar

- `workshop_config.json`
  Client/server Workshop metadata'sinin tek kaynagi
- `templates/workshop_item.vdf.tmpl`
  VDF sablonu
- `render_workshop_files.py`
  Proje ici ve ASCII-safe SteamCMD VDF dosyalarini uretir
- `upload_workshop.ps1`
  SteamCMD ile yukleme/guncelleme yardimci scripti
  Not: Script calismadan once `render_workshop_files.py` komutunu otomatik cagirir.

## Render

```bash
python tools/workshop/render_workshop_files.py
```

Bu komut iki cikti uretir:

- `tools/workshop/workshop_client.vdf`
- `tools/workshop/workshop_server.vdf`

ve SteamCMD icin ASCII-safe kopyalari:

- `C:/Users/husey/workshop_upload_dst/client_upload.vdf`
- `C:/Users/husey/workshop_upload_dst/server_upload.vdf`
