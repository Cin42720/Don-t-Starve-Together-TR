from __future__ import annotations

import json
import os
from pathlib import Path
from string import Template


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSHOP_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = WORKSHOP_ROOT / "workshop_config.json"
TEMPLATE_PATH = WORKSHOP_ROOT / "templates" / "workshop_item.vdf.tmpl"


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _load_template() -> Template:
    return Template(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_if_changed(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def _render_vdf(template: Template, values: dict) -> str:
    return template.substitute(values)


def render_workshop_files() -> None:
    config = _load_config()
    template = _load_template()
    common = config["common"]
    ascii_root = Path(os.path.expandvars(common["ascii_output_root"])).expanduser()

    for target_name, target_cfg in config["targets"].items():
        base_values = {
            "appid": common["appid"],
            "publishedfileid": target_cfg["publishedfileid"],
            "visibility": common["visibility"],
            "title": target_cfg["title"],
            "description": target_cfg["description"],
            "change_note": common["change_note"],
        }

        project_values = {
            **base_values,
            "contentfolder": str((PROJECT_ROOT / target_cfg["project_contentfolder"]).resolve()),
            "previewfile": str((PROJECT_ROOT / target_cfg["project_previewfile"]).resolve()),
        }
        project_output = WORKSHOP_ROOT / target_cfg["project_output"]
        _write_if_changed(project_output, _render_vdf(template, project_values))
        print(f"rendered {project_output}")

        ascii_values = {
            **base_values,
            "contentfolder": target_cfg["ascii_contentfolder"],
            "previewfile": target_cfg["ascii_previewfile"],
        }
        ascii_output = ascii_root / target_cfg["ascii_output"]
        _write_if_changed(ascii_output, _render_vdf(template, ascii_values))
        print(f"rendered {ascii_output}")


if __name__ == "__main__":
    render_workshop_files()
