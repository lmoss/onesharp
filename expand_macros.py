#!/usr/bin/env python3
"""
expand_macros.py

Generates a separate copy of your notebooks that's safe to open on Colab or
CoCalc. Two independent problems are fixed:

1. Custom LaTeX macros (like \\onesharp, \\set{...}, \\semantics{...}) are
   expanded into literal LaTeX, since Colab/CoCalc don't read your
   _config.yml and don't support \\gdef/\\newcommand in math mode.

2. MyST-specific Markdown syntax -- things like ```{admonition}, {exercise},
   {prf:theorem} fenced blocks, (label)= anchors, and {ref}`label` /
   {prf:ref}`label` cross-references -- is converted into plain Markdown.
   Colab/CoCalc don't understand MyST directives at all; they just show a
   ```{admonition} fence as a literal, unstyled code block, which also
   stops the math *inside* it from ever reaching MathJax. Each directive
   block is turned into a bolded label (e.g. "**Problems.**" or
   "**Theorem (Post, 1946).**") followed by its ordinary content, so the
   math renders normally. See convert_myst_directives() below for exactly
   how labels are derived and for a caveat about nested fences.

IMPORTANT: this script never touches your original notebooks. It reads from
one folder and writes fully independent copies into another folder that you
choose. Your real source notebooks, and your Jupyter Book build, are
completely unaffected -- you can delete the output folder or stop running
this script at any time with zero impact on your book.

USAGE:
    python expand_macros.py SOURCE_DIR OUTPUT_DIR [--dry-run]

    Example:
        python expand_macros.py . ../onesharp-for-colab

HOW TO UPDATE YOUR MACROS LATER:
    Edit the MACROS dictionary below to match your _config.yml, then rerun
    this script. It always regenerates the output folder from scratch based
    on your current source notebooks and current macro list.

HOW ARGUMENT-TAKING MACROS ARE HANDLED (e.g. \\set{...}, \\semantics{...}):
    The script looks for a '{' immediately after the macro name (skipping
    whitespace), then scans forward counting nested braces to find the
    matching '}'. Whatever is between those braces becomes the argument,
    substituted in for #1 (and #2, #3, ... if a macro ever takes more than
    one argument). This correctly handles braces nested inside the
    argument itself, e.g. \\semantics{\\writeprog}(x).

    Expansion is repeated in passes until nothing changes, so macros that
    expand to *other* macros (like \\onehash -> \\onett\\hash) get fully
    resolved, however many levels deep.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Keep this in sync with the "macros" section of your _config.yml.
# ---------------------------------------------------------------------------
MACROS = {
    "quadiff": ["\\quad\\mbox{iff}\\quad"],
    "quadeq": ["\\quad =\\quad"],
    "dar": ["\\downarrow"],
    "uar": ["\\uparrow"],
    "eps": ["\\varepsilon"],
    "id": ["id"],
    "o": ["\\circ"],
    "N": "\\mathbb{N}",
    "set": ["\\left\\{#1\\right\\}", 1],
    "one": ["\\mathtt{1}"],
    "onett": ["\\mathtt{1}"],
    "hash": ["\\mathtt{\\#}"],
    "onehash": ["\\onett\\hash"],
    "onesharp": ["\\mathtt{1\\#}"],
    "diag": ["\\mathtt{diag}"],
    "self": ["\\mathtt{self}"],
    "diagprog": ["\\mathtt{diag}"],
    "selfprog": ["\\mathtt{self}"],
    "copyprog": ["\\mathtt{copy}"],
    "uprog": ["\\mathtt{u}"],
    "clearprog": ["\\mathtt{clear}"],
    "reverseprog": ["\\mathtt{reverse}"],
    "writeprog": ["\\mathtt{write}"],
    "writetotwo": ["\\mathtt{write}_2"],
    "tradeprog": ["\\mathtt{trade}"],
    "tidyprog": ["\\mathtt{tidy}"],
    "semantics": ["[\\![#1]\\!]", 1],
    "semanticsalt": ["\\langle\\!\\langle #1\\rangle\\!\\rangle", 1],
    "moveprog": ["\\mathtt{move}"],
    "moveprogtwoone": ["\\mathtt{move}_{2,1}"],
    "phifn": ["\\varphi"],
    "Tile": ["\\mathit{Tile}"],
    "TT": ["\\mathcal{T}"],
    "DD": ["\\mathcal{D}"],
    "Rone": ["R1"],
    "Rtwo": ["R2"],
    "words": ["\\mbox{words}"],
    "Words": ["\\textit{words}"],
    "Rings": ["\\mathsf{Rings}"],
    "iif": ["\\rightarrow"],
    "andd": ["\\wedge"],
    "proves": ["\\vdash"],
    "xbar": ["\\overline{x}"],
    "ybar": ["\\overline{y}"],
    "Ronesharp": ["R\\onesharp"],
}


def _normalize(spec):
    """Turn a MACROS value into (replacement, nargs)."""
    if isinstance(spec, str):
        return spec, 0
    if len(spec) == 1:
        return spec[0], 0
    return spec[0], spec[1]


# ---------------------------------------------------------------------------
# MyST directive / anchor / cross-reference conversion.
# ---------------------------------------------------------------------------

# Matches a full fenced directive, e.g.:
#     ```{admonition} Problems
#     :class: danger
#
#     content...
#     ```
# Tolerates leading/trailing whitespace around the fence lines (some cells
# in this book indent the whole block by one space).
#
# CAVEAT: this does not handle a directive block that itself contains
# another ``` fence nested inside it (e.g. a code example inside an
# exercise). None of the sample notebooks had that, but if your book does
# somewhere, that block would need a manual look at the output.
DIRECTIVE_RE = re.compile(
    r'^[ \t]*```\{([a-zA-Z0-9_:-]+)\}[ \t]*([^\n]*)\n'
    r'(.*?)'
    r'^[ \t]*```[ \t]*$',
    re.MULTILINE | re.DOTALL,
)

# A directive "option" line, e.g. ":class: danger" or ":label: exer-clear".
# These configure the built book's styling/cross-referencing and have no
# plain-Markdown equivalent, so they're just dropped.
OPTION_LINE_RE = re.compile(r'^[ \t]*:[a-zA-Z_-]+:[^\n]*\n?', re.MULTILINE)

# A MyST explicit target/anchor on its own line, e.g. "(content:halting)=".
# These are invisible in the built book too (they just mark a spot other
# pages can link to), so they're removed entirely.
ANCHOR_RE = re.compile(r'^[ \t]*\([a-zA-Z0-9_:.-]+\)=[ \t]*\n?', re.MULTILINE)

# An inline cross-reference role, e.g. {ref}`on-halting` or
# {prf:ref}`Turings-theorem`. There's no way to make these clickable outside
# the built book, so they're replaced with just the label in backticks, as a
# readable (if inert) fallback.
REF_ROLE_RE = re.compile(r'\{(?:[a-zA-Z]+:)?ref\}`([^`]+)`')


def compute_label(name, argument):
    """
    Turn a directive name + optional same-line argument into a readable
    bolded label. Examples:
        admonition, "Problems"        -> "Problems"
        admonition, "Definition"      -> "Definition"
        admonition, ""                -> "Note"
        exercise,   ""                -> "Exercise"
        "prf:theorem", "Post, 1946"   -> "Theorem (Post, 1946)"
        "prf:definition", ""          -> "Definition"
    """
    base = name.split(":")[-1]
    base_label = base[:1].upper() + base[1:] if base else "Note"
    if base == "admonition":
        return argument if argument else "Note"
    return f"{base_label} ({argument})" if argument else base_label


def _directive_replacer(match):
    name = match.group(1)
    argument = match.group(2).strip()
    content = match.group(3)
    content = OPTION_LINE_RE.sub("", content)
    content = content.strip("\n")
    label = compute_label(name, argument)
    return f"**{label}.**\n\n{content}\n"


def convert_myst_directives(text):
    text = DIRECTIVE_RE.sub(_directive_replacer, text)
    text = ANCHOR_RE.sub("", text)
    text = REF_ROLE_RE.sub(r"`\1`", text)
    return text


def find_matching_brace(text, open_index):
    """Given the index of a '{', return the index of its matching '}'."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return None  # unbalanced -- caller should leave things alone


def expand_once(text):
    """
    One left-to-right pass over `text`, expanding every macro call it can
    find. Returns (new_text, changed).
    """
    out = []
    i = 0
    changed = False
    n = len(text)

    while i < n:
        if text[i] != "\\":
            out.append(text[i])
            i += 1
            continue

        # Capture the macro name: backslash followed by a maximal run of letters.
        j = i + 1
        while j < n and text[j].isalpha():
            j += 1
        name = text[i + 1 : j]

        if not name or name not in MACROS:
            out.append(text[i])
            i += 1
            continue

        replacement, nargs = _normalize(MACROS[name])
        pos = j
        args = []
        ok = True

        for _ in range(nargs):
            # Skip whitespace before the argument.
            k = pos
            while k < n and text[k] in " \t":
                k += 1
            if k < n and text[k] == "{":
                close = find_matching_brace(text, k)
                if close is None:
                    ok = False
                    break
                args.append(text[k + 1 : close])
                pos = close + 1
            elif k < n:
                # Fallback: a single bare token as the argument.
                args.append(text[k])
                pos = k + 1
            else:
                ok = False
                break

        if not ok:
            # Couldn't cleanly find the arguments -- leave this occurrence
            # untouched rather than risk mangling the text.
            out.append(text[i])
            i += 1
            continue

        expanded = replacement
        for idx, arg in enumerate(args, start=1):
            expanded = expanded.replace(f"#{idx}", arg)

        out.append(expanded)
        i = pos
        changed = True

    return "".join(out), changed


def expand_fully(text, max_passes=25):
    for _ in range(max_passes):
        text, changed = expand_once(text)
        if not changed:
            break
    return text


def get_source_text(cell):
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def set_source_text(cell, text, original_was_list):
    if original_was_list:
        cell["source"] = text.splitlines(keepends=True)
    else:
        cell["source"] = text


AUTO_MACROS_MARKER = "AUTO-MACROS-START"


def strip_auto_macros_cell(nb) -> bool:
    """
    Remove any leftover cell inserted by insert_macros.py. That cell relies
    on \\gdef and is not needed here (macros are being expanded to literal
    LaTeX instead) -- and if left in, this script's expansion pass would
    mangle it, since it can't distinguish a macro being *defined* from one
    being *used*. Returns True if a cell was removed.
    """
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
    nb["cells"] = kept
    return removed


def process_notebook(in_path: Path, out_path: Path, dry_run: bool) -> bool:
    with open(in_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    any_change = strip_auto_macros_cell(nb)
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        original_was_list = isinstance(cell.get("source", ""), list)
        text = get_source_text(cell)
        new_text = convert_myst_directives(text)
        new_text = expand_fully(new_text)
        if new_text != text:
            any_change = True
            set_source_text(cell, new_text, original_was_list)

    if not dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")

    return any_change


def find_notebooks(root: Path):
    for nb_path in sorted(root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in nb_path.parts:
            continue
        if "_build" in nb_path.parts:
            continue
        yield nb_path


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if len(args) != 2:
        print(__doc__)
        sys.exit(1)

    source_dir = Path(args[0]).resolve()
    output_dir = Path(args[1]).resolve()

    if output_dir == source_dir or str(output_dir).startswith(str(source_dir) + "/"):
        print("ERROR: OUTPUT_DIR must not be inside SOURCE_DIR. "
              "Choose a separate folder so your originals are never touched.")
        sys.exit(1)

    changed_count = 0
    total_count = 0
    for nb_path in find_notebooks(source_dir):
        rel = nb_path.relative_to(source_dir)
        out_path = output_dir / rel
        total_count += 1
        changed = process_notebook(nb_path, out_path, dry_run)
        changed_count += 1 if changed else 0
        verb = "Would expand macros in" if dry_run else "Wrote"
        note = "" if changed else " (no macros found, copied as-is)" if not dry_run else " (no macros found)"
        print(f"{verb}: {rel}{note}")

    print(f"\n{total_count} notebook(s) processed, {changed_count} contained macros to expand.")
    if dry_run:
        print("(Dry run -- no files were written. Rerun without --dry-run to generate the output copies.)")
    else:
        print(f"Colab/CoCalc-ready copies are in: {output_dir}")


if __name__ == "__main__":
    main()
