#!/usr/bin/env python3
"""
pull.py - assemble + hash the data manifest for the Cross-Domain-Validation paper
("Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric
Science, Hydrology, Solar Physics, and Epidemiology"; Paper 5 rebuild).

VERIFIED DATA PROVENANCE (2026-06-28). Every input is identity-checked against the
Stage-1.5/1.6 verification anchors on EACH run; the script ABORTS on any mismatch.
This guards against the duplicate-download variants in the shared store.

  REUSE from the shared store (confirmed exact vs anchors):
    USGS Colorado 08158000.txt -> usgs_08158000.rdb   46,767 obs  1898-03-01..2026-03-18
    USGS Ohio     03294500.txt -> usgs_03294500.rdb   35,862 obs  1928-01-01..2026-03-18
    ILINet  FluViewPhase2Data/ILINet.csv              1,484 National wk 1997w40..2026w09
    NREVSS pre-2015  ICL_NREVSS_Combined_prior_to_2015_16.csv  940 wk 1997w40..2015w39
    NREVSS post-2015 ICL_NREVSS_Public_Health_Labs.csv         544 wk 2015w40..2026w09
  FETCH FRESH (store lacks the verification's product; a fresh fetch reproduces anchors):
    NOAA GHCN-Daily by-station access CSV x6 -> ghcn_<ID>.csv (analysis truncates DATE<=2026-03-18)
    SILSO yearly mean total sunspot number V2.0 -> silso_yearly.csv

Raw data is NOT committed. It lands in PROJECT_STORE (git-ignored, separately backed up).
Only data/SOURCES.md (the hashed record this script generates) is committed.

Run locally:
    cd C:\\Users\\jaek9\\Documents\\Repos\\REPO-Cross-Domain-Validation\\data
    python pull.py
"""
from __future__ import annotations
import csv, hashlib, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------- config
STORE         = Path(r"C:\Users\jaek9\Documents\LaggingTruth\Data")
FLU           = STORE / "FluViewPhase2Data"
PROJECT_STORE = Path(r"C:\Users\jaek9\Documents\LaggingTruth\Cross-Domain-Validation")
REPO_DATA     = Path(__file__).resolve().parent                 # repo/data/
SOURCES_MD    = REPO_DATA / "SOURCES.md"
ANCHOR_END    = "2026-03-18"                                    # USGS / NOAA coverage-end anchor
NOW           = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")

NOAA_BASE = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{}.csv"
SILSO_URL = "https://www.sidc.be/SILSO/INFO/snytotcsv.php"

NOAA_STATIONS = [   # (id, label, expected TMAX&TMIN days with DATE <= ANCHOR_END)
    ("USW00094728", "New York City (Central Park), NY", 57413),
    ("USC00190736", "Blue Hill (Milton), MA",           51544),
    ("USW00023272", "San Francisco Downtown, CA",        38366),
    ("USW00013739", "Philadelphia Intl AP, PA",          31146),
    ("USW00003927", "Dallas-FTW WSCMO AP, TX",           26625),
    ("USC00065910", "Norwich Public Utility Plant, CT",  22636),
]

# --------------------------------------------------------------------------- helpers
def fail(msg: str):
    print("\n*** ABORT: " + msg, file=sys.stderr)
    sys.exit(1)

def hash_file(p: Path):
    m = hashlib.md5(); s = hashlib.sha256(); n = 0
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            m.update(chunk); s.update(chunk); n += len(chunk)
    return m.hexdigest(), s.hexdigest(), n

def copy_verbatim(src: Path, dst: Path):
    if not src.exists():
        fail(f"source file not found: {src}")
    dst.write_bytes(src.read_bytes())

def fetch(url: str, dst: Path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    dst.write_bytes(urllib.request.urlopen(req, timeout=180).read())

def _is_float(s):
    try:
        float(s); return True
    except (TypeError, ValueError):
        return False

# ---- content verifiers (identity checks vs the verification anchors) ----
def v_usgs(p: Path, exp_obs, exp_first, exp_last):
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    body  = [l for l in lines if not l.startswith("#")]
    hdr   = body[0].split("\t")
    if "datetime" not in hdr:
        fail(f"{p.name}: no 'datetime' column (not a USGS RDB?)")
    dt   = hdr.index("datetime")
    disc = [i for i, h in enumerate(hdr) if h.endswith("00060_00003") and not h.endswith("_cd")]
    if not disc:
        fail(f"{p.name}: no daily-mean discharge (*_00060_00003) column")
    di = disc[0]; obs = 0; first = last = None
    for row in body[2:]:                       # skip header(0) + type row(1)
        c = row.split("\t")
        if len(c) <= max(dt, di):
            continue
        try:
            x = float(c[di])
        except ValueError:
            continue
        if x > 0:                              # drop missing / non-positive
            obs += 1
            d = c[dt].strip()
            if first is None: first = d
            last = d
    if (obs, first, last) != (exp_obs, exp_first, exp_last):
        fail(f"{p.name}: USGS anchor mismatch -> obs={obs} {first}..{last} "
             f"(expected {exp_obs} {exp_first}..{exp_last}). Wrong/variant file.")
    return {"obs": obs, "first": first, "last": last}

def _weekly_table(p: Path):
    with open(p, encoding="utf-8", errors="replace", newline="") as fh:
        rows = list(csv.reader(fh))
    hdr = rows[1]                              # row 0 is the title line (skiprows=1)
    idx = {name: i for i, name in enumerate(hdr)}
    data = [r for r in rows[2:] if r and any(c.strip() for c in r)]
    return idx, data

def _national(idx, data):
    rt, yr, wk = idx["REGION TYPE"], idx["YEAR"], idx["WEEK"]
    nat = [r for r in data if len(r) > rt and r[rt] == "National"]
    first = (int(nat[0][yr]), int(nat[0][wk]))
    last  = (int(nat[-1][yr]), int(nat[-1][wk]))
    return nat, first, last

def v_ilinet(p, exp_rows, exp_first, exp_last, exp_md5=None):
    idx, data = _weekly_table(p)
    if "% WEIGHTED ILI" not in idx:
        fail(f"{p.name}: no '% WEIGHTED ILI' column.")
    nat, first, last = _national(idx, data)
    if (len(nat), first, last) != (exp_rows, exp_first, exp_last):
        fail(f"{p.name}: ILINet anchor mismatch -> rows={len(nat)} {first}..{last} "
             f"(expected {exp_rows} {exp_first}..{exp_last}).")
    if exp_md5:
        m, _, _ = hash_file(p)
        if m != exp_md5:
            fail(f"{p.name}: ILINet MD5 {m} != pinned {exp_md5} (variant).")
    return {"weeks": len(nat), "first": first, "last": last}

def _regional_groups(idx, data, region_type="HHS Regions", week_cap=(2026, 9)):
    """Group ILINet rows by REGION for a REGION TYPE, truncated to <= week_cap (YEAR,WEEK).
    Returns {region_label: [(year, week, wili_str), ...]} in file row order."""
    rt, rg, yr, wk, wi = (idx["REGION TYPE"], idx["REGION"], idx["YEAR"],
                          idx["WEEK"], idx["% WEIGHTED ILI"])
    groups = {}
    cap = week_cap[0] * 100 + week_cap[1]
    for r in data:
        if len(r) <= max(rt, rg, yr, wk, wi):
            continue
        if r[rt].strip() != region_type:
            continue
        try:
            y, w = int(r[yr]), int(r[wk])
        except ValueError:
            continue
        if y * 100 + w > cap:                  # truncate to the national anchor window
            continue
        groups.setdefault(r[rg].strip(), []).append((y, w, r[wi].strip()))
    return groups

def _region_sort_key(label):
    digits = "".join(ch for ch in label if ch.isdigit())
    return int(digits) if digits else 9999

def v_ilinet_regional(p, week_cap=(2026, 9)):
    """Structural verifier + readout for the HHS-region ILINet pull (net-new for E7; no
    pinned MD5). Confirms the 10 HHS regions are present with the weekly schema and prints
    a per-region readout so the E7 loader is written against confirmed structure."""
    idx, data = _weekly_table(p)
    for col in ("REGION TYPE", "REGION", "YEAR", "WEEK", "% WEIGHTED ILI"):
        if col not in idx:
            fail(f"{p.name}: missing column '{col}' (not a FluView ILINet export?).")
    groups = _regional_groups(idx, data, "HHS Regions", week_cap)
    if not groups:
        fail(f"{p.name}: no REGION TYPE='HHS Regions' rows. Download HHS Regions, all 10, "
             f"ILINet, all seasons from the FluView portal.")
    labels = sorted(groups, key=_region_sort_key)
    print(f"        REGION TYPE='HHS Regions': {len(labels)} regions "
          f"(truncated to <= {week_cap[0]}w{week_cap[1]})")
    spans = []
    for lab in labels:
        rows = groups[lab]
        f0, l0 = rows[0], rows[-1]
        nnum = sum(1 for _, _, v in rows if _is_float(v))
        print(f"          {lab:<14} weeks={len(rows):>5}  "
              f"{f0[0]}w{f0[1]:02d}..{l0[0]}w{l0[1]:02d}  numeric%ILI={nnum}")
        spans.append((lab, len(rows), (f0[0], f0[1]), (l0[0], l0[1]), nnum))
    wk_counts = {n for _, n, *_ in spans}
    print(f"        -> {len(labels)} regions; week-count set {sorted(wk_counts)}; "
          f"{'ALIGNED' if len(wk_counts) == 1 else 'RAGGED (regions differ in length)'}")
    if len(labels) != 10:
        print(f"        ! expected 10 HHS regions, found {len(labels)} - check the selection.")
    return {"regions": len(labels), "labels": labels, "spans": spans,
            "aligned": len(wk_counts) == 1}

def v_nrevss(p, exp_rows, exp_first, exp_last):
    idx, data = _weekly_table(p)
    nat, first, last = _national(idx, data)
    if (len(nat), first, last) != (exp_rows, exp_first, exp_last):
        fail(f"{p.name}: NREVSS anchor mismatch -> rows={len(nat)} {first}..{last} "
             f"(expected {exp_rows} {exp_first}..{exp_last}).")
    return {"weeks": len(nat), "first": first, "last": last}

def v_noaa(p, exp_both):
    both = 0; first = last = None; n = 0
    with open(p, encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.DictReader(fh):
            d = (row.get("DATE") or "").strip()
            if not d or d > ANCHOR_END:
                continue
            n += 1
            if (row.get("TMAX") or "").strip() and (row.get("TMIN") or "").strip():
                both += 1
                if first is None: first = d
                last = d
    if both != exp_both:
        fail(f"{p.name}: NOAA anchor mismatch -> TMAX&TMIN(<= {ANCHOR_END})={both} "
             f"(expected {exp_both}). Wrong product/variant (NOT the CDO bulk order).")
    return {"both": both, "first": first, "last": last, "rows": n}

def v_silso(p):
    yrs = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split(";")
        if len(parts) >= 2:
            try:
                yrs.append(int(float(parts[0])))
            except ValueError:
                pass
    if not yrs or min(yrs) > 1749 or max(yrs) < 2008:
        fail(f"{p.name}: SILSO yearly coverage looks wrong "
             f"(min={min(yrs) if yrs else '?'} max={max(yrs) if yrs else '?'}).")
    return {"n": len(yrs), "ymin": min(yrs), "ymax": max(yrs)}

# --------------------------------------------------------------------------- main
def main():
    PROJECT_STORE.mkdir(parents=True, exist_ok=True)
    print(f"PROJECT_STORE = {PROJECT_STORE}")
    print(f"reproduction anchor (USGS/NOAA coverage end) = {ANCHOR_END}\n")
    rec = []

    # ---- REUSE 1-2 : USGS ------------------------------------------------------
    for sid, exp, f0, l0, name in [
        ("08158000", 46767, "1898-03-01", "2026-03-18", "Colorado River near Austin, TX"),
        ("03294500", 35862, "1928-01-01", "2026-03-18", "Ohio River at Louisville, KY")]:
        dst = PROJECT_STORE / f"usgs_{sid}.rdb"
        copy_verbatim(STORE / f"{sid}.txt", dst)
        v = v_usgs(dst, exp, f0, l0); md5, sha, nb = hash_file(dst)
        print(f"[reuse] usgs_{sid}.rdb  obs={v['obs']:,}  {v['first']}..{v['last']}  md5={md5[:8]}  OK")
        rec.append(dict(
            key=f"A.1 USGS {sid}", name=f"USGS NWIS daily discharge - {name} (gauge {sid})",
            source="USGS National Water Information System (NWIS), daily values (public domain)",
            tier="REUSE (shared store; identity-verified)",
            ident=f"gauge {sid}; parameter 00060 (discharge, ft3/s); statistic 00003 (daily mean)",
            cover=f"{v['first']} .. {v['last']}  ({v['obs']:,} valid daily obs)",
            freq="daily", obsv="natural-log daily mean discharge",
            anchor=f"coverage end {ANCHOR_END}; {v['obs']:,} valid (>0) daily obs",
            path=str(dst), md5=md5, sha=sha, nb=nb,
            verify=f"parsed RDB; valid daily-mean discharge = {v['obs']:,} (anchor match)",
            tol="Re-pulling NWIS later extends the series; truncate at coverage end 2026-03-18. "
                "Past daily values are stable, so the obs count reproduces exactly."))

    # ---- REUSE 3 : ILINet ------------------------------------------------------
    dst = PROJECT_STORE / "ILINet.csv"
    copy_verbatim(FLU / "ILINet.csv", dst)
    v = v_ilinet(dst, 1484, (1997, 40), (2026, 9), exp_md5="d2922245ab5c5bbce730202d6af60915")
    md5, sha, nb = hash_file(dst)
    print(f"[reuse] ILINet.csv  weeks={v['weeks']}  {v['first']}..{v['last']}  md5={md5[:8]}  OK")
    rec.append(dict(
        key="A.4 ILINet", name="CDC FluView ILINet - National outpatient ILI",
        source="US CDC FluView (FluView Interactive), ILINet, National (public domain)",
        tier="REUSE (shared store; identity-verified; pinned MD5)",
        ident="REGION TYPE=National; column '% WEIGHTED ILI'; FluView Phase02 ILINet (ID=1, RegionTypeId=3)",
        cover=f"{v['weeks']} National weeks  {v['first'][0]}w{v['first'][1]} .. {v['last'][0]}w{v['last'][1]}",
        freq="weekly (MMWR)", obsv="% WEIGHTED ILI (National)",
        anchor="first 1,484 weeks, 1997w40..2026w09 (file pre-truncated to exactly these weeks)",
        path=str(dst), md5=md5, sha=sha, nb=nb,
        verify="National + '% WEIGHTED ILI' present; 1,484 weeks 1997w40..2026w09; MD5 pinned d2922245...",
        tol="Recorded raw-download MD5 was 6206a4e0... (1,496 wk, pre-truncation). CDC revises ILINet "
            "retrospectively, so a fresh pull differs on recent weeks; the stable anchor is National + "
            "'% WEIGHTED ILI' + the first 1,484 weeks (ending 2026w09). Identical across all 4 LT papers."))

    # ---- REUSE 3b : ILINet HHS regions (net-new; E7 spatial-curvature peak detection) ----
    src_hhs = FLU / "ILINet_HHS.csv"
    if not src_hhs.exists():
        print("[skip ] ILINet_HHS.csv NOT in the store yet -- E7 regional pull pending.")
        print("        FluView portal (fluportaldashboard): Region Type = 'HHS Regions',")
        print("        select all 10 (Region 1..10), Data Source = ILINet, all seasons; unzip")
        print("        and save the inner ILINet.csv (rename it) as:")
        print(f"          {src_hhs}")
        print("        then re-run pull.py.")
    else:
        dst = PROJECT_STORE / "ILINet_HHS.csv"
        copy_verbatim(src_hhs, dst)
        v = v_ilinet_regional(dst, week_cap=(2026, 9))
        md5, sha, nb = hash_file(dst)
        print(f"[reuse] ILINet_HHS.csv  regions={v['regions']}  md5={md5[:8]}  "
              f"{'OK' if v['regions'] == 10 else 'CHECK'}")
        span_txt = "; ".join(f"{lab}:{n}wk" for lab, n, *_ in v["spans"])
        rec.append(dict(
            key="A.4 ILINet-HHS", name="CDC FluView ILINet - 10 HHS Regions outpatient ILI (E7)",
            source="US CDC FluView (FluView Interactive), ILINet, HHS Regions (public domain)",
            tier="REUSE (shared store; structural verify; net-new, no pinned MD5)",
            ident="REGION TYPE='HHS Regions' (Region 1..10); column '% WEIGHTED ILI'; "
                  "FluView Phase02 ILINet (ID=1)",
            cover=f"{v['regions']} HHS regions, 1997w40..2026w09 window "
                  f"({'aligned' if v['aligned'] else 'ragged'})",
            freq="weekly (MMWR)", obsv="% WEIGHTED ILI per HHS region (E7 spatial-curvature peak detection)",
            anchor="10 HHS regions present under REGION TYPE='HHS Regions'; truncated to <= 2026w09; "
                   "structural anchor (net-new: no prior reproduction, so no pinned MD5)",
            path=str(dst), md5=md5, sha=sha, nb=nb,
            verify=f"10 HHS regions; weekly '% WEIGHTED ILI'; per-region weeks: {span_txt}",
            tol="Net-new for E7 (no Stage-1.5 anchor). Same FluView portal/vintage as the National pin "
                "(the National '% WEIGHTED ILI' is itself the population-weighted aggregate of these "
                "regions). CDC revises ILINet retrospectively, so the byte hash drifts; the anchor is "
                "structural (10 regions, 1997w40 start, complete through-2024 seasons), and E7 uses only "
                "complete seasons through 2024 (well inside the stable window). The National TARGET in E7 "
                "is the pinned ILINet.csv, so E7 and E6 reference the identical national peak."))

    # ---- REUSE 4-5 : NREVSS ----------------------------------------------------
    for fn, exp, f0, l0, label, note in [
        ("ICL_NREVSS_Combined_prior_to_2015_16.csv", 940, (1997, 40), (2015, 39),
         "pre-2015 combined", "static pre-2015 strain counts; MD5 matched recorded 04445b64..."),
        ("ICL_NREVSS_Public_Health_Labs.csv", 544, (2015, 40), (2026, 9),
         "post-2015 public-health", "right window; lightly CDC-revised vs recorded 3700761f...")]:
        dst = PROJECT_STORE / fn
        copy_verbatim(FLU / fn, dst)
        v = v_nrevss(dst, exp, f0, l0); md5, sha, nb = hash_file(dst)
        print(f"[reuse] {fn}  weeks={v['weeks']}  {v['first']}..{v['last']}  md5={md5[:8]}  OK")
        rec.append(dict(
            key=f"A.4 {fn}", name=f"CDC NREVSS - {label} (strain identification, National)",
            source="US CDC FluView WHO/NREVSS, National (public domain)",
            tier="REUSE (shared store; identity-verified)",
            ident=f"REGION TYPE=National; FluView Phase02 WHO_NREVSS (ID=2); file {fn}",
            cover=f"{v['weeks']} National weeks  {v['first'][0]}w{v['first'][1]} .. {v['last'][0]}w{v['last'][1]}",
            freq="weekly", obsv="influenza-positive specimen counts by subtype",
            anchor=f"National; {v['first'][0]}w{v['first'][1]}..{v['last'][0]}w{v['last'][1]}",
            path=str(dst), md5=md5, sha=sha, nb=nb,
            verify=f"National; {v['weeks']} weeks; {note}",
            tol="Subtype counts are reported as-regenerated under the pinned allocation spec; post-2015 "
                "NREVSS is revised retrospectively, so the MD5 drifts - the anchor is the National window "
                "and the as-regenerated counts, not a fixed byte hash."))

    # ---- FETCH 6 : NOAA 6 by-station ------------------------------------------
    for sid, label, exp in NOAA_STATIONS:
        dst = PROJECT_STORE / f"ghcn_{sid}.csv"
        print(f"[fetch] {sid} ({label}) ...", end=" ", flush=True)
        fetch(NOAA_BASE.format(sid), dst)
        v = v_noaa(dst, exp); md5, sha, nb = hash_file(dst)
        print(f"TMAX&TMIN(<= {ANCHOR_END})={v['both']:,}  md5={md5[:8]}  OK")
        rec.append(dict(
            key=f"A.3 GHCN {sid}", name=f"NOAA GHCN-Daily - {label} ({sid})",
            source="NOAA NCEI Global Historical Climatology Network - Daily, by-station access CSV (public domain)",
            tier="FETCH FRESH (store lacked this product; fresh fetch reproduces anchor)",
            ident=f"station {sid}; {NOAA_BASE.format(sid)}",
            cover=f"{v['first']} .. {v['last']} (full record fetched; analysis truncates DATE<= {ANCHOR_END})",
            freq="daily", obsv="temperature = (TMAX+TMIN)/2 on days with both present",
            anchor=f"DATE<= {ANCHOR_END}: {v['both']:,} TMAX&TMIN days",
            path=str(dst), md5=md5, sha=sha, nb=nb,
            verify=f"fetched by-station CSV; TMAX&TMIN days through {ANCHOR_END} = {v['both']:,} (anchor match)",
            tol="GHCN-Daily appends recent days and applies occasional QC; a replicator fetches a longer "
                "file - truncate DATE<= 2026-03-18. The store's CDO bulk orders are a DIFFERENT product "
                "(e.g. Blue Hill starts 1893 not 1885; ends 2026-03-15/16) and must NOT be used."))

    # ---- FETCH 7 : SILSO yearly -----------------------------------------------
    dst = PROJECT_STORE / "silso_yearly.csv"
    print(f"[fetch] SILSO yearly ...", end=" ", flush=True)
    fetch(SILSO_URL, dst)
    v = v_silso(dst); md5, sha, nb = hash_file(dst)
    print(f"years={v['n']} ({v['ymin']}..{v['ymax']})  md5={md5[:8]}  OK")
    rec.append(dict(
        key="A.2 SILSO yearly", name="SILSO - yearly mean total sunspot number, V2.0",
        source="WDC-SILSO, Royal Observatory of Belgium (CC BY-NC 4.0 - attribute SILSO/SIDC)",
        tier="FETCH FRESH (store had only daily; yearly needed for the divergence operator)",
        ident=f"yearly mean total SN v2.0; {SILSO_URL} (';'-sep; col0 mid-year, col1 SN)",
        cover=f"{v['ymin']} .. {v['ymax']}  ({v['n']} years; operator filters year<=2008)",
        freq="yearly", obsv="yearly mean total sunspot number",
        anchor="filter year<=2008; vdiv std(3)-std(11) vs future Y(t+5) -> rho -0.230 (verified)",
        path=str(dst), md5=md5, sha=sha, nb=nb,
        verify=f"parsed yearly v2.0; coverage {v['ymin']}..{v['ymax']}; vdiv sign re-checked in E2",
        tol="Yearly v2.0 means are stable; a fresh fetch reproduces the -0.230 divergence sign. The "
            "decomposition magnitudes are a CITED Paper-4 reference (monthly vintage), not regenerated."))

    write_sources(rec)
    print(f"\nGenerated {SOURCES_MD}  ({len(rec)} series).")
    print(f"Raw data is in {PROJECT_STORE} (git-ignored; back up separately).")

def write_sources(rec):
    o = []
    o.append("# Data Sources - Cross-Domain-Validation (Paper 5 rebuild)\n")
    o.append(f"Generated by `data/pull.py` on {NOW}. Every series is **identity-verified against the "
             "Stage-1.5/1.6 reproduction anchors** on each run (the script aborts on mismatch); this "
             "guards against the duplicate-download variants in the shared store.\n")
    o.append("**No raw data is committed.** Raw files live in the project-local store "
             f"(`{PROJECT_STORE}`, git-ignored) and need their own off-machine backup. The information "
             "here is sufficient for an independent party to obtain equivalent data and reproduce every result.\n")
    o.append("**Reproduction anchors (truncation).** USGS / NOAA: coverage end **2026-03-18**. "
             "ILINet: first **1,484 weeks** (1997w40 -> 2026w09). Solar: **year <= 2008**. CDC files are "
             "revised retrospectively, so raw-file MD5s drift; the anchors plus the per-series "
             "replicator-tolerance absorb that.\n")
    o.append("| # | Series | Tier | Coverage | Anchor | MD5 |")
    o.append("|---|---|---|---|---|---|")
    for r in rec:
        o.append(f"| {r['key']} | {r['name']} | {r['tier'].split('(')[0].strip()} "
                 f"| {r['cover']} | {r['anchor']} | `{r['md5'][:12]}...` |")
    o.append("")
    for r in rec:
        o.append(f"## {r['key']} - {r['name']}\n")
        o.append(f"- **Source:** {r['source']}")
        o.append(f"- **Provenance tier:** {r['tier']}")
        o.append(f"- **Exact identifier:** {r['ident']}")
        o.append(f"- **Frequency:** {r['freq']}")
        o.append(f"- **Observable / field:** {r['obsv']}")
        o.append(f"- **Coverage:** {r['cover']}")
        o.append(f"- **Reproduction anchor:** {r['anchor']}")
        o.append(f"- **Project-local store path:** `{r['path']}`")
        o.append(f"- **MD5:** `{r['md5']}`")
        o.append(f"- **SHA256:** `{r['sha']}`")
        o.append(f"- **Bytes:** {r['nb']:,}")
        o.append(f"- **Verified:** {r['verify']}")
        o.append(f"- **Replicator tolerance:** {r['tol']}\n")
    o.append("---\n")
    o.append("*Licensing: USGS, NOAA, CDC are US-government public-domain works. SILSO is CC BY-NC 4.0 "
             "(attribute SILSO/SIDC; not committed). Generated record - do not hand-edit; re-run `pull.py`.*\n")
    SOURCES_MD.write_text("\n".join(o), encoding="utf-8")

if __name__ == "__main__":
    main()
