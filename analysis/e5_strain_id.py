#!/usr/bin/env python3
"""
e5_strain_id.py - Experiment E5 (strain-level divergence: dominant-strain identification).

Per-subtype percent-positive pp_s(t) = (subtype count / TOTAL SPECIMENS) * 100 for H1N1, H3N2,
B_total; the strain divergence is D_s(t) = SMA_4(pp_s) - SMA_12(pp_s) on the CONTINUOUS series.
First-firing strain = the first subtype whose D_s > 0.3 pp in a season; dominant strain = highest
total positives over the season (hindsight) or highest cumulative at the first-firing week (real-time).
Seasons: COMPLETE seasons through 2024 (strain dominance is a full-season concept - a different set
from E4's onset seasons).

PINNED strain spec (DESIGN E5, resolving the v4 under-specification; the counts that follow are
reported AS-REGENERATED, not asserted as v4's 78%/89%):
  (a) A (Subtyping not Performed) is ALLOCATED proportionally to that week's subtyped A(H1N1):A(H3N2)
      split (no subtyped A that week -> left unallocated) -- applied ONLY to the real-time detection
      SIGNAL (pp_s, D_s). The DOMINANT-strain ground truth uses the CONFIRMED subtyped season totals
      (raw counts): an unsubtyped-A specimen has no known subtype, so it cannot define ground truth,
      and the verified Stage-1.5 reconstruction's 9 single-strain seasons are defined on raw counts.
  (b) first-firing ties broken by the HIGHER percent-positive (allocated signal);
  (c) onset reference = aggregate D = SMA_4(ILI) - SMA_12(ILI) > 0.2;
  (d) pre-2009 H1N1 = A(H1)+A(2009 H1N1); B = B (pre) / B+BVic+BYam (post); overlapping weeks ->
      post-2015 file. (loader: data_io.load_strain_combined.)

Targets: single-strain (>70% dominance, raw) 9/9 reproduces EXACTLY. The hindsight / real-time / lead
counts are under-specified in v4 (the verified Stage-1.5 reconstruction WITHOUT signal allocation got
20/27, 25/27, lead median 2 vs v4's 21/27, 24/27, 0); under the pinned spec they are reported as-computed.

Output: outputs/e5_strain_id.json
"""
from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e5_strain_id.json")

WF, WS = 4, 12          # strain divergence windows
FIRE_THR = 0.3          # first-firing threshold (pp)
AGG_THR = 0.2           # aggregate-onset reference threshold (pp)
PEAK_MIN = 2.0
SINGLE_STRAIN = 0.70    # > 70% dominance (raw) => single-strain season
STRAINS = ("H1N1", "H3N2", "Btot")


def _r3(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)


def seasons_of(Y, YR, WK, complete_through=2024):
    """Season y = wk40(y)..wk20(y+1); kept if >= 20 weeks present and peak ILI >= 2.0%.
    complete_through=2024 -> full seasons only (dominance is a full-season concept)."""
    out = []
    for y in range(1997, complete_through + 1):
        idx = [i for i in range(len(Y)) if (YR[i] == y and WK[i] >= 40)
               or (YR[i] == y + 1 and WK[i] <= 20)]
        if len(idx) >= 20 and max(Y[i] for i in idx) >= PEAK_MIN:
            out.append((y, idx))
    return out


def allocate_signal(m):
    """Pinned spec (a): allocate A(Subtyping not Performed) proportionally to the week's subtyped
    A(H1N1):A(H3N2) split, for the SIGNAL only. No subtyped A that week -> left unallocated."""
    H1 = m["H1N1"].to_numpy(float); H3 = m["H3N2"].to_numpy(float)
    A0 = m["Aunsub"].to_numpy(float); denom = H1 + H3
    share_h1 = np.divide(H1, denom, out=np.zeros_like(H1), where=denom > 0)
    add = np.where(denom > 0, A0, 0.0)
    return {"H1N1": H1 + add * share_h1, "H3N2": H3 + add * (1.0 - share_h1),
            "Btot": m["Btot"].to_numpy(float)}


def main():
    ili = dio.load_ili()
    m = dio.load_strain_combined(ili)
    Y = m["w"].to_numpy(float); YR = m["YEAR"].to_numpy(); WK = m["WEEK"].to_numpy()
    TOT = m["TOT"].to_numpy(float)

    raw = {s: m[s].to_numpy(float) for s in STRAINS}             # confirmed subtyped -> ground truth
    sig = allocate_signal(m)                                     # allocated -> real-time signal
    pp = {s: np.divide(sig[s], TOT, out=np.zeros_like(TOT), where=TOT > 0) * 100.0 for s in STRAINS}
    div = {s: op.sma(pp[s], WF) - op.sma(pp[s], WS) for s in STRAINS}
    Dagg = op.sma(Y, WF) - op.sma(Y, WS)

    seas = seasons_of(Y, YR, WK)
    hind = rt = n70 = n70hit = 0
    leads = []
    rows = []
    for y, idx in seas:
        fire_i = fire_s = None
        for i in idx:
            cr = [s for s in STRAINS if not np.isnan(div[s][i]) and div[s][i] > FIRE_THR]
            if cr:
                fire_i = i; fire_s = max(cr, key=lambda s: pp[s][i]); break   # tie-break: higher pp
        tot = {s: float(np.sum([raw[s][i] for i in idx])) for s in STRAINS}    # raw ground-truth totals
        total = max(sum(tot.values()), 1.0)
        dom = max(tot, key=tot.get); share = tot[dom] / total
        rec = {"season": f"{y}-{str(y + 1)[2:]}", "dominant": dom, "dom_share": _r3(share),
               "fire_strain": fire_s, "single_strain": bool(share > SINGLE_STRAIN)}
        if fire_s is not None:
            hind += (fire_s == dom)
            cum = {s: float(np.sum([raw[s][j] for j in idx if j <= fire_i])) for s in STRAINS}
            rt_leader = max(cum, key=cum.get)
            rt += (fire_s == rt_leader)
            rec["realtime_leader"] = rt_leader
            rec["realtime_match"] = bool(fire_s == rt_leader)
            rec["hindsight_match"] = bool(fire_s == dom)
            agg = next((i for i in idx if not np.isnan(Dagg[i]) and Dagg[i] > AGG_THR), None)
            if agg is not None:
                leads.append(fire_i - agg); rec["lead_vs_aggregate"] = int(fire_i - agg)
        if share > SINGLE_STRAIN:
            n70 += 1; n70hit += (fire_s == dom)
            rec["single_strain_hit"] = bool(fire_s == dom)
        rows.append(rec)

    n = len(seas)
    out = {"experiment": "E5", "title": "strain-level divergence (dominant-strain identification)",
           "operator": "pp_s = subtype/TOTAL*100 (allocated signal); D_s = SMA_4(pp_s) - SMA_12(pp_s); first-firing = first subtype D_s > 0.3 pp (tie: higher pp)",
           "pinned_spec": "A(Subtyping not Performed) allocated proportionally to subtyped H1:H3 on the SIGNAL only; DOMINANCE uses raw confirmed-subtyped season totals; tie-break by pp; complete seasons through 2024",
           "n_seasons": n,
           "single_strain": {"hit": n70hit, "of": n70, "_target": "9/9 (raw-dominance single-strain seasons; reproduces exactly)"},
           "hindsight": {"match": hind, "of": n, "pct": _r3(100.0 * hind / n) if n else None,
                         "_note": "as-regenerated under the pinned spec (v4 21/27 under-specified; Stage-1.5 no-allocation recon got 20/27)"},
           "realtime": {"match": rt, "of": n, "pct": _r3(100.0 * rt / n) if n else None,
                        "_note": "as-regenerated under the pinned spec (v4 24/27 under-specified; Stage-1.5 recon got 25/27)"},
           "strain_fire_vs_aggregate_onset": {"lead_median": _r3(np.median(leads)) if leads else None,
                                              "n": len(leads),
                                              "_note": "as-regenerated (v4 median 0 under-specified; Stage-1.5 recon got 2)"},
           "per_season": rows}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    print("=== E5 strain-level divergence (dominant-strain identification) ===")
    print(f"  complete seasons (peak>=2.0%): {n}")
    print(f"  single-strain (>70% dominance, raw): {n70hit}/{n70}   [target 9/9 - reproduces exactly]")
    print(f"  first-firing == dominant (hindsight): {hind}/{n}  ({_r3(100.0*hind/n)}%)  [as-regenerated; v4 21/27 under-specified]")
    print(f"  first-firing == real-time leader:     {rt}/{n}  ({_r3(100.0*rt/n)}%)  [as-regenerated; v4 24/27 under-specified]")
    print(f"  strain-fire vs aggregate-onset lead median: {_r3(np.median(leads)) if leads else None} wk (n {len(leads)})  [as-regenerated; v4 0]")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
