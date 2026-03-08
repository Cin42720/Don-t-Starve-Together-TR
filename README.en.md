# Don't Starve Together Turkish Translation Project

Türkçe sürüm: [README.md](./README.md)

This repository contains the Turkish translation packages, build tools, and Workshop publishing workflow for `Don't Starve Together`.

## Structure

- [`data`](./data)
  - `data/json`: Translation data and glossary files
  - `data/source_scripts`: Source Lua files kept for local reference
- [`tools`](./tools)
  - `extract`
  - `translate`
  - `generate`
  - `package`
  - `workshop`
- [`mod`](./mod): Shared source package
- [`mod-client`](./mod-client): Client-side release package
- [`mod-server`](./mod-server): Server-side release package
- [`DST_LOCALIZATION_RESEARCH.md`](./DST_LOCALIZATION_RESEARCH.md): Terminology policy and localization notes
- [`NOTICE.md`](./NOTICE.md): Licensing scope and derivative-content notes

## Goal

- Localize core game text into Turkish
- Improve character dialogue and event conversations
- Translate client-only UI, skill tree, and similar screens
- Push as much Turkish text as possible to guest players from the server side

## Single-Source Design

The project has two main single-source layers:

1. Shared game files
- Source package: `mod`
- Target packages: `mod-client`, `mod-server`
- Tools: `tools/package/*`

2. Workshop metadata
- Source file: `tools/workshop/workshop_config.json`
- Locally generated files:
  - `tools/workshop/workshop_client.vdf`
  - `tools/workshop/workshop_server.vdf`
  - `%USERPROFILE%/workshop_upload_dst/client_upload.vdf`
  - `%USERPROFILE%/workshop_upload_dst/server_upload.vdf`

## Typical Workflow

### 1. If translation data changed

```bash
python tools/generate/generate_strings_lua.py
python tools/generate/generate_speech_lua.py
python tools/generate/generate_stageactor_lua.py
python tools/generate/generate_skin_lua.py
python tools/package/sync_packages.py --live
```

Notes:
- Generate scripts first write shared output into `mod`.
- They then sync shared files into `mod-client` and `mod-server`.
- `--live` also copies files into the local DST mod folders.

### 2. If package metadata changed

Examples:
- `modmain.lua`
- `modinfo.lua`
- version, description, author metadata

```bash
python tools/package/render_package_files.py --live
```

Source files:
- `tools/package/package_config.json`
- `tools/package/templates/modmain.lua.tmpl`
- `tools/package/templates/modinfo.lua.tmpl`

### 3. If Workshop metadata changed

```bash
python tools/workshop/render_workshop_files.py
```

Source files:
- `tools/workshop/workshop_config.json`
- `tools/workshop/templates/workshop_item.vdf.tmpl`

### 4. If you want to publish a Workshop update

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target client -SteamCmdPath "<path-to-steamcmd.exe>" -SteamUser "<steam-username>"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\workshop\upload_workshop.ps1 -Target server -SteamCmdPath "<path-to-steamcmd.exe>" -SteamUser "<steam-username>"
```

Notes:
- `upload_workshop.ps1` automatically runs `render_workshop_files.py` first.
- VDF files should not be edited manually.

## Build Flow

### 1. Extract source data

Scripts under `tools/extract` generate English and Turkish data files:

- `tools/extract/extract_strings.py`
- `tools/extract/extract_speech.py`
- `tools/extract/extract_stageactor.py`
- `tools/extract/extract_skin.py`

### 2. Update translation data

Core JSON files are stored under `data/json`:

- `data/json/strings_tr.json`
- `data/json/speech_tr.json`
- `data/json/stageactor_tr.json`
- `data/json/skin_tr.json`

### 3. Generate Lua output

Generator scripts live under `tools/generate`:

- `tools/generate/generate_strings_lua.py`
- `tools/generate/generate_speech_lua.py`
- `tools/generate/generate_stageactor_lua.py`
- `tools/generate/generate_skin_lua.py`

### 4. Render package files

```bash
python tools/package/render_package_files.py
```

### 5. Sync shared files

```bash
python tools/package/sync_packages.py
```

To also update live DST folders:

```bash
python tools/package/render_package_files.py --live
python tools/package/sync_packages.py --live
```

## Runtime Fix Layers

When generated data is not enough, these layers are used:

- `compat_skilltree.lua`
- `compat_levels.lua`
- `compat_stageactor_cache.lua`
- `compat_shb_guard.lua`
- `tr_dialogue_fixes.lua`
- `tr_speech_fixes.lua`
- `tr_speech_polish.lua`
- `tr_pearl.lua`
- `tr_yotb.lua`

## Package Roles

### Client mod

- Main menu and frontend translations
- UI text
- Skill tree descriptions
- Craft and some client-cache fixes
- Stage performance and stageactor cache fixes
- Speech bubble and font-specific fixes

### Server mod

- Loads shared translation data on the server side
- Pushes as much shared event, NPC, and world text as possible to guest players
- Should be used together with the client mod for the full experience

## Workshop Information

Main files:

- `tools/workshop/workshop_config.json`
- `tools/workshop/render_workshop_files.py`
- `tools/workshop/upload_workshop.ps1`

Current Workshop IDs:

- Client: `3680639043`
- Server: `3680639406`

## Live Mod Folders

Live mod folders used for local testing:

- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-client`
- `C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-server`

Notes:
- Project folders and live game folders are different.
- Updated files must be copied into the live mod folders before in-game testing.

## Maintenance Notes

- Temporary extract folders should not stay in the project root.
- Unused icon variants should not stay in the project.
- Unused compatibility files should be removed.
- New localization decisions should be noted in `DST_LOCALIZATION_RESEARCH.md` when possible.
- `data/source_scripts` is for local reference only and is not committed.
