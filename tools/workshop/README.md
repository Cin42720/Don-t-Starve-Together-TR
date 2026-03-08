# Workshop

Bu klasör Steam Workshop metadata ve upload yardımcıları için kullanılır.

## Dosyalar

- `workshop_config.json`
  Client/server Workshop metadata'sının tek kaynağı
- `templates/workshop_item.vdf.tmpl`
  VDF şablonu
- `render_workshop_files.py`
  Proje içi ve ASCII-safe SteamCMD VDF dosyalarını üretir
- `upload_workshop.ps1`
  SteamCMD ile yükleme/güncelleme yardımcı scripti
  Not: Script çalışmadan önce `render_workshop_files.py` komutunu otomatik çağırır.

## Render

```bash
python tools/workshop/render_workshop_files.py
```

Bu komut iki çıktı üretir:

- `tools/workshop/workshop_client.vdf`
- `tools/workshop/workshop_server.vdf`

ve SteamCMD için ASCII-safe kopyaları:

- `C:/Users/husey/workshop_upload_dst/client_upload.vdf`
- `C:/Users/husey/workshop_upload_dst/server_upload.vdf`
