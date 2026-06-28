# OUTLINE.md — Paper Roadmap

The paper's skeleton: the ordered argument, every citation, the load-bearing findings (by LB-id, never valued), the figures/tables/equations, the assumptions/scope, and the conclusions. The manuscript is **written from** this and mechanically **reconciled against** it at Phases 4–5. No values live here. **v0.2 is grounded in the pre-fix repo's completed Stage 1.5/1.6 verification record** (corrected values + the 24 load-bearing claims), not the v4 manuscript's as-printed numbers.

## Metadata

- **Paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
- **Archetype:** empirical-with-verified-theory
- **Source pin (rebuild):** v4 manuscript, SHA256 `982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50` (MD5 `23428fb275f6ea6d6a3846fc17d91a86`) — pre-audit; no revised paper exists
- **Verification record consulted:** pre-fix repo `verification/Stage_1.1…1.6`, `Discrepancy_Register.md`, `analysis/repro_*.py`, `FINDINGS_*.md`
- **Standard:** v1.8 · **Outline version:** v0.2 — 2026-06-28 · **Status:** draft

## Changelog

- v0.1 2026-06-28 — initial roadmap from the v4 manuscript + COVERAGE. Orphan citations resolved (cite all four). **Superseded.**
- v0.2 2026-06-28 — **rebuilt on the Stage 1.5/1.6 verification record** (with DESIGN v0.2). Argument-chain wording corrected (ARG-06/07 vdiv operator is domain-specific; ARG-08 the Colorado flip is **not** an ACF zero-crossing); load-bearing findings carry a status tier (regenerate / correct / cite / open) and an original-LB cross-reference to the 24 Stage-1.1 claims; FIG-1/TBL-1/EQ-2 corrected; scope condition S5 (domain-adapted operator) and limits L-06/07/08 added; the seven DISC-1.3 reference-list metadata fixes tracked for Phase 4 (keys unchanged); LB-1 "identical methodology" refined.

## 1. IMRaD structural map (the skeleton)

Ordered section list; every node below lands in one of these. (Parts structure, not a single Related-Literature section — prior art distributed across §1.2, §3.1, §4.1, §5.1.1, tracked in §3.) **Abstract carries a Phase-4 correction** (DISC-1.4-04): the Colorado "sign flip at the ACF zero-crossing" clause is wrong (Colorado ACF stays positive) and is reworded to the R̄_near<R̄_far mechanism.

Abstract → Part I Introduction (1.1 What This Paper Tests · 1.2 Why Natural Sciences · 1.3 Organization) → Part II Calibration Scale / Decomposition (2.1 Methodology · 2.2 Weather · 2.3 Rivers [2.3.1–2.3.5] · 2.4 Sunspots · 2.5 Influenza · 2.6 Complete Scale) → Part III Divergence Operator + CSD (3.1 · 3.2 Methodology · 3.3 Results by Domain [3.3.1–3.3.4] · 3.4 Summary · 3.5 Bias Audit) → Part IV Persistence-Sign / Theorem 8b (4.1 · 4.2 · 4.3 · 4.4 Results · 4.5 Post-Test · 4.6 Correction Note) → Part V Applications (5.1 Flu Onset [5.1.0–5.1.6] · 5.2 Weather-to-River) → Part VI Synthesis (6.1 Table · 6.2 ACF Diagram · 6.3 Conclusions · 6.4 Bias Audit) → Part VII Forward Predictions (7.1 · 7.2 · 7.3 · 7.4) → Acknowledgments & AI Disclosure → References → Appendix A (A.1–A.4).

## 2. Argument chain (the spine)

| ID | Claim (one line) | § | Depends on | Support (LB-id / cite key) | Status |
|---|---|---|---|---|---|
| ARG-01 | The framework (decomposition + divergence operator + Theorem-8b ACF-sign rule + CSD-superset) was derived from first principles and validated only on financial data | 1.1 | — | Kim-2026a, Kim-2026b, Kim-2026c, Kim-2026d | RETAINED |
| ARG-02 | Testing it on systems where the physics is independently known validates by external calibration | 1.2 | ARG-01 | Kaya-2025 | RETAINED |
| ARG-03 | Each domain's known restoring-force structure predicts specific framework behavior (weather strong, rivers storage-dependent, sunspots oscillatory, flu none) | 1.2 | ARG-02 | Hurst-1951, Koutsoyiannis-2002 | RETAINED |
| ARG-04 | The decomposition — applied **identically** across domains — orders systems by restoring-force strength (weather low S_W → deseasonalized rivers intermediate → flu extreme; financial + sunspot cited from Paper 4) | 2.2–2.6 | ARG-03 | LB-e1-weather-sw, LB-e1-colorado-sw, LB-e1-ohio-sw, LB-e1-flu-sw, LB-e1-rw-control | RETAINED |
| ARG-05 | Deseasonalization separates genuine non-seasonal persistence (Colorado) from seasonal artifact (Ohio collapse), corroborating Paper-4's Ohio finding by an independent method | 2.3.4 | ARG-04 | LB-e1-deseas-gradient, Kim-2026d, Koutsoyiannis-2005, O'Connell-2016 | CORRECTED (sweep → matched +3.9/+4.7/+6.4) |
| ARG-06 | The divergence operator — **adapted to each domain's natural innovation representation** (log-returns / first-differences / level) — produces significant IS/OOS-stable signals where ACF structure exists, and a null where basin-averaging removes it (Ohio deseasonalized) | 3.2–3.3 | ARG-03 | LB-e2-colorado-rho, LB-e2-ohio-rho, LB-e2-flu-rho, LB-e2-weather-rho, LB-e2-sunspot-rho | CORRECTED (domain-specific operators; Colorado ≈+0.10; Norwich OPEN) |
| ARG-07 | The divergence operator outperforms single-window CSD in each domain; CSD is opposite-signed in epidemiology | 3.3–3.4 | ARG-06 | LB-e2-csd-compare, Scheffer-2009, Dakos-2008, Corsi-2009 | CORRECTED (sunspot "CSD also negative" sub-claim dropped) |
| ARG-08 | Theorem-8b's ACF-sign prediction holds 100% on statistically significant predictions, including two sign flips — Colorado h=252 (R̄_near<R̄_far, ACF still positive) and flu h=26 (at the seasonal-ACF zero-crossing) | 4.4–4.5 | ARG-03 | LB-e3-significant, LB-e3-overall, LB-e3-perdomain, LB-e3-colorado-flip, LB-e3-flu-flip, Lo-MacKinlay-1988, Hong-Satchell-2015 | CORRECTED (flip mechanism wording) |
| ARG-09 | The ACF is the unifying variable governing the divergence operator's sign, magnitude, deseasonalization response, and failure modes across all domains | 6.2–6.3 | ARG-04, ARG-06, ARG-07, ARG-08 | FIG-1, Hurst-1951, Mandelbrot-Wallis-1968 | RETAINED |
| ARG-10 | A divergence-based flu-onset detector fires ~8 weeks earlier than level-based surveillance across nearly all seasons | 5.1.2 | ARG-06 | LB-e4-lead, LB-e4-seasons, LB-e4-floor, Shaman-Karspeck-2012, Steiner-2010, Vega-2013 | RETAINED |
| ARG-11 | Strain-level divergence identifies the dominant circulating strain (hindsight, real-time, and clearly-single-strain seasons) | 5.1.3 | ARG-10 | LB-e5-hindsight, LB-e5-realtime, LB-e5-single, LB-e5-lead, Goldstein-2011, Kandula-2017 | CORRECTED (strain spec pinned; counts as-regenerated) |
| ARG-12 | The divergence zero-crossing does NOT improve peak detection — a rejected hypothesis, reported honestly | 5.1.2 | ARG-10 | LB-e6-zerocross, LB-e6-divpeak | RETAINED |
| ARG-13 | The natural-science validation corroborates the financial findings by external calibration; the decomposition and Theorem 8b are applied identically, the divergence operator is domain-adapted (disclosed) | 6.3 | ARG-04, ARG-05, ARG-06, ARG-07, ARG-08, ARG-09 | Kaya-2025 | CORRECTED (LB-1 refinement) |
| ARG-14 | Two dated 2026–27 flu forward predictions convert the retrospective validation into a falsifiable out-of-sample test | 7 | ARG-10, ARG-11 | (registered prediction; resolves post-publication) | RETAINED |

## 3. Citations

One row per reference; `Key` is what the reconciliation gate greps for; PRESENCE + ROLE only. The four v4 orphans are cited (decided 2026-06-28). **Seven reference-list metadata fixes (DISC-1.3-01…07) apply at Phase 4 — keys are unchanged, flagged ✦ below:** Kim-2026d cited title → Paper 4's current title; Hong initial H→K; Li initial Z→Y; Vega author tail → Mott, Ortiz de Lejarazu, Nunes; Zakamulin-Giner title/venue → "…momentum versus moving averages: a tale of differences," *Quantitative Finance* 20(6), 985–1007; Kaya in-text quote corrected.

| Key (Surname-YEAR) | Role | Supports (ARG / §) | Status |
|---|---|---|---|
| Kim-2026a | foundation (self-cite, framework origin) | ARG-01 / 1.1 | RETAINED |
| Kim-2026b | foundation (self-cite) | ARG-01 / 1.1 | RETAINED |
| Kim-2026c | foundation (self-cite) | ARG-01 / 1.1 | RETAINED |
| Kim-2026d ✦ | foundation (self-cite; Theorem-8b source + financial/sunspot reference values) | ARG-01, ARG-05, ARG-08 / 1.1, 2.3.4, 4.1 | RETAINED (title fix) |
| Hurst-1951 | foundation (cross-domain universality) | ARG-03, ARG-09 / 1.2, 6.3 | RETAINED |
| Mandelbrot-Wallis-1968 | foundation (universality / fractional Gaussian) | ARG-09 / 1.2, 6.3 | RETAINED |
| Kaya-2025 ✦ | prior-art (nearest precedent: financial indicators → natural science) | ARG-02, ARG-13 / 1.2, 6.3 | RETAINED (quote fix) |
| Lo-MacKinlay-1988 | prior-art (ACF-sign / variance ratio, finance) | ARG-08 / 4.1 | RETAINED |
| Hong-Satchell-2015 ✦ | prior-art (ACF-sign / momentum amplification, finance) | ARG-08 / 4.1 | RETAINED (initial fix) |
| Ferreira-2019 | prior-art (MA trading rule autocovariance, finance) | ARG-08 / 4.1 | RETAINED |
| Moskowitz-2012 | prior-art (time-series momentum autocovariance, finance) | ARG-08 / 4.1 | RETAINED |
| Zakamulin-Giner-2020 ✦ | prior-art (MA-indicator correlation under AR(p), finance) | ARG-08 / 4.1 | RETAINED (title/venue fix) |
| Corsi-2009 | prior-art (multi-scale realized volatility / HAR) | ARG-06, ARG-07 / 3.1 | RETAINED |
| Scheffer-2009 | prior-art (CSD / early-warning foundation) | ARG-07 / 3.1 | RETAINED |
| Dakos-2008 | prior-art (CSD for abrupt climate change) | ARG-07 / 3.1 | RETAINED |
| Dakos-2012a | prior-art (CSD indicator suite) | ARG-07 / 3.1 | RETAINED |
| Dakos-2012b | prior-art (CSD robustness; variance can decrease) | ARG-07 / 3.1, 3.3.2 | RETAINED |
| Dablander-2022 | prior-art (overlapping-timescale EWS, COVID) | ARG-07 / 3.1, 3.3.2 | RETAINED |
| Koutsoyiannis-2002 | prior-art (hydrological persistence / fGn) | ARG-03, ARG-05 / 1.2, 2.3.4 | RETAINED |
| Koutsoyiannis-2005 | prior-art (hydrologic persistence) | ARG-05 / 2.3.4 | RETAINED |
| Koutsoyiannis-2006 | prior-art (nonstationarity vs scaling) | ARG-05 / 2.3.4 | RETAINED |
| O'Connell-2016 | prior-art (Hurst legacy, hydrology) | ARG-05 / 2.3.4 | RETAINED |
| Shaman-Karspeck-2012 | contrast (mechanistic flu forecasting, >7wk peak) | ARG-10 / 5.1.1 | RETAINED |
| Shaman-2013 | contrast (real-time flu forecasts) | ARG-10 / 5.1.1 | RETAINED |
| Pei-2018 | contrast (spatial flu transmission forecast) | ARG-10 / 5.1.1 | RETAINED |
| Vega-2013 ✦ | contrast (Moving Epidemic Method, WHO/ECDC) | ARG-10 / 5.1.1 | RETAINED (author-tail fix) |
| Steiner-2010 | method-precedent (EWMA control charts, closest precedent) | ARG-10 / 5.1.1 | RETAINED |
| Goldstein-2011 | method-precedent (strain-specific incidence) | ARG-11 / 5.1.3 | RETAINED |
| Kandula-2017 | method-precedent (subtype-specific forecast) | ARG-11 / 5.1.3 | RETAINED |
| Gatti-2026 | contrast (pre-season subtype forecasting) | ARG-11 / 5.1.4 | RETAINED |
| Boettiger-Hastings-2012 ✦ | prior-art (CSD detection limits) | ARG-07 / 3.1 (orphan in v4; cited in rebuild) | RETAINED |
| Boettiger-Ross-Hastings-2013 ✦ | prior-art (EWS charted/uncharted) | ARG-07 / 3.1 (orphan in v4; cited in rebuild) | RETAINED |
| Hsiang-2016 ✦ | prior-art (climate econometrics) | 1.2 (orphan in v4; cited in rebuild) | RETAINED |
| Li-2025 ✦ | prior-art (operator analysis of MACD) | 3.1 / 4.1 (orphan in v4; cited in rebuild; initial fix) | RETAINED |

Roles: prior-art · motivating-anomaly · method-precedent · corroboration · contrast · foundation (self-cite).

## 4. Load-bearing findings

Keyed to `claims.lock` (Phase 3); **no values here.** Each carries a **status tier** — REGEN (reproduces, regenerate) · CORRECT (regenerate to the corrected value) · CITE (Paper-4 reference, not regenerated) · OPEN (unresolved) — and a cross-reference to the original Stage-1.1 claim (LB-N).

| LB-id (provisional) | Finding (one line, no value) | Supports (ARG) | Status | orig LB |
|---|---|---|---|---|
| LB-e1-weather-sw | Weather temperature-anomaly filter-share (benchmark low end) | ARG-04 | REGEN | LB-3 |
| LB-e1-colorado-sw | Colorado River filter-share, raw and deseasonalized | ARG-04, ARG-05 | REGEN | LB-5 |
| LB-e1-ohio-sw | Ohio River filter-share, raw and deseasonalized (collapse) | ARG-04, ARG-05 | REGEN | LB-5 |
| LB-e1-flu-sw | Influenza filter-share (extreme mechanical adaptation; SMA-4/16 H=13 cell) | ARG-04 | REGEN | LB-4 |
| LB-e1-rw-control | Synthetic random-walk control filter-share + toward (seed 0; tolerance band) | ARG-04 | REGEN | (support) |
| LB-e1-deseas-gradient | Deseasonalized Colorado-vs-Ohio gap and horizon sweep | ARG-05 | CORRECT (matched +3.9/+4.7/+6.4) | LB-5 |
| LB-e1-sunspot-sw | Sunspot filter-share | ARG-04 | CITE (Paper-4 ref; not on SILSO v2.0) | LB-2 |
| LB-e1-financial-band | Financial-market filter-share band | ARG-04 | CITE (Paper-4 ref) | LB-2 |
| LB-e2-colorado-rho | Colorado divergence↔forward-vol correlation (log-returns op) | ARG-06 | CORRECT (≈+0.10/+0.08; was +0.33) | LB-8 |
| LB-e2-ohio-rho | Ohio divergence correlation (raw borderline; deseasonalized null + shuffle z) | ARG-06 | REGEN (exact) | LB-9 |
| LB-e2-flu-rho | Influenza divergence correlation (first-differences op) | ARG-06 | REGEN | LB-11 |
| LB-e2-weather-rho | Weather divergence (Dallas reproduces; Norwich deseasonalized) | ARG-06 | OPEN (Norwich ~+0.05; Dallas exact) | LB-10 |
| LB-e2-sunspot-rho | Sunspot divergence — unique negative sign (yearly level / future-Y) | ARG-06 | REGEN (sign on v2.0 yearly) | LB-12 |
| LB-e2-csd-compare | Divergence-vs-CSD per domain (opposite sign in epidemiology) | ARG-07 | CORRECT (sunspot CSD sub-claim dropped) | LB-7, LB-13 |
| LB-e3-significant | Significant-correct count (Theorem-8b sign) | ARG-08 | REGEN (exact 13/13) | LB-14 |
| LB-e3-overall | Overall-correct count across 25 predictions | ARG-08 | REGEN (exact 20/25) | LB-15 |
| LB-e3-perdomain | Per-domain Theorem-8b breakdown (5/5·5/5·5/5·3/5·2/5) | ARG-08 | REGEN (exact) | LB-17 |
| LB-e3-colorado-flip | Colorado long-horizon sign flip (R̄_near<R̄_far; ACF positive) | ARG-08, ARG-09 | REGEN | LB-16 |
| LB-e3-flu-flip | Influenza sign flip at seasonal-ACF zero-crossing | ARG-08, ARG-09 | REGEN | LB-16 |
| LB-e3-rejected-volform | Rejected volatility-divergence formulation (≈44%, 11 sig-wrong) | ARG-08 | REGEN (documented rejected alternative) | (support) |
| LB-e4-lead | Divergence-vs-level lead, and divergence-vs-peak lead | ARG-10 | REGEN (exact) | LB-18 |
| LB-e4-seasons | Fraction of seasons divergence fires earlier (26/27) | ARG-10 | REGEN (exact) | LB-18 |
| LB-e4-floor | Minimum lead-time floor (vs peak) + Q1 | ARG-10 | REGEN (exact) | LB-19 |
| LB-e5-hindsight | Dominant-strain accuracy (full-season hindsight) | ARG-11 | CORRECT (as-regenerated, pinned spec) | LB-20 |
| LB-e5-realtime | Dominant-strain accuracy (real-time at detection) | ARG-11 | CORRECT (as-regenerated) | LB-20 |
| LB-e5-single | Accuracy in single-strain-dominated seasons | ARG-11 | REGEN (9/9 robust) | LB-20 |
| LB-e5-lead | Strain-fire vs aggregate-onset lead | ARG-11 | CORRECT (as-regenerated) | LB-21 |
| LB-e6-zerocross | Divergence zero-crossing peak-lag (rejected) | ARG-12 | REGEN | (support) |
| LB-e6-divpeak | Divergence-peak lead over the true ILI peak | ARG-12 | REGEN | (support) |

Interpretations (no value): **LB-1** (external-calibration thesis, refined) → ARG-01/13; **LB-6** (gradient corroborates Paper 4) → ARG-05; **LB-22** (ACF governs behavior) → ARG-09. Forward predictions **LB-23/24** → ARG-14.

## 5. Figures, tables & equations

Gate checks each is PRESENT at its anchor AND REFERENCED. Each carries a COVERAGE disposition.

| ID | What it shows (one line) | § | Referenced by (ARG / §) | Status |
|---|---|---|---|---|
| FIG-1 | ACF unification diagram (deseasonalized ACF: Colorado, Ohio, Dallas, flu, common lag axis) | 6.2 | ARG-09 / 6.2 | CORRECT (regenerate **without** the spurious "CO 0-cross ~132d" annotation; **commit it** — DISC-1.4-04) |
| TBL-1 | Unified cross-domain table (S_W, toward, divergence ρ, Theorem-8b, seasonality, ACF lags per system) | 6.1 | ARG-09, ARG-13 / 6.1 | CORRECT (Colorado ρ≈+0.10; matched sweep; sunspot/financial cited; Norwich open; sunspot ACF on v2.0) |
| EQ-1 | Gap-closure decomposition (filter-share = filter gap-closure / total gap-closure) | 2.1 | ARG-04 / 2.1 | REGEN (anchor added) |
| EQ-2 | Volatility-divergence operator — generic form (fast std − slow std) **plus the four domain-specific constructions** | 3.2 | ARG-06 / 3.2 | CORRECT (document domain-specific operators) |
| EQ-3 | Level-divergence operator (fast SMA − slow SMA) | 4.1 | ARG-08 / 4.1 | REGEN (anchor added) |
| EQ-4 | Theorem-8b sign rule + mean-ACF definition | 4.1 | ARG-08 / 4.1 | REGEN (anchor added) |
| EQ-5 | Flu-onset divergence (4-week SMA − 12-week SMA of ILI) | 5.1 | ARG-10 / 5.1.2 | REGEN (anchor added) |

## 6. Assumptions & scope conditions

Each carries a greppable `S-` anchor in the manuscript.

| ID | Statement | Where stated (anchor) | Status |
|---|---|---|---|
| S1 | The observable's autocorrelation structure is approximately stationary over the sample | 3.2 / 4.1 | RETAINED |
| S2 | Deseasonalization (monthly-mean, day-of-year mean, or per-month z-score) adequately removes the seasonal cycle while preserving stochastic departures | 2.3.2 / 3.3.3 / 4.2 | RETAINED |
| S3 | The divergence operator requires sufficient autocorrelation structure; it returns a null where basin-scale averaging or deseasonalization removes that structure | 3.3 / 6.3 | RETAINED |
| S4 | The forward-prediction test requires a genuine flu season (peak ILI ≥ activity floor); a low-activity season is untestable, not falsifying | 7.1 | RETAINED |
| S5 | The decomposition and Theorem 8b are applied identically across all four domains; the divergence operator is adapted to each domain's natural innovation representation (log-returns / first-differences / level), disclosed as such | 3.2 | NEW |

## 7. Conclusions & limits-of-claim

Each carries a greppable `C-`/`L-` anchor.

| ID | Conclusion or limit-of-claim | Where (anchor) | Status |
|---|---|---|---|
| C-01 | The ACF governs the divergence operator's qualitative behavior across all domains tested | 6.3 | RETAINED |
| C-02 | The financial-market findings are corroborated by external calibration against systems with known physics | 6.3 | RETAINED |
| C-03 | Direct practical value outside finance: ~8-week-earlier flu onset detection with simultaneous strain identification | 5.1 / 6.3 | RETAINED |
| L-01 | No new mathematics; pre-existing theory validated (Theorem 8b cited). The decomposition and Theorem 8b are applied identically across domains; the divergence operator is domain-adapted | 1.1 / 4.1 | CORRECTED |
| L-02 | The divergence zero-crossing does NOT improve seasonal-peak detection | 5.1.2 | RETAINED |
| L-03 | National-aggregate flu data only; regional/age-stratified/facility-level behavior unknown | 5.1.6 | RETAINED |
| L-04 | The retrospective lead-time is the evidentiary basis; the registered 2026–27 prediction is the unresolved out-of-sample test | 7 | RETAINED |
| L-05 | Financial-market **and sunspot-decomposition** comparison values are cited from Paper 4, not regenerated here | 2.6 / 6.1 | CORRECTED |
| L-06 | The Colorado divergence magnitude is reported at the defensible subsampled value (≈+0.10), correcting Paper-4's overlap-inflated +0.33; the qualitative Colorado-vs-Ohio contrast holds | 3.3.1 | NEW |
| L-07 | The Norwich deseasonalized-divergence contrast magnitude is unverified on the current record (reported at the reproduced value; the larger figure is source-authentic but unreproduced) | 3.3.3 | NEW |
| L-08 | The sunspot "CSD also negative" sub-claim is dropped (does not reproduce on SILSO v2.0); the load-bearing sunspot claim is the negative divergence sign, which reproduces | 3.3.4 | NEW |

## Reconciliation (run before signing; re-run at Phase 4 open/close and Phase 5)

- [x] Every ARG node has ≥1 support and a valid `Depends on` (or "—").
- [x] Every citation key maps to ≥1 ARG node or section; four orphans cited; seven DISC-1.3 metadata fixes tracked for Phase 4 (keys unchanged).
- [x] Every load-bearing finding names an LB-id, a status tier, and an original-LB cross-reference; **all 24 Stage-1.1 claims covered** (LB-1…24 ↔ LB-e* / ARG nodes); no values here.
- [x] Every figure/table/equation has an anchor + a referencing ARG node; FIG-1/TBL-1/EQ-2 corrections noted.
- [x] Every scope condition (S-) and limit-of-claim (C-/L-) has an anchor; S5 + L-06/07/08 added for the corrections.
- [ ] Every internal cross-reference resolves — verify.py check-5 once the manuscript exists (Phase 4).
- [x] Every node has a status; the one source DROP (Connecticut River) is a dataset, recorded in COVERAGE.
- [x] The IMRaD map matches the source's section list; the abstract correction (DISC-1.4-04) is flagged.
- [x] (Rebuild) every COVERAGE keep/correct row maps to ≥1 node here; corrected values trace to the DESIGN §6 ledger + Register dispositions.

## What the gate checks (machine vs checklist)

- **Mechanical (verify.py check-5 at Phase 4+):** every citation key, LB-id, FIG-/TBL-/EQ- id, S-/C-/L- anchor, and required section title present; every internal cross-reference resolves; every figure/table/equation referenced; no STUB/TODO/PLACEHOLDER/un-rendered {{…}}.
- **Accuracy (routed):** numbers → verify.py (against claims.lock with provenance tags); citations → Phase-5b all-tier check (incl. the seven DISC-1.3 fixes); display elements → present-and-referenced (gate) + rendered (5c); arguments → Phase-5a reviewer ticks each ARG node.

## Author sign-off

> The roadmap captures the full argument (ARG-01…14, corrected wording), every citation (34; four orphans cited; seven metadata fixes tracked), every load-bearing finding by LB-id with a status tier and a cross-reference covering all 24 Stage-1.1 claims, every figure/table/equation (FIG-1/TBL-1/EQ-1…5, corrections noted), the assumptions/scope (S1–S5), and the conclusions/limits (C-01…03, L-01…08); every node has a status; corrected values trace to the DESIGN §6 ledger; no values are hard-coded. LB-1 "identical methodology" is refined to the domain-adapted operator.

**Signed:** Jae Kim / ORCID 0009-0005-3260-7880 — **Date:** 2026-06-28 *(pending review of the five rebuild decisions in this session)*

---

*Paper roadmap, Standard v1.8, grounded in the Stage 1.5/1.6 verification record. Living + versioned: updated, re-committed, and pushed whenever a Phase-2/3 result changes a node.*
