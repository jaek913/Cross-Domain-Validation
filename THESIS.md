# THESIS — Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology

**Date:** 2026-06-28 (Phase 0 — Conceive; this commit's git timestamp is the pre-registration)
**Archetype:** empirical-paper-with-verified-theory
**Build type:** rebuild (see Source)
**Standard:** Research-to-Publication Standard v1.8

## Claim

A moving-average framework — the gap-closure decomposition (filter-share S_W versus series-share S_P), the fast/slow volatility-divergence operator, the Persistence-Sign rule (the sign of the correlation between a fast−slow level divergence and the future observable equals the sign of the difference between the near-lag and far-lag mean autocorrelation), and the property that this divergence operator is a superset of classical critical-slowing-down (CSD) indicators — was derived from mathematical first principles and previously validated only on financial-market data.

The claim of this paper is that the identical framework, applied with the same methodology and no domain-specific modification, recovers the independently-known physical behavior of four natural-science domains — atmospheric science (temperature anomalies), hydrology (river discharge), solar physics (sunspots), and epidemiology (influenza) — and that a single measured quantity, the autocorrelation function (ACF) of the observable, governs the divergence operator's qualitative behavior in every domain tested: its sign, its magnitude, its response to deseasonalization, and its failure modes. The framework's behavior is predicted by a measurable property of each series rather than fitted per domain.

## Why it matters

Testing a framework on systems whose answer is known in advance validates it by external calibration rather than internal consistency alone: if a tool derived for markets — where the data-generating physics is not independently known — recovers the known restoring-force structure of weather, rivers, sunspots, and epidemics, then its financial findings are corroborated from outside finance. The work also yields a practically consequential result: a divergence-based influenza-onset detector that, in retrospective analysis, fires roughly eight weeks earlier than standard level-based surveillance, with simultaneous dominant-strain identification — a public-health-relevant lead time obtained with no epidemiological model, no parameter estimation, and no external data.

## The gap (prior-art scan)

**What is already known.** (i) *Cross-domain statistical universality* — Hurst (1951) found long-range dependence simultaneously in Nile discharge, rainfall, and tree rings; Mandelbrot & Wallis (1968) generalized it to a self-similar (fractional Gaussian) framework. (ii) *The autocorrelation → moving-average-crossover relationship is established within finance* — Lo & MacKinlay (1988, variance ratio as a weighted sum of autocorrelations), Hong & Satchell (2015), Ferreira–Silva–Yen (2019), Moskowitz–Ooi–Pedersen (2012), Zakamulin & Giner (2020); Corsi (2009) for multi-scale realized volatility (HAR). (iii) *Single-window critical-slowing-down early-warning indicators* in ecology/climate — Scheffer et al. (2009), Dakos et al. (2008, 2012a, 2012b), Boettiger & Hastings (2012), Boettiger–Ross–Hastings (2013). (iv) *Hydrological persistence from physical storage* — Koutsoyiannis (2002, 2005, 2006), O'Connell et al. (2016). (v) *Influenza forecasting* — Shaman & Karspeck (2012, 2013), Pei et al. (2018), Vega et al. (2013, Moving Epidemic Method), Steiner et al. (2010, EWMA control charts), Goldstein et al. (2011) and Kandula–Yang–Shaman (2017) for strain-level work, Gatti et al. (2026) for pre-season subtype forecasting.

**What has been tried.** The closest precedent for applying financial time-series indicators to natural science is Kaya (2025), who applied MACD and RSI to 122 years of temperature and precipitation data — a single domain, used descriptively for trend and anomaly detection.

**Why the gap survives.** No prior work has (1) tested a full multi-operator moving-average framework *simultaneously* across four natural-science domains where the physics is independently known; (2) shown that *one measured variable — the ACF — governs the divergence operator's full qualitative behavior* (sign, magnitude, deseasonalization response, and failure modes) rather than treating each domain's behavior as a separate phenomenon; or (3) demonstrated that the finance-derived ACF-sign relationship *transfers to physical systems*, including the predicted sign flip at the ACF zero-crossing. The ACF-sign results above were developed and tested only within financial markets; the CSD literature uses single-window indicators, not a multi-scale volatility comparison; and the universality literature concerns a scaling exponent, not the behavior of a specific operator. The gap is real and matters: it is the difference between "a market tool that happens to work" and "a measurable property that governs a known operator across physical systems."

## The single result that would falsify it

**Headline falsifier (forward, out-of-sample, reader-runnable).** The paper registers a dated prediction for the 2026–2027 Northern Hemisphere influenza season: the divergence onset detector (D = SMA_4 − SMA_12 of the weekly national ILI rate, threshold 0.2 percentage points) will fire at least **6 weeks** before the standard level-based detector (early-season baseline + 1.0 percentage point). In any 2026–27 season with peak ILI ≥ 2.0% (a genuine flu season), **if the divergence detector does not fire ≥ 6 weeks before the level-based detector — or fires after it — the practical claim is falsified.** A reader can run this from public CDC FluView (ILINet) data using the protocol stated in the paper.

**In-paper falsifier (retrospective, load-bearing mechanism).** The unifying-ACF mechanism predicts the sign of the divergence ↔ future-observable correlation from the ACF in every domain. It currently holds on **13 of 13 statistically significant predictions** (p < 0.05), including the two predicted sign flips (Colorado River at h = 252 days; influenza at h = 26 weeks). **A single statistically significant prediction whose observed sign contradicts the ACF-predicted sign falsifies the mechanism.** This is reproducible from the committed analysis on the pinned data.

## Archetype

**empirical-paper-with-verified-theory.** The paper's contribution is empirical cross-domain validation, not new mathematics. The one theorem it relies on (the Persistence-Sign / ACF-sign rule) is treated as prior art and **cited, not re-proved** here; under the standing rule that each paper stands alone, it is referenced like any external result (e.g. Hurst, Scheffer), with no cross-paper dependency. There is therefore no in-paper proof apparatus to retain; the machine checks (claims.lock + verify.py + the 7-point CIC) are the primary integrity layer for every load-bearing number, supplemented by the Phase-5a validity review.

## Source (rebuild — source material, not inherited results)

This paper rebuilds prior work. The source is used as **source material, not inherited results** — every number is regenerated under the contract; nothing is carried over on the strength of the prior manuscript.

- **Primary source artifact (hash-pinned):** `C:\Users\jaek9\Documents\Repos\lagging-truth-paper-05\paper\Paper5_Final_Natural_Sciences_Validation_v4.md`
  - MD5 `23428fb275f6ea6d6a3846fc17d91a86`
  - SHA256 `982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50`
  - A byte-identical copy exists at `C:\Users\jaek9\Documents\LaggingTruth\05-13-2026\Paper 5\` (same MD5, verified 2026-06-28).
- **Supporting source assets (to be inventoried and hashed in Phase 1 — COVERAGE.md / SOURCES.md):** `C:\Users\jaek9\Documents\LaggingTruth\05-13-2026\Paper 5\` — `figure1.png` (the ACF unification diagram), `References\` (eight cited-work PDFs), `Paper5_Plain_English.md` (plain-English companion), and `PDF_Build\` (build chain + built PDFs; its title block carries the superseded working title "Cross-Domain Validation of the Adaptation Framework in Natural Sciences" and the placeholder front matter — both to be replaced with the finalized title and full front matter during the rebuild).

---

*Phase 0 — Conceive. Standard v1.8. This file is the pre-registration: the manuscript is written from it (via the Phase-1 OUTLINE.md) and reconciled against it at Phases 4–5.*
