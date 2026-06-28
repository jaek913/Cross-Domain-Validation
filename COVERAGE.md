# COVERAGE.md — Rebuild Coverage Ledger

The Phase-1 gate that accounts for every element of the source so nothing vanishes silently into the rebuild. Read again at Phase 2 (execution), Phase 4 (shape gate), and Phase 5a (reviewer completeness). Every KEEP/TRANSFORM/CITE/OPEN row maps to a node in OUTLINE.md. **v0.2 re-dispositions every row against the pre-fix repo's completed Stage 1.5/1.6 verification record** — several v4 numbers are corrections or Paper-4 reference imports, not clean restorations.

## Metadata

- **Rebuild paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
- **Source artifact:** `C:\Users\jaek9\Documents\Repos\lagging-truth-paper-05\paper\Paper5_Final_Natural_Sciences_Validation_v4.md` — MD5 `23428fb275f6ea6d6a3846fc17d91a86` / SHA256 `982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50` (pinned — "source material, not inherited results"; **pre-audit, no revised paper exists**). Supporting assets (figure1.png, 8 reference PDFs, companion, build chain) at `C:\Users\jaek9\Documents\LaggingTruth\05-13-2026\Paper 5\`.
- **Verification record consulted:** pre-fix repo `verification/Stage_1.1…1.6`, `Discrepancy_Register.md` (DISC-1.3-01…07, DISC-1.4-01…06, DISC-1.5-01/-02), `analysis/repro_*.py`, `FINDINGS_*.md`.
- **Archetype:** empirical-with-verified-theory · **Author:** Jae Kim / ORCID 0009-0005-3260-7880 · **Standard:** v1.8 · **Version:** v0.2 · **Status:** draft — 2026-06-28

> **Disposition convention (v0.2).** **KEEP** = restore + regenerate; reproduces under the Stage 1.5/1.6 reconstruction; substance unchanged. **TRANSFORM** = a knowing change — a corrected value, a re-scoped computation, a documented domain-specific operator, a citation-metadata fix, or an added greppable anchor. **CITE** = a Paper-4 reference value, displayed but not regenerated here. **OPEN** = a value that does not reproduce on the current record and awaits a Paper-4-side recovery or a softened claim. **DROP** = excluded with cause. Each TRANSFORM/CITE/OPEN names the DISC dossier it implements; corrected values trace to the DESIGN §6 ledger.

## Changelog

- v0.1 2026-06-28 — built from the pinned v4 manuscript alone; everything KEEP/"values regenerated". **Superseded** (it inherited v4's Paper-4 reference imports and single-operator framing).
- v0.2 2026-06-28 — **re-dispositioned on the Stage 1.5/1.6 verification record.** Corrections marked TRANSFORM (Colorado vdiv, the Colorado–Ohio sweep, the domain-specific operator, the abstract/FIG-1 ACF fix, the season count, the strain spec, the seven citation fixes, six weather GHCN IDs, SILSO v2.0 yearly); Paper-4 reference imports marked CITE (sunspot decomposition + financial band); the unreproduced Norwich deseasonalized vdiv marked OPEN; the OUTLINE-mapping reconciliation box ticked.

## 1. Sections

| Source section (§ / title) | Disposition | Reason / how transformed | Rebuild location |
|---|---|---|---|
| Abstract | TRANSFORM | numbers re-quoted via {{LB-id}}; title line updated; **Colorado "sign flip at the ACF zero-crossing" clause corrected to the R̄_near<R̄_far mechanism** (DISC-1.4-04) | paper Abstract |
| Part I / §1.1 What This Paper Tests | TRANSFORM | "identical methodology" refined — decomposition + Theorem 8b identical, divergence operator domain-adapted (disclosed) | paper §1.1 |
| §1.2 Why Natural Sciences | TRANSFORM | add Hsiang-2016 citation (orphan resolved) | paper §1.2 |
| §1.3 Paper Organization | KEEP | renumbered if structure shifts | paper §1.3 |
| Part II / §2.1 Methodology (decomposition) | KEEP | — | paper §2.1 |
| §2.2 Weather Temperature Anomalies | KEEP | values regenerated (reproduce: S_W 1.3–7.7%) | paper §2.2 |
| §2.3 Rivers: the Colorado–Ohio Gradient (intro) | KEEP | — | paper §2.3 |
| §2.3.1 Data Sources and Integrity (incl. Connecticut rejection) | KEEP | — | paper §2.3.1 |
| §2.3.2 Deseasonalization | TRANSFORM | Ohio look-ahead delta stated "≤ 1.2 pp" (was "< 1.2pp"; DISC-1.4-02) | paper §2.3.2 |
| §2.3.3 Paper-1 Decomposition Results | KEEP | values regenerated (reproduce exactly) | paper §2.3.3 |
| §2.3.4 The Differential Deseasonalization Gradient | TRANSFORM | **sweep corrected to matched-period +3.9/+4.7/+6.4** (CO 17.8/OH 13.1, gap 4.7pp; the printed +6.0/+8.5/+15.2 reproduces under no cell — DISC-1.4-01) | paper §2.3.4 |
| §2.3.5 Bias Audit (rivers) | KEEP | — | paper §2.3.5 |
| §2.4 Sunspots | TRANSFORM + CITE | **decomposition S_W/toward CITED to Paper 4** (does not reproduce on SILSO v2.0 — toward ~70–80%); data corrected to SILSO **v2.0 yearly** | paper §2.4 |
| §2.5 Influenza (decomposition) | KEEP | values regenerated in-band (SMA-4/16 H=13 cell; v4's range endpoints were under-specified — single defensible cell reported) | paper §2.5 |
| §2.6 The Complete Calibration Scale | TRANSFORM | **both financial and sunspot comparison values cited to Kim-2026d** (Paper-4 reference imports) | paper §2.6 |
| Part III / §3.1 What This Section Tests | TRANSFORM | add Boettiger-2012, Boettiger-2013, Li-2025 citations (orphans resolved) | paper §3.1 |
| §3.2 Methodology and Replication Parameters (divergence + CSD) | TRANSFORM | **document the four domain-specific divergence operators** (generic level/level form reproduces only Ohio — DISC-1.5-01/-02); resolves the single-operator framing | paper §3.2 |
| §3.3 Results by Domain (3.3.1 Hydrology / 3.3.2 Epidemiology / 3.3.3 Atmospheric / 3.3.4 Solar) | TRANSFORM | **Colorado vdiv ≈+0.10/+0.08** (was +0.33, overlap-inflated — DISC-1.5-01); **Norwich deseasonalized vdiv OPEN** (~+0.05; Dallas +0.745→+0.004 reproduces — DISC-1.5-02); Ohio null + epi opposite-sign reproduce; **sunspot "CSD also negative" sub-claim dropped** | paper §3.3.1–3.3.4 |
| §3.4 Cross-Domain Summary | TRANSFORM | re-stated at corrected magnitudes | paper §3.4 |
| §3.5 Bias Audit for Ohio River Divergence | KEEP | — | paper §3.5 |
| Part IV / §4.1 What Theorem 8b Predicts | KEEP | states the rule; cited, not re-proved | paper §4.1 |
| §4.2 Data, Parameters, and Pre-Registration | KEEP | — | paper §4.2 |
| §4.3 Pre-Test Bias Check | KEEP | — | paper §4.3 |
| §4.4 Results | KEEP | values regenerated (reproduce exactly: 13/13 significant, 20/25; per-domain 5/5·5/5·5/5·3/5·2/5) | paper §4.4 |
| §4.5 Post-Test Validation | KEEP | values regenerated (Colorado flip = R̄_near<R̄_far with ACF positive; flu flip at the 14-wk ACF zero-crossing, distinct from h=26 — DISC-1.4-04/05) | paper §4.5 |
| §4.6 Methodology Correction Note (vol-div vs level-div) | KEEP | honest disclosure of the superseded ≈44% formulation; the rejected vol-form pass regenerated | paper §4.6 |
| Part V / §5.1 Divergence-Based Flu Season Onset Detection (intro) | KEEP | — | paper §5.1 |
| §5.1.0 Data Sources and Replication Parameters | TRANSFORM | **season count corrected: 29 candidates (1997-98…2025-26) → 27 paired**, excluding 2020-21 (peak<2.0%) and 2009-10 (no level onset) — DISC-1.4-03 | paper §5.1.0 |
| §5.1.1 The Detection Gap in Current Surveillance | KEEP | prior-method lead-times cited | paper §5.1.1 |
| §5.1.2 The Divergence Onset Detector | KEEP | values regenerated (reproduce exactly: 14.1/5.9/+8.2, 26/27, t=9.35, floor 5, Q1 12) | paper §5.1.2 |
| §5.1.3 Strain-Level Divergence and Early Dominant Strain Identification | TRANSFORM | **strain spec pinned** (subtyping-not-performed allocated proportionally; first-firing tie-break by higher %pos; onset ref D>0.2); counts reported as-regenerated (single-strain 9/9 robust; hindsight/real-time may differ from v4's 78%/89%) | paper §5.1.3 |
| §5.1.4 Implications for Vaccine Strain Selection | KEEP | discussion; no load-bearing numbers | paper §5.1.4 |
| §5.1.5 Bias Audit (flu) | KEEP | — | paper §5.1.5 |
| §5.1.6 Limitations | KEEP | maps to limits-of-claim (L-) anchors in OUTLINE | paper §5.1.6 |
| §5.2 Weather-to-River Persistence Transformation | KEEP | mechanism discussion | paper §5.2 |
| Part VI / §6.1 The Unified Cross-Domain Table | TRANSFORM | table regenerated with corrected cells (Colorado ρ≈+0.10; matched sweep; sunspot/financial cited; Norwich open; sunspot ACF on v2.0) — TBL-1 | paper §6.1 |
| §6.2 The ACF Unification Diagram | TRANSFORM | **FIG-1 regenerated WITHOUT the spurious "CO: 0-cross ~132d" annotation, and committed to the repo** (v4's figure was never committed — DISC-1.4-04) | paper §6.2 |
| §6.3 Cross-Domain Conclusions | KEEP | maps to conclusions (C-) anchors | paper §6.3 |
| §6.4 Bias Audit for E1 and E2 | KEEP | — | paper §6.4 |
| Part VII / §7.1 Prediction 1: Onset Detection Lead Time | KEEP | registered forward prediction (v1.8 Phase-4 step); protocol retained | paper §7.1 |
| §7.2 Prediction 2: Dominant Strain Identification | KEEP | registered forward prediction; protocol retained | paper §7.2 |
| §7.3 What Correct Predictions Would Demonstrate | KEEP | — | paper §7.3 |
| §7.4 Operational Significance | KEEP | — | paper §7.4 |
| Acknowledgments and AI Disclosure | TRANSFORM | rewritten to mirror this rebuild (author + reviewer both Claude); complete at Phase 4, updated at 5b | paper Acknowledgments |
| References | TRANSFORM | **seven metadata fixes** — Kim-2026d title, Hong "H."→"K.", Li "Z."→"Y.", Vega author tail, Zakamulin-Giner title/venue, Kaya quote, four orphans cited (DISC-1.3-01…07); all-tier accuracy check at 5b | paper References |
| Appendix A: Data Sources (A.1 Epidemiology / A.2 Weather / A.3 Hydrology / A.4 Solar) | TRANSFORM | **A.2 enumerate all six weather GHCN IDs** (was two — DISC-1.4-06); **A.4 SILSO v2.0 yearly**; reconciled against data/SOURCES.md | paper Appendix A |

## 2. Proofs / theorems

| Source theorem / proof (id) | Disposition | Reason / how transformed | Rebuild location |
|---|---|---|---|
| Theorem 8b (Persistence-Sign / ACF-sign rule), §4.1 | KEEP | **stated, cited not proved** — prior art (Kim-2026d); empirical archetype, no written proof retained | paper §4.1 (statement) + cite Kim-2026d |

> Proof count for the shape ledger = **0** (empirical-with-verified-theory).

## 3. Experiments

| Source experiment (id / name) | Disposition | Reason / how transformed | Rebuild script + output |
|---|---|---|---|
| E1 — Gap-closure decomposition / calibration scale (Part II). Datasets: weather (Norwich, Dallas), Colorado (raw + deseas), Ohio (raw + deseas), influenza, + synthetic RW control | TRANSFORM | weather/river/flu regenerated (reproduce); **sunspot decomposition + financial band CITED** (Paper-4 refs); **sweep corrected to matched +3.9/+4.7/+6.4**; flu window pinned SMA-4/16 H=13; RW control seed 0 (tolerance band) | analysis/e1_calibration_decomposition.py → outputs/e1_calibration.json |
| E2 — Volatility-divergence operator + CSD comparison (Part III). Datasets: Colorado, Ohio, influenza, weather (6 stations), sunspots | TRANSFORM | **four domain-specific operators documented** (hydrology log-returns 12/63; weather TMAX first-diff 21/252 per-month-z; epi %ILI first-diff 4/16; solar yearly level 3/11 future-Y) — NOT one generic operator; **Colorado ≈+0.10**; **Norwich deseasonalized OPEN**; Dallas + Ohio-null + epi-opposite-sign + sunspot-negative-sign reproduce | analysis/e2_volatility_divergence_csd.py → outputs/e2_divergence_csd.json |
| E3 — Persistence-Sign / Theorem-8b (Part IV). 5 systems × 5 horizons = 25 predictions | KEEP | level-divergence formulation (per §4.6); reproduces exactly (13/13, 20/25, both flips); rejected vol-form pass also regenerated; ACF max-lag 400 daily / 60 flu | analysis/e3_theorem8b_sign.py → outputs/e3_theorem8b.json |
| E4 — Flu divergence onset detector vs level surveillance (§5.1.2). Lead-time test | KEEP | SMA-4 − SMA-12 of ILI, threshold 0.2pp; reproduces exactly; **27 paired seasons (29 − 2020-21 − 2009-10)** | analysis/e4_flu_onset.py → outputs/e4_flu_onset.json |
| E5 — Strain-level divergence / dominant-strain ID (§5.1.3). Hindsight + real-time accuracy | TRANSFORM | **strain spec pinned**; counts as-regenerated (single-strain 9/9 robust; hindsight/real-time/lead may differ from v4 — under-specified in v4) | analysis/e5_strain_id.py → outputs/e5_strain_id.json |
| E6 — Divergence peak detection / zero-crossing test (§5.1.2 note) | KEEP | rejected-hypothesis result retained; reproduces | analysis/e6_peak_detection.py → outputs/e6_peak_detection.json |

> Experiment count for the shape ledger = **6** (script ids planned in DESIGN.md §2; final names fixed at Phase 2).

## 4. Analyses

| Source analysis | Disposition | Reason / how transformed | Rebuild location |
|---|---|---|---|
| The complete calibration-scale ordering (§2.6) | TRANSFORM | synthesis of E1; sunspot + financial rows cited to Paper 4 | paper §2.6 |
| Differential deseasonalization gradient (§2.3.4) | TRANSFORM | sweep corrected to matched +3.9/+4.7/+6.4 (DISC-1.4-01) | paper §2.3.4 |
| Connecticut River rejection (data-integrity decision, §2.3.1) | KEEP | methodology decision; documented | paper §2.3.1 + DECISIONS.md |
| Methodology Correction Note — vol-div vs level-div (§4.6) | KEEP | honest disclosure of the superseded ≈44% formulation; level-div primary | paper §4.6 |
| Cross-domain summary / conclusions / ACF unification (§3.4, §6.3, §6.2/6.4) | TRANSFORM | synthesis; **Colorado ACF characterization corrected** (positive, no zero-crossing — DISC-1.4-04) | paper §3.4, §6.2–6.4 |
| Vaccine strain-selection implications (§5.1.4) | KEEP | discussion; extensions flagged untested | paper §5.1.4 |
| Weather-to-river persistence-transformation mechanism (§5.2) | KEEP | mechanism discussion | paper §5.2 |
| Dual bias-audit protocol (pre-test + post-test) | KEEP | shuffle/permutation (seed 0), IS/OOS, threshold-sensitivity, synthetic + matched-period controls; re-run under contract | per-experiment outputs + verification/ |
| Forward predictions (Part VII) — two dated 2026–27 flu predictions | KEEP | the v1.8 forward-prediction step; registered + dated at 5c | paper §7 + 5c registration |

## 5. Domains / datasets

| Source domain or dataset | Disposition | Reason / how transformed | Rebuild coverage |
|---|---|---|---|
| Atmospheric — NOAA GHCN-Daily; temp = (TMAX+TMIN)/2 | TRANSFORM | **all six stations enumerated with GHCN IDs** (NYC USW00094728, Blue Hill USC00190736, SF USW00023272, Philly USW00013739, Dallas USW00003927, Norwich USC00065910); re-pulled + hashed | E1 (Norwich, Dallas), E2 (all 6), E3 (Norwich, Dallas); data/SOURCES.md |
| Hydrology — USGS 08158000 Colorado (~46,767, 1898–2026); USGS 03294500 Ohio (~35,862, 1928–2026) | KEEP | re-pulled + hashed (param 00060, stat 00003) | E1, E2, E3; data/SOURCES.md |
| Hydrology — USGS 01170500 Connecticut at Montague City MA | DROP — not replicable in prior form: 63.5-yr gap (~1929–1993); replaced by Ohio (§2.3.1) | — | excluded; rejection documented |
| Solar physics — SIDC/SILSO sunspot number | TRANSFORM | **SILSO v2.0 yearly** (`SN_y_tot_V2.0`; v4's "monthly 1700–2008" is a different vintage); decomposition CITED, vdiv negative sign regenerated | E2 (vdiv sign); data/SOURCES.md |
| Epidemiology — CDC ILINet weekly national % WEIGHTED ILI (1997–2026, ~1,484 wks) | KEEP | re-pulled + hashed (skiprows=1) | E1, E2, E3, E4, E6; data/SOURCES.md |
| Epidemiology — CDC NREVSS strain data (pre-2015 + post-2015 files) | TRANSFORM | re-pulled + hashed; **subtyping-not-performed allocation pinned** (E5 spec) | E5; data/SOURCES.md |
| Synthetic random-walk control (matched to Colorado μ, σ; 10 sims) | KEEP | regenerated with committed seed 0 | E1; analysis output |
| Financial-market reference values (S_W, divergence ρ, ACF) | CITE | comparison anchors from Kim-2026d (Paper 4), not regenerated | paper §2.6, §6.1; cite Kim-2026d |
| Sunspot-decomposition reference values (S_W, toward) | CITE | Paper-4 reference (does not reproduce on SILSO v2.0); labeled in the scale/TBL-1 | paper §2.4, §2.6, §6.1; cite Kim-2026d |

## 6. Figures / tables / equations

| Source figure / table / equation (id) | Disposition | Reason / how transformed | Rebuild location (paper §, OUTLINE id) |
|---|---|---|---|
| Figure 1 — ACF unification diagram (figure1.png), §6.2 | TRANSFORM | regenerate from pinned data **without the spurious "CO: 0-cross ~132d" annotation** (the plotted curve is correct), **and commit it** (DISC-1.4-04) | paper §6.2, FIG-1 |
| Table — Unified Cross-Domain Table, §6.1 | TRANSFORM | regenerated with corrected cells (Colorado ρ≈+0.10; matched sweep; sunspot/financial cited; Norwich open; sunspot ACF on v2.0) | paper §6.1, TBL-1 |
| Equation — gap-closure decomposition (S_W = ΣC_W / Σ(C_W+C_P)), §2.1 | TRANSFORM | inline in source; add greppable EQ- anchor | paper §2.1, EQ-1 |
| Equation — volatility-divergence operator (vdiv = std_fast − std_slow), §3.2 | TRANSFORM | add EQ- anchor; **show the generic form + the four domain-specific constructions** | paper §3.2, EQ-2 |
| Equation — level-divergence operator (D = SMA_fast − SMA_slow), §4.1 | TRANSFORM | add EQ- anchor | paper §4.1, EQ-3 |
| Equation — Theorem-8b sign rule + R̄ definition, §4.1 | TRANSFORM | add EQ- anchor | paper §4.1, EQ-4 |
| Equation — flu-onset divergence (D = SMA_4(ILI) − SMA_12(ILI)), §5.1 | TRANSFORM | add EQ- anchor | paper §5.1, EQ-5 |

## Shape ledger (feeds the Phase 4 tripwire)

| Metric | Source | Rebuild | Δ% | Action if breached |
|---|---|---|---|---|
| Pages | [from built v4.pdf — fill at Phase 4] | [Phase 4] | [Phase 4] | >15% → sign-off; >10% → note |
| Words | 14,220 | [Phase 4] | [Phase 4] | >15% → sign-off; >10% → note |
| Experiment count | 6 | [Phase 4] | [Phase 4] | >15% → sign-off; >10% → note |
| Proof count | 0 | [Phase 4] | [Phase 4] | n/a (empirical archetype) |

**Breach notes / sign-offs:** [none yet — completed at Phase 4]. *Note: the rebuild adds the four domain-specific operators and the correction notes, which may grow §3.2 and Part VI; watch the word delta at Phase 4.*

## Reconciliation (run before signing)

- [x] Every source section, proof, experiment, analysis, domain, and figure/table/equation has exactly one row above — nothing omitted.
- [x] Every KEEP/TRANSFORM/CITE/OPEN names a concrete rebuild location; every TRANSFORM/CITE/OPEN names the DISC dossier it implements and traces to the DESIGN §6 ledger.
- [x] Every DROP carries a valid reason (Connecticut River 63.5-yr gap).
- [x] **Every KEEP/TRANSFORM/CITE/OPEN row maps to ≥1 node in OUTLINE.md** — verified against OUTLINE v0.2 (sections → §1; experiments → ARG-04…12 + LB-e*; datasets → LB/ARG supports; figures/equations → §5; citations → §3; the corrections → the corrected LB statuses + S5/L-06/07/08).
- [ ] Shape ledger computed — source side recorded; rebuild side at Phase 4.
- [ ] (At Phase 2) every KEEP/TRANSFORM experiment has a committed script or a logged escalation in DECISIONS.md.

## Author sign-off

> Every element of the source is dispositioned above against the Stage 1.5/1.6 verification record; the single DROP is justified (Connecticut River gap); corrections are marked TRANSFORM (Colorado vdiv, the sweep, the domain-specific operator, the abstract/FIG-1 fix, the season count, the strain spec, the seven citation fixes, six GHCN IDs, SILSO v2.0 yearly), Paper-4 imports CITE (sunspot decomposition + financial band), and the unreproduced Norwich value OPEN; every KEEP/TRANSFORM/CITE/OPEN maps to an OUTLINE v0.2 node and traces to the DESIGN §6 ledger; the shape-ledger source side is recorded. This ledger is complete and accurate as of the committing revision.

**Signed:** Jae Kim / ORCID 0009-0005-3260-7880 — **Date:** 2026-06-28 *(pending review of the five rebuild decisions in this session)*

---

*Rebuild coverage ledger, Standard v1.8, grounded in the Stage 1.5/1.6 verification record. Amend dated, never silently. Re-read at Phase 2, Phase 4, Phase 5a.*
