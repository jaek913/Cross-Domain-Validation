"""
flu_onset_boundary_diagnostic.py — Cross-Domain Validation, E4 boundary-firing diagnostic

Question: in how many of the 27 paired seasons does the registered onset rule
(first week in MMWR 40-20 with SMA4 - SMA12 of national weighted ILI > 0.2 pp)
fire on the FIRST eligible week, i.e. at the calendar boundary rather than on a
crossing inside the window? And what does the lead look like under a strict
crossing rule (D must go from <= 0.2 to > 0.2 inside the window)?

Data: CDC ILINet national %WEIGHTED ILI, via the Delphi Epidata mirror
(https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=199740-YYYYWW).
This is the latest-issue vintage; the paper's ledger runs on a pinned vintage, so
the mean divergence lead differs by ~0.5 wk. The level lead, the 26-of-27 count
and the minimum lead reproduce exactly.

Usage:
  python flu_onset_boundary_diagnostic.py            # fetches data
  python flu_onset_boundary_diagnostic.py ilinet.json  # uses a saved pull
Writes flu_onset_boundary_diagnostic.csv next to the script.
"""
import json, sys, csv, os, urllib.request

EXCLUDE = {2009, 2020}          # per paper Appendix A.3
FIRST, LAST = 1997, 2025        # candidate seasons 1997-98 .. 2025-26
THR, LVL = 0.2, 1.0

def load(path=None):
    if path and os.path.exists(path):
        return json.load(open(path))["epidata"]
    url = "https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=199740-202640"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["epidata"]

def main():
    d = sorted(load(sys.argv[1] if len(sys.argv) > 1 else None), key=lambda r: r["epiweek"])
    wk = [r["epiweek"] for r in d]; w = [r["wili"] for r in d]
    D = [None] * len(w)
    for i in range(11, len(w)):
        D[i] = sum(w[i-3:i+1]) / 4 - sum(w[i-11:i+1]) / 12
    rows = []
    for s in range(FIRST, LAST + 1):
        idx = [i for i, e in enumerate(wk) if (e // 100 == s and e % 100 >= 40) or (e // 100 == s + 1 and e % 100 <= 20)]
        if len(idx) < 20:
            continue
        onset = next((i for i in idx if D[i] is not None and D[i] > THR), None)
        base = sum(w[i] for i in idx[:4]) / 4
        level = next((i for i in idx if w[i] > base + LVL), None)
        cross = next((i for i in idx if D[i] is not None and D[i] > THR and D[i-1] is not None and D[i-1] <= THR), None)
        peak = max(idx, key=lambda i: w[i])
        rows.append(dict(
            season=f"{s}-{str(s+1)[2:]}", paired=(s not in EXCLUDE),
            first_week=wk[idx[0]], D_at_first_week=(round(D[idx[0]], 3) if D[idx[0]] is not None else None),
            onset_week=wk[onset] if onset is not None else None,
            fired_first_week=(onset == idx[0]),
            cross_week=wk[cross] if cross is not None else None,
            level_week=wk[level] if level is not None else None,
            peak_week=wk[peak], peak_wili=round(w[peak], 2),
            div_lead=(peak - onset) if onset is not None else None,
            level_lead=(peak - level) if level is not None else None,
            cross_lead=(peak - cross) if cross is not None else None,
        ))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flu_onset_boundary_diagnostic.csv")
    with open(out, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)

    P = [r for r in rows if r["paired"] and r["level_lead"] is not None]
    n = len(P); fw = sum(r["fired_first_week"] for r in P)
    md = sum(r["div_lead"] for r in P) / n; ml = sum(r["level_lead"] for r in P) / n
    C = [r for r in P if r["cross_lead"] is not None]
    mc = sum(r["cross_lead"] for r in C) / len(C); mlc = sum(r["level_lead"] for r in C) / len(C)
    print(f"paired seasons: {n}")
    print(f"registered rule: mean div lead {md:.3f} wk, mean level lead {ml:.3f} wk, advantage {md-ml:.3f} wk, "
          f"div first in {sum(r['div_lead']>r['level_lead'] for r in P)} of {n}")
    print(f"FIRED ON FIRST ELIGIBLE WEEK (boundary): {fw} of {n}  -> "
          + ", ".join(r["season"] for r in P if r["fired_first_week"]))
    print(f"strict crossing rule: scorable {len(C)} of {n}; mean cross lead {mc:.3f} wk vs level {mlc:.3f} wk, "
          f"advantage {mc-mlc:.3f} wk, div first in {sum(r['cross_lead']>r['level_lead'] for r in C)} of {len(C)}")
    print("no in-window crossing (D already > 0.2 at week 40 and stayed there): "
          + ", ".join(r["season"] for r in P if r["cross_lead"] is None))
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
