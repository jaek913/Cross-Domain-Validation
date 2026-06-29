#!/usr/bin/env python3
"""render_claims.py - the {{LB-id}} renderer for the Cross-Domain-Validation paper.

The manuscript (Phase 4) carries NO hard-coded numbers: every load-bearing value
appears as a token {{LB-id}}. This renderer substitutes each token with the value
locked in claims.lock, so the paper text and the verified ledger can never drift.
verify.py's Phase-4 reconciliation then confirms no token survives unrendered.

Usage:
  python render_claims.py --list                 # print every {{LB-id}} + value
  python render_claims.py <template.md> <out.md>  # render a template to a file
  python render_claims.py --selftest             # render a built-in template, assert all tokens resolve

format_value() is imported by verify.py so the paper-presence check uses the
identical formatting.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK_PATH = HERE / "claims.lock"
TOKEN = re.compile(r"\{\{([A-Za-z0-9_\-.]+)\}\}")


def load_lock(path: Path = LOCK_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _fmt_num(x) -> str:
    s = f"{float(x):.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def format_value(row: dict) -> str:
    """Render a single claim row's locked value to display text."""
    chk = row.get("check")
    v = row.get("value")
    if chk == "num":
        return _fmt_num(v)
    if chk == "int":
        return str(v)
    if chk == "bool":
        return "true" if v else "false"
    if chk == "null":
        return "none"
    if chk == "num_list":
        return "[" + ", ".join(_fmt_num(x) for x in v) + "]"
    if chk == "int_dict":
        return " / ".join(f"{k} {v[k]}" for k in v)
    if chk == "band":
        b = row.get("band", [None, None])
        return f"{_fmt_num(v)} (band {b[0]}-{b[1]})"
    if chk in ("contains", "cite", "script"):
        return str(v)
    return str(v)


def render_text(template: str, lock: dict):
    """Return (rendered_text, unresolved_token_list)."""
    claims = lock["claims"]
    unresolved = []

    def repl(m):
        key = m.group(1)
        if key in claims:
            return format_value(claims[key])
        unresolved.append(key)
        return m.group(0)

    return TOKEN.sub(repl, template), unresolved


SELFTEST_TEMPLATE = (
    "Onset leads the peak by {{LB-e4-div-lead}} weeks (floor {{LB-e4-floor}}); "
    "Theorem 8b gives {{LB-e3-significant-correct}}/{{LB-e3-significant-total}} significant-correct "
    "with {{LB-e3-significant-wrong}} significant-wrong. Per domain: {{LB-e3-perdomain-significant}}. "
    "The RW control sits at {{LB-e1-rw-control}}. Sunspot vdiv is {{LB-e2-sunspot-rho}}. "
    "E7 verdict: {{LB-e7-verdict}}"
)


def main(argv):
    lock = load_lock()
    if "--list" in argv:
        for cid, row in lock["claims"].items():
            print(f"  {{{{{cid}}}}}  ->  {format_value(row)}    [{row.get('provenance')}]")
        print(f"\n{len(lock['claims'])} tokens available.")
        return 0
    if "--selftest" in argv:
        out, unresolved = render_text(SELFTEST_TEMPLATE, lock)
        print("Rendered self-test template:\n")
        print(" ", out, "\n")
        if unresolved:
            print(f"RENDER SELFTEST: FAIL - unresolved tokens: {unresolved}")
            return 1
        print("RENDER SELFTEST: PASS - every token resolved to a locked value.")
        return 0
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    tin, tout = Path(args[0]), Path(args[1])
    out, unresolved = render_text(tin.read_text(encoding="utf-8"), lock)
    Path(tout).write_text(out, encoding="utf-8")
    if unresolved:
        print(f"WROTE {tout} but {len(unresolved)} token(s) UNRESOLVED: {sorted(set(unresolved))}")
        return 1
    print(f"WROTE {tout} ({len(out)} chars); all tokens resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
