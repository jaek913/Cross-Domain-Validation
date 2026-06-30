# Phase 5a — Independent Adversarial Review (Cross-Domain-Validation)

**How to run this:** Start a NEW claude.ai conversation, upload every file in this package folder, and paste this prompt as your first message. You are reviewing by READING — you cannot run code in this session, and you don't need to: a committed run of the verification gate is included (`06_verify_output.txt`).

You are an independent, skeptical reviewer. You have not seen how this paper was built and you have no access to the author's reasoning — the author's decision log and the discrepancy dossiers are deliberately excluded from this package so your review is independent. Your job is to test the paper's **validity**, not just its arithmetic. Would its claims survive a determined attempt to break them? Be adversarial but fair: a skeptical-but-constructive colleague who invites discussion rather than arguing with an imagined critic.

## Your materials (everything is in this package)
- `00_REVIEW_PROMPT.md` — this file.
- `01_paper_rendered.md` — the manuscript, with every load-bearing number substituted in.
- `02_claims_lock.json` — the load-bearing-number ledger: each id → value, provenance tier, the input data hashes, and the numerical tolerance. Every number in the paper traces to this.
- `03_SOURCES_data_dictionary.md` — the data dictionary: every source, its hash, and the manifest.
- `04_OUTLINE.md` — the paper's argument roadmap (argument nodes, citation keys, load-bearing findings, figures, scope conditions, conclusions/limits).
- `05_COVERAGE.md` — the rebuild coverage ledger (what this rebuild kept, dropped, and why; its shape vs the prior version).
- `06_verify_output.txt` — the committed output of `python analysis/verify.py --paper paper/paper.md`. It is the mechanical gate: data hashes, reproduction within tolerance, the seven look-ahead / common-implementation-check flags signed, every ledger value present at its marker, and the OUTLINE reconciliation GREEN. You cannot re-run it — treat it as evidence the mechanical checks pass, and spend your effort on the judgment the gate cannot make.
- `07_theorem8b_three_way.md` — the record reconciling the theorem's written proof, a symbolic grid check, and a numerical stress check.
- `08_analysis_code_bundle.txt` — ALL analysis scripts concatenated (operators, data loaders, the seven experiments + the regional diagnostic, the claim builder/renderer, the verifier, the figure builder, and the two theorem checks), each under a `# ===== FILE: … =====` header. Read the code behind any number you doubt — this is where look-ahead, alignment, and inference bugs hide.
- `09_outputs_bundle.txt` — the raw committed experiment outputs (JSON), concatenated. Cross-check any ledger value here if you doubt it.

## Part 1 — The fixed six-concern menu (one finding each)
For EACH concern give a verdict — **PASS** / **CONCERN** / **FAIL** — and cite specific evidence (file, function, value). Inspect the code bundle; do not take the prose's word for it.

1. **Look-ahead / leakage.** Does any reported predictor use information at or after the target it predicts? Check the divergence operators, the forward targets (`fwd_realized_std`, the forward-shifted correlations), the deseasonalization (causal vs full-sample), and the onset / strain detectors. The paper deliberately reproduces ONE look-ahead *artifact* to explain a discrepancy in the prior version — confirm it is clearly labeled an artifact and is NOT among the headline results.
2. **Index / row alignment.** Are series aligned correctly in time when correlated or compared — same calendar index, correct forward shift, no off-by-one between predictor and target, no misaligned region↔national join? Check the alignment in the data loaders and `corr_sub` / the forward-target construction in `operators.py`.
3. **Statistical-inference validity.** Are the significance claims sound — subsampling for autocorrelation, Fisher-z confidence intervals, block-shuffle / permutation nulls, paired tests — applied correctly and not double-counting overlapping windows? Is "significant" defined consistently across experiments?
4. **Does the spec test the thesis?** Do the pre-registered operators / horizons / thresholds actually test each section's claim, or could a result pass for an unrelated reason? In particular: does the persistence-sign grid genuinely test the autocorrelation-sign rule, and does the onset comparison genuinely test "earlier than a level-based detector"?
5. **Interpretation overreach.** Does any sentence claim more than the evidence supports — causal language on correlational results, "proves / demonstrates" where "is consistent with" is warranted, or generalization beyond what was tested? Flag specific sentences.
6. **Is the gap claim real?** The paper claims novelty: that no prior work tests a full multi-operator moving-average divergence framework simultaneously across four natural-science domains, and that one measured quantity — the autocorrelation function — governs the operator's qualitative behavior. Is that defensible, does it overlook obvious prior art, and is it appropriately scoped ("to our knowledge")?

## Part 2 — Completeness pass
1. `06_verify_output.txt` already shows the mechanical reconciliation GREEN (every citation key, load-bearing id, theorem id, and required section present; no placeholders). Confirm you see that in the transcript and note it.
2. Now do the JUDGMENT pass the gate cannot: walk `04_OUTLINE.md` node by node — every argument node, citation key, load-bearing finding, figure / table / equation, scope condition, and conclusion / limit — and for EACH confirm it is present AND genuinely supported in `01_paper_rendered.md`. Raise any missing citation, finding, section, or argument — or any DROP recorded in `05_COVERAGE.md` that looks unjustified — as a finding. (This is the pass meant to catch a silently dropped analysis or citation.)

## Output
Return:
- A one-line overall verdict: **ship** / **ship-with-fixes** / **hold**.
- The six concern findings (verdict + evidence each).
- The completeness-pass result (reconciliation confirmation + any missing / unsupported / unjustifiably-dropped node).
- A numbered list of any required fixes, most material first.

Be specific and evidence-based. If a concern is clean, say so and say what you checked. A short, sharp review beats a long vague one.
