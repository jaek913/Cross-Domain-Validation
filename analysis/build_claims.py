#!/usr/bin/env python3
"""build_claims.py - Phase-3 ledger builder for the Cross-Domain-Validation paper.

Produces analysis/claims.lock (JSON): one row per load-bearing number, wired to
its generating script, the SHA256 of its input data, the regenerated expected
value, a tolerance, a provenance tag (regenerate / cite / open / negative /
theorem-check), and a reference to the per-experiment 7-point CIC block.

GENERATED ARTIFACT CONTRACT
  - claims.lock is produced ONLY by this committed builder and is NEVER hand-edited.
  - Expected values are read from the committed analysis/outputs/*.json at build
    time (so the ledger is a snapshot of the regenerated results). verify.py then
    RE-RUNS each script and checks the fresh output against this lock within tol.
  - Input hashes are parsed from data/SOURCES.md (the Phase-2 hashed-data manifest).
  - The 7-point CIC flags are signed here (the committing author's attestation);
    verify.py checks every flag is present and signed.

Run:  python build_claims.py          # writes analysis/claims.lock
      python build_claims.py --check  # dry-run: resolve every path, do not write

Standard v1.8 - Phase 3. Empirical-with-verified-theory archetype (Theorem 8b is
cited, not re-derived; it carries a registered numeric stress + symbolic step-check).
"""
from __future__ import annotations
import json, re, sys, hashlib, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent           # analysis/
REPO = HERE.parent                                # repo root
OUTDIR = HERE / "outputs"
SOURCES_MD = REPO / "data" / "SOURCES.md"
LOCK_PATH = HERE / "claims.lock"

SIGNOFF = {"signer": "Jae Kim", "orcid": "0009-0005-3260-7880"}
DESIGN_VERSION = "v0.10"
SOURCE_PIN_SHA256 = "982176a228c35cd76856b76fee17433ad5f6312e3490bf58f893dc17c3302a50"

# --------------------------------------------------------------------------- #
# 1. SOURCES.md parser -> {store_filename: {sha256, md5, bytes, anchor}}        #
# --------------------------------------------------------------------------- #
def parse_sources(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    # split into per-series sections at the markdown H2 headers
    sections = re.split(r"\n##\s+", text)
    out = {}
    for sec in sections:
        m_store = re.search(r"store path:\*\*\s*`[^`]*[\\/]([^\\/`]+)`", sec)
        m_sha = re.search(r"\*\*SHA256:\*\*\s*`([0-9a-fA-F]+)`", sec)
        if not (m_store and m_sha):
            continue
        fname = m_store.group(1).strip()
        m_md5 = re.search(r"\*\*MD5:\*\*\s*`([0-9a-fA-F]+)`", sec)
        m_bytes = re.search(r"\*\*Bytes:\*\*\s*([\d,]+)", sec)
        m_anchor = re.search(r"\*\*Reproduction anchor:\*\*\s*(.+)", sec)
        out[fname] = {
            "store_file": fname,
            "sha256": m_sha.group(1).lower(),
            "md5": (m_md5.group(1).lower() if m_md5 else None),
            "bytes": (int(m_bytes.group(1).replace(",", "")) if m_bytes else None),
            "anchor": (m_anchor.group(1).strip() if m_anchor else None),
        }
    return out

# --------------------------------------------------------------------------- #
# 2. path resolver into a loaded JSON (list-of-keys; keys may contain . / spaces)#
# --------------------------------------------------------------------------- #
def get_path(obj, path):
    cur = obj
    for k in path:
        if isinstance(k, int):
            cur = cur[k]
        else:
            if not isinstance(cur, dict) or k not in cur:
                raise KeyError(f"path miss at {k!r} in {path}")
            cur = cur[k]
    return cur

# --------------------------------------------------------------------------- #
# 3. CIC - the 7 classes, signed per generating script                          #
#    classes: 1 re-exec | 2 align | 3 nan/gap | 4 look-ahead | 5 overlap |      #
#             6 record/station boundaries | 7 input integrity                   #
# --------------------------------------------------------------------------- #
def cic(script, f1, f2, f3, f4, f5, f6, f7):
    keys = ["1_reexecutes", "2_index_alignment", "3_nan_gap", "4_no_lookahead",
            "5_overlap_consistency", "6_record_boundaries", "7_input_integrity"]
    notes = [f1, f2, f3, f4, f5, f6, f7]
    flags = {}
    for k, n in zip(keys, notes):
        status = "n/a" if n.startswith("N/A") else "pass"
        flags[k] = {"status": status, "note": n}
    return {"script": script, "flags": flags}

CIC_SPEC = {
    "E1": cic("analysis/e1_calibration_decomposition.py",
        "deterministic; expanding-75th-pctile event rule; RW control seed=0 reproduces.",
        "deseason via day-of-year / per-month groupby aligns on the index; events spaced >= H; no truncation onto a gap-filtered series.",
        "TMAX&TMIN both-present filter; valid (>0) discharge only; expanding window min 50 prior obs.",
        "event threshold = EXPANDING 75th pctile (prior obs only); look-ahead robustness shows causal-vs-full S_W delta <= 1.2pp.",
        "N/A - decomposition events are non-overlapping by construction (spaced >= H); RW control is a tolerance band, not an exact match.",
        "each station / gauge / series decomposed separately; no computation across record boundaries.",
        "obs counts match SOURCES anchors (CO 46767, OH 35862, flu 1484 wk, Norwich 22636, Dallas 26625)."),
    "E2": cic("analysis/e2_volatility_divergence_csd.py",
        "deterministic; sub-21 sampling; block-shuffle nsh=1000 seed=0 reproduces.",
        "log-returns / first-difference shift drops the first obs; the forward target is shifted; sub-21 sampling is on the aligned index.",
        "returns/first-diff dropna; per-month / day-of-year deseason; dropna before each correlation.",
        "THE D01/CIC#4 GUARD: the forward target is strictly future (forward vol / future level Y(t+5)); the v4 +0.33 (vdiv vs its OWN CONTEMPORANEOUS std(12)) is recorded as v4_artifact_contemp_fast and is NOT used as a result.",
        "sub-21 non-overlapping value cross-checked against the overlapping value (D01: overlap ~ subsample in every cell).",
        "computed per station / gauge / domain; no cross-record computation.",
        "obs counts match anchors; solar filtered to year<=2008 (n=294)."),
    "E3": cic("analysis/e3_theorem8b_sign.py",
        "deterministic; subsample every 21 (daily) / 8 (flu); 5 systems x 5 horizons = 25.",
        "D(t)=SMA_wf-SMA_ws vs Y(t+h) aligned by the h-shift; subsample on the aligned index.",
        "dropna on the (D, Y_{t+h}) pairs before Spearman.",
        "D is built from data <= t; Y_{t+h} is the prediction TARGET (not an input to D); no future leakage into the predictor.",
        "subsample stride 21/8 is SHORTER than the slow window (63/16), so adjacent subsamples' divergence windows OVERLAP -> the parametric Fisher-z significance is anti-conservative and DEMOTED to a cross-check (Phase-5a); the load-bearing backbone is the predicted SIGN + IS/OOS sign-stability (all 13 significant predictions sign-consistent across both temporal halves) + the causal-deseasonalization recompute (no significant-correct verdict flips). A moving-block bootstrap was attempted and rejected as the wrong tool for a theory-derived correlation (DECISIONS 2026-06-29).",
        "computed per system; sunspots are NOT in the E3 set; no cross-record computation.",
        "obs counts match anchors; ACF max-lag 400 daily / 60 flu covers h+w_s (315 / 42)."),
    "E4": cic("analysis/e4_flu_onset.py",
        "deterministic; 27 paired seasons; random-onset-week shuffle (seed 0) is a non-load-bearing diagnostic.",
        "SMA_4/SMA_12 on the CONTINUOUS weekly series; only the onset SEARCH is season-bounded; no index truncation.",
        "seasons require >= 20 weeks and peak ILI >= 2.0%; 2020-21 (peak<2.0%) and 2009-10 (no level onset) excluded.",
        "D(t)=SMA_4-SMA_12 from data <= t; the level baseline uses only the season's first 4 weeks (wk40-43); the peak is the target.",
        "N/A - one onset per season; no overlapping-subsample issue.",
        "national ILINet only; no cross-record computation.",
        "1484 weeks; 29 candidate -> 28 with valid peak -> 27 paired (DISC-1.4-03)."),
    "E5": cic("analysis/e5_strain_id.py",
        "deterministic; complete seasons through 2024 (n=27).",
        "A(Subtyping not Performed) allocated per-week to the subtyped H1:H3 split on the SIGNAL only; SMA_4/SMA_12 on the continuous percent-positive series.",
        "pre-2015 + post-2015 NREVSS merged; overlapping weeks resolved to the post-2015 file; dropna on per-subtype series.",
        "real-time leader = cumulative positives AT first firing (data <= t); hindsight dominance = raw confirmed-subtyped SEASON totals, explicitly labeled as hindsight ground truth.",
        "N/A - one firing per season per subtype.",
        "national NREVSS only; pre/post-2015 file boundary handled (no double-count); no cross-record computation.",
        "pre-2015 940 wk + post-2015 544 wk = 1484; dominance on raw subtyped counts."),
    "E6": cic("analysis/e6_peak_detection.py",
        "deterministic; 27 complete seasons (identical E5/E7 set).",
        "SMA_4/SMA_12 on the continuous series; lead = peak-wk - detector-wk on the aligned weekly index.",
        "seasons >= 20 wk, peak >= 2.0%; dropna.",
        "zero-crossing / divergence-peak / SMA-4 peak all from data <= t; the true ILI peak is the target.",
        "N/A - one detection per season.",
        "national ILINet only; no cross-record computation.",
        "27 seasons; zero-crossing lag -5.07 and SMA-4 lag -2.15 reproduce v4 (~-5.6 / -2.1)."),
    "E7": cic("analysis/e7_spatial_peak.py",
        "deterministic; net-new; 27 complete seasons; 10 HHS regions.",
        "each regional SMA_4/SMA_12 aligned 1:1 to the national week index; lead = national-peak-pos - detector-pos.",
        "10 regions complete over the window; momentum rollover guarded by the E4 onset (onset_pp=0.2).",
        "THE D01 LESSON, LOAD-BEARING: every regional turn from data <= t; the running-max is causal; the feasibility diagnostic is HINDSIGHT and labeled; the finished season is NEVER used to label a region peaked.",
        "N/A - one fire per season; the robustness check sweeps frac {0.25/0.5/0.75} and theta {0.2/0.3/0.5/0.7} as declared sensitivity.",
        "computed per region; the national TARGET is the pinned ILINet.csv (identical national peak to E6); no cross-record computation.",
        "10 HHS regions x 1484 weeks; 27 complete-through-2024 seasons inside the stable window."),
    "E7b": cic("analysis/e7b_regional_consistency.py",
        "deterministic; leave-one-season-out region selection; 27 seasons, 10 regions; same operators/season set as E7.",
        "each regional SMA_4/SMA_12 aligned 1:1 to the national week index; identical alignment to E7.",
        "10 regions complete over the window; dropna; chi-square on earliest-credit counts.",
        "CIC#4 GUARD: the targeted region(s) are selected from the OTHER 26 seasons ONLY (true leave-one-out); the in-sample ceiling is explicitly labeled OVERFIT-PRONE and is NOT the reported result.",
        "N/A - one fire per season; the frac sweep {0.5/0.75} is a declared sensitivity.",
        "computed per region; the national TARGET is the pinned ILINet.csv (identical national peak to E6/E7); no cross-record computation.",
        "10 HHS regions x 1484 weeks; 27 complete-through-2024 seasons; identical to E7."),
}

# --------------------------------------------------------------------------- #
# 4. The load-bearing-number registry. Each row:                                #
#    id, exp, out (output json filename), path (list of keys), value-derivation #
#    is by reading `path` from the output at build time; check + tol + prov +   #
#    inputs (SOURCES store filenames) + lb (DESIGN section6 id) + claim.         #
#    check in {num,int,bool,contains,num_list,int_dict,null,band,cite}.          #
# --------------------------------------------------------------------------- #
GHCN = {  # convenience
    "NYC": "ghcn_USW00094728.csv", "BlueHill": "ghcn_USC00190736.csv",
    "SF": "ghcn_USW00023272.csv", "Philly": "ghcn_USW00013739.csv",
    "Dallas": "ghcn_USW00003927.csv", "Norwich": "ghcn_USC00065910.csv",
}
CO = "usgs_08158000.rdb"; OH = "usgs_03294500.rdb"
ILI = "ILINet.csv"; ILIHHS = "ILINet_HHS.csv"
NREVSS = ["ICL_NREVSS_Combined_prior_to_2015_16.csv", "ICL_NREVSS_Public_Health_Labs.csv"]
SILSO = "silso_yearly.csv"

def R(id, exp, out, path, check, prov, inputs, lb, claim, tol=None, band_path=None):
    return dict(id=id, exp=exp, out=out, path=path, check=check, prov=prov,
                inputs=inputs, lb=lb, claim=claim, tol=tol, band_path=band_path)

CLAIMS = [
    # ---- E1 calibration-scale decomposition --------------------------------
    R("LB-e1-weather-sw", "E1", "e1_calibration.json", ["weather", "_band_S_W_pct"],
      "num_list", "regenerate", [GHCN["Norwich"], GHCN["Dallas"]], "LB-2/LB-3",
      "weather deseasonalized S_W band (Norwich/Dallas); paper band ~2.5-5.2%", tol=0.1),
    R("LB-e1-colorado-seasonal", "E1", "e1_calibration.json",
      ["rivers", "Colorado", "seasonal_variance_fraction_pct"], "num", "regenerate",
      [CO], "LB-2/LB-5", "Colorado seasonal variance fraction (~15.5%)", tol=0.1),
    R("LB-e1-colorado-sw", "E1", "e1_calibration.json",
      ["rivers", "Colorado", "cells", "deseas", "SMA-200", "S_W"], "num", "regenerate",
      [CO], "LB-2", "Colorado deseasonalized SMA-200 S_W", tol=0.05),
    R("LB-e1-ohio-seasonal", "E1", "e1_calibration.json",
      ["rivers", "Ohio", "seasonal_variance_fraction_pct"], "num", "regenerate",
      [OH], "LB-2/LB-5", "Ohio seasonal variance fraction (~45.7%)", tol=0.1),
    R("LB-e1-ohio-sw", "E1", "e1_calibration.json",
      ["rivers", "Ohio", "cells", "deseas", "SMA-200", "S_W"], "num", "regenerate",
      [OH], "LB-2", "Ohio deseasonalized SMA-200 S_W", tol=0.05),
    R("LB-e1-flu-sw", "E1", "e1_calibration.json", ["flu", "cells", "SMA-4", "S_W"],
      "num", "regenerate", [ILI], "LB-4", "flu pinned-cell S_W (~153.7%)", tol=0.1),
    R("LB-e1-flu-toward", "E1", "e1_calibration.json", ["flu", "cells", "SMA-4", "toward"],
      "num", "regenerate", [ILI], "LB-4", "flu pinned-cell toward (~13%)", tol=0.1),
    R("LB-e1-gradient-h42", "E1", "e1_calibration.json",
      ["gradient", "matched_1928_2026", "H=42", "gap_pp"], "num", "regenerate",
      [CO, OH], "LB-5/DISC-1.4-01", "matched CO-OH gradient gap H=42 (+3.9pp)", tol=0.1),
    R("LB-e1-gradient-h63", "E1", "e1_calibration.json",
      ["gradient", "matched_1928_2026", "H=63", "gap_pp"], "num", "regenerate",
      [CO, OH], "LB-5/DISC-1.4-01", "matched CO-OH gradient gap H=63 (+4.6pp)", tol=0.1),
    R("LB-e1-gradient-h126", "E1", "e1_calibration.json",
      ["gradient", "matched_1928_2026", "H=126", "gap_pp"], "num", "regenerate",
      [CO, OH], "LB-5/DISC-1.4-01", "matched CO-OH gradient gap H=126 (+6.4pp)", tol=0.1),
    R("LB-e1-rw-control", "E1", "e1_calibration.json",
      ["rw_control", "SMA-200", "S_W_mean"], "band", "regenerate", [CO],
      "LB-e1-rw-control", "RW control SMA-200 S_W mean within band ~88-115% (seed 0)",
      band_path=["rw_control", "SMA-200", "S_W_range"]),
    R("LB-e1-lookahead-co", "E1", "e1_calibration.json",
      ["lookahead_robustness", "Colorado", "delta_pp"], "num", "regenerate", [CO],
      "DISC-1.4-02", "Colorado look-ahead S_W delta (<=1.2pp)", tol=0.05),
    R("LB-e1-lookahead-oh", "E1", "e1_calibration.json",
      ["lookahead_robustness", "Ohio", "delta_pp"], "num", "regenerate", [OH],
      "DISC-1.4-02", "Ohio look-ahead S_W delta (<=1.2pp)", tol=0.05),
    R("LB-e1-sunspot-decomp-cite", "E1", "e1_calibration.json",
      ["cited_not_regenerated", "sunspot_decomposition"], "cite", "cite", [], "LB-2",
      "sunspot decomposition S_W/toward = cited Paper-4 reference (not regenerated)"),
    R("LB-e1-financial-band-cite", "E1", "e1_calibration.json",
      ["cited_not_regenerated", "financial_S_W_band"], "cite", "cite", [], "LB-2",
      "financial S_W band = cited Paper-4 reference (~64-167%, not regenerated)"),

    # ---- E2 volatility-divergence operators + CSD --------------------------
    R("LB-e2-colorado-rho-returns", "E2", "e2_divergence_csd.json",
      ["hydrology", "Colorado", "returns_op", "sub21_raw"], "num", "regenerate", [CO],
      "LB-8/D01", "Colorado returns-op vdiv = the signal (+0.12)", tol=0.01),
    R("LB-e2-colorado-rho-level", "E2", "e2_divergence_csd.json",
      ["hydrology", "Colorado", "level_op", "sub21_raw"], "num", "regenerate", [CO],
      "LB-8/D01", "Colorado level-op vdiv = the seasonal-confound null (~ -0.00)", tol=0.01),
    R("LB-e2-colorado-artifact", "E2", "e2_divergence_csd.json",
      ["hydrology", "Colorado", "v4_artifact_contemp_fast", "raw"], "num", "regenerate",
      [CO], "LB-8", "v4 +0.33 reproduced as the CIC#4 look-ahead artifact (~+0.322)", tol=0.01),
    R("LB-e2-ohio-rho-returns", "E2", "e2_divergence_csd.json",
      ["hydrology", "Ohio", "returns_op", "sub21_raw"], "num", "regenerate", [OH],
      "LB-9/D01", "Ohio returns-op vdiv = the strongest hydrology signal (~+0.30)", tol=0.01),
    R("LB-e2-ohio-rho-level", "E2", "e2_divergence_csd.json",
      ["hydrology", "Ohio", "level_op", "sub21_raw"], "num", "regenerate", [OH],
      "LB-9/D01", "Ohio level-op vdiv = the seasonal-confound null (+0.047)", tol=0.01),
    R("LB-e2-ohio-blockshuffle-z", "E2", "e2_divergence_csd.json",
      ["block_shuffle_null", "Ohio_deseas", "z"], "num", "regenerate", [OH], "LB-9",
      "Ohio level-op block-shuffle z (<2.0, the null holds)", tol=0.05),
    R("LB-e2-weather-dallas", "E2", "e2_divergence_csd.json",
      ["weather", "Dallas_TX", "operator_B_design", "raw"], "num", "regenerate",
      [GHCN["Dallas"]], "LB-10", "Dallas operator-B raw vdiv (+0.745)", tol=0.01),
    R("LB-e2-weather-dallas-deseas", "E2", "e2_divergence_csd.json",
      ["weather", "Dallas_TX", "operator_B_design", "deseas_zdiff"], "num", "regenerate",
      [GHCN["Dallas"]], "LB-10", "Dallas operator-B deseasonalized vdiv (collapse -> ~0)", tol=0.01),
    R("LB-e2-weather-norwich-raw", "E2", "e2_divergence_csd.json",
      ["weather", "Norwich_CT", "operator_B_design", "raw"], "num", "regenerate",
      [GHCN["Norwich"]], "LB-10", "Norwich operator-B raw vdiv (+0.40)", tol=0.01),
    R("LB-e2-weather-norwich-deseas", "E2", "e2_divergence_csd.json",
      ["weather", "Norwich_CT", "operator_B_design", "deseas_zdiff"], "num", "open",
      [GHCN["Norwich"]], "LB-10/DISC-1.5-02",
      "OPEN: Norwich deseasonalized vdiv ~+0.05 (v4 +0.232 not confirmed; contrast softened)", tol=0.01),
    R("LB-e2-flu-rho", "E2", "e2_divergence_csd.json",
      ["epidemiology", "first_diff_op", "% WEIGHTED ILI", "rho"], "num", "regenerate",
      [ILI], "LB-11", "epidemiology first-diff vdiv (+0.39 weighted)", tol=0.01),
    R("LB-e2-sunspot-rho", "E2", "e2_divergence_csd.json", ["solar", "vdiv_rho"],
      "num", "regenerate", [SILSO], "LB-12", "sunspot vdiv = the unique negative sign (-0.230)", tol=0.01),
    R("LB-e2-sunspot-permz", "E2", "e2_divergence_csd.json", ["solar", "perm_z"],
      "num", "regenerate", [SILSO], "LB-12", "sunspot vdiv permutation z (-3.94)", tol=0.05),
    R("LB-e2-csd-epi", "E2", "e2_divergence_csd.json", ["csd", "epidemiology", "csd_rho"],
      "num", "regenerate", [ILI], "LB-11/13", "epidemiology CSD = opposite (negative) sign (~ -0.165)", tol=0.01),
    R("LB-e2-csd-solar", "E2", "e2_divergence_csd.json", ["csd", "solar", "csd_rho"],
      "num", "regenerate", [SILSO], "LB-12/D02",
      "sunspot CSD RETAINED: negative, lower magnitude than vdiv (-0.103, matched future-level target)", tol=0.01),

    # ---- E3 Theorem-8b persistence-sign (in-paper falsifier) ---------------
    R("LB-e3-significant-correct", "E3", "e3_theorem8b.json", ["summary", "significant_correct"],
      "int", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-14",
      "significant-correct count (13/13)"),
    R("LB-e3-significant-total", "E3", "e3_theorem8b.json", ["summary", "significant_total"],
      "int", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-14",
      "significant total (13)"),
    R("LB-e3-significant-wrong", "E3", "e3_theorem8b.json", ["summary", "significant_wrong"],
      "int", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-14",
      "significant-WRONG count (0 - the in-paper falsifier is not triggered)"),
    R("LB-e3-overall", "E3", "e3_theorem8b.json", ["summary", "total_correct"],
      "int", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-15",
      "overall correct (20 of 25)"),
    R("LB-e3-perdomain-significant", "E3", "e3_theorem8b.json", ["summary", "per_domain_significant"],
      "int_dict", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-17",
      "per-domain significant-correct (CO5/OH3/Nor0/Dal0/Flu5)"),
    R("LB-e3-perdomain-correct", "E3", "e3_theorem8b.json", ["summary", "per_domain_correct"],
      "int_dict", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-17",
      "per-domain correct (CO5/OH5/Nor3/Dal2/Flu5)"),
    R("LB-e3-colorado-flip-sign", "E3", "e3_theorem8b.json",
      ["summary", "colorado_h252_flip", "observed_sign"], "int", "regenerate", [CO], "LB-16/DISC-1.4-04",
      "Colorado h=252 sign flip (-1)"),
    R("LB-e3-colorado-flip-acf", "E3", "e3_theorem8b.json",
      ["summary", "colorado_h252_flip", "acf_first_zero_crossing"], "null", "regenerate", [CO],
      "DISC-1.4-04", "Colorado ACF has NO zero-crossing (flip = Rbar_near<Rbar_far, ACF positive)"),
    R("LB-e3-flu-flip-sign", "E3", "e3_theorem8b.json",
      ["summary", "flu_h26_flip", "observed_sign"], "int", "regenerate", [ILI], "LB-16/DISC-1.4-05",
      "flu h=26 sign flip (-1)"),
    R("LB-e3-flu-flip-acf", "E3", "e3_theorem8b.json",
      ["summary", "flu_h26_flip", "acf_first_zero_crossing"], "int", "regenerate", [ILI],
      "DISC-1.4-05", "flu ACF zero-crossing at 14 wk (distinct from h=26)"),
    R("LB-e3-falsifier", "E3", "e3_theorem8b.json", ["summary", "in_paper_falsifier_triggered"],
      "bool", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-14",
      "in-paper falsifier triggered = false (no significant wrong-sign prediction)"),
    R("LB-e3-rejected-volform-pct", "E3", "e3_theorem8b.json",
      ["summary", "rejected_vol_formulation", "pct"], "num", "open",
      [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "E3-rejected-volform",
      "OPEN: rejected vol-formulation correct-pct (v4 ~44% not reproduced; regenerated ~72%)", tol=0.5),
    R("LB-e3-rejected-volform-sigwrong", "E3", "e3_theorem8b.json",
      ["summary", "rejected_vol_formulation", "significant_wrong_fisher"], "int", "open",
      [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "E3-rejected-volform",
      "OPEN: rejected vol-formulation significant-wrong (>=5 vs the level form's 0 - contrast holds)"),
    R("LB-e3-isoos-consistent", "E3", "e3_theorem8b.json", ["summary", "isoos_consistent_among_significant"],
      "int", "regenerate", [CO, OH, GHCN["Norwich"], GHCN["Dallas"], ILI], "LB-14",
      "IS/OOS sign-stable among the significant predictions (13/13; the block-independent backbone of the sign claim)"),
    R("LB-e3-causal-sigcorrect-flips", "E3", "e3_theorem8b.json",
      ["summary", "causal_deseason_robustness", "n_significant_correct_flips"], "int", "regenerate",
      [CO, OH, GHCN["Norwich"], GHCN["Dallas"]], "LB-14",
      "causal (expanding) deseasonalization flips 0 significant-correct verdicts (5a 4A robustness)"),
    R("LB-e3-causal-obs-flips", "E3", "e3_theorem8b.json",
      ["summary", "causal_deseason_robustness", "n_observed_sign_flips"], "int", "regenerate",
      [CO, OH, GHCN["Norwich"], GHCN["Dallas"]], "LB-14",
      "causal deseasonalization flips only 2/20 daily observed signs (both non-significant near-zero weather)"),

    # ---- E4 divergence-based flu onset (load-bearing) ----------------------
    R("LB-e4-div-lead", "E4", "e4_flu_onset.json", ["divergence_lead_vs_peak", "mean"],
      "num", "regenerate", [ILI], "LB-18", "divergence onset lead-vs-peak (14.1 wk)", tol=0.05),
    R("LB-e4-level-lead", "E4", "e4_flu_onset.json", ["level_lead_vs_peak", "mean"],
      "num", "regenerate", [ILI], "LB-18", "level onset lead-vs-peak (5.9 wk)", tol=0.05),
    R("LB-e4-advantage", "E4", "e4_flu_onset.json", ["advantage_div_minus_level", "mean"],
      "num", "regenerate", [ILI], "LB-18", "divergence advantage over level (+8.2 wk)", tol=0.05),
    R("LB-e4-earlier", "E4", "e4_flu_onset.json", ["advantage_div_minus_level", "earlier"],
      "int", "regenerate", [ILI], "LB-18", "divergence fires earlier in 26 of 27 seasons"),
    R("LB-e4-paired-t", "E4", "e4_flu_onset.json", ["advantage_div_minus_level", "paired_t"],
      "num", "regenerate", [ILI], "LB-18", "paired t for the advantage (9.35)", tol=0.05),
    R("LB-e4-seasons", "E4", "e4_flu_onset.json", ["n_paired"], "int", "regenerate", [ILI],
      "DISC-1.4-03", "27 paired seasons (29 candidate - 2020-21 - 2009-10)"),
    R("LB-e4-floor", "E4", "e4_flu_onset.json", ["divergence_lead_vs_peak", "floor_min"],
      "num", "regenerate", [ILI], "LB-19", "minimum divergence lead-vs-peak (floor 5 wk)", tol=0.05),
    R("LB-e4-q1", "E4", "e4_flu_onset.json", ["divergence_lead_vs_peak", "q1"],
      "num", "regenerate", [ILI], "LB-19", "Q1 divergence lead-vs-peak (~12 wk)", tol=0.05),
    R("LB-e4-adv-lvl-low", "E4", "e4_flu_onset.json", ["level_sensitivity", "lvl+0.5", "advantage_mean"],
      "num", "regenerate", [ILI], "LB-18",
      "onset advantage at the LOOSER level threshold (+0.5pp): lower bound of the symmetric-sweep range (~5.3 wk)", tol=0.05),
    R("LB-e4-adv-lvl-high", "E4", "e4_flu_onset.json", ["level_sensitivity", "lvl+1.5", "advantage_mean"],
      "num", "regenerate", [ILI], "LB-18",
      "onset advantage at the STRICTER level threshold (+1.5pp): upper bound of the symmetric-sweep range (~9.7 wk)", tol=0.05),

    # ---- E5 strain-level divergence ----------------------------------------
    R("LB-e5-single", "E5", "e5_strain_id.json", ["single_strain", "hit"], "int", "regenerate",
      NREVSS, "LB-20", "single-strain anchor (9/9, reproduces exactly)"),
    R("LB-e5-hindsight", "E5", "e5_strain_id.json", ["hindsight", "match"], "int", "regenerate",
      NREVSS, "LB-20", "hindsight dominant-strain matches (19/27, as-regenerated)"),
    R("LB-e5-realtime", "E5", "e5_strain_id.json", ["realtime", "match"], "int", "regenerate",
      NREVSS, "LB-20", "real-time dominant-strain matches (24/27, as-regenerated)"),
    R("LB-e5-lead", "E5", "e5_strain_id.json", ["strain_fire_vs_aggregate_onset", "lead_median"],
      "num", "regenerate", NREVSS, "LB-21", "strain-fire vs aggregate-onset lead median (0 wk)", tol=0.01),

    # ---- E6 peak-detection (honest negative) -------------------------------
    R("LB-e6-zerocross", "E6", "e6_peak_detection.json", ["divergence_zerocross_lead", "mean"],
      "num", "regenerate", [ILI], "ARG-12", "zero-crossing lead (lags -5.07 wk; rejected; reproduces)", tol=0.05),
    R("LB-e6-sma4peak", "E6", "e6_peak_detection.json", ["sma4_peak_lead", "mean"],
      "num", "regenerate", [ILI], "ARG-12", "SMA-4 peak lead (lags -2.15 wk)", tol=0.05),
    R("LB-e6-divpeak-precede", "E6", "e6_peak_detection.json", ["divergence_peak_lead", "precede_count"],
      "int", "open", [ILI], "LB-e6-divpeak", "OPEN: divergence-peak precedes only 7/27 (v4 96% not reproduced)"),
    R("LB-e6-divpeak-p", "E6", "e6_peak_detection.json", ["divergence_peak_lead", "paired_p"],
      "num", "open", [ILI], "LB-e6-divpeak", "OPEN: divergence-peak lead is not significant (p=0.17)", tol=0.01),

    # ---- E7 spatial-curvature peak detection (net-new; honest negative) ----
    R("LB-e7-feasibility-e1", "E7", "e7_spatial_peak.json",
      ["LB_e7_feasibility", "earliest_region_leads_by_rank", "earliest_1", "median"], "num", "negative",
      [ILIHHS, ILI], "LB-e7-feasibility", "only the single earliest region leads (~5 wk)", tol=0.05),
    R("LB-e7-feasibility-e3", "E7", "e7_spatial_peak.json",
      ["LB_e7_feasibility", "earliest_region_leads_by_rank", "earliest_3", "median"], "num", "negative",
      [ILIHHS, ILI], "LB-e7-feasibility", "theta=0.3 detector feasibility headroom ~0 (3rd-earliest median 0)", tol=0.05),
    R("LB-e7-spatial-primary", "E7", "e7_spatial_peak.json",
      ["LB_e7_spatial_lead", "spatial_momentum_rollover_PRIMARY", "mean"], "num", "negative",
      [ILIHHS, ILI], "LB-e7-spatial-lead", "PRIMARY rollover APPEARS to lead (+4.2) but is NOT robust (see robustness)", tol=0.05),
    R("LB-e7-curvature-control", "E7", "e7_spatial_peak.json",
      ["LB_e7_spatial_lead", "national_rollover_CONTROL", "mean"], "num", "negative",
      [ILIHHS, ILI], "LB-e7-curvature", "national-only control LAGS (-1.37) under the identical rule", tol=0.05),
    R("LB-e7-robust-threshold", "E7", "e7_spatial_peak.json",
      ["robustness_check", "robust_to_threshold"], "bool", "negative", [ILIHHS, ILI],
      "LB-e7-spatial-lead", "H0 anchor: the lead does NOT survive a genuine (frac=0.75) rollover"),
    R("LB-e7-robust-headroom", "E7", "e7_spatial_peak.json",
      ["robustness_check", "genuine_headroom"], "bool", "negative", [ILIHHS, ILI],
      "LB-e7-feasibility", "H0 anchor: there is no genuine feasibility headroom"),
    R("LB-e7-robust-strictp", "E7", "e7_spatial_peak.json",
      ["robustness_check", "strict_rollover_p_vs0"], "num", "negative", [ILIHHS, ILI],
      "LB-e7-spatial-lead", "the genuine-rollover lead is not significant (p=0.49)", tol=0.01),
    R("LB-e7-verdict", "E7", "e7_spatial_peak.json", ["verdict"], "contains", "negative",
      [ILIHHS, ILI], "ARG-15", "H0 / ARTIFACT verdict (apparent lead is a regional-noise artifact)"),

    # ---- E7b regional-consistency diagnostic (confirms H0 complete) --------
    R("LB-e7b-chi2", "E7b", "e7b_regional_consistency.json",
      ["part_a_consistency", "concentration", "chi2"], "num", "negative", [ILIHHS, ILI],
      "ARG-15 (diagnostic)", "earliest-region concentration chi-square (13.96)", tol=0.1),
    R("LB-e7b-chi2-p", "E7b", "e7b_regional_consistency.json",
      ["part_a_consistency", "concentration", "p_value"], "num", "negative", [ILIHHS, ILI],
      "ARG-15 (diagnostic)", "concentration not distinguishable from uniform (p=0.12): no consistent leader", tol=0.01),
    R("LB-e7b-targeted-collapse-p", "E7b", "e7b_regional_consistency.json",
      ["part_b_targeted_loo", "K_1", "frac_0.75", "p_vs0"], "num", "negative", [ILIHHS, ILI],
      "ARG-15 (diagnostic)", "leave-one-out targeted detector collapses at frac=0.75 (p=0.94)", tol=0.01),
    R("LB-e7b-verdict", "E7b", "e7b_regional_consistency.json", ["verdict"], "contains", "negative",
      [ILIHHS, ILI], "ARG-15 (diagnostic)", "NO CONSISTENT LEADER verdict (pooled H0 robust and complete)"),
]

# Theorem-8b machine-checks (Phase-3 proof-check part 1 of 3): registered like
# any empirical check; verify.py runs the scripts and requires a clean exit.
THEOREM_CHECKS = [
    dict(id="THM-8b-stress", kind="theorem-check", check="script",
         script="checks/theorem8b_stress.py",
         claim="Theorem-8b numeric stress: the sign rule sign[Corr(D,Y_{t+h})]="
               "sign[Rbar_near-Rbar_far] holds from a known ACF across an AR-grid, "
               "incl. a deliberate sign-flip case; finite-sample sim confirms.",
         lb="LB-14/LB-16 (Theorem 8b)"),
    dict(id="THM-8b-symbolic", kind="theorem-check", check="script",
         script="checks/theorem8b_symbolic.py",
         claim="Theorem-8b symbolic step-check: Cov(SMA_wf-SMA_ws, Y_{t+h}) reduces "
               "to ((ws-wf)/ws)*(Rbar_near - Rbar_far) in ACF terms, so the sign "
               "equals sign(Rbar_near - Rbar_far). sympy simplify == 0 over a (wf,ws,h) grid.",
         lb="LB-14/LB-16 (Theorem 8b)"),
]

# --------------------------------------------------------------------------- #
def build(check_only=False):
    sources = parse_sources(SOURCES_MD)
    outputs_cache, missing_files, claim_rows, errors = {}, [], {}, []

    # validate every claim's inputs are known in SOURCES
    for c in CLAIMS:
        for fn in c["inputs"]:
            if fn not in sources:
                errors.append(f"{c['id']}: input {fn!r} not found in SOURCES.md")

    for c in CLAIMS:
        out = c["out"]
        if out not in outputs_cache:
            p = OUTDIR / out
            if not p.exists():
                errors.append(f"{c['id']}: output {out} not found")
                outputs_cache[out] = None
            else:
                outputs_cache[out] = json.loads(p.read_text(encoding="utf-8"))
        data = outputs_cache[out]
        if data is None:
            continue
        try:
            value = get_path(data, c["path"])
        except (KeyError, IndexError, TypeError) as e:
            errors.append(f"{c['id']}: {e}")
            continue
        row = {
            "claim": c["claim"], "experiment": c["exp"], "provenance": c["prov"],
            "script": CIC_SPEC[c["exp"]]["script"] if c["exp"] in CIC_SPEC else None,
            "output": f"outputs/{out}", "json_path": c["path"], "check": c["check"],
            "value": value, "design_lb": c["lb"], "cic_ref": c["exp"],
            "inputs": {fn: sources[fn]["sha256"] for fn in c["inputs"] if fn in sources},
        }
        if c["tol"] is not None:
            row["tol"] = c["tol"]
        if c["check"] == "band" and c["band_path"]:
            try:
                row["band"] = get_path(data, c["band_path"])
            except Exception as e:
                errors.append(f"{c['id']}: band {e}")
        claim_rows[c["id"]] = row

    for t in THEOREM_CHECKS:
        claim_rows[t["id"]] = {
            "claim": t["claim"], "experiment": "THM", "provenance": t["kind"],
            "script": t["script"], "check": t["check"], "design_lb": t["lb"],
            "cic_ref": "THM", "value": "clean-exit-required",
        }

    if errors:
        print("BUILD ERRORS (no lock written):")
        for e in errors:
            print("  -", e)
        sys.exit(2)

    today = datetime.date.today().isoformat()
    signed_cic = {}
    for exp, blk in CIC_SPEC.items():
        signed_cic[exp] = {**blk, "signed_by": f"{SIGNOFF['signer']} / ORCID {SIGNOFF['orcid']}",
                           "signed_date": today}

    n_prov = {}
    for r in claim_rows.values():
        n_prov[r["provenance"]] = n_prov.get(r["provenance"], 0) + 1

    lock = {
        "_meta": {
            "paper": "Cross-Domain Validation of a Moving-Average Divergence Framework "
                     "in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology",
            "standard": "v1.8", "phase": 3, "design_version": DESIGN_VERSION,
            "source_pin_sha256": SOURCE_PIN_SHA256,
            "generated_by": "analysis/build_claims.py",
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "warning": "GENERATED ARTIFACT - DO NOT HAND-EDIT. Regenerate via build_claims.py.",
            "n_claims": len(claim_rows), "n_by_provenance": n_prov,
            "provenance_tiers": {
                "regenerate": "value regenerated from in-manifest hashed data; verify must reproduce within tol",
                "cite": "Paper-4 reference import; displayed, not regenerated, no numeric check",
                "open": "does NOT reproduce the v4 figure; the as-regenerated value is locked + flagged in DECISIONS",
                "negative": "honest-negative / artifact disposition; the negative (booleans/values) is locked + must reproduce",
                "theorem-check": "registered numeric stress / symbolic step-check script; must exit clean",
            },
            "signoff": {**SIGNOFF, "date": None,
                        "note": "Phase-3 gate sign-off pending verify.py green + reviewer; CIC flags signed at build."},
        },
        "inputs": sources,
        "cic": signed_cic,
        "claims": claim_rows,
    }

    print(f"Resolved {len(claim_rows)} ledger rows; provenance counts: {n_prov}")
    print(f"Inputs parsed from SOURCES.md: {len(sources)} series.")
    if check_only:
        print("--check: all paths resolved; lock NOT written.")
        return
    LOCK_PATH.write_text(json.dumps(lock, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    h = hashlib.md5(LOCK_PATH.read_bytes()).hexdigest()
    print(f"WROTE {LOCK_PATH}  ({LOCK_PATH.stat().st_size} bytes, MD5 {h})")


if __name__ == "__main__":
    build(check_only=("--check" in sys.argv))
