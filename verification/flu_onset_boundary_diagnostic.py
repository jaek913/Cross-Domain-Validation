"""
flu_onset_boundary_diagnostic.py — Cross-Domain Validation, E4 boundary-firing diagnostic

Question: in how many of the 27 paired seasons does the registered onset rule
(first week in MMWR 40-20 with SMA4 - SMA12 of national weighted ILI > 0.2 pp)
fire on the FIRST eligible week, i.e. at the calendar boundary rather than on a
crossing inside the window? And what does the lead look like under a strict
crossing rule (D must go from <= 0.2 to > 0.2 inside the window)?

Data: CDC ILINet national %WEIGHTED ILI, via the Delphi Epidata mirror
(https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=199740-YYYYWW).

Series convention — MUST match the paper. The paper's pinned ILINet file is a
continuous MMWR-week grid from 1997w40 in which the non-reported summer weeks
(weeks 21-39, seasons before 2003-04) are present as 0.0. This script regrids
the API rows onto the same grid and zero-fills the same gaps, so the registered
rule reproduces the paper's ledger exactly (mean divergence lead 14.148 wk,
level lead 5.926 wk, advantage 8.222 wk, divergence first in 26 of 27).
An earlier version (2026-09-30, first commit) ran on the raw API rows with the
summer gap simply absent, so the moving averages at week 40 spanned into the
previous spring; that gave 10 of 27 and a 7.17-wk crossing advantage. The
three seasons that differ (1998-99, 2001-02, 2002-03) are ones where the
pre-season weeks are zero-filled, so D at week 40 there rests on the fill.
The year-round-reporting subset (2003-04 onward, 21 paired seasons) is
identical under both conventions and is printed separately for that reason.

Usage:
  python flu_onset_boundary_diagnostic.py            # fetches data
  python flu_onset_boundary_diagnostic.py ilinet.json  # uses a saved pull
Writes flu_onset_boundary_diagnostic.csv next to the script.
"""
import json, sys, csv, os, urllib.request
from datetime import date, timedelta

EXCLUDE = {2009, 2020}          # per paper Appendix A.3 (no level onset; peak < 2.0%)
FIRST, LAST = 1997, 2025        # candidate seasons 1997-98 .. 2025-26
YEAR_ROUND_FROM = 2003          # first season with weeks 21-39 reported
THR, LVL = 0.2, 1.0
WF, WS = 4, 12

def load(path=None):
    if path and os.path.exists(path):
        return json.load(open(path))["epidata"]
    url = "https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=199740-202640"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["epidata"]

def mmwr_start(y):
    """Sunday starting MMWR week 1 of year y (the week containing Jan 4)."""
    j4 = date(y, 1, 4)
    return j4 - timedelta(days=(j4.weekday() + 1) % 7)

def weeks_in_mmwr_year(y):
    return (mmwr_start(y + 1) - mmwr_start(y)).days // 7

def regrid(rows):
    """Continuous MMWR grid 1997w40..last observed week; missing weeks -> 0.0
    (the pinned file's representation of the early non-reporting summers)."""
    obs = {e: w for e, w in rows}
    last = rows[-1][0]
    grid = []
    y, w = 1997, 40
    while y * 100 + w <= last:
        grid.append(y * 100 + w)
        w += 1
        if w > weeks_in_mmwr_year(y):
            y, w = y + 1, 1
    return grid, [obs.get(e, 0.0) for e in grid], [e for e in grid if e not in obs]

def sma(x, n):
    return [None if i < n - 1 else sum(x[i - n + 1:i + 1]) / n for i in range(len(x))]

def main():
    d = sorted(load(sys.argv[1] if len(sys.argv) > 1 else None), key=lambda r: r["epiweek"])
    wk, w, missing = regrid([(r["epiweek"], float(r["wili"])) for r in d])
    in_season_fill = [e for e in missing if e % 100 >= 40 or e % 100 <= 20]
    print(f"grid: {len(d)} observed -> {len(wk)} continuous MMWR weeks, {len(missing)} zero-filled "
          f"({len(in_season_fill)} inside season windows)")
    f, s = sma(w, WF), sma(w, WS)
    D = [None if (a is None or b is None) else a - b for a, b in zip(f, s)]
    rows = []
    for sy in range(FIRST, LAST + 1):
        idx = [i for i, e in enumerate(wk) if (e // 100 == sy and e % 100 >= 40) or (e // 100 == sy + 1 and e % 100 <= 20)]
        if len(idx) < 20:
            continue
        onset = next((i for i in idx if D[i] is not None and D[i] > THR), None)
        base = sum(w[i] for i in idx[:4]) / 4
        level = next((i for i in idx if w[i] > base + LVL), None)
        cross = next((i for i in idx if D[i] is not None and D[i] > THR and D[i-1] is not None and D[i-1] <= THR), None)
        peak = max(idx, key=lambda i: w[i])
        rows.append(dict(
            season=f"{sy}-{str(sy+1)[2:]}", paired=(sy not in EXCLUDE), year_round=(sy >= YEAR_ROUND_FROM),
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
    with open(out, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)

    def report(P, label):
        n = len(P); fw = sum(r["fired_first_week"] for r in P)
        md = sum(r["div_lead"] for r in P) / n; ml = sum(r["level_lead"] for r in P) / n
        C = [r for r in P if r["cross_lead"] is not None]
        mc = sum(r["cross_lead"] for r in C) / len(C); mlc = sum(r["level_lead"] for r in C) / len(C)
        B = [r["div_lead"] - r["level_lead"] for r in P if r["fired_first_week"]]
        N = [r["div_lead"] - r["level_lead"] for r in P if not r["fired_first_week"]]
        print(f"\n[{label}] paired seasons: {n}")
        print(f"registered rule: mean div lead {md:.3f} wk, mean level lead {ml:.3f} wk, advantage {md-ml:.3f} wk, "
              f"div first in {sum(r['div_lead']>r['level_lead'] for r in P)} of {n}")
        print(f"FIRED ON FIRST ELIGIBLE WEEK (boundary): {fw} of {n}  -> "
              + ", ".join(r["season"] for r in P if r["fired_first_week"]))
        print(f"advantage in boundary seasons {sum(B)/len(B):.2f} wk (n={len(B)}) vs non-boundary {sum(N)/len(N):.2f} wk (n={len(N)})")
        print(f"strict crossing rule: scorable {len(C)} of {n}; mean cross lead {mc:.3f} wk vs level {mlc:.3f} wk, "
              f"advantage {mc-mlc:.3f} wk, div first in {sum(r['cross_lead']>r['level_lead'] for r in C)} of {len(C)}")
        print("no in-window crossing (D already > 0.2 at week 40 and stayed there): "
              + ", ".join(r["season"] for r in P if r["cross_lead"] is None))

    P = [r for r in rows if r["paired"] and r["level_lead"] is not None and r["div_lead"] is not None]
    report(P, "all paired seasons, paper convention")
    report([r for r in P if r["year_round"]], f"year-round reporting era, {YEAR_ROUND_FROM}-{str(YEAR_ROUND_FROM+1)[2:]} onward")
    print(f"\nwrote {out}")

if __name__ == "__main__":
    main()
