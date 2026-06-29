#!/usr/bin/env python3
"""
e7b_regional_consistency.py - E7 follow-up diagnostic: is there a CONSISTENT early region?

Motivation (author's question): the E7 pooled detector ('fire when 3 of 10 regions have turned')
asks only how early WHICHEVER region happens to peak first does so - it never asks whether the SAME
region(s) lead season after season. Those are different claims:
  - if a DIFFERENT region leads each year (positional noise), the single-earliest ~5-wk hindsight
    lead is NOT usable in real time (you do not know which region will be early) -> the E7 pooled H0
    stands and is complete;
  - if the SAME region(s) reliably lead (structural), there IS a usable signal and the pooled
    'any-3-of-10' detector was simply the wrong tool (it dilutes the one early leader with two
    coincident regions and waits until the peak) -> a TARGETED detector on the known-early region(s)
    could behave very differently, and E7's H0 would be incomplete.

This script settles it WITHOUT new data, reusing the E7 season set + operators verbatim:
  PART A (hindsight, descriptive): per-region lead over the national peak across the 27 seasons, and
    whether 'who leads' is CONCENTRATED in a few regions (chi-square vs uniform) or spread evenly
    (= random / positional noise).
  PART B (the honest test): a TARGETED causal detector that watches the consistently-early region(s)
    and fires when the FIRST of them rolls over - evaluated LEAVE-ONE-SEASON-OUT (the leading regions
    are selected from the OTHER 26 seasons only, never the season being scored), so data-driven region
    selection cannot manufacture the lead. Reported for K=1/2/3 watched regions and for frac=0.5
    (primary) and frac=0.75 (the genuine-rollover robustness end - the same artifact check as E7). An
    in-sample (all-27-selection) ceiling is reported separately and labeled overfit-prone.

If a region leads far above chance AND the LOO targeted detector gives a positive lead that survives
frac=0.75, there is a real, generalizing, usable signal and E7's pooled H0 is INCOMPLETE. Otherwise
the pooled H0 is robust and complete (the ~5-wk single-earliest lead is positional noise).

This is a diagnostic - it informs the E7 disposition; it is not itself a pre-registered LB claim.

Output: outputs/e7b_regional_consistency.json
"""
from __future__ import annotations
import json, os, sys
from collections import Counter
import numpy as np
from scipy.stats import chisquare

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio
from e7_spatial_peak import (_argmax_pos, seasons_of, region_turn_rollover, lead_stats,
                             WF, WS, FRAC_PRIMARY, _r3)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e7b_regional_consistency.json")
FRAC_ROBUST = 0.75
KSET = [1, 2, 3]


def main():
    ili = dio.load_ili()
    Y = ili["w"].to_numpy(float); YR = ili["YEAR"].to_numpy(); WK = ili["WEEK"].to_numpy()
    reg = dio.load_ili_regional(ili)
    W, labels = reg["W"], reg["labels"]
    nreg = len(labels)
    Dr = np.vstack([op.sma(W[r], WF) - op.sma(W[r], WS) for r in range(nreg)])  # regional divergence

    seas = seasons_of(Y, YR, WK)
    n = len(seas)
    npp = [_argmax_pos(Y, idx) for _, idx in seas]            # national peak position per season

    # per-season, per-region hindsight peak position + lead over the national peak
    rp = np.zeros((n, nreg), int)                            # region peak position
    for s, (_, idx) in enumerate(seas):
        for r in range(nreg):
            rp[s, r] = _argmax_pos(W[r], idx)
    lead = np.array(npp)[:, None] - rp                       # (n, nreg); + => region peaks before nation

    def _score(r):
        return (float(np.median(lead[:, r])), float(np.mean(lead[:, r] > 0)))

    # ---- PART A: per-region consistency (hindsight) ---------------------------
    per_region = []
    for r in range(nreg):
        col = lead[:, r]
        per_region.append({
            "region": labels[r],
            "median_lead": _r3(np.median(col)), "mean_lead": _r3(np.mean(col)),
            "lead_freq_pct": _r3(100.0 * np.mean(col > 0)),
            "lead_ge2_pct": _r3(100.0 * np.mean(col >= 2)),
            "max_lead": int(col.max()), "min_lead": int(col.min())})
    # earliest-region credit (ties split): per season the regions at the min peak position share 1.0
    credit = np.zeros(nreg)
    sole_earliest = np.zeros(nreg, int)
    for s in range(n):
        m = rp[s].min()
        tied = np.where(rp[s] == m)[0]
        credit[tied] += 1.0 / len(tied)
        if len(tied) == 1:
            sole_earliest[tied[0]] += 1
    for r in range(nreg):
        per_region[r]["earliest_credit"] = _r3(credit[r])
        per_region[r]["times_sole_earliest"] = int(sole_earliest[r])

    exp = n / nreg                                           # uniform expectation (sums to n)
    chi2, pchi = chisquare(credit, f_exp=[exp] * nreg)
    order = list(np.argsort(-credit))
    concentrated = bool(pchi < 0.05)
    concentration = {
        "_what": "is 'which region leads' concentrated in a few regions (structural) or spread "
                 "uniformly (positional noise)? earliest-credit per region (seasons where the region "
                 "is at the earliest peak week, ties split); chi-square vs the uniform expectation",
        "expected_credit_per_region_if_uniform": _r3(exp),
        "chi2": _r3(chi2), "p_value": _r3(pchi),
        "most_often_earliest": labels[order[0]], "its_credit": _r3(credit[order[0]]),
        "interpretation": ("CONCENTRATED (some regions lead above chance) - a structural early region "
                           "may exist" if concentrated else
                           "NOT distinguishable from uniform - leadership is spread across regions "
                           "(positional noise); no consistent early region")}
    best_r = max(range(nreg), key=_score)
    single_best = {"region": labels[best_r], "median_lead": _r3(np.median(lead[:, best_r])),
                   "lead_freq_pct": _r3(100.0 * np.mean(lead[:, best_r] > 0)),
                   "_note": "the most-consistently-early region IN-SAMPLE (by median hindsight lead); "
                            "Part B tests whether watching it generalizes out-of-sample"}

    # ---- PART B: targeted causal detector, LEAVE-ONE-SEASON-OUT ----------------
    def fire_pos(frac):
        F = np.full((n, nreg), -1, int)                      # -1 = never fired
        for s, (_, idx) in enumerate(seas):
            for r in range(nreg):
                f = region_turn_rollover(Dr[r], idx, frac)
                F[s, r] = f if f is not None else -1
        return F
    Ffrac = {fr: fire_pos(fr) for fr in (FRAC_PRIMARY, FRAC_ROBUST)}

    def loo_targeted(K, frac):
        """For each season s, pick the top-K regions by score over the OTHER seasons, then fire at the
        EARLIEST rollover among them on season s. Returns (causal leads, picks, hindsight-ceiling leads)."""
        F = Ffrac[frac]
        leads, ceil_leads, picks = [], [], []
        for s in range(n):
            others = [s2 for s2 in range(n) if s2 != s]
            score = [(float(np.median(lead[others, r])), float(np.mean(lead[others, r] > 0)))
                     for r in range(nreg)]
            sel = sorted(range(nreg), key=lambda r: score[r], reverse=True)[:K]
            picks.append([labels[r] for r in sel])
            fires = [F[s, r] for r in sel if F[s, r] >= 0]      # causal rollover among selected
            leads.append((npp[s] - min(fires)) if fires else None)
            ceil_leads.append(npp[s] - min(rp[s, r] for r in sel))  # best a perfect detector could do
        return leads, picks, ceil_leads

    part_b = {}
    for K in KSET:
        kb = {}
        for fr in (FRAC_PRIMARY, FRAC_ROBUST):
            leads, picks, ceil_leads = loo_targeted(K, fr)
            entry = {**lead_stats(leads), "n_fired": int(sum(x is not None for x in leads))}
            if fr == FRAC_PRIMARY:
                entry["hindsight_ceiling"] = {**lead_stats(ceil_leads)}
                entry["selected_regions_per_season"] = picks
            kb[f"frac_{fr}"] = entry
        part_b[f"K_{K}"] = kb

    # selection stability for K=1 (how often the SAME region is chosen across LOO folds)
    k1picks = [p[0] for p in part_b["K_1"]["frac_0.5"]["selected_regions_per_season"]]
    mode, mc = Counter(k1picks).most_common(1)[0]
    part_b["K_1"]["frac_0.5"]["selection_stability"] = {
        "most_chosen_region": mode, "chosen_in_seasons": int(mc), "of": n,
        "_note": "if the SAME region is chosen in most LOO folds, selection is stable (a consistent "
                 "leader); if it jitters across regions, there is no consistent leader and any LOO "
                 "lead is luck"}

    # in-sample ceiling (K=1, region chosen from ALL seasons) - overfit-prone, labeled
    sel_all = max(range(nreg), key=_score)
    is_leads = [(npp[s] - Ffrac[FRAC_PRIMARY][s, sel_all]) if Ffrac[FRAC_PRIMARY][s, sel_all] >= 0
                else None for s in range(n)]
    in_sample_ceiling = {"region": labels[sel_all], **lead_stats(is_leads),
                         "_note": "OVERFIT-PRONE: region chosen using all 27 seasons then scored on the "
                                  "same seasons; an optimistic ceiling, not an honest estimate - compare "
                                  "to the LOO K=1 result"}

    # ---- verdict --------------------------------------------------------------
    loo1 = part_b["K_1"]["frac_0.5"]; loo1r = part_b["K_1"]["frac_0.75"]
    loo_positive = ((loo1.get("median") or -1) > 0 and (loo1.get("mean") or -1) > 0
                    and loo1.get("p_vs0") is not None and loo1["p_vs0"] < 0.05)
    loo_robust = ((loo1r.get("median") or -1) > 0 and (loo1r.get("mean") or -1) > 0
                  and loo1r.get("p_vs0") is not None and loo1r["p_vs0"] < 0.05)
    if concentrated and loo_positive and loo_robust:
        verdict = ("TARGETED SIGNAL EXISTS: leadership is concentrated (some regions lead above chance) "
                   "AND a leave-one-season-out detector that watches the consistently-early region(s) "
                   "gives a significant positive lead that SURVIVES the genuine-rollover threshold "
                   "(frac=0.75). The pooled E7 H0 is INCOMPLETE - a targeted detector works where the "
                   "any-3-of-10 pool did not. Reconsider E7's disposition.")
    elif concentrated and loo_positive and not loo_robust:
        verdict = ("WEAK/NOISE: leadership is concentrated and the LOO targeted lead is positive at "
                   "frac=0.5 but does NOT survive frac=0.75 - the same regional-noise artifact as the "
                   "pool. No robust usable lead; the pooled E7 H0 stands.")
    elif not concentrated:
        verdict = ("NO CONSISTENT LEADER: 'which region leads' is not distinguishable from uniform - a "
                   "different region leads each season (positional noise). The single-earliest ~5-wk "
                   "hindsight lead is NOT usable in real time. The pooled E7 H0 is ROBUST and COMPLETE.")
    else:
        verdict = ("NO GENERALIZING LEAD: the LOO targeted detector does not give a significant positive "
                   "out-of-sample lead. The pooled E7 H0 stands.")

    out = {"experiment": "E7b",
           "title": "regional-consistency diagnostic (is there a consistently early region?) - E7 follow-up",
           "n_seasons": n, "n_regions": nreg, "regions": labels,
           "method": "hindsight per-region lead + chi-square concentration; LEAVE-ONE-SEASON-OUT "
                     "targeted causal detector (region selection from the other 26 seasons only); "
                     "operators + season set identical to E7. Diagnostic, not a pre-registered LB claim.",
           "part_a_consistency": {"per_region": per_region, "concentration": concentration,
                                  "single_best_region_in_sample": single_best},
           "part_b_targeted_loo": part_b,
           "in_sample_ceiling_K1": in_sample_ceiling,
           "verdict": verdict}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    print("=== E7b regional-consistency diagnostic (is there a consistently early region?) ===")
    print(f"  seasons {n}  regions {nreg}")
    print("  [Part A: per-region hindsight lead over the national peak, sorted earliest-first]")
    for pr in sorted(per_region, key=lambda d: d["median_lead"], reverse=True):
        print(f"    {pr['region']:<11} median {pr['median_lead']:>5}  mean {pr['mean_lead']:>6}  "
              f"leads {pr['lead_freq_pct']:>5}%  earliest-credit {pr['earliest_credit']:>4} "
              f"(sole {pr['times_sole_earliest']})")
    c = concentration
    print(f"  [concentration] chi2 {c['chi2']} p {c['p_value']} (uniform credit/region "
          f"{c['expected_credit_per_region_if_uniform']}) -> {c['interpretation']}")
    print(f"  [single best region in-sample] {single_best['region']}: median lead "
          f"{single_best['median_lead']} wk, leads {single_best['lead_freq_pct']}% of seasons")
    print("  [Part B: LEAVE-ONE-SEASON-OUT targeted detector - watch the early region(s), fire on the earliest rollover]")
    for K in KSET:
        a = part_b[f"K_{K}"]["frac_0.5"]; b = part_b[f"K_{K}"]["frac_0.75"]; cl = a["hindsight_ceiling"]
        print(f"    K={K}: frac0.5 lead median {a.get('median')} mean {a.get('mean')} "
              f"lead% {a.get('lead_pct')} p {a.get('p_vs0')} (fired {a['n_fired']}/{n}) | "
              f"frac0.75 median {b.get('median')} p {b.get('p_vs0')} | "
              f"hindsight ceiling median {cl.get('median')}")
    st = part_b["K_1"]["frac_0.5"]["selection_stability"]
    print(f"  [K=1 selection stability] most-chosen region {st['most_chosen_region']} in "
          f"{st['chosen_in_seasons']}/{st['of']} LOO folds")
    ic = in_sample_ceiling
    print(f"  [in-sample ceiling K=1, OVERFIT-PRONE] region {ic['region']}: lead median {ic.get('median')} "
          f"mean {ic.get('mean')} p {ic.get('p_vs0')}")
    print(f"  VERDICT: {verdict}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
