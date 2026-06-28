#!/usr/bin/env python3
"""
operators.py - shared analysis primitives for the Cross-Domain-Validation paper.

These are the exact operators verified in the Stage-1.5/1.6 reconstruction (the pre-fix
repo's analysis/repro_*.py corpus): the gap-closure decomposition, the volatility-divergence
building blocks, the subsampled Spearman, the ACF, and the Theorem-8b sign machinery. Every
e1..e6 experiment imports from here so a single definition backs every result.

DESIGN.md S1 is the spec; this file is its implementation. Do not change an operator without a
dated DESIGN/DECISIONS amendment.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


# --------------------------------------------------------------------------- moving averages / vol
def sma(a, N):
    """Simple moving average over the most recent N obs; no look-ahead (min_periods=N)."""
    return pd.Series(np.asarray(a, float)).rolling(N, min_periods=N).mean().values


def tstd(a, w):
    """Trailing sample standard deviation (ddof=1) over the most recent w obs."""
    return pd.Series(np.asarray(a, float)).rolling(w, min_periods=w).std(ddof=1).values


def vdiv(a, wf, ws):
    """Volatility divergence: std(a, wf) - std(a, ws)."""
    return tstd(a, wf) - tstd(a, ws)


def fwd_realized_std(a, H):
    """Realized std of a over the NEXT H obs (forward target), no look-ahead leakage."""
    return pd.Series(np.asarray(a, float)).rolling(H, min_periods=H).std(ddof=1).shift(-H).values


# --------------------------------------------------------------------------- correlation
def corr_sub(a, b, sub=None, min_n=3):
    """Spearman rho between a and b on aligned non-NaN pairs, optionally taking every `sub`-th
    pair. Returns (rho, p, n). Matches the repro corpus (concat+dropna == boolean-mask alignment,
    then ::sub). Returns (nan, nan, n) if fewer than min_n pairs survive."""
    a = pd.Series(np.asarray(a, float)).reset_index(drop=True)
    b = pd.Series(np.asarray(b, float)).reset_index(drop=True)
    al = pd.concat([a, b], axis=1).dropna()
    if sub:
        al = al.iloc[::sub]
    if len(al) < min_n:
        return float("nan"), float("nan"), int(len(al))
    r, p = spearmanr(al.iloc[:, 0], al.iloc[:, 1])
    return float(r), float(p), int(len(al))


# --------------------------------------------------------------------------- ACF / Theorem 8b
def acf_vals(a, maxlag):
    """Sample ACF at integer lags 0..maxlag (pandas Series.autocorr, no taper)."""
    s = pd.Series(np.asarray(a, float))
    return np.array([s.autocorr(lag=k) for k in range(maxlag + 1)])


def first_zero_crossing(ac):
    """First lag k>=1 where the ACF is <= 0 (None if it never crosses within the array)."""
    return next((k for k in range(1, len(ac)) if ac[k] <= 0), None)


def predicted_sign(ac, h, wf, ws):
    """Theorem-8b predicted sign of Corr(D_t, Y_{t+h}) = sign[ Rbar(h, h+wf) - Rbar(h+wf, h+ws) ],
    where Rbar(a,b) is the mean ACF over lags [a, b). Returns (sign, Rnear, Rfar)."""
    Rn = ac[h:h + wf].mean()
    Rf = ac[h + wf:h + ws].mean()
    return np.sign(Rn - Rf), float(Rn), float(Rf)


def observed_8b(a, h, wf, ws, sub):
    """Observed Theorem-8b correlation: Spearman( D(t)=SMA_wf - SMA_ws , Y(t+h) ), subsampled.
    Returns (rho, p, n)."""
    a = np.asarray(a, float)
    D = sma(a, wf) - sma(a, ws)
    T = len(a)
    t = np.arange(T - h)
    return corr_sub(D[t], a[t + h], sub=sub)


# --------------------------------------------------------------------------- gap-closure decomposition
def decompose(series, N, H=63, pct=75, min_history=50):
    """Paper-1 gap-closure decomposition (P5 S2.1 / DESIGN S1).

    x = Y - SMA_N(Y). An EVENT is a t where |x_t| exceeds the expanding `pct`-th percentile of
    |x| (min `min_history` prior valid obs, no look-ahead); events are non-overlapping and spaced
    >= H. Over horizon H, with sgn = sign(x_t):
        C_P = -sgn * (Y_{t+H} - Y_t)        (price/observable closes the gap)
        C_W = +sgn * (SMA_{t+H} - SMA_t)    (filter closes the gap)
    S_W = 100 * sum(C_W) / sum(C_W + C_P).  `toward` = % of events whose first post-event step
    moves toward the filter; z = (toward - 0.5*total)/sqrt(0.25*total).

    Returns dict(N=n_events, SW=%, toward=%, z=).
    """
    a = np.asarray(series, float)
    MA = sma(a, N)
    x = a - MA
    absx = np.abs(x)
    valid = ~np.isnan(x)
    tau = (pd.Series(np.where(valid, absx, np.nan))
           .expanding(min_periods=min_history).quantile(pct / 100.0).values)
    T = len(a)
    last = -H
    CW = CP = 0.0
    n = toward = total = 0
    for t in range(T - H):
        if not valid[t] or np.isnan(tau[t]):
            continue
        if absx[t] > tau[t] and (t - last) >= H:
            dP, dW, sgn = a[t + H] - a[t], MA[t + H] - MA[t], np.sign(x[t])
            cP, cW = -sgn * dP, sgn * dW
            if (cP + cW) != 0:
                CW += cW
                CP += cP
                n += 1
                last = t
                nr = a[t + 1] - a[t]
                if (x[t] > 0 and nr < 0) or (x[t] < 0 and nr > 0):
                    toward += 1
                total += 1
    return dict(N=n,
                SW=100.0 * CW / (CW + CP) if (CW + CP) != 0 else float("nan"),
                toward=100.0 * toward / total if total else float("nan"),
                z=(toward - 0.5 * total) / np.sqrt(0.25 * total) if total else float("nan"))
