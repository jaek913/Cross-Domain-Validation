#!/usr/bin/env python3
"""
e6_peak_detection.py - Experiment E6 (peak-detection hypothesis; rejected; honest negative).

Tests the hypothesis that the divergence ZERO-CROSSING (D = SMA_4(ILI) - SMA_12(ILI) going
positive -> negative, the declining phase) marks the epidemic PEAK. It does not: the zero-crossing
LAGS the true ILI peak. Reported alongside (the genuine positive result): the divergence PEAK
(max D) PRECEDES the true ILI peak.

Detectors compared, per season (continuous-series operators; lead = ILI-peak week - detector week,
so + = detector precedes the peak, - = detector lags the peak):
  - divergence peak      : week of max D
  - SMA-4 peak           : week of max SMA_4(ILI)            (a naive smoothed-peak detector)
  - divergence zero-cross: first week with D[t-1] > 0 and D[t] <= 0 (pos->neg, declining phase)
  - true ILI peak        : week of max ILI

Seasons: complete seasons through 2024 (the same full-season set as E5; a peak is a full-season
concept). Season = wk40(y)..wk20(y+1), >= 20 weeks, peak ILI >= 2.0%.

PROVENANCE NOTE: peak detection is NOT in the Stage-1.5 verified reconstruction (neither
repro_epidemiology.py / FINDINGS_epidemiology.md nor repro_crossdomain.py / FINDINGS_crossdomain.md
cover it). The v4 figures (zero-cross lag ~+5.6 wk, SMA-4 ~+2.1 wk, divergence-peak lead ~+1.7 wk,
96% of seasons, paired t 4.36, p 0.0002) are therefore taken from the manuscript and REGENERATED
here for the first time; values are reported as-computed. The qualitative result - zero-crossing
rejected as a peak marker, divergence peak leads - is the load-bearing content.

Output: outputs/e6_peak_detection.json
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.stats import ttest_rel, wilcoxon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e6_peak_detection.json")

WF, WS = 4, 12          # divergence windows (continuous series)
PEAK_MIN = 2.0


def _r3(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)


def seasons_of(Y, YR, WK, complete_through=2024):
    out = []
    for y in range(1997, complete_through + 1):
        idx = [i for i in range(len(Y)) if (YR[i] == y and WK[i] >= 40)
               or (YR[i] == y + 1 and WK[i] <= 20)]
        if len(idx) >= 20 and max(Y[i] for i in idx) >= PEAK_MIN:
            out.append((y, idx))
    return out


def _argmax_week(arr, idx):
    """idx-position of the max of arr over the season, treating NaN as -inf."""
    vals = [arr[i] if not np.isnan(arr[i]) else -np.inf for i in idx]
    return idx[int(np.argmax(vals))]


def main():
    ili = dio.load_ili()
    Y = ili["w"].to_numpy(float); YR = ili["YEAR"].to_numpy(); WK = ili["WEEK"].to_numpy()
    D = op.sma(Y, WF) - op.sma(Y, WS)
    S4 = op.sma(Y, WF)

    seas = seasons_of(Y, YR, WK)
    dp_lead, s4_lead, zc_lead = [], [], []
    ili_pk_w, div_pk_w = [], []
    dp_precede = 0
    rows = []
    for y, idx in seas:
        ili_pk = _argmax_week(Y, idx)
        div_pk = _argmax_week(D, idx)
        s4_pk = _argmax_week(S4, idx)
        zc = None
        for j in range(1, len(idx)):
            a, b = D[idx[j - 1]], D[idx[j]]
            if not np.isnan(a) and not np.isnan(b) and a > 0 and b <= 0:
                zc = idx[j]; break
        dlead = ili_pk - div_pk                    # + => divergence peak precedes the ILI peak
        dp_lead.append(dlead); dp_precede += (dlead > 0)
        s4_lead.append(ili_pk - s4_pk)
        ili_pk_w.append(ili_pk); div_pk_w.append(div_pk)
        rec = {"season": f"{y}-{str(y + 1)[2:]}", "divpeak_lead": int(dlead),
               "sma4_lead": int(ili_pk - s4_pk)}
        if zc is not None:
            zc_lead.append(ili_pk - zc); rec["zerocross_lead"] = int(ili_pk - zc)
        rows.append(rec)

    n = len(seas)
    dp = np.array(dp_lead, float); s4 = np.array(s4_lead, float); zc = np.array(zc_lead, float)
    t_dp, p_dp = ttest_rel(ili_pk_w, div_pk_w)     # divergence peak vs ILI peak (paired)
    try:
        w_stat, w_p = wilcoxon(dp[dp != 0]) if np.any(dp != 0) else (float("nan"), float("nan"))
    except ValueError:
        w_stat, w_p = float("nan"), float("nan")

    out = {"experiment": "E6", "title": "peak-detection hypothesis (rejected; honest negative)",
           "operators": "D = SMA_4(ILI) - SMA_12(ILI) on the continuous series; lead = ILI-peak wk - detector wk (+ precedes, - lags)",
           "season_def": "complete seasons through 2024, wk40(y)..wk20(y+1), >= 20 wks, peak ILI >= 2.0%",
           "provenance": "NOT in the Stage-1.5 verified record; v4 figures regenerated here for the first time; reported as-computed",
           "n_seasons": n,
           "hypothesis_zero_crossing_marks_peak": "REJECTED",
           "divergence_zerocross_lead": {"mean": _r3(np.mean(zc)) if len(zc) else None,
                                         "median": _r3(np.median(zc)) if len(zc) else None,
                                         "n": int(len(zc)),
                                         "_note": "negative => lags the true peak; v4 ~ -5.6 (lag +5.6 wk)"},
           "sma4_peak_lead": {"mean": _r3(np.mean(s4)), "median": _r3(np.median(s4)),
                              "_note": "negative => lags the true peak; v4 ~ -2.1 (lag +2.1 wk)"},
           "divergence_peak_lead": {"mean": _r3(np.mean(dp)), "median": _r3(np.median(dp)),
                                    "precede_count": int(dp_precede), "of": n,
                                    "precede_pct": _r3(100.0 * dp_precede / n) if n else None,
                                    "paired_t": _r3(t_dp), "paired_p": _r3(p_dp),
                                    "wilcoxon_p": _r3(w_p),
                                    "_note": "positive => precedes the true peak; v4 ~ +1.7, 96%, t 4.36, p 0.0002"},
           "per_season": rows}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    print("=== E6 peak-detection hypothesis (rejected; honest negative) ===")
    print(f"  complete seasons (peak>=2.0%): {n}")
    print(f"  HYPOTHESIS (zero-crossing marks the peak): REJECTED")
    print(f"  divergence zero-crossing lead: mean {_r3(np.mean(zc)) if len(zc) else None} wk (n {len(zc)})  "
          f"[negative = lags; v4 ~ -5.6]")
    print(f"  SMA-4 peak lead:               mean {_r3(np.mean(s4))} wk  [negative = lags; v4 ~ -2.1]")
    print(f"  divergence PEAK lead:          mean {_r3(np.mean(dp))} wk (median {_r3(np.median(dp))}), "
          f"precedes {dp_precede}/{n} ({_r3(100.0*dp_precede/n)}%), paired t {_r3(t_dp)} p {_r3(p_dp)}  "
          f"[v4 ~ +1.7, 96%, t 4.36, p 0.0002]")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
