# COVERAGE.md — Rebuild Coverage Ledger

The Phase-1 gate that accounts for every element of the source so nothing vanishes silently into the rebuild. Read again at Phase 2 (execution), Phase 4 (shape gate), and Phase 5a (reviewer completeness). Every KEEP/TRANSFORM row maps to a node in OUTLINE.md. Default disposition is **restore-and-verify** (KEEP); a DROP is valid only as "not necessary — why" or "not replicable in prior form — why."

## Metadata

- **Rebuild paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
- **Source artifact:** `C:\Users\jaek9\Documents\Repos\lagging-truth-paper-05\paper\Paper5_Final_Natural_Sciences_Validation_v4.md` — MD5 `23428fb275f6ea6d6a3846fc17d91a86` / SHA256 `982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50` (pinned — "source material, not inherited results"). Supporting assets (figure1.png, 8 reference PDFs, companion, build chain) at `C:\Users\jaek9\Documents\LaggingTruth\05-13-2026\Paper 5\`.
- **Archetype:** empirical-with-verified-theory
- **Author:** Jae Kim / ORCID 0009-0005-3260-7880
- **Standard:** v1.8
- **Status:** draft — 2026-06-28

> Disposition convention for this rebuild: the goal is to reproduce the paper faithfully and re-verify every number under the contract. Almost everything is **KEEP** in substance; every load-bearing number is **regenerated** by a committed Phase-2 script (KEEP of the result, new provenance) — that regeneration is not a content change. **TRANSFORM** marks a knowing change (title/front-matter, an added greppable anchor, a re-scoped or corrected computation). No element is dropped without explicit cause; none is dropped here.

## 1. Sections

| Source section (§ / title) | Disposition | Reason / how transformed | Rebuild location |
|---|---|---|---|
| Abstract | KEEP | numbers re-quoted from the ledger via {{LB-id}}; title line updated | paper Abstract |
| Part I / §1.1 What This Paper Tests | KEEP | — | paper §1.1 |
| §1.2 Why Natural Sciences | KEEP | — | paper §1.2 |
| §1.3 Paper Organization | KEEP | renumbered if structure shifts | paper §1.3 |
| Part II / §2.1 Methodology (decomposition) | KEEP | — | paper §2.1 |
| §2.2 Weather Temperature Anomalies | KEEP | values regenerated | paper §2.2 |
| §2.3 Rivers: the Colorado–Ohio Gradient (intro) | KEEP | — | paper §2.3 |
| §2.3.1 Data Sources and Integrity (incl. Connecticut rejection) | KEEP | — | paper §2.3.1 |
| §2.3.2 Deseasonalization | KEEP | — | paper §2.3.2 |
| §2.3.3 Paper-1 Decomposition Results | KEEP | values regenerated | paper §2.3.3 |
| §2.3.4 The Differential Deseasonalization Gradient | KEEP | values regenerated | paper §2.3.4 |
| §2.3.5 Bias Audit (rivers) | KEEP | — | paper §2.3.5 |
| §2.4 Sunspots | KEEP | values regenerated; data re-pulled + hashed | paper §2.4 |
| §2.5 Influenza (decomposition) | KEEP | values regenerated | paper §2.5 |
| §2.6 The Complete Calibration Scale | KEEP | prose ordering; financial/sunspot comparison values cited to Kim-2026d | paper §2.6 |
| Part III / §3.1 What This Section Tests | KEEP | — | paper §3.1 |
| §3.2 Methodology and Replication Parameters (vol-divergence + CSD) | KEEP | — | paper §3.2 |
| §3.3 Results by Domain (3.3.1 Hydrology / 3.3.2 Epidemiology / 3.3.3 Atmospheric / 3.3.4 Solar) | KEEP | values regenerated | paper §3.3.1–3.3.4 |
| §3.4 Cross-Domain Summary | KEEP | values regenerated | paper §3.4 |
| §3.5 Bias Audit for Ohio River Divergence | KEEP | — | paper §3.5 |
| Part IV / §4.1 What Theorem 8b Predicts | KEEP | states the rule; cited, not re-proved | paper §4.1 |
| §4.2 Data, Parameters, and Pre-Registration | KEEP | — | paper §4.2 |
| §4.3 Pre-Test Bias Check | KEEP | — | paper §4.3 |
| §4.4 Results | KEEP | values regenerated | paper §4.4 |
| §4.5 Post-Test Validation | KEEP | values regenerated | paper §4.5 |
| §4.6 Methodology Correction Note (vol-div vs level-div) | KEEP | honest-disclosure of the superseded formulation; retained | paper §4.6 |
| Part V / §5.1 Divergence-Based Flu Season Onset Detection (intro) | KEEP | — | paper §5.1 |
| §5.1.0 Data Sources and Replication Parameters | KEEP | — | paper §5.1.0 |
| §5.1.1 The Detection Gap in Current Surveillance | KEEP | prior-method lead-times cited | paper §5.1.1 |
| §5.1.2 The Divergence Onset Detector | KEEP | values regenerated | paper §5.1.2 |
| §5.1.3 Strain-Level Divergence and Early Dominant Strain Identification | KEEP | values regenerated | paper §5.1.3 |
| §5.1.4 Implications for Vaccine Strain Selection | KEEP | discussion; no load-bearing numbers | paper §5.1.4 |
| §5.1.5 Bias Audit (flu) | KEEP | — | paper §5.1.5 |
| §5.1.6 Limitations | KEEP | maps to limits-of-claim (L-) anchors in OUTLINE | paper §5.1.6 |
| §5.2 Weather-to-River Persistence Transformation | KEEP | mechanism discussion | paper §5.2 |
| Part VI / §6.1 The Unified Cross-Domain Table | KEEP | table regenerated (TBL-1) | paper §6.1 |
| §6.2 The ACF Unification Diagram | KEEP | figure regenerated (FIG-1) | paper §6.2 |
| §6.3 Cross-Domain Conclusions | KEEP | maps to conclusions (C-) anchors | paper §6.3 |
| §6.4 Bias Audit for E1 and E2 | KEEP | — | paper §6.4 |
| Part VII / §7.1 Prediction 1: Onset Detection Lead Time | KEEP | the registered forward prediction (v1.8 Phase-4 step); protocol retained | paper §7.1 |
| §7.2 Prediction 2: Dominant Strain Identification | KEEP | registered forward prediction; protocol retained | paper §7.2 |
| §7.3 What Correct Predictions Would Demonstrate | KEEP | — | paper §7.3 |
| §7.4 Operational Significance | KEEP | — | paper §7.4 |
| Acknowledgments and AI Disclosure | TRANSFORM | rewritten to mirror what was actually done in this rebuild (author + reviewer both Claude); complete at Phase 4, updated at 5b | paper Acknowledgments |
| References | KEEP | every entry carried; all-tier accuracy check at 5b; presence enforced by OUTLINE §3 | paper References |
| Appendix A: Data Sources and Specifications (A.1 Epidemiology / A.2 Weather / A.3 Hydrology / A.4 Solar) | KEEP | reconciled against data/SOURCES.md (exact identifiers + hashes) | paper Appendix A |

## 2. Proofs / theorems

| Source theorem / proof (id) | Disposition | Reason / how transformed | Rebuild location |
|---|---|---|---|
| Theorem 8b (Persistence-Sign / ACF-sign rule), §4.1 | KEEP | **stated, cited not proved** — prior art (Kim-2026d); empirical archetype, no written proof retained in this paper | paper §4.1 (statement) + cite Kim-2026d |

> Proof count for the shape ledger = **0** (empirical-with-verified-theory: this paper proves no theorems of its own; the one theorem it uses is cited).

## 3. Experiments

| Source experiment (id / name) | Disposition | Reason / how transformed | Rebuild script + output |
|---|---|---|---|
| E1 — Gap-closure decomposition / calibration scale (Part II). Operator: Paper-1 S_W decomposition. Datasets: weather (Norwich, Dallas), Colorado (raw + deseasonalized), Ohio (raw + deseasonalized), sunspots, influenza, + synthetic random-walk control | KEEP | same operator; all values regenerated; data re-pulled + hashed | analysis/e1_decomposition.py → outputs/e1.json |
| E2 — Volatility-divergence operator + CSD comparison (Part III). Datasets: Colorado (raw + deseas), Ohio (raw + deseas), influenza, weather (Norwich + Dallas), sunspots | KEEP | same operator (fast/slow trailing std; AR(1) CSD comparator); values regenerated | analysis/e2_vdiv_csd.py → outputs/e2.json |
| E3 — Persistence-Sign / Theorem-8b sign prediction (Part IV). 5 systems (Colorado-deseas, Ohio-deseas, Norwich, Dallas, flu) × 5 pre-registered horizons = 25 predictions | KEEP | level-divergence formulation (the corrected one per §4.6); values regenerated | analysis/e3_persistence_sign.py → outputs/e3.json |
| E4 — Flu divergence onset detector vs level-based surveillance (Part V §5.1.2). 27 seasons; lead-time test | KEEP | same operator (SMA_4 − SMA_12 of ILI, threshold 0.2pp); values regenerated | analysis/e4_flu_onset.py → outputs/e4.json |
| E5 — Strain-level divergence / dominant-strain identification (Part V §5.1.3). 27 seasons; hindsight + real-time accuracy | KEEP | same operator on per-subtype percent-positive; values regenerated | analysis/e5_strain_id.py → outputs/e5.json |
| E6 — Divergence peak detection / zero-crossing test (Part V §5.1.2 note). Peak-lag comparison vs SMA-4 peak | KEEP | rejected-hypothesis result retained for honest disclosure; values regenerated | analysis/e6_peak_detection.py → outputs/e6.json |

> Experiment count for the shape ledger = **6** (rebuild script ids are planned in DESIGN.md; final names fixed at Phase 2).

## 4. Analyses

Analytical content that is not a standalone experiment.

| Source analysis | Disposition | Reason / how transformed | Rebuild location |
|---|---|---|---|
| The complete calibration-scale ordering (§2.6) | KEEP | synthesis of E1 across domains | paper §2.6 |
| Differential deseasonalization gradient (§2.3.4) — corroborates Paper-4 Ohio-collapse finding | KEEP | derived from E1/E2 outputs | paper §2.3.4 |
| Connecticut River rejection (data-integrity decision, §2.3.1) | KEEP | methodology decision; documented | paper §2.3.1 + DECISIONS.md |
| Methodology Correction Note — vol-divergence vs level-divergence for Theorem 8b (§4.6) | KEEP | honest disclosure of the superseded 44%-formulation; both reported, level-div primary | paper §4.6 |
| Cross-domain summary / conclusions / ACF unification (§3.4, §6.3, §6.2/6.4) | KEEP | synthesis | paper §3.4, §6.2–6.4 |
| Vaccine strain-selection implications (§5.1.4) | KEEP | discussion; mRNA/Southern-Hemisphere extensions flagged as untested | paper §5.1.4 |
| Weather-to-river persistence-transformation mechanism (§5.2) | KEEP | mechanism discussion | paper §5.2 |
| Dual bias-audit protocol (pre-test + post-test) — §2.3.5, §3.5, §4.3/4.5, §5.1.5, §6.4 | KEEP | shuffle/permutation, IS/OOS, threshold-sensitivity, synthetic + matched-period controls; re-run under contract | per-experiment outputs + verification/ |
| Forward predictions (Part VII) — two dated 2026–27 flu predictions with replication protocols | KEEP | the v1.8 forward-prediction step; registered publicly + dated at 5c | paper §7 + 5c registration |

## 5. Domains / datasets

| Source domain or dataset | Disposition | Reason / how transformed | Rebuild coverage |
|---|---|---|---|
| Atmospheric science — NOAA daily, Norwich CT (NORWICH PUBLIC UTILITY PLANT) + Dallas TX (DAL FTW WSCMO AIRPORT); temp = (TMAX+TMIN)/2 | KEEP | re-pulled + hashed | E1, E2, E3; data/SOURCES.md |
| Hydrology — USGS 08158000 Colorado nr Austin TX (~46,767 daily, 1898–2026); USGS 03294500 Ohio at Louisville KY (~35,862 daily, 1928–2026) | KEEP | re-pulled + hashed | E1, E2, E3; data/SOURCES.md |
| Hydrology — USGS 01170500 Connecticut at Montague City MA | DROP — not replicable in prior form: 63.5-yr record gap (~1929–1993) fails data-integrity; replaced by Ohio (documented in §2.3.1) | — | excluded; rejection documented |
| Solar physics — SIDC/SILSO monthly mean sunspot number | KEEP | re-pulled + hashed; range reconciled to Appendix A.4 | E1, E2, E3; data/SOURCES.md |
| Epidemiology — CDC ILINet weekly national % WEIGHTED ILI (1997–2026, ~1,484 wks) | KEEP | re-pulled + hashed | E1, E2, E3, E4, E6; data/SOURCES.md |
| Epidemiology — CDC NREVSS strain data (ICL_NREVSS_Combined_prior_to_2015_16.csv + ICL_NREVSS_Public_Health_Labs.csv) | KEEP | re-pulled + hashed | E5; data/SOURCES.md |
| Synthetic random-walk control (matched to Colorado μ, σ; 10 sims × ~46,767 obs) | KEEP | regenerated with committed seed | E1; analysis output |
| Financial-market reference values (S_W, divergence ρ, ACF) | KEEP | **cited** comparison anchors from Kim-2026d (Paper 4), not regenerated here — prior-art citation, not a load-bearing computation of this paper | paper §2.6, §6.1; cite Kim-2026d |

## 6. Figures / tables / equations

| Source figure / table / equation (id) | Disposition | Reason / how transformed | Rebuild location (paper §, OUTLINE id) |
|---|---|---|---|
| Figure 1 — ACF unification diagram (figure1.png), §6.2 | KEEP | regenerated from pinned data by a committed plotting script | paper §6.2, FIG-1 |
| Table — Unified Cross-Domain Table, §6.1 | KEEP | regenerated; all cells from the ledger | paper §6.1, TBL-1 |
| Equation — gap-closure decomposition (S_W = ΣC_W / Σ(C_W+C_P)), §2.1 | TRANSFORM | inline in source; add greppable EQ- anchor for the gate | paper §2.1, EQ-1 |
| Equation — volatility-divergence operator (vdiv = std_fast − std_slow), §3.2 | TRANSFORM | add EQ- anchor | paper §3.2, EQ-2 |
| Equation — level-divergence operator (D = SMA_fast − SMA_slow), §4.1 | TRANSFORM | add EQ- anchor | paper §4.1, EQ-3 |
| Equation — Theorem-8b sign rule (sign[Corr(D_t,Y_{t+h})] = sign[R̄_near − R̄_far]) + R̄ definition, §4.1 | TRANSFORM | add EQ- anchor | paper §4.1, EQ-4 |
| Equation — flu-onset divergence (D = SMA_4(ILI) − SMA_12(ILI)), §5.1 | TRANSFORM | add EQ- anchor | paper §5.1, EQ-5 |

## Shape ledger (feeds the Phase 4 tripwire)

Filled at Phase 4 against the rebuild draft; source side recorded now.

| Metric | Source | Rebuild | Δ% | Action if breached |
|---|---|---|---|---|
| Pages | [from built v4.pdf — fill at Phase 4] | [Phase 4] | [Phase 4] | >15% → sign-off; >10% → note |
| Words | 14,220 | [Phase 4] | [Phase 4] | >15% → sign-off; >10% → note |
| Experiment count | 6 | [Phase 4] | [Phase 4] | >15% → sign-off; >10% → note |
| Proof count | 0 | [Phase 4] | [Phase 4] | n/a (empirical archetype) |

**Breach notes / sign-offs:** [none yet — completed at Phase 4]

## Reconciliation (run before signing)

- [x] Every source section, proof, experiment, analysis, domain, and figure/table/equation has exactly one row above — nothing omitted.
- [x] Every KEEP / TRANSFORM names a concrete rebuild location (experiment id, paper §, appendix, or file).
- [x] Every DROP carries a valid reason ("not replicable in prior form" — Connecticut River 63.5-yr gap).
- [ ] **Every KEEP / TRANSFORM row maps to ≥1 node in OUTLINE.md** — *pending: OUTLINE.md is the next Phase-1 deliverable; this box is ticked when the outline is committed and the mapping is verified.*
- [ ] Shape ledger computed — *source side recorded; rebuild side at Phase 4.*
- [ ] (At Phase 2) every KEEP / TRANSFORM experiment has a committed script or a logged escalation in DECISIONS.md.

## Author sign-off

> Every element of the source is dispositioned above; the single DROP is justified as "not replicable in prior form" (Connecticut River record gap); every KEEP/TRANSFORM maps to an OUTLINE.md node (verified at outline commit); the shape ledger source side is recorded and the rebuild side is completed at Phase 4. This ledger is complete and accurate as of the committing revision.

**Signed:** Jae Kim / ORCID 0009-0005-3260-7880 — **Date:** 2026-06-28

---

*Rebuild coverage ledger, Standard v1.8. Amend dated, never silently. Re-read at Phase 2, Phase 4, Phase 5a.*
