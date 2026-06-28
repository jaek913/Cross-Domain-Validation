#!/usr/bin/env python3
"""
e1_calibration_decomposition.py - Experiment E1 (calibration-scale gap-closure decomposition).

Reproduces (Stage 1.5 / DESIGN S2-E1):
  - weather S_W band + toward (deseasonalized temp anomaly, SMA-50/200, H=63)       [LB-2,3]
  - river S_W raw+deseas + seasonal-variance fraction (CO ~15.5%, OH ~45.7%)        [LB-2,5,6]
  - flu S_W/toward (SMA-4/16, H=13 pinned cell ~153.7% / ~13%)                       [LB-4]
  - S_W ordering weather (low) < deseasonalized rivers (mid) < flu (extreme)        [LB-2]
  - Colorado-Ohio deseas SMA-200 gradient on the matched 1928-2026 period,
    widening across H=42/63/126 as +3.9/+4.7/+6.4 (corrected; printed +6.0/+8.5/+15.2
    reproduces under no cell)                                                        [LB-5, DISC-1.4-01]
  - deseasonalization look-ahead robustness: full-history vs causal expanding monthly
    means change deseas S_W by <=1.2 pp (CO ~0.8, OH ~1.2)                           [DISC-1.4-02]
  - synthetic random-walk control (10 sims matched to Colorado log-returns, seed=0):
    S_W ~99-101%, toward ~48-52% (tolerance band, not an exact match)               [LB-e1-rw-control]

CITED (Paper-4 reference imports, NOT regenerated here): sunspot decomposition S_W/toward and the
financial S_W band - labeled imports in the TBL-1 scale, recorded as such, not computed.

Output: outputs/e1_calibration.json
"""
from __future__ import annotations
import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import operators as op
import data_io as dio

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "e1_calibration.json")
SMAS = (50, 200)
H = 63


def seasonal_fraction(raw, des):
    return 100.0 * (1.0 - np.var(des) / np.var(raw))


def deseason_month_causal(series, months):
    """Causal (no future) per-month mean: expanding mean within each calendar month."""
    s = pd.Series(np.asarray(series, float)).reset_index(drop=True)
    m = pd.Series(np.asarray(months)).reset_index(drop=True)
    causal = s.groupby(m).transform(lambda g: g.expanding().mean())
    return (s - causal).values


def main():
    out = {"experiment": "E1", "title": "calibration-scale gap-closure decomposition",
           "params": {"daily_SMAs": list(SMAS), "daily_H": H, "flu_SMAs": [4, 16], "flu_H": 13,
                      "event_threshold": "expanding 75th pctile, min 50"},
           "weather": {}, "rivers": {}, "flu": {}, "ordering": {}, "gradient": {},
           "lookahead_robustness": {}, "rw_control": {},
           "cited_not_regenerated": {
               "sunspot_decomposition": "Paper-4 reference import (TBL-1); does not reproduce on SILSO v2.0 (toward ~70-80%)",
               "financial_S_W_band": "Paper-4 reference import (~64-167%); not regenerated"}}

    # ---- weather: the Norwich/Dallas calibration pair (DESIGN E1), deseasonalized temp anomaly ----
    WEATHER = {"Norwich_CT": "USC00065910", "Dallas_TX": "USW00003927"}
    weather_sw = []
    for name, sid in WEATHER.items():
        df = dio.load_ghcn_temp(sid)
        des = dio.deseason_doy(df["temp"].values, df["date"].dt.dayofyear.values)
        cells = {}
        for N in SMAS:
            r = op.decompose(des, N, H=H)
            cells[f"SMA-{N}"] = {"N": r["N"], "S_W": round(r["SW"], 2), "toward": round(r["toward"], 1)}
            weather_sw.append(r["SW"])
        out["weather"][name] = {"station": sid, "n": len(df), "cells": cells,
                                "calibration_pair": name in ("Norwich_CT", "Dallas_TX")}
    out["weather"]["_band_S_W_pct"] = [round(min(weather_sw), 1), round(max(weather_sw), 1)]
    out["weather"]["_LB"] = "LB-2/LB-3 (paper band 1.3-7.7%)"

    # ---- rivers: raw + deseasonalized log-discharge ----
    rivers = {}
    river_deseas_sw = {}
    for name, site in dio.USGS.items():
        df = dio.load_usgs(site)
        logq = dio.log_discharge(df)
        des = dio.deseason_month(logq, df["date"].dt.month.values)
        cells = {}
        for lbl, ser in (("raw", logq), ("deseas", des)):
            cells[lbl] = {}
            for N in SMAS:
                r = op.decompose(ser, N, H=H)
                cells[lbl][f"SMA-{N}"] = {"N": r["N"], "S_W": round(r["SW"], 2), "toward": round(r["toward"], 1)}
        rivers[name] = {"gauge": site, "n": len(df),
                        "seasonal_variance_fraction_pct": round(seasonal_fraction(logq, des), 1),
                        "cells": cells}
        river_deseas_sw[name] = des
    out["rivers"] = rivers
    out["rivers"]["_LB"] = "LB-2/LB-5/LB-6 (seasonal fraction CO ~15.5%, OH ~45.7%)"

    # ---- flu: SMA-4/16, H=13 ----
    ili = dio.load_ili()
    Y = ili["w"].values.astype(float)
    flu_cells = {}
    for N in (4, 16):
        r = op.decompose(Y, N, H=13)
        flu_cells[f"SMA-{N}"] = {"N": r["N"], "S_W": round(r["SW"], 1), "toward": round(r["toward"], 1)}
    out["flu"] = {"n_weeks": len(ili), "cells": flu_cells,
                  "_LB": "LB-4 (pinned cell ~153.7% / toward ~13%; v4's 122.6-288.8% range under-specified)"}

    # ---- S_W ordering: weather(low) < deseas rivers(mid) < flu(extreme) ----
    out["ordering"] = {
        "weather_S_W_band": out["weather"]["_band_S_W_pct"],
        "rivers_deseas_S_W": {n: {f"SMA-{N}": rivers[n]["cells"]["deseas"][f"SMA-{N}"]["S_W"] for N in SMAS}
                              for n in dio.USGS},
        "flu_S_W": {k: v["S_W"] for k, v in flu_cells.items()},
        "holds": None}  # filled below

    # ---- Colorado-Ohio deseas SMA-200 gradient (DISC-1.4-01) ----
    co = dio.load_usgs("08158000"); oh = dio.load_usgs("03294500")
    co_logq, oh_logq = dio.log_discharge(co), dio.log_discharge(oh)
    co_des = dio.deseason_month(co_logq, co["date"].dt.month.values)
    oh_des = dio.deseason_month(oh_logq, oh["date"].dt.month.values)
    com = co[co["date"] >= pd.Timestamp("1928-01-01")].reset_index(drop=True)
    com_logq = dio.log_discharge(com)
    com_des = dio.deseason_month(com_logq, com["date"].dt.month.values)
    grad = {"full_history": {}, "matched_1928_2026": {}}
    for H2 in (42, 63, 126):
        co_full = op.decompose(co_des, 200, H=H2)["SW"]
        co_match = op.decompose(com_des, 200, H=H2)["SW"]
        oh_sw = op.decompose(oh_des, 200, H=H2)["SW"]
        grad["full_history"][f"H={H2}"] = round(co_full - oh_sw, 1)
        grad["matched_1928_2026"][f"H={H2}"] = {
            "CO": round(co_match, 1), "OH": round(oh_sw, 1), "gap_pp": round(co_match - oh_sw, 1)}
    out["gradient"] = grad
    out["gradient"]["_LB"] = "LB-5 / DISC-1.4-01 (matched gap +3.9/+4.7/+6.4; CO 17.8/OH 13.1 at H=63)"

    # ---- look-ahead robustness (DISC-1.4-02): full-history vs causal expanding monthly means ----
    lar = {}
    for name, df, logq in (("Colorado", co, co_logq), ("Ohio", oh, oh_logq)):
        months = df["date"].dt.month.values
        des_full = dio.deseason_month(logq, months)
        des_causal = deseason_month_causal(logq, months)
        sw_full = op.decompose(des_full, 200, H=H)["SW"]
        sw_causal = op.decompose(des_causal, 200, H=H)["SW"]
        lar[name] = {"S_W_full_history": round(sw_full, 2), "S_W_causal_expanding": round(sw_causal, 2),
                     "delta_pp": round(abs(sw_full - sw_causal), 2)}
    out["lookahead_robustness"] = lar
    out["lookahead_robustness"]["_LB"] = "DISC-1.4-02 (delta <=1.2pp; CO ~0.8, OH ~1.2)"

    # ---- synthetic random-walk control (10 sims matched to Colorado log-returns, seed=0) ----
    rng = np.random.default_rng(0)
    r = np.diff(co_logq); mu, sig = float(r.mean()), float(r.std(ddof=1))
    T = len(co_logq)
    sims = {f"SMA-{N}": {"S_W": [], "toward": []} for N in SMAS}
    for _ in range(10):
        walk = np.cumsum(rng.normal(mu, sig, T))
        for N in SMAS:
            d = op.decompose(walk, N, H=H)
            sims[f"SMA-{N}"]["S_W"].append(d["SW"]); sims[f"SMA-{N}"]["toward"].append(d["toward"])
    rwc = {"n_sims": 10, "seed": 0, "matched_to": "Colorado daily log-return drift/vol",
           "drift": round(mu, 6), "vol": round(sig, 6)}
    for N in SMAS:
        sw = np.array(sims[f"SMA-{N}"]["S_W"]); tw = np.array(sims[f"SMA-{N}"]["toward"])
        rwc[f"SMA-{N}"] = {"S_W_mean": round(sw.mean(), 1), "S_W_range": [round(sw.min(), 1), round(sw.max(), 1)],
                           "toward_mean": round(tw.mean(), 1), "toward_range": [round(tw.min(), 1), round(tw.max(), 1)]}
    out["rw_control"] = rwc
    out["rw_control"]["_LB"] = "LB-e1-rw-control (band S_W ~99-101%, toward ~48-52%)"

    # ordering check (use SMA-200 cells)
    w_hi = out["weather"]["_band_S_W_pct"][1]
    riv_mid = min(rivers[n]["cells"]["deseas"]["SMA-200"]["S_W"] for n in dio.USGS)
    flu_hi = flu_cells["SMA-4"]["S_W"]
    out["ordering"]["holds"] = bool(w_hi < riv_mid < flu_hi)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    def _ser(o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        return str(o)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=_ser)

    # ---- human-readable summary ----
    print("=== E1 calibration decomposition ===")
    print(f"weather S_W band: {out['weather']['_band_S_W_pct']}%  (paper 1.3-7.7%)")
    for n in dio.USGS:
        c = rivers[n]["cells"]
        print(f"{n}: seasonal-frac {rivers[n]['seasonal_variance_fraction_pct']}%  "
              f"raw SMA-200 S_W {c['raw']['SMA-200']['S_W']}  deseas SMA-200 S_W {c['deseas']['SMA-200']['S_W']}")
    print(f"flu SMA-4/16 H=13 S_W: {flu_cells['SMA-4']['S_W']}/{flu_cells['SMA-16']['S_W']}  toward "
          f"{flu_cells['SMA-4']['toward']}/{flu_cells['SMA-16']['toward']}  (paper ~153.7% / ~13%)")
    print(f"ordering weather<rivers<flu holds: {out['ordering']['holds']}")
    print("CO-OH deseas SMA-200 gradient (matched 1928-2026):",
          {k: v["gap_pp"] for k, v in grad["matched_1928_2026"].items()}, " (paper +3.9/+4.7/+6.4)")
    print("look-ahead delta (pp):", {k: lar[k]["delta_pp"] for k in ("Colorado", "Ohio")}, " (paper CO 0.8/OH 1.2)")
    print(f"RW control SMA-200: S_W mean {rwc['SMA-200']['S_W_mean']} range {rwc['SMA-200']['S_W_range']}, "
          f"toward mean {rwc['SMA-200']['toward_mean']}  (band ~100%/~50%)")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
