#!/usr/bin/env python3
"""theorem8b_stress.py - numeric stress test for the cited Theorem 8b.

Confirms the persistence-sign rule
    sign[ Corr(D_t, Y_{t+h}) ]  =  sign[ Rbar(h, h+wf) - Rbar(h+wf, h+ws) ]
holds in a CONTROLLED setting with KNOWN structure: processes whose theoretical
autocorrelation is available in closed form. For each process the PREDICTED sign
is computed from the theoretical ACF, and the EMPIRICAL sign is the sign of the
finite-sample correlation between the level divergence D_t = SMA_wf - SMA_ws and
the future value Y_{t+h} on a long simulated path. They must agree.

Processes (closed-form ACF):
  - AR(1), rho(k) = phi^k, phi in {0.3, 0.6, 0.9}  (monotone decay -> predicted + at all h)
  - AR(1), phi = -0.4                              (alternating ACF -> produces sign flips)
  - AR(2), phi1=0.5, phi2=-0.6 (complex roots)     (oscillatory ACF -> several sign flips)

The test is deliberately a STRESS, not a tautology: the prediction comes from the
theoretical ACF while the measurement comes from a simulated path, and the grid
includes regimes where the rule must predict a NEGATIVE correlation (>=1 flip
case is required to pass).

Pass: every gated (wf,ws,h) case has matching predicted/empirical sign, with at
least one matched sign-flip case. Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations
import sys
import numpy as np

SEED = 0
N = 300_000
BURN = 2_000
WF, WS = 4, 16
HORIZONS = [1, 2, 3, 4, 5, 6, 8, 10, 13, 16, 21, 26]
FLOOR_PRED = 0.01     # ignore near-zero predicted differences (ambiguous sign)
FLOOR_EMP = 0.003     # ignore correlations too small to sign reliably in-sample


def acf_ar1(phi, max_lag):
    return np.array([phi ** k for k in range(max_lag + 1)], dtype=float)


def acf_ar2(phi1, phi2, max_lag):
    rho = np.zeros(max_lag + 1)
    rho[0] = 1.0
    if max_lag >= 1:
        rho[1] = phi1 / (1.0 - phi2)
    for k in range(2, max_lag + 1):
        rho[k] = phi1 * rho[k - 1] + phi2 * rho[k - 2]
    return rho


def simulate_ar(coeffs, rng, n=N, burn=BURN):
    """coeffs = [phi1, phi2, ...]; returns a length-n stationary path."""
    p = len(coeffs)
    e = rng.standard_normal(n + burn)
    y = np.zeros(n + burn)
    for t in range(p, n + burn):
        y[t] = sum(coeffs[i] * y[t - 1 - i] for i in range(p)) + e[t]
    return y[burn:]


def sma(y, w):
    """SMA_w aligned: out[t] = mean(y[t-w+1 .. t]) for t >= w-1, else nan."""
    c = np.convolve(y, np.ones(w) / w, mode="valid")   # len = len(y)-w+1
    out = np.full(y.shape, np.nan)
    out[w - 1:] = c
    return out


def predicted_diff(rho, wf, ws, h):
    near = rho[h:h + wf].mean()
    far = rho[h + wf:h + ws].mean()
    return near - far, near, far


def empirical_corr(y, wf, ws, h):
    d = sma(y, wf) - sma(y, ws)
    t0 = ws - 1
    t1 = len(y) - h
    dd = d[t0:t1]
    yy = y[t0 + h:t1 + h]
    m = ~np.isnan(dd)
    return float(np.corrcoef(dd[m], yy[m])[0, 1])


def main():
    rng = np.random.default_rng(SEED)
    processes = [
        ("AR1(phi=0.3)", acf_ar1(0.3, max(HORIZONS) + WS), [0.3]),
        ("AR1(phi=0.6)", acf_ar1(0.6, max(HORIZONS) + WS), [0.6]),
        ("AR1(phi=0.9)", acf_ar1(0.9, max(HORIZONS) + WS), [0.9]),
        ("AR1(phi=-0.4)", acf_ar1(-0.4, max(HORIZONS) + WS), [-0.4]),
        ("AR2(0.5,-0.6)", acf_ar2(0.5, -0.6, max(HORIZONS) + WS), [0.5, -0.6]),
    ]

    checked = 0
    flips_checked = 0
    mismatches = []
    print(f"  N={N:,}  wf={WF} ws={WS}  seed={SEED}")
    for name, rho, coeffs in processes:
        y = simulate_ar(coeffs, rng)
        for h in HORIZONS:
            pdiff, near, far = predicted_diff(rho, WF, WS, h)
            psign = int(np.sign(pdiff))
            ecorr = empirical_corr(y, WF, WS, h)
            esign = int(np.sign(ecorr))
            gated = abs(pdiff) > FLOOR_PRED and abs(ecorr) > FLOOR_EMP
            tag = ""
            if gated:
                checked += 1
                if psign == -1:
                    flips_checked += 1
                if psign != esign:
                    mismatches.append((name, h, psign, esign, pdiff, ecorr))
                    tag = "  <-- MISMATCH"
                else:
                    tag = "  ok" + ("  [FLIP]" if psign == -1 else "")
            else:
                tag = "  (skipped: near-zero)"
            print(f"  {name:<15} h={h:>3}  pred_diff={pdiff:+.4f} (near {near:+.3f}/far {far:+.3f}) "
                  f"-> pred {psign:+d} | emp_corr={ecorr:+.4f} -> emp {esign:+d}{tag}")

    print()
    if mismatches:
        print(f"THM-8b STRESS: FAIL - {len(mismatches)} sign mismatch(es) of {checked} gated cases.")
        for m in mismatches:
            print("   mismatch:", m)
        sys.exit(1)
    if flips_checked < 1:
        print("THM-8b STRESS: FAIL - no sign-flip (predicted -1) case was exercised.")
        sys.exit(1)
    print(f"THM-8b STRESS: PASS - {checked} gated cases, sign matches in all; "
          f"{flips_checked} sign-flip case(s) matched. The ACF-derived sign rule "
          f"predicts the empirical D-vs-future correlation sign, including flips.")
    sys.exit(0)


if __name__ == "__main__":
    main()
