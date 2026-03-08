from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_MOD = PROJECT_ROOT / "mod"
PACKAGE_TARGETS = {
    "client": PROJECT_ROOT / "mod-client",
    "server": PROJECT_ROOT / "mod-server",
}
LIVE_TARGETS = {
    "client": Path(r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-client"),
    "server": Path(r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods\turkish-translation-server"),
}
SHARED_DIRS = ("fonts", "scripts")


def _copy_if_changed(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or src.read_bytes() != dst.read_bytes():
        shutil.copy2(src, dst)
        return True
    return False


def _remove_stale_entries(src_root: Path, dst_root: Path) -> tuple[int, int]:
    removed_files = 0
    removed_dirs = 0
    if not dst_root.exists():
        return removed_files, removed_dirs

    for path in sorted(dst_root.rglob("*"), reverse=True):
        rel = path.relative_to(dst_root)
        source_path = src_root / rel
        if source_path.exists():
            continue
        if path.is_file():
            path.unlink()
            removed_files += 1
        elif path.is_dir():
            try:
                path.rmdir()
                removed_dirs += 1
            except OSError:
                pass
    return removed_files, removed_dirs


def _sync_tree(src_root: Path, dst_root: Path) -> dict[str, int]:
    copied = 0
    created_dirs = 0

    if not src_root.exists():
        return {"copied": copied, "removed_files": 0, "removed_dirs": 0, "created_dirs": created_dirs}

    for path in src_root.rglob("*"):
        rel = path.relative_to(src_root)
        target = dst_root / rel
        if path.is_dir():
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
                created_dirs += 1
            continue
        if _copy_if_changed(path, target):
            copied += 1

    removed_files, removed_dirs = _remove_stale_entries(src_root, dst_root)
    return {
        "copied": copied,
        "removed_files": removed_files,
        "removed_dirs": removed_dirs,
        "created_dirs": created_dirs,
    }


def sync_shared_package_files(include_live: bool = False) -> dict[str, dict[str, int]]:
    results: dict[str, dict[str, int]] = {}

    for package_name, package_root in PACKAGE_TARGETS.items():
        package_stats = {"copied": 0, "removed_files": 0, "removed_dirs": 0, "created_dirs": 0}
        for shared_dir in SHARED_DIRS:
            src = SOURCE_MOD / shared_dir
            dst = package_root / shared_dir
            stats = _sync_tree(src, dst)
            for key, value in stats.items():
                package_stats[key] += value
        results[f"package:{package_name}"] = package_stats

    if include_live:
        for package_name, package_root in LIVE_TARGETS.items():
            if not package_root.exists():
                continue
            package_stats = {"copied": 0, "removed_files": 0, "removed_dirs": 0, "created_dirs": 0}
            for shared_dir in SHARED_DIRS:
                src = SOURCE_MOD / shared_dir
                dst = package_root / shared_dir
                stats = _sync_tree(src, dst)
                for key, value in stats.items():
                    package_stats[key] += value
            results[f"live:{package_name}"] = package_stats

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync shared mod files from mod/ into mod-client/ and mod-server/.")
    parser.add_argument("--live", action="store_true", help="Also sync shared files into the local live DST mod folders.")
    args = parser.parse_args()

    results = sync_shared_package_files(include_live=args.live)
    for target, stats in results.items():
        print(
            f"{target}: copied={stats['copied']} created_dirs={stats['created_dirs']} "
            f"removed_files={stats['removed_files']} removed_dirs={stats['removed_dirs']}"
        )


if __name__ == "__main__":
    main()
