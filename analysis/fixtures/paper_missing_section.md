# Fixture: MISSING-SECTION paper (verify.py --selftest expects reconciliation to go RED)

## Methods

We apply the divergence operator D = SMA_4 - SMA_12 to weekly national % weighted
ILI on the continuous series, following the cited persistence-sign rule
(Kim 2026d \cite{kim2026d}). The required Results section has been removed from
this fixture on purpose, so the reconciliation must fail on the missing section.

Divergence onset leads the seasonal peak by 14.148 weeks on average (floor 5 wk);
this prose is present, but it is not under a Results header.
