# Discrepancy Register — Cross-Domain Validation

Single home for every discrepancy found in verification that cannot be immediately and trivially explained (Pre-Print Review Protocol Appendix B; carried under Standard v1.8). One dossier per issue; the Register is auditable and is the build instruction for the correction/Phase-4 work.

- **Paper:** Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology
- **Created:** 2026-06-28 (opened at the first Phase-2 discrepancy crossing the "cannot be immediately and trivially explained" threshold; the rebuild's pre-fix dispositions DISC-1.3…1.5 live in DESIGN §6 and are not re-dossiered here).

## Dossier format

Each dossier records: **identifier**; **discrepancy as found** + the stage/experiment that found it; **kind** (computational / consistency-wording); **second-review validation status** (CONFIRMED / WITHDRAWN); **Step 1 — cascade map**; **Step 2 — method-recovery result + methods used** (+ the Computational Integrity Check where a value is disputed); **Step 3 — adjudication + specified fix**; **state** (OPEN at discovery → RESOLVED when the fix is specified; Phase-2/4 implements).

## Summary

| ID | Discrepancy (short) | Kind | 2nd review | State |
|---|---|---|---|---|
| D01 | Hydrology vdiv — v4's Colorado +0.33 is a look-ahead artifact (divergence correlated with its own contemporaneous fast vol); Ohio's +0.047 used the forward target, so the two rivers used different operators. Under either consistent operator Ohio ≥ Colorado; on the pre-registered returns operator Ohio is the strongest river signal | computational | CONFIRMED | RESOLVED |
| D02 | Solar CSD sub-claim — the "CSD also negative" sub-claim was dropped on two off-target values (+0.42 monthly operator; −0.257 forward-vol). Under the operator-matched comparison (CSD vs the vdiv's future-level target) it is −0.103: negative, lower magnitude than the vdiv's −0.230 → v4's sub-claim reproduces; retain it | computational | CONFIRMED | RESOLVED |

---

## D01 — Hydrology volatility-divergence operator & the Colorado-vs-Ohio contrast

**Discrepancy as found.** Phase 2, experiment E2 (`analysis/e2_volatility_divergence_csd.py`). The v4 manuscript reports a hydrology contrast — Colorado volatility-divergence ρ = +0.33 (a significant signal, attributed to reservoir-driven persistence) vs Ohio ρ = +0.047 (null) — and the rebuild's DESIGN §2 carried it forward under a domain-specific **log-returns** operator, recording "Ohio +0.047/+0.021 exact (returns op, null); Colorado ≈+0.10/+0.08 (returns op)." E2's regeneration shows the **returns** operator gives **Ohio +0.30** (a strong signal), not +0.047; the **+0.047 is the LEVEL-operator value**; and **+0.33 does not reproduce under the documented operator at all** — neither returns nor level, neither overlapping nor subsampled windows. The "Ohio null" and the Colorado-vs-Ohio contrast do not survive a consistently-applied operator. (Builds on DISC-1.5-01, which adjudicated only the Colorado magnitude — never the cross-river contrast, the Ohio operator mis-attribution, or the true provenance of +0.33.)

**Kind:** computational (a regeneration produced a different result; all three steps apply).

**Second-review validation status: CONFIRMED.** Dedicated isolated re-examination of this item alone: (1) v4 does state the contrast — source-recovered verbatim ("Colorado … ρ = +0.33 … reservoir storage creates genuine multi-month volatility persistence … Ohio … ρ = +0.047"); (2) the behaviour does differ — under every consistently-applied operator Ohio ≥ Colorado (level forward: −0.00 vs +0.047; returns forward: +0.12 vs +0.30), reproduced exactly in-repo (`e2_divergence_csd.json`) and against the original `repro_hydrology.py`; (3) the fix is exactly true and introduces no new inconsistency — E3 (the level-*divergence* sign test) is a different operator and still reproduces 5/5 for both rivers, and the stronger Ohio returns-signal is consistent with Ohio's higher seasonality (45.7% vs 15.5%, E1) producing more volatility events. Not a false positive.

**Step 1 — Cascade map** (everything that changes if the corrected analysis enters the paper):
- **DESIGN §2 E2** — hydrology operator row (Ohio +0.047 mis-filed under the returns operator); decision rule (2) ("deseasonalized Ohio null"); the block-shuffle and provenance notes. **DESIGN §6** — LB-7, LB-8, LB-9.
- **OUTLINE** — ARG-06 (vdiv "null where basin-averaging removes structure"); LB-e2-ohio-rho ("raw borderline; deseasonalized null"); scope condition S3 ("returns a null where … averaging … removes that structure"); limit-of-claim L-06 ("the qualitative Colorado-vs-Ohio contrast holds"); TBL-1 (Colorado/Ohio divergence column).
- **Interpretation echoes to reconcile when the manuscript is written (Phase 4), recorded here so they are not silently dropped:** ARG-03 ("rivers storage-dependent" physics prediction), ARG-05 ("genuine non-seasonal persistence (Colorado) from seasonal artifact (Ohio collapse)"; "corroborating Paper-4's Ohio finding"), ARG-09 / FIG-1 ("the ACF governs … failure modes"). These are E1/ACF nodes whose numbers reproduce; their interpretive wording must align with the corrected vdiv story (Ohio has ACF structure and signals under the returns operator — it is not a method failure).
- **Manuscript** — §3.3.1 (rivers), the abstract/conclusion hydrology sentences, §3.2 (operator definition).
- **E2 output** `analysis/outputs/e2_divergence_csd.json` (carries the 2×2 and the recovered v4 artifact).

**Step 2 — Method recovery (authoritative recovery + reproduced artifact).**
- **(8) Design-rationale framing gate** *(run first)* — v4's stated rationale is reservoir-driven, non-seasonal volatility persistence unique to the Colorado (raw +0.33 ≈ deseas +0.32). The disputed value is reached by an inadmissible route and the rationale is disconfirmed: the admissible sub-21 level op gives Colorado −0.00 (no persistence), and the un-regulated Ohio shows the *stronger* returns-op signal (+0.30 vs +0.12). The gate rejects both the +0.33 and the reservoir-uniqueness interpretation.
- **(1) Source recovery** [`wing_import_raw`, semantic pass] — recovered the v4 manuscript: Y = log-discharge (level), vdiv(t) = std(Y,w_f) − std(Y,w_s), Colorado +0.33/+0.32, Ohio +0.047, "same window spec" both rivers. Ground truth on the operator *family* (level, 12/63) and the vdiv *windows* — but the manuscript's "same window spec" refers to the vdiv windows, not the forward-target shift, which (per the reproduction below) differed between the two rivers.
- **(7 / 3) Convergent cross-validation + provenance triangulation** — the original `repro_hydrology.py` reproduces Ohio +0.047/+0.021 **exactly** under the level + forward operator and Colorado **~0.00** under the consistent sub-21 subsample; E2's level + forward op matches to the digit.
- **(5 / 6) Downstream inversion + bounded variant sweep** *(reconstruction grade; corroborated by an exact magnitude match)* — a variant sweep over {log, raw, deseasonalized} discharge × {forward 63/126/252, contemporaneous} targets located v4's +0.33 **precisely**: it is the divergence `vdiv = std(12) − std(63)` correlated with the **contemporaneous fast std(12)** — i.e. with the predictor's *own* fast-volatility term, with **no forward shift**. Reproduced at Spearman **+0.322 (raw log-discharge ≈ v4's +0.33)** and **+0.365 (deseasonalized ≈ v4's +0.32)**. The same buggy target applied to **Ohio** gives **+0.62**, not +0.047 — so v4 computed **Colorado with the contemporaneous target and Ohio with the forward target**: two different operators on the two rivers. Committed as code: `e2_divergence_csd.json → hydrology[*].v4_artifact_contemp_fast`.
- **Computational Integrity Check on v4's +0.33 — fails #4 (look-ahead):** the forward lag was not enforced; the "forward volatility" target was the contemporaneous std(12), which is a component of the predictor `std(12) − std(63)`, so the correlation is mechanical (the divergence is correlated with part of itself), not predictive. Apply a genuine forward target and Colorado collapses to ~0 across horizons (−0.014 to +0.024). **This is NOT CIC #5 (overlap/subsample)** — overlapping and subsampled windows are near-identical in all four hydrology cells (e.g. Colorado returns +0.105 overlap / +0.12 sub-21), so overlap inflates nothing; the initial overlap hypothesis was tested and refuted. The cross-river contrast additionally fails an **operator-consistency** check (the two rivers were not computed with the same target).
- **Result:** method recovery **succeeds** with a reproduced mechanism. v4 operator family = level/12/63; +0.33 = look-ahead artifact (divergence vs contemporaneous fast vol); +0.047 = the level + forward null; the pre-registered **returns + forward** operator gives Colorado +0.12 / Ohio +0.30.

**Step 3 — Adjudication: RECONSTRUCTION-CORRECT / ORIGINAL-IN-ERROR.** v4's +0.33 is an authentic-but-buggy value (CIC #4 look-ahead; the "forward" target was contemporaneous and is a sub-term of the predictor), not a genuine forward-predictive signal; and the Colorado-vs-Ohio contrast is an artifact of applying two different targets to the two rivers. Under any single consistently-applied operator the contrast vanishes (level + forward: both ~null) or reverses (returns + forward: both signal, Ohio stronger).

**Specified fix.**
1. Report the verified 2×2 (level vs returns, both rivers, forward target) — already in `e2_divergence_csd.json` — plus the recovered v4 artifact value for both rivers.
2. Reframe the hydrology finding (LB-7 / ARG-06 / §3.3.1): volatility-clustering is significant on the **returns** of both rivers (Ohio +0.30 > Colorado +0.12); the **level** operator (volatility confounded with the seasonal cycle) is ~null for both (Colorado −0.00, Ohio +0.047) — the operator choice, not the river, drives the apparent contrast.
3. Correct LB-8: Colorado +0.33 → look-ahead artifact (CIC #4: divergence vs contemporaneous fast vol; reproduced at +0.322); +0.12 returns / −0.00 level (DISC-1.5-01 + D01).
4. Rewrite LB-9: Ohio is null *only* under the level + forward op (+0.047, block-shuffle z < 2.0); under the pre-registered returns op it is +0.30 — the strongest hydrology signal. Drop "Ohio null" as a standalone claim; remove the reservoir-uniqueness interpretation.
5. State the cross-river inconsistency plainly in §3.3.1/abstract: the v4 "Colorado signal vs Ohio null" contrast came from computing the two rivers with different forward-target definitions, not from a real difference between the rivers.
6. Update OUTLINE S3 (the null is the level-op seasonal confound, not absent structure) and L-06 (the contrast does not hold — it reverses); flag the ARG-03/05/09 + FIG-1 interpretation echoes for Phase-4 reconciliation.
7. E2 addition (CIC #4 reproduction, self-contained): compute the contemporaneous-fast-target correlation for both rivers (`v4_artifact_contemp_fast`) so the repo reproduces v4's +0.33 (Colorado +0.322) and shows it disappears under a genuine forward target; retain the level-op overlap value as evidence that overlap is not the cause.
8. Dated DESIGN amendment (v0.3) recording all of the above.

**Standing rule 3 (resolved construction committed as code):** the operative construction is `analysis/e2_volatility_divergence_csd.py` (returns + level operators, forward target, sub-21, both rivers), extended with the recovered v4 look-ahead artifact (`v4_artifact_contemp_fast`); this dossier documents the *decision*, the committed script preserves the *executable construction* — both the corrected result and the reproduced bug.

**State: RESOLVED** (fix specified; Phase-2/4 implements). Discovered 2026-06-28; adjudicated 2026-06-28 (overlap hypothesis tested and refuted, then the look-ahead mechanism recovered and reproduced, same day).

---

## D02 — Solar CSD sign & target (the "CSD also negative" sub-claim)

**Discrepancy as found.** Phase 2, experiment E2 (`analysis/e2_volatility_divergence_csd.py`). DESIGN §2 / §6 LB-12 / OUTLINE L-08 record that v4's sunspot "CSD also negative" sub-claim does NOT reproduce on SILSO v2.0 (CSD +0.42, positive) and should be dropped. But E2 computes the solar CSD = −0.257 (negative) — contradicting that disposition: the printed value reproduces v4's claimed sign rather than refuting it.

**Kind:** computational.

**Second-review validation status: CONFIRMED.** Isolated re-examination: the contradiction is real (DESIGN says positive/drop; E2 prints negative) and bears on a recorded disposition (L-08), so it crosses the threshold. Not a false positive.

**Step 1 — Cascade map.** Contained to the sunspot CSD sub-claim: DESIGN §2 CSD note + §6 LB-12; OUTLINE L-08 (the "drop" disposition) + ARG-07 (sunspot sub-claim "dropped"); the e2 solar-CSD computation + `e2_divergence_csd.json → csd.solar`; manuscript §3.3.4. The load-bearing sunspot result (the negative *vdiv* sign −0.230) is a separate computation and is NOT in the cascade.

**Step 2 — Method recovery (authoritative + matched recomputation).**
- **(8) Design-rationale framing gate** *(run first, decisive)* — the CSD comparator exists to test whether the single-window CSD indicator beats the vdiv *at the vdiv's own prediction task*. The rebuild's solar vdiv predicts a **future-level** target Y(t+5) (Theorem-8b form; vdiv = −0.230, and vdiv vs forward-vol = +0.029, confirming the target is level, not vol). So the matched solar CSD must use the **future-level** target — not forward volatility.
- **(1 / 7) Source recovery + convergent cross-validation** [original `repro_solar.py` / `FINDINGS_solar.md`] — the +0.42 (actually +0.418) was computed on **monthly** data with vdiv *and* CSD both against **forward 63-mo volatility** (vdiv −0.406, CSD +0.418): a superseded operator the rebuild replaced with yearly / future-level / 3-11. The DESIGN imported the CSD value from an operator the rebuild no longer uses.
- **(5) Matched recomputation** — solar CSD as AR1 over the slow window (ws=11, the convention `csd_corr` and `repro_solar` share) correlated with the vdiv's **future-level** target Y(t+5) = **−0.103** (negative; |ρ| < the vdiv's 0.230). e2's −0.257 used a forward-vol target (a generic-CSD leftover, mismatched to the solar vdiv); the ws=3 fast-window alternative (+0.151) is rejected — too short for a stable AR1 and not the convention.
- **Computational Integrity Check** — e2's solar CSD fails the operator-consistency requirement: the CSD and the vdiv it is compared against used **different targets** (CSD forward-vol vs vdiv future-level). The matched −0.103 is the admissible comparison; the +0.42 (monthly) and −0.257 (yearly forward-vol) are both off-target.

**Step 3 — Adjudication: ORIGINAL CORRECT.** v4's sub-claim — "CSD also shows the correct negative sign with lower magnitude than the vdiv" — **reproduces** under the operator-matched comparison: solar CSD = −0.103 (negative, ~0.45× the vdiv's 0.230). The rebuild's "drop it" disposition was the error, caused by two off-target CSD values (the DESIGN's superseded-monthly +0.42 and e2's forward-vol −0.257). The sub-claim was effectively right in v4; the rebuild's operator/documentation was wrong.

**Specified fix.**
1. e2 — compute the solar CSD against the vdiv's **future-level** target → −0.103; retain the forward-vol value as a labeled diagnostic so the −0.257 is explained, not silently dropped.
2. OUTLINE L-08 — **reverse**: the sunspot "CSD also negative, lower magnitude" sub-claim **reproduces** (−0.103 vs vdiv −0.230) and is **retained**, not dropped.
3. OUTLINE ARG-07 — sunspot CSD sub-claim retained.
4. DESIGN §2 CSD note + §6 LB-12 — the matched sunspot CSD is −0.103 (negative, lower magnitude); the +0.42 was the superseded monthly operator and −0.257 a target mismatch.
5. Dated DESIGN/OUTLINE amendment (v0.4).

**Standing rule 3 (resolved construction committed as code):** the operative construction is the matched solar CSD in `e2_volatility_divergence_csd.py` (AR1 ws=11 vs future-level Y(t+5) = −0.103), with the forward-vol value kept as a diagnostic.

**State: RESOLVED** (fix specified; Phase-2/4 implements). Discovered 2026-06-28; adjudicated 2026-06-28.
