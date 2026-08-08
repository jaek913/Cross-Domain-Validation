# REPLICATION.md - Cross-Domain Validation
Version 1.0 - 2026-08-08. ASCII-only. This document makes the paper
rebuildable from text: it consolidates the environment, the committed
scripts, the hashed inputs, the run commands, and the verification levels.
The frozen operators, decision rules, and dated amendments live in DESIGN.md
and DECISIONS.md, and COVERAGE.md maps every argument to its experiment -
this document POINTS to them and never restates them, so it cannot drift
from the record.

## 0. Environment

- OS: Windows 11 (author machine); analyses are pure Python and run on any OS.
- Python 3.12 with the versions in requirements.txt.
- Repo: github.com/jaek913/Cross-Domain-Validation.
- Data store: git-ignored; every input series pinned by SHA-256 in the data
  dictionary (data/), with source identities, ranges, and replicator
  tolerances per series. Raw data are public scientific and surveillance
  records (NOAA, USGS, SILSO/sunspots, CDC FluView) plus documented exports.
- Every analysis writes JSON to analysis/outputs/ (committed).

## 1. The contract

A number may appear in the paper only if a committed script, run on hashed
input data, regenerates it on demand. The canonical manuscript
(paper/Cross-Domain-Validation.md) carries {{LB-id}} tokens;
analysis/render_claims.py substitutes the ledger's locked values
(python analysis/render_claims.py paper/Cross-Domain-Validation.md
paper/Cross-Domain-Validation.rendered.md), so the paper and the verified
ledger can never drift. analysis/claims.lock is the ledger;
analysis/verify.py regenerates and re-verifies every value on demand and is
itself run against a deliberately broken fixture it must fail.

## 2. Analysis scripts (committed; outputs in analysis/outputs/)

| Script | Subject |
|---|---|
| analysis/operators.py + data_io.py | Shared operator library and hashed-data IO |
| analysis/e1_calibration_decomposition.py | Restoring-force calibration decomposition across the four domains |
| analysis/e2_volatility_divergence_csd.py | Volatility divergence vs critical slowing down |
| analysis/e3_theorem8b_sign.py | The pre-registered 25-prediction persistence-sign grid |
| analysis/e4_flu_onset.py | Influenza onset detector (reference implementation for registered prediction P1) |
| analysis/e5_strain_id.py | Dominant-strain identification (reference implementation for registered prediction P2) |
| analysis/e6_peak_detection.py | Spatial-curvature peak-detection hypothesis (pre-registered; honest negative) |
| analysis/e7_spatial_peak.py + e7b_regional_consistency.py | Spatial disaggregation and regional consistency |
| analysis/checks/theorem8b_symbolic.py + theorem8b_stress.py | Symbolic + numeric checks of Theorem 8b (reconciled in verification/theorem8b_three_way.md) |
| analysis/make_fig1.py | Figure 1 generator (paper/figure1.png) |

## 3. Build chain

```
python analysis/render_claims.py paper/Cross-Domain-Validation.md paper/Cross-Domain-Validation.rendered.md
python analysis/verify.py        # full verification (see the script header for modes)
.\build_pdf.ps1                  # series PDF (Cambria preamble, stale-output
                                 #   guard, PDF-only conformance transforms)
```

## 4. Registered predictions, reviews, and records

PREDICTIONS.md at the repo root is the dated public registration of the
paper's two 2026-27 influenza predictions (P1 onset lead, P2 dominant
strain), with a reader-runnable protocol and a single-vintage lock date of
2027-09-01; PREDICTIONS_TRACKER.md tracks provisional weekly values. The
capped adversarial review record is committed verbatim in verification/,
with the author's per-finding dispositions. Citations were verified under
the tiered protocol described in the Disclosure. CORRECTIONS.md at the repo
root is the public post-publication log.
