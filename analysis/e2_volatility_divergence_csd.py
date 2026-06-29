#!/usr/bin/env python3
"""
e2_volatility_divergence_csd.py - Experiment E2 (volatility-divergence operators + CSD comparison).

The vdiv operator is DOMAIN-SPECIFIC (Stage-1.6 FINDINGS_vdiv_operator.md): the single generic
level/level form reproduces only Ohio. This script computes each domain's reproducible value under
its recovered operator, the block-shuffle null, and the CSD comparator.

Recovered operators (FINDINGS_vdiv_operator.md):
  hydrology     log-RETURNS of discharge   fwd returns-vol   12/63 d   sub-21   (D01: BOTH rivers signal on returns - Ohio +0.30 > Colorado +0.12; the level op is the seasonal-confound null, NOT a per-river property)
  weather       temperature LEVEL          fwd 63-d level-vol 12/63 d  sub-21   day-of-year deseason  [VERIFIED]
  epidemiology  FIRST DIFFERENCES of %ILI  fwd diff-vol      4/16 wk   none
  solar         sunspot LEVEL (yearly)     FUTURE LEVEL Y(t+5) 3/11 yr n/a (Thm-8b form), year<=2008

WEATHER OPERATOR ADJUDICATION (DISC-1.5-02): the verified operator is level/level (above), giving
Dallas ~+0.30 with NO deseasonalization collapse; v4's +0.745->+0.004 is a Paper-4 source-authentic
but under-determined headline. DESIGN.md v0.2's E2 weather row instead specifies a TMAX-first-diff /
21-252 / per-month-z-score operator claimed to reproduce +0.745->+0.004. This script runs BOTH the
verified level operator (A) AND the DESIGN's first-diff operator (B) so the discrepancy is resolved
empirically rather than asserted.

Targets (FINDINGS_vdiv_operator.md reproduction table):
  Ohio vdiv      RETURNS op +0.30 (the signal; D01) ; LEVEL op +0.047/+0.021 (consistent null, exact; block-shuffle z=+1.99<2.0)
  Colorado vdiv  RETURNS op +0.105 overlap / +0.120 sub-21 ; LEVEL op -0.00 (consistent null) ; v4 +0.33 = vdiv vs CONTEMP std(12) (CIC #4 look-ahead, ~+0.32; LB-8/DISC-1.5-01)
  Dallas vdiv    level op +0.301 -> +0.313    (+0.745->+0.004 is under-determined Paper-4 headline; LB-10)
  Norwich vdiv   level op +0.129 -> +0.101    (+0.39->+0.232 under-determined; LB-10)
  ILI vdiv       +0.393 weighted / +0.420 unweighted  (first-diff op; LB-11)
  sunspot vdiv   -0.230 (perm-z -3.94)        (yearly 3/11 future-level; LB-12)
  epi CSD        ~ -0.165 (opposite sign)     (LB-11/13)   ;  solar CSD -0.103 matched future-level (D02: v4 "also negative, lower mag" reproduces; +0.42 was monthly op, -0.257 fwd-vol mismatch)

Output: outputs/e2_divergence_csd.json
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e2_divergence_csd.json")
WF_D, WS_D, SUB = 12, 63, 21       # daily windows + subsample (hydrology, weather A)
WF_E, WS_E = 4, 16                  # weekly windows (epidemiology)
WF_S, WS_S, H_S = 3, 11, 5         # yearly windows + future-level horizon (solar)


def _r3(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)


def load_tmax(station_id):
    """TMAX-only loader (degC) for the DESIGN's first-difference weather operator B."""
    df = pd.read_csv(dio.DATA / f"ghcn_{station_id}.csv", low_memory=False)
    df["date"] = pd.to_datetime(df["DATE"], errors="coerce")
    df["TMAX"] = pd.to_numeric(df.get("TMAX"), errors="coerce")
    df = df.dropna(subset=["date", "TMAX"])
    df = df[df["date"] <= dio.END].sort_values("date").reset_index(drop=True)
    df["tmax"] = df["TMAX"] / 10.0
    return df[["date", "tmax"]]


def deseason_month_z(series, months):
    """Per-calendar-month z-score: (x - month_mean) / month_std."""
    s = pd.Series(np.asarray(series, float)).reset_index(drop=True)
    m = pd.Series(np.asarray(months)).reset_index(drop=True)
    mu = s.groupby(m).transform("mean")
    sd = s.groupby(m).transform("std")
    return ((s - mu) / sd).values


def vdiv_fwd_corr(Y, wf, ws, hfwd, sub):
    """Spearman( std(Y,wf)-std(Y,ws) , forward hfwd-realized-std(Y) ), subsampled."""
    return op.corr_sub(op.vdiv(Y, wf, ws), op.fwd_realized_std(Y, hfwd), sub=sub)


def block_z(Y, wf=WF_D, ws=WS_D, hfwd=WS_D, sub=SUB, block=63, nsh=1000, seed=0):
    """Block-shuffle null z for the level-op vdiv correlation (Ohio LB-9)."""
    rng = np.random.default_rng(seed)
    r0, _, _ = vdiv_fwd_corr(Y, wf, ws, hfwd, sub)
    a = Y[~np.isnan(Y)]
    nb = len(a) // block
    sh = np.empty(nsh)
    for i in range(nsh):
        order = rng.permutation(nb)
        ys = np.concatenate([a[j * block:(j + 1) * block] for j in order])
        sh[i], _, _ = vdiv_fwd_corr(ys, wf, ws, hfwd, sub)
    return r0, float((r0 - sh.mean()) / sh.std())


def csd_corr(Y, ws, hfwd, sub):
    """CSD comparator: Spearman( trailing lag-1 autocorr over rolling ws , forward hfwd-vol )."""
    csd = pd.Series(Y).rolling(ws).corr(pd.Series(Y).shift(1)).values
    return op.corr_sub(csd, op.fwd_realized_std(Y, hfwd), sub=sub)


def main():
    out = {"experiment": "E2", "title": "volatility-divergence operators + CSD comparison",
           "operators": {"hydrology": "log-returns + level, fwd vol, 12/63, sub-21 (D01: returns=signal both rivers OH>CO; level=consistent null; v4 +0.33 = contemp std(12) self-corr, CIC #4)",
                         "weather_A_verified": "temperature level, fwd 63d level-vol, 12/63, sub-21, day-of-year deseason",
                         "weather_B_design": "TMAX first-diff, fwd 21d vol, 21/252, sub-21, per-month z-score deseason",
                         "epidemiology": "first-diff %ILI, fwd diff-vol, 4/16, none",
                         "solar": "yearly level, future level Y(t+5), 3/11, year<=2008"},
           "hydrology": {}, "weather": {}, "epidemiology": {}, "solar": {},
           "block_shuffle_null": {}, "csd": {}}

    # ---------------- hydrology: returns op + level op, Colorado/Ohio ----------------
    for name, site in (("Colorado", "08158000"), ("Ohio", "03294500")):
        d = dio.load_usgs(site)
        lq = dio.log_discharge(d)
        mon = d["date"].dt.month.values
        r = pd.Series(lq).diff().values
        rds = pd.Series(dio.deseason_month(lq, mon)).diff().values
        lds = dio.deseason_month(lq, mon)
        ret_ov, _, n_ov = op.corr_sub(op.vdiv(r, WF_D, WS_D), op.fwd_realized_std(r, WS_D))
        ret_sb, _, n_sb = vdiv_fwd_corr(r, WF_D, WS_D, WS_D, SUB)
        ret_sb_d, _, _ = vdiv_fwd_corr(rds, WF_D, WS_D, WS_D, SUB)
        lvl_sb, _, _ = vdiv_fwd_corr(lq, WF_D, WS_D, WS_D, SUB)
        lvl_sb_d, _, _ = vdiv_fwd_corr(lds, WF_D, WS_D, WS_D, SUB)
        # D01 diagnostic: the documented LEVEL+forward operator gives ~0 with OR without subsampling - overlap is NOT the cause
        lvl_ov, _, n_lov = op.corr_sub(op.vdiv(lq, WF_D, WS_D), op.fwd_realized_std(lq, WS_D))
        lvl_ov_d, _, _ = op.corr_sub(op.vdiv(lds, WF_D, WS_D), op.fwd_realized_std(lds, WS_D))
        # D01 CIC #4 (look-ahead): v4's +0.33 reproduced - vdiv correlated with the CONTEMPORANEOUS fast std(12), its own
        # fast-vol component, with NO forward shift. Colorado ~+0.32 (= v4 +0.33); Ohio ~+0.62, so had v4 applied this
        # target to Ohio it would read +0.62 not +0.047 - the two rivers were computed with different targets.
        art, _, _ = op.corr_sub(op.vdiv(lq, WF_D, WS_D), op.tstd(lq, WF_D))
        art_d, _, _ = op.corr_sub(op.vdiv(lds, WF_D, WS_D), op.tstd(lds, WF_D))
        out["hydrology"][name] = {
            "n": len(d),
            "returns_op": {"overlap": _r3(ret_ov), "sub21_raw": _r3(ret_sb), "sub21_deseas": _r3(ret_sb_d),
                           "n_overlap": n_ov, "n_sub": n_sb},
            "level_op": {"overlap": _r3(lvl_ov), "overlap_deseas": _r3(lvl_ov_d),
                         "sub21_raw": _r3(lvl_sb), "sub21_deseas": _r3(lvl_sb_d), "n_overlap": n_lov},
            "v4_artifact_contemp_fast": {"raw": _r3(art), "deseas": _r3(art_d),
                                         "note": "vdiv vs contemporaneous std(12) = predictor's own fast term; CIC #4 look-ahead; raw = v4's +0.33"}}
    out["hydrology"]["_targets"] = ("D01: returns op = signal (Ohio +0.30 > Colorado +0.12, both rivers); "
                                    "level op (consistent, forward) = null both rivers (Colorado -0.00, Ohio +0.047); "
                                    "v4's +0.33 = Colorado vdiv vs CONTEMPORANEOUS std(12) (CIC #4 look-ahead, ~+0.32); "
                                    "Ohio's +0.047 used the forward target - the two rivers used different targets")

    # ---------------- weather: operator A (verified) + operator B (DESIGN), Dallas/Norwich + all-6 range (A) ----------------
    A_all = []
    for name, sid in dio.GHCN.items():
        df = dio.load_ghcn_temp(sid)
        Y = df["temp"].values
        doy = df["date"].dt.dayofyear.values
        rawA, _, nA = vdiv_fwd_corr(Y, WF_D, WS_D, WS_D, SUB)
        Yds = dio.deseason_doy(Y, doy)
        desA, _, _ = vdiv_fwd_corr(Yds, WF_D, WS_D, WS_D, SUB)
        A_all.append(rawA)
        entry = {"station": sid, "n": len(df),
                 "operator_A_level": {"raw": _r3(rawA), "deseas": _r3(desA)}}
        if name in ("Dallas_TX", "Norwich_CT"):
            # operator B: TMAX first-diff, 21/252, fwd 21-d vol, per-month z-score deseason
            tdf = load_tmax(sid)
            T = tdf["tmax"].values
            tmon = tdf["date"].dt.month.values
            dT = pd.Series(T).diff().values
            rawB, _, nB = vdiv_fwd_corr(dT, 21, 252, 21, SUB)
            dT_z = deseason_month_z(pd.Series(T).diff().values, tmon)        # z-score the first-differences by month
            desB, _, _ = vdiv_fwd_corr(dT_z, 21, 252, 21, SUB)
            # also: z-score the level then difference (alt deseason ordering)
            Tz = deseason_month_z(T, tmon)
            dTz2 = pd.Series(Tz).diff().values
            desB2, _, _ = vdiv_fwd_corr(dTz2, 21, 252, 21, SUB)
            entry["operator_B_design"] = {"raw": _r3(rawB), "deseas_zdiff": _r3(desB),
                                          "deseas_diffz": _r3(desB2), "n_sub": nB,
                                          "v4_headline": "+0.745 -> +0.004" if name == "Dallas_TX" else "+0.39 -> +0.232"}
        out["weather"][name] = entry
    out["weather"]["_A_all6_raw_range"] = [_r3(min(A_all)), _r3(max(A_all))]
    out["weather"]["_targets"] = ("operator A: Dallas +0.301->+0.313, Norwich +0.129->+0.101 (verified, NO collapse); "
                                  "operator B resolves whether first-diff/21-252/per-month-z reproduces the +0.745->+0.004 collapse")

    # ---------------- epidemiology: first-diff op (headline) ----------------
    ili = dio.load_ili()
    epi = {}
    for col in ("% WEIGHTED ILI", "%UNWEIGHTED ILI"):
        dL = pd.to_numeric(ili[col], errors="coerce").diff().values
        r, _, n = vdiv_fwd_corr(dL, WF_E, WS_E, WS_E, None)
        epi[col] = {"rho": _r3(r), "n": n}
    out["epidemiology"] = {"first_diff_op": epi, "_target": "+0.393 weighted / +0.420 unweighted (LB-11)"}

    # ---------------- solar: yearly 3/11 future-level Y(t+5), year<=2008 ----------------
    sn = dio.load_silso_yearly()
    full = sn[sn["year"] <= 2008].reset_index(drop=True)
    Ys = full["sn"].values.astype(float)
    vd_s = op.vdiv(Ys, WF_S, WS_S)
    fut = pd.Series(Ys).shift(-H_S).values
    rho_s, _, n_s = op.corr_sub(vd_s, fut)
    rng = np.random.default_rng(0)
    null = []
    for _ in range(2000):
        p = rng.permutation(Ys)
        v = op.vdiv(p, WF_S, WS_S); f = pd.Series(p).shift(-H_S).values
        rr, _, _ = op.corr_sub(v, f); null.append(rr)
    null = np.array(null, float)
    perm_z = float((rho_s - np.nanmean(null)) / np.nanstd(null))
    out["solar"] = {"years": f"{int(full.year.min())}-{int(full.year.max())}", "n": n_s,
                    "vdiv_rho": _r3(rho_s), "perm_z": round(perm_z, 2),
                    "_target": "-0.230 (perm-z -3.94), the unique negative-sign domain (LB-12)"}

    # ---------------- block-shuffle null: Ohio deseasonalized, level op ----------------
    oh = dio.load_usgs("03294500")
    oh_des = dio.deseason_month(dio.log_discharge(oh), oh["date"].dt.month.values)
    r0, z = block_z(oh_des)
    out["block_shuffle_null"] = {"Ohio_deseas": {"rho": _r3(r0), "z": round(z, 2),
                                 "_target": "rho +0.021, z +1.7 < 2.0 -> null holds (LB-9)"}}

    # ---------------- CSD comparator: epidemiology (opposite sign) + solar ----------------
    Yili = ili["w"].values.astype(float)
    epi_csd, _, _ = csd_corr(Yili, WS_E, 13, 8)
    # D02: the solar CSD must use the vdiv's target (future-level Y(t+5)), NOT forward-vol, for an
    # apples-to-apples comparison. Matched AR1(ws=11) vs Y(t+5) = -0.103 (negative, |rho| < vdiv's
    # 0.230 -> v4's "CSD also negative, lower magnitude" REPRODUCES). fut/Ys are in scope from solar.
    sol_ar1 = pd.Series(Ys).rolling(WS_S).corr(pd.Series(Ys).shift(1)).values
    sol_csd, _, _ = op.corr_sub(sol_ar1, fut)
    sol_csd_vol, _, _ = csd_corr(Ys, WS_S, WS_S, None)   # forward-vol target (mismatched) - diagnostic only
    out["csd"] = {"epidemiology": {"csd_rho": _r3(epi_csd), "_target": "~ -0.165 (opposite sign to vdiv; LB-11/13)"},
                  "solar": {"csd_rho": _r3(sol_csd), "csd_rho_fwdvol_diagnostic": _r3(sol_csd_vol),
                            "_note": "D02: matched to the vdiv's future-level target = -0.103 (negative, lower magnitude than vdiv -0.230) -> v4's 'CSD also negative' REPRODUCES; the forward-vol value (-0.257) is a target mismatch, NOT the comparison"}}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    # ---------------- human-readable summary ----------------
    print("=== E2 volatility-divergence operators + CSD ===")
    print("HYDROLOGY (D01: returns=signal both rivers OH>CO ; level=consistent null ; v4 +0.33 = contemp-fast self-corr, CIC #4):")
    for n in ("Colorado", "Ohio"):
        h = out["hydrology"][n]
        print(f"  {n:9s} returns sub21 {h['returns_op']['sub21_raw']} (ov {h['returns_op']['overlap']})  |  "
              f"level sub21 {h['level_op']['sub21_raw']} (ov {h['level_op']['overlap']})  |  "
              f"v4-artifact(contemp std12) {h['v4_artifact_contemp_fast']['raw']}")
    print("  targets: returns OH +0.30 > CO +0.12 ; level OH +0.047 CO -0.00 ; v4 CO +0.33 = contemp std12 (CIC #4); OH +0.047 = forward")
    print("WEATHER:")
    for n in ("Dallas_TX", "Norwich_CT"):
        w = out["weather"][n]
        print(f"  {n:11s} A(level) raw {w['operator_A_level']['raw']} deseas {w['operator_A_level']['deseas']}  "
              f"|  B(design) raw {w['operator_B_design']['raw']} deseas(zdiff) {w['operator_B_design']['deseas_zdiff']} "
              f"deseas(diffz) {w['operator_B_design']['deseas_diffz']}  [v4 {w['operator_B_design']['v4_headline']}]")
    print(f"  A all-6 raw range {out['weather']['_A_all6_raw_range']}")
    print(f"  >>> WEATHER RESOLUTION: operator A verified ~+0.30 (no collapse); does operator B reproduce +0.745->+0.004?")
    print("EPIDEMIOLOGY (first-diff op):", {k: v["rho"] for k, v in epi.items()}, " target +0.393/+0.420")
    print(f"SOLAR yearly 3/11 future-level: rho {out['solar']['vdiv_rho']} perm-z {out['solar']['perm_z']}  target -0.230 / -3.94")
    print(f"OHIO block-shuffle null: rho {r0:+.3f} z {z:+.2f}  target +0.021 / +1.7")
    print(f"CSD epi {out['csd']['epidemiology']['csd_rho']} (target ~-0.165) ; solar {out['csd']['solar']['csd_rho']} matched-future-level (D02: v4 'also negative, lower mag' REPRODUCES vs vdiv -0.230 ; fwd-vol diagnostic {out['csd']['solar']['csd_rho_fwdvol_diagnostic']})")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
