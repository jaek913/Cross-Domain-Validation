# Cross-Domain Validation of a Moving-Average Divergence Framework

Replication package for the paper *"Cross-Domain Validation of a Moving-Average
Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and
Epidemiology."* Every quantitative claim in the manuscript is generated from data
by the scripts in `analysis/`, locked in `analysis/claims.lock`, and checked
end-to-end by `analysis/verify.py`.

## Layout

- `paper/` - manuscript: `paper.md` is the token-bearing source, `paper.rendered.md`
  the rendered copy, plus `figure1.png` and `paper_companion.md`.
- `analysis/` - generating scripts `e1_*` .. `e7b_*`; shared `data_io.py` and
  `operators.py`; `build_claims.py` (writes the lock); `render_claims.py` (renders
  the manuscript); `make_fig1.py`; `claims.lock`; `outputs/*.json`; `checks/`
  (Theorem 8b symbolic + stress checks); `fixtures/` (verifier self-test).
- `data/` - `pull.py` (assembles + hashes the inputs) and `SOURCES.md` (the
  generated, hashed data record). No raw data is committed.
- `verification/` - the adversarial-review record and the three-way theorem cross-check.
- Root `DESIGN.md` / `OUTLINE.md` / `COVERAGE.md` / `THESIS.md` / `DECISIONS.md` -
  design, manifest, coverage map, thesis statement, and the append-only decision log.

## Requirements

Python 3.12.10. Install the pinned dependencies into a clean virtual environment:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
python -m pip install -U pip
pip install -r requirements.txt
```

## Data

Raw data is **not** committed. It is assembled into a project-local store (an
absolute path given by the `LT_CDV_DATA` environment variable) by `data/pull.py`,
which also writes the hashed record `data/SOURCES.md`. The store holds 13 input
files across five domains: USGS daily discharge (x2), NOAA GHCN-Daily temperature
(x6), CDC ILINet (national + 10 HHS regions), CDC NREVSS (pre-/post-2015), and
SILSO yearly sunspot number. Every file is identity-checked against fixed
reproduction anchors on each `pull.py` run, and its SHA256 is pinned in
`analysis/claims.lock`.

Two of the sources are live and revised over time: NOAA appends recent days, and
CDC revises ILINet/NREVSS retrospectively. The analysis truncates every series to a
fixed coverage anchor (USGS/NOAA: 2026-03-18; ILINet: first 1,484 weeks, to 2026w09;
solar: year <= 2008), so **every result reproduces exactly even though a fresh
download's raw bytes may differ** from the pinned hashes. `SOURCES.md` records the
per-series replicator tolerance and the public provenance needed to obtain
equivalent data. The exact hash-pinned snapshot is the fixed input to the verifier
(and is deposited alongside the paper at release).

## Reproduce (clean clone)

1. Clone the repository to a fresh directory and create the environment (above).
2. Point `LT_CDV_DATA` at the directory holding the hash-pinned data snapshot:
   ```
   $env:LT_CDV_DATA = "C:\path\to\Cross-Domain-Validation-data"
   ```
3. Run the full gate:
   ```
   python analysis\verify.py --paper paper\paper.md
   ```
   Expected: `VERIFY: PASS`, with (1) input integrity 13/13, (2a) re-run scripts
   8/8, (2b) reproduction 74/74, (3) CIC signed 8/8, (4) theorem checks 2/2, and
   (5) paper reconciliation 12/12 (76 LB tokens, 34 citation keys, 16 sections,
   23 FIG/TBL/EQ/S/C/L anchors; no surviving placeholders). `claims.lock` carries
   78 rows (design v0.10).
4. (Optional) regenerate the derived artifacts and confirm they are unchanged:
   ```
   python analysis\build_claims.py            # rewrites claims.lock from outputs/
   python analysis\render_claims.py paper\paper.md paper\paper.rendered.md
   python analysis\make_fig1.py               # rewrites paper\figure1.png
   ```

`verify.py` also self-tests: `python analysis\verify.py --selftest` must turn every
deliberately broken fixture RED.

## Re-acquiring the data

`data/pull.py` re-stages the inputs and regenerates `SOURCES.md`: it downloads the
NOAA GHCN and SILSO series directly and copies the USGS/CDC series from a local
shared source folder (configured by the `LT_CDV_DATA` (output store) and `LT_CDV_SHARED`
(shared source folder) environment variables, defaulting to the author's paths if unset). `SOURCES.md` records
the public provenance for each series so an independent party can obtain equivalent
data. Because the live sources move, a fresh pull reproduces every result (after
truncation to the coverage anchors) but not necessarily the raw byte hashes, so the
GREEN gate above runs against the deposited snapshot.

## What verify.py checks

(1) re-hashes every input file in `LT_CDV_DATA` against `claims.lock`; (2) re-runs
all eight generating scripts and compares every regenerated value to the lock within
tolerance; (3) confirms each experiment's seven computational-integrity flags are
signed; (4) runs the Theorem 8b symbolic and stress checks; (5) reconciles the
manuscript against `OUTLINE.md` and the lock - every claim token resolves, no
placeholder survives, and all required sections, citation keys, and FIG/TBL/EQ/S/C/L
anchors are present.

## Forward predictions

Section 7 registers two dated, falsifiable predictions - P1 (influenza onset lead)
and P2 (dominant-strain identification) - resolved on the finalized CDC FluView data
in the first release on or after 1 September 2027. P3 (spatial peak lead) is reported
as an honest negative and is not registered.

## Licensing

USGS, NOAA, and CDC inputs are U.S.-government public-domain works. SILSO sunspot
data is CC BY-NC 4.0 (attribute SILSO/SIDC) and is not committed.
