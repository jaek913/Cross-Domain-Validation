# Forward Predictions -- 2026-27 Influenza Season

**Cross-Domain Validation of a Moving-Average Divergence Framework** (see the paper, Section 7, "Forward Predictions"). This file is the dated public registration of the paper's two standing forward predictions. The git commit that adds this file is the immutable registration timestamp; the public release accompanies the coordinated launch.

- **Registered:** 2026-07-01 (repo commit timestamp).
- **Season:** 2026-27 Northern-Hemisphere influenza season, MMWR weeks **2026-40 through 2027-20** (33 weeks).
- **Data:** public CDC FluView -- ILINet (national % WEIGHTED ILI) for P1; virologic surveillance / NREVSS subtype positivity for P2.
- **Lock date:** **1 September 2027.** Both predictions are resolved once, on the **first finalized FluView release on or after the lock date**, with every detector computed on that single data vintage -- so weekly backfill revisions cannot change the verdict. Provisional weekly values are tracked in `PREDICTIONS_TRACKER.md`; only the locked-vintage computation is binding.
- **Status:** OPEN (season not yet begun).

## Why these are registered
A dated, out-of-sample prediction a reader can run is stronger evidence than a retrospective fit, and it is the one check that routes around both author and reviewer. A confirmed onset lead would show the operator captures a stable structural property of influenza dynamics rather than a historical fit; a strain miss in a clearly single-strain season would falsify the strain claim specifically while leaving the onset result intact.

## P1 -- Onset Lead
**Claim.** The onset divergence fires **at least six weeks before** the level detector, over MMWR weeks 2026-40 ... 2027-20.

- **Onset divergence:** D(t) = SMA4(ILI) - SMA12(ILI) on the continuous weekly national % WEIGHTED ILI series (SMA4, SMA12 = trailing 4- and 12-week simple moving averages). It **fires** at the first season-week with D(t) > **+0.2 pp**.
- **Level detector (comparator):** fires at the first week with ILI(t) > (mean of the season's first four weeks, 2026-40 ... 2026-43) + **1.0 pp**.
- **Lead** = (level-detector fire week) - (divergence fire week), in weeks.
- **CONFIRMED** if lead >= 6 weeks (divergence earlier).
- **FALSIFIED** if lead < 6 weeks, **or** the divergence fires after (later than) the level detector.
- **UNTESTABLE** (carries forward to the next season) if peak national % WEIGHTED ILI stays below **2.0%** for 2026-27.

## P2 -- Dominant Strain
**Claim.** The **first subtype whose percent-positivity divergence fires** will match the **full-season plurality (dominant) subtype**.

- **Per-subtype signal:** for each subtype s, pp_s(t) = 100 x (subtype-s positive specimens / total specimens tested); D_s(t) = SMA4(pp_s) - SMA12(pp_s), continuous. Subtypes: A(H1N1)pdm09, A(H3N2), B.
- **First-firing subtype:** the first s with D_s(t) > **+0.3 pp** (tie-break: higher pp_s at the firing week).
- **Plurality strain:** the subtype with the highest full-season positive total.
- **CONFIRMED** if the first-firing subtype equals the plurality subtype.
- **FALSIFIED** if they differ **and** the season is single-strain (one subtype >= **70%** of the season's subtyped positives).
- **INCONCLUSIVE** if they differ in a mixed season (no subtype >= 70%).

## P3 -- Peak Lead (NOT registered)
A 2026-27 peak-lead prediction was contingent on a positive retrospective spatial-curvature lead (paper Section 5.1.6). That retrospective is an honest negative, so **P3 is not registered** and is omitted from the falsifier set. P1 and P2 stand on their own.

## Step-by-step replication protocol (reader-runnable)
Anyone can reproduce the verdict from public data.

**P1 (onset lead)**
1. **Download** CDC FluView **ILINet**, geography = National, for the 2026-27 season (FluView portal, or the ILINet CSV export). Use the **% WEIGHTED ILI** column, weekly, MMWR 2026-40 ... 2027-20.
2. On the continuous weekly series compute **SMA4** and **SMA12** (trailing 4- and 12-week simple moving averages) and **D = SMA4 - SMA12**.
3. **Divergence fire week** = first week (from 2026-40) with D > 0.2 pp.
4. **Baseline** = mean % WEIGHTED ILI over 2026-40 ... 2026-43; **level fire week** = first week with % WEIGHTED ILI > baseline + 1.0 pp.
5. **Lead** = level-fire-week - divergence-fire-week. Apply the CONFIRMED / FALSIFIED / UNTESTABLE rules above. (If peak % WEIGHTED ILI < 2.0%, mark UNTESTABLE and carry forward.)

**P2 (dominant strain)**
1. **Download** CDC FluView **virologic surveillance** (clinical + public-health-lab subtype counts / NREVSS), National, 2026-27.
2. For each subtype s in {A(H1N1)pdm09, A(H3N2), B}, compute weekly **pp_s = 100 x positives_s / total specimens**, then **D_s = SMA4(pp_s) - SMA12(pp_s)**.
3. **First-firing subtype** = first s with D_s > 0.3 pp (tie-break: higher pp_s).
4. **Plurality subtype** = highest full-season positive total.
5. Compare; apply the CONFIRMED / FALSIFIED / INCONCLUSIVE rules (single-strain = one subtype >= 70% of the season's subtyped positives).

The reference implementations are the committed `analysis/e4_flu_onset.py` (onset) and `analysis/e5_strain_id.py` (strain); the same operators, thresholds, and season rule apply to the 2026-27 data.

## Resolution (at the lock date)
On or after **2027-09-01**, pull the first finalized FluView release for the 2026-27 season, run the protocol above **on that single vintage**, and record the verdict here (dated) and in `PREDICTIONS_TRACKER.md`:

- **P1:** CONFIRMED / FALSIFIED / UNTESTABLE (carried forward).
- **P2:** CONFIRMED / FALSIFIED / INCONCLUSIVE.

If either prediction resolves **against** the paper, the outcome is also recorded in `CORRECTIONS.md` with the date and the change made.

---

*Registered 2026-07-01. Part of the Cross-Domain Validation paper's Phase-5c certification. Public at the coordinated launch.*
