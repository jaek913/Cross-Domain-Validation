# Phase 5a — Adjudication of the Independent Adversarial Review (Cross-Domain-Validation)

**Author of this document:** Jae Kim (drafted with AI assistance under the v1.8 protocol).
**Companion files:** `review_prompt_5a.md` (the prompt the reviewer was given) and `review_5a_transcript.md` (the reviewer's verbatim output, returned from a fresh claude.ai session with the 10-file package uploaded). This file records how each finding was adjudicated against the code and data, and the one capped fix round that resulted.

**Reviewer verdict:** ship-with-fixes.
**Disposition of this round:** every finding adjudicated against `analysis/*.py` + `analysis/outputs/*.json` (not taken on the reviewer's word); fixes applied or rebutted with a recorded reason; one capped round, no reopen loop. The cross-domain thesis, the influenza-onset headline, and the in-paper falsifier are unaffected — the net effect is a more honest framing of the persistence-sign evidence (the predicted **sign** + IS/OOS stability, with the parametric significance demoted) and a more honest onset comparator, plus two stale-document corrections.

---

## Adjudication table

| # | Finding (reviewer) | Verdict | What I confirmed against code/data | Remedy class |
|---|---|---|---|---|
| F1 | Look-ahead — PASS, but E3 uses full-sample deseasonalization while the causal-vs-full check covers only E1 | **Partially upheld** (minor; a fixed per-calendar offset is very unlikely to flip a correlation sign) | Operators are causal (`fwd_realized_std` = `rolling(H).std().shift(-H)`; forward-shifted targets); the one look-ahead artifact (Colorado contemporaneous-fast, +0.322) is labeled `v4_artifact_contemp_fast` and is NOT a headline result | gated check (4A) |
| F2 | Index / row alignment — PASS | **Affirmed** | `corr_sub` concat→dropna alignment, `shift(-H)` targets, region↔national reindex by `k=YEAR*100+WEEK` all correct | none |
| F3 | Statistical inference — the "13/13 significant" screen is anti-conservative | **UPHELD (most material)** | `e3` `SUB_D=21 < WS_D=63` → adjacent subsamples share 42 of 63 days of the slow window; `_is_sig` uses Fisher-z `1/√(n−3)` on the full n≈2220; hydrology |ρ|≈0.06–0.17. **Mitigant already in hand: IS/OOS sign-consistency = 13/13** (`isoos_consistent_among_significant`), block-independent | gated analysis attempted → re-tooled; headline recast |
| F4 | Onset comparison is a soft test (asymmetric sweep) | **UPHELD** | `e4` swept only the divergence threshold {0.1,0.2,0.3} and pinned `LVL_ADD=1.0`; the docstring even named an unimplemented level sweep; advantage runs 8.2→4.8 wk across the div-sweep | gated analysis (2A) + reframe |
| F5 | Three overreaching phrasings ("≈8 wk earlier than level-based surveillance"; "the ACF governs … every domain"; "13/13 significant") | **Upheld** | wording in Abstract / C-01 / C-03 / §6.2 vs the evidence | prose |
| F6 | Gap claim — PASS; sub-claim (ii) "ACF governs the operator's full qualitative behavior" slightly strong | **Affirmed** + minor prose | the MA-divergence literature is financial (Kaya-2025 single-domain descriptive; Li-2025 cited); Theorem 8b attributed, not claimed new | prose |
| note-a | The "four-domain" significance is carried by 2 domains (hydrology + epidemiology) | **Disclosed — no change required**; one honest clause added | §4.2 excludes sunspots by design; the per-domain counts are already shown; weather contributes 0 significant predictions | folded into the §4.4 prose |
| note-b | COVERAGE §3.3 said the solar CSD sub-claim was "dropped" while the paper RETAINS it (`LB-e2-csd-solar` = −0.103, D02) | **Upheld** | COVERAGE §3.3 row read "…sub-claim dropped"; the value is a live LB token in the paper | doc fix |

I also caught, while grounding note-b, a second stale COVERAGE annotation: §2.2 read weather "S_W 1.3–7.7%" but the locked/regenerated value is the band `[2.5, 5.2]`. Record-only; fixed in the same doc pass.

Nothing required a pure rebuttal. The reviewer's "do not change" list — the theorem + three-way proof, the reproductions, the look-ahead discipline, the two honest negatives (E6 peak, E7/E7b spatial), and the hydrology returns-operator correction — I agree with; all untouched.

---

## F3, the material finding: a bootstrap was attempted, then rejected as the wrong tool

The reviewer's recommended remedy was a moving-block bootstrap to replace the anti-conservative Fisher-z screen with an autocorrelation-robust one, plus a recast of the headline toward the IS/OOS sign-stability. I implemented the bootstrap to test the concern with evidence rather than hedge in prose: a moving-block bootstrap of the subsampled Spearman, two block lengths (slow-window `ceil(ws/sub)` = 3 daily / 2 flu, and ~1 year `ceil(period/sub)` = 18 daily / 7 flu), B=1000, seed 0.

**It backfired revealingly.** Instead of weakening the marginal river predictions it *strengthened* them: slow-window block → 13/13; year block → 14/14 (Dallas *gained* one). A longer block produced *more* robust-significant predictions, the opposite of a conservative correction. Per the standing rule to scrutinize a too-good / counterintuitive result hardest (the D01 Colorado-+0.33 lesson), this was the signal that the tool was wrong, not the result:

1. **Mechanically** — a joint-block percentile CI *tightens* around a weak, structure-driven correlation as the block grows: long blocks preserve the seasonal coherence, so every resample reproduces the same small ρ and the CI narrows. The bootstrap therefore makes a true small correlation look *more* significant at longer blocks, not less. The Dallas 0→1 gain at the year block is exactly that artifact.
2. **More fundamentally** — Theorem 8b *predicts this correlation's sign from the ACF*. The correlation is a theory-derived *consequence* of the autocorrelation, not a spurious artifact *of* it. "Correct the significance for autocorrelation" (which treats the correlation as spurious noise) partly mis-frames the claim. The claim was never "ρ is large"; it is "the sign matches the theorem," scored by 20/25 correct, **0 significant-wrong**, and **13/13 IS/OOS sign-stable**.

**Adjudication: the bootstrap is the wrong tool; recast on the SIGN (recommendation B, author-approved).** The robust, assumption-light evidence is already in hand and block-independent — the sign is what the theorem predicts (proven + three-way verified) and every one of the 13 screened predictions keeps its sign across both temporal halves. The bootstrap code, constants, and the scipy import were fully **removed** from `e3_theorem8b_sign.py` (reverted to the original + the 4A addition only); a post-revert re-run confirms the original values reproduce (20/25, 13/13, both flips, IS/OOS 13/13) plus the new 4A field. The attempt and the reasoning are recorded in DECISIONS (2026-06-29) so the dead end is in the research log, not erased.

**Prose remedy (§4.3/§4.4):** the headline is now the predicted **sign**, scored two ways that do not depend on a parametric significance model — overall accuracy (20/25) and the block-independent IS/OOS stability (13/13, the load-bearing result). The Fisher-z screen is explicitly **demoted** to a labeled cross-check, with the anti-conservatism stated plainly: the subsample stride (21 d / 8 wk) is shorter than the slow window (63 d / 16 wk), so adjacent subsamples share overlapping divergence windows and the rivers carry long-range dependence — both push the effective sample size below the nominal count, so the marginal river ρ are directionally informative, not precisely calibrated. The in-paper falsifier (one significant prediction whose sign contradicts the rule) passed a *stricter*-than-intended test, since over-calling significance only makes a significant-wrong *easier* to trip and none tripped. The E3 CIC #5 note was corrected from the inaccurate "subsample every 21/8 (non-overlapping)" to the accurate overlapping-windows / demoted-Fisher-z / sign+IS/OOS+causal-backbone description.

---

## F4, 2A — symmetric onset sweep (clean, wired)

`e4_flu_onset.py` gained a symmetric level-threshold sweep {0.5, 1.0, 1.5 pp}: advantage **5.286 / 8.222 / 9.731 wk** (divergence earlier in 92.9% / 96.3% / 100% of seasons), and the divergence leads in 88–100% of seasons across all threshold pairs. So the onset advantage is robust to the comparator threshold, not an artifact of the 1.0 pp pin. Prose reframed in §5.1.1/§5.1.2 + Abstract + C-03 from "earlier than level-based surveillance" to "≈8 weeks earlier than a **simple** level-threshold rule (baseline + 1.0 pp), range ~5.3–9.7 wk as the threshold varies +0.5→+1.5 pp"; §5.1.1 keeps the more sophisticated published detectors (SIRS-EAKF, metapopulation, Moving Epidemic Method, EWMA) as the state-of-the-art context, with the simple level rule as the transparent comparator for the *mechanism* (slope vs level).

## F1, 4A — causal deseasonalization (clean, wired)

`e3` recomputes the daily grid under strictly expanding (causal) per-calendar means (flu is RAW, unaffected). Result: **0** significant-correct verdicts flip, and only **2 of 20** daily observed signs flip — both among non-significant, near-zero-ρ weather predictions. The load-bearing E3 results are unaffected by full-sample vs causal seasonal means, closing the F1 sub-gap.

---

## What changed (this single capped round)

- **Code:** `e4_flu_onset.py` (2A symmetric sweep); `e3_theorem8b_sign.py` (4A causal recompute; the attempted 1A bootstrap removed on the recast decision); `data_io.py` (`deseason_month_causal`, `deseason_doy_causal`).
- **Ledger (`build_claims.py` → `claims.lock`):** 5 new load-bearing numbers registered, all `regenerate` — `LB-e3-isoos-consistent` (13), `LB-e3-causal-sigcorrect-flips` (0), `LB-e3-causal-obs-flips` (2), `LB-e4-adv-lvl-low` (5.286), `LB-e4-adv-lvl-high` (9.731); the lock grows 73 → 78 rows (76 non-theorem LB tokens). The E3 CIC #5 note and the `LB-e1-weather-sw` claim description ("1.3–7.7%" → "~2.5–5.2%") corrected.
- **Paper (`paper/paper.md`):** §4.3/§4.4 recast (sign + IS/OOS headline, Fisher-z demoted, falsifier-stricter caveat, causal-robustness line, honest thin-coverage clause); §5.1.1/§5.1.2 + Abstract + C-03 onset reframed to a simple level rule with the symmetric-sweep range; Abstract + §1.2(ii) + §6.2 + C-01 softened from "the ACF governs the operator's full qualitative behavior" to "governs the **sign** (proven) and tracks the magnitude / deseasonalization response / failure modes." All 5 new `{{LB-id}}` tokens placed.
- **Docs:** `COVERAGE.md` → v0.4 (§2.2 band fixed, §3.3 solar "dropped" → RETAINED, a dense 5a changelog entry, and a clarifying note that the §3-table E2 hydrology cells describe the rebuild-time "Ohio null" narrative while the authoritative current result is the returns-operator reframing per D01); `DECISIONS.md` dated 5a entry appended; the review prompt, this responses file, and the reviewer transcript preserved under `verification/`.

**Verification:** the full gate (`e3` → `build_claims` → `render_claims` → `verify --paper`) must run GREEN with the lock at 78 rows and reconciliation finding all 76 LB tokens, before commit. Read-back of `claims.lock` + `paper.rendered.md` by MD5.
