# OUTLINE.md — Paper Roadmap

The paper's skeleton: the ordered argument, every citation, the load-bearing findings (by LB-id, never valued), the figures/tables/equations, the assumptions/scope, and the conclusions. The manuscript is **written from** this and mechanically **reconciled against** it at Phases 4–5. No values live here.

## Metadata

- **Paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
- **Archetype:** empirical-with-verified-theory
- **Source pin (rebuild):** `lagging-truth-paper-05\paper\Paper5_...v4.md`, SHA256 `982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50` (MD5 `23428fb275f6ea6d6a3846fc17d91a86`)
- **Standard:** v1.8
- **Outline version:** v0.1 — 2026-06-28
- **Status:** draft

## Changelog

- v0.1 2026-06-28 — initial roadmap built from the pinned v4 + COVERAGE.md (commit ddb9849). LB-ids provisional (claims.lock is built at Phase 3); all finding nodes TRANSFORM pending Phase-2 regeneration. The 4 v4 orphan citations resolved (author decision 2026-06-28): cite all four — Boettiger-Hastings 2012 + Boettiger-Ross-Hastings 2013 → §3.1; Li 2025 → §3.1/§4.1; Hsiang 2016 → §1.2; none removed.

## 1. IMRaD structural map (the skeleton)

Ordered section list; every node below lands in one of these. (This paper uses a Parts structure rather than a single Related-Literature section — prior art is distributed across §1.2, §3.1, §4.1, §5.1.1 and tracked in §3 below; the reconciliation gate enforces each citation's presence wherever it sits.)

Abstract → Part I Introduction (1.1 What This Paper Tests · 1.2 Why Natural Sciences · 1.3 Organization) → Part II Calibration Scale / Decomposition (2.1 Methodology · 2.2 Weather · 2.3 Rivers [2.3.1–2.3.5] · 2.4 Sunspots · 2.5 Influenza · 2.6 Complete Scale) → Part III Divergence Operator + CSD (3.1 · 3.2 Methodology · 3.3 Results by Domain [3.3.1–3.3.4] · 3.4 Summary · 3.5 Bias Audit) → Part IV Persistence-Sign / Theorem 8b (4.1 · 4.2 · 4.3 · 4.4 Results · 4.5 Post-Test · 4.6 Correction Note) → Part V Applications (5.1 Flu Onset [5.1.0–5.1.6] · 5.2 Weather-to-River) → Part VI Synthesis (6.1 Table · 6.2 ACF Diagram · 6.3 Conclusions · 6.4 Bias Audit) → Part VII Forward Predictions (7.1 · 7.2 · 7.3 · 7.4) → Acknowledgments & AI Disclosure → References → Appendix A (A.1–A.4).

## 2. Argument chain (the spine)

| ID | Claim (one line) | § | Depends on | Support (LB-id / cite key) | Status |
|---|---|---|---|---|---|
| ARG-01 | The framework (decomposition + vol-divergence + Theorem-8b ACF-sign rule + CSD-superset) was derived from first principles and validated only on financial data | 1.1 | — | Kim-2026a, Kim-2026b, Kim-2026c, Kim-2026d | RETAINED |
| ARG-02 | Testing it on systems where the physics is independently known validates by external calibration | 1.2 | ARG-01 | Kaya-2025 | RETAINED |
| ARG-03 | Each domain's known restoring-force structure predicts specific framework behavior (weather strong, rivers storage-dependent, sunspots oscillatory, flu none) | 1.2 | ARG-02 | Hurst-1951, Koutsoyiannis-2002 | RETAINED |
| ARG-04 | The decomposition orders systems by restoring-force strength (weather low S_W → deseasonalized rivers intermediate → flu extreme; financial between rivers and flu) | 2.2–2.6 | ARG-03 | LB-e1-weather-sw, LB-e1-colorado-sw, LB-e1-ohio-sw, LB-e1-sunspot-sw, LB-e1-flu-sw, LB-e1-rw-control | TRANSFORM |
| ARG-05 | Deseasonalization separates genuine non-seasonal persistence (Colorado) from seasonal artifact (Ohio collapse), corroborating Paper-4's Ohio finding by an independent method | 2.3.4 | ARG-04 | LB-e1-deseas-gradient, Kim-2026d, Koutsoyiannis-2005, O'Connell-2016 | TRANSFORM |
| ARG-06 | The vol-divergence operator produces significant IS/OOS-stable signals where ACF structure exists, and a null where basin-averaging removes it (Ohio deseasonalized) | 3.3 | ARG-03 | LB-e2-colorado-rho, LB-e2-ohio-rho, LB-e2-flu-rho, LB-e2-weather-rho, LB-e2-sunspot-rho | TRANSFORM |
| ARG-07 | Vol-divergence outperforms single-window CSD in each domain; CSD is opposite-signed in epidemiology | 3.3–3.4 | ARG-06 | LB-e2-csd-compare, Scheffer-2009, Dakos-2008, Corsi-2009 | TRANSFORM |
| ARG-08 | Theorem-8b's ACF-sign prediction holds 100% on statistically significant predictions, including two sign flips at ACF zero-crossings | 4.4–4.5 | ARG-03 | LB-e3-significant, LB-e3-overall, LB-e3-colorado-flip, LB-e3-flu-flip, Lo-MacKinlay-1988, Hong-Satchell-2015 | TRANSFORM |
| ARG-09 | The ACF is the unifying variable governing the divergence operator's sign, magnitude, deseasonalization response, and failure modes across all domains | 6.2–6.3 | ARG-04, ARG-06, ARG-07, ARG-08 | FIG-1, Hurst-1951, Mandelbrot-Wallis-1968 | TRANSFORM |
| ARG-10 | A divergence-based flu-onset detector fires ~8 weeks earlier than level-based surveillance across nearly all seasons | 5.1.2 | ARG-06 | LB-e4-lead, LB-e4-seasons, LB-e4-floor, Shaman-Karspeck-2012, Steiner-2010, Vega-2013 | TRANSFORM |
| ARG-11 | Strain-level divergence identifies the dominant circulating strain (hindsight, real-time, and clearly-single-strain seasons) | 5.1.3 | ARG-10 | LB-e5-hindsight, LB-e5-realtime, LB-e5-single, Goldstein-2011, Kandula-2017 | TRANSFORM |
| ARG-12 | The divergence zero-crossing does NOT improve peak detection — a rejected hypothesis, reported honestly | 5.1.2 | ARG-10 | LB-e6-zerocross, LB-e6-divpeak | TRANSFORM |
| ARG-13 | The natural-science validation corroborates the financial findings by external calibration rather than internal consistency | 6.3 | ARG-04, ARG-05, ARG-06, ARG-07, ARG-08, ARG-09 | Kaya-2025 | TRANSFORM |
| ARG-14 | Two dated 2026–27 flu forward predictions convert the retrospective validation into a falsifiable out-of-sample test | 7 | ARG-10, ARG-11 | (registered prediction; resolves post-publication) | RETAINED |

## 3. Citations

One row per reference; `Key` is what the reconciliation gate greps for. Accuracy is the Phase-5b all-tier check's job; this table guarantees PRESENCE + ROLE. (v4 had 4 references present in its list but uncited in its body — prior P5 audit. **Author decision 2026-06-28: cite all four** in the rebuild, at the locations shown below; none removed.)

| Key (Surname-YEAR) | Role | Supports (ARG / §) | Status |
|---|---|---|---|
| Kim-2026a | foundation (self-cite, framework origin) | ARG-01 / 1.1 | RETAINED |
| Kim-2026b | foundation (self-cite) | ARG-01 / 1.1 | RETAINED |
| Kim-2026c | foundation (self-cite) | ARG-01 / 1.1 | RETAINED |
| Kim-2026d | foundation (self-cite; Theorem-8b source + financial reference values) | ARG-01, ARG-05, ARG-08 / 1.1, 2.3.4, 4.1 | RETAINED |
| Hurst-1951 | foundation (cross-domain universality) | ARG-03, ARG-09 / 1.2, 6.3 | RETAINED |
| Mandelbrot-Wallis-1968 | foundation (universality / fractional Gaussian) | ARG-09 / 1.2, 6.3 | RETAINED |
| Kaya-2025 | prior-art (nearest precedent: financial indicators → natural science) | ARG-02, ARG-13 / 1.2, 6.3 | RETAINED |
| Lo-MacKinlay-1988 | prior-art (ACF-sign / variance ratio, finance) | ARG-08 / 4.1 | RETAINED |
| Hong-Satchell-2015 | prior-art (ACF-sign / momentum amplification, finance) | ARG-08 / 4.1 | RETAINED |
| Ferreira-2019 | prior-art (MA trading rule autocovariance, finance) | ARG-08 / 4.1 | RETAINED |
| Moskowitz-2012 | prior-art (time-series momentum autocovariance, finance) | ARG-08 / 4.1 | RETAINED |
| Zakamulin-Giner-2020 | prior-art (MA-indicator correlation under AR(p), finance) | ARG-08 / 4.1 | RETAINED |
| Corsi-2009 | prior-art (multi-scale realized volatility / HAR) | ARG-06, ARG-07 / 3.1 | RETAINED |
| Scheffer-2009 | prior-art (CSD / early-warning foundation) | ARG-07 / 3.1 | RETAINED |
| Dakos-2008 | prior-art (CSD for abrupt climate change) | ARG-07 / 3.1 | RETAINED |
| Dakos-2012a | prior-art (CSD indicator suite) | ARG-07 / 3.1 | RETAINED |
| Dakos-2012b | prior-art (CSD robustness) | ARG-07 / 3.1 | RETAINED |
| Dablander-2022 | prior-art (overlapping-timescale EWS, COVID) | ARG-07 / 3.1 | RETAINED |
| Koutsoyiannis-2002 | prior-art (hydrological persistence / fGn) | ARG-03, ARG-05 / 1.2, 2.3.4 | RETAINED |
| Koutsoyiannis-2005 | prior-art (hydrologic persistence) | ARG-05 / 2.3.4 | RETAINED |
| Koutsoyiannis-2006 | prior-art (nonstationarity vs scaling) | ARG-05 / 2.3.4 | RETAINED |
| O'Connell-2016 | prior-art (Hurst legacy, hydrology) | ARG-05 / 2.3.4 | RETAINED |
| Shaman-Karspeck-2012 | contrast (mechanistic flu forecasting, >7wk peak) | ARG-10 / 5.1.1 | RETAINED |
| Shaman-2013 | contrast (real-time flu forecasts) | ARG-10 / 5.1.1 | RETAINED |
| Pei-2018 | contrast (spatial flu transmission forecast) | ARG-10 / 5.1.1 | RETAINED |
| Vega-2013 | contrast (Moving Epidemic Method, WHO/ECDC) | ARG-10 / 5.1.1 | RETAINED |
| Steiner-2010 | method-precedent (EWMA control charts, closest precedent) | ARG-10 / 5.1.1 | RETAINED |
| Goldstein-2011 | method-precedent (strain-specific incidence) | ARG-11 / 5.1.3 | RETAINED |
| Kandula-2017 | method-precedent (subtype-specific forecast) | ARG-11 / 5.1.3 | RETAINED |
| Gatti-2026 | contrast (pre-season subtype forecasting) | ARG-11 / 5.1.4 | RETAINED |
| Boettiger-Hastings-2012 | prior-art (CSD detection limits) | ARG-07 / 3.1 (uncited in v4; cited in rebuild) | RETAINED |
| Boettiger-Ross-Hastings-2013 | prior-art (EWS charted/uncharted) | ARG-07 / 3.1 (uncited in v4; cited in rebuild) | RETAINED |
| Hsiang-2016 | prior-art (climate econometrics) | 1.2 (uncited in v4; cited in rebuild) | RETAINED |
| Li-2025 | prior-art (operator analysis of MACD) | 3.1 / 4.1 (uncited in v4; cited in rebuild) | RETAINED |

Roles: prior-art · motivating-anomaly · method-precedent · corroboration · contrast · foundation (self-cite).

## 4. Load-bearing findings

Keyed to the ledger (claims.lock, Phase 3); **no values here.** All TRANSFORM pending Phase-2 regeneration.

| LB-id (provisional) | Finding (one line, no value) | Supports (ARG) | Status |
|---|---|---|---|
| LB-e1-weather-sw | Weather temperature-anomaly filter-share (benchmark low end of the scale) | ARG-04 | TRANSFORM |
| LB-e1-colorado-sw | Colorado River filter-share, raw and deseasonalized | ARG-04, ARG-05 | TRANSFORM |
| LB-e1-ohio-sw | Ohio River filter-share, raw and deseasonalized (collapse on deseasonalization) | ARG-04, ARG-05 | TRANSFORM |
| LB-e1-sunspot-sw | Sunspot filter-share (cyclical reversion + short-term momentum) | ARG-04 | TRANSFORM |
| LB-e1-flu-sw | Influenza filter-share (extreme mechanical adaptation end of the scale) | ARG-04 | TRANSFORM |
| LB-e1-rw-control | Synthetic random-walk control filter-share + toward rate (methodology check) | ARG-04 | TRANSFORM |
| LB-e1-deseas-gradient | Deseasonalized Colorado-vs-Ohio gap and its widening with horizon | ARG-05 | TRANSFORM |
| LB-e2-colorado-rho | Colorado vol-divergence ↔ forward-volatility rank correlation (raw ≈ deseasonalized) | ARG-06 | TRANSFORM |
| LB-e2-ohio-rho | Ohio vol-divergence correlation (raw borderline; deseasonalized null + block-shuffle z) | ARG-06 | TRANSFORM |
| LB-e2-flu-rho | Influenza vol-divergence correlation | ARG-06 | TRANSFORM |
| LB-e2-weather-rho | Weather vol-divergence correlation (Norwich, Dallas) | ARG-06 | TRANSFORM |
| LB-e2-sunspot-rho | Sunspot vol-divergence correlation | ARG-06 | TRANSFORM |
| LB-e2-csd-compare | Vol-divergence-vs-CSD comparison per domain (vdiv outperforms; opposite sign in epidemiology) | ARG-07 | TRANSFORM |
| LB-e3-significant | Significant-correct count for the Theorem-8b sign prediction | ARG-08 | TRANSFORM |
| LB-e3-overall | Overall-correct count across the 25 pre-registered predictions | ARG-08 | TRANSFORM |
| LB-e3-colorado-flip | Colorado long-horizon sign flip (predicted + observed) | ARG-08, ARG-09 | TRANSFORM |
| LB-e3-flu-flip | Influenza long-horizon sign flip at the seasonal ACF zero-crossing | ARG-08, ARG-09 | TRANSFORM |
| LB-e4-lead | Divergence-vs-level onset lead, and divergence-vs-peak lead | ARG-10 | TRANSFORM |
| LB-e4-seasons | Fraction of seasons the divergence fires earlier than the level method | ARG-10 | TRANSFORM |
| LB-e4-floor | Minimum (worst-case) lead-time floor across seasons | ARG-10 | TRANSFORM |
| LB-e5-hindsight | Dominant-strain identification accuracy (full-season hindsight benchmark) | ARG-11 | TRANSFORM |
| LB-e5-realtime | Dominant-strain accuracy at the real-time moment of detection | ARG-11 | TRANSFORM |
| LB-e5-single | Accuracy in clearly single-strain-dominated seasons | ARG-11 | TRANSFORM |
| LB-e6-zerocross | Divergence zero-crossing peak-lag (rejected hypothesis) | ARG-12 | TRANSFORM |
| LB-e6-divpeak | Divergence-peak lead over the true ILI peak | ARG-12 | TRANSFORM |

## 5. Figures, tables & equations

Gate checks each is PRESENT at its anchor AND REFERENCED in the text. Each carries a COVERAGE disposition.

| ID | What it shows (one line) | § | Referenced by (ARG / §) | Status |
|---|---|---|---|---|
| FIG-1 | ACF unification diagram — deseasonalized ACF for Colorado, Ohio, Dallas, flu on a common lag axis | 6.2 | ARG-09 / 6.2 | TRANSFORM (regenerated) |
| TBL-1 | Unified cross-domain table (S_W, toward, divergence ρ, Theorem-8b, seasonality, ACF half-life/zero-cross per system) | 6.1 | ARG-09, ARG-13 / 6.1 | TRANSFORM (regenerated) |
| EQ-1 | Gap-closure decomposition (filter-share = filter gap-closure / total gap-closure) | 2.1 | ARG-04 / 2.1 | TRANSFORM (anchor added) |
| EQ-2 | Volatility-divergence operator (fast trailing std − slow trailing std) | 3.2 | ARG-06 / 3.2 | TRANSFORM (anchor added) |
| EQ-3 | Level-divergence operator (fast SMA − slow SMA) | 4.1 | ARG-08 / 4.1 | TRANSFORM (anchor added) |
| EQ-4 | Theorem-8b sign rule (sign of divergence↔future correlation = sign of near-minus-far mean-ACF difference) + mean-ACF definition | 4.1 | ARG-08 / 4.1 | TRANSFORM (anchor added) |
| EQ-5 | Flu-onset divergence (4-week SMA − 12-week SMA of ILI) | 5.1 | ARG-10 / 5.1.2 | TRANSFORM (anchor added) |

## 6. Assumptions & scope conditions

Each carries a greppable `S-` anchor in the manuscript.

| ID | Statement | Where stated (anchor) | Status |
|---|---|---|---|
| S1 | The observable's autocorrelation structure is approximately stationary over the sample (the operator's behavior is read from a stationary ACF) | 3.2 / 4.1 | RETAINED |
| S2 | Deseasonalization (monthly or day-of-year mean subtraction) adequately removes the seasonal cycle while preserving stochastic departures | 2.3.2 / 4.2 | RETAINED |
| S3 | The divergence operator requires sufficient autocorrelation structure; it returns a null where basin-scale averaging or deseasonalization removes that structure | 3.3 / 6.3 | RETAINED |
| S4 | The forward-prediction test requires a genuine flu season (peak ILI at or above the activity floor); a low-activity season is untestable, not falsifying | 7.1 | RETAINED |

## 7. Conclusions & limits-of-claim

Each carries a greppable `C-`/`L-` anchor so it cannot vanish.

| ID | Conclusion or limit-of-claim | Where (anchor) | Status |
|---|---|---|---|
| C-01 | The ACF governs the divergence operator's qualitative behavior — sign, magnitude, deseasonalization response, failure modes — across all domains tested | 6.3 | RETAINED |
| C-02 | The financial-market findings are corroborated by external calibration against systems with known physics | 6.3 | RETAINED |
| C-03 | The framework has direct practical value outside finance: ~8-week-earlier flu onset detection with simultaneous strain identification | 5.1 / 6.3 | RETAINED |
| L-01 | The paper does NOT introduce new mathematics; it validates pre-existing theory (Theorem 8b cited, not re-proved) | 1.1 / 4.1 | RETAINED |
| L-02 | The divergence zero-crossing does NOT improve seasonal-peak detection | 5.1.2 | RETAINED |
| L-03 | Performance is established on national-aggregate flu data only; regional, age-stratified, or facility-level behavior is unknown | 5.1.6 | RETAINED |
| L-04 | The retrospective lead-time is the evidentiary basis; the registered 2026–27 prediction is the unresolved out-of-sample test | 7 | RETAINED |
| L-05 | Financial-market comparison values are cited from Paper 4, not regenerated in this paper | 2.6 / 6.1 | RETAINED |

## Reconciliation (run before signing; re-run at Phase 4 open/close and Phase 5)

- [x] Every ARG node has ≥1 support and a valid `Depends on` (or "—" for a premise).
- [x] Every citation key maps to ≥1 ARG node or section — the 4 v4 orphans resolved 2026-06-28 (cite all four: Boettigers → §3.1, Li → §3.1/§4.1, Hsiang → §1.2).
- [x] Every load-bearing finding names a provisional LB-id; no values in this file (claims.lock fixes ids at Phase 3).
- [x] Every figure/table/equation (FIG-/TBL-/EQ-) has an anchor + a referencing ARG node.
- [x] Every scope condition (S-) and limit-of-claim (C-/L-) has an anchor.
- [ ] Every internal cross-reference resolves — checked mechanically by verify.py check-5 once the manuscript exists (Phase 4).
- [x] Every node has a status; no DROPPED nodes in this outline (the only source DROP — Connecticut River — is a dataset, recorded in COVERAGE §5).
- [x] The IMRaD map matches the source's section list.
- [x] (Rebuild) every COVERAGE KEEP/TRANSFORM row maps to ≥1 node here (sections → §1 map; experiments → ARG-04…12 + LB; figure/table/equations → §5; datasets → LB/ARG supports; AI-disclosure → IMRaD node).

## What the gate checks (machine vs checklist)

- **Mechanical (reconciliation gate, verify.py check-5 at Phase 4+):** every citation key, LB-id, FIG-/TBL-/EQ- id, S-/C-/L- anchor, and required section title present in the manuscript; every internal cross-reference resolves; every figure/table/equation referenced in text; no STUB/TODO/PLACEHOLDER/un-rendered {{…}}.
- **Accuracy (routed per element):** numbers → verify.py; citations → Phase-5b all-tier check; display elements → present-and-referenced (gate) + rendered (5c PDF QA); arguments → Phase-5a reviewer ticks each ARG node.

## Author sign-off

> The roadmap captures the paper's full argument (ARG-01…14), every citation (34; the 4 v4 orphans now cited, none removed), every load-bearing finding (by LB-id), every figure/table/equation (FIG-1, TBL-1, EQ-1…5), the assumptions/scope (S1–S4), and the conclusions/limits (C-01…03, L-01…05); every node has a status and (where applicable) a manuscript anchor; every COVERAGE keep maps to a node; no values are hard-coded. The 4 v4 orphan citations are resolved (cite all four; none removed).

**Signed:** Jae Kim / ORCID 0009-0005-3260-7880 — **Date:** 2026-06-28

---

*Paper roadmap, Standard v1.8. Living + versioned: updated, re-committed, and pushed whenever a Phase-2/3 result changes a node.*
