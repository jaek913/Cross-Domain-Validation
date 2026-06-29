#!/usr/bin/env python3
"""theorem8b_symbolic.py - symbolic step-check for the cited Theorem 8b.

Theorem 8b (persistence-sign rule), as applied in E3:
    sign[ Corr(D_t, Y_{t+h}) ]  =  sign[ Rbar(h, h+wf) - Rbar(h+wf, h+ws) ]
with the LEVEL divergence D_t = SMA_wf(Y,t) - SMA_ws(Y,t).

This script does NOT re-derive the theorem (it is cited; empirical-with-verified-
theory archetype). It machine-checks the ONE algebraic step the empirical test
rests on: that, written in ACF terms, the covariance of the divergence with the
future value reduces exactly to a positive multiple of (Rbar_near - Rbar_far),
so the sign rule follows.

Derivation checked:
    SMA_w(t) = (1/w) * sum_{i=0}^{w-1} Y_{t-i}
    Cov(SMA_w(t), Y_{t+h}) / gamma(0) = (1/w) * sum_{i=0}^{w-1} rho(h+i) = Rbar(h, h+w)
    => Corr-term(D_t, Y_{t+h}) ∝ Rbar(h, h+wf) - Rbar(h, h+ws)
       = ((ws-wf)/ws) * ( Rbar(h, h+wf) - Rbar(h+wf, h+ws) )
    Since (ws-wf)/ws > 0 (ws>wf) and gamma(0)>0, the SIGN equals
    sign(Rbar_near - Rbar_far). QED-step.

Pass: sympy.simplify(LHS - RHS) == 0 for every (wf, ws, h) on the grid.
Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations
import sys
import sympy as sp


def rbar(rho, a, b):
    """Mean autocorrelation over integer lags [a, b)."""
    n = b - a
    return sp.Rational(1, n) * sum(rho[lag] for lag in range(a, b))


def check_identity(wf, ws, h, rho):
    # LHS: the ACF-form covariance term of D_t = SMA_wf - SMA_ws with Y_{t+h}
    lhs = (sp.Rational(1, wf) * sum(rho[h + i] for i in range(wf))
           - sp.Rational(1, ws) * sum(rho[h + j] for j in range(ws)))
    # RHS: the positive multiple of (Rbar_near - Rbar_far) the sign rule uses
    near = rbar(rho, h, h + wf)
    far = rbar(rho, h + wf, h + ws)
    rhs = sp.Rational(ws - wf, ws) * (near - far)
    return sp.simplify(lhs - rhs)


def main():
    # (wf, ws, h) grid: the daily windows (12/63) and the flu windows (4/16),
    # plus small generic cases, across several horizons.
    grid = [
        (4, 16, 4), (4, 16, 8), (4, 16, 13), (4, 16, 17), (4, 16, 26),
        (12, 63, 21), (12, 63, 42), (12, 63, 63), (12, 63, 126),
        (2, 5, 1), (3, 7, 2), (5, 20, 10),
    ]
    max_lag = max(h + ws for (wf, ws, h) in grid) + 1
    rho = {lag: sp.Symbol(f"rho_{lag}", real=True) for lag in range(0, max_lag + 1)}

    failures = []
    for (wf, ws, h) in grid:
        resid = check_identity(wf, ws, h, rho)
        ok = (resid == 0)
        print(f"  wf={wf:>2} ws={ws:>2} h={h:>3}  simplify(LHS-RHS) = {resid}  "
              f"[{'OK' if ok else 'FAIL'}]")
        if not ok:
            failures.append((wf, ws, h, resid))

    # Also assert the sign-coefficient (ws-wf)/ws is strictly positive on the grid
    for (wf, ws, h) in grid:
        assert (ws - wf) / ws > 0, f"sign coefficient non-positive for wf={wf}, ws={ws}"

    print()
    if failures:
        print(f"THM-8b SYMBOLIC: FAIL - {len(failures)} identity case(s) did not reduce to 0.")
        sys.exit(1)
    print(f"THM-8b SYMBOLIC: PASS - the covariance reduces to ((ws-wf)/ws)*(Rbar_near-Rbar_far) "
          f"for all {len(grid)} (wf,ws,h) cases; sign rule follows.")
    sys.exit(0)


if __name__ == "__main__":
    main()
