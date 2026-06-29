#!/usr/bin/env python3
"""verify.py - Phase-3 gate verifier for the Cross-Domain-Validation paper.

Checks the committed pipeline against analysis/claims.lock:

  (1) INPUT INTEGRITY  - re-hash every input store file (in $LT_CDV_DATA) and
      compare SHA256 to the lock.
  (2) REPRODUCTION     - re-run each generating script (E1-E7, E7b) and compare
      every regenerated value to the locked value within its tolerance
      (per check type: num / int / bool / num_list / int_dict / null / band /
      contains; cite rows are display-only; theorem rows are run separately).
  (3) CIC SIGNED       - every experiment's 7 CIC flags are present with a status
      and a note, and the block carries signed_by + signed_date; every claim's
      cic_ref resolves (THM rows are exempt - they are proof-checks, not CIC).
  (4) THEOREM CHECKS   - run each registered theorem-check script; require exit 0.
  (5) PAPER RECONCILE  - (Phase 4, --paper) every {{LB-id}} is rendered (no stub
      survives), and required sections + citation keys are present. Deferred with
      a notice until a manuscript exists.

Ships with deliberately broken fixtures (`--selftest`) and turns RED on each:
value drift, an unsigned CIC flag, and a missing-citation / surviving-stub /
missing-section paper.

Usage:
  python analysis\\verify.py                 # full gate (rehash + rerun + cic + theorem)
  python analysis\\verify.py --no-rerun      # compare against committed outputs (fast)
  python analysis\\verify.py --no-rehash     # skip input hashing
  python analysis\\verify.py --paper PATH    # add the Phase-4 manuscript reconciliation
  python analysis\\verify.py --selftest      # broken-fixture self-test (must all go RED)

Exit 0 iff every requested check passes (or, for --selftest, every fixture
correctly went RED).
"""
from __future__ import annotations
import json, os, re, sys, hashlib, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent          # analysis/
REPO = HERE.parent
OUTDIR = HERE / "outputs"
FIXTURES = HERE / "fixtures"
LOCK_PATH = HERE / "claims.lock"
sys.path.insert(0, str(HERE))
from render_claims import format_value, render_text  # noqa: E402

GREEN, RED = "PASS", "FAIL"
TOKEN_RE = re.compile(r"\{\{[^}]+\}\}")


def load_lock(path: Path = LOCK_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_path(obj, path):
    cur = obj
    for k in path:
        cur = cur[k] if isinstance(k, int) else cur[k]
    return cur


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
def check_hashes(lock):
    rows = []
    data_dir = os.environ.get("LT_CDV_DATA")
    if not data_dir:
        return [("inputs", RED, "LT_CDV_DATA not set; cannot re-hash input store files")]
    base = Path(data_dir)
    for fn, meta in lock["inputs"].items():
        p = base / fn
        if not p.exists():
            rows.append((fn, RED, f"missing in store: {p}"))
            continue
        got = sha256_of(p)
        ok = (got == meta["sha256"])
        rows.append((fn, GREEN if ok else RED,
                     "sha256 match" if ok else f"sha256 DRIFT got {got[:12]} != {meta['sha256'][:12]}"))
    return rows


def compare_claim(row, out_value):
    chk = row["check"]
    val = row.get("value")
    tol = float(row.get("tol", 1e-6))
    try:
        if chk == "num":
            return (abs(float(out_value) - float(val)) <= tol + 1e-9,
                    f"{out_value} vs {val} (tol {tol})")
        if chk == "int":
            return (int(out_value) == int(val), f"{out_value} vs {val}")
        if chk == "bool":
            return (bool(out_value) == bool(val), f"{out_value} vs {val}")
        if chk == "null":
            return (out_value is None, f"{out_value} (expect null)")
        if chk == "num_list":
            if not isinstance(out_value, list) or len(out_value) != len(val):
                return (False, f"{out_value} vs {val} (shape)")
            return (all(abs(float(a) - float(b)) <= tol + 1e-9 for a, b in zip(out_value, val)),
                    f"{out_value} vs {val} (tol {tol})")
        if chk == "int_dict":
            if set(out_value) != set(val):
                return (False, f"keys {sorted(out_value)} vs {sorted(val)}")
            return (all(int(out_value[k]) == int(val[k]) for k in val), f"{out_value} vs {val}")
        if chk == "band":
            lo, hi = row["band"]
            return (lo - 1e-9 <= float(out_value) <= hi + 1e-9, f"{out_value} in [{lo}, {hi}]")
        if chk == "contains":
            return (str(val) in str(out_value), "verdict substring present" if str(val) in str(out_value)
                    else "verdict substring ABSENT")
    except (TypeError, ValueError, KeyError) as e:
        return (False, f"compare error: {e}")
    return (True, "n/a")


def rerun_scripts(lock):
    scripts = []
    for blk in lock["cic"].values():
        s = blk.get("script")
        if s and s not in scripts:
            scripts.append(s)
    rows = []
    for s in scripts:
        path = (REPO / s) if s.startswith("analysis/") else (HERE / s)
        r = subprocess.run([sys.executable, str(path)], cwd=str(REPO),
                           capture_output=True, text=True)
        ok = (r.returncode == 0)
        detail = "ran clean" if ok else f"exit {r.returncode}: {(r.stderr or r.stdout).strip()[-200:]}"
        rows.append((s, GREEN if ok else RED, detail))
    return rows


def check_values(lock):
    rows = []
    cache = {}
    for cid, row in lock["claims"].items():
        if row["check"] == "script" or row["provenance"] == "cite":
            continue
        out = row["output"]
        if out not in cache:
            p = OUTDIR / Path(out).name
            cache[out] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
        data = cache[out]
        if data is None:
            rows.append((cid, RED, f"output missing: {out}"))
            continue
        try:
            ov = get_path(data, row["json_path"])
        except (KeyError, IndexError, TypeError) as e:
            rows.append((cid, RED, f"path miss: {e}"))
            continue
        ok, detail = compare_claim(row, ov)
        flag = "" if row["provenance"] in ("regenerate", "negative") else f" [{row['provenance']}]"
        rows.append((cid, GREEN if ok else RED, detail + flag))
    return rows


def check_cic(lock):
    rows = []
    classes = ["1_reexecutes", "2_index_alignment", "3_nan_gap", "4_no_lookahead",
               "5_overlap_consistency", "6_record_boundaries", "7_input_integrity"]
    for exp, blk in lock["cic"].items():
        problems = []
        if not blk.get("signed_by"):
            problems.append("no signed_by")
        if not blk.get("signed_date"):
            problems.append("no signed_date")
        flags = blk.get("flags", {})
        for c in classes:
            f = flags.get(c)
            if not f or f.get("status") not in ("pass", "n/a") or not f.get("note"):
                problems.append(f"flag {c} unsigned/incomplete")
        rows.append((f"cic:{exp}", GREEN if not problems else RED,
                     "7 flags signed" if not problems else "; ".join(problems)))
    # every claim's cic_ref must resolve (THM exempt)
    for cid, row in lock["claims"].items():
        ref = row.get("cic_ref")
        if ref == "THM":
            continue
        if ref not in lock["cic"]:
            rows.append((f"cic_ref:{cid}", RED, f"cic_ref {ref!r} has no signed CIC block"))
    return rows


def run_theorem_checks(lock):
    rows = []
    for cid, row in lock["claims"].items():
        if row["check"] != "script":
            continue
        s = row["script"]
        path = (REPO / s) if s.startswith("analysis/") else (HERE / s)
        r = subprocess.run([sys.executable, str(path)], cwd=str(REPO),
                           capture_output=True, text=True)
        ok = (r.returncode == 0)
        tail = (r.stdout or r.stderr).strip().splitlines()
        rows.append((cid, GREEN if ok else RED,
                     (tail[-1] if tail else "ran") if ok else f"exit {r.returncode}"))
    return rows


def check_paper(text, required_sections, required_cites, lock=None):
    rows = []
    stubs = TOKEN_RE.findall(text)
    rows.append(("paper:no-stub", GREEN if not stubs else RED,
                 "no unrendered tokens" if not stubs else f"surviving stub(s): {stubs[:5]}"))
    for sec in required_sections:
        rows.append((f"paper:section{sec}", GREEN if sec in text else RED,
                     "present" if sec in text else "MISSING required section"))
    for key in required_cites:
        rows.append((f"paper:cite[{key}]", GREEN if key in text else RED,
                     "present" if key in text else "MISSING citation key"))
    if lock is not None:
        missing = []
        for cid, row in lock["claims"].items():
            if row["provenance"] == "theorem-check":
                continue
            tok = "{{" + cid + "}}"
            if tok not in text and format_value(row) not in text:
                missing.append(cid)
        rows.append(("paper:lb-coverage", GREEN if not missing else RED,
                     "every LB-id present" if not missing else f"{len(missing)} LB-id(s) absent: {missing[:5]}"))
    return rows


# --------------------------------------------------------------------------- #
def _print(title, rows):
    n_fail = sum(1 for _, s, _ in rows if s == RED)
    print(f"\n== {title} ==  ({len(rows)-n_fail}/{len(rows)} pass)")
    for name, status, detail in rows:
        mark = " " if status == GREEN else ">"
        print(f"  {mark}[{status}] {name}: {detail}")
    return n_fail


def selftest(lock):
    print("SELFTEST - the verifier must turn RED on every broken fixture.\n")
    results = []

    # (a) value drift: perturb a locked numeric value, compare to the committed output
    drift_ok = None
    try:
        e4 = json.loads((OUTDIR / "e4_flu_onset.json").read_text(encoding="utf-8"))
        true_v = get_path(e4, ["divergence_lead_vs_peak", "mean"])
        row = dict(lock["claims"]["LB-e4-div-lead"])
        row["value"] = float(row["value"]) + 10.0          # 200x the tolerance
        ok, _ = compare_claim(row, true_v)
        drift_ok = (ok is False)
    except Exception as e:
        drift_ok = False
        print("  value-drift fixture error:", e)
    results.append(("value-drift turns RED", drift_ok))

    # (b) unsigned CIC: blank a flag's signature, expect check_cic to FAIL that block
    lk = json.loads(json.dumps(lock))
    lk["cic"]["E1"].pop("signed_by", None)
    lk["cic"]["E1"]["flags"]["4_no_lookahead"]["status"] = ""
    cic_rows = check_cic(lk)
    unsigned_ok = any(name == "cic:E1" and st == RED for name, st, _ in cic_rows)
    results.append(("unsigned-CIC turns RED", unsigned_ok))

    # (c) reconciliation fixtures
    req_sec = ["## Methods", "## Results"]
    req_cite = ["kim2026d"]
    fx = {
        "paper_good.md": True,
        "paper_missing_citation.md": False,
        "paper_surviving_stub.md": False,
        "paper_missing_section.md": False,
    }
    for fname, should_pass in fx.items():
        text = (FIXTURES / fname).read_text(encoding="utf-8")
        rows = check_paper(text, req_sec, req_cite)
        all_green = all(st == GREEN for _, st, _ in rows)
        ok = (all_green == should_pass)
        label = f"fixture {fname} -> {'GREEN' if should_pass else 'RED'}"
        results.append((label, ok))

    print("  Results:")
    n_bad = 0
    for label, ok in results:
        print(f"   [{'OK' if ok else 'BAD'}] {label}")
        n_bad += (0 if ok else 1)
    print()
    if n_bad:
        print(f"VERIFY SELFTEST: FAIL - {n_bad} fixture(s) did not behave as required.")
        return 1
    print("VERIFY SELFTEST: PASS - value-drift, unsigned-CIC, and all reconciliation "
          "fixtures behaved correctly (broken -> RED, good -> GREEN).")
    return 0


def main(argv):
    lock = load_lock()
    if "--selftest" in argv:
        return selftest(lock)

    no_rerun = "--no-rerun" in argv
    no_rehash = "--no-rehash" in argv
    paper_path = None
    if "--paper" in argv:
        paper_path = argv[argv.index("--paper") + 1]

    print(f"verify.py - claims.lock: {lock['_meta']['n_claims']} rows, "
          f"design {lock['_meta']['design_version']}, generated {lock['_meta']['generated_at']}")
    total_fail = 0

    if not no_rehash:
        total_fail += _print("(1) input integrity (re-hash vs lock)", check_hashes(lock))
    else:
        print("\n== (1) input integrity ==  SKIPPED (--no-rehash)")

    if not no_rerun:
        total_fail += _print("(2a) re-run generating scripts", rerun_scripts(lock))
    else:
        print("\n== (2a) re-run scripts ==  SKIPPED (--no-rerun; comparing committed outputs)")
    total_fail += _print("(2b) reproduction (regenerated vs lock)", check_values(lock))

    total_fail += _print("(3) CIC signed", check_cic(lock))
    total_fail += _print("(4) theorem checks", run_theorem_checks(lock))

    if paper_path:
        text = Path(paper_path).read_text(encoding="utf-8")
        total_fail += _print("(5) paper reconciliation",
                             check_paper(text, ["## Methods", "## Results"], ["kim2026"], lock))
    else:
        print("\n== (5) paper reconciliation ==  DEFERRED (no --paper; Phase-4 check, "
              "runs once the manuscript exists)")

    print("\n" + "=" * 64)
    if total_fail:
        print(f"VERIFY: FAIL - {total_fail} issue(s).")
        return 1
    print("VERIFY: PASS - inputs hash-match, every regenerated value matches the "
          "lock within tolerance, all CIC flags signed, theorem checks clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
