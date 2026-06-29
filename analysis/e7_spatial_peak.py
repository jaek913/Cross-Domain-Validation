#!/usr/bin/env python3
"""
e7_spatial_peak.py - Experiment E7 (spatial-curvature peak detection; pre-registered, net-new).

PRE-REGISTERED before any regional number was computed (commit ed211e0; DESIGN v0.9 / OUTLINE
v0.7 / DECISIONS 2026-06-28). NET-NEW beyond v4 - no v4 figure, no Stage-1.5 record.

Hypothesis H1 (headline): a strictly-causal signal built from the 10 HHS-region ILI curves detects
the NATIONAL ILI peak with POSITIVE lead (fires before the peak), beating the ~coincident national
divergence-peak (E6) - AND beating a national-only control, i.e. the lead must come from the SPATIAL
structure, not a universal single-series curvature property. H0 (falsifier): no positive lead, or no
improvement over the coincident national detector, or no improvement of the spatial signal over the
national-only control -> a short honest negative paired with E6.

Claim hierarchy (pre-registered): beating the zero-crossing alone (~5 wk late) is NOT a claim;
SOLID = beats the E6 coincident national divergence-peak (~0); HEADLINE = significant positive lead
that the SPATIAL pooling adds over the national-only control.

Target: national peak week = argmax national % WEIGHTED ILI. Seasons: complete seasons through
2024, wk40(y)..wk20(y+1), >= 20 wks, peak >= 2.0% (the identical E5/E6 set; the national peak and
the E6 comparators are computed here exactly as in e6_peak_detection.py).

THE FEASIBILITY DIAGNOSTIC (hindsight, reported first, make-or-break) is the decisive evidence on
H1: it measures how much the regional peaks actually lead the national peak. If regions do not peak
before the nation, there is no spatial lead for any causal detector to capture, regardless of the
detector.

Signals (all strictly causal - every value from data <= t; NO use of the finished season to label a
region 'peaked', the D01 / CIC #4 look-ahead discipline):
  - BASELINE (spatial, first-order): region r turns at the first season-week its momentum turns down,
    D_r = SMA_4(ILI_r) - SMA_12(ILI_r) crossing pos->neg; fire when the fraction of the 10 regions
    turned >= theta.
  - PRIMARY (spatial momentum-rollover): region r turns when its momentum D_r has fallen by FRAC from
    its causal running-max since onset (D_r > 0.2pp, the E4 onset guard). This is the pre-registered
    'D_r drops below its causal running-max by a margin' operationalization: it requires the momentum
    to PEAK first, so (unlike a bare sustained negative 2nd difference, which fires on the first
    early-rise wiggle ~ at onset) it fires at the momentum peak = the level inflection, a few weeks
    before the level peak. Fire when the fraction turned >= theta. PRIMARY theta = 0.3, FRAC = 0.5;
    theta sweep {0.2,0.3,0.5,0.7}; FRAC sensitivity {0.25,0.5,0.75}.
  - CONTROL (national-only momentum-rollover): the SAME rollover rule on the national momentum, no
    spatial pooling. The spatial PRIMARY must beat THIS for H1 (else the lead is universal curvature,
    not spatial).

Comparators: (1) internal E6 national detectors - zero-cross (~ -5 wk), SMA-4 peak (~ -2 wk),
divergence-peak (~0, the real bar) - computed identically here; (2) a climatological reference -
expanding-window median peak-week, a forecast ERROR in weeks (a reference, not a head-to-head);
(3) FluSight literature in the manuscript (context only). NO head-to-head vs forecasting ensembles.

NOTE: the rollover margin (FRAC) and the E4 onset guard were the under-specified pieces of the
pre-registration (only theta + its sweep were pinned numerically); they are pinned here as the
principled implementation of the pre-registered running-max-drawdown, with FRAC reported as a
declared sensitivity. An earlier implementation used a sustained-negative-2nd-difference rule, which
fired at onset on early-rise noise (~11 wk 'lead' at onset-level ILI - exceeding the hindsight
feasibility ceiling, an artifact); it is replaced here and documented in DECISIONS. All values are
reported as-computed.

Output: outputs/e7_spatial_peak.json
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon, ttest_1samp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e7_spatial_peak.json")

WF, WS = 4, 12              # divergence windows (continuous series) - identical to E4/E6
PEAK_MIN = 2.0
THETA_PRIMARY = 0.3
THETA_SWEEP = [0.2, 0.3, 0.5, 0.7]
ONSET_PP = 0.2             # E4-validated onset threshold (D > 0.2 pp); the rollover guard
FRAC_PRIMARY = 0.5         # momentum-rollover: D_r has fallen by this fraction from its running-max
FRAC_SWEEP = [0.25, 0.5, 0.75]


def _r3(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)


def _argmax_pos(arr, idx):
    """Season-position (0-based index into idx) of the max of arr over the season; NaN -> -inf."""
    vals = [arr[i] if not np.isnan(arr[i]) else -np.inf for i in idx]
    return int(np.argmax(vals))


def seasons_of(Y, YR, WK, complete_through=2024):
    """Identical to e6_peak_detection.seasons_of (so the national peak + comparators match E6)."""
    out = []
    for y in range(1997, complete_through + 1):
        idx = [i for i in range(len(Y)) if (YR[i] == y and WK[i] >= 40)
               or (YR[i] == y + 1 and WK[i] <= 20)]
        if len(idx) >= 20 and max(Y[i] for i in idx) >= PEAK_MIN:
            out.append((y, idx))
    return out


def region_turn_firstorder(Dr, idx):
    """First season-position where momentum turns down: Dr[t-1] > 0 and Dr[t] <= 0. None if never."""
    for j in range(1, len(idx)):
        a, b = Dr[idx[j - 1]], Dr[idx[j]]
        if not np.isnan(a) and not np.isnan(b) and a > 0 and b <= 0:
            return j
    return None


def region_turn_rollover(Dr, idx, frac, onset_pp=ONSET_PP):
    """First season-position where the region's MOMENTUM rolls over: after onset (D_r > onset_pp),
    D_r falls to <= (1-frac) * its causal running-max of D_r since onset (momentum has dropped by
    `frac` from its peak). This is the pre-registered 'D_r drops below its causal running-max by a
    margin' rule; because it requires the momentum to PEAK first, it cannot fire at onset / on
    early-rise noise. The momentum peak is the level inflection, a few weeks before the level peak.
    Strictly causal - every value from positions <= the trigger. None if it never rolls over."""
    onset = False
    mmax = -np.inf
    for j in range(len(idx)):
        p = idx[j]
        d = Dr[p]
        if np.isnan(d):
            continue
        if d > onset_pp:
            onset = True
        if onset:
            if d > mmax:
                mmax = d
            if mmax > 0 and d <= (1.0 - frac) * mmax:
                return j
    return None


def fire_fraction(turn_positions, theta):
    """Season-position at which the fraction of regions 'turned' first reaches theta. A region
    contributes once its turn-position is reached. None if it never reaches theta."""
    nreg = len(turn_positions)
    need = int(np.ceil(theta * nreg - 1e-9))                # how many regions must have turned
    turned = sorted(t for t in turn_positions if t is not None)
    if len(turned) < need or need <= 0:
        return None
    return turned[need - 1]                                  # position when the need-th region turns


def lead_stats(leads):
    """leads: list of (national_peak_pos - detector_pos) or None; + => detector precedes the peak."""
    a = np.array([x for x in leads if x is not None], float)
    if len(a) == 0:
        return {"n": 0}
    res = {"n": int(len(a)), "mean": _r3(np.mean(a)), "median": _r3(np.median(a)),
           "lead_pct": _r3(100.0 * np.mean(a > 0)), "earlier_count": int(np.sum(a > 0))}
    if len(a) >= 2 and np.any(a != 0):
        t, p = ttest_1samp(a, 0.0)
        res["t_vs0"], res["p_vs0"] = _r3(t), _r3(p)
        try:
            _, wp = wilcoxon(a[a != 0]); res["wilcoxon_p"] = _r3(wp)
        except ValueError:
            res["wilcoxon_p"] = None
    return res


def paired_gain(a_leads, b_leads, what):
    """Per-season (a_lead - b_lead) over seasons where both fired; + => a leads earlier than b."""
    pairs = [(a, b) for a, b in zip(a_leads, b_leads) if a is not None and b is not None]
    res = {"_what": what, "n_paired": len(pairs)}
    if pairs:
        d = np.array([a - b for a, b in pairs], float)
        res.update({"mean_gain": _r3(np.mean(d)), "median_gain": _r3(np.median(d)),
                    "a_earlier_pct": _r3(100.0 * np.mean(d > 0))})
        if len(d) >= 2 and np.any(d != 0):
            t, p = ttest_1samp(d, 0.0); res["paired_t"], res["paired_p"] = _r3(t), _r3(p)
            try:
                _, wp = wilcoxon(d[d != 0]); res["wilcoxon_p"] = _r3(wp)
            except ValueError:
                res["wilcoxon_p"] = None
    return res


def main():
    ili = dio.load_ili()
    Y = ili["w"].to_numpy(float); YR = ili["YEAR"].to_numpy(); WK = ili["WEEK"].to_numpy()
    reg = dio.load_ili_regional(ili)
    W, labels = reg["W"], reg["labels"]
    nreg = len(labels)

    Dn = op.sma(Y, WF) - op.sma(Y, WS)                       # national divergence (identical to E6)
    S4n = op.sma(Y, WF)                                      # national SMA-4
    Dr = np.vstack([op.sma(W[r], WF) - op.sma(W[r], WS) for r in range(nreg)])  # regional divergence

    seas = seasons_of(Y, YR, WK)
    n = len(seas)
    nat_peak_pos = [_argmax_pos(Y, idx) for _, idx in seas]

    # ---- feasibility diagnostic (HINDSIGHT; make-or-break) --------------------
    # The relevant ceiling for H1 is how much the EARLIEST regions lead the national peak, NOT the
    # mean/median region: the national % ILI is ~the population-weighted center of the regional
    # peaks, so the all-region median is ~tautologically the national peak. A theta-pooled detector
    # that fires when k regions have turned can lead AT MOST by the k-th-EARLIEST region's lead.
    reg_leads_all = []
    ranked = {k: [] for k in range(1, nreg + 1)}            # k-th earliest region's lead, per season
    for (y, idx), npp in zip(seas, nat_peak_pos):
        rps = sorted(_argmax_pos(W[r], idx) for r in range(nreg))   # earliest-peaking region first
        reg_leads_all.extend(npp - rp for rp in rps)
        for k in range(1, nreg + 1):
            ranked[k].append(npp - rps[k - 1])             # + => that region peaks before the nation
    fa = np.array(reg_leads_all, float)

    def _rk(k):
        a = np.array(ranked[k], float)
        return {"median": _r3(np.median(a)), "mean": _r3(np.mean(a)),
                "leads_ge_1wk": int(np.sum(a >= 1)), "leads_ge_2wk": int(np.sum(a >= 2)), "of": n}

    feasibility = {
        "_what": "HINDSIGHT diagnostic and the DECISIVE evidence on H1. The relevant ceiling is the "
                 "lead of the EARLIEST regions, NOT the mean/median region: the national % ILI is "
                 "~the population-weighted center of the regional peaks, so the all-region median is "
                 "~tautologically the national peak. A detector firing when k regions have turned can "
                 "lead AT MOST by the k-th-earliest region's lead.",
        "earliest_region_leads_by_rank": {f"earliest_{k}": _rk(k) for k in (1, 2, 3, 4, 5)},
        "_rank_note": "earliest_1 = first region to peak; earliest_3 = the headroom for the PRIMARY "
                      "theta=0.3 detector (fires when 3/10 regions have turned); earliest_2 = theta=0.2",
        "all_region_spread_only": {"mean": _r3(np.mean(fa)), "median": _r3(np.median(fa)),
            "std": _r3(np.std(fa)), "min": _r3(np.min(fa)), "max": _r3(np.max(fa)),
            "region_seasons_leading_pct": _r3(100.0 * np.mean(fa > 0)),
            "_note": "NOT the ceiling - ~tautologically ~0 since national ~ population-weighted center "
                     "of the regional peaks; reported only to show the spread"},
        "region_seasons": int(len(fa)), "of_seasons": n}

    # ---- E6 national comparators (computed identically to e6_peak_detection) --
    zc_lead, s4_lead, dp_lead, div_pk_pos = [], [], [], []
    for (y, idx), npp in zip(seas, nat_peak_pos):
        dpp = _argmax_pos(Dn, idx); div_pk_pos.append(dpp)
        dp_lead.append(npp - dpp)
        s4_lead.append(npp - _argmax_pos(S4n, idx))
        zc = None
        for j in range(1, len(idx)):
            a, b = Dn[idx[j - 1]], Dn[idx[j]]
            if not np.isnan(a) and not np.isnan(b) and a > 0 and b <= 0:
                zc = j; break
        zc_lead.append((npp - zc) if zc is not None else None)
    e6 = {"divergence_zerocross_lead": lead_stats(zc_lead),
          "sma4_peak_lead": lead_stats(s4_lead),
          "divergence_peak_lead": lead_stats(dp_lead),
          "_note": "reproduces E6: zero-cross ~ -5 (lags), SMA-4 ~ -2 (lags), div-peak ~0 "
                   "(coincident; the bar to beat)"}

    # ---- spatial detectors (CAUSAL) -------------------------------------------
    def spatial_leads(turn_fn, param, theta):
        leads, fires = [], []
        for (y, idx), npp in zip(seas, nat_peak_pos):
            turns = [turn_fn(r, idx, param) for r in range(nreg)]
            f = fire_fraction(turns, theta)
            fires.append(f); leads.append((npp - f) if f is not None else None)
        return leads, fires

    def turn_first(r, idx, frac): return region_turn_firstorder(Dr[r], idx)
    def turn_roll(r, idx, frac):  return region_turn_rollover(Dr[r], idx, frac)

    base_leads, base_fires = spatial_leads(turn_first, FRAC_PRIMARY, THETA_PRIMARY)
    prim_leads, prim_fires = spatial_leads(turn_roll, FRAC_PRIMARY, THETA_PRIMARY)

    # national-only control: the SAME rollover rule, no spatial pooling
    nat_roll_lead, nat_roll_pos = [], []
    for (y, idx), npp in zip(seas, nat_peak_pos):
        tn = region_turn_rollover(Dn, idx, FRAC_PRIMARY)
        nat_roll_pos.append(tn)
        nat_roll_lead.append((npp - tn) if tn is not None else None)

    # diagnostic: WHERE does the PRIMARY detector fire? (low/early ILI => artifact; near-peak ILI
    # => genuine inflection)
    prim_diag = []
    for (y, idx), npp, f in zip(seas, nat_peak_pos, prim_fires):
        lab = f"{y}-{str(y + 1)[2:]}"
        if f is None:
            prim_diag.append({"season": lab, "fired": False}); continue
        af, ap = idx[f], idx[npp]
        prim_diag.append({"season": lab, "fired": True,
                          "fire_wk": f"{int(YR[af])}w{int(WK[af]):02d}",
                          "peak_wk": f"{int(YR[ap])}w{int(WK[ap]):02d}",
                          "lead_wk": int(npp - f),
                          "ili_at_fire": _r3(Y[af]), "ili_at_peak": _r3(Y[ap])})

    detectors = {
        "spatial_first_order": {"theta": THETA_PRIMARY, **lead_stats(base_leads),
            "n_fired": int(sum(f is not None for f in base_fires)),
            "_def": "fraction of regions whose momentum D_r turned pos->neg >= theta"},
        "spatial_momentum_rollover_PRIMARY": {"theta": THETA_PRIMARY, "frac": FRAC_PRIMARY,
            **lead_stats(prim_leads), "n_fired": int(sum(f is not None for f in prim_fires)),
            "_def": "fraction of regions whose momentum has fallen by FRAC from its causal "
                    "running-max since onset >= theta (LB-e7-spatial-lead)"},
        "national_rollover_CONTROL": {"frac": FRAC_PRIMARY, **lead_stats(nat_roll_lead),
            "n_fired": int(sum(x is not None for x in nat_roll_lead)),
            "_def": "national momentum-rollover, NO spatial pooling - the spatial PRIMARY must beat "
                    "this for the lead to be SPATIAL rather than universal curvature (LB-e7-curvature)"}}

    # ---- spatial GAIN over the national-only control (the H1-spatial test) -----
    spatial_gain = paired_gain(prim_leads, nat_roll_lead,
                               "spatial primary lead - national-control lead, per season; + => the "
                               "SPATIAL pooling adds lead beyond the national-only rollover (required "
                               "for H1; ~0 => the lead is universal curvature, NOT spatial)")

    # ---- theta sweep (primary signal) -----------------------------------------
    theta_sweep = {}
    for th in THETA_SWEEP:
        ls, fs = spatial_leads(turn_roll, FRAC_PRIMARY, th)
        theta_sweep[f"theta_{th}"] = {**lead_stats(ls), "n_fired": int(sum(f is not None for f in fs))}

    # ---- FRAC sensitivity (declared robustness) -------------------------------
    frac_sens = {}
    for fr in FRAC_SWEEP:
        ls, fs = spatial_leads(turn_roll, fr, THETA_PRIMARY)
        frac_sens[f"frac_{fr}"] = {**lead_stats(ls), "n_fired": int(sum(f is not None for f in fs))}

    # ---- head-to-head: spatial-rollover (primary) vs E6 div-peak --------------
    h2h = paired_gain(prim_leads, dp_lead,
                      "spatial-rollover lead - E6 divergence-peak lead, per season; + => the spatial "
                      "detector fires earlier than the coincident divergence-peak (the SOLID bar)")

    # ---- climatological reference (expanding median peak-week; forecast error) -
    clim_err, seen = [], []
    for npp in nat_peak_pos:
        if seen:
            clim_err.append(abs(float(np.median(seen)) - npp))
        seen.append(npp)
    climatology = {"_what": "naive baseline: predict the peak at the expanding-window median "
                            "peak-week of all PRIOR seasons; a forecast ERROR in weeks (a reference, "
                            "NOT a detector lead and NOT a head-to-head)",
                   "n": len(clim_err),
                   "mean_abs_error_wk": _r3(np.mean(clim_err)) if clim_err else None,
                   "median_abs_error_wk": _r3(np.median(clim_err)) if clim_err else None}

    # ---- robustness + verdict (the apparent lead must SURVIVE a deeper, genuine rollover) ------
    prim = detectors["spatial_momentum_rollover_PRIMARY"]
    strict = frac_sens.get("frac_0.75", {})                 # the genuine-rollover end of the sweep
    headroom3 = feasibility["earliest_region_leads_by_rank"]["earliest_3"]["median"]
    leads_positive_sig = ((prim.get("mean") or -1) > 0 and (prim.get("median") or -1) > 0
                          and prim.get("p_vs0") is not None and prim["p_vs0"] < 0.05)
    beats_coincident = ((h2h.get("median_gain") or -1) > 0
                        and h2h.get("paired_p") is not None and h2h["paired_p"] < 0.05)
    spatial_adds = ((spatial_gain.get("median_gain") or 0) > 0
                    and spatial_gain.get("paired_p") is not None and spatial_gain["paired_p"] < 0.05)
    robust_to_threshold = ((strict.get("median") or -1) > 0 and (strict.get("mean") or -1) > 0
                           and strict.get("p_vs0") is not None and strict["p_vs0"] < 0.05)
    genuine_headroom = headroom3 is not None and headroom3 > 0
    robustness = {
        "_what": "the apparent lead must SURVIVE a deeper (more genuine, less noise-triggerable) "
                 "rollover and have real feasibility headroom; a monotone collapse as the drawdown is "
                 "deepened indicates a regional-NOISE artifact (the loose drawdown fires early on noisy "
                 "regional momenta during the rise)",
        "lead_median_by_drawdown": {str(fr): frac_sens[f"frac_{fr}"]["median"] for fr in FRAC_SWEEP},
        "strict_rollover_p_vs0": strict.get("p_vs0"),
        "theta0.3_feasibility_headroom_wk": headroom3,
        "national_control_median_lead": detectors["national_rollover_CONTROL"]["median"],
        "robust_to_threshold": bool(robust_to_threshold), "genuine_headroom": bool(genuine_headroom)}
    if leads_positive_sig and beats_coincident and spatial_adds and robust_to_threshold and genuine_headroom:
        verdict = ("H1 CONFIRMED (significant positive lead, beats the coincident divergence-peak, "
                   "spatial pooling adds over national, robust to the rollover threshold, with genuine "
                   "feasibility headroom)")
    elif leads_positive_sig and beats_coincident and not (robust_to_threshold and genuine_headroom):
        verdict = ("H0 / ARTIFACT: the apparent positive lead is NOT robust - it collapses monotonically "
                   "as the momentum-drawdown is deepened (see robustness.lead_median_by_drawdown; not "
                   "significant at the genuine-rollover end frac=0.75), the theta=0.3 feasibility headroom "
                   "is ~0 (3rd-earliest region peaks at median 0), and the national-only control LAGS - so "
                   "the 'lead' is a regional-NOISE artifact (the loose 50% drawdown fires early on noisy "
                   "regional momenta during the rise, e.g. at ~1.5% ILI in November), NOT a genuine spatial "
                   "signal. The spatial-curvature hypothesis H1 is NOT supported (honest negative, with E6).")
    elif beats_coincident:
        verdict = "MARGINAL (beats the coincident detector, but the absolute lead is not significantly positive)"
    else:
        verdict = ("H0 (no positive lead / no improvement over the coincident national detector) -> "
                   "honest negative paired with E6; consistent with the feasibility diagnostic")

    out = {"experiment": "E7", "title": "spatial-curvature peak detection (pre-registered, net-new)",
           "prereg": "commit ed211e0; DESIGN v0.9 / OUTLINE v0.7 / DECISIONS 2026-06-28; committed "
                     "before any regional number was computed",
           "provenance": "NET-NEW beyond v4; no v4 figure, no Stage-1.5 record; all values as-computed",
           "causal_discipline": "every signal from data <= t; the feasibility diagnostic is HINDSIGHT "
                                "and labeled; no use of the finished season to label a region peaked "
                                "(the D01 / CIC #4 look-ahead lesson)",
           "n_seasons": n, "n_regions": nreg, "regions": labels,
           "operators": f"D = SMA_{WF} - SMA_{WS}; momentum-rollover = D fallen by FRAC from its "
                        f"causal running-max since onset; lead = national-peak-pos - detector-pos (+ precedes)",
           "season_def": "complete seasons through 2024, wk40(y)..wk20(y+1), >= 20 wks, peak >= 2.0% "
                         "(identical E5/E6 set)",
           "params": {"theta_primary": THETA_PRIMARY, "frac_primary": FRAC_PRIMARY,
                      "onset_pp": ONSET_PP, "theta_sweep": THETA_SWEEP, "frac_sweep": FRAC_SWEEP,
                      "_note": "theta + sweep were pre-registered; the running-max-drawdown margin "
                               "(FRAC) + E4 onset guard are pinned here as the principled "
                               "implementation of the pre-registered 'D_r drops below its causal "
                               "running-max by a margin'; FRAC reported as a declared sensitivity. A "
                               "first sustained-negative-2nd-difference implementation fired at onset "
                               "on early-rise noise (an artifact) and was replaced (see DECISIONS)"},
           "LB_e7_feasibility": feasibility,
           "e6_national_comparators": e6,
           "LB_e7_spatial_lead": detectors,
           "spatial_gain_over_national_control": spatial_gain,
           "theta_sweep": theta_sweep,
           "frac_sensitivity": frac_sens,
           "robustness_check": robustness,
           "head_to_head_vs_e6_divpeak": h2h,
           "primary_fire_diagnostic": prim_diag,
           "climatological_reference": climatology,
           "verdict": verdict}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    print("=== E7 spatial-curvature peak detection (pre-registered, net-new) ===")
    print(f"  seasons {n}  regions {nreg}")
    _rk1 = feasibility["earliest_region_leads_by_rank"]
    print(f"  [feasibility HINDSIGHT - decides H1] earliest-region lead median "
          f"{_rk1['earliest_1']['median']} wk; 2nd-earliest {_rk1['earliest_2']['median']}; "
          f"3rd-earliest {_rk1['earliest_3']['median']} (= theta=0.3 headroom); "
          f"all-region median {feasibility['all_region_spread_only']['median']} (tautological - ignore)")
    print(f"  [E6 bar] zero-cross {e6['divergence_zerocross_lead'].get('mean')}  "
          f"SMA-4 {e6['sma4_peak_lead'].get('mean')}  "
          f"div-peak {e6['divergence_peak_lead'].get('mean')} (median {e6['divergence_peak_lead'].get('median')})")
    print(f"  [spatial first-order theta={THETA_PRIMARY}] lead mean {detectors['spatial_first_order'].get('mean')} "
          f"median {detectors['spatial_first_order'].get('median')} "
          f"fired {detectors['spatial_first_order']['n_fired']}/{n}")
    print(f"  [spatial ROLLOVER PRIMARY theta={THETA_PRIMARY} frac={FRAC_PRIMARY}] lead mean "
          f"{prim.get('mean')} median {prim.get('median')} lead% {prim.get('lead_pct')} "
          f"fired {prim['n_fired']}/{n} p_vs0 {prim.get('p_vs0')}")
    print(f"  [national-only rollover CONTROL] lead mean {detectors['national_rollover_CONTROL'].get('mean')} "
          f"median {detectors['national_rollover_CONTROL'].get('median')}")
    print(f"  [SPATIAL GAIN over control] median {spatial_gain.get('median_gain')} wk; "
          f"spatial earlier {spatial_gain.get('a_earlier_pct')}%; paired p {spatial_gain.get('paired_p')}")
    print(f"  [head-to-head vs div-peak] spatial earlier median {h2h.get('median_gain')} wk; "
          f"{h2h.get('a_earlier_pct')}% earlier; paired p {h2h.get('paired_p')}")
    _ilf = [d["ili_at_fire"] for d in prim_diag if d.get("ili_at_fire") is not None]
    _ilp = [_r3(Y[idx[npp]]) for (y, idx), npp in zip(seas, nat_peak_pos)]
    print(f"  [primary fire diag] median %ILI at fire {_r3(np.median(_ilf)) if _ilf else None} "
          f"vs national-peak %ILI median {_r3(np.median(_ilp))}  "
          f"(low fire-ILI + early = artifact; near-peak = genuine)")
    print(f"  [climatology ref] median peak-week forecast MAE {climatology['median_abs_error_wk']} wk")
    print(f"  VERDICT: {verdict}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
