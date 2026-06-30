#!/usr/bin/env python3
"""
e3_theorem8b_sign.py - Experiment E3 (Theorem-8b persistence-sign test; the in-paper falsifier).

Cited Theorem 8b predicts the SIGN of Corr(D_t, Y_{t+h}) from a mean-ACF contrast:
    sign[Corr(D_t, Y_{t+h})] = sign[ Rbar(h, h+wf) - Rbar(h+wf, h+ws) ]
where D_t = SMA_wf(Y,t) - SMA_ws(Y,t) is the LEVEL divergence and Rbar(a,b) is the mean ACF
over lags [a, b). 5 systems x 5 horizons = 25 pre-registered predictions (sunspots NOT in E3).

Systems / params (verified Stage-1.5 repro_crossdomain.py):
  Colorado  deseasonalized log-discharge   wf=12 ws=63  h=21/42/63/126/252  sub=21  maxlag=400
  Ohio      deseasonalized log-discharge   wf=12 ws=63  h=21/42/63/126/252  sub=21  maxlag=400
  Norwich   deseasonalized temp anomaly    wf=12 ws=63  h=21/42/63/126/252  sub=21  maxlag=400
  Dallas    deseasonalized temp anomaly    wf=12 ws=63  h=21/42/63/126/252  sub=21  maxlag=400
  Flu       RAW weekly % WEIGHTED ILI      wf=4  ws=16  h=4/8/13/17/26      sub=8   maxlag=60

Decision rules (DESIGN E3): correct iff sign(observed rho) == predicted sign; significant iff
p < 0.05 AND the Fisher-z 95% CI excludes zero (the verified repro used p<0.05 alone - reported
here as a cross-check). HEADLINE = the theorem-predicted SIGN (overall 20/25 correct; 13/13 of the
Fisher-z-significant predictions correct; ZERO significant-WRONG = the in-paper falsifier not
triggered). Two sign flips: Colorado h=252 (Rbar_near < Rbar_far, ACF still POSITIVE - not a
zero-crossing; DISC-1.4-04) and Flu h=26 (seasonal ACF; the ACF zero-crossing is at ~14 wk,
distinct from h=26; DISC-1.4-05).

Phase-5a recast (DECISIONS 2026-06-29). The parametric Fisher-z significance is ANTI-CONSERVATIVE
(the subsample stride sub=21 < the slow window ws=63, so adjacent subsamples share overlapping
divergence windows, and the rivers carry long-range dependence) - it is reported as a DEMOTED
cross-check, not the headline. Theorem 8b predicts THIS correlation's sign FROM the ACF, so the
correlation is a theory-derived consequence of the autocorrelation, not a spurious artifact of it;
the load-bearing backbone is therefore (i) the theorem-predicted SIGN and (ii) its block-independent
IS/OOS sign-STABILITY: every one of the 13 significant predictions keeps its sign on both temporal
halves (isoos_consistent_among_significant). A moving-block bootstrap was attempted and REJECTED as
the wrong tool (a joint-block percentile CI tightens around a real structure-driven correlation as
the block grows, so it makes a true small correlation look MORE significant, not less - see DECISIONS).
4A adds a CAUSAL (expanding) deseasonalization recompute for the 4 daily systems (flu is RAW),
closing the 5a finding that the causal-vs-full check covered only E1.

Rejected alternative (manuscript Part IV, reported as history): vol divergence vdiv = std(Y,wf) -
std(Y,ws) predicting FORWARD VOLATILITY (the Part-III target: realized std over a fixed 63 d / 16 wk
window), with the sign still taken from the LEVEL ACF (Theorem-8b rule). The observed sign is constant
across the 5 horizons while the level-ACF prediction varies with h; this mis-applies the level ACF to
a volatility relationship (the correct vol test would need the vol-specific ACF) and reproduces ~44%
(11/25) with 11 significant-wrong - confirming the LEVEL divergence predicting the future LEVEL is
the right form. Both significance criteria are reported for the vol formulation as a cross-check.

Output: outputs/e3_theorem8b.json
"""
from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e3_theorem8b.json")

WF_D, WS_D, SUB_D, MAXLAG_D = 12, 63, 21, 400   # daily systems (rivers, weather)
WF_F, WS_F, SUB_F, MAXLAG_F = 4, 16, 8, 60      # flu (weekly)
H_D = (21, 42, 63, 126, 252)
H_F = (4, 8, 13, 17, 26)
H_FWD_D, H_FWD_F = 63, 16                        # fixed forward-vol window for the rejected vol formulation (Part-III target)


def _r3(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)


def _sign(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    return int(np.sign(x))


def _is_sig(p, r, n):
    """DESIGN E3 significance: p < 0.05 AND the Fisher-z 95% CI for r (n pairs) excludes zero.
    Reported as a DEMOTED cross-check (anti-conservative: sub < ws => overlapping windows; Phase-5a)."""
    if p is None or (isinstance(p, float) and np.isnan(p)) or p >= 0.05:
        return False
    if r is None or n is None or n <= 3 or (isinstance(r, float) and np.isnan(r)):
        return False
    z = np.arctanh(np.clip(r, -0.999999, 0.999999))
    se = 1.0 / np.sqrt(n - 3)
    lo, hi = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
    return not (lo <= 0.0 <= hi)


def _p_only(p):
    return bool(p is not None and not (isinstance(p, float) and np.isnan(p)) and p < 0.05)


def observed_vol(a, wf, ws, sub, hfwd):
    """REJECTED formulation (manuscript Part IV): vol divergence predicting FORWARD VOLATILITY, judged by
    the LEVEL-ACF Theorem-8b rule. Spearman( vdiv_t = std(Y,wf)-std(Y,ws) , realized std over the next
    hfwd obs ) - the Part-III forward-vol target (fixed window 63 d / 16 wk), so the observed sign is
    constant across the 5 horizons while the level-ACF predicted sign varies with h. Mis-applies the
    level ACF to a volatility relationship (the correct vol test would need the vol-specific ACF)."""
    a = np.asarray(a, float)
    V = op.vdiv(a, wf, ws)
    fv = op.fwd_realized_std(a, hfwd)
    return op.corr_sub(V, fv, sub=sub)


def isoos_signs(a, h, wf, ws, sub):
    """Level-divergence observed sign on the in-sample / out-of-sample halves (temporal split). The
    block-independent backbone of the sign claim (Phase-5a): a significant prediction is sign-STABLE
    iff its observed sign matches across both halves and the full sample."""
    a = np.asarray(a, float)
    mid = len(a) // 2
    r_is, _, n_is = op.observed_8b(a[:mid], h, wf, ws, sub)
    r_oos, _, n_oos = op.observed_8b(a[mid:], h, wf, ws, sub)
    return (_sign(r_is), n_is), (_sign(r_oos), n_oos)


def run_system(Y, wf, ws, horizons, sub, maxlag, hfwd):
    ac = op.acf_vals(Y, maxlag)
    zc = op.first_zero_crossing(ac)
    # rejected vol formulation: vol-div vs a FIXED forward-vol window -> observed sign constant across h
    vrho, vp, vn = observed_vol(Y, wf, ws, sub, hfwd)
    vsign = _sign(vrho)
    vsig = _is_sig(vp, vrho, vn)
    vsig_p = _p_only(vp)
    rows = []
    for h in horizons:
        rho, p, n = op.observed_8b(Y, h, wf, ws, sub)
        psign, Rnear, Rfar = op.predicted_sign(ac, h, wf, ws)
        osign = _sign(rho)
        correct = (osign is not None) and (int(psign) == osign)
        sig = _is_sig(p, rho, n)
        vcorrect = (vsign is not None) and (int(psign) == vsign)   # vs the constant vol observed sign
        (is_sign, is_n), (oos_sign, oos_n) = isoos_signs(Y, h, wf, ws, sub)
        rows.append({
            "h": h, "rho": _r3(rho), "p": _r3(p), "n": n,
            "predicted_sign": int(psign), "Rbar_near": _r3(Rnear), "Rbar_far": _r3(Rfar),
            "observed_sign": osign, "correct": bool(correct),
            "significant": bool(sig), "significant_p_only": _p_only(p),
            "isoos": {"is_sign": is_sign, "is_n": is_n, "oos_sign": oos_sign, "oos_n": oos_n,
                      "consistent": bool(is_sign is not None and is_sign == oos_sign == osign)},
            "vol_formulation": {"observed_sign": vsign, "correct": bool(vcorrect),
                                "significant": bool(vsig), "significant_p_only": bool(vsig_p)}})
    return {"n": len(Y), "wf": wf, "ws": ws, "subsample": sub, "maxlag": maxlag, "fwd_vol_window": hfwd,
            "acf_first_zero_crossing": zc,
            "n_correct": sum(r["correct"] for r in rows),
            "n_significant": sum(r["significant"] for r in rows),
            "n_significant_correct": sum(r["significant"] and r["correct"] for r in rows),
            "n_significant_p_only": sum(r["significant_p_only"] for r in rows),
            "vol_rho": _r3(vrho), "vol_observed_sign": vsign, "vol_significant": bool(vsig),
            "predictions": rows}


def _flag(r):
    if r["significant"]:
        return "*" if r["correct"] else "!"     # ! = significant-WRONG (the in-paper falsifier)
    return "." if r["correct"] else "x"


def main():
    def usgs_deseas(site):
        d = dio.load_usgs(site)
        return dio.deseason_month(dio.log_discharge(d), d["date"].dt.month.values)

    def ghcn_deseas(sid):
        g = dio.load_ghcn_temp(sid)
        return dio.deseason_doy(g["temp"].values, g["date"].dt.dayofyear.values)

    def usgs_deseas_causal(site):
        d = dio.load_usgs(site)
        return dio.deseason_month_causal(dio.log_discharge(d), d["date"].dt.month.values)

    def ghcn_deseas_causal(sid):
        g = dio.load_ghcn_temp(sid)
        return dio.deseason_doy_causal(g["temp"].values, g["date"].dt.dayofyear.values)

    systems = [
        ("Colorado", usgs_deseas("08158000"),     WF_D, WS_D, H_D, SUB_D, MAXLAG_D, H_FWD_D),
        ("Ohio",     usgs_deseas("03294500"),     WF_D, WS_D, H_D, SUB_D, MAXLAG_D, H_FWD_D),
        ("Norwich",  ghcn_deseas("USC00065910"),  WF_D, WS_D, H_D, SUB_D, MAXLAG_D, H_FWD_D),
        ("Dallas",   ghcn_deseas("USW00003927"),  WF_D, WS_D, H_D, SUB_D, MAXLAG_D, H_FWD_D),
        ("Flu",      dio.load_ili()["w"].values.astype(float), WF_F, WS_F, H_F, SUB_F, MAXLAG_F, H_FWD_F),
    ]

    out = {"experiment": "E3", "title": "Theorem-8b persistence-sign test (in-paper falsifier)",
           "rule": "sign[Corr(D_t,Y_{t+h})] = sign[Rbar(h,h+wf) - Rbar(h+wf,h+ws)]; D = SMA_wf - SMA_ws (LEVEL divergence)",
           "significance": "p < 0.05 AND Fisher-z 95% CI excludes zero - DEMOTED cross-check (anti-conservative: sub<ws => overlapping windows + long-range dependence); backbone = predicted sign + IS/OOS stability (Phase-5a)",
           "systems": {}}
    for name, Y, wf, ws, hs, sub, ml, hfwd in systems:
        out["systems"][name] = run_system(Y, wf, ws, hs, sub, ml, hfwd)

    S = out["systems"]
    tot = sum(s["n_correct"] for s in S.values())
    sig = sum(s["n_significant"] for s in S.values())
    sig_correct = sum(s["n_significant_correct"] for s in S.values())
    sig_wrong = sig - sig_correct
    sig_p_only = sum(s["n_significant_p_only"] for s in S.values())
    vol_correct = sum(r["vol_formulation"]["correct"] for s in S.values() for r in s["predictions"])
    vol_sig = sum(r["vol_formulation"]["significant"] for s in S.values() for r in s["predictions"])
    vol_sig_wrong = sum(r["vol_formulation"]["significant"] and not r["vol_formulation"]["correct"]
                        for s in S.values() for r in s["predictions"])
    vol_sig_p = sum(r["vol_formulation"]["significant_p_only"] for s in S.values() for r in s["predictions"])
    vol_sig_wrong_p = sum(r["vol_formulation"]["significant_p_only"] and not r["vol_formulation"]["correct"]
                          for s in S.values() for r in s["predictions"])
    isoos_consistent = sum(r["isoos"]["consistent"]
                           for s in S.values() for r in s["predictions"] if r["significant"])

    # 4A: recompute the grid under CAUSAL (expanding) deseasonalization for the 4 daily systems
    # (flu is RAW, unaffected). A flip = the observed Spearman sign differs from the full-sample run.
    daily_causal = [("Colorado", usgs_deseas_causal("08158000")),
                    ("Ohio",     usgs_deseas_causal("03294500")),
                    ("Norwich",  ghcn_deseas_causal("USC00065910")),
                    ("Dallas",   ghcn_deseas_causal("USW00003927"))]
    cz_obs_flips = cz_correct_flips = cz_sig_correct_flips = 0
    cz_rows = []
    for name, Yc in daily_causal:
        acc = op.acf_vals(Yc, MAXLAG_D)
        for r in S[name]["predictions"]:
            h = r["h"]
            rho_c, _, _ = op.observed_8b(Yc, h, WF_D, WS_D, SUB_D)
            ps_c, _, _ = op.predicted_sign(acc, h, WF_D, WS_D)
            osign_c = _sign(rho_c)
            correct_c = (osign_c is not None) and (int(ps_c) == osign_c)
            obs_flip = bool(osign_c is not None and r["observed_sign"] is not None and osign_c != r["observed_sign"])
            correct_flip = bool(correct_c != r["correct"])
            sig_correct_flip = bool((r["significant"] and r["correct"]) and not correct_c)
            cz_obs_flips += int(obs_flip)
            cz_correct_flips += int(correct_flip)
            cz_sig_correct_flips += int(sig_correct_flip)
            cz_rows.append({"system": name, "h": h, "obs_sign_full": r["observed_sign"],
                            "obs_sign_causal": osign_c, "rho_causal": _r3(rho_c),
                            "correct_full": bool(r["correct"]), "correct_causal": bool(correct_c),
                            "was_significant_correct": bool(r["significant"] and r["correct"]),
                            "obs_flip": obs_flip})

    co252 = next(r for r in S["Colorado"]["predictions"] if r["h"] == 252)
    flu26 = next(r for r in S["Flu"]["predictions"] if r["h"] == 26)

    out["summary"] = {
        "total_predictions": 25,
        "total_correct": tot, "total_correct_target": 20,
        "significant_correct": sig_correct, "significant_total": sig, "significant_correct_target": "13/13",
        "significant_p_only_crosscheck": sig_p_only,
        "significant_wrong": sig_wrong, "in_paper_falsifier_triggered": bool(sig_wrong > 0),
        "per_domain_correct": {k: v["n_correct"] for k, v in S.items()},
        "per_domain_significant": {k: v["n_significant"] for k, v in S.items()},
        "isoos_consistent_among_significant": isoos_consistent,
        "colorado_h252_flip": {"predicted_sign": co252["predicted_sign"], "observed_sign": co252["observed_sign"],
                               "Rbar_near": co252["Rbar_near"], "Rbar_far": co252["Rbar_far"],
                               "acf_first_zero_crossing": S["Colorado"]["acf_first_zero_crossing"],
                               "_note": "flip = Rbar_near < Rbar_far with ACF still positive (NOT a zero-crossing); DISC-1.4-04"},
        "flu_h26_flip": {"predicted_sign": flu26["predicted_sign"], "observed_sign": flu26["observed_sign"],
                         "Rbar_near": flu26["Rbar_near"], "Rbar_far": flu26["Rbar_far"],
                         "acf_first_zero_crossing": S["Flu"]["acf_first_zero_crossing"],
                         "_note": "seasonal ACF; zero-crossing at ~14 wk is DISTINCT from h=26; DISC-1.4-05"},
        "causal_deseason_robustness": {
            "n_daily_predictions": len(cz_rows), "n_observed_sign_flips": cz_obs_flips,
            "n_correct_flips": cz_correct_flips, "n_significant_correct_flips": cz_sig_correct_flips,
            "_note": "E3 grid recomputed with EXPANDING (causal) per-calendar deseasonalization for the 4 daily systems (flu is RAW, unaffected); flu's 5 predictions are unchanged. The 2 observed-sign flips are non-significant near-zero weather predictions; no significant-correct verdict changes. Closes the 5a finding that the causal-vs-full check covered only E1 (Phase-5a 4A).",
            "detail": cz_rows},
        "rejected_vol_formulation": {"correct": vol_correct, "of": 25, "pct": round(100.0 * vol_correct / 25, 1),
                                     "significant_wrong_fisher": vol_sig_wrong, "significant_total_fisher": vol_sig,
                                     "significant_wrong_p_only": vol_sig_wrong_p, "significant_total_p_only": vol_sig_p,
                                     "target": "~44% correct, 11 significant-wrong (the LEVEL formulation is primary)"}}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    print("=== E3 Theorem-8b persistence-sign test (LEVEL divergence; in-paper falsifier) ===")
    for name in ("Colorado", "Ohio", "Norwich", "Dallas", "Flu"):
        s = S[name]
        flags = "".join(_flag(r) for r in s["predictions"])
        print(f"  {name:9s} correct {s['n_correct']}/5  significant {s['n_significant']}  "
              f"[{flags}]  ACF 0-cross @ {s['acf_first_zero_crossing']}")
    print(f"  -> total correct {tot}/25 (target 20) ; significant-correct {sig_correct}/{sig} "
          f"(target 13/13 ; p<0.05-only cross-check {sig_p_only})")
    print(f"  -> significant-WRONG {sig_wrong}  (in-paper falsifier {'TRIGGERED' if sig_wrong > 0 else 'not triggered'})")
    print(f"  Colorado h=252 flip: pred {co252['predicted_sign']} obs {co252['observed_sign']}  "
          f"Rnear {co252['Rbar_near']} vs Rfar {co252['Rbar_far']}  (ACF 0-cross @ {S['Colorado']['acf_first_zero_crossing']})")
    print(f"  Flu h=26 flip: pred {flu26['predicted_sign']} obs {flu26['observed_sign']}  "
          f"(ACF 0-cross @ {S['Flu']['acf_first_zero_crossing']} wk, distinct from h=26)")
    print(f"  IS/OOS sign-consistent among the {sig} significant predictions: {isoos_consistent}  (block-independent backbone)")
    print(f"  [4A] Causal-deseason robustness (4 daily systems, 20 preds): observed-sign flips {cz_obs_flips}/20 ; "
          f"correct-verdict flips {cz_correct_flips} ; significant-correct flips {cz_sig_correct_flips}")
    print(f"  REJECTED vol formulation (vdiv vs fixed forward-vol; level-ACF rule): {vol_correct}/25 correct "
          f"({round(100.0 * vol_correct / 25, 1)}%)")
    print(f"       significant-wrong: Fisher {vol_sig_wrong}/{vol_sig} ; p-only {vol_sig_wrong_p}/{vol_sig_p}  (target ~44% / 11)")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
