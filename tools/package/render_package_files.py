from __future__ import annotations

import argparse
import json
from pathlib import Path
from string import Template


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).with_name("package_config.json")
TEMPLATES_DIR = Path(__file__).with_name("templates")
LIVE_TARGETS = {
    "client": Path(r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-client"),
    "server": Path(r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-server"),
}


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _load_template(name: str) -> Template:
    return Template((TEMPLATES_DIR / name).read_text(encoding="utf-8"))


def _lua_bool(value: bool) -> str:
    return "true" if value else "false"


def _merge_dict(base: dict, override: dict) -> dict:
    merged = dict(base)
    merged.update(override)
    return merged


def _lua_string_list(items: list[str]) -> str:
    quoted = ", ".join(f'"{item}"' for item in items)
    return "{" + quoted + "}"


def _render_modimports(paths: list[str], indent: str = "") -> str:
    return "\n".join(f'{indent}modimport("{path}")' for path in paths)


def _optional_block(block: str) -> str:
    return f"{block}\n\n" if block else ""


def _copy_if_changed(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or src.read_bytes() != dst.read_bytes():
        dst.write_bytes(src.read_bytes())
        return True
    return False


def _render_modmain(package_cfg: dict, common_cfg: dict) -> str:
    merged_cfg = _merge_dict(common_cfg["modmain_defaults"], package_cfg)

    game_post_init_block = ""
    if merged_cfg["include_game_post_init"]:
        game_post_init_block = "\n".join(
            [
                "AddGamePostInit(function()",
                "    ApplyAllTranslations()",
                "end)",
            ]
        )

    frontend_hook_block = ""
    if merged_cfg["include_frontend_hook"]:
        frontend_hook_block = "\n".join(
            [
                'if GLOBAL.rawget(GLOBAL, "TheFrontEnd") then',
                "    local old_on_become_active = GLOBAL.TheFrontEnd.OnBecomeActive",
                "    if old_on_become_active then",
                "        GLOBAL.TheFrontEnd.OnBecomeActive = function(self, ...)",
                "            local ret = old_on_become_active(self, ...)",
                "            STRINGS = GLOBAL.STRINGS",
                _render_modimports(common_cfg["frontend_hook_imports"], indent="            "),
                "            return ret",
                "        end",
                "    end",
                "end",
            ]
        )

    template = _load_template("modmain.lua.tmpl")
    return template.substitute(
        modmain_header=merged_cfg["modmain_header"],
        early_imports=_render_modimports(common_cfg["early_imports"]),
        early_comment_block=_optional_block(merged_cfg["early_comment"]),
        frontend_imports=_render_modimports(common_cfg["frontend_imports"]),
        apply_imports=_render_modimports(common_cfg["apply_imports"], indent="    "),
        print_prefix=merged_cfg["print_prefix"],
        success_message=merged_cfg["success_message"],
        game_post_init_block=_optional_block(game_post_init_block),
        frontend_hook_block=_optional_block(frontend_hook_block),
        intro_message=merged_cfg["intro_message"],
    )


def _render_modinfo(package_cfg: dict, common_cfg: dict) -> str:
    info = _merge_dict(common_cfg["modinfo_defaults"], package_cfg["modinfo"])
    icon_block = '-- icon_atlas = "modicon.xml"\n-- icon = "modicon.tex"'
    if info["with_icon"]:
        icon_block = 'icon_atlas = "modicon.xml"\nicon = "modicon.tex"'

    template = _load_template("modinfo.lua.tmpl")
    return template.substitute(
        header=info["header"],
        name=info["name"],
        author=info["author"],
        version=info["version"],
        description_en=info["description_en"],
        description_tr=info["description_tr"],
        api_version=info["api_version"],
        dst_compatible=_lua_bool(info["dst_compatible"]),
        dont_starve_compatible=_lua_bool(info["dont_starve_compatible"]),
        reign_of_giants_compatible=_lua_bool(info["reign_of_giants_compatible"]),
        shipwrecked_compatible=_lua_bool(info["shipwrecked_compatible"]),
        client_only_mod=_lua_bool(info["client_only_mod"]),
        all_clients_require_mod=_lua_bool(info["all_clients_require_mod"]),
        icon_block=icon_block,
        server_filter_tags=_lua_string_list(info["server_filter_tags"]),
        priority=info["priority"],
    )


def render_package_files(include_live: bool = False) -> None:
    config = _load_config()
    common_cfg = config["common"]

    for package_name, package_cfg in config["packages"].items():
        package_root = PROJECT_ROOT / package_cfg["folder"]
        modmain_path = package_root / "modmain.lua"
        modinfo_path = package_root / "modinfo.lua"

        modmain_path.write_text(_render_modmain(package_cfg, common_cfg), encoding="utf-8")
        modinfo_path.write_text(_render_modinfo(package_cfg, common_cfg), encoding="utf-8")
        print(f"rendered {modmain_path}")
        print(f"rendered {modinfo_path}")

        live_root = LIVE_TARGETS.get(package_name)
        if include_live and live_root and live_root.exists():
            live_modmain = live_root / "modmain.lua"
            live_modinfo = live_root / "modinfo.lua"
            if _copy_if_changed(modmain_path, live_modmain):
                print(f"synced {live_modmain}")
            if _copy_if_changed(modinfo_path, live_modinfo):
                print(f"synced {live_modinfo}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render package-specific modmain.lua and modinfo.lua files.")
    parser.add_argument("--live", action="store_true", help="Also copy rendered files into the local live DST mod folders.")
    args = parser.parse_args()
    render_package_files(include_live=args.live)


if __name__ == "__main__":
    main()
