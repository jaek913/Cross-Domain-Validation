# DESIGN.md — Experiment & Data Design (Pre-Registration)

The exact operators, the pre-registered decision rules, the data manifest Phase 2 pulls-and-hashes against, and the specification-count disclosure — **grounded in this project's completed Stage 1.5/1.6 reproducibility verification** (the pre-fix repo's `verification/` + `analysis/` corpus), not the v4 manuscript's as-printed values. Committed before the first analysis commit; Phase-2 scripts implement exactly this; Phase-3 `verify.py` checks regenerated outputs against `claims.lock`.

## Metadata

- **Paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
- **Archetype:** empirical-with-verified-theory (proof count 0; Theorem 8b / Theorem 5 / the Paper-1 decomposition are **cited**, not re-derived)
- **Source pin (rebuild):** v4 manuscript, SHA256 `982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50` (MD5 `23428fb275f6ea6d6a3846fc17d91a86`) — the **pre-audit** manuscript; no revised paper exists
- **Verification record consulted (method-spec + corrected values, NOT a results target):** pre-fix repo `verification/Stage_1.1…1.6`, `Discrepancy_Register.md`, `analysis/repro_*.py`, `analysis/FINDINGS_*.md`
- **Standard:** v1.8 · **Design version:** v0.2 — 2026-06-28 · **Status:** draft (locks at first analysis commit)

## Changelog

- v0.1 2026-06-28 — initial pre-registration from the v4 manuscript alone. **Superseded.**
- v0.2 2026-06-28 — **rebuilt on the Stage 1.5/1.6 verification record** after an audit found v0.1 inherited v4's hidden Paper-4 reference imports and its single-generic-operator framing. Material changes: (1) the vdiv operator is **domain-specific** (four operators, §2/E2), not one generic operator; (2) corrected values baked in — Colorado vdiv ≈+0.10/+0.08 (was +0.33), Colorado–Ohio sweep matched +3.9/+4.7/+6.4 (was +6.0/+8.5/+15.2), Norwich deseasonalized vdiv flagged OPEN/unreproduced (Dallas +0.745→+0.004 reproduces); (3) provenance tiers added (regenerate / cite-Paper-4-reference / open); (4) sunspot decomposition + financial band = cited Paper-4 references, sunspot vdiv sign regenerated on SILSO v2.0 yearly; (5) manifest fixed (sunspot v2.0 yearly; six weather GHCN IDs); (6) spec pins added (continuous-vs-season SMAs, season exclusions, ACF max-lags, RW seed, strain spec); (7) §6 correction & provenance ledger added against the 24 LB claims + DISC-1.3…1.5 dispositions; (8) LB-1 "identical methodology" refined.
- v0.3 2026-06-28 — **D01 (Discrepancy Register).** Phase-2 reproduction showed the pre-registered **returns** operator gives **Ohio +0.30** (significant), not the +0.047 the v0.2 table recorded — which is the **level**-op value. Source recovery confirmed v4 used the level op; a variant sweep then pinned Colorado's +0.33 as a **look-ahead artifact** (CIC #4: the divergence `std(12)−std(63)` correlated with its own **contemporaneous** fast `std(12)`, no forward shift; reproduced at +0.322), while Ohio's +0.047 used the genuine forward target — so the two rivers were computed with **different targets** (the initial overlap/CIC-#5 hypothesis was tested and refuted: overlap ≈ subsample in every cell). Adjudication: reconstruction-correct / original-in-error. The "Colorado signal vs Ohio null" contrast **reverses** — volatility-clustering is universal across both rivers and *stronger* for the more seasonal Ohio; the level operator confounds volatility with the seasonal cycle. Updated: §2 hydrology row, §2 decision rule (2), §2 block-shuffle/provenance notes, §6 LB-7/8/9; OUTLINE ARG-06 / LB-e2-ohio-rho / S3 / L-06 / TBL-1; `verification/Discrepancy_Register.md` D01.
- v0.4 2026-06-28 — **D02 (Discrepancy Register).** The solar CSD sub-claim is restored. E2 printed solar CSD = −0.257 (negative), contradicting v0.2's "drop the sunspot 'CSD also negative' sub-claim (CSD +0.42)." Source recovery: the +0.42 came from the superseded **monthly / forward-vol** operator (`repro_solar`), and e2's −0.257 used a **forward-vol** target while the rebuild's solar vdiv predicts **future-level Y(t+5)**. Under the operator-matched comparison (AR1 ws=11 vs future-level) the sunspot CSD is **−0.103** — negative, lower magnitude than the vdiv's −0.230 — so v4's "CSD also negative, lower magnitude" **reproduces**. Adjudication: original correct. Updated: §2 CSD note, §6 LB-12; OUTLINE L-08 (reversed → retained) + ARG-07; e2 solar CSD → future-level target (forward-vol kept as a diagnostic); `verification/Discrepancy_Register.md` D02.
- v0.5 2026-06-28 — **E3 regeneration finding (not a Register dossier).** The LEVEL persistence-sign formulation reproduces exactly (20/25 overall, 13/13 significant-correct under the p<0.05 + Fisher-z rule with the p-only cross-check also 13, 0 significant-wrong, both flips, IS/OOS 13/13). The **rejected volatility formulation's exact v4 figures (≈44% / 11 significant-wrong) do NOT reproduce** — under-determined by the manuscript prose and absent from the Stage-1.5 verified record; three faithful constructions give 40% / 76% / 72% (all 5 significant-wrong). Marked **E3-rejected-volform OPEN** (DISC-1.5-02 pattern); the reproduced methodological contrast (vol form ≥5 significant-wrong vs level form 0) is retained. Amended: §2 E3 rejected-formulation bullet, open-items; OUTLINE LB-e3-rejected-volform.

## 0. Design summary

| Field | Value |
|---|---|
| Experiments | 6 (E1–E6) |
| Proofs | 0 |
| Load-bearing claims tracked | 24 (LB-1…LB-24; §6) |
| Datasets pulled + hashed | 5 sources (Connecticut River dropped) |
| **Provenance tiers** | **regenerate** (every value with in-manifest data) · **cite-Paper-4-reference** (financial S_W band; sunspot decomposition S_W/toward — labeled, not regenerable) · **open** (Norwich deseasonalized vdiv) |
| Falsifiers | headline = registered 2026–27 flu forward prediction (§5); in-paper = one statistically-significant wrong-sign Theorem-8b prediction (E3) |
| Verification status of design | every operator/value below traces to a Stage 1.5/1.6 reproduction or a Register disposition (DISC id cited) |

## 1. Shared operators

- **`SMA_N(Y,t)`** — mean of `Y` over the most recent `N` observations; no look-ahead. **Computed on the continuous series** (weekly flu SMAs reach across season boundaries; only the onset *search* is season-bounded — see E4/E5).
- **`std(Y,w,t)`** — trailing sample standard deviation over the most recent `w` observations.
- **Level divergence `D(t; w_f, w_s) = SMA_{w_f}(Y,t) − SMA_{w_s}(Y,t)`** (operator on the series itself).
- **Volatility divergence `vdiv(t; w_f, w_s) = std(Y',w_f,t) − std(Y',w_s,t)`**, where `Y'` is a **domain-specific transform** of the observable and the forward target is domain-specific — **defined per domain in E2** (the single generic level/level form reproduces only Ohio; see §6 / DISC-1.5-01/-02).
- **`ACF(Y, lag)`** — `pandas Series.autocorr`, integer lags, no taper. Max lag pinned per experiment.
- **Mean-ACF `R̄(a,b) = (1/(b−a)) Σ_{lag=a}^{b−1} ACF(lag)`**.
- **Gap-closure decomposition** — event = week where `|Y(t) − SMA(Y,t)|` exceeds the expanding 75th percentile of absolute displacement (min 50 prior obs, no look-ahead); over horizon `H` measure `C_W` (filter→Y) and `C_P` (Y→filter); `S_W = Σ C_W / Σ(C_W + C_P)`; `toward` = fraction of events whose first post-event step moves toward the filter; events non-overlapping, spaced ≥ `H`.

## 2. Experiments

### E1 — Calibration-scale decomposition

- **ARG / LB:** ARG-04/05 · LB-2, LB-3, LB-4, LB-5, LB-6.
- **Observable, by domain:** weather deseasonalized temperature anomaly `(TMAX+TMIN)/2` (**2 stations: Norwich, Dallas**); rivers daily log-discharge (raw + deseasonalized); influenza weekly `% WEIGHTED ILI`; sunspots — **see provenance**.
- **Operator/params:** SMA-50 & SMA-200, `H = 63` d (daily); rivers/weather as above; **flu pinned to SMA-4/SMA-16, `H = 13` wk** (the reconstructed cell; S_W ≈ 153.7%, toward ≈ 13% reproduces — v4's 122.6–288.8% range endpoints were under-specified and are not claimed). Event threshold = expanding 75th pctile, min 50.
- **Deseasonalization:** rivers per-calendar-month mean of log-discharge; weather day-of-year mean. Seasonal variance fraction `1 − Var(deseas)/Var(raw)` (Colorado 15.5%, Ohio 45.7% reproduce).
- **Control:** synthetic random walk — 10 sims matched to Colorado daily log-return drift/vol, **fixed `seed = 0`**; verify.py treats the control as a **tolerance band** (S_W ∈ ~99–101%, toward ∈ ~48–52%), not an exact match.
- **Pre-registered decision rules:** (1) S_W ordering weather (low) → deseasonalized rivers (mid) → flu (extreme) — reproduces; (2) **Colorado–Ohio deseasonalized SMA-200 gradient on the matched 1928–2026 period** (CO 17.8% / OH 13.1%, gap 4.7pp) widening across `H = 42/63/126` as **+3.9 / +4.7 / +6.4** (corrected; the printed +6.0/+8.5/+15.2 reproduces under no cell — DISC-1.4-01); (3) deseasonalization look-ahead robustness — expanding monthly means change deseasonalized S_W by **≤ 1.2 pp** (CO 0.8, OH 1.2 — DISC-1.4-02).
- **Provenance:** weather, rivers, flu S_W/toward **regenerated**. **Sunspot decomposition (S_W/toward) = cited Paper-4 reference** (v4 Part-VI footnote; does not reproduce on SILSO v2.0 — toward ~70–80%); **financial S_W band (~64–167%) = cited Paper-4 reference**. Both labeled as imports in the scale/TBL-1, not regenerated.
- **Produces:** LB-e1-weather-sw, LB-e1-colorado-sw, LB-e1-ohio-sw, LB-e1-flu-sw, LB-e1-rw-control, LB-e1-deseas-gradient. (sunspot/financial rows = cited).
- **Script → output:** `analysis/e1_calibration_decomposition.py` → `outputs/e1_calibration.json`.

### E2 — Volatility-divergence operator + CSD comparison (**domain-specific operators**)

- **ARG / LB:** ARG-06/07 · LB-7, LB-8, LB-9, LB-10, LB-11, LB-12, LB-13.
- **The operator is domain-specific** in both the volatility input and the forward target (Stage 1.6; the single generic level/level form reproduces only Ohio). The rebuild **documents all four** (resolving v4 §3.2's single-operator framing) and reports each domain's reproducible value:

| domain | volatility input `Y'` | forward target | windows | subsample | reproduces |
|---|---|---|---|---|---|
| hydrology | log-**returns** of discharge | forward returns-vol | 12/63 d | every 21 | **returns op (the signal): Ohio +0.30, Colorado +0.12** (both rivers); **level op (seasonal-confound null): Ohio +0.047/+0.021, Colorado -0.00** (both rivers) — D01; Ohio's +0.047 was mis-filed as the returns value in v0.2 |
| weather | **TMAX first-differences** | forward 21-d realized-vol | 21/252 d | every 21 | Dallas **+0.745 → +0.004** exact (per-month z-score deseason); Norwich raw +0.40 exact, **deseas +0.232 OPEN (~+0.05)** |
| epidemiology | **first differences** of %ILI | forward diff-vol | 4/16 wk | none | ILI **+0.42** (first-diff op; +0.393 wtd / +0.420 unwtd) |
| solar | yearly sunspot **level** | **future level `Y(t+5)`** (Theorem-8b form) | 3/11 yr | n/a | sunspot **−0.230** (perm-z −3.94) |

- **Deseasonalization:** rivers per-month log-discharge; weather **per-calendar-month z-score** (the recovered weather operator); flu/solar none (seasonal/oscillatory structure is the signal).
- **IS/OOS stability:** split at temporal midpoint; sign consistent across halves.
- **Block-shuffle null:** blocks of 63, **`nsh = 1000`, `seed = 0`**, `z = (ρ_real − μ_shuffle)/σ_shuffle`, threshold 2.0. (Deseasonalized Ohio **under the LEVEL op**: z = +1.99, borderline but < 2.0 → the level-op null reproduces; **under the pre-registered RETURNS op Ohio is +0.30, significant** — the null is operator-specific, not a property of the river — D01/LB-9.)
- **CSD comparator:** trailing lag-1 autocorrelation (AR(1) over a rolling `w_s` window); Spearman vs **the same target the domain's vdiv predicts** (forward vol for epi; **future-level Y(t+5) for solar** — D02); `vdiv` "outperforms" = correct sign with magnitude exceeding CSD's. **Epidemiology CSD carries the opposite (negative) sign** (ρ ≈ −0.165, reproduces — LB-11/13). **Sunspot CSD REPRODUCES v4's sub-claim** under the matched future-level target: ρ = −0.103 (negative, lower magnitude than the vdiv's −0.230 — D02); the +0.42 was the superseded monthly/forward-vol operator and −0.257 a forward-vol target mismatch.
- **Pre-registered decision rules:** (1) significant, IS/OOS-stable signal on storage-bearing systems — reproduces on the **returns** op for *both* rivers (Ohio +0.30, Colorado +0.12); (2) **FALSIFIED under the pre-registered returns op (D01):** Ohio is null only under the *level* op (the seasonal confound, +0.047); under the returns op it is +0.30 (the strongest hydrology signal) — the "Ohio null" expectation was grounded in v4's level-op value and does not hold for the pre-registered operator; (3) sunspot unique **negative** vdiv sign, Theorem-8b-predicted (LB-12 — reproduces); (4) epidemiology CSD opposite sign.
- **Provenance:** all four domains **regenerated** under their documented operator; **hydrology corrected per D01** — the **returns** op is the signal (Ohio +0.30, Colorado +0.12); the **level** op is the seasonal-confound null (Ohio +0.047, Colorado -0.00); Colorado's printed +0.33 is a **look-ahead artifact** (CIC #4: the divergence correlated with its own contemporaneous fast volatility, reproduced at +0.322 — not an overlap effect; DISC-1.5-01 + D01, CORRECT not restore), Ohio's +0.047 is the level+forward value, and the v4 "Colorado vs Ohio" contrast came from using different targets on the two rivers; **Norwich deseasonalized vdiv = OPEN** (report reproduced ~+0.05 + soften contrast; retrieving Paper-4's exact Norwich GHCN file to confirm +0.232 is a tracked option — DISC-1.5-02).
- **Produces:** LB-e2-colorado-rho, LB-e2-ohio-rho, LB-e2-weather-rho (Dallas/Norwich), LB-e2-flu-rho, LB-e2-sunspot-rho, LB-e2-csd-compare.
- **Script → output:** `analysis/e2_volatility_divergence_csd.py` → `outputs/e2_divergence_csd.json`.

### E3 — Theorem-8b persistence-sign test (the in-paper falsifier)

- **ARG / LB:** ARG-08/09 · LB-14, LB-15, LB-16, LB-17. **Reproduces exactly** (Stage 1.5/1.6).
- **Prediction rule (cited Theorem 8b):** `sign[Corr(D_t, Y_{t+h})] = sign[R̄(h, h+w_f) − R̄(h+w_f, h+w_s)]`.
- **Design:** 5 systems × 5 horizons = **25 pre-registered predictions**. Systems: Colorado (deseasonalized log-discharge), Ohio (deseasonalized log-discharge), Norwich (deseasonalized temp anomaly), Dallas (deseasonalized temp anomaly), Flu (**raw** weekly ILI). **Sunspots are NOT in the E3 set.**
- **Windows:** daily `w_f=12, w_s=63`; flu `w_f=4, w_s=16`. **Horizons:** daily `h = 21/42/63/126/252`; flu `h = 4/8/13/17/26`.
- **Observed sign:** Spearman `ρ`(`D(t)`, `Y(t+h)`); subsample every **21** (daily) / **8** (flu).
- **ACF:** `pandas Series.autocorr`, integer lags, **max lag 400** (daily; covers `h+w_s=315`) / **max lag 60** (flu; covers `h+w_s=42`); `R̄` arithmetic mean.
- **Pre-registered decision rules:** correct iff observed sign = predicted sign; significance = `p < 0.05` with Fisher-z 95% CI excluding zero. **Headline = significant-correct count** (reproduces 13/13: Colorado 5 + Ohio 3 + flu 5; weather 0 significant); overall 20/25. Both sign flips verify: Colorado `h=252` (R̄_near < R̄_far, **ACF still positive — not a zero-crossing**, DISC-1.4-04) and flu `h=26` (seasonal ACF; the ACF zero-crossing is at **14 wk**, distinct from `h=26`, DISC-1.4-05). IS/OOS on 6 representative predictions incl. both flips.
- **Falsifier (in-paper):** one statistically-significant prediction whose observed sign contradicts the rule.
- **Rejected formulation (correction note):** the **volatility**-divergence formulation (vol divergence vs forward volatility, judged by the level-ACF rule) is the documented rejected alternative. **The v4 exact ≈44% / 11-significant-wrong figures do NOT reproduce** and are under-determined by the prose (the horizon/sign convention is unspecified) and absent from the Stage-1.5 verified record; three faithful constructions (future-level / per-horizon / fixed-window forward-vol targets) give 40% / 76% / 72%, all with 5 significant-wrong — **E3-rejected-volform OPEN** (the DISC-1.5-02 pattern, not fabricated to match). **The robust reproduced contrast holds:** the vol formulation has **≥5 significant WRONG-signed** predictions vs the **level** formulation's **0**, confirming the level form is the correct application of Theorem 8b. The level formulation is primary; the vol formulation is reported as history at its regenerated value.
- **Provenance:** all 25 predictions **regenerated**.
- **Produces:** LB-e3-significant, LB-e3-overall, LB-e3-colorado-flip, LB-e3-flu-flip, LB-e3-rejected-volform.
- **Script → output:** `analysis/e3_theorem8b_sign.py` → `outputs/e3_theorem8b.json`.

### E4 — Divergence-based flu onset detection

- **ARG / LB:** ARG-10 · LB-18, LB-19. **Reproduces exactly** (Stage 1.5).
- **Observable / operator:** weekly national `% WEIGHTED ILI`; `D(t) = SMA_4(ILI,t) − SMA_12(ILI,t)` on the **continuous** series.
- **Divergence onset:** first week in a season with `D(t) > 0.2` pp (primary); sensitivity `0.1/0.2/0.3` (0.5 breaks).
- **Level comparator:** baseline = mean ILI over the season's first 4 weeks (≈ wk40–43); onset = first week `ILI > baseline + 1.0` pp; sensitivity `+0.5/+1.0/+1.5`.
- **Seasons (corrected — DISC-1.4-03):** **29 candidate seasons (1997-98 … 2025-26**, incl. the partial 23-wk 2025-26**); 27 enter the paired comparison** after excluding 2020-21 (peak < 2.0%) **and** 2009-10 (no level-based onset).
- **Decision rules:** lead = (level-onset wk) − (divergence-onset wk); divergence fires earlier in 26/27; mean lead-vs-level 8.2 wk, lead-vs-peak 14.1 wk, **floor 5 wk (vs peak), Q1 12 wk**; paired t / Wilcoxon; temporal-concentration shuffle (z ≈ +2.6).
- **Provenance:** **regenerated.** **Produces:** LB-e4-lead, LB-e4-seasons, LB-e4-floor.
- **Script → output:** `analysis/e4_flu_onset.py` → `outputs/e4_flu_onset.json`.

### E5 — Strain-level divergence (dominant-strain identification)

- **ARG / LB:** ARG-11 · LB-20, LB-21. **Single-strain 9/9 reproduces exact; hindsight/real-time counts are under-specified** (reconstruction got 20/27 & 25/27 & lead 2 vs v4's 21/27 & 24/27 & lead 0).
- **Observable / operator:** per-subtype percent-positive `(subtype count / total specimens) × 100` for H1N1, H3N2, B_total; `D_strain(t) = SMA_4 − SMA_12` on the **continuous** percent-positive series.
- **First-firing strain:** first subtype with `D_strain(t) > 0.3` pp in a season. **Dominant strain:** highest total positives over the season (hindsight) / highest cumulative at first firing (real-time).
- **Seasons:** **complete seasons through 2024** (strain dominance is a full-season concept — a different set from E4).
- **Strain spec — PINNED (resolves the under-specification; the exact counts follow from this and are reported as-regenerated, not asserted as v4's 78%/89%):** (a) `A (Subtyping not Performed)` counts **allocated proportionally** to the subtyped A(H1N1):A(H3N2) split that week; (b) first-firing **tie-break by higher percent-positive**; (c) onset reference = aggregate `D>0.2`; (d) pre-2009 H1N1 = `A (H1) + A (2009 H1N1)`; B lineages `B + BVic + BYam`; overlapping weeks → post-2015 file.
- **Provenance:** **regenerated** (counts = whatever the pinned spec yields; single-strain 9/9 robust).
- **Produces:** LB-e5-hindsight, LB-e5-realtime, LB-e5-single, LB-e5-lead.
- **Script → output:** `analysis/e5_strain_id.py` → `outputs/e5_strain_id.json`.

### E6 — Peak-detection hypothesis (rejected; honest negative)

- **ARG / LB:** ARG-12 · (supporting). Reproduces.
- **Operators:** divergence zero-crossing (pos→neg, declining phase) vs divergence peak (max `D`) vs SMA-4 peak vs true ILI peak (max ILI in season); lead = (peak wk) − (detector wk); continuous series.
- **Decision rules:** hypothesis **rejected** — zero-crossing lags the true peak (≈ +5.6 wk, worse than SMA-4 peak +2.1). Reported alongside: divergence peak precedes the ILI peak (≈ 1.7 wk; 96% of seasons; paired t = 4.36, p = 0.0002).
- **Provenance:** **regenerated.** **Produces:** LB-e6-zerocross, LB-e6-divpeak.
- **Script → output:** `analysis/e6_peak_detection.py` → `outputs/e6_peak_detection.json`.

## 3. Data manifest (Phase-2 pull-and-hash targets)

`pull.py` fetches + hashes (MD5 + SHA256) → `SOURCES.md`; scripts read only hashed copies; raw data git-ignored + separately backed up.

| Source | Exact identifier(s) | Fields | Coverage | Used by | Access |
|---|---|---|---|---|---|
| CDC ILINet | `ILINet.csv`, `REGION TYPE="National"` (title line → skiprows=1) | `% WEIGHTED ILI` (+ YEAR, WEEK) | 1997–2026, ~1,484 wks | E1,E2,E3,E4,E6 | FluView `gis.cdc.gov/grasp/fluview/fluportaldashboard.html` |
| CDC NREVSS (pre-2015) | `ICL_NREVSS_Combined_prior_to_2015_16.csv`, `REGION TYPE="National"` | TOTAL SPECIMENS, A(2009 H1N1), A(H1), A(H3), A(Subtyping not Performed), B | 1997–2015 | E5 | `cdc.gov/fluview/surveillance/` |
| CDC NREVSS (post-2015) | `ICL_NREVSS_Public_Health_Labs.csv`, `REGION TYPE="National"` | TOTAL SPECIMENS, A(2009 H1N1), A(H3), A(Subtyping not Performed), B, BVic, BYam | 2015–2026 | E5 | `cdc.gov/fluview/surveillance/` |
| NOAA GHCN-Daily | **6 stations:** NYC `USW00094728`, Blue Hill `USC00190736`, San Francisco `USW00023272`, Philadelphia `USW00013739`, **Dallas `USW00003927`** (DAL-FTW WSCMO — the 26,622-obs station, *not* the FAA station), Norwich `USC00065910` | TMAX, TMIN | 70–157 yr/station | E1 (Norwich, Dallas), E2 (all 6), E3 (Norwich, Dallas) | `ncdc.noaa.gov/cdo-web/` |
| USGS NWIS daily discharge | Colorado `08158000`; Ohio `03294500` | mean daily discharge (param `00060`, stat `00003`) | CO 1898–2026 (46,767); OH 1928–2026 (35,862) | E1, E2, E3 | `waterdata.usgs.gov/nwis` |
| SIDC / SILSO | **yearly** mean total sunspot number, **v2.0** (`SN_y_tot_V2.0`; mid-year, SN) | sunspot number | v2.0 (1700-present annual) | E2 (vdiv) | `sidc.be/SILSO/datafiles` |
| ~~Connecticut River~~ **DROPPED** | ~~USGS `01170500`~~ | — | 63.5-yr gap | — | replaced by Ohio |

Notes: the v4 sunspot-decomposition figures are a **cited Paper-4 reference** (no regeneration target); the SILSO **monthly v2.0 begins 1749** (v4's "1700–2008" is a different vintage). The six GHCN IDs resolve DISC-1.4-06 (Appendix A.2 listed only 2).

## 4. Specification-count disclosure

| Exp | Specs examined | Primary reported | Pre-registered | Notes |
|---|---|---|---|---|
| E1 | SMA-50/200 × H 42/63/126 + look-ahead variant + RW control (10 sims, seed 0) | SMA-50/200, H=63, matched-period gradient | yes | flu window SMA-4/16 H=13 pinned (v4 range under-specified) |
| E2 | **4 domain-specific operators** (table above) × block-shuffle (1000, seed 0) × horizons (42/63/126 Ohio) | one operator per domain (documented) | Paper-4-inherited | Colorado reported subsampled (~+0.10); Norwich deseas OPEN |
| E3 | 5 systems × 5 horizons = 25 + **2 formulations** (level primary / volatility rejected) | level divergence, 25-grid | yes | 13/13 significant reproduces exactly |
| E4 | 4 div thresholds (0.1/0.2/0.3/0.5) × 3 level baselines (+0.5/+1.0/+1.5) | Div>0.2 vs Level+1.0 | yes | 27 paired seasons (29 − 2020-21 − 2009-10) |
| E5 | 1 strain threshold (0.3) × **2 benchmarks** (hindsight/real-time) + pinned allocation/tie-break | first-firing>0.3 vs hindsight | partially | exact counts follow the pinned spec; single-strain 9/9 robust |
| E6 | 1 hypothesis (zero-crossing) + 1 alternative (divergence peak) | zero-crossing (rejected) | yes | honest negative |

## 5. Forward-prediction design (registered 2026–27 falsifier)

Two timestamped, reader-runnable predictions (CDC FluView), registered/dated at Phase 5c, tracked weekly at `LaggingTruth.com`.

**P1 — Onset lead.** `SMA_4(ILI) − SMA_12(ILI)` crosses `0.2` pp **≥ 6 weeks before** `ILI` crosses `baseline + 1.0` pp (baseline = mean ILI wk40–43/2026); window MMWR wk40/2026 → wk20/2027. **Falsified if** lead < 6 wk or divergence fires after level. **Untestable if** peak ILI < 2.0% → carries to 2027-28. Stronger variant: ≥ 10 wk before the peak.
**P2 — Dominant strain.** First subtype whose percent-positive divergence (`SMA_4 − SMA_12`, `0.3` pp) fires matches the full-season plurality strain. **Falsified if** mismatch **and** single-strain season (>70%). **Inconclusive if** mismatch in a mixed season. **Untestable if** specimens < 50% of the 2017-19 average.

## 6. Correction & provenance ledger (the 24 load-bearing claims + Register dispositions)

**Status key:** ✅ reproduces (regenerate, keep) · ✏️ CORRECT (regenerate to the corrected value) · 📎 cite Paper-4 reference (not regenerable) · ⚠️ OPEN (unresolved).

| LB | Claim (short) | Status | Action in rebuild | DISC |
|---|---|---|---|---|
| LB-1 | "identical methodology" external-calibration thesis | ✏️ | **refine:** decomposition + Theorem 8b applied identically (reproduce exactly); vdiv operator **adapted per domain** (disclosed) | (LB-1.5-01/-02 root) |
| LB-2 | S_W ordering weather≪rivers≪flu | ✅ (sunspot/financial rows 📎) | regenerate weather/river/flu; cite sunspot+financial | — |
| LB-3 | weather S_W 1.3–7.7%, toward 72–76% | ✅ | regenerate | — |
| LB-4 | flu S_W 122.6–288.8%, toward 13–25% | ✅ in-band | regenerate SMA-4/16 H=13 point; drop unsupported range endpoints | — |
| LB-5 | Colorado–Ohio gradient + sweep | ✏️ | gradient keeps; **sweep → matched +3.9/+4.7/+6.4** | 1.4-01 |
| LB-6 | gradient corroborates Paper 4 (Ohio OOS) | ✅ | keep (interpretation) | — |
| LB-7 | vdiv significant where ACF structure, null where averaged | ✏️ | **reframe (D01):** vol-clustering significant on the **returns** of *both* rivers (Ohio +0.30 > Colorado +0.12); the **level** op (vol confounded with the seasonal cycle) is ~null for both — the null is the operator/confound, not absent ACF structure | D01 |
| LB-8 | Colorado vdiv +0.33/+0.32 | ✏️ | **→ +0.12 returns / -0.00 level** (sub-21); the +0.33 is a **look-ahead artifact** (CIC #4: vdiv vs its own contemporaneous fast vol, ~+0.322) | 1.5-01 + D01 |
| LB-9 | Ohio vdiv +0.047/+0.021 (null) | ✏️ | **rewrite (D01):** +0.047 is the **level**-op value (seasonal confound, block-shuffle z=+1.99<2.0); under the pre-registered **returns** op Ohio is **+0.30** (the strongest river signal) — drop "Ohio null" as a standalone claim | D01 |
| LB-10 | weather vdiv; Dallas +0.745→+0.004; Norwich +0.39→+0.232 | ✅ Dallas / ⚠️ Norwich | Dallas regenerate exact; **Norwich deseas → ~+0.05 + soften contrast** (retrieve Paper-4 Norwich file = option) | 1.5-02 |
| LB-11 | epi vdiv +0.42; CSD opposite sign | ✅ | regenerate (first-diff op; CSD ρ≈−0.165) | — |
| LB-12 | sunspot unique negative vdiv | ✅ (sign) | regenerate sign on v2.0 yearly (−0.230); **sunspot "CSD also negative" RETAINED** (D02: matched future-level CSD −0.103, negative & lower-magnitude — reproduces) | D02 |
| LB-13 | vdiv outperforms CSD each domain | ✅ | keep at corrected magnitudes | — |
| LB-14 | 13/13 significant correct | ✅ | regenerate (exact) | — |
| LB-15 | 20/25 overall | ✅ | regenerate (exact) | — |
| LB-16 | two sign flips (Colorado h=252, flu h=26) | ✅ (✏️ wording) | values keep; **abstract/caption: Colorado flip is R̄_near<R̄_far, NOT an ACF zero-crossing** | 1.4-04 |
| LB-17 | per-domain 5/5·5/5·5/5·3/5·2/5 | ✅ | regenerate (exact) | — |
| LB-18 | onset 14.1 vs 5.9, +8.2, 26/27, t=9.35 | ✅ | regenerate (exact) | — |
| LB-19 | floor 5 wk, Q1 12 wk | ✅ | regenerate (exact) | — |
| LB-20 | strain 78%/100%/89% | ✏️ (single-strain ✅) | regenerate under pinned strain spec; report as-computed | 1.4-03 (count) |
| LB-21 | strain lead median 0 wk | ✏️ | regenerate (reconstruction got median 2) | — |
| LB-22 | ACF governs divergence behavior | ✅ | keep (interpretation) | — |
| LB-23/24 | 2026-27 forward predictions | — | register/date at 5c | — |

**Also (non-LB, Phase-2/4 fixes):** FIG-1 regenerate without the spurious "CO 0-cross ~132d" annotation + **commit it** (DISC-1.4-04); flu ACF zero-crossing stated once as **14 wk**, distinct from h=26 (DISC-1.4-05); Appendix A.2 list all six GHCN IDs (DISC-1.4-06); Ohio look-ahead "≤1.2pp" (DISC-1.4-02). **Citations (DISC-1.3-01…07):** Kim-2026d title → Paper 4's current title; Hong "H."→"K."; Li "Z."→"Y." (or removed); the four orphans cited (decided — §3 OUTLINE); Kaya quote fixed; Vega author tail → Mott, Ortiz de Lejarazu, Nunes; Zakamulin-Giner → "…momentum versus moving averages: a tale of differences," *Quantitative Finance* 20(6), 985–1007.

**Open items carried forward:** (1) **Norwich deseasonalized vdiv** — report ~+0.05 unless Paper-4's exact Norwich GHCN record confirms +0.232; (2) **flu E1 S_W range** — single pinned cell only unless the v4 window set is recovered; (3) **strain exact counts** — whatever the pinned spec yields; (4) **E3 rejected vol-formulation exact figures (≈44% / 11 significant-wrong)** — under-determined and not reproduced (regenerated constructions give 40–76%, 5 significant-wrong); report the regenerated value, with the vol form confirmed inferior (≥5 significant-wrong vs the level form's 0).

## 7. Planned Phase-2/3 artifacts

- **Phase 2:** `pull.py` (fetch + hash §3 → `SOURCES.md`); `analysis/operators.py` (§1 primitives + the four E2 domain operators); `analysis/data_io.py` (hashed loaders); `analysis/e1…e6_*.py` → `outputs/e1…e6_*.json`.
- **Phase 3:** committed builder → `claims.lock` (LB-id ↔ regenerated value, **provenance tag** regenerate/cite/open per §6); `verify.py` (7-point CIC + check-5 OUTLINE/COVERAGE reconciliation, RW-control tolerance band); `{{LB-id}}` renderer.

## Reconciliation (run before signing)

- [x] Every experiment E1–E6 maps to OUTLINE ARG nodes + LB-ids, and to the 24 Stage-1.1 LB claims (§6).
- [x] Every operator/window/threshold/horizon traces to a Stage 1.5/1.6 reproduction or a Register disposition (DISC id cited).
- [x] Every value is tiered: regenerate / cite-Paper-4-reference / open; no non-reproducing value is silently "restored."
- [x] The vdiv operator is documented per domain (resolves the §3.2 single-operator framing; DISC-1.5-01/-02).
- [x] All seven citation fixes (DISC-1.3) and six consistency fixes (DISC-1.4) are captured for Phase-2/4.
- [x] Spec gaps pinned: continuous-vs-season SMAs, season exclusions (29→27), ACF max-lags, RW seed, strain spec, flu E1 window.
- [x] Both falsifiers specified; no result values hard-coded in this file.
- [ ] (Phase-4) every internal cross-reference resolves — verify.py check-5 once the manuscript exists.

## Sign-off

> The design pre-registers all six experiments grounded in the completed Stage 1.5/1.6 verification: domain-specific vdiv operators (not one generic operator), corrected values baked in (Colorado vdiv, the Colorado–Ohio sweep, the sunspot/financial cited references), the open Norwich and strain-spec items flagged, the full pull-and-hash manifest (sunspot fixed to SILSO v2.0 yearly; six weather GHCN IDs), the spec-count disclosure, both falsifiers, and a correction-and-provenance ledger against all 24 load-bearing claims and the DISC-1.3…1.5 dispositions. The "identical methodology" thesis (LB-1) is refined to match the domain-adapted operator. Committed before the first analysis commit.

**Signed:** Jae Kim / ORCID 0009-0005-3260-7880 — **Date:** 2026-06-28 *(pending review of the five rebuild decisions in this session)*

---

*Pre-registration, Standard v1.8, grounded in the Stage 1.5/1.6 verification record. Locks at the first analysis commit; any later change to an operator, threshold, value tier, or manifest entry is a documented decision in the changelog + DECISIONS.md.*
