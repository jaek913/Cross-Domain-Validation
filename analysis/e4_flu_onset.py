#!/usr/bin/env python3
"""
e4_flu_onset.py - Experiment E4 (divergence-based influenza onset detection).

Weekly national % WEIGHTED ILI; the onset divergence is D(t) = SMA_4(ILI) - SMA_12(ILI) on the
CONTINUOUS series (the SMAs reach across season boundaries; only the onset SEARCH is season-bounded).
A season y = MMWR week 40(y) .. week 20(y+1); a season is testable if it has >= 20 weeks present and
peak ILI >= 2.0% (a low-activity season is untestable, not falsifying - DESIGN S4).

Detectors (per season):
  divergence onset = first week with D(t) > 0.2 pp        (sensitivity 0.1/0.2/0.3; 0.5 breaks)
  level comparator = first week ILI > baseline + 1.0 pp   (baseline = mean ILI over the season's
                                                           first 4 weeks ~ wk40-43; sens +0.5/+1.0/+1.5)
Lead is measured against the season PEAK week: lead = peak_wk - onset_wk (weeks of warning before the
peak). The paper's headline advantage is (level lead) - (divergence lead) per season = how many weeks
EARLIER the divergence fires than the level rule.

Seasons (DISC-1.4-03): 29 candidates (1997-98 .. 2025-26, incl. the partial 23-wk 2025-26); 27 enter
the paired comparison after the peak<2.0% drop (2020-21) and the no-level-onset drop (2009-10).

Targets (verified Stage-1.5 repro_epidemiology.py): divergence lead-vs-peak 14.1 wk, level lead-vs-peak
5.9 wk, advantage +8.2 wk, divergence earlier 26/27, paired t = 9.35; floor (min divergence lead vs
peak) 5 wk, Q1 12 wk. The temporal-concentration shuffle (z ~ +2.6 target) is a supporting robustness
diagnostic - NOT in the verified repro and NOT a load-bearing claim - reported here as-computed.

Output: outputs/e4_flu_onset.json
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.stats import ttest_rel, wilcoxon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e4_flu_onset.json")

WF, WS = 4, 12          # onset divergence windows (SMA_4 - SMA_12)
DIV_THR = 0.2           # primary divergence-onset threshold (pp)
LVL_ADD = 1.0           # primary level-onset increment over baseline (pp)
PEAK_MIN = 2.0          # season testability floor (peak ILI %)


def _r3(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)


def seasons_of(Y, YR, WK, complete_through=2025):
    """Season y = wk40(y)..wk20(y+1); kept if >= 20 weeks present and peak >= PEAK_MIN."""
    out = []
    for y in range(1997, complete_through + 1):
        idx = [i for i in range(len(Y)) if (YR[i] == y and WK[i] >= 40)
               or (YR[i] == y + 1 and WK[i] <= 20)]
        if len(idx) >= 20 and max(Y[i] for i in idx) >= PEAK_MIN:
            out.append((y, idx))
    return out


def _peak(idx, Y):
    return idx[int(np.argmax([Y[i] for i in idx]))]


def lead_div(idx, Y, D, thr):
    """Weeks from the divergence onset to the season peak (None if it never fires)."""
    pk = _peak(idx, Y)
    on = next((i for i in idx if not np.isnan(D[i]) and D[i] > thr), None)
    return None if on is None else pk - on


def lead_lvl(idx, Y, add):
    """Weeks from the level onset to the season peak (None if it never fires)."""
    pk = _peak(idx, Y)
    base = np.mean([Y[i] for i in idx[:4]])
    on = next((i for i in idx if Y[i] > base + add), None)
    return None if on is None else pk - on


def temporal_concentration_z(paired_idx, Y, nsh=2000, seed=0):
    """Robustness diagnostic (NOT load-bearing): null = replace each paired season's divergence
    onset with a uniformly random week from that season, recompute the lead-vs-peak, and compare the
    real mean divergence lead to the shuffled distribution. Tests whether the divergence onsets are
    temporally CONCENTRATED early in the season. Returns (real_mean, z)."""
    rng = np.random.default_rng(seed)
    real = np.array([dl for dl, _ in paired_idx], float)
    idxs = [idx for _, idx in paired_idx]
    sh = np.empty(nsh)
    for s in range(nsh):
        leads = []
        for idx in idxs:
            pk = _peak(idx, Y)
            leads.append(pk - idx[int(rng.integers(len(idx)))])
        sh[s] = np.mean(leads)
    return float(real.mean()), float((real.mean() - sh.mean()) / sh.std())


def main():
    ili = dio.load_ili()
    Y = ili["w"].values.astype(float)
    YR = ili["YEAR"].values
    WK = ili["WEEK"].values
    D = op.sma(Y, WF) - op.sma(Y, WS)

    seas = seasons_of(Y, YR, WK)                 # candidates after the peak>=2.0 drop

    dl, ll, earlier = [], [], 0
    paired_idx = []                              # (div_lead, idx) for the seasons that enter the pair
    per_season = []
    for y, idx in seas:
        a = lead_div(idx, Y, D, DIV_THR)
        b = lead_lvl(idx, Y, LVL_ADD)
        paired = a is not None and b is not None
        if paired:
            dl.append(a); ll.append(b); earlier += (a > b); paired_idx.append((a, idx))
        per_season.append({"season": f"{y}-{str(y + 1)[2:]}", "div_lead": a, "level_lead": b,
                           "paired": bool(paired), "earlier": bool(paired and a > b)})
    dl, ll = np.array(dl, float), np.array(ll, float)
    adv = dl - ll
    t, p = ttest_rel(dl, ll)
    w_stat, w_p = wilcoxon(dl, ll)

    sens = {}
    for thr in (0.1, 0.2, 0.3):
        d2, l2, e2 = [], [], 0
        for _, idx in seas:
            a = lead_div(idx, Y, D, thr); b = lead_lvl(idx, Y, LVL_ADD)
            if a is not None and b is not None:
                d2.append(a); l2.append(b); e2 += (a > b)
        d2, l2 = np.array(d2, float), np.array(l2, float)
        sens[f"div>{thr}"] = {"advantage_mean": _r3((d2 - l2).mean()),
                              "earlier_pct": _r3(100.0 * e2 / len(d2)), "n": int(len(d2))}

    # 2A (Phase-5a): SYMMETRIC level-threshold sweep - the div sweep above moved only the FAVORABLE knob
    lvl_sens = {}
    for add in (0.5, 1.0, 1.5):
        d3, l3, e3c = [], [], 0
        for _, idx in seas:
            a = lead_div(idx, Y, D, DIV_THR); b = lead_lvl(idx, Y, add)
            if a is not None and b is not None:
                d3.append(a); l3.append(b); e3c += (a > b)
        d3, l3 = np.array(d3, float), np.array(l3, float)
        lvl_sens[f"lvl+{add}"] = {"advantage_mean": _r3((d3 - l3).mean()),
                                  "earlier_pct": _r3(100.0 * e3c / len(d3)) if len(d3) else None,
                                  "n": int(len(d3))}
    _lvl_adv = [v["advantage_mean"] for v in lvl_sens.values() if v["advantage_mean"] is not None]
    _div_adv = [v["advantage_mean"] for v in sens.values() if v["advantage_mean"] is not None]
    advantage_range_level = [min(_lvl_adv), max(_lvl_adv)]
    advantage_range_all = [min(_lvl_adv + _div_adv), max(_lvl_adv + _div_adv)]

    real_mean, tc_z = temporal_concentration_z(paired_idx, Y)

    out = {"experiment": "E4", "title": "divergence-based influenza onset detection",
           "operator": "D = SMA_4(ILI) - SMA_12(ILI) on the continuous series; onset = first week D > 0.2 pp",
           "level_comparator": "first week ILI > (mean of season's first 4 weeks) + 1.0 pp",
           "season_def": "wk40(y)..wk20(y+1), >= 20 weeks, peak ILI >= 2.0%",
           "n_candidate_seasons": len(seas), "n_paired": int(len(dl)),
           "divergence_lead_vs_peak": {"mean": _r3(dl.mean()), "median": _r3(np.median(dl)),
                                       "iqr": [_r3(np.percentile(dl, 25)), _r3(np.percentile(dl, 75))],
                                       "floor_min": _r3(dl.min()), "q1": _r3(np.percentile(dl, 25)),
                                       "_target": "mean 14.1, floor 5, Q1 12"},
           "level_lead_vs_peak": {"mean": _r3(ll.mean()), "_target": "mean 5.9"},
           "advantage_div_minus_level": {"mean": _r3(adv.mean()), "median": _r3(np.median(adv)),
                                         "earlier": int(earlier), "of": int(len(dl)),
                                         "paired_t": _r3(t), "paired_p": _r3(p),
                                         "wilcoxon_stat": _r3(w_stat), "wilcoxon_p": _r3(w_p),
                                         "_target": "advantage +8.2, earlier 26/27, t 9.35"},
           "sensitivity": sens,
           "level_sensitivity": lvl_sens,
           "advantage_range_level_sweep": advantage_range_level,
           "advantage_range_all_thresholds": advantage_range_all,
           "temporal_concentration_shuffle": {"div_lead_mean": _r3(real_mean), "z": _r3(tc_z),
                                               "_note": "robustness diagnostic only (random-onset-week null, seed 0); NOT load-bearing; v4 reported z ~ +2.6 by an under-determined shuffle"},
           "per_season": per_season,
           "excluded": [{"season": f"{y}-{str(y + 1)[2:]}",
                         "div_lead": next((s["div_lead"] for s in per_season if s["season"] == f"{y}-{str(y + 1)[2:]}"), None),
                         "level_lead": next((s["level_lead"] for s in per_season if s["season"] == f"{y}-{str(y + 1)[2:]}"), None)}
                        for y, idx in seas if not (lead_div(idx, Y, D, DIV_THR) is not None and lead_lvl(idx, Y, LVL_ADD) is not None)]}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    print("=== E4 divergence-based influenza onset detection ===")
    print(f"  candidate seasons (peak>=2.0%): {len(seas)}  ;  paired (div & level both fire): {len(dl)}  [target 27]")
    print(f"  divergence lead vs peak: mean {dl.mean():.1f}  median {np.median(dl):.1f}  "
          f"IQR {np.percentile(dl,25):.0f}-{np.percentile(dl,75):.0f}  floor {dl.min():.0f}  Q1 {np.percentile(dl,25):.0f}  [target 14.1 / floor 5 / Q1 12]")
    print(f"  level lead vs peak:      mean {ll.mean():.1f}  [target 5.9]")
    print(f"  advantage (div earlier): mean {adv.mean():.1f}  median {np.median(adv):.1f}  "
          f"earlier {earlier}/{len(dl)}  paired t {t:.2f} (p {p:.2g})  Wilcoxon p {w_p:.2g}  [target +8.2 / 26 / t 9.35]")
    for k, v in sens.items():
        print(f"    {k}: advantage {v['advantage_mean']}, earlier {v['earlier_pct']}% (n {v['n']})")
    print("  [2A] level-threshold sweep (div fixed at 0.2):")
    for k, v in lvl_sens.items():
        print(f"    {k}: advantage {v['advantage_mean']}, earlier {v['earlier_pct']}% (n {v['n']})")
    print(f"  [2A] advantage range - level sweep {advantage_range_level} ; all thresholds {advantage_range_all}")
    print(f"  temporal-concentration shuffle (diagnostic): div-lead mean {real_mean:.1f}, z {tc_z:+.2f}  (v4 ~+2.6, under-determined)")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
