#!/usr/bin/env python3
"""
data_io.py - hashed-data loaders for the Cross-Domain-Validation paper.

Reads ONLY the identity-verified copies pull.py staged into the project-local store
(LT_CDV_DATA; default below). Loaders mirror the Stage-1.5/1.6 reconstruction exactly:
USGS RDB (log-discharge), NOAA GHCN by-station (temp = (TMAX+TMIN)/2, truncated to the
2026-03-18 anchor), CDC ILINet (first 1,484 National weeks), CDC NREVSS (pre/post combined
strain counts), SILSO yearly. Plus the two deseasonalization helpers.

Run `python data_io.py` for a smoke test (loads everything, prints counts vs anchors).
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd

DATA   = Path(os.environ.get("LT_CDV_DATA", r"C:\Users\jaek9\Documents\LaggingTruth\Cross-Domain-Validation"))
END    = pd.Timestamp("2026-03-18")     # USGS / NOAA coverage-end reproduction anchor
N_WEEKS = 1484                          # ILINet extent (1997w40 -> 2026w09)

USGS  = {"Colorado": "08158000", "Ohio": "03294500"}
GHCN  = {"NYC_CentralPark": "USW00094728", "BlueHill_MA": "USC00190736",
         "SanFrancisco": "USW00023272", "Philadelphia": "USW00013739",
         "Dallas_TX": "USW00003927", "Norwich_CT": "USC00065910"}


# --------------------------------------------------------------------------- USGS rivers
def load_usgs(site):
    """USGS daily-values RDB -> DataFrame[date, q] (q>0, <= anchor, sorted)."""
    rows = []
    with open(DATA / f"usgs_{site}.rdb") as f:
        for line in f:
            if line.startswith("#"):
                continue
            rows.append(line.rstrip("\n").split("\t"))
    header, data = rows[0], rows[2:]
    disc = [c for c in header if c.endswith("_00060_00003") and not c.endswith("_cd")][0]
    df = pd.DataFrame(data, columns=header)
    df["date"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["q"] = pd.to_numeric(df[disc], errors="coerce")
    df = df.dropna(subset=["date", "q"])
    df = df[(df["q"] > 0) & (df["date"] <= END)]
    return df.sort_values("date").reset_index(drop=True)[["date", "q"]]


def log_discharge(df):
    return np.log(df["q"].to_numpy())


# --------------------------------------------------------------------------- NOAA weather
def load_ghcn_temp(station_id):
    """NOAA GHCN-Daily by-station CSV -> DataFrame[date, temp] (both TMAX&TMIN, <= anchor)."""
    df = pd.read_csv(DATA / f"ghcn_{station_id}.csv", low_memory=False)
    df["date"] = pd.to_datetime(df["DATE"], errors="coerce")
    for c in ("TMAX", "TMIN"):
        df[c] = pd.to_numeric(df.get(c), errors="coerce")
    df = df.dropna(subset=["date", "TMAX", "TMIN"])
    df = df[df["date"] <= END].sort_values("date").reset_index(drop=True)
    df["temp"] = (df["TMAX"] + df["TMIN"]) / 20.0      # GHCN tenths-degC -> degC
    return df[["date", "temp"]]


# --------------------------------------------------------------------------- CDC influenza
def load_ili():
    """CDC ILINet -> first 1,484 National weeks; column 'w' = % WEIGHTED ILI (+ YEAR, WEEK)."""
    df = pd.read_csv(DATA / "ILINet.csv", skiprows=1)
    df = df[df["REGION TYPE"] == "National"].reset_index(drop=True).iloc[:N_WEEKS].copy()
    df["w"] = pd.to_numeric(df["% WEIGHTED ILI"], errors="coerce")
    return df


def _num(s):
    return pd.to_numeric(s, errors="coerce").fillna(0)


def load_strain_combined(ili):
    """CDC NREVSS pre+post combined on (year,week), post-2015 precedence, merged onto ILI weeks.
    Returns the ILI frame with TOT, H1N1, H3N2, Btot, Aunsub (A-subtyping-not-performed) columns;
    the pinned-spec proportional allocation of Aunsub into H1N1/H3N2 is applied in E5."""
    pre = pd.read_csv(DATA / "ICL_NREVSS_Combined_prior_to_2015_16.csv", skiprows=1)
    pre = pre[pre["REGION TYPE"] == "National"].copy()
    pre["H1N1"] = _num(pre["A (2009 H1N1)"]) + _num(pre["A (H1)"])
    pre["H3N2"] = _num(pre["A (H3)"]); pre["Btot"] = _num(pre["B"]); pre["TOT"] = _num(pre["TOTAL SPECIMENS"])
    pre["Aunsub"] = _num(pre.get("A (Subtyping not Performed)", 0))
    post = pd.read_csv(DATA / "ICL_NREVSS_Public_Health_Labs.csv", skiprows=1)
    post = post[post["REGION TYPE"] == "National"].copy()
    post["H1N1"] = _num(post["A (2009 H1N1)"]); post["H3N2"] = _num(post["A (H3)"])
    post["Btot"] = _num(post["B"]) + _num(post.get("BVic", 0)) + _num(post.get("BYam", 0))
    post["TOT"] = _num(post["TOTAL SPECIMENS"])
    post["Aunsub"] = _num(post.get("A (Subtyping not Performed)", 0))
    pre["k"] = pre.YEAR * 100 + pre.WEEK; post["k"] = post.YEAR * 100 + post.WEEK
    comb = pd.concat([pre[pre.k < 201540], post[post.k >= 201540]], ignore_index=True)
    comb = comb[["k", "TOT", "H1N1", "H3N2", "Btot", "Aunsub"]].sort_values("k")
    ili = ili.copy(); ili["k"] = ili.YEAR * 100 + ili.WEEK
    m = ili.merge(comb, on="k", how="left")
    for c in ["TOT", "H1N1", "H3N2", "Btot", "Aunsub"]:
        m[c] = m[c].fillna(0)
    return m


HHS_REGIONS = [f"Region {i}" for i in range(1, 11)]


def load_ili_regional(ili):
    """CDC ILINet HHS-region % WEIGHTED ILI, aligned 1:1 to the national week index.

    Reads ILINet_HHS.csv (REGION TYPE='HHS Regions'; the confirmed pull has all 10 regions
    x 1,484 weeks 1997w40..2026w09, fully numeric, aligned), restricts each region to the
    national weeks (k = YEAR*100 + WEEK from `ili`, the load_ili frame -- this also drops any
    weeks a fresh download carries past 2026w09), and returns a dict:
        weeks  : national k-array (length N == len(ili))
        labels : ['Region 1' .. 'Region 10'] in numeric order
        W      : float ndarray (len(labels), N); W[r, j] = region r's % WEIGHTED ILI on
                 national week j (np.nan if a region lacks that week -- none in the pull)
    """
    df = pd.read_csv(DATA / "ILINet_HHS.csv", skiprows=1)
    df = df[df["REGION TYPE"] == "HHS Regions"].copy()
    df["k"] = df["YEAR"] * 100 + df["WEEK"]
    df["w"] = pd.to_numeric(df["% WEIGHTED ILI"], errors="coerce")
    ili = ili.copy(); ili["k"] = ili["YEAR"] * 100 + ili["WEEK"]
    weeks = ili["k"].to_numpy()
    piv = df.pivot_table(index="k", columns="REGION", values="w", aggfunc="first").reindex(weeks)
    labels = [r for r in HHS_REGIONS if r in piv.columns]
    if len(labels) != len(piv.columns):       # fall back to numeric-sorted whatever is present
        labels = sorted(piv.columns,
                        key=lambda s: int("".join(ch for ch in str(s) if ch.isdigit()) or 9999))
    W = piv[labels].to_numpy(dtype=float).T
    return {"weeks": weeks, "labels": labels, "W": W}


# --------------------------------------------------------------------------- SILSO solar
def load_silso_yearly():
    """SILSO yearly mean total SN v2.0 -> DataFrame[year, sn] (year floored; the E2 solar
    operator applies the year<=2008 filter)."""
    raw = pd.read_csv(DATA / "silso_yearly.csv", sep=";", header=None, usecols=[0, 1],
                      names=["year", "sn"])
    raw["year"] = np.floor(pd.to_numeric(raw["year"], errors="coerce"))
    raw["sn"] = pd.to_numeric(raw["sn"], errors="coerce")
    return raw.dropna().reset_index(drop=True)


# --------------------------------------------------------------------------- deseasonalization
def deseason_month(series, months):
    """Subtract the per-calendar-month mean (rivers: month of the date)."""
    s = pd.Series(np.asarray(series, float)).reset_index(drop=True)
    m = pd.Series(np.asarray(months)).reset_index(drop=True)
    return (s - s.groupby(m).transform("mean")).values


def deseason_doy(series, doy):
    """Subtract the day-of-year mean over the full history (weather)."""
    s = pd.Series(np.asarray(series, float)).reset_index(drop=True)
    d = pd.Series(np.asarray(doy)).reset_index(drop=True)
    return (s - s.groupby(d).transform("mean")).values


# --------------------------------------------------------------------------- smoke test
def _smoke():
    print(f"LT_CDV_DATA = {DATA}\n")
    for name, site in USGS.items():
        d = load_usgs(site)
        print(f"USGS {name:9s} ({site}): n={len(d):,}  {d.date.min().date()}..{d.date.max().date()}")
    for name, sid in GHCN.items():
        d = load_ghcn_temp(sid)
        print(f"GHCN {name:16s} ({sid}): n={len(d):,}  {d.date.min().date()}..{d.date.max().date()}")
    ili = load_ili()
    print(f"ILINet: weeks={len(ili)}  {int(ili.YEAR.iloc[0])}w{int(ili.WEEK.iloc[0])}"
          f"..{int(ili.YEAR.iloc[-1])}w{int(ili.WEEK.iloc[-1])}")
    m = load_strain_combined(ili)
    print(f"strain-merged: rows={len(m)}  weeks-with-specimens={(m.TOT>0).sum()}")
    reg = load_ili_regional(ili)
    print(f"ILINet HHS: regions={len(reg['labels'])} {reg['labels']}  W shape={reg['W'].shape}  "
          f"NaN={int(np.isnan(reg['W']).sum())}")
    sn = load_silso_yearly()
    print(f"SILSO yearly: years={len(sn)}  {int(sn.year.min())}..{int(sn.year.max())}"
          f"  (<=2008: {(sn.year<=2008).sum()})")
    print("\nsmoke test OK")


if __name__ == "__main__":
    _smoke()
