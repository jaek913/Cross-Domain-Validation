# Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology

**Jae Kim** · ORCID 0009-0005-3260-7880 · Independent researcher · jae@laggingtruth.com
*Lagging Truth research series. Draft — Phase 4 (Write). Every load-bearing number is rendered from the committed ledger `analysis/claims.lock` by the committed renderer (`analysis/render_claims.py`); bibliographic formatting is finalized at Phase 5b.*

---

## Abstract

A moving-average framework developed from mathematical first principles — a gap-closure decomposition that measures whether a moving-average filter leads or lags its series (the filter-share `S_W`), a fast-minus-slow volatility-divergence operator, a persistence-sign rule that predicts the sign of the correlation between a fast-minus-slow level divergence and the future observable from the series' autocorrelation function (ACF), and the property that the divergence operator is a superset of classical critical-slowing-down (CSD) indicators — had previously been validated only on financial-market data \cite{Kim-2026a}\cite{Kim-2026b}\cite{Kim-2026c}\cite{Kim-2026d}. This paper tests whether the identical framework recovers the independently-known physical behavior of four natural-science domains: atmospheric science (station temperature anomalies), hydrology (river discharge), solar physics (sunspot numbers), and epidemiology (influenza-like illness). The decomposition and the persistence-sign rule are applied identically across all four domains; the volatility-divergence operator is adapted to each domain's natural innovation representation (log-returns, first-differences, or level), a choice we disclose rather than tune.

Three results follow. First, the decomposition orders the four domains by restoring-force strength exactly as their physics predicts, from a near-random-walk weather benchmark (`S_W` band {{LB-e1-weather-sw}}%) through deseasonalized rivers to mechanically-adapting influenza ({{LB-e1-flu-sw}}%), against a synthetic random-walk control that sits at {{LB-e1-rw-control}}. Second, the persistence-sign rule holds on every statistically significant prediction it makes — {{LB-e3-significant-correct}} of {{LB-e3-significant-total}} significant predictions correct with {{LB-e3-significant-wrong}} significant wrong-signed predictions across a pre-registered 25-prediction grid — including two predicted sign flips: the Colorado River at horizon 252 days, where the flip arises because the near-lag mean ACF falls below the far-lag mean ACF while the ACF itself remains positive (it is **not** an ACF zero-crossing), and influenza at horizon 26 weeks, near the seasonal ACF structure whose zero-crossing sits at {{LB-e3-flu-flip-acf}} weeks. Third, a divergence-based influenza-onset detector fires {{LB-e4-advantage}} weeks earlier on average than level-based surveillance across {{LB-e4-seasons}} seasons, with simultaneous dominant-strain identification, obtained with no epidemiological model. A unifying variable — the ACF of the observable — governs the divergence operator's sign, magnitude, deseasonalization response, and failure modes in every domain tested. We register dated, reader-runnable 2026–27 influenza predictions as the headline falsifier; a single statistically significant prediction whose observed sign contradicts the ACF-predicted sign would falsify the central mechanism. A spatial-curvature peak-detection hypothesis was pre-registered and **failed**: spatial disaggregation of the national signal does not yield a robust causal lead on the national peak, and we report that honest negative alongside the onset result.

**Keywords:** time-series analysis · moving averages · autocorrelation · critical slowing down · external validation · influenza surveillance · hydrology · sunspots
**JEL:** C22 (time-series models) · C53 (forecasting) · Q54 (climate; natural disasters)

---

## 1. Introduction

### 1.1 What this paper tests

A statistical tool derived for one domain can succeed there for the wrong reasons. Financial markets are a hard setting in which to validate a method, because the data-generating process is not independently known: a result that "works" on prices cannot be checked against a ground-truth mechanism. The moving-average framework studied here — the decomposition, the volatility-divergence operator, the persistence-sign rule, and the CSD-superset property — was derived from first principles and, until now, exercised only on market data \cite{Kim-2026a}\cite{Kim-2026d}.

This paper applies the framework to four natural-science domains whose restoring-force physics is independently established, and asks a single question: does the framework recover the behavior the physics already predicts? Weather temperature anomalies are strongly mean-reverting on short horizons; river discharge carries persistence set by physical catchment storage; sunspots are oscillatory; influenza prevalence has essentially no stationary restoring force during an outbreak. If a market-derived tool reconstructs these known structures with no per-domain fitting, its financial findings are corroborated from outside finance — the difference between "a market tool that happens to work" and "a measurable property that governs a known operator across physical systems."

The decomposition and the persistence-sign rule are applied **identically** across the four domains. The volatility-divergence operator is **adapted** to each domain's natural innovation representation — log-returns for discharge, first-differences for temperature and influenza, level for sunspots — because the physically meaningful volatility lives in different transforms of different observables. We treat that adaptation as a disclosed modeling choice (scope condition S5), not a free parameter, and we report each operator's reproducible value.

### 1.2 Why the natural sciences, and what is already known (related work)

Several literatures border this work without occupying it. Cross-domain statistical *universality* is long established: Hurst \cite{Hurst-1951} found long-range dependence simultaneously in Nile discharge, rainfall, and tree rings, and Mandelbrot and Wallis \cite{Mandelbrot-Wallis-1968} generalized it to a self-similar fractional-Gaussian framework — but that literature concerns a scaling *exponent*, not the behavior of a specific operator. The relationship between autocorrelation and moving-average crossovers is established *within finance*: the variance-ratio decomposition \cite{Lo-MacKinlay-1988}, momentum and moving-average autocovariance results \cite{Hong-Satchell-2015}\cite{Ferreira-2019}\cite{Moskowitz-2012}\cite{Zakamulin-Giner-2020}, and multi-scale realized-volatility modeling \cite{Corsi-2009} — but these were developed and tested only on market data. The CSD early-warning literature in ecology and climate \cite{Scheffer-2009}\cite{Dakos-2008}\cite{Dakos-2012a}\cite{Dakos-2012b}\cite{Dablander-2022}\cite{Boettiger-Hastings-2012}\cite{Boettiger-Ross-Hastings-2013} uses *single-window* indicators (rising lag-1 autocorrelation or variance), not a multi-scale volatility comparison. Hydrological persistence from physical storage is well characterized \cite{Koutsoyiannis-2002}\cite{Koutsoyiannis-2005}\cite{Koutsoyiannis-2006}\cite{O'Connell-2016}, as is the broader use of econometric methods on climate data \cite{Hsiang-2016}. Influenza forecasting has a mature toolkit — mechanistic and statistical forecasts \cite{Shaman-Karspeck-2012}\cite{Shaman-2013}\cite{Pei-2018}, epidemic-threshold methods \cite{Vega-2013}, EWMA control charts \cite{Steiner-2010}, strain-level incidence and subtype forecasting \cite{Goldstein-2011}\cite{Kandula-2017}\cite{Gatti-2026} — and operator-level analyses of moving-average indicators have begun to appear \cite{Li-2025}.

The nearest precedent for applying financial time-series indicators to natural science is Kaya \cite{Kaya-2025}, who applied MACD and RSI to 122 years of temperature and precipitation in a single domain, descriptively. No prior work has (i) tested a full multi-operator moving-average framework *simultaneously* across four natural-science domains with independently-known physics; (ii) shown that *one measured variable — the ACF — governs the divergence operator's full qualitative behavior* rather than treating each domain separately; or (iii) demonstrated that the finance-derived ACF-sign relationship *transfers to physical systems*, including a predicted sign flip driven by the mean-ACF structure. That gap is what this paper fills.

### 1.3 Organization

Part 2 builds the calibration scale from the gap-closure decomposition and orders the domains by restoring-force strength. Part 3 applies the volatility-divergence operator and compares it to single-window CSD. Part 4 tests the persistence-sign rule (the in-paper falsifier). Part 5 turns the framework to practice: influenza onset detection, dominant-strain identification, and two pre-registered peak-detection tests (one rejected in this paper's own prior work, one net-new and reported here as an honest negative). Part 6 synthesizes the unifying-ACF account. Part 7 registers the 2026–27 forward predictions. Methods appear where each operator is first used; the exact operators, windows, thresholds, and data manifest are pre-registered in the design record, and every load-bearing number is wired to a committed script on hashed data through the ledger.

---

## 2. The calibration scale: gap-closure decomposition

### 2.1 Methodology

For an observable `Y` and its `N`-period simple moving average `SMA_N(Y,t)` (the mean of the most recent `N` observations, no look-ahead), an **event** is a week at which the displacement `|Y(t) − SMA_N(Y,t)|` exceeds the expanding 75th percentile of absolute displacement computed from prior observations only (minimum 50 prior observations). Over a horizon `H` following each event we measure two quantities: `C_W`, how far the filter moves toward the series, and `C_P`, how far the series moves toward the filter. The **filter-share** is

> **(EQ-1)** `S_W = Σ C_W / Σ (C_W + C_P)`,

the fraction of post-event gap-closure accomplished by the filter rather than the series, and `toward` is the fraction of events whose first post-event step moves the series toward the filter. A high `S_W` means the filter chases the series — the hallmark of a near-random-walk with no restoring force; a low `S_W` means the series returns to the filter — the hallmark of mean reversion. Events are non-overlapping and spaced at least `H` apart. All moving averages are computed on the continuous series; only the seasonal searches of Part 5 are season-bounded.

Unless stated otherwise, the decomposition uses `SMA-50` and `SMA-200` with `H = 63` days for daily series; influenza is pinned to `SMA-4`/`SMA-16` with `H = 13` weeks. As a control we generate a synthetic random walk (ten simulations matched to Colorado daily log-return drift and volatility, fixed seed 0); the framework treats this control as a tolerance band, not an exact target, because a pure random walk has no restoring force and should sit near `S_W` ≈ 100%, `toward` ≈ 50%.

### 2.2 Weather

Station temperature anomalies `(TMAX+TMIN)/2`, deseasonalized by day-of-year mean (Norwich CT and Dallas TX), set the low end of the scale: the deseasonalized filter-share band is {{LB-e1-weather-sw}}%. A daily temperature anomaly is close to white once the annual cycle is removed, so the filter does most of the chasing — the expected behavior for a weakly-persistent observable, and the calibration anchor against which the other domains are read.

### 2.3 Rivers

**2.3.1** River discharge carries persistence set by physical storage — snowpack, soil moisture, aquifers, and (for regulated rivers) reservoirs. We study daily log-discharge for the Colorado River (USGS 08158000, 1898–2026) and the Ohio River (USGS 03294500, 1928–2026), raw and deseasonalized by per-calendar-month mean.

**2.3.2** Raw discharge is dominated by the annual cycle; the seasonal variance fraction (one minus the variance ratio of deseasonalized to raw) is {{LB-e1-colorado-seasonal}}% for the Colorado and {{LB-e1-ohio-seasonal}}% for the more strongly seasonal Ohio.

**2.3.3** After deseasonalization the rivers occupy the middle of the scale. The Colorado's deseasonalized `SMA-200` filter-share is {{LB-e1-colorado-sw}}% and the Ohio's is {{LB-e1-ohio-sw}}% — intermediate between weather and influenza, consistent with storage-driven persistence that survives removal of the seasonal cycle.

**2.3.4** Deseasonalization separates genuine non-seasonal persistence from seasonal artifact. On the matched 1928–2026 period the deseasonalized Colorado-minus-Ohio filter-share gap widens with horizon — {{LB-e1-gradient-h42}} pp at `H = 42`, {{LB-e1-gradient-h63}} pp at `H = 63`, and {{LB-e1-gradient-h126}} pp at `H = 126` — corroborating, by an independent method, the out-of-sample hydrological persistence reported for these basins \cite{Kim-2026d}\cite{Koutsoyiannis-2005}\cite{O'Connell-2016}. (This matched-period sweep replaces an earlier, larger sweep that did not survive consistent re-computation; see §4.6.)

**2.3.5** A deseasonalization that used the full-sample monthly means would leak future information into the past. Re-running with strictly expanding (causal) monthly means changes the deseasonalized filter-share by only {{LB-e1-lookahead-co}} pp for the Colorado and {{LB-e1-lookahead-oh}} pp for the Ohio — within the load-bearing tolerance — so the decomposition is not an artifact of look-ahead in the seasonal adjustment.

### 2.4 Sunspots

Sunspots are oscillatory rather than mean-reverting, and their decomposition statistics are imported from the financial-and-natural-science reference paper rather than regenerated here: {{LB-e1-sunspot-decomp-cite}}. We flag this explicitly because the cited decomposition does not reproduce on the SILSO v2.0 series; what this paper regenerates for sunspots is the divergence-operator *sign* (Part 3), not the decomposition.

### 2.5 Influenza

Weekly national influenza-like-illness (`% WEIGHTED ILI`) sits at the extreme high end. Pinned to the reconstructed `SMA-4`/`SMA-16`, `H = 13` cell, the filter-share is {{LB-e1-flu-sw}}% with `toward` ≈ {{LB-e1-flu-toward}}% — the filter chases an explosively-rising series that does not return to it within the horizon, the signature of an observable with no stationary restoring force during an outbreak. (We report the single reconstructed cell; the wider range printed in the source paper was under-specified and is not claimed.)

### 2.6 The complete scale

The four domains order exactly as their physics predicts: weather (low `S_W`) → deseasonalized rivers (intermediate) → influenza (extreme), with the financial benchmark imported as a cited reference ({{LB-e1-financial-band-cite}}) and the synthetic random-walk control at {{LB-e1-rw-control}} anchoring the no-restoring-force end. The scale is built from a single operator applied identically; the ordering is not fitted.

---

## 3. The volatility-divergence operator and critical slowing down

### 3.1 Motivation

A single-window early-warning indicator — rising lag-1 autocorrelation or rising variance — asks whether a system is slowing down at one timescale \cite{Scheffer-2009}\cite{Dakos-2008}. The volatility-divergence operator compares *two* timescales: a fast trailing volatility minus a slow trailing volatility. When the fast volatility rises above the slow, short-horizon fluctuations are growing relative to the long-horizon baseline — a multi-scale generalization of CSD. The single-window CSD indicator is the special case in which the slow window is the whole sample, so the divergence operator is a superset \cite{Dakos-2012b}\cite{Dablander-2022}.

### 3.2 Methodology

The level divergence is

> **(EQ-2, generic form)** `vdiv(t; w_f, w_s) = std(Y', w_f, t) − std(Y', w_s, t)`,

where `std(Y',w,t)` is the trailing sample standard deviation over the most recent `w` observations and `Y'` is the domain's natural innovation representation. The physically meaningful volatility lives in different transforms in different domains, so we **document four domain-specific constructions** rather than force one generic operator (resolving an ambiguity in the source paper):

| Domain | Innovation `Y'` | Forward target | Windows |
|---|---|---|---|
| Hydrology | log-returns of discharge | forward returns-volatility | 12/63 d |
| Atmospheric | `TMAX` first-differences | forward 21-day realized vol | 21/252 d |
| Epidemiology | first-differences of %ILI | forward diff-volatility | 4/16 wk |
| Solar | yearly sunspot level | future level `Y(t+5)` | 3/11 yr |

We correlate each domain's `vdiv` with its forward target by subsampled Spearman correlation (non-overlapping subsamples where windows overlap), check sign stability across an in-sample/out-of-sample split at the temporal midpoint, and test against a block-shuffle null (blocks of 63, 1000 shuffles, seed 0, significance threshold `z = 2.0`). The CSD comparator is a trailing lag-1 autocorrelation (an AR(1) coefficient over a rolling slow window) correlated with **the same forward target the domain's `vdiv` predicts**; `vdiv` "outperforms" CSD when it carries the correct sign with magnitude exceeding the CSD's.

### 3.3 Results by domain

**3.3.1 Hydrology.** Under the pre-registered returns operator the volatility divergence is a significant signal on *both* rivers, and the more strongly seasonal Ohio is the stronger of the two: the Colorado returns-operator correlation is {{LB-e2-colorado-rho-returns}} and the Ohio is {{LB-e2-ohio-rho-returns}}. The apparent "Ohio null" of earlier work is an artifact of the **level** operator, which confounds volatility with the seasonal cycle: under the level operator the Ohio is {{LB-e2-ohio-rho-level}} and the Colorado is {{LB-e2-colorado-rho-level}}, and the Ohio level-operator value does not clear the block-shuffle null (`z` = {{LB-e2-ohio-blockshuffle-z}} < 2.0). The previously-reported Colorado value of +0.33 is a look-ahead artifact — the divergence correlated against its own contemporaneous fast volatility with no forward shift, which reproduces at {{LB-e2-colorado-artifact}} — not a forward-predictive signal (see §3.5 and §4.6). The corrected reading is that volatility-clustering is universal across both rivers and *stronger* for the more seasonal one; the level operator's apparent null is a seasonal confound, not absent structure.

**3.3.2 Atmospheric.** On raw temperature, the divergence is large but seasonal: the Dallas operator-B raw value is {{LB-e2-weather-dallas}}. Deseasonalizing by per-calendar-month z-score collapses it to {{LB-e2-weather-dallas-deseas}} — essentially zero — confirming that the raw signal was the annual cycle. For Norwich the raw value is {{LB-e2-weather-norwich-raw}}; the deseasonalized Norwich value is an **open** item, reproduced here at {{LB-e2-weather-norwich-deseas}}, below the larger figure reported in the source (which we have not been able to reproduce on the current record), so we soften that contrast rather than assert it.

**3.3.3 Epidemiology.** On first-differenced %ILI the divergence is a strong positive signal, {{LB-e2-flu-rho}}, and — as predicted for an explosively-growing observable with no stationary restoring force — the single-window CSD comparator carries the **opposite** (negative) sign, {{LB-e2-csd-epi}}. The divergence operator and the CSD indicator disagree in epidemiology precisely because epidemic growth is not a slowing-down phenomenon.

**3.3.4 Solar.** Sunspots are the one domain whose divergence carries a unique **negative** sign, {{LB-e2-sunspot-rho}} (permutation `z` = {{LB-e2-sunspot-permz}}), reflecting their oscillatory structure. The matched single-window CSD is also negative and smaller in magnitude, {{LB-e2-csd-solar}}, reproducing the source paper's "CSD also negative, lower magnitude" sub-claim once the comparator uses the same future-level target the solar divergence predicts.

### 3.4 Summary

In every domain the divergence operator carries the correct, ACF-consistent sign and outperforms the single-window CSD comparator at its own target; the CSD indicator is opposite-signed in epidemiology and lower-magnitude in solar physics. The operator's behavior tracks each series' autocorrelation structure rather than any per-domain tuning.

### 3.5 Bias audit

The largest correction in this work is in hydrology. The earlier "Colorado signal versus Ohio null" contrast arose from computing the two rivers with **different forward targets** — the Colorado against its own contemporaneous fast volatility (a look-ahead construction failing computational-integrity check 4, reproduced at {{LB-e2-colorado-artifact}}) and the Ohio against a genuine forward target. Applied consistently, the returns operator makes the Ohio the stronger signal and the level operator a seasonal-confound null for both rivers. We retain the look-ahead value in the committed analysis as a labeled reproduction of the artifact, not as a result. The Norwich deseasonalized value is flagged open rather than reported at the unreproduced source figure.

---

## 4. The persistence-sign rule

### 4.1 The rule

The framework's one cited theorem is a persistence-sign rule relating a level divergence to the future observable through the ACF \cite{Kim-2026d}. For the level divergence `D(t; w_f, w_s) = SMA_{w_f}(Y,t) − SMA_{w_s}(Y,t)` and the mean ACF over a lag window `R̄(a,b) = (1/(b−a)) Σ_{lag=a}^{b−1} ACF(lag)`,

> **(EQ-3)** `D(t; w_f, w_s) = SMA_{w_f}(Y,t) − SMA_{w_s}(Y,t)`,
> **(EQ-4, Theorem 8b)** `sign[ Corr(D_t, Y_{t+h}) ] = sign[ R̄(h, h+w_f) − R̄(h+w_f, h+w_s) ]`.

In words: whether a fast-minus-slow moving-average divergence predicts the future observable with a positive or negative sign is fixed by whether the near-lag mean autocorrelation exceeds the far-lag mean autocorrelation. The theorem is treated as prior art and **cited, not re-derived in the main text**; because this paper stands alone, its statement and a short proof are reproduced for completeness in Appendix B, and the proof is independently confirmed by a symbolic step-check and a numeric stress test (Appendix B, three-way verification).

### 4.2 Design

We test the rule on five systems — Colorado and Ohio (deseasonalized log-discharge), Norwich and Dallas (deseasonalized temperature anomaly), and influenza (raw weekly ILI) — across five forward horizons each, a pre-registered grid of 25 predictions. Daily systems use `w_f = 12`, `w_s = 63` and horizons `h ∈ {21, 42, 63, 126, 252}` days; influenza uses `w_f = 4`, `w_s = 16` and `h ∈ {4, 8, 13, 17, 26}` weeks. Sunspots are deliberately excluded from this grid.

### 4.3 Decision rule

A prediction is **correct** when the observed sign of the subsampled Spearman correlation `ρ(D(t), Y(t+h))` matches the sign the rule predicts from the mean ACF; **significance** requires `p < 0.05` with a Fisher-z 95% confidence interval excluding zero. The headline statistic is the significant-correct count. The in-paper falsifier is one statistically significant prediction whose observed sign contradicts the rule.

### 4.4 Results

The rule holds on every significant prediction: {{LB-e3-significant-correct}} of {{LB-e3-significant-total}} significant predictions correct, with {{LB-e3-significant-wrong}} significant wrong-signed predictions — the in-paper falsifier is not triggered ({{LB-e3-falsifier}}). Overall accuracy across all 25 predictions is {{LB-e3-overall}} of 25. The per-domain significant-correct breakdown is {{LB-e3-perdomain-significant}}, and the per-domain overall-correct breakdown is {{LB-e3-perdomain-correct}} (the weather stations contribute no statistically significant predictions but their signs are mostly correct).

### 4.5 Post-test: the two sign flips

Two predictions flip sign exactly where the mean-ACF structure says they should. The Colorado River at `h = 252` days flips to a negative observed sign ({{LB-e3-colorado-flip-sign}}); critically, this flip occurs because the near-lag mean ACF falls below the far-lag mean ACF **while the ACF itself remains positive** — there is no ACF zero-crossing on the Colorado (first zero-crossing: {{LB-e3-colorado-flip-acf}}). Influenza at `h = 26` weeks flips to a negative observed sign ({{LB-e3-flu-flip-sign}}) in the neighborhood of the seasonal ACF structure, whose first zero-crossing is at {{LB-e3-flu-flip-acf}} weeks — distinct from `h = 26`. We emphasize the Colorado mechanism because it is easy to misread a sign flip as a zero-crossing; here the flip is governed by the difference of mean autocorrelations, exactly as the rule states.

### 4.6 Correction note

A volatility-divergence formulation of the rule (volatility divergence predicting forward volatility, judged by the level-ACF criterion) is the documented rejected alternative. Its exact source-paper figures could not be reproduced and are under-determined by the original prose; three faithful constructions give a spread, and the value locked here is {{LB-e3-rejected-volform-pct}}% correct with {{LB-e3-rejected-volform-sigwrong}} significant wrong-signed predictions. The robust, reproduced contrast is what matters: the volatility formulation produces five or more significant *wrong*-signed predictions while the level formulation produces zero, confirming the level divergence predicting the future level as the correct application of the rule. The level formulation is primary throughout; the volatility formulation is reported as history at its regenerated value, not asserted at the source figure.

---

## 5. Applications

### 5.1 Influenza onset and peak detection

**5.1.0** The persistence-sign account predicts that a fast-minus-slow level divergence on an explosively-rising observable will move early — before a level threshold is crossed. Influenza onset is the natural test, and peak timing is the natural follow-up.

**5.1.1** Standard surveillance fires when prevalence crosses a level threshold — by which point the outbreak is already well underway — and the trailing average itself peaks *after* the true peak, a direct consequence of the lag the framework's own decomposition measures. The research literature offers more sophisticated alternatives, but their reported lead is modest: mechanistic state-space forecasts report peak-timing skill on the order of a couple of weeks up to somewhat over seven weeks ahead of the peak \cite{Shaman-Karspeck-2012}\cite{Shaman-2013}, metapopulation-mobility models forecast local onset roughly six weeks ahead \cite{Pei-2018}, and the Moving Epidemic Method adopted across European surveillance reports onset timeliness of about a week \cite{Vega-2013}; the closest methodological precedent is a single-EWMA control chart on laboratory-confirmed counts \cite{Steiner-2010}. The divergence detector instead fires on the change in slope, and (§5.1.2) obtains its lead with no epidemiological model, no parameter estimation, and no data beyond the ILI series itself.

**5.1.2** We define the onset divergence `D(t) = SMA_4(ILI,t) − SMA_12(ILI,t)` on the continuous weekly series (EQ-5), with the divergence onset the first week in a season at which `D(t) > 0.2` pp; the level comparator fires when ILI first exceeds the season's early baseline (mean of the first four weeks) by 1.0 pp. Across {{LB-e4-seasons}} paired seasons the divergence onset leads the season peak by {{LB-e4-div-lead}} weeks on average, versus {{LB-e4-level-lead}} weeks for the level comparator — an advantage of {{LB-e4-advantage}} weeks — and the divergence fires earlier in {{LB-e4-earlier}} of {{LB-e4-seasons}} seasons (paired `t` = {{LB-e4-paired-t}}). The minimum divergence lead over the peak is {{LB-e4-floor}} weeks and the first-quartile lead is {{LB-e4-q1}} weeks, so even the worst seasons retain a usable lead. This is obtained with no epidemiological model, no parameter estimation, and no data beyond the ILI series itself.

> **(EQ-5)** `D(t) = SMA_4(ILI,t) − SMA_12(ILI,t)`.

**5.1.3** The same construction applied to per-subtype percent-positivity identifies the dominant circulating strain. In clearly single-strain seasons the divergence-first-firing strain matches the dominant strain in {{LB-e5-single}} of nine seasons; against full-season hindsight dominance it matches in {{LB-e5-hindsight}} of {{LB-e4-seasons}} seasons, and in real time (cumulative positives at first firing) in {{LB-e5-realtime}} of {{LB-e4-seasons}} seasons. The strain signal fires at the same time as the aggregate onset (median lead {{LB-e5-lead}} weeks), so strain identification is available when onset is, not later. The proportional allocation of unsubtyped specimens is applied to the detection signal only; the dominant-strain ground truth uses raw confirmed-subtyped season totals \cite{Goldstein-2011}\cite{Kandula-2017}.

**5.1.4 Why early strain identification matters.** Onset and strain together give a public-health-relevant early read with simultaneous subtype information, complementary to pre-season subtype forecasting \cite{Gatti-2026}. The practical value is concrete: influenza subtypes differ in who they harm — H3N2 seasons fall hardest on the elderly, H1N1 disproportionately on younger adults — so knowing the accelerating strain weeks ahead of the peak lets hospital systems calibrate surge planning to the expected patient mix, lets pharmacies pre-position antivirals against the circulating strain's susceptibility profile, and lets agencies target messaging to the populations most at risk. Looking further out, mRNA vaccine platforms with demonstrated production timelines of roughly six to eight weeks could in principle use a mid-season strain signal to update composition before the peak — a possibility we flag, not a claim we test. This is a proof of concept on public surveillance data; clinical validation, regional and age-stratified performance, and false-positive characterization require collaboration with public-health agencies.

**5.1.5 Peak detection — a rejected hypothesis (reported honestly).** Whether the divergence helps detect the seasonal *peak* is a separate question, and the answer is no. The divergence zero-crossing does not lead the peak at all — its mean lead is {{LB-e6-zerocross}} weeks (negative: it *lags* the true peak), worse even than the naive SMA-4 peak's {{LB-e6-sma4peak}} weeks — so it is rejected as a peak marker (limit L-02). A secondary "divergence-peak leads the ILI peak" claim from the source does not reproduce under the pre-registered operator: the divergence peak precedes the ILI peak in only {{LB-e6-divpeak-precede}} of {{LB-e4-seasons}} seasons (paired `p` = {{LB-e6-divpeak-p}}, not significant), so we report it as an open non-reproduction rather than a lead. The early-onset result is unaffected; a trailing-average momentum filter structurally cannot lead its own reversal at the peak.

**5.1.6 Spatial-curvature peak detection — a pre-registered net-new test, reported as an honest negative.** Because the national signal is a population-weighted blur of staggered regional peaks, we pre-registered a strictly-causal spatial-curvature detector over the 10 HHS-region ILI curves, asking whether it leads the national peak. It does not, and we report that negative. The make-or-break feasibility diagnostic shows that only the single earliest region leads the nation meaningfully ({{LB-e7-feasibility-e1}} weeks), with the third-earliest region already coincident ({{LB-e7-feasibility-e3}} weeks), so a fire-when-θ-of-10-regions-have-turned detector has essentially no genuine headroom. The primary rollover detector *appears* to lead by {{LB-e7-spatial-primary}} weeks, but this is a regional-noise artifact: a national-only control under the identical rule does not lead at all (its mean lead is {{LB-e7-curvature-control}} weeks — negative), the apparent lead does not survive a genuine (frac=0.75) rollover threshold (robust-to-threshold = {{LB-e7-robust-threshold}}; the strict-rollover lead is not significant, `p` = {{LB-e7-robust-strictp}}), and there is no genuine feasibility headroom (genuine-headroom = {{LB-e7-robust-headroom}}). The verdict: {{LB-e7-verdict}}

**5.1.7** A leave-one-season-out targeted-region follow-up confirms the negative is complete rather than a wrong-tool artifact: there is no consistent geographic leader to exploit. The earliest-region concentration is not distinguishable from uniform (χ² = {{LB-e7b-chi2}}, `p` = {{LB-e7b-chi2-p}}), and a detector watching the consistently-early region(s) selected from other seasons collapses at a genuine rollover threshold exactly like the pool (`p` = {{LB-e7b-targeted-collapse-p}}). The conclusion: {{LB-e7b-verdict}} Spatial disaggregation does not yield a reliable causal lead on the national peak; the early-onset result (5.1.2) stands on its own.

### 5.2 Weather-to-river

The decomposition's ordering has a physical reading across domains: a weakly-persistent driver (temperature anomaly) feeding a storage system (a catchment) produces the intermediate persistence measured for deseasonalized discharge — the same restoring-force logic that orders the calibration scale, here connecting two of its rungs.

---

## 6. Synthesis

### 6.1 The unified cross-domain picture

Table 1 (**TBL-1**) collects, per system, the filter-share, the `toward` fraction, the divergence correlation (reported on the returns operator for the rivers, with the level-operator null noted), the persistence-sign result, the seasonality, and the governing ACF lags. The rivers are reported at the returns-operator values ({{LB-e2-ohio-rho-returns}} for the Ohio, {{LB-e2-colorado-rho-returns}} for the Colorado), with the financial and sunspot decomposition statistics imported as cited references and the Norwich deseasonalized value left open. The single thread running down the table is the autocorrelation structure of each observable.

### 6.2 The ACF is the unifying variable

![FIG-1 — deseasonalized ACFs of the Colorado, Ohio, and Dallas with the raw weekly influenza ACF on a common day-lag axis; the only zero-crossing marked is the genuine flu seasonal crossing at 14 weeks.](figure1.png)

Figure 1 (**FIG-1**) overlays the deseasonalized ACFs of the Colorado, the Ohio, Dallas, and influenza on a common lag axis. The figure makes the paper's central claim visible: the divergence operator's sign, magnitude, deseasonalization response, and failure modes in each domain are all read off the same curve. (The figure is regenerated for this paper without a spurious zero-crossing annotation present in the source; the Colorado sign flip is governed by the mean-ACF difference, not a zero-crossing — §4.5.)

### 6.3 Conclusions

**C-01** The autocorrelation function governs the divergence operator's qualitative behavior — sign, magnitude, deseasonalization response, and failure modes — across every domain tested, exactly as the persistence-sign rule predicts and as Figure 1 shows.

**C-02** The financial-market findings of the source framework are corroborated by external calibration: a tool derived where the physics is unknown recovers the independently-known restoring-force structure of four physical systems with no per-domain fitting of the decomposition or the persistence-sign rule.

**C-03** The framework has direct practical value outside finance: a divergence-based influenza-onset detector fires roughly {{LB-e4-advantage}} weeks earlier than level-based surveillance, with simultaneous dominant-strain identification.

### 6.4 Bias audit (synthesis level)

Two negatives and one large correction are load-bearing for honesty. Peak detection by the divergence (5.1.5) and by spatial disaggregation (5.1.6–5.1.7) both fail, and we report them as failures answering pre-registered questions; the hydrology operator correction (§3.5) reverses a headline contrast from the source. None of these touches the onset result or the persistence-sign rule, and stating them is what licenses confidence in what did hold.

### 6.5 Scope, assumptions, and limits of claim

*Assumptions (scope conditions).* **S1** — the observable's autocorrelation structure is approximately stationary over the sample. **S2** — deseasonalization (monthly-mean, day-of-year mean, or per-month z-score) adequately removes the seasonal cycle while preserving the stochastic departures. **S3** — the divergence operator requires sufficient autocorrelation structure; on the rivers the apparent null arises under the level operator (volatility confounded with the seasonal cycle), not from absent structure, and the returns operator recovers a significant signal in both rivers. **S4** — the forward-prediction test requires a genuine flu season (peak ILI at or above the activity floor); a low-activity season is untestable, not falsifying. **S5** — the decomposition and the persistence-sign rule are applied identically across all four domains; the divergence operator is adapted to each domain's natural innovation representation (log-returns, first-differences, or level), disclosed as such.

*Limits of claim.* **L-01** — no new mathematics; pre-existing theory is validated (Theorem 8b is cited). The decomposition and the persistence-sign rule are applied identically across domains; the divergence operator is domain-adapted. **L-02** — the divergence zero-crossing does **not** improve seasonal-peak detection. **L-03** — national-aggregate influenza data only; regional, age-stratified, and facility-level behavior is unknown. **L-04** — the retrospective lead-time is the evidentiary basis; the registered 2026–27 prediction is the unresolved out-of-sample test. **L-05** — the financial-market and sunspot-decomposition comparison values are cited from the source framework, not regenerated here. **L-06** — the Colorado divergence is reported at the defensible subsampled value, correcting the source's +0.33 look-ahead artifact; under any consistent operator the Ohio signal is at least as strong as the Colorado, and on the pre-registered returns operator the Ohio is the stronger. **L-07** — the Norwich deseasonalized-divergence contrast magnitude is unverified on the current record (reported at the reproduced value; the larger source figure is source-authentic but unreproduced). **L-08** — the sunspot "CSD also negative, lower magnitude" sub-claim is **retained** under the operator-matched comparison (negative, below the divergence magnitude); the load-bearing sunspot claim is the negative divergence sign, which reproduces.

---

## 7. Forward predictions (registered 2026–27 falsifier)

### 7.1 Why register

A retrospective fit, however clean, is weaker than a dated out-of-sample prediction a reader can run. We register two influenza predictions for the 2026–27 Northern-Hemisphere season, runnable from public CDC FluView data, tracked weekly. A confirmed onset-lead would show the operator captures a stable structural property of influenza dynamics rather than a historical fit; a strain miss in a clearly single-strain season would falsify the strain claim specifically while leaving the onset result intact. The full step-by-step replication protocol — data download, the national-region filter, the `SMA_4 − SMA_12` computation, and the lead and strain comparisons — is published with the dated registration and the weekly tracker at the coordinated launch, so the prediction is reader-runnable exactly as stated.

### 7.2 P1 — onset lead

The onset divergence (`SMA_4 − SMA_12` of weekly national ILI, threshold 0.2 pp) will fire at least six weeks before the level detector (early-season baseline + 1.0 pp), over MMWR weeks 40/2026–20/2027. The prediction is **falsified** if the lead is under six weeks or the divergence fires after the level detector; it is **untestable** (and carries forward) if peak ILI stays below 2.0%.

### 7.3 P2 — dominant strain

The first subtype whose percent-positivity divergence fires (threshold 0.3 pp) will match the full-season plurality strain. **Falsified** on a mismatch in a single-strain (>70%) season; **inconclusive** on a mismatch in a mixed season.

### 7.4 P3 — peak lead (not registered)

A 2026–27 peak-lead prediction was contingent on a positive retrospective spatial-curvature lead. Because that retrospective is an honest negative (5.1.6), **P3 is not registered** and is omitted from the falsifier set; the onset and strain predictions stand on their own.

---

## Acknowledgments and AI disclosure

This paper is part of the Lagging Truth research series by an independent researcher. Analysis, verification, and drafting were carried out with AI assistance under a disciplined research-to-publication protocol: every load-bearing number is generated by a committed script on hash-pinned public data and checked against a committed ledger by an automated verifier; the theorem is verified three independent ways (written proof, symbolic step-check, numeric stress test); and all non-reproductions and corrections are logged openly in the project's decision record. The author is responsible for all claims. No funding was received. All data are public (CDC FluView, NOAA GHCN-Daily, USGS NWIS, SIDC/SILSO).

---

## References

*Bibliographic formatting is finalized at Phase 5b; entries below carry the corrected author/title metadata tracked in the design record. Keys in brackets are the reconciliation identifiers.*

- **[Kim-2026a]** Kim, J. (2026). *Moving Averages Follow Price: a mathematical proof and empirical validation of the adaptation property in trailing averages.* Lagging Truth research series (working paper; full bibliographic details finalized at the coordinated launch).
- **[Kim-2026b]** Kim, J. (2026). *The Adaptation Rate Theorem: predictable lead times in multi-scale trailing measures.* Lagging Truth research series (working paper; details finalized at launch).
- **[Kim-2026c]** Kim, J. (2026). *Multi-Sensor Convergence as a Regime Detection Signal: the sensor convergence theorem.* Lagging Truth research series (working paper; details finalized at launch).
- **[Kim-2026d]** Kim, J. (2026). *The Divergence Theorem for regime-transition detection: multi-scale estimator disagreement as a cross-domain early-warning signal* — the persistence-sign rule (Theorem 8b) and the financial and sunspot reference values. Lagging Truth research series (working paper; details finalized at launch).
- **[Hurst-1951]** Hurst, H. E. (1951). Long-term storage capacity of reservoirs. *Transactions of the American Society of Civil Engineers*, 116, 770–808.
- **[Mandelbrot-Wallis-1968]** Mandelbrot, B. B., & Wallis, J. R. (1968). Noah, Joseph, and operational hydrology. *Water Resources Research*, 4(5), 909–918.
- **[Kaya-2025]** Kaya, Y. Z. (2025). Detection of trends and anomalies with MACD and RSI market indicators for temperature and precipitation. *Symmetry*, 17(8), 1268.
- **[Lo-MacKinlay-1988]** Lo, A. W., & MacKinlay, A. C. (1988). Stock market prices do not follow random walks: Evidence from a simple specification test. *Review of Financial Studies*, 1(1), 41–66.
- **[Hong-Satchell-2015]** Hong, K., & Satchell, S. (2015). Time series momentum trading strategy and autocorrelation amplification. *Quantitative Finance*, 15(9), 1471–1487.
- **[Ferreira-2019]** Ferreira, F. F., Silva, A. C., & Yen, J.-Y. (2019). Detailed study of a moving average trading rule. *arXiv:1907.00212*.
- **[Moskowitz-2012]** Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics*, 104(2), 228–250.
- **[Zakamulin-Giner-2020]** Zakamulin, V., & Giner, J. (2020). Trend following with momentum versus moving averages: a tale of differences. *Quantitative Finance*, 20(6), 985–1007.
- **[Corsi-2009]** Corsi, F. (2009). A simple approximate long-memory model of realized volatility. *Journal of Financial Econometrics*, 7(2), 174–196.
- **[Scheffer-2009]** Scheffer, M., Bascompte, J., Brock, W. A., et al. (2009). Early-warning signals for critical transitions. *Nature*, 461, 53–59.
- **[Dakos-2008]** Dakos, V., Scheffer, M., van Nes, E. H., et al. (2008). Slowing down as an early warning signal for abrupt climate change. *Proceedings of the National Academy of Sciences*, 105(38), 14308–14312.
- **[Dakos-2012a]** Dakos, V., Carpenter, S. R., Brock, W. A., et al. (2012). Methods for detecting early warnings of critical transitions in time series. *PLoS ONE*, 7(7), e41010.
- **[Dakos-2012b]** Dakos, V., van Nes, E. H., D'Odorico, P., & Scheffer, M. (2012). Robustness of variance and autocorrelation as indicators of critical slowing down. *Ecology*, 93(2), 264–271.
- **[Dablander-2022]** Dablander, F., Heesterbeek, H., Borsboom, D., & Drake, J. M. (2022). Overlapping timescales obscure early warning signals of the second COVID-19 wave. *Proceedings of the Royal Society B*, 289(1968), 20211809.
- **[Koutsoyiannis-2002]** Koutsoyiannis, D. (2002). The Hurst phenomenon and fractional Gaussian noise made easy. *Hydrological Sciences Journal*, 47(4), 573–595.
- **[Koutsoyiannis-2005]** Koutsoyiannis, D. (2005). Hydrologic persistence and the Hurst phenomenon. *Water Encyclopedia: Surface and Agricultural Water*, 5, 210–221.
- **[Koutsoyiannis-2006]** Koutsoyiannis, D. (2006). Nonstationarity versus scaling in hydrology. *Journal of Hydrology*, 324(1–4), 239–254.
- **[O'Connell-2016]** O'Connell, P. E., Koutsoyiannis, D., Lins, H. F., et al. (2016). The scientific legacy of Harold Edwin Hurst. *Hydrological Sciences Journal*, 61(9), 1571–1590.
- **[Shaman-Karspeck-2012]** Shaman, J., & Karspeck, A. (2012). Forecasting seasonal outbreaks of influenza. *Proceedings of the National Academy of Sciences*, 109(50), 20425–20430.
- **[Shaman-2013]** Shaman, J., Karspeck, A., Yang, W., et al. (2013). Real-time influenza forecasts during the 2012–2013 season. *Nature Communications*, 4, 2837.
- **[Pei-2018]** Pei, S., Kandula, S., Yang, W., & Shaman, J. (2018). Forecasting the spatial transmission of influenza in the United States. *Proceedings of the National Academy of Sciences*, 115(11), 2752–2757.
- **[Vega-2013]** Vega, T., Lozano, J. E., Meerhoff, T., Snacken, R., Mott, J., Ortiz de Lejarazu, R., Nunes, B., et al. (2013). Influenza surveillance in Europe: establishing epidemic thresholds by the Moving Epidemic Method. *Influenza and Other Respiratory Viruses*, 7(4), 546–558.
- **[Steiner-2010]** Steiner, S. H., Grant, K., Coory, M., & Kelly, H. A. (2010). Detecting the start of an influenza outbreak using exponentially weighted moving average charts. *BMC Medical Informatics and Decision Making*, 10, 37.
- **[Goldstein-2011]** Goldstein, E., Cobey, S., Takahashi, S., Miller, J. C., & Lipsitch, M. (2011). Predicting the epidemic sizes of influenza A/H1N1, A/H3N2, and B: a statistical method. *PLoS Medicine*, 8(7), e1001051.
- **[Kandula-2017]** Kandula, S., Yang, W., & Shaman, J. (2017). Type- and subtype-specific influenza forecast. *American Journal of Epidemiology*, 185(5), 395–402.
- **[Gatti-2026]** Gatti, L., Koenen, M., Zhang, D., Baguelin, M., & Pebody, R. G. (2026). Characterization and forecast of global influenza subtype dynamics. *Nature Health*, 1, 69.
- **[Boettiger-Hastings-2012]** Boettiger, C., & Hastings, A. (2012). Quantifying limits to detection of early warning for critical transitions. *Journal of the Royal Society Interface*, 9(75), 2527–2539.
- **[Boettiger-Ross-Hastings-2013]** Boettiger, C., Ross, N., & Hastings, A. (2013). Early warning signals: the charted and uncharted territories. *Theoretical Ecology*, 6(3), 255–264.
- **[Hsiang-2016]** Hsiang, S. (2016). Climate econometrics. *Annual Review of Resource Economics*, 8, 43–75.
- **[Li-2025]** Li, Y. (2025). Operator analysis of MACD. *arXiv:2509.21326*.

---

## Appendix A — Data and reproduction

**A.1 Data sources.** CDC FluView ILINet (national `% WEIGHTED ILI`, 1997–2026; and the 10 HHS-region series for the spatial test); CDC NREVSS subtype counts (pre-2015 and post-2015 national files); NOAA GHCN-Daily `TMAX`/`TMIN`; USGS NWIS daily discharge (Colorado 08158000, Ohio 03294500); SIDC/SILSO yearly mean total sunspot number, v2.0. All series are pulled and hash-pinned (MD5 + SHA256) before analysis; scripts read only the hashed copies.

**A.2 Weather stations.** Six GHCN-Daily stations are used across the paper: New York `USW00094728`, Blue Hill `USC00190736`, San Francisco `USW00023272`, Philadelphia `USW00013739`, Dallas `USW00003927` (the DAL-FTW WSCMO record), and Norwich `USC00065910`. The calibration scale (Part 2) and the persistence-sign grid (Part 4) use Norwich and Dallas; the divergence operator (Part 3) uses all six.

**A.3 Seasons.** The onset comparison (E4) draws on 29 candidate influenza seasons (1997-98 through the partial 2025-26) and enters {{LB-e4-seasons}} into the paired comparison after excluding 2020-21 (peak below 2.0%) and 2009-10 (no level-based onset). The strain (E5), peak (E6), and spatial (E7) analyses use the complete-through-2024 season set.

**A.4 Reproduction.** Every load-bearing number in this paper is produced by a committed script (`analysis/e1…e7`), wired to its input hashes and expected value in `analysis/claims.lock`, and checked by `analysis/verify.py`, which re-hashes the inputs, re-runs each script, and compares every value to the ledger within tolerance. Numbers in the text are rendered from the ledger by `analysis/render_claims.py`; none is typed by hand.

---

## Appendix B — The persistence-sign rule: statement, proof, and three-way verification

**Theorem 8b (persistence-sign rule).** Let `{Y_t}` be weakly stationary with autocovariance `γ(k) = Cov(Y_t, Y_{t+k}) = σ² ρ(k)`, where `ρ` is the autocorrelation function and `σ² = Var(Y_t) > 0`. For window lengths `w_f < w_s`, let `SMA_w(Y,t) = (1/w) Σ_{i=0}^{w-1} Y_{t-i}` and let the level divergence be `D_t = SMA_{w_f}(Y,t) − SMA_{w_s}(Y,t)`. Define the mean ACF over a lag window `R̄(a,b) = (1/(b−a)) Σ_{lag=a}^{b−1} ρ(lag)`. Then for any forward horizon `h ≥ 1`,

`sign[ Corr(D_t, Y_{t+h}) ] = sign[ R̄(h, h+w_f) − R̄(h+w_f, h+w_s) ]`.

**Proof.** Center `Y` (the correlation is invariant to the mean). For a single moving average,

`Cov(SMA_w(Y,t), Y_{t+h}) = (1/w) Σ_{i=0}^{w-1} Cov(Y_{t-i}, Y_{t+h}) = (1/w) Σ_{i=0}^{w-1} γ(h+i) = σ² · (1/w) Σ_{lag=h}^{h+w-1} ρ(lag) = σ² · R̄(h, h+w).`

Applying this to both windows of the divergence,

`Cov(D_t, Y_{t+h}) = σ² · [ R̄(h, h+w_f) − R̄(h, h+w_s) ].`

Split the slow-window mean ACF at `h + w_f`:

`R̄(h, h+w_s) = (1/w_s) [ Σ_{lag=h}^{h+w_f-1} ρ(lag) + Σ_{lag=h+w_f}^{h+w_s-1} ρ(lag) ] = (1/w_s) [ w_f · R̄(h, h+w_f) + (w_s − w_f) · R̄(h+w_f, h+w_s) ].`

Substituting,

`R̄(h, h+w_f) − R̄(h, h+w_s) = R̄(h, h+w_f) (1 − w_f/w_s) − ((w_s − w_f)/w_s) R̄(h+w_f, h+w_s) = ((w_s − w_f)/w_s) [ R̄(h, h+w_f) − R̄(h+w_f, h+w_s) ].`

Therefore

`Cov(D_t, Y_{t+h}) = σ² · ((w_s − w_f)/w_s) · [ R̄(h, h+w_f) − R̄(h+w_f, h+w_s) ].`

Both `σ² > 0` and `(w_s − w_f)/w_s > 0` (since `w_s > w_f`), and the correlation equals the covariance divided by the positive product of standard deviations, so `sign[ Corr(D_t, Y_{t+h}) ] = sign[ R̄(h, h+w_f) − R̄(h+w_f, h+w_s) ]`. Writing the near-lag and far-lag mean ACFs as `R̄_near = R̄(h, h+w_f)` and `R̄_far = R̄(h+w_f, h+w_s)`, the sign of the divergence-to-future correlation equals `sign(R̄_near − R̄_far)`. ∎

**Three-way verification.** Consistent with the project's proof-retention rule, the theorem is checked three independent ways and all three agree: (1) the written proof above; (2) a symbolic step-check (`analysis/checks/theorem8b_symbolic.py`) that reduces `Cov(SMA_{w_f} − SMA_{w_s}, Y_{t+h})` to `((w_s − w_f)/w_s)(R̄_near − R̄_far)` and confirms the difference simplifies to zero over a grid of `(w_f, w_s, h)` values; and (3) a numeric stress test (`analysis/checks/theorem8b_stress.py`) that confirms, on autoregressive processes with closed-form ACFs (including deliberately oscillatory cases), that the ACF-derived sign predicts the empirically-measured sign of `Corr(D_t, Y_{t+h})`, including the predicted sign flips. The result of each check is recorded in `verification/theorem8b_three_way.md`.

---

*Draft manuscript — Cross-Domain Validation. Standard v1.8, Phase 4. Numbers rendered from `analysis/claims.lock`; reconciled against `OUTLINE.md` by `analysis/verify.py --paper`.*
