
# 1# idea tool (Colab)
#
# Requires:
# !python -m pip install -U git+https://github.com/lmoss/onesharp.git@main
# from onesharp.interpreter.interpreter import *

import ast
import re
from dataclasses import dataclass

import ipywidgets as widgets
from IPython.display import display

RESERVED = {"cases", "goto", "end"}

CELL_W = "88px"
DEL_W = "42px"
GRID_W = "500px"

# ---------- helpers ----------

def is_label(s):
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", (s or "").strip())) and (s or "").strip() not in RESERVED

def is_cases(s):
    return bool(re.fullmatch(r"cases\s+(?:R)?\d+", (s or "").strip(), re.I))

def cases_num(s):
    m = re.fullmatch(r"cases\s+(?:R)?(\d+)", (s or "").strip(), re.I)
    return int(m.group(1)) if m else None

def parse_defs(txt):
    d = {}
    for line in (txt or "").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            try:
                val = ast.literal_eval(v)
                if isinstance(val, str):
                    d[k] = val
            except Exception:
                pass
    return d

def valid_expr(expr, defs):
    expr = (expr or "").strip()

    if re.fullmatch(r"[1#]+", expr):
        return True, ""

    if expr in defs:
        return True, ""

    try:
        tree = ast.parse(expr, mode="eval")
    except Exception:
        return False, "Box 2 is not valid Python syntax"

    allowed = set(defs) | {"move", "copy"}

    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id not in allowed:
            return False, f"variable '{n.id}' is not defined"

    return True, ""

# ---------- row ----------

@dataclass
class Row:
    boxes: list
    delete: widgets.Button
    widget: widgets.HBox

    def vals(self):
        return [b.value.strip() for b in self.boxes]

    def empty(self):
        return not any(self.vals())

# ---------- tool ----------

class IdeaTool:

    def __init__(self):
        self.add = widgets.Button(description="Add segment")
        self.load = widgets.Button(description="Load example")
        self.clear = widgets.Button(description="Clear input")
        self.validate_btn = widgets.Button(description="Validate", button_style="primary")

        self.strings = widgets.Textarea(
            layout=widgets.Layout(width=GRID_W, height="80px")
        )

        self.rows = []
        self.grid = widgets.VBox(layout=widgets.Layout(gap="0px"))
        self.out = widgets.Output()

        self.add.on_click(self.add_row)
        self.load.on_click(self.load_example)
        self.clear.on_click(lambda _: self.reset())
        self.validate_btn.on_click(self.run)

        self.reset()
        self.ui = self.build()

    # ---------- UI helpers ----------

    def cell(self, v=""):
        t = widgets.Text(
            value=v,
            layout=widgets.Layout(width=CELL_W, height="26px")
        )

        def highlight(change=None):
            if t.value.strip() == "end":
                t.add_class("end-box")
            else:
                t.remove_class("end-box")

        highlight()
        t.observe(highlight, names="value")
        t.on_submit(self.run)
        return t

    def make_row(self, *vals):
        vals = list(vals) + [""] * (5 - len(vals))
        cells = [self.cell(v) for v in vals]

        delete_btn = widgets.Button(
            description="Del",
            layout=widgets.Layout(width=DEL_W)
        )

        row = Row(cells, delete_btn, None)

        def kill(_):
            self.rows = [r for r in self.rows if r != row]
            if not self.rows:
                self.rows = [self.make_row()]
            self.refresh()

        delete_btn.on_click(kill)

        row.widget = widgets.HBox(
            cells + [delete_btn],
            layout=widgets.Layout(width=GRID_W)
        )
        return row

    def refresh(self):
        self.grid.children = [r.widget for r in self.rows]

    def reset(self):
        self.rows = [self.make_row()]
        self.strings.value = ""
        self.refresh()
        self.out.clear_output()

    def add_row(self, _=None):
        self.rows.append(self.make_row())
        self.refresh()

    def load_example(self, _=None):
        self.strings.value = "xyz='111##'"
        data = [
            ("top", "cases R1", "move_back", "one_found", "hash_found"),
            ("one_found", "111#", "", "", ""),
            ("", "goto move_phase", "", "", ""),
            ("hash_found", "xyz", "", "", ""),
            ("", "goto move_phase", "", "", ""),
            ("move_phase", "move(2,3)+move(3,2)", "", "", ""),
            ("", "goto top", "", "", ""),
            ("move_back", "move(2,1)", "", "", ""),
        ]
        self.rows = [self.make_row(*d) for d in data]
        self.refresh()

    # ---------- validation ----------

    def clear_highlights(self):
        for r in self.rows:
            for b in r.boxes:
                b.remove_class("error-box")
                if b.value.strip() == "end":
                    b.add_class("end-box")
                else:
                    b.remove_class("end-box")

    def mark_error(self, box):
        box.add_class("error-box")

    def validate(self):
        defs = parse_defs(self.strings.value)
        labels = {}
        refs = []
        issues = []

        self.clear_highlights()

        for i, r in enumerate(self.rows, 1):
            if r.empty():
                continue

            b = r.vals()

            # CASES
            if is_cases(b[1]):
                if not is_label(b[0]):
                    issues.append(f"Row {i}: Box 1 can only contain labels")
                    self.mark_error(r.boxes[0])

                if not is_cases(b[1]):
                    issues.append(f"Row {i}: Box 2 must be 'cases k' or 'cases Rk'")
                    self.mark_error(r.boxes[1])

                for j, t in enumerate(b[2:5]):
                    if not (is_label(t) or t == "end"):
                        issues.append(f"Row {i}: Box {j+3} must be label or 'end'")
                        self.mark_error(r.boxes[j+2])
                    else:
                        refs.append(t)

            # GOTO
            elif b[1].startswith("goto"):
                parts = b[1].split()

                if len(parts) != 2:
                    if b[1] == "goto" and is_label(b[2]):
                        issues.append(f"Row {i}: Move label from Box 3 into Box 2")
                        self.mark_error(r.boxes[1])
                        self.mark_error(r.boxes[2])
                    else:
                        issues.append(f"Row {i}: Box 2 must be 'goto label'")
                        self.mark_error(r.boxes[1])
                else:
                    target = parts[1]
                    if not (is_label(target) or target == "end"):
                        issues.append(f"Row {i}: invalid goto target '{target}'")
                        self.mark_error(r.boxes[1])
                    else:
                        refs.append(target)

            # RAW
            else:
                if not is_label(b[0]):
                    issues.append(f"Row {i}: Box 1 can only contain labels")
                    self.mark_error(r.boxes[0])

                ok, msg = valid_expr(b[1], defs)
                if not ok:
                    issues.append(f"Row {i}: {msg}")
                    self.mark_error(r.boxes[1])

            # duplicate labels
            if is_label(b[0]):
                if b[0] in labels:
                    issues.append(f"Row {i}: duplicate label '{b[0]}'")
                    self.mark_error(r.boxes[0])
                labels[b[0]] = i

        # missing labels
        for t in refs:
            if t != "end" and t not in labels:
                issues.append(f"Missing label: {t}")

        return issues

    # ---------- execution ----------

    def eval_code(self, expr, defs):
        expr = (expr or "").strip()

        if re.fullmatch(r"[1#]+", expr):
            return expr

        if expr in defs:
            return "".join(defs[expr].split())

        val = str(
            eval(
                expr,
                {"__builtins__": {}, "move": move, "copy": copy} | defs,
                {}
            )
        )

        return "".join(val.split())

    def plan(self):
        defs = parse_defs(self.strings.value)
        p = []
        counter = 0

        def fix(x):
            return "end" if x == "end" else x

        for r in self.rows:
            if r.empty():
                continue

            b = r.vals()
            label = b[0] if is_label(b[0]) else f"_L{counter}"
            counter += 1

            if is_cases(b[1]):
                p.append([
                    label,
                    "cases",
                    cases_num(b[1]),
                    fix(b[2]),
                    fix(b[3]),
                    fix(b[4])
                ])

            elif b[1].startswith("goto"):
                parts = b[1].split()
                target = parts[1] if len(parts) > 1 else ""
                p.append([
                    label,
                    "goto",
                    fix(target)
                ])

            else:
                p.append([
                    label,
                    self.eval_code(b[1], defs)
                ])

        return p

    def run(self, _=None):
        self.out.clear_output()

        try:
            issues = self.validate()
        except Exception as e:
            with self.out:
                print("Validation error:", e)
            return

        with self.out:
            if issues:
                print("Validation issues:")
                for e in issues:
                    print("-", e)
                return

            try:
                print(sanity(self.plan()))
            except Exception as e:
                print("sanity() error:", e)

    # ---------- UI ----------

    def build(self):
        headers = widgets.HBox([
            widgets.HTML("<b>Label</b>", layout=widgets.Layout(width=CELL_W)),
            widgets.HTML("<b>Instruction</b>", layout=widgets.Layout(width=CELL_W)),
            widgets.HTML("<b>'empty'</b>", layout=widgets.Layout(width=CELL_W)),
            widgets.HTML("<b>'1'</b>", layout=widgets.Layout(width=CELL_W)),
            widgets.HTML("<b>'#'</b>", layout=widgets.Layout(width=CELL_W)),
        ], layout=widgets.Layout(width=GRID_W))

        return widgets.VBox([
            widgets.HTML("""
            <style>
              .widget-textarea textarea {
                  resize: none !important;
              }
              .end-box input {
                  background-color: #e6ffe6 !important;
              }
              .error-box input {
                  background-color: #ffe6e6 !important;
              }
            </style>
            """),
            widgets.HTML("<b>1# idea tool</b>"),
            widgets.HTML("<b>String definitions</b>"),
            self.strings,
            headers,
            self.grid,
            widgets.HBox([self.add, self.load, self.clear, self.validate_btn], layout=widgets.Layout(width=GRID_W)),
            self.out
        ])

    def show(self):
        self.reset()
        display(self.ui)

app = IdeaTool()
app.show()
