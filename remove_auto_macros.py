#!/usr/bin/env python3
"""
remove_auto_macros.py

One-time cleanup: removes the \\gdef macro-definition cell that
insert_macros.py previously added to the top of your notebooks. That
approach didn't work for Colab/CoCalc (their MathJax doesn't support
\\gdef-with-arguments), and it's not needed for the built book either
(your _config.yml already supplies macros there). This just removes the
now-unnecessary cell, in place, from your real source notebooks.

USAGE:
    python remove_auto_macros.py PATH [PATH ...] [--dry-run]

    PATH can be a single .ipynb file or a directory (searched recursively).
    --dry-run shows what would change without writing any files.
"""

import json
import sys
from pathlib import Path

AUTO_MACROS_MARKER = "AUTO-MACROS-START"


def process_notebook(path: Path, dry_run: bool) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    kept = []
    removed = False
    for cell in cells:
        src = cell.get("source", "")
        text = "".join(src) if isinstance(src, list) else src
        if AUTO_MACROS_MARKER in text:
            removed = True
            continue
        kept.append(cell)

    if not removed:
        return False

    nb["cells"] = kept
    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return True


def find_notebooks(paths):
    for p in paths:
        p = Path(p)
        if p.is_file() and p.suffix == ".ipynb":
            yield p
        elif p.is_dir():
            for nb_path in sorted(p.rglob("*.ipynb")):
                if ".ipynb_checkpoints" in nb_path.parts:
                    continue
                if "_build" in nb_path.parts:
                    continue
                yield nb_path


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if not args:
        print(__doc__)
        sys.exit(1)

    changed = []
    for nb_path in find_notebooks(args):
        if process_notebook(nb_path, dry_run):
            changed.append(nb_path)

    verb = "Would remove AUTO-MACROS cell from" if dry_run else "Removed AUTO-MACROS cell from"
    for p in changed:
        print(f"{verb}: {p}")
    print(f"\n{verb.split(' from')[0]} in {len(changed)} notebook(s).")
    if dry_run:
        print("(Dry run -- no files were actually written. Rerun without --dry-run to apply.)")


if __name__ == "__main__":
    main()
