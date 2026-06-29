# Theorem 8b — Three-Way Verification Record

**Paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
**Standard:** v1.8 · **Phase:** 4 (Write) — proof check part 3 of 3
**Theorem:** the persistence-sign rule (Theorem 8b), cited from the Lagging Truth framework paper (Kim-2026d), reproduced for self-containedness in the manuscript Appendix B.

The framework's one load-bearing theorem is checked **three independent ways**, and all three agree. The written proof is the primary deliverable; the two machine checks supplement it (they do not replace it).

## Statement

For a weakly-stationary series `{Y_t}` with ACF `ρ`, window lengths `w_f < w_s`, level divergence `D_t = SMA_{w_f}(Y,t) − SMA_{w_s}(Y,t)`, and mean ACF `R̄(a,b) = (1/(b−a)) Σ_{lag=a}^{b−1} ρ(lag)`, for any forward horizon `h ≥ 1`:

`sign[ Corr(D_t, Y_{t+h}) ] = sign[ R̄(h, h+w_f) − R̄(h+w_f, h+w_s) ]`.

Writing `R̄_near = R̄(h, h+w_f)` and `R̄_far = R̄(h+w_f, h+w_s)`, the sign of the divergence-to-future correlation equals `sign(R̄_near − R̄_far)`.

## Check 1 — Written proof (PASS)

**Location:** manuscript Appendix B. **Method:** direct computation. `Cov(SMA_w, Y_{t+h}) = σ² R̄(h, h+w)`; applying this to both windows and splitting the slow-window mean ACF at `h + w_f` gives `Cov(D_t, Y_{t+h}) = σ² · ((w_s − w_f)/w_s) · (R̄_near − R̄_far)`. Since `σ² > 0` and `(w_s − w_f)/w_s > 0`, and the correlation is the covariance over a positive product of standard deviations, the sign of the correlation equals `sign(R̄_near − R̄_far)`. **Result: the identity holds; the sign rule follows.**

## Check 2 — Symbolic step-check (PASS)

**Script:** `analysis/checks/theorem8b_symbolic.py` (sympy). **Method:** symbolically reduce `Cov(SMA_{w_f} − SMA_{w_s}, Y_{t+h})` in ACF terms to `((w_s − w_f)/w_s)(R̄_near − R̄_far)` and assert `simplify(LHS − RHS) == 0` over a grid of `(w_f, w_s, h)` values spanning the paper's daily and weekly window/horizon choices (12/63 with h up to 126; 4/16 with h up to 26) plus additional grids. **Result: all 12 grid cases reduce to 0** — the covariance reduces to the claimed closed form, so the sign rule follows. Ledger row: `THM-8b-symbolic` (check = script, clean-exit-required).

## Check 3 — Numeric stress test (PASS)

**Script:** `analysis/checks/theorem8b_stress.py` (numpy). **Method:** for autoregressive processes with closed-form ACFs — AR(1) with φ ∈ {0.3, 0.6, 0.9} (monotone decay), AR(1) with φ = −0.4, and AR(2) with (φ₁, φ₂) = (0.5, −0.6) (oscillatory) — compute the predicted sign from the theoretical ACF (via `R̄_near − R̄_far`) and the empirical sign of `corr(D_t, Y_{t+h})` on long simulations (N = 300,000, seed 0), with windows `w_f = 4`, `w_s = 16` over a horizon grid. Gate the comparison where the predicted difference and the empirical correlation are both non-negligible, and require at least one sign flip among the oscillatory cases. **Result: 29 gated cases match in sign, including 5 deliberate sign-flip cases** (the AR(1) φ = −0.4 and AR(2) cases flip exactly where `R̄_near < R̄_far`). The ACF-derived sign predicts the finite-sample empirical sign, flips included. Ledger row: `THM-8b-stress` (check = script, clean-exit-required).

## Summary

| Check | Artifact | Result |
|---|---|---|
| Written proof | manuscript Appendix B | PASS — identity + sign rule derived |
| Symbolic step-check | `analysis/checks/theorem8b_symbolic.py` | PASS — 12/12 grid cases simplify to 0 |
| Numeric stress test | `analysis/checks/theorem8b_stress.py` | PASS — 29 gated cases match, 5 flips matched |

All three checks are registered and run by `analysis/verify.py` (the two scripts via the theorem-check stage; the written proof is present in the committed manuscript). The theorem is verified written + symbolic + numeric, and the three agree.

---

*Three-way verification record, Standard v1.8, Phase 4. The persistence-sign rule is prior art (cited); this record documents that the paper's reliance on it is independently substantiated.*
