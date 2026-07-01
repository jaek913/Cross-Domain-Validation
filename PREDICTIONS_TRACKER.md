# Forward-Prediction Weekly Tracker -- 2026-27 Influenza Season

Companion to `PREDICTIONS.md`. Tracks **P1** (onset lead) and **P2** (dominant strain) against CDC FluView as the season unfolds, MMWR **2026-40 ... 2027-20** (33 weeks).

**Provisional, not binding.** Weekly FluView values are revised by backfill; these rows are a running view only. The **binding verdict** is computed once on the finalized vintage at the lock date (**2027-09-01**) per `PREDICTIONS.md`. Fill one row per FluView weekly release.

## P1 -- Onset lead
National **% WEIGHTED ILI** (ILINet). Divergence D = SMA4 - SMA12; **divergence fires** at D > +0.2 pp. **Level fires** at % WEIGHTED ILI > baseline + 1.0 pp, where baseline = mean of 2026-40 ... 2026-43.

- Baseline (mean % WEIGHTED ILI, 2026-40 ... 2026-43): _____
- Divergence fire week: _____  |  Level fire week: _____  |  **Lead (weeks): _____**
- Peak % WEIGHTED ILI: _____ (mark UNTESTABLE if < 2.0%)  |  **P1 provisional verdict: _____**

| MMWR week | % WEIGHTED ILI | SMA4 | SMA12 | D = SMA4-SMA12 | div fired (D>0.2)? | level fired? | notes |
|---|---|---|---|---|---|---|---|
| 2026-40 |  |  |  |  |  |  |  |
| 2026-41 |  |  |  |  |  |  |  |
| 2026-42 |  |  |  |  |  |  |  |
| 2026-43 |  |  |  |  |  |  |  |
| 2026-44 |  |  |  |  |  |  |  |
| 2026-45 |  |  |  |  |  |  |  |
| 2026-46 |  |  |  |  |  |  |  |
| 2026-47 |  |  |  |  |  |  |  |
| 2026-48 |  |  |  |  |  |  |  |
| 2026-49 |  |  |  |  |  |  |  |
| 2026-50 |  |  |  |  |  |  |  |
| 2026-51 |  |  |  |  |  |  |  |
| 2026-52 |  |  |  |  |  |  |  |
| 2027-01 |  |  |  |  |  |  |  |
| 2027-02 |  |  |  |  |  |  |  |
| 2027-03 |  |  |  |  |  |  |  |
| 2027-04 |  |  |  |  |  |  |  |
| 2027-05 |  |  |  |  |  |  |  |
| 2027-06 |  |  |  |  |  |  |  |
| 2027-07 |  |  |  |  |  |  |  |
| 2027-08 |  |  |  |  |  |  |  |
| 2027-09 |  |  |  |  |  |  |  |
| 2027-10 |  |  |  |  |  |  |  |
| 2027-11 |  |  |  |  |  |  |  |
| 2027-12 |  |  |  |  |  |  |  |
| 2027-13 |  |  |  |  |  |  |  |
| 2027-14 |  |  |  |  |  |  |  |
| 2027-15 |  |  |  |  |  |  |  |
| 2027-16 |  |  |  |  |  |  |  |
| 2027-17 |  |  |  |  |  |  |  |
| 2027-18 |  |  |  |  |  |  |  |
| 2027-19 |  |  |  |  |  |  |  |
| 2027-20 |  |  |  |  |  |  |  |

## P2 -- Dominant strain
Subtype **percent-positivity** pp_s = 100 x positives_s / total specimens (NREVSS / public-health labs). D_s = SMA4(pp_s) - SMA12(pp_s); **fires** at D_s > +0.3 pp.

- First-firing subtype: _____  |  Full-season plurality subtype: _____
- Single-strain (one subtype >= 70% of subtyped positives)? _____  |  **P2 provisional verdict: _____**

| MMWR week | H1N1pdm09 %pos | H3N2 %pos | B %pos | total specimens | first D_s>0.3 this week | notes |
|---|---|---|---|---|---|---|
| 2026-40 |  |  |  |  |  |  |
| 2026-41 |  |  |  |  |  |  |
| 2026-42 |  |  |  |  |  |  |
| 2026-43 |  |  |  |  |  |  |
| 2026-44 |  |  |  |  |  |  |
| 2026-45 |  |  |  |  |  |  |
| 2026-46 |  |  |  |  |  |  |
| 2026-47 |  |  |  |  |  |  |
| 2026-48 |  |  |  |  |  |  |
| 2026-49 |  |  |  |  |  |  |
| 2026-50 |  |  |  |  |  |  |
| 2026-51 |  |  |  |  |  |  |
| 2026-52 |  |  |  |  |  |  |
| 2027-01 |  |  |  |  |  |  |
| 2027-02 |  |  |  |  |  |  |
| 2027-03 |  |  |  |  |  |  |
| 2027-04 |  |  |  |  |  |  |
| 2027-05 |  |  |  |  |  |  |
| 2027-06 |  |  |  |  |  |  |
| 2027-07 |  |  |  |  |  |  |
| 2027-08 |  |  |  |  |  |  |
| 2027-09 |  |  |  |  |  |  |
| 2027-10 |  |  |  |  |  |  |
| 2027-11 |  |  |  |  |  |  |
| 2027-12 |  |  |  |  |  |  |
| 2027-13 |  |  |  |  |  |  |
| 2027-14 |  |  |  |  |  |  |
| 2027-15 |  |  |  |  |  |  |
| 2027-16 |  |  |  |  |  |  |
| 2027-17 |  |  |  |  |  |  |
| 2027-18 |  |  |  |  |  |  |
| 2027-19 |  |  |  |  |  |  |
| 2027-20 |  |  |  |  |  |  |

---

*Companion to PREDICTIONS.md (registered 2026-07-01). Weekly rows provisional; binding verdict computed on the finalized vintage at the 2027-09-01 lock date.*
