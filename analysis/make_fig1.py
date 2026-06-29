#!/usr/bin/env python3
"""make_fig1.py - FIG-1, the ACF unification diagram for the Cross-Domain-Validation paper.

Overlays the deseasonalized ACFs of the Colorado, Ohio, and Dallas with the raw weekly influenza
ACF on a COMMON time-lag axis (days; influenza weekly lags shown x7). The figure makes the paper's
central claim visible: the divergence operator's sign, magnitude, deseasonalization response, and
failure modes in each domain are read off the same curve.

Regenerated WITHOUT the spurious 'CO 0-cross ~132d' annotation (DISC-1.4-04): the deseasonalized
Colorado ACF has no zero-crossing in this range, so none is drawn. The ONLY zero-crossing marked
is the genuine flu seasonal-ACF crossing (14 wk), which is what the Theorem-8b flu sign flip sits
near (distinct from h=26 wk).

Uses the committed operators (operators.acf_vals / first_zero_crossing) and hashed loaders
(data_io). Reads only the identity-verified store ($LT_CDV_DATA). Saves paper/figure1.png.

Run:  python analysis/make_fig1.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
from data_io import (load_usgs, log_discharge, load_ghcn_temp, load_ili,  # noqa: E402
                     deseason_month, deseason_doy, USGS, GHCN)
from operators import acf_vals, first_zero_crossing                       # noqa: E402

MAXLAG_D = 420            # days on the common axis
MAXLAG_FLU_W = 60        # flu weekly lags; x7 -> 420 days, matching the daily span


def _deseas_river(site):
    df = load_usgs(site)
    return deseason_month(log_discharge(df), df["date"].dt.month.to_numpy())


def _deseas_dallas():
    df = load_ghcn_temp(GHCN["Dallas_TX"])
    return deseason_doy(df["temp"].to_numpy(), df["date"].dt.dayofyear.to_numpy())


def main():
    co = acf_vals(_deseas_river(USGS["Colorado"]), MAXLAG_D)
    oh = acf_vals(_deseas_river(USGS["Ohio"]), MAXLAG_D)
    dal = acf_vals(_deseas_dallas(), MAXLAG_D)
    ili = load_ili()["w"].to_numpy()
    flu = acf_vals(ili, MAXLAG_FLU_W)
    flu_zc = first_zero_crossing(flu)          # expected 14 (weeks)

    lags_d = np.arange(MAXLAG_D + 1)
    lags_flu_d = np.arange(MAXLAG_FLU_W + 1) * 7

    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    ax.axhline(0, color="0.6", lw=0.8, zorder=1)
    ax.plot(lags_d, co, color="#1f77b4", lw=1.8, label="Colorado - deseas. log-discharge")
    ax.plot(lags_d, oh, color="#2ca02c", lw=1.8, label="Ohio - deseas. log-discharge")
    ax.plot(lags_d, dal, color="#ff7f0e", lw=1.6, label="Dallas - deseas. temp anomaly")
    ax.plot(lags_flu_d, flu, color="#d62728", lw=1.8, marker="o", ms=3,
            label="Influenza - raw weekly %ILI")

    # the ONE genuine zero-crossing drawn: the flu seasonal ACF (in weeks), placed on the day axis.
    # NO Colorado zero-crossing is annotated (DISC-1.4-04: the deseas. CO ACF does not cross zero
    # in this range; its Theorem-8b flip is R-near < R-far with the ACF still positive).
    if flu_zc is not None:
        ax.axvline(flu_zc * 7, color="#d62728", ls="--", lw=1.0, alpha=0.7, zorder=1)
        ax.annotate(f"flu ACF zero-crossing\n{flu_zc} wk",
                    xy=(flu_zc * 7, 0.0), xytext=(flu_zc * 7 + 16, 0.45),
                    color="#d62728", fontsize=8,
                    arrowprops=dict(arrowstyle="->", color="#d62728", lw=0.8))

    ax.set_xlim(0, MAXLAG_D)
    ax.set_xlabel("lag (days; influenza weekly lags shown x7)")
    ax.set_ylabel("autocorrelation")
    ax.set_title("FIG-1   The autocorrelation function is the unifying variable across domains")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()

    out = REPO / "paper" / "figure1.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"WROTE {out}")
    print("  ACF first zero-crossings (for the record; NOT all annotated):")
    print(f"    Colorado (daily, within {MAXLAG_D}d): {first_zero_crossing(co)}   "
          f"(expected None / no crossing - DISC-1.4-04)")
    print(f"    Ohio     (daily): {first_zero_crossing(oh)}")
    print(f"    Dallas   (daily): {first_zero_crossing(dal)}")
    print(f"    Flu      (weeks): {flu_zc}   (expected 14)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
